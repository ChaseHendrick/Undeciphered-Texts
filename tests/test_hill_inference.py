"""Aligned-crib Hill recovery against independent literal and algebra controls."""

from __future__ import annotations

import hashlib
from itertools import product
import json
from math import gcd
from pathlib import Path
import unittest

from engine.reverse_engineer import Crib
from engine.solvers.hill_inference import infer_hill

PLAIN = "HELPTHESMALLBOATSLEFTATDAWNX"
CIPHER = "DRPAHAQIGCJIPJWBGHQVDBBIUIPG"
CERT = Path(__file__).resolve().parents[1] / "engine/data/hill_inference_certificate.json"


class HillInferenceTest(unittest.TestCase):
    def test_published_vector_recovers_key_from_crib_without_supplied_matrix(self):
        report = infer_hill("HIAT", cribs=(Crib(0, "HELP"),))
        self.assertTrue(report["search_complete"])
        self.assertEqual(report["compatible_key_count"], 1)
        self.assertTrue(report["key_unique_within_model"])
        self.assertEqual(report["candidates"][0]["matrix"], [[3, 3], [2, 5]])
        self.assertEqual(report["candidates"][0]["inverse_matrix"], [[15, 17], [20, 9]])
        self.assertEqual(report["candidates"][0]["plaintext"], "HELP")
        self.assertEqual(report["consensus_plaintext"], "HELP")
        self.assertEqual(report["checks"], 1353)
        self.assertIsNone(report["claimed_plaintext"])

    def test_odd_aligned_crib_predicts_unprovided_suffix_and_preserves_x(self):
        report = infer_hill(CIPHER, cribs=(Crib(1, "ELPTHES"),))
        self.assertTrue(report["search_complete"])
        self.assertEqual(report["compatible_key_count"], 1)
        recovered = report["candidates"][0]
        self.assertEqual(recovered["plaintext"], PLAIN)
        self.assertEqual(recovered["matrix"], [[7, 8], [11, 11]])
        self.assertTrue(recovered["forward_consistent"])
        self.assertTrue(recovered["crib_match"])
        self.assertEqual(report["consensus_plaintext"], PLAIN)
        json.dumps(report, allow_nan=False)

    def test_complete_sparse_crib_count_and_consensus_match_full_matrix_oracle(self):
        # Enumerate encryption matrices directly, unlike the solver's two inverse-row search.
        count, consensus = 0, None
        ciphertext = (7, 8, 0, 19)
        for a, b, c, d in product(range(26), repeat=4):
            determinant = (a * d - b * c) % 26
            if gcd(determinant, 26) != 1:
                continue
            inverse = pow(determinant, -1, 26)
            values = tuple(v % 26 for i in (0, 2) for v in
                           (inverse * (d * ciphertext[i] - b * ciphertext[i + 1]),
                            inverse * (-c * ciphertext[i] + a * ciphertext[i + 1])))
            if values[1:3] != (4, 11):
                continue
            plain = "".join(chr(65 + v) for v in values)
            count += 1
            consensus = (list(plain) if consensus is None else
                         [old if old == new else "?" for old, new in zip(consensus, plain)])
        report = infer_hill("HIAT", cribs=(Crib(1, "EL"),), max_candidates=2)
        self.assertTrue(report["search_complete"])
        self.assertEqual(report["compatible_key_count"], count)
        self.assertGreater(count, 2)
        self.assertEqual(report["consensus_plaintext"], "".join(consensus))
        self.assertFalse(report["key_unique_within_model"])
        self.assertFalse(report["plaintext_unique_within_model"])
        self.assertEqual(len(report["candidates"]), 2)
        self.assertTrue(report["candidates_truncated"])

    def test_budget_never_promotes_prefix_to_global_consensus_or_uniqueness(self):
        for budget in (0, 1, 675, 676, 1351, 1352, 1353):
            report = infer_hill("HIAT", cribs=(Crib(0, "HELP"),), max_checks=budget)
            self.assertLessEqual(report["checks"], budget)
            self.assertEqual(report["checks"], sum(report["row_checks"]) + report["key_pair_checks"])
            self.assertEqual(report["search_complete"], budget >= 1353)
            if budget < 1353:
                self.assertIsNone(report["compatible_key_count"])
                self.assertIsNone(report["consensus_plaintext"])
                self.assertIsNone(report["key_unique_within_model"])
                self.assertIsNone(report["plaintext_unique_within_model"])
        weak = infer_hill("AAAA", cribs=(Crib(0, "A"),), max_checks=2100, max_candidates=3)
        self.assertFalse(weak["search_complete"])
        self.assertGreater(weak["compatible_keys_seen"], 0)
        self.assertIsNone(weak["consensus_plaintext"])
        self.assertLessEqual(len(weak["candidates"]), 3)

    def test_impossible_rows_are_a_scoped_empty_complete_search(self):
        report = infer_hill("AAAA", cribs=(Crib(0, "B"),))
        self.assertTrue(report["search_complete"])
        self.assertEqual(report["compatible_key_count"], 0)
        self.assertEqual(report["candidates"], [])
        self.assertIsNone(report["consensus_plaintext"])
        self.assertFalse(report["key_unique_within_model"])
        self.assertFalse(report["plaintext_unique_within_model"])
        self.assertIsNone(report["claimed_plaintext"])

    def test_strict_inputs_require_cribs_even_blocks_and_finite_limits(self):
        for text in (None, 123, "ABC", "ABCDE", "A" * 514, "α" * 4, "AB12CD"):
            with self.subTest(text=str(text)[:20]), self.assertRaises((TypeError, ValueError)):
                infer_hill(text, cribs=(Crib(0, "A"),))
        for options in ({"cribs": ()}, {"cribs": "HELP"}, {"cribs": (Crib(3, "LP"),)},
                        {"cribs": (Crib(0, "HE"), Crib(1, "XX"))},
                        {"cribs": (Crib(True, "H"),)}, {"cribs": (Crib(0, "H1"),)},
                        {"max_checks": True}, {"max_checks": -1}, {"max_checks": 100001},
                        {"max_candidates": 0}, {"max_candidates": 101}):
            parameters = {"cribs": (Crib(0, "HELP"),), **options}
            with self.subTest(options=options), self.assertRaises((TypeError, ValueError)):
                infer_hill("HIAT", **parameters)

    def test_hash_certificate_matches_recovered_bytes(self):
        certificate = json.loads(CERT.read_text())
        for vector in certificate["vectors"]:
            cribs = tuple(Crib(c["offset"], c["plaintext"]) for c in vector["cribs"])
            report = infer_hill(vector["ciphertext"], cribs=cribs)
            self.assertTrue(report["search_complete"])
            recovered = report["candidates"][0]["plaintext"]
            self.assertEqual(recovered, vector["expected_plaintext"])
            self.assertEqual(hashlib.sha256(recovered.encode("ascii")).hexdigest(),
                             vector["plaintext_sha256"])
            self.assertFalse(vector["matrix_supplied_to_solver"])


if __name__ == "__main__":
    unittest.main()
