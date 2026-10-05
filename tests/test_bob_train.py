"""A warm start that ties the shipped network does not replace it."""

from __future__ import annotations

import unittest

from engine.bob_train import bob_train_report
from engine.solvers.dagapeyeff import consider_bob_train

_SHIPPED = "5c271f426812d6307f208a636b80f820201e25b3dc6778333e5d08d4d5aaaf4b"


class BobTrainTest(unittest.TestCase):
    def test_the_warm_start_is_not_promoted(self) -> None:
        report = bob_train_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["weights_sha256"], _SHIPPED)
        self.assertFalse(report["weights_replaced"])
        self.assertTrue(report["weights_match_shipped"])
        self.assertEqual(report["epochs"], 16)
        self.assertEqual(report["train_per_class"], 32)
        self.assertEqual(report["checkpoint_epochs"], [0, 0, 0])
        self.assertEqual(report["held_before"], 429)
        self.assertEqual(report["held_after"], 429)
        self.assertEqual(report["held_total"], 480)
        self.assertEqual(report["held_top3"], 477)
        self.assertEqual(report["benchmark_before"], 193)
        self.assertEqual(report["benchmark_after"], 193)
        self.assertEqual(report["benchmark_total"], 204)
        self.assertTrue(report["internal_promoted"])
        self.assertFalse(report["scores_rose"])
        self.assertFalse(report["beat_lift"])
        self.assertEqual(report["lift_held"], 433)
        self.assertEqual(report["lift_benchmark"], 195)
        self.assertFalse(report["promoted"])
        claim = consider_bob_train()
        self.assertFalse(claim["bob_train_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIn("not replaced", claim["learned"])


if __name__ == "__main__":
    unittest.main()
