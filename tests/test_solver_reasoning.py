"""Bounded investigative composition, with independent literal controls."""
from __future__ import annotations

import json
import hashlib
from pathlib import Path
import unittest
from unittest.mock import patch

from engine.reverse_engineer import Crib
from engine.solver_reasoning import investigate_cipher, score_reward, evaluation_policy

PLAIN = "THEHARBORBELLRANGTWICEBEFOREDAWNANDTHESMALLBOATSLEFTTHEQUAYWITHNETSFOLDEDONTHEDECKATHINMISTHIDTHEFARSHOREBUTTHECREWKNEWTHECHANNELBYTHESOUNDOFWATERAGAINSTSTONE"
CAESAR = "ESPSLCMZCMPWWCLYREHTNPMPQZCPOLHYLYOESPDXLWWMZLEDWPQEESPBFLJHTESYPEDQZWOPOZYESPOPNVLESTYXTDESTOESPQLCDSZCPMFEESPNCPHVYPHESPNSLYYPWMJESPDZFYOZQHLEPCLRLTYDEDEZYP"
AFFINE = "ZRCRIPNAPNCLLPIVMZOWSCNCHAPCXIOVIVXZRCUQILLNAIZULCHZZRCKEIYOWZRVCZUHALXCXAVZRCXCSGIZRWVQWUZRWXZRCHIPURAPCNEZZRCSPCOGVCOZRCSRIVVCLNYZRCUAEVXAHOIZCPIMIWVUZUZAVC"
REDEFENCE = "HROLRTIEOANTELBSEHQWTTFEOEETISHHFHRTHEKTENETENOTRISOEHBNEENMATANLTKMDRBCEHBOWGSTBLWFWHLLEISDDHTEOTWHNHDENNEAREAGCBRDADSAOTFTUYHEODNHCANIITASEUERNWCALYSUFAAATT"


