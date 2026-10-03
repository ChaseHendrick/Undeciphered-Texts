"""Independent-reference policy controls, not a cipher classifier benchmark."""
import copy
import hashlib
import json
import math
import unittest

from engine.solver_scheduler import allocate_solver_budget, baseline_relative_gate


STRATEGIES = ("normal-man", "hallucinogens", "mechanic")


def profile(count=18, *, correct=(True, False, False), baseline=False,
            checks=(100, 1, 1)):
    cases = []
    for index in range(count):
        cases.append({
            "case_id": f"constructed-reference-{index}",
            "ciphertext_sha256": hashlib.sha256(f"cipher-{index}".encode()).hexdigest(),
            "reference_sha256": hashlib.sha256(f"independent-answer-{index}".encode()).hexdigest(),
            "evidence_id": f"independent-policy-control/{index}",
            "partition": "calibration", "independently_verified": True,
            "evaluation_budget": 100,
            "baseline": {"correct": baseline, "checks": 100},
            "outcomes": {name: {"correct": valid, "checks": cost}
                         for name, valid, cost in zip(STRATEGIES, correct, checks)},
        })
    return {"format_version": 1, "baseline_name": "uniform-council", "cases": cases}


def allocate(prior=None, budget=100, **kwargs):
    return allocate_solver_budget(
        STRATEGIES, max_checks=budget, adaptive_profile=prior,
        ciphertext_sha256="f" * 64 if prior is not None else None, **kwargs)


