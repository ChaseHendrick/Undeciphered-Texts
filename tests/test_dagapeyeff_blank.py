"""Seven empty cells clear both re-pairings. Not a reading."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_blank import blank_report
from engine.solvers.dagapeyeff import consider_blank


class BlankTest(unittest.TestCase):
    def test_seven_empty_cells_clear_both_re_pairings(self) -> None:
        report = blank_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["empty"], 7)
        self.assertEqual(report["once_digit"], "0")
        self.assertEqual(report["once_empty"], 4)
        self.assertEqual(report["further"], ["61", "73", "95"])
        self.assertEqual(report["draws"], 20000)
        self.assertEqual(report["column_as_many"], 0)
        self.assertEqual(report["column_furthest"], 6)
        self.assertEqual(report["column_at_furthest"], 31)
        self.assertEqual(report["row_as_many"], 0)
        self.assertEqual(report["row_furthest"], 6)
        self.assertEqual(report["row_at_furthest"], 26)
        self.assertEqual(report["exercise_empty"], 3)
        self.assertEqual(report["exercise_column_as_many"], 2205)
        self.assertEqual(report["exercise_row_as_many"], 2280)
        self.assertTrue(report["allowed"])
        claim = consider_blank()
        self.assertTrue(claim["blank_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIsNone(claim["claimed_plaintext"])
        self.assertIn("exercise does not", claim["learned"])


if __name__ == "__main__":
    unittest.main()
