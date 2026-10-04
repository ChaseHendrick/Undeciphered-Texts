"""A fourth move from the best three-move states can match English counts. It is not a reading."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_depth4 import depth4_report
from engine.solvers.dagapeyeff import consider_depth4


class DagapeyeffDepth4Test(unittest.TestCase):
    def test_the_fourth_move_clears_counts_only(self) -> None:
        report = depth4_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["tied_after_three"], 140)
        self.assertEqual(report["fourth_states"], 52003)
        self.assertEqual(report["best_chi"], 22.4243)
        self.assertEqual(report["point_under_line"], 18760)
        self.assertEqual(report["ball_lo"], 22.377631)
        self.assertEqual(report["ball_hi"], 22.471061)
        self.assertEqual(report["english_line"], 24.165)
        self.assertTrue(report["ball_clears"])
        claim = consider_depth4()
        self.assertFalse(claim["depth4_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIsNone(claim["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
