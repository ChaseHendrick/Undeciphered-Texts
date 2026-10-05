"""The lifted ranking holds both bars. The weight file stays."""

from __future__ import annotations

import unittest

from engine.bob_lift import bob_lift_report
from engine.solvers.dagapeyeff import consider_bob_lift

_SHIPPED = "5c271f426812d6307f208a636b80f820201e25b3dc6778333e5d08d4d5aaaf4b"


class BobLiftTest(unittest.TestCase):
    def test_majority_and_the_sure_vote_hold_both_bars(self) -> None:
        report = bob_lift_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["weights_sha256"], _SHIPPED)
        self.assertFalse(report["weights_replaced"])
        self.assertTrue(report["weights_match_shipped"])
        self.assertEqual(report["train_correct"], 155)
        self.assertEqual(report["train_total"], 200)
        self.assertEqual(report["sure"], 0.8)
        self.assertEqual(report["margin"], 0.7)
        self.assertEqual(report["held_before"], 429)
        self.assertEqual(report["held_after"], 433)
        self.assertEqual(report["held_total"], 480)
        self.assertEqual(report["held_flips"], 8)
        self.assertEqual(report["held_corrections"], 6)
        self.assertEqual(report["held_mistakes"], 2)
        self.assertEqual(report["held_top3"], 477)
        self.assertEqual(report["benchmark_before"], 193)
        self.assertEqual(report["benchmark_after"], 195)
        self.assertEqual(report["benchmark_total"], 204)
        self.assertEqual(report["benchmark_flips"], 2)
        self.assertEqual(report["benchmark_corrections"], 2)
        self.assertEqual(report["benchmark_mistakes"], 0)
        self.assertEqual(report["benchmark_top3"], 204)
        self.assertTrue(report["promoted"])
        claim = consider_bob_lift()
        self.assertTrue(claim["bob_lift_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIsNone(claim["claimed_plaintext"])
        self.assertIn("weight file stays", claim["learned"])
        self.assertIn("not 480 of 480", claim["learned"])


if __name__ == "__main__":
    unittest.main()
