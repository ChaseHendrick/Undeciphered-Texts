"""One row of the square steps down. Not a reading."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_monotone import monotone_report
from engine.solvers.dagapeyeff import consider_monotone


class DagapeyeffMonotoneTest(unittest.TestCase):
    def test_the_row_clears_and_the_two_directions_do_not(self) -> None:
        report = monotone_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["strict_row"], [12, 3, 2, 1, 0])
        self.assertEqual(report["strict_rows"], 1)
        self.assertEqual(report["strict_columns"], 0)
        self.assertEqual(report["rows_with_one"], 1432)
        self.assertEqual(report["either_with_one"], 5768)
        self.assertEqual(report["draws"], 100000)
        self.assertLess(report["rows_with_one"] / report["draws"], 0.05)
        self.assertGreater(report["either_with_one"] / report["draws"], 0.05)
        claim = consider_monotone()
        self.assertFalse(claim["monotone_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIn("Not a reading", claim["learned"])


if __name__ == "__main__":
    unittest.main()
