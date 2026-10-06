"""Chosen plain squares let English reach the cells' four-square side counts, so the count excludes only standard squares."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_fskeyed import fskeyed_report
from engine.solvers.dagapeyeff import consider_fskeyed


class DagapeyeffFskeyedTest(unittest.TestCase):
    def test_keyed_plain_squares_reach_the_cells(self) -> None:
        report = fskeyed_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["target"], [13, 18])
        self.assertEqual(report["windows"], 15)
        self.assertEqual(report["reaching"], 15)
        self.assertFalse(consider_fskeyed()["fskeyed_allowed"])


if __name__ == "__main__":
    unittest.main()
