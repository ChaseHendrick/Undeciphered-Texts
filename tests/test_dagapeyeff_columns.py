"""A searched reading order can look word-like, and so can a shuffle."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_columns import column_report
from engine.solvers.dagapeyeff import consider_columns


class DagapeyeffRouteTest(unittest.TestCase):
    def test_the_column_search_is_not_a_reading(self) -> None:
        report = column_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["route_hits"], 544)
        self.assertEqual(report["route_width"], 27)
        self.assertEqual(report["route_read"], "down")
        self.assertEqual(report["column_draws"], 25000)
        self.assertEqual(report["column_best"], 581)
        self.assertEqual(report["null_grids"], 8)
        self.assertEqual(report["nulls_as_high"], 4)
        self.assertEqual(report["trials"], 225000)
        claim = consider_columns()
        self.assertFalse(claim["column_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIsNone(claim["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
