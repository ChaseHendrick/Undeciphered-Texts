"""Council integration preserves budgets and keeps calibration out of fitting."""
from hashlib import sha256
import unittest
from unittest.mock import patch

from engine.persona_solver_common import make_report
from engine.persona_solvers import investigate_personas


class AdaptiveCouncilTest(unittest.TestCase):
    def runners(self, names, spends=None):
        calls = []

        def runner(name):
            def run(text, **params):
                calls.append((name, params))
                checks = params["max_checks"] if spends is None else spends[name]
                return make_report(name, name, [], checks, params["max_checks"],
                                   True, "complete", [], [])
            return run

        return {name: runner(name) for name in names}, calls

    def test_prior_profile_is_wired_and_unused_checks_are_redistributed(self):
        names = ("emperor", "inheritance", "hallucinogens")
        strategies, calls = self.runners(names, dict(zip(names, (2, 0, 7))))
        profile = {"supplied": "mocked scheduling input"}
        plan = {"allocations": dict(zip(names, (6, 2, 1))),
                "adaptation_strength": .5, "claimed_plaintext": None}
        with patch("engine.persona_solvers._strategies", return_value=strategies), \
             patch("engine.solver_scheduler.allocate_solver_budget", return_value=plan) as allocate:
            report = investigate_personas("ab cd!", personas=names, max_checks=9,
                                          adaptive_profile=profile)
        allocate.assert_called_once_with(names, max_checks=9, adaptive_profile=profile,
            ciphertext_sha256=sha256(b"ABCD").hexdigest())
        self.assertEqual([params["max_checks"] for _, params in calls], [6, 4, 7])
        self.assertTrue(all("adaptive_profile" not in params for _, params in calls))
        self.assertEqual(report["checks"], 9)
        self.assertEqual(report["budget_schedule"], plan)
        self.assertFalse(report["correctness_known"])

    def test_default_keeps_original_policy_without_loading_scheduler(self):
        names = ("emperor", "inheritance", "hallucinogens")
        strategies, calls = self.runners(names, dict(zip(names, (2, 0, 7))))
        with patch("engine.persona_solvers._strategies", return_value=strategies), \
             patch.dict("sys.modules", {"engine.solver_scheduler": None}):
            report = investigate_personas("ABCD", personas=names, max_checks=9)
        self.assertEqual([params["max_checks"] for _, params in calls], [3, 4, 7])
        self.assertNotIn("budget_schedule", report)

    def test_current_cipher_cannot_contribute_to_its_own_allocation(self):
        names = ("emperor", "pacifist")
        strategies, calls = self.runners(names)
        profile = {"format_version": 1, "baseline_name": "uniform-council", "cases": [{
            "case_id": "already-seen", "ciphertext_sha256": sha256(b"ABCD").hexdigest(),
            "reference_sha256": sha256(b"REFERENCE").hexdigest(), "evidence_id": "test-reference",
            "partition": "calibration", "independently_verified": True,
            "evaluation_budget": 9, "baseline": {"correct": False, "checks": 9},
            "outcomes": {"emperor": {"correct": True, "checks": 1},
                         "pacifist": {"correct": False, "checks": 9}},
        }]}
        with patch("engine.persona_solvers._strategies", return_value=strategies):
            report = investigate_personas("a b c d", personas=names, max_checks=9,
                                          adaptive_profile=profile)
        self.assertEqual([params["max_checks"] for _, params in calls], [5, 4])
        self.assertEqual(report["budget_schedule"]["excluded_current_case_count"], 1)
        self.assertEqual(report["budget_schedule"]["adaptation_strength"], 0)
        self.assertEqual(report["checks"], 9)

    def test_malformed_profile_is_rejected_before_any_search(self):
        names = ("emperor",)
        strategies, calls = self.runners(names)
        with patch("engine.persona_solvers._strategies", return_value=strategies):
            with self.assertRaises(ValueError):
                investigate_personas("ABCD", personas=names, max_checks=0,
                                      adaptive_profile={"plaintext": "answer"})
        self.assertEqual(calls, [])


if __name__ == "__main__":
    unittest.main()
