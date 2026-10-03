"""Unknown-offset Vigenere investigations against literal and exhaustive controls."""
from __future__ import annotations

from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from engine.solvers.persona_detective import investigate_detective

PLAIN = "THELIBRARIANPLACEDTHESEALEDLETTERBESIDETHEMAPANDWAITEDFORTHENIGHTTRAINWHILETHERAINFELLONTHESILENTPLATFORM"
CIPHER = "HYEYOFFRRVGRDCAPKHHYEFKEZVDYKXHVROKWWUEGNIARPNTHKRIGKHTFRGNIBZGUZXFRIACLWCEGNIFRIALIZCOAZLSJIYKRHGLNZJCIM"
CERT = Path(__file__).resolve().parents[1] / "engine/data/persona_detective_solver_certificate.json"


class DetectiveSolverTest(unittest.TestCase):
    def test_literal_short_crib_recovers_unknown_offset_key_and_outside_plaintext(self):
        report = investigate_detective(CIPHER, crib="LETTER BESIDE")
        hit = next(c for c in report["candidates"] if c["plaintext"] == PLAIN)
        self.assertEqual(hit["key"], {"keyword": "ORANGE", "period": 6, "crib_offset": 27})
        self.assertGreaterEqual(hit["evidence"]["repeated_confirmations"], 2)
        self.assertTrue(hit["forward_consistent"])
        self.assertTrue(hit["crib_match"])
        self.assertEqual(report["checks"], 940)
        self.assertTrue(report["search_complete"])
        self.assertIsNone(report["claimed_plaintext"])
        json.dumps(report, allow_nan=False)

    def test_small_oracle_enumerates_actual_keys_and_unknown_offsets(self):
        cipher, crib = "DFHJDF", "ABCD"
        expected = set()
        for period in (1, 2):
            for key in product(range(26), repeat=period):
                plain = "".join(chr(65 + (ord(ch) - 65 - key[i % period]) % 26)
                                for i, ch in enumerate(cipher))
                for start in range(3):
                    if plain[start:start + 4] == crib:
                        expected.add((start, period, "".join(chr(65 + k) for k in key), plain))
        report = investigate_detective(cipher, crib=crib, max_period=2, min_checks=1, max_candidates=100)
        actual = {(c["key"]["crib_offset"], c["key"]["period"], c["key"]["keyword"], c["plaintext"])
                  for c in report["candidates"]}
        self.assertEqual(actual, expected)
        self.assertEqual(report["checks"], 6)
        self.assertTrue(report["search_complete"])

    def test_prefix_budget_and_confirmation_policy_are_explicit(self):
        for budget in (0, 1, 3, 5, 6):
            report = investigate_detective("DFHJDF", crib="ABCD", max_period=2,
                                          min_checks=1, max_checks=budget, max_candidates=1)
            self.assertEqual(report["checks"], budget)
            self.assertEqual(report["search_complete"], budget == 6)
            self.assertLessEqual(len(report["candidates"]), 1)
            self.assertEqual(report["checks"], sum(a["checks"] for a in report["actions"]))
        report = investigate_detective("DFHJDF", crib="AB", min_checks=2)
        self.assertEqual(report["checks"], 0)
        self.assertEqual(report["candidates"], [])
        self.assertEqual(report["bounds"]["eligible_periods"], [])
        self.assertTrue(report["search_complete"])

    def test_core_solver_is_available_without_numpy_or_symbolic_dependency(self):
        with patch.dict("sys.modules", {"numpy": None, "z3": None}):
            report = investigate_detective(CIPHER, crib="LETTERBESIDE")
        self.assertTrue(any(c["plaintext"] == PLAIN for c in report["candidates"]))
        self.assertEqual(report["neural_advice"]["status"], "not_used")

    def test_invalid_parameters_and_missing_crib(self):
        for options in ({"crib": "A"}, {"crib": "A" * 106}, {"crib": 123}, {"crib": "A1BC"},
                        {"max_period": True}, {"max_period": 0}, {"max_period": 129},
                        {"min_checks": 0}, {"min_checks": True}, {"min_checks": 513},
                        {"max_checks": -1}, {"max_checks": 100001}, {"max_candidates": 0}):
            params = {"crib": "LETTERBESIDE", **options}
            with self.subTest(options=options), self.assertRaises((TypeError, ValueError)):
                investigate_detective(CIPHER, **params)
        with self.assertRaises(TypeError):
            investigate_detective(CIPHER)
        for text in (None, "ABC", "A" * 513, "AB12CD", "α" * 30):
            with self.assertRaises((TypeError, ValueError)):
                investigate_detective(text, crib="AB")

    def test_certificate_hash_covers_recovered_literal_plaintext(self):
        certificate = json.loads(CERT.read_text())
        report = investigate_detective(certificate["ciphertext"], crib=certificate["crib"])
        recovered = next(c["plaintext"] for c in report["candidates"]
                         if c["plaintext"] == certificate["expected_plaintext"])
        self.assertEqual(sha256(recovered.encode("ascii")).hexdigest(), certificate["plaintext_sha256"])
        self.assertFalse(certificate["key_supplied_to_solver"])
        self.assertFalse(certificate["crib_offset_supplied_to_solver"])


if __name__ == "__main__":
    unittest.main()
