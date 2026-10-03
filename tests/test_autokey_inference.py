"""Blind autokey recovery, exact crib propagation, and training-only features."""
from __future__ import annotations

import hashlib
import json
import math
import random
import unittest
from pathlib import Path
from unittest.mock import patch

from engine.reverse_engineer import Crib
from engine.solvers.autokey_inference import infer_autokey, autokey_feature_scores

PLAIN = "THELIBRARIANOPENEDTHEQUIETREADINGROOMBEFORETHEFIRSTMORNINGTRAINARRIVEDSHEPLACEDTHERETURNEDBOOKSBESIDETHEWINDOWANDWROTEASHORTNOTEFORTHENEXTPERSONONDUTYOUTSIDETHEGLASSAGARDENERCARRIEDFRESHFLOWERSTHROUGHTHESQUARETHESCHOOLCHILDRENWOULDCOMEAFTERLUNCHTOREADABOUTDISTANTISLANDSANDTHEPEOPLEWHOHADSAILEDTHEREEVERYVISITORCOULDASKAQUESTIONANDTAKETIMETOTHINKABOUTTHEANSWERWHENTHERAINBEGANTHEOLDCLOCKSOUNDEDANDTHEROOMFELTWARMANDPEACEFUL"
CIPHER = "FVROIZKHVTIOFPVVEQHWIDYLXAVUULMGXVORUOKWCFQULJTZVLAQTZEAGSHINQAGKIIDRDJYMKPDULHISETIWNYRVHUIFXWEFGWNWULWELRWVAWVQZFKTRDOYCKXNGASWHEHAISSOMWIEWLGDRUMHLCHWMBBSNAWOOELZEMLRVWNKRTDVEMVFFIVALIQFAWYXEVNSLYAAYSMWBTYILXYSTLHVPUJPZRCGUEZXCHPKAYLIVSDPUSVLKZLRCKTPFYTGITHUGWQKEAAWASYDGKWPRRISILLCWLHOHWSEGLHMCIHOLVPZMNMKMMKGCERRUYUBXEKDIEHEFWBOXEGLFEDSMPURDOUVCGDHFOHLPLVWUWJXYAYEVGIIXAVGIIULQVSSQVVQFBFOVOHQWLHRBRFMICHKMWQLGZPVMCRIJP"


def independent_encrypt(plaintext, key):
    stream = key + plaintext
    return "".join(chr(65 + (ord(letter) + ord(stream[index]) - 130) % 26)
                   for index, letter in enumerate(plaintext))


def independent_feature_scores(ciphertext, english, digraph, maximum):
    cipher = [ord(ch) - 65 for ch in ciphertext]
    log_unigram = [math.log(value) for value in english]
    scores = []
    for period in range(1, maximum + 1):
        plaintext = [0] * len(cipher)
        for offset in range(period):
            trials = []
            for first in range(26):
                column = [first]
                for index in range(offset + period, len(cipher), period):
                    column.append((cipher[index] - column[-1]) % 26)
                trials.append(column)
            best = max(range(26), key=lambda seed: sum(log_unigram[v] for v in trials[seed]))
            for index, letter in zip(range(offset, len(cipher), period), trials[best]):
                plaintext[index] = letter
        scores.append(sum(digraph[a][b] for a, b in zip(plaintext, plaintext[1:])) / (len(cipher) - 1))
    return scores


