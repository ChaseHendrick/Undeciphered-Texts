"""Independent integration regressions for council evidence and selected loading."""
from __future__ import annotations

from hashlib import sha256
import unittest
from unittest.mock import patch

from engine.persona_solver_common import make_report
from engine.persona_solvers import investigate_personas
from engine.reverse_engineer import Crib
from tests.test_persona_detective_solver import CIPHER as VIGENERE, PLAIN
from tests.test_persona_emperor_solver import CAESAR


class CouncilAuditTest(unittest.TestCase):
    def test_selected_emperor_does_not_import_unselected_strategy_modules(self):
        with patch.dict("sys.modules", {
            "engine.solvers.persona_skeptic": None,
            "engine.solvers.persona_adversary": None,
        }):
            report = investigate_personas("ABCD", personas=("emperor",), max_checks=0)
        self.assertEqual(report["selected_personas"], ["emperor"])
        self.assertEqual(report["checks"], 0)

    def test_detective_fit_letters_cannot_be_claimed_as_reserved_crib_support(self):
        try:
            report = investigate_personas(
                VIGENERE, personas=("detective", "skeptic"),
                unplaced_crib="LETTERBESIDE", verification_cribs=(Crib(27, "LETTERBESIDE"),),
                max_checks=2500, max_candidates=5,
            )
        except ValueError as error:
            self.assertIn("overlap", str(error).lower())
            return
        for candidate in report["candidates"]:
            if candidate["plaintext"] == PLAIN:
                verdict = candidate["skeptic_review"]
                self.assertTrue(verdict["evidence_used_for_generation"])
                self.assertNotEqual(verdict["status"], "crib-supported")
        for verdict in report["persona_reports"]["skeptic"]["reviews"]:
            if verdict["plaintext"] == PLAIN:
                self.assertTrue(verdict["evidence_used_for_generation"])
                self.assertNotEqual(verdict["status"], "crib-supported")

    def test_rejected_shortlist_does_not_backfill_a_silently_unreviewed_answer(self):
        report = investigate_personas(
            CAESAR, personas=("emperor", "pacifist", "skeptic"),
            expected_plaintext_sha256=sha256(("A" * len(CAESAR)).encode("ascii")).hexdigest(),
            max_checks=5000, max_candidates=1,
        )
        self.assertTrue(report["contradicted_candidates"])
        for candidate in report["candidates"]:
            self.assertIn("skeptic_review", candidate)
            status = candidate["skeptic_review"]["status"]
            self.assertNotIn(status, ("contradicted", "rejected"))
            if status in ("unreviewed", "unchecked"):
                self.assertFalse(report["search_complete"])

    def test_reserved_evidence_only_reaches_postsearch_review_and_not_fitting(self):
        from engine.solvers.persona_skeptic import investigate_skeptic
        calls = []

        def generate(text, **params):
            calls.append(params)
            candidate = {"plaintext": PLAIN, "family": "caesar", "key": {"multiplier": 1, "offset": 9},
                         "score": 123., "forward_consistent": True, "crib_match": True, "evidence": {}}
            return make_report("emperor", "controlled fitting", [candidate], 1,
                               params["max_checks"], True, "complete", [], [])

        heldout = (Crib(27, "LETTERBESIDE"),)
        digest = sha256(PLAIN.encode("ascii")).hexdigest()
        with patch("engine.persona_solvers._strategies", return_value={
            "emperor": generate, "skeptic": investigate_skeptic,
        }):
            report = investigate_personas(CAESAR, personas=("skeptic", "emperor"),
                cribs=(Crib(0, "THE"),), verification_cribs=heldout,
                expected_plaintext_sha256=digest, max_checks=5)
        self.assertEqual(report["selected_personas"], ["emperor", "skeptic"])
        self.assertEqual(calls[0]["cribs"], (Crib(0, "THE"),))
        self.assertNotIn("verification_cribs", calls[0])
        self.assertNotIn("expected_plaintext_sha256", calls[0])
        self.assertNotIn("candidate_plaintexts", calls[0])
        self.assertFalse(report["persona_reports"]["skeptic"]["search_executed"])
        self.assertEqual(report["candidates"][0]["skeptic_review"]["status"], "exact-reference-match")
        self.assertEqual(report["checks"], 2)
        self.assertLessEqual(report["checks"], 5)


if __name__ == "__main__":
    unittest.main()
