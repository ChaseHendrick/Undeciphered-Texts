"""The frequency hole and the period-7 claim. Not a reading."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_hole import hole_report
from engine.solvers.dagapeyeff import consider_hole


class DagapeyeffHoleTest(unittest.TestCase):
    def test_the_low_side_is_new_and_the_period_is_not(self) -> None:
        report = hole_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["occupied"], [1, 2, 3, 9, 11, 12, 14, 15, 16, 17, 20])
        self.assertEqual((report["low_max"], report["high_min"], report["gap"]), (3, 9, 6))
        self.assertEqual(report["low_cells"], 8)
        self.assertEqual(report["low_in_named_column"], 8)
        self.assertEqual(report["already_recorded_cells"], 5)
        self.assertEqual(report["new_cells"], 3)
        self.assertEqual((report["step_numerator"], report["step_denominator"]), (4, 54435))
        self.assertLess(report["step_numerator"] / report["step_denominator"], 0.05)
        self.assertEqual(report["high_in_named_column"], 0)
        self.assertEqual(report["period7_as_high"], 1088)
        self.assertGreater(report["period7_as_high"] / report["period7_draws"], 0.05)
        claim = consider_hole()
        self.assertFalse(claim["hole_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIn("Neither is a reading", claim["learned"])


if __name__ == "__main__":
    unittest.main()
