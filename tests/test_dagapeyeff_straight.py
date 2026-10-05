"""Four counts in a row that differ by one. Not a reading."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_straight import straight_report
from engine.solvers.dagapeyeff import consider_straight


class DagapeyeffStraightTest(unittest.TestCase):
    def test_the_straight_survives_both_directions(self) -> None:
        report = straight_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["strict_row"], [12, 3, 2, 1, 0])
        self.assertEqual(report["row_length"], 4)
        self.assertEqual(report["column_length"], 2)
        self.assertEqual(report["rows_as_long"], 1237)
        self.assertEqual(report["columns_as_long"], 0)
        self.assertEqual(report["either_as_long"], 1237)
        self.assertEqual(report["control_rows_as_long"], 5113)
        self.assertEqual(report["draws"], 100000)
        self.assertLess(report["either_as_long"] / report["draws"], 0.05)
        self.assertGreater(report["control_rows_as_long"] / report["draws"], 0.05)
        claim = consider_straight()
        self.assertTrue(claim["straight_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIn("Not a reading", claim["learned"])


if __name__ == "__main__":
    unittest.main()
