"""The logit student and the Sinkhorn mix do not beat the lifted ranking."""

from __future__ import annotations

import unittest

import numpy as np

from engine.bob_distill import apply_student, bob_distill_report, fit_student
from engine.solvers.dagapeyeff import consider_bob_distill

_SHIPPED = "5c271f426812d6307f208a636b80f820201e25b3dc6778333e5d08d4d5aaaf4b"


class BobDistillTest(unittest.TestCase):
    def test_a_separable_toy_is_learned(self) -> None:
        labels = np.array([index % 3 for index in range(30)])
        each = np.zeros((2, 30, 3))
        for index, label in enumerate(labels):
            each[0, index, label] = 5.0
        weights = fit_student(each, labels, steps=150, strength=0.0)
        predicted, _scores = apply_student(each, weights)
        self.assertEqual(int((predicted == labels).sum()), 30)

    def test_neither_student_is_promoted(self) -> None:
        report = bob_distill_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["weights_sha256"], _SHIPPED)
        self.assertFalse(report["weights_replaced"])
        self.assertTrue(report["weights_match_shipped"])
        self.assertEqual(report["train_total"], 160)
        self.assertEqual(report["train_student_correct"], 153)
        self.assertEqual(report["held_mean"], 429)
        self.assertEqual(report["held_lift"], 433)
        self.assertEqual(report["held_student"], 427)
        self.assertEqual(report["held_student_top3"], 477)
        self.assertEqual(report["held_sinkhorn"], 429)
        self.assertEqual(report["held_total"], 480)
        self.assertEqual(report["benchmark_mean"], 193)
        self.assertEqual(report["benchmark_lift"], 195)
        self.assertEqual(report["benchmark_student"], 192)
        self.assertEqual(report["benchmark_student_top3"], 204)
        self.assertEqual(report["benchmark_sinkhorn"], 193)
        self.assertEqual(report["benchmark_total"], 204)
        self.assertFalse(report["student_promoted"])
        self.assertFalse(report["sinkhorn_promoted"])
        self.assertFalse(report["promoted"])
        claim = consider_bob_distill()
        self.assertFalse(claim["bob_distill_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIsNone(claim["claimed_plaintext"])
        self.assertIn("weight file stays", claim["learned"])


if __name__ == "__main__":
    unittest.main()
