"""ACA literal vector and bounded unknown-key constraint controls."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest

from engine.reverse_engineer import Crib
from engine.solvers.interrupted_key import (
    interrupted_key_encrypt, interrupted_key_decrypt, interrupted_key_stream,
    solve_interrupted_key, infer_interrupted_key,
)

PLAIN = "THISCIPHERCANBEUSEDWITHANYOFTHEPERIODICS"
CIPHER = "HYIFQZPUKVQRBSEIJEQKZTVOBPOSZVSGSIICUIPY"
RUNS = (4, 6, 2, 3, 4, 3, 1, 1, 5, 1, 2, 3, 5)
KEY_STREAM = "ORANORANGEORORAORANORAOOORANGOORORAORANG"


class InterruptedKeyTest(unittest.TestCase):
    def test_literal_aca_diagram_and_published_recovery(self):
        self.assertEqual(interrupted_key_stream("ORANGE", RUNS), KEY_STREAM)
        self.assertEqual(interrupted_key_encrypt(PLAIN, "ORANGE", segment_lengths=RUNS), CIPHER)
        self.assertEqual(interrupted_key_decrypt("HYIFQ ZPUKV QRBSE IJEQK ZTVOB POSZ VSGSI ICUIP Y.", "ORANGE", segment_lengths=RUNS), PLAIN)
        result = solve_interrupted_key(CIPHER, keyword="ORANGE", segment_lengths=RUNS)
        self.assertEqual(result.plaintext, PLAIN)
        self.assertEqual(result.details["mode"], "supplied_key_and_reset_pattern")

    def test_independent_prefix_sum_oracle_repeated_key_letters(self):
        for keyword, lengths in (("A", (1, 1, 1)), ("ABA", (3, 1, 2, 3)), ("LEMON", (1, 2, 5, 3)), ("ABA", (5, 3))):
            plaintext = ("ABCDEFGHIJKLMNOPQRSTUVWXYZ" * 2)[:sum(lengths)]
            stream = "".join((keyword * ((count + len(keyword) - 1) // len(keyword)))[:count] for count in lengths)
            expected = "".join(chr(65 + ((ord(p) - 65) + (ord(k) - 65)) % 26) for p, k in zip(plaintext, stream))
            self.assertEqual(interrupted_key_encrypt(plaintext, keyword, segment_lengths=lengths), expected)
            self.assertEqual(interrupted_key_decrypt(expected, keyword, segment_lengths=lengths), plaintext)

    def test_unknown_key_recovers_from_short_crib_and_predicts_unseen_text(self):
        report = infer_interrupted_key(CIPHER, segment_lengths=RUNS, cribs=(Crib(4, "CIPHER"),))
        self.assertEqual(report.key, "ORANGE")
        self.assertEqual(report.predicted_plaintext, PLAIN)
        self.assertEqual(report.known_positions, 6)
        self.assertEqual(report.predicted_positions, 40)
        self.assertEqual(report.unresolved_parameters, 0)
        self.assertTrue(report.search_complete)
        self.assertEqual(report.checks, 6)
        self.assertTrue(report.re_encryption_matches)
        self.assertIsNone(report.claimed_plaintext)
        json.dumps(report.to_dict())

    def test_partial_key_slots_are_not_invented(self):
        report = infer_interrupted_key(CIPHER, segment_lengths=RUNS, cribs=(Crib(0, "THIS"),))
        self.assertEqual(report.key, "ORAN??")
        self.assertEqual(report.unresolved_parameters, 2)
        self.assertIn("?", report.predicted_plaintext)
        self.assertIsNone(report.re_encryption_matches)
        self.assertTrue(report.search_complete)
        self.assertFalse(report.unique_key_within_pattern)

    def test_explicit_length_supports_multiple_keyword_cycles_in_a_run(self):
        report = infer_interrupted_key("ACCDFFHH", segment_lengths=(5, 3), keyword_length=3,
                                      cribs=(Crib(0, "ABC"),))
        self.assertEqual(report.key, "ABA")
        self.assertEqual(report.predicted_plaintext, "ABCDEFGH")
        self.assertFalse(report.bounds["keyword_length_assumed_from_longest_run"])
        self.assertTrue(report.re_encryption_matches)

    def test_global_equation_budget_and_duplicate_cribs(self):
        for budget in (0, 1, 5, 6):
            report = infer_interrupted_key(CIPHER, segment_lengths=RUNS,
                                           cribs=(Crib(4, "CIPHER"), Crib(4, "CIPHER")), max_checks=budget)
            self.assertEqual(report.checks, budget)
            self.assertEqual(report.known_positions, 6)
            self.assertEqual(report.search_complete, budget == 6)
            self.assertEqual(report.unique_key_within_pattern, budget == 6)
        self.assertEqual(infer_interrupted_key(CIPHER, segment_lengths=RUNS,
                                              cribs=(Crib(4, "CIPHER"),), max_checks=0).key, "??????")

    def test_incompatible_crib_equations_reject_the_key_model(self):
        report = infer_interrupted_key(CIPHER, segment_lengths=RUNS, cribs=(Crib(0, "THIS"), Crib(4, "ZZ")))
        self.assertTrue(report.search_complete)
        self.assertFalse(report.compatible)
        self.assertEqual(report.predicted_plaintext, "")
        self.assertIsNone(report.re_encryption_matches)
        self.assertGreater(len(report.contradictions), 0)
        self.assertIsNone(report.claimed_plaintext)

    def test_strict_keyword_runs_coordinates_and_size_validation(self):
        for params in ({"keyword": ""}, {"keyword": "OR4NGE"}, {"keyword": "CAFÉ"},
                       {"keyword": "O" * 65, "segment_lengths": (40,)},
                       {"keyword": "ORANGE", "segment_lengths": (4, 4)},
                       {"keyword": "ORANGE", "segment_lengths": (5,) * 8},
                       {"keyword": "ORANGE", "segment_lengths": (True,) * 40},
                       {"keyword": "ORANGE", "segment_lengths": iter(RUNS)}):
            args = {"keyword": "ORANGE", "segment_lengths": RUNS, **params}
            with self.subTest(params=params), self.assertRaises((ValueError, TypeError)):
                interrupted_key_decrypt(CIPHER, **args)
        for cribs in ((), (Crib(-1, "A"),), (Crib(40, "A"),), (Crib(0, "A"), Crib(0, "B")), ((0, "A"),)):
            with self.assertRaises((ValueError, TypeError)):
                infer_interrupted_key(CIPHER, segment_lengths=RUNS, cribs=cribs)
        for budget in (-1, True, 4097):
            with self.assertRaises((ValueError, TypeError)):
                infer_interrupted_key(CIPHER, segment_lengths=RUNS, cribs=(Crib(4, "CIPHER"),), max_checks=budget)
        for length in (0, 65, True, 7):
            with self.assertRaises((ValueError, TypeError)):
                infer_interrupted_key(CIPHER, segment_lengths=RUNS, cribs=(Crib(4, "CIPHER"),), keyword_length=length)
        for text in ("", "CAFÉ", "1234", "A" * 4097, None):
            with self.assertRaises((ValueError, TypeError)):
                interrupted_key_decrypt(text, "ORANGE", segment_lengths=RUNS)

    def test_certificate_hashes_actual_no_key_inference(self):
        certificate = json.loads((Path(__file__).parents[1] / "engine/data/interrupted_key_certificate.json").read_text())
        report = infer_interrupted_key(certificate["ciphertext"], segment_lengths=certificate["segment_lengths"],
                                      cribs=tuple(Crib(c["offset"], c["plaintext"]) for c in certificate["cribs"]),
                                      **certificate["inference_parameters"])
        self.assertEqual(report.predicted_plaintext, PLAIN)
        self.assertEqual(hashlib.sha256(report.predicted_plaintext.encode("ascii")).hexdigest(), certificate["plaintext_sha256"])
        held_out = report.predicted_plaintext[:4] + report.predicted_plaintext[10:]
        self.assertEqual(hashlib.sha256(held_out.encode("ascii")).hexdigest(), certificate["held_out_plaintext_sha256"])
        self.assertNotIn("keyword", certificate["inference_parameters"])


if __name__ == "__main__":
    unittest.main()
