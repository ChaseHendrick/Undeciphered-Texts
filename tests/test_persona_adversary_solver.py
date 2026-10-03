"""Concrete counterexamples to unsupported unique-answer claims."""
import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from engine.reverse_engineer import Crib
from engine.solvers.persona_adversary import investigate_adversary

PLAIN = "THEHEIRREADTHESEALEDLETTERANDMOVEDTHEGOLDTOTHEESTATEBEFORESUNRISE"
CIPHER = "AOLOLPYYLHKAOLZLHSLKSLAALYHUKTVCLKAOLNVSKAVAOLLZAHALILMVYLZBUYPZL"


class AdversarySolverTest(unittest.TestCase):
    def test_blind_literal_control_recovers_and_excludes_a_wrong_proposal(self):
        report = investigate_adversary(CIPHER, candidate="A" * len(PLAIN))
        self.assertTrue(any(c["plaintext"] == PLAIN for c in report["candidates"]))
        self.assertFalse(any(c["plaintext"] == "A" * len(PLAIN) for c in report["candidates"]))
        self.assertTrue(report["ambiguity_observed"])
        self.assertFalse(report["exhaustive_all_cipher_uniqueness"])
        self.assertIsNone(report["claimed_plaintext"])

    def test_alternatives_use_same_cribs_and_proposal_is_not_a_fitting_constraint(self):
        from engine.solver_reasoning import investigate_cipher
        with patch("engine.solvers.persona_adversary.investigate_cipher", wraps=investigate_cipher) as run:
            report = investigate_adversary(CIPHER, cribs=(Crib(0, "THE"),), candidate="A" * len(PLAIN))
        self.assertEqual(run.call_args.kwargs["cribs"], (Crib(0, "THE"),))
        self.assertNotIn("candidate", run.call_args.kwargs)
        self.assertTrue(report["proposal_contradicted_by_supplied_cribs"])
        self.assertTrue(all(c["plaintext"].startswith("THE") for c in report["candidates"]))

    def test_normalized_proposal_is_excluded_even_with_case_and_spacing(self):
        report = investigate_adversary(CIPHER, candidate=" ".join(PLAIN.lower()))
        self.assertFalse(any(c["plaintext"] == PLAIN for c in report["candidates"]))
        self.assertTrue(report["proposed_witness_seen"])

    def test_bounds_and_optional_neural_fallback(self):
        with patch.dict("sys.modules", {"numpy": None}):
            for budget in (0, 1, 2, 26, 312, 500):
                report = investigate_adversary(CIPHER, candidate=PLAIN, max_checks=budget, max_candidates=2)
                self.assertLessEqual(report["checks"], budget)
                self.assertLessEqual(len(report["candidates"]), 2)
                self.assertEqual(report["checks"], report["search_checks"] + report["proposal_checks"])
                self.assertEqual(report["ledger"]["neural_advice"]["status"], "unavailable")

    def test_one_or_zero_retained_alternatives_does_not_prove_uniqueness(self):
        report = investigate_adversary(CIPHER, max_checks=1, max_candidates=1)
        self.assertFalse(report["exhaustive_all_cipher_uniqueness"])
        self.assertFalse(report["search_complete"])
        self.assertFalse(report["correctness_known"])

    def test_invalid_proposed_text_and_bounds_reject(self):
        for proposal in (123, "", "ABC", "A" * 64, "A" * 66, "α" * 65, "1" * 65):
            with self.assertRaises((TypeError, ValueError)):
                investigate_adversary(CIPHER, candidate=proposal)
        for opts in ({"max_checks": True}, {"max_checks": -1}, {"max_candidates": 0}, {"cribs": (Crib(0, "T"), Crib(0, "X"))}):
            with self.assertRaises((TypeError, ValueError)):
                investigate_adversary(CIPHER, **opts)

    def test_certificate_hashes_an_actual_generated_alternative(self):
        path = Path(__file__).resolve().parents[1] / "engine/data/persona_adversary_solver_certificate.json"
        vector = json.loads(path.read_text())
        report = investigate_adversary(vector["ciphertext"], candidate=vector["proposed_plaintext"])
        self.assertTrue(any(hashlib.sha256(c["plaintext"].encode("ascii")).hexdigest() == vector["plaintext_sha256"] for c in report["candidates"]))


if __name__ == "__main__":
    unittest.main()
