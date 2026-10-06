"""The 13 common symbols are as flat as uniform draws."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_body import body_report, top_flatness
from engine.solvers.dagapeyeff import consider_body


class DagapeyeffBodyTest(unittest.TestCase):
    def test_flatness_of_equal_counts_is_zero(self) -> None:
        self.assertEqual(top_flatness([10] * 13 + [1, 1]), 0.0)

    def test_the_body_is_uniform_like_and_rare_in_prose(self) -> None:
        report = body_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["common_counts"], [20, 17, 17, 17, 17, 16, 15, 14, 12, 12, 11, 11, 9])
        self.assertEqual(report["cells_top13_chi"], 8.66)
        self.assertEqual(report["windows_as_flat"], 194)
        self.assertEqual(report["uniform_as_flat_or_flatter"], 5274)
        self.assertLess(report["cells_top13_chi"], report["uniform_median"])
        self.assertLess(report["cells_top13_chi"], report["window_top13_chi_median"])
        claim = consider_body()
        self.assertFalse(claim["body_allowed"])


if __name__ == "__main__":
    unittest.main()
