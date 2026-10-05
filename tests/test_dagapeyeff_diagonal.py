"""Empty cells on the two diagonals. Not a reading."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_diagonal import diagonal_report
from engine.solvers.dagapeyeff import consider_diagonal


class DagapeyeffDiagonalTest(unittest.TestCase):
    def test_the_empty_cells_survive_both_diagonals(self) -> None:
        report = diagonal_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["main_zeros"], 2)
        self.assertEqual(report["anti_zeros"], 1)
        self.assertEqual(report["either_zeros_as_many"], 1193)
        self.assertEqual(report["sum_either"], 21907)
        self.assertEqual(report["control_main_zeros"], 2)
        self.assertEqual(report["control_either_zeros_as_many"], 3357)
        self.assertEqual(report["draws"], 100000)
        self.assertLess(report["either_zeros_as_many"] / report["draws"], 0.05)
        self.assertGreater(report["sum_either"] / report["draws"], 0.05)
        self.assertLess(report["control_either_zeros_as_many"] / report["draws"], 0.05)
        claim = consider_diagonal()
        self.assertTrue(claim["diagonal_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIn("Not a reading", claim["learned"])


if __name__ == "__main__":
    unittest.main()
