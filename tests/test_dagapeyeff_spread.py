"""The exercise has an uneven line. The challenge does not share it."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_spread import spread_report
from engine.solvers.dagapeyeff import consider_spread


class DagapeyeffSpreadTest(unittest.TestCase):
    def test_the_exercise_stays_rare_when_columns_count(self) -> None:
        report = spread_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["row_line"], [1, 9, 0, 14, 17])
        self.assertEqual(report["column_line"], [0, 1, 20, 12, 0])
        self.assertEqual(report["rows_as_uneven"], 112)
        self.assertEqual(report["columns_as_uneven"], 3337)
        self.assertEqual(report["either_as_uneven"], 3345)
        self.assertEqual(report["control_either_as_uneven"], 250)
        self.assertEqual(report["draws"], 20000)
        self.assertLess(report["control_either_as_uneven"] / report["draws"], 0.05)
        self.assertGreater(report["either_as_uneven"] / report["draws"], 0.05)
        claim = consider_spread()
        self.assertTrue(claim["spread_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIn("Not a reading", claim["learned"])


if __name__ == "__main__":
    unittest.main()