class AutokeyInferenceTest(unittest.TestCase):
    def test_blind_synthetic_recovery_and_hash_certificate(self):
        report = infer_autokey(CIPHER, max_period=8)
        best = report.candidates[0]
        self.assertEqual(best.plaintext, PLAIN)
        self.assertEqual(best.key, "MONDAY")
        self.assertEqual(best.period, 6)
        self.assertEqual(independent_encrypt(best.plaintext, best.key), CIPHER)
        self.assertIsNone(report.claimed_plaintext)
        self.assertEqual(report.consensus_plaintext, "?" * len(CIPHER))
        self.assertFalse(report.ranking_exhaustive)
        certificate = json.loads((Path(__file__).resolve().parents[1] / "engine/data/autokey_inference_certificate.json").read_text())
        self.assertEqual(certificate["input_ciphertext"], CIPHER)
        self.assertEqual(hashlib.sha256(best.plaintext.encode("ascii")).hexdigest(), certificate["plaintext_sha256"])

    def test_primary_single_letter_primer_vector_uses_only_a_plaintext_crib(self):
        report = infer_autokey("EHPFS FEBHM HPF", max_period=1, cribs=[Crib(4, "O")])
        best = report.candidates[0]
        self.assertEqual(best.plaintext, "TOBEORNOTTOBE")
        self.assertEqual(best.key, "L")
        self.assertEqual(best.forced_plaintext, best.plaintext)
        self.assertEqual(report.consensus_plaintext, best.plaintext)
        self.assertTrue(report.plaintext_unique_within_period_bounds)
        self.assertIsNone(report.claimed_plaintext)

    def test_sparse_disjoint_cribs_force_all_columns_of_correct_period(self):
        report = infer_autokey(CIPHER, max_period=8,
                              cribs=[Crib(100, PLAIN[100:103]), Crib(313, PLAIN[313:316])])
        candidate = next(item for item in report.candidates if item.period == 6)
        self.assertEqual(candidate.plaintext, PLAIN)
        self.assertEqual(candidate.forced_plaintext, PLAIN)
        self.assertEqual(candidate.unresolved_seed_columns, 0)
        self.assertEqual(report.known_positions, 6)
        for item in report.candidates:
            self.assertEqual(independent_encrypt(item.plaintext, item.key), CIPHER)

    def test_contradictory_column_has_no_compatible_period(self):
        report = infer_autokey("EHPFSFEBHMHPF", max_period=1, cribs=[Crib(0, "TOA")])
        self.assertEqual(report.candidates, ())
        self.assertEqual(report.compatible_period_count, 0)
        self.assertTrue(report.constraint_space_complete)
        self.assertFalse(report.plaintext_unique_within_period_bounds)
        self.assertIsNone(report.claimed_plaintext)

    def test_one_retained_example_and_tied_language_weights_do_not_prove_uniqueness(self):
        report = infer_autokey("AAAAAAAA", max_period=1, max_candidates=1, log_unigram=[0.] * 26)
        self.assertEqual(report.candidates[0].key, "A")
        self.assertEqual(report.compatible_primer_count, 26)
        self.assertEqual(report.consensus_plaintext, "?" * 8)
        self.assertFalse(report.plaintext_unique_within_period_bounds)
        self.assertFalse(report.ranking_exhaustive)

    def test_random_constructed_crib_cases_match_independent_modular_algebra(self):
        draw = random.Random(731)
        for period in range(1, 13):
            plain = "".join(draw.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(96))
            key = "".join(draw.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(period))
            cipher = independent_encrypt(plain, key)
            report = infer_autokey(cipher, max_period=period,
                                  cribs=[Crib(period * 2, plain[period * 2:period * 3])])
            candidate = next(item for item in report.candidates if item.period == period)
            self.assertEqual((candidate.plaintext, candidate.key), (plain, key))
            self.assertEqual(candidate.forced_plaintext, plain)

    def test_invalid_input_bounds_types_and_cribs(self):
        for text, options in [(None, {}), ("ABC", {}), ("A" * 513, {}), ("A" * 8193, {}),
                              ("ABCDEFGſ", {}), ("ABCDEFGı", {}), ("ABCDEFGH", {"max_period": True}),
                              ("ABCDEFGH", {"max_period": 129}), ("ABCDEFGH", {"max_candidates": 0}),
                              ("ABCDEFGH", {"cribs": iter([Crib(0, "A")])}),
                              ("ABCDEFGH", {"cribs": [Crib(True, "A")]}),
                              ("ABCDEFGH", {"cribs": [Crib(7, "AB")]}),
                              ("ABCDEFGH", {"cribs": [Crib(0, "A"), Crib(0, "B")]}),
                              ("ABCDEFGH", {"log_unigram": [float("nan")] * 26}),
                              ("ABCDEFGH", {"log_unigram": [True] * 26}),
                              ("ABCDEFGH", {"log_unigram": [-1001.] * 26})]:
            with self.subTest(options=options), self.assertRaises((TypeError, ValueError)):
                infer_autokey(text, **options)

    def test_training_feature_numpy_and_stdlib_paths_match_independent_enumeration(self):
        english = [(index + 1) / 351 for index in range(26)]
        digraph = [[-((a * 7 + b * 11) % 31) / 10 for b in range(26)] for a in range(26)]
        expected = independent_feature_scores(CIPHER, english, digraph, 16)
        tables = {"english": english, "logdig": digraph}
        actual = autokey_feature_scores(CIPHER, tables)
        with patch("engine.solvers.autokey_inference._load_numpy", return_value=None):
            fallback = autokey_feature_scores(CIPHER, tables)
        for wanted, fast, pure in zip(expected, actual, fallback):
            self.assertAlmostEqual(fast, wanted, places=12)
            self.assertAlmostEqual(pure, wanted, places=12)
        self.assertEqual(len(actual), 16)

    def test_training_feature_rejects_invalid_tables_and_sizes(self):
        valid = {"english": [1 / 26] * 26, "logdig": [[-1.] * 26 for _ in range(26)]}
        for text, tables, period in [("A" * 8193, valid, 16), ("ABC", valid, 16),
                                     ("A" * 16, valid, 17), ("A" * 16, {}, 16),
                                     ("A" * 16, {**valid, "english": [0.] * 26}, 16),
                                     ("A" * 16, {**valid, "logdig": [[float("inf")] * 26] * 26}, 16)]:
            with self.assertRaises((TypeError, ValueError)):
                autokey_feature_scores(text, tables, max_period=period)


if __name__ == "__main__":
    unittest.main()
