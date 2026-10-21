"""Exact delta mathematics, bounded search and independent recovery controls."""
from __future__ import annotations

import math
import random
import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from engine.alphabet import letters_only
from engine.fixtures import SUBSTITUTION_PLAIN, SUBSTITUTION_KEY
from engine.language import get_model
from engine.solvers.substitution_parallel_tempering import (
    QuadgramSwapState, exchange_log_ratio, solve_substitution_parallel_tempering,
)


SHORT_PLAIN = 'THEMANENTEREDTHEROOMANDTHENTHEOTHERMENCAMETOMEETHIMTHEREINTHEMORNINGTHEYWEREALLREADYAND'
SHORT_CIPHER = 'CEIOPFIFCIKIGCEIKDDOPFGCEIFCEIDCEIKOIFQPOICDOIICEAOCEIKIAFCEIODKFAFMCEIWTIKIPNNKIPGWPFG'
COURIER_PLAIN = 'THECOURIERPLACEDTHEPARCELBESIDETHEGATEANDWAITEDUNDERTHEPORCHUNTILTHEHEAVYRAINHADSTOPPED'
COURIER_CIPHER = 'CEIQDVKAIKXNPQIGCEIXPKQINHIRAGICEIMPCIPFGTPACIGVFGIKCEIXDKQEVFCANCEIEIPSWKPAFEPGRCDXXIG'


def oracle_encrypt(plain, key):
    return ''.join(key[ord(ch) - 65] for ch in plain)


def oracle_score(seq, key, table):
    plain = [key[c] for c in seq]
    return sum(table[sum(plain[i + j] * 26 ** (3 - j) for j in range(4))]
               for i in range(len(plain) - 3))


class DeltaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.table = get_model().logp

    def test_every_pair_delta_matches_independent_full_score(self):
        seq = [ord(c) - 65 for c in 'AAAABACADABAEDDCAFABACABADAAAABAAA']
        key = list(range(26))
        random.Random(7).shuffle(key)
        state = QuadgramSwapState(seq, key, self.table)
        initial = oracle_score(seq, key, self.table)
        for a in range(25):
            for b in range(a + 1, 26):
                swapped = key[:]
                swapped[a], swapped[b] = swapped[b], swapped[a]
                expected = oracle_score(seq, swapped, self.table) - initial
                self.assertAlmostEqual(state.delta(a, b), expected, places=10)
        self.assertEqual(state.key, key)

    def test_committed_random_swaps_and_inverse_restore_exact_state(self):
        seq = [ord(c) - 65 for c in letters_only(SUBSTITUTION_PLAIN)]
        state = QuadgramSwapState(seq, list(range(26)), self.table)
        rng = random.Random(171)
        for _ in range(250):
            a, b = rng.sample(range(26), 2)
            change = state.delta(a, b)
            state.commit(a, b, change)
            self.assertAlmostEqual(state.score, oracle_score(seq, state.key, self.table), places=8)
        before = (state.key[:], state.indices[:], state.score)
        state.commit(0, 25, state.delta(0, 25))
        state.commit(0, 25, state.delta(0, 25))
        self.assertEqual(state.key, before[0])
        self.assertEqual(state.indices, before[1])
        self.assertAlmostEqual(state.score, before[2], places=9)

    def test_delta_handles_absent_letters_and_repeated_window_symbols(self):
        state = QuadgramSwapState([0] * 8, list(range(26)), self.table)
        self.assertEqual(state.delta(24, 25), 0)
        change = state.delta(0, 1)
        state.commit(0, 1, change)
        self.assertAlmostEqual(state.score, 5 * self.table[17576 + 676 + 26 + 1])

    def test_state_rejects_non_bijective_or_bad_symbols(self):
        for key in ([0] * 26, list(range(25)), [True] + list(range(1, 26))):
            with self.assertRaises(ValueError):
                QuadgramSwapState([0, 1, 2, 3], key, self.table)
        with self.assertRaises(ValueError):
            QuadgramSwapState([0, 1, -1, 3], list(range(26)), self.table)

    def test_exchange_sign_and_equal_temperature_boundary(self):
        self.assertEqual(exchange_log_ratio(-20, -10, 1, 2), 5)
        self.assertEqual(exchange_log_ratio(-10, -20, 1, 2), -5)
        self.assertEqual(exchange_log_ratio(-10, -20, 2, 2), 0)
        self.assertEqual(exchange_log_ratio(-10, -10, 1, 2), 0)


