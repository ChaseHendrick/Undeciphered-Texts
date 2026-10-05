"""The order left after the rare column is pinned. Not a reading."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_residual import residual_report
from engine.solvers.dagapeyeff import consider_residual


class DagapeyeffResidualTest(unittest.TestCase):
    def test_no_residual_score_clears_and_the_exercise_still_does(self) -> None:
        report = residual_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["pinned"], 8)
        self.assertEqual(report["draws"], 10000)
        self.assertEqual(len(report["scores"]), 7)
        self.assertEqual(report["best_name"], "step")
        self.assertEqual(report["best_tail"], 1549)
        self.assertGreater(report["best_tail"] / report["draws"], 0.05)
        self.assertEqual(report["control_trigram_high"], 59)
        self.assertLess(report["control_trigram_high"] / report["draws"], 0.05)
        claim = consider_residual()
        self.assertFalse(claim["residual_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIn("Not a reading", claim["learned"])


if __name__ == "__main__":
    unittest.main()
