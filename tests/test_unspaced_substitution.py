"""Blind known answers, independent exhaustive oracles and strict search bounds."""

import hashlib
from itertools import permutations
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import engine.solvers.unspaced_substitution as solver


class UnspacedSubstitutionTests(unittest.TestCase):
    def test_certificate_recovers_87_letters_and_unknown_boundaries_without_key(self):
        certificate = json.loads((Path(__file__).parents[1] / 'engine/data/unspaced_substitution_certificate.json').read_text())
        vector = certificate['vectors'][0]
        self.assertEqual(len(vector['ciphertext']), 87)
        self.assertFalse(vector['key_supplied_to_solver'])
        self.assertFalse(vector['word_boundaries_supplied_to_solver'])
        report = solver.infer_unspaced_substitution(vector['ciphertext'], lexicon=vector['lexicon'],
                                                   max_nodes=100000, max_candidates=100)
        self.assertTrue(report['search_complete'])
        self.assertTrue(report['unique_plaintext_within_lexicon'])
        self.assertTrue(report['unique_segmentation_within_lexicon'])
        recovered = report['candidates'][0]
        self.assertEqual(recovered['plaintext_letters'], vector['expected_plaintext'])
        self.assertEqual(recovered['words'], vector['expected_words'])
        self.assertEqual(hashlib.sha256(recovered['plaintext_letters'].encode('ascii')).hexdigest(),
                         vector['plaintext_sha256'])
        # This independently checks the frozen control encoder, not a solver parameter.
        self.assertEqual(''.join(chr(65 + (5 * (ord(c) - 65) + 8) % 26)
                                 for c in recovered['plaintext_letters']), vector['ciphertext'])
        self.assertEqual(report['nodes'], vector['nodes'])

    def test_blind_literal_cipher_recovers_unknown_words_and_observed_key(self):
        ciphertext = 'ZRCSWFRCPGCCFULCZZCPUSAVUWUZCVZ'
        expected = 'THECIPHERKEEPSLETTERSCONSISTENT'
        vocabulary = ['THE', 'CIPHER', 'KEEPS', 'LETTERS', 'CONSISTENT', 'OTHER',
                      'PEERS', 'KEEP', 'SENT', 'LINE', 'REST', 'THERE']
        # Independent encoder verifies the literal, but its key never enters inference.
        enc = {chr(65 + i): chr(65 + (5 * i + 8) % 26) for i in range(26)}
        self.assertEqual(''.join(enc[ch] for ch in expected), ciphertext)
        report = solver.infer_unspaced_substitution(ciphertext, lexicon=vocabulary,
            max_nodes=100000, max_candidates=100)
        self.assertTrue(report['search_complete'])
        answers = [candidate for candidate in report['candidates'] if candidate['plaintext_letters'] == expected]
        self.assertTrue(answers)
        candidate = answers[0]
        self.assertEqual(candidate['words'], ['THE', 'CIPHER', 'KEEPS', 'LETTERS', 'CONSISTENT'])
        inverse = {plain: cipher for cipher, plain in candidate['cipher_to_plain'].items()}
        self.assertEqual(''.join(inverse[plain] for plain in candidate['plaintext_letters']), ciphertext)
        for cipher, plain in candidate['cipher_to_plain'].items():
            self.assertEqual(enc[plain], cipher)
        self.assertTrue(candidate['forward_consistent'])
        self.assertEqual(candidate['plaintext_sha256'], hashlib.sha256(expected.encode()).hexdigest())
        self.assertIsNone(report['claimed_plaintext'])
        self.assertFalse(report['correctness_known'])

    def test_global_bijection_rejects_inconsistent_repetitions_and_collisions(self):
        for ciphertext in ('ABCA', 'ABAC'):
            report = solver.infer_unspaced_substitution(ciphertext, lexicon=['NOON'])
            self.assertTrue(report['search_complete'])
            self.assertEqual(report['solutions_found'], 0)
            self.assertEqual(report['model_status'], 'unsat')
            self.assertFalse(report['unique_plaintext_within_lexicon'])

    def test_same_plaintext_has_two_distinct_word_boundary_hypotheses(self):
        report = solver.infer_unspaced_substitution('ZRCPIFWUZ', lexicon=['THE', 'RAPIST', 'THERAPIST'])
        self.assertTrue(report['search_complete'])
        self.assertEqual(report['plaintexts_found'], 1)
        self.assertEqual(report['segmentations_found'], 2)
        self.assertTrue(report['unique_plaintext_within_lexicon'])
        self.assertFalse(report['unique_segmentation_within_lexicon'])
        self.assertEqual(report['forced_plaintext'], 'THERAPIST')
        self.assertEqual({tuple(c['word_boundaries']) for c in report['candidates']}, {(9,), (3, 9)})

    def test_distinct_plaintexts_can_share_one_forced_boundary_pattern(self):
        report = solver.infer_unspaced_substitution('ABBA', lexicon=['NOON', 'DEED'])
        self.assertTrue(report['search_complete'])
        self.assertEqual(report['plaintexts_found'], 2)
        self.assertEqual(report['solutions_found'], 2)
        self.assertEqual(report['segmentations_found'], 1)
        self.assertTrue(report['ambiguous_plaintext'])
        self.assertFalse(report['ambiguous_boundaries'])
        self.assertTrue(report['unique_segmentation_within_lexicon'])
        self.assertFalse(report['unique_plaintext_within_lexicon'])

    def test_complete_search_matches_independent_mapping_and_partition_oracle(self):
        ciphertext = 'ABBA'
        vocabulary = {'A', 'B', 'AA', 'AB', 'BA', 'BB', 'ABBA'}

        def partitions(text, position=0, boundaries=()):
            if position == len(text):
                yield boundaries
            for end in range(position + 1, len(text) + 1):
                if text[position:end] in vocabulary:
                    yield from partitions(text, end, boundaries + (end,))

        expected = set()
        for assignment in permutations('AB'):
            mapping = dict(zip('AB', assignment))
            text = ''.join(mapping[ch] for ch in ciphertext)
            expected.update((text, boundaries) for boundaries in partitions(text))
        report = solver.infer_unspaced_substitution(ciphertext, lexicon=vocabulary,
            max_nodes=10000, max_candidates=100)
        actual = {(c['plaintext_letters'], tuple(c['word_boundaries'])) for c in report['candidates']}
        self.assertTrue(report['search_complete'])
        self.assertEqual(actual, expected)
        self.assertEqual(report['solutions_found'], len(expected))
        self.assertEqual(report['plaintexts_found'], 2)
        self.assertEqual(report['forced_plaintext'], '????')
        self.assertTrue(report['ambiguous_plaintext'])

    def test_node_state_and_candidate_budgets_never_assert_exhaustion_or_uniqueness(self):
        words = ['NOON', 'DEED', 'ABBA']
        node = solver.infer_unspaced_substitution('ABBA', lexicon=words, max_nodes=1)
        self.assertEqual(node['nodes'], 1)
        self.assertEqual(node['stop_reason'], 'node_limit')
        self.assertFalse(node['search_complete'])
        self.assertEqual(node['forced_plaintext'], '????')
        state = solver.infer_unspaced_substitution('ABBA', lexicon=words, max_states=1)
        self.assertEqual(state['stop_reason'], 'state_limit')
        self.assertFalse(state['search_complete'])
        self.assertLessEqual(state['peak_states'], 1)
        candidate = solver.infer_unspaced_substitution('ABBA', lexicon=words, max_candidates=1)
        self.assertEqual(candidate['stop_reason'], 'candidate_limit')
        self.assertFalse(candidate['search_complete'])
        self.assertEqual(len(candidate['candidates']), 1)
        self.assertEqual(candidate['solutions_found'], 2)
        self.assertFalse(candidate['unique_plaintext_within_lexicon'])
        self.assertTrue(candidate['ambiguous_plaintext'])

    def test_exact_last_node_budget_can_prove_declared_dictionary_completion(self):
        full = solver.infer_unspaced_substitution('ABBA', lexicon=['NOON'])
        exact = solver.infer_unspaced_substitution('ABBA', lexicon=['NOON'], max_nodes=full['nodes'])
        short = solver.infer_unspaced_substitution('ABBA', lexicon=['NOON'], max_nodes=full['nodes'] - 1)
        self.assertTrue(exact['search_complete'])
        self.assertEqual(exact['candidates'], full['candidates'])
        self.assertFalse(short['search_complete'])
        self.assertFalse(short['unique_plaintext_within_lexicon'])
        self.assertEqual(short['forced_plaintext'], '????')

    def test_timeout_is_unknown_and_does_not_turn_missing_candidates_into_unsat(self):
        moments = iter([0., 1., 1.])
        with patch.object(solver.time, 'monotonic', side_effect=lambda: next(moments, 1.)):
            report = solver.infer_unspaced_substitution('ABBA', lexicon=['NOON'], timeout_seconds=.01)
        self.assertEqual(report['nodes'], 0)
        self.assertEqual(report['model_status'], 'unknown')
        self.assertEqual(report['stop_reason'], 'timeout')
        self.assertIsNone(report['ambiguous_plaintext'])
        self.assertEqual(report['forced_plaintext'], '????')

    def test_validation_bounded_iterable_and_effective_empty_dictionary(self):
        for text in ('', 'ABC', 'AB!C', 'ABßC', 'ABéC', 'A' * 513):
            with self.subTest(text=text), self.assertRaises(ValueError):
                solver.infer_unspaced_substitution(text, lexicon=['NOON'])
        with self.assertRaises(TypeError):
            solver.infer_unspaced_substitution(None, lexicon=['NOON'])
        for lexicon in ('NOON', b'NOON', {'NOON': 1}, 7):
            with self.subTest(lexicon=lexicon), self.assertRaises(TypeError):
                solver.infer_unspaced_substitution('ABBA', lexicon=lexicon)
        for lexicon in ([], ['NO ON'], ['NOON!'], ['NÖÖN'], [True]):
            with self.subTest(lexicon=lexicon), self.assertRaises((TypeError, ValueError)):
                solver.infer_unspaced_substitution('ABBA', lexicon=lexicon)
        for options in ({'max_nodes': 0}, {'max_nodes': True}, {'max_nodes': 1000001},
                        {'max_states': 16385}, {'max_candidates': 101}, {'min_word_length': 0},
                        {'min_word_length': 5, 'max_word_length': 4}, {'max_word_length': 65},
                        {'max_lexicon_entries': 50001}, {'timeout_seconds': float('nan')},
                        {'timeout_seconds': True}, {'timeout_seconds': 121.}):
            with self.subTest(options=options), self.assertRaises(ValueError):
                solver.infer_unspaced_substitution('ABBA', lexicon=['NOON'], **options)
        consumed = []

        def forever():
            while True:
                consumed.append(1)
                yield 'NOON'

        with self.assertRaises(ValueError):
            solver.infer_unspaced_substitution('ABBA', lexicon=forever(), max_lexicon_entries=3)
        self.assertEqual(len(consumed), 4)
        empty = solver.infer_unspaced_substitution('ABBA', lexicon=['NOON'], min_word_length=5)
        self.assertEqual(empty['nodes'], 0)
        self.assertTrue(empty['search_complete'])
        self.assertEqual(empty['model_status'], 'unsat')
        self.assertEqual(empty['effective_dictionary_size'], 0)
        normalized = solver.infer_unspaced_substitution('ab ba\n', lexicon=['noon', 'NOON'])
        self.assertEqual(normalized['normalized_ciphertext'], 'ABBA')
        self.assertEqual(normalized['dictionary_size'], 1)
        self.assertEqual(normalized['raw_input_sha256'], hashlib.sha256(b'ab ba\n').hexdigest())


if __name__ == '__main__':
    unittest.main()