class SolverSchedulerTests(unittest.TestCase):
    def test_uniform_fallback_and_exact_integer_budget(self):
        result = allocate(budget=100)
        self.assertEqual(result["allocations"],
                         {"normal-man": 34, "hallucinogens": 33, "mechanic": 33})
        self.assertEqual(result["adaptation_strength"], 0)
        self.assertEqual(result["feedback_case_count"], 0)
        self.assertEqual(sum(result["allocations"].values()), 100)

    def test_actual_fins_gate_numeric_control_and_maturity(self):
        # These errors and strength were observed by executing current Fins' director.
        result = baseline_relative_gate(0.1472, 0.1952, 1)
        self.assertAlmostEqual(result["relative_lift"], 0.2459016393442623)
        self.assertAlmostEqual(result["adaptation_strength"], 1 / 18)
        self.assertEqual(baseline_relative_gate(.1, .2, 18)["adaptation_strength"], 1)
        self.assertEqual(baseline_relative_gate(.3, .2, 100)["adaptation_strength"], 0)
        self.assertEqual(baseline_relative_gate(0, 0, 100)["adaptation_strength"], 0)
        self.assertEqual(baseline_relative_gate(.1, .2, 0)["adaptation_strength"], 0)

    def test_verified_correct_beats_fast_wrong_and_preserves_exploration(self):
        result = allocate(profile(), minimum_exploration=2)
        self.assertEqual(result["allocations"],
                         {"normal-man": 96, "hallucinogens": 2, "mechanic": 2})
        self.assertEqual(result["adaptation_strength"], 1)
        self.assertEqual(result["winning_strategies"], ["normal-man"])
        self.assertEqual(result["strategy_metrics"]["hallucinogens"]["correct_rate"], 0)

    def test_verified_check_efficiency_is_only_an_accuracy_tie_break(self):
        result = allocate(profile(correct=(True, True, False), checks=(100, 25, 0)))
        self.assertEqual(result["winning_strategies"], ["hallucinogens"])
        self.assertEqual(result["allocations"]["hallucinogens"], 98)
        prior = profile(correct=(True, True, False), checks=(100, 0, 0))
        prior["cases"][0]["outcomes"]["hallucinogens"]["correct"] = False
        result = allocate(prior)
        self.assertEqual(result["winning_strategies"], ["normal-man"])

    def test_baseline_dominance_and_perfect_baseline_keep_uniform(self):
        for prior in (profile(correct=(False, False, False), baseline=True),
                      profile(correct=(True, True, True), baseline=True)):
            with self.subTest(prior=prior["cases"][0]["outcomes"]):
                result = allocate(prior)
                self.assertEqual(result["allocations"], allocate()["allocations"])
                self.assertEqual(result["adaptation_strength"], 0)

    def test_small_sample_has_only_limited_influence(self):
        result = allocate(profile(1))
        self.assertAlmostEqual(result["adaptation_strength"], 1 / 18)
        self.assertGreater(result["allocations"]["normal-man"], 34)
        self.assertGreaterEqual(result["allocations"]["mechanic"], 30)

    def test_current_ciphertext_evidence_is_excluded(self):
        prior = profile(1)
        current = prior["cases"][0]["ciphertext_sha256"]
        result = allocate_solver_budget(STRATEGIES, max_checks=100,
                                       adaptive_profile=prior, ciphertext_sha256=current)
        self.assertEqual(result["feedback_case_count"], 0)
        self.assertEqual(result["excluded_current_case_count"], 1)
        self.assertEqual(result["allocations"], allocate()["allocations"])
        with self.assertRaisesRegex(ValueError, "current ciphertext"):
            allocate_solver_budget(STRATEGIES, adaptive_profile=prior)

    def test_unknown_unverified_fitting_and_final_cases_are_rejected(self):
        for field, value in (("independently_verified", False),
                             ("partition", "fitting"), ("partition", "final")):
            prior = profile(1)
            prior["cases"][0][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                allocate(prior)
        for value in (None, "unknown", 1):
            prior = profile(1)
            prior["cases"][0]["outcomes"]["normal-man"]["correct"] = value
            with self.subTest(value=value), self.assertRaises(TypeError):
                allocate(prior)

    def test_duplicate_case_ids_and_ciphertexts_cannot_inflate_evidence(self):
        for field in ("case_id", "ciphertext_sha256"):
            prior = profile(2)
            prior["cases"][1][field] = prior["cases"][0][field]
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "duplicate"):
                allocate(prior)

    def test_all_selected_strategies_need_fair_same_case_measurements(self):
        prior = profile(1)
        del prior["cases"][0]["outcomes"]["mechanic"]
        with self.assertRaisesRegex(ValueError, "selected strategy"):
            allocate(prior)
        prior = profile(1)
        prior["cases"][0]["baseline"]["checks"] = 101
        with self.assertRaises(ValueError):
            allocate(prior)
        prior = profile(1)
        prior["cases"][0]["outcomes"]["mechanic"]["checks"] = -1
        with self.assertRaises(ValueError):
            allocate(prior)

    def test_zero_and_small_budgets_and_largest_remainder_are_exact(self):
        for budget in (0, 1, 2, 3, 4, 19, 101, 99999, 100000):
            result = allocate(profile(4), budget=budget, minimum_exploration=3)
            with self.subTest(budget=budget):
                self.assertEqual(sum(result["allocations"].values()), budget)
                self.assertTrue(all(isinstance(v, int) and v >= 0
                                    for v in result["allocations"].values()))
                if budget >= 9:
                    self.assertTrue(all(v >= 3 for v in result["allocations"].values()))
                else:
                    self.assertEqual(result["adaptation_strength"], 0)

    def test_equivalent_winners_share_budget_and_input_is_unchanged(self):
        prior = profile(correct=(True, True, False), checks=(50, 50, 0))
        original = copy.deepcopy(prior)
        first = allocate(prior, budget=101)
        self.assertEqual(first["allocations"],
                         {"normal-man": 50, "hallucinogens": 50, "mechanic": 1})
        self.assertEqual(first, allocate(prior, budget=101))
        self.assertEqual(prior, original)
        self.assertEqual(json.loads(json.dumps(first, allow_nan=False)), first)
        self.assertIsNone(first["claimed_plaintext"])
        self.assertFalse(first["current_case_correctness_known"])

    def test_finite_bounded_strict_parameters_and_provenance(self):
        for bad in (True, 1.5, -1, 100001):
            with self.subTest(budget=bad), self.assertRaises((TypeError, ValueError)):
                allocate(budget=bad)
        for names in ((), ("normal-man", "normal-man"), "normal-man", ("../evil",)):
            with self.subTest(names=names), self.assertRaises((TypeError, ValueError)):
                allocate_solver_budget(names)
        for bad in (math.nan, math.inf, -.01, 1.01, True):
            with self.subTest(error=bad), self.assertRaises((TypeError, ValueError)):
                baseline_relative_gate(bad, .5, 1)
        for field, bad in (("ciphertext_sha256", "bad"), ("reference_sha256", ""),
                           ("evidence_id", ""), ("evaluation_budget", math.inf)):
            prior = profile(1)
            prior["cases"][0][field] = bad
            with self.subTest(field=field), self.assertRaises((TypeError, ValueError)):
                allocate(prior)
        prior = profile(1)
        prior["cases"][0]["expected_plaintext"] = "DO NOT FEED THE ANSWER"
        with self.assertRaisesRegex(ValueError, "fields"):
            allocate(prior)


if __name__ == "__main__":
    unittest.main()
