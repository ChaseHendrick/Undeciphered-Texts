"""The smaller students do not beat the lifted ranking."""

from __future__ import annotations

import unittest

import numpy as np

from engine.bob_slim import bob_slim_report, fit_bias, fit_mix
from engine.solvers.dagapeyeff import consider_bob_slim

_SHIPPED = "5c271f426812d6307f208a636b80f820201e25b3dc6778333e5d08d4d5aaaf4b"


class BobSlimTest(unittest.TestCase):
    def test_a_constant_shift_is_unlearned_by_a_bias(self) -> None:
        logits = np.tile(np.array([0.0, 3.0]), (20, 1))
        labels = np.zeros(20, dtype=int)
        bias = fit_bias(logits, labels, steps=200, rate=0.2, ridge=0.0, strength=0.0)
        self.assertEqual(int((logits + bias).argmax(axis=1).sum()), 0)

    def test_a_mix_can_prefer_the_correct_network(self) -> None:
        labels = np.zeros(12, dtype=int)
        each = np.zeros((2, 12, 2))
        each[0, :, 0] = 4.0
        each[1, :, 1] = 4.0
        weights = fit_mix(each, labels, steps=80, rate=0.5, ridge=0.0)
        mixed = np.einsum("k,knc->nc", weights, each)
        self.assertEqual(int(mixed.argmax(axis=1).sum()), 0)
        self.assertAlmostEqual(float(weights.sum()), 1.0, places=5)

    def test_neither_small_student_is_promoted(self) -> None:
        report = bob_slim_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["weights_sha256"], _SHIPPED)
        self.assertFalse(report["weights_replaced"])
        self.assertTrue(report["weights_match_shipped"])
        self.assertEqual(report["train_total"], 160)
        self.assertEqual(report["train_bias_correct"], 145)
        self.assertEqual(report["train_lift_bias_correct"], 145)
        self.assertEqual(report["train_mix_correct"], 146)
        self.assertEqual(report["held_mean"], 429)
        self.assertEqual(report["held_lift"], 433)
        self.assertEqual(report["held_bias"], 431)
        self.assertEqual(report["held_bias_top3"], 477)
        self.assertEqual(report["held_lift_bias"], 430)
        self.assertEqual(report["held_mix"], 429)
        self.assertEqual(report["held_mix_top3"], 477)
        self.assertEqual(report["held_total"], 480)
        self.assertEqual(report["benchmark_mean"], 193)
        self.assertEqual(report["benchmark_lift"], 195)
        self.assertEqual(report["benchmark_bias"], 193)
        self.assertEqual(report["benchmark_lift_bias"], 193)
        self.assertEqual(report["benchmark_mix"], 193)
        self.assertEqual(report["benchmark_total"], 204)
        self.assertFalse(report["bias_promoted"])
        self.assertFalse(report["lift_bias_promoted"])
        self.assertFalse(report["mix_promoted"])
        self.assertFalse(report["promoted"])
        claim = consider_bob_slim()
        self.assertFalse(claim["bob_slim_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIn("weight file stays", claim["learned"])


if __name__ == "__main__":
    unittest.main()
