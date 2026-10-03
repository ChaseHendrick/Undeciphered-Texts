"""Real bounded Emperor investigation, separate from sentence preferences."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from engine.reverse_engineer import Crib
from engine.solvers.persona_court_notice import investigate_emperor

PLAIN = "THELIBRARIANPLACEDTHESEALEDLETTERBESIDETHEMAPANDWAITEDFORTHENIGHTTRAINWHILETHERAINFELLONTHESILENTPLATFORM"
CAESAR = "CQNURKAJARJWYUJLNMCQNBNJUNMUNCCNAKNBRMNCQNVJYJWMFJRCNMOXACQNWRPQCCAJRWFQRUNCQNAJRWONUUXWCQNBRUNWCYUJCOXAV"
RAIL = "TIRPEELERIHPWERNTIIHILTITTMHLBAINLCDHSAELTEBSDTEAADATDOTEIHTANHLTEANELNHSLNPAFRERAATEDTEEMNIFHGRWERFOEELO"
CERT = Path(__file__).resolve().parents[1] / "engine/data/persona_emperor_solver_certificate.json"


class EmperorInvestigationTest(unittest.TestCase):
    def test_blind_literal_controls_recover_without_key_or_persona_words(self):
        for ciphertext, families in ((CAESAR, {"caesar"}), (RAIL, {"rail-fence", "redefence"})):
            report = investigate_emperor(ciphertext)
            hit = next(c for c in report["candidates"] if c["plaintext"] == PLAIN)
            self.assertIn(hit["family"], families)
            self.assertTrue(hit["forward_consistent"])
            self.assertTrue(hit["crib_match"])
            self.assertTrue(hit["evidence"])
            self.assertIsNone(report["claimed_plaintext"])
            self.assertTrue(report["search_complete"])
            self.assertEqual(report["persona"], "emperor")
            self.assertEqual(report["checks"], report["ledger"]["checks"])
            self.assertEqual(report["search_complete"], report["ledger"]["search_complete"])
            self.assertEqual(report["checks"], sum(a["checks"] for a in report["ledger"]["actions"]))
            self.assertLessEqual(report["checks"], 5000)
            self.assertTrue(report["actions"])
            json.dumps(report, allow_nan=False)

    def test_aligned_crib_predicts_unprovided_suffix_and_surfaces_partial_models(self):
        report = investigate_emperor("LXFOPVEFRNHR", cribs=(Crib(0, "ATTACK"),))
        hit = next(c for c in report["candidates"] if c["family"] == "vigenere"
                   and c["key"].get("keyword") == "LEMON")
        self.assertEqual(hit["plaintext"], "ATTACKATDAWN")
        self.assertTrue(hit["forward_consistent"])
        self.assertTrue(hit["crib_match"])
        self.assertTrue(report["hypotheses"])
        self.assertTrue(any("?" in h["predicted_plaintext"] for h in report["hypotheses"]))
        self.assertEqual(report["conditional_predictions"], report["hypotheses"])
        self.assertIsNone(report["claimed_plaintext"])

    def test_global_budget_and_unavailable_neural_fallback(self):
        with patch.dict("sys.modules", {"numpy": None}):
            for budget in (0, 1, 26, 312, 500):
                report = investigate_emperor(CAESAR, max_checks=budget, max_candidates=3)
                self.assertLessEqual(report["checks"], budget)
                self.assertLessEqual(len(report["candidates"]), 3)
                self.assertEqual(report["checks"], report["ledger"]["checks"])
                self.assertEqual(report["neural_advice"]["status"], "unavailable")
                self.assertEqual(report["neural_advice"]["candidates"], [])
                if budget == 0:
                    self.assertEqual(report["candidates"], [])
                    self.assertFalse(report["search_complete"])
                    self.assertEqual(report["stop_reason"], "check_limit")
        self.assertEqual(report["neural_advice"]["reason"], "NumPy is unavailable")

    def test_conflicting_constraints_reject_and_model_failures_keep_the_ledger(self):
        with self.assertRaisesRegex(ValueError, "contradict"):
            investigate_emperor(CAESAR, cribs=(Crib(0, "THE"), Crib(1, "ZZ")))
        report = investigate_emperor("ABCDEFGHIJKLMNOPQ", cribs=(Crib(0, "A" * 17),))
        self.assertEqual(report["candidates"], [])
        self.assertTrue(report["search_complete"])
        self.assertTrue(any(c["kind"] == "no_compatible_model" for c in report["contradictions"]))
        self.assertEqual(report["contradictions"], list(report["ledger"]["contradictions"]))

    def test_input_bounds_and_types(self):
        for text in (None, 123, "ABC", "1" * 20, "A" * 513, "Α" * 20, "A1BCDE"):
            with self.subTest(text=str(text)[:20]), self.assertRaises((TypeError, ValueError)):
                investigate_emperor(text)
        for options in ({"max_checks": True}, {"max_checks": -1}, {"max_checks": 100001},
                        {"max_candidates": 0}, {"max_candidates": 101}, {"cribs": "THE"},
                        {"cribs": (Crib(104, "TOO"),)}):
            with self.subTest(options=options), self.assertRaises((TypeError, ValueError)):
                investigate_emperor(CAESAR, **options)

    def test_certificate_hashes_actual_recovered_plaintext(self):
        certificate = json.loads(CERT.read_text())
        for control in certificate["controls"]:
            report = investigate_emperor(control["ciphertext"])
            recovered = next(c["plaintext"] for c in report["candidates"]
                             if c["plaintext"] == control["expected_plaintext"])
            self.assertEqual(hashlib.sha256(recovered.encode("ascii")).hexdigest(),
                             control["plaintext_sha256"])
            self.assertFalse(control["key_supplied_to_solver"])
        self.assertIn("synthetic", certificate["note"].lower())


if __name__ == "__main__":
    unittest.main()