class SolverReasoningTest(unittest.TestCase):
    def test_unknown_key_literal_controls_and_honest_mission(self):
        for cipher, family in ((CAESAR, "caesar"), (AFFINE, "affine"), (REDEFENCE, "redefence")):
            report = investigate_cipher(cipher)
            hit = next(c for c in report.candidates if c.plaintext == PLAIN)
            self.assertEqual(hit.family, family)
            self.assertTrue(hit.re_encryption_matches)
            self.assertTrue(report.search_complete)
            self.assertLessEqual(report.checks, 5000)
            self.assertFalse(report.correctness_known)
            self.assertIsNone(report.happiness)
            self.assertIsNone(report.claimed_plaintext)
            self.assertEqual(report.objective, "seek independently verifiable solutions to unresolved ciphers")
            self.assertTrue(any(step["stage"] == "verify_case" for step in report.next_actions))
            json.dumps(report.to_dict())

    def test_crib_inference_predicts_unseen_suffix_without_supplying_key(self):
        report = investigate_cipher("LXFOPVEFRNHR", cribs=(Crib(0, "ATTACK"),))
        hit = next(c for c in report.candidates if c.family == "vigenere" and c.key.get("keyword") == "LEMON")
        self.assertEqual(hit.plaintext, "ATTACKATDAWN")
        self.assertTrue(hit.re_encryption_matches)
        self.assertEqual(report.coordinate_system, "zero-based A-Z plaintext letters after removing spaces and punctuation")
        self.assertFalse(report.correctness_known)
        self.assertTrue(any(h["unresolved_parameters"] > 0 for h in report.hypotheses))

    def test_one_global_budget_and_zero_checks(self):
        for budget in (0, 1, 26, 312, 314, 315, 330, 1000):
            report = investigate_cipher("LXFOPVEFRNHR", cribs=(Crib(0, "ATTACK"),), max_checks=budget, max_candidates=3)
            self.assertLessEqual(report.checks, budget)
            self.assertEqual(report.checks, sum(action["checks"] for action in report.actions))
            self.assertLessEqual(len(report.candidates), 3)
            self.assertLessEqual(report.consistency_checks, report.checks)
            if budget == 0:
                self.assertEqual(report.candidates, ())
                self.assertEqual(report.checks, 0)
                self.assertFalse(report.search_complete)

    def test_numeric_uses_evidence_and_preserves_space_coordinates(self):
        report = investigate_cipher("0", lexicon=("E",), max_checks=6)
        self.assertEqual(report.checks, 6)
        self.assertEqual(report.candidates[0].plaintext, "E")
        self.assertEqual(report.candidates[0].family, "pollux")
        self.assertFalse(report.search_complete)
        self.assertIsNone(report.happiness)
        self.assertEqual(report.coordinate_system, "zero-based uppercase decoded characters including word spaces and punctuation")
        report = investigate_cipher("0", max_checks=6)
        self.assertEqual(report.checks, 0)
        self.assertEqual(report.candidates, ())
        self.assertTrue(any(step["reason"] == "Morse inference requires aligned cribs or a lexicon" for step in report.next_actions))
        with patch("engine.solver_reasoning.search_morse_constraints", wraps=__import__("engine.solvers.morse_constraints", fromlist=["search_morse_constraints"]).search_morse_constraints) as search:
            investigate_cipher("12345", cribs=(Crib(0, "E E"),), max_checks=0)
            self.assertEqual(search.call_args.kwargs["cribs"][0].plaintext, "E E")

    def test_contradictory_premises_stop_without_search(self):
        report = investigate_cipher(CAESAR, cribs=(Crib(0, "THE"), Crib(1, "ZZ")))
        self.assertEqual(report.checks, 0)
        self.assertEqual(report.candidates, ())
        self.assertEqual(report.stop_reason, "constraint_conflict")
        self.assertFalse(report.search_complete)
        self.assertEqual(report.contradictions[0]["kind"], "overlapping_cribs")
        self.assertTrue(any(step["stage"] == "review_constraints" for step in report.next_actions))

    def test_no_candidate_is_a_scoped_failure_not_a_decipherment(self):
        report = investigate_cipher("ABCDEFGHIJKLMNOPQ", cribs=(Crib(0, "A" * 17),))
        self.assertEqual(report.candidates, ())
        self.assertTrue(report.search_complete)
        self.assertTrue(any(item["kind"] == "no_compatible_model" for item in report.contradictions))
        self.assertTrue(any(item["stage"] == "alternative_models" for item in report.next_actions))

    def test_neural_advice_falls_back_without_fabricated_probabilities(self):
        with patch.dict("sys.modules", {"numpy": None}):
            report = investigate_cipher(CAESAR, max_checks=312)
        self.assertEqual(report.candidates[0].plaintext, PLAIN)
        self.assertEqual(report.neural_advice["status"], "unavailable")
        self.assertEqual(report.neural_advice["reason"], "NumPy is unavailable")
        self.assertEqual(report.neural_advice["candidates"], [])
        self.assertTrue(all(c.neural_probability is None for c in report.candidates))

    def test_real_neural_ranking_is_advisory_only_when_available(self):
        report = investigate_cipher(CAESAR, max_checks=312)
        if report.neural_advice["status"] == "available":
            self.assertTrue(report.neural_advice["candidates"])
            self.assertTrue(all(0 <= row["probability"] <= 1 for row in report.neural_advice["candidates"]))
            self.assertIn("model_sha256", report.neural_advice)
        self.assertFalse(report.correctness_known)
        self.assertIsNone(report.happiness)

    def test_temperament_cannot_change_evidence_or_transform_checks(self):
        reports = [investigate_cipher(CAESAR, max_checks=312, temperament=t) for t in ("balanced", "curious", "cautious")]
        for report in reports[1:]:
            self.assertEqual(report.candidates, reports[0].candidates)
            self.assertEqual(report.actions, reports[0].actions)
            self.assertEqual(report.checks, reports[0].checks)
            self.assertEqual(report.contradictions, reports[0].contradictions)
        state = reports[0].simulated_affect
        self.assertFalse(state["literal_feelings_or_sentience"])
        self.assertEqual(set(state["states"]), {"curiosity", "caution", "frustration"})
        self.assertIn("plan", reports[0].thought)

    def test_forward_consistency_failures_are_logged_and_rejected(self):
        with patch("engine.solver_reasoning.affine_decrypt", return_value="A" * len(CAESAR)):
            report = investigate_cipher(CAESAR, max_checks=26)
        self.assertEqual(report.candidates, ())
        self.assertEqual(report.consistency_checks, 26)
        self.assertEqual(report.contradictions[0]["kind"], "transform_inconsistency")

    def test_reward_needs_independent_cases_and_prioritizes_correctness(self):
        self.assertIsNone(score_reward(0, 0, 0, 10))
        self.assertEqual(score_reward(0, 1, 0, 10), 0)
        self.assertEqual(score_reward(1, 2, 0, 10), 0)
        self.assertGreater(score_reward(1, 1, 10, 10), score_reward(0, 1, 0, 10))
        self.assertGreater(score_reward(1, 1, 1, 10), score_reward(1, 1, 10, 10))
        self.assertEqual(score_reward(1, 1, 0, 0), 1)
        for args in ((2, 1, 0, 1), (True, 1, 0, 1), (1, 1, 2, 1), (-1, 1, 0, 1)):
            with self.assertRaises((ValueError, TypeError)):
                score_reward(*args)

    def test_retirement_policy_requires_independently_checked_failures(self):
        self.assertIsNone(evaluation_policy(0, 0)["eligible"])
        self.assertEqual(evaluation_policy(0, 0)["recommendation"], "collect_independent_cases")
        self.assertIsNone(evaluation_policy(0, 19)["eligible"])
        self.assertTrue(evaluation_policy(19, 20)["eligible"])
        self.assertFalse(evaluation_policy(14, 20)["eligible"])
        self.assertEqual(evaluation_policy(14, 20)["recommendation"], "retire_or_demote")
        self.assertFalse(evaluation_policy(95, 100)["eligible"])
        self.assertTrue(evaluation_policy(95, 100, max_failures=6)["eligible"])
        unresolved = investigate_cipher("ABCDEFGHIJKLMNOPQ", cribs=(Crib(0, "A" * 17),))
        self.assertIsNone(unresolved.evaluation["failures"])
        self.assertIsNone(unresolved.evaluation["eligible"])
        for params in ({"min_cases": 0}, {"min_accuracy": True}, {"min_accuracy": float("nan")}, {"max_failures": 0}):
            with self.assertRaises((ValueError, TypeError)):
                evaluation_policy(0, 0, **params)

    def test_strict_bounds_types_and_unsupported_inputs(self):
        for params in ({"max_checks": -1}, {"max_checks": 100001}, {"max_checks": True},
                       {"max_candidates": 0}, {"max_candidates": 101}, {"temperament": "angry"},
                       {"cribs": iter(())}, {"cribs": (Crib(True, "A"),)},
                       {"cribs": (Crib(999, "A"),)}, {"lexicon": "THE"}, {"lexicon": ()}):
            with self.subTest(params=params), self.assertRaises((ValueError, TypeError)):
                investigate_cipher(CAESAR, **params)
        for text in (None, "", "ABC", "123A", "123.4", "CAFÉ", "A" * 513, "1" * 513):
            with self.subTest(text=text), self.assertRaises((ValueError, TypeError)):
                investigate_cipher(text)

    def test_certificate_hashes_an_actual_blind_recovered_output(self):
        cert = json.loads((Path(__file__).parents[1] / "engine/data/solver_reasoning_certificate.json").read_text())
        report = investigate_cipher(cert["ciphertext"], **cert["search_limits"])
        self.assertEqual(report.candidates[0].plaintext, PLAIN)
        self.assertEqual(hashlib.sha256(report.candidates[0].plaintext.encode("ascii")).hexdigest(), cert["plaintext_sha256"])
        self.assertEqual(report.checks, cert["checks"])
        self.assertEqual(report.search_complete, cert["search_complete"])
        self.assertEqual(cert["tool_name"], "solver-reasoning")
        self.assertNotIn("cipher_name", cert)


if __name__ == "__main__":
    unittest.main()