class SearchTests(unittest.TestCase):
    def test_hidden_key_short_literal_recovery_and_independent_forward_check(self):
        self.assertEqual(oracle_encrypt(SHORT_PLAIN, 'PHQGIUMEAYLNOFDXJKRCVSTZWB'), SHORT_CIPHER)
        result = solve_substitution_parallel_tempering(
            SHORT_CIPHER, seed=1729, restarts=4, sweeps=5000,
            max_proposals=180000, timeout_seconds=20,
        )
        self.assertEqual(letters_only(result.plaintext), SHORT_PLAIN)
        self.assertEqual(oracle_encrypt(SHORT_PLAIN, result.key), SHORT_CIPHER)
        self.assertIsNone(result.details['claimed_plaintext'])
        self.assertFalse(result.details['exhaustive_key_search'])
        certificate = json.loads((Path(__file__).resolve().parents[1] /
            'engine/data/substitution_parallel_tempering_certificate.json').read_text())
        self.assertEqual(certificate['ciphertext'], SHORT_CIPHER)
        self.assertEqual(certificate['plaintext'], SHORT_PLAIN)
        self.assertEqual(hashlib.sha256(letters_only(result.plaintext).encode('ascii')).hexdigest(),
                         certificate['recovered_plaintext_sha256'])
        self.assertFalse(certificate['key_supplied'])
        self.assertFalse(certificate['cribs_supplied'])

    def test_repository_fixture_unknown_key_recovery(self):
        plain = letters_only(SUBSTITUTION_PLAIN)
        cipher = oracle_encrypt(plain, SUBSTITUTION_KEY)
        result = solve_substitution_parallel_tempering(
            cipher, seed=20261003, restarts=2, sweeps=3500,
            max_proposals=65000, timeout_seconds=20,
        )
        self.assertEqual(letters_only(result.plaintext), plain)
        self.assertEqual(result.key, SUBSTITUTION_KEY)

    def test_wrong_short_candidate_can_outscore_independent_ground_truth(self):
        result = solve_substitution_parallel_tempering(
            COURIER_CIPHER, seed=1729, restarts=4, sweeps=5000,
            max_proposals=180000, timeout_seconds=20,
        )
        expected_score = get_model().score([ord(c) - 65 for c in COURIER_PLAIN])
        self.assertNotEqual(letters_only(result.plaintext), COURIER_PLAIN)
        self.assertGreater(result.score, expected_score)
        self.assertEqual(oracle_encrypt(letters_only(result.plaintext), result.key), COURIER_CIPHER)
        self.assertIsNone(result.details['claimed_plaintext'])

    def test_supplied_score_table_is_used_and_invalid_tables_rejected(self):
        flat = [0.0] * 26 ** 4
        result = solve_substitution_parallel_tempering(
            SHORT_CIPHER, sweeps=2, restarts=1, max_proposals=16, polish_passes=0, logp=flat,
        )
        self.assertEqual(result.score, 0.0)
        self.assertTrue(result.details['supplied_score_table'])
        self.assertEqual(result.details['proposals'], 16)
        self.assertFalse(any(flat))
        for table in ([0.0], [math.inf] * 26 ** 4, [1e308] * 26 ** 4, [True] * 26 ** 4):
            with self.assertRaises(ValueError):
                solve_substitution_parallel_tempering(SHORT_CIPHER, logp=table)

    def test_proposal_cap_includes_polish_and_partial_search_is_not_complete(self):
        result = solve_substitution_parallel_tempering(
            SHORT_CIPHER, max_proposals=17, sweeps=5000, polish_passes=16,
        )
        self.assertEqual(result.details['proposals'], 17)
        self.assertEqual(result.details['stop_reason'], 'proposal_limit')
        self.assertFalse(result.details['configured_search_complete'])
        self.assertLessEqual(len(result.details['candidates']), 10)
        self.assertEqual(oracle_encrypt(letters_only(result.plaintext), result.key), SHORT_CIPHER)

    def test_seed_reproduces_candidates_counts_and_keeps_case_and_punctuation(self):
        kwargs = dict(seed=98, sweeps=10, restarts=2, max_proposals=500, polish_passes=0)
        first = solve_substitution_parallel_tempering(SHORT_CIPHER.lower() + '!?', **kwargs)
        second = solve_substitution_parallel_tempering(SHORT_CIPHER.lower() + '!?', **kwargs)
        self.assertEqual((first.plaintext, first.key, first.score), (second.plaintext, second.key, second.score))
        self.assertEqual(first.details['candidates'], second.details['candidates'])
        self.assertEqual(first.details['proposals'], 160)
        self.assertTrue(first.plaintext.endswith('!?'))
        self.assertTrue(first.plaintext[:-2].islower())

    def test_exchange_events_and_distinct_bounded_candidates(self):
        result = solve_substitution_parallel_tempering(
            SHORT_CIPHER, sweeps=12, restarts=3, exchange_interval=2,
            max_proposals=1000, max_candidates=2, polish_passes=0,
        )
        self.assertGreater(result.details['exchange_attempts'], 0)
        self.assertGreaterEqual(result.details['exchange_accepted'], 0)
        candidates = result.details['candidates']
        self.assertLessEqual(len(candidates), 2)
        self.assertEqual(len({c['plaintext'] for c in candidates}), len(candidates))
        self.assertTrue(result.details['configured_search_complete'])
        self.assertEqual(result.details['stop_reason'], 'configured_work_completed')

    def test_timeout_is_reported_without_claiming_search_completeness(self):
        with patch('engine.solvers.substitution_parallel_tempering.time.perf_counter', side_effect=[0, 0, 2, 2, 2, 2]):
            result = solve_substitution_parallel_tempering(SHORT_CIPHER, timeout_seconds=1)
        self.assertEqual(result.details['stop_reason'], 'time_limit')
        self.assertFalse(result.details['configured_search_complete'])

    def test_invalid_bounds_and_text(self):
        for kwargs in ({'seed': True}, {'restarts': 0}, {'sweeps': -1}, {'max_proposals': True},
                       {'max_proposals': 50000001}, {'temperatures': (1, 1)},
                       {'temperatures': (1, math.nan)}, {'temperatures': (.1,)},
                       {'temperatures': (True, 2)}, {'timeout_seconds': math.inf},
                       {'exchange_interval': 0}, {'polish_passes': 33}, {'max_candidates': 0}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                solve_substitution_parallel_tempering(SHORT_CIPHER, **kwargs)
        for text in ('A' * 39, 'A' * 4097, 'é' * 100, 1):
            with self.subTest(text_type=type(text)), self.assertRaises(ValueError):
                solve_substitution_parallel_tempering(text)


if __name__ == '__main__':
    unittest.main()
