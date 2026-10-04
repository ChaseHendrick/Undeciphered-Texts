"""The repetitive column is not filler."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_column_null import column_null_report
from engine.solvers.dagapeyeff import consider_column_null


class DagapeyeffColumnNullTest(unittest.TestCase):
    def test_dropping_a_column_does_not_reach_prose(self) -> None:
        report = column_null_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["columns"], 14)
        self.assertEqual(report["kept_after_column"], 182)
        self.assertEqual(report["best_column"], 5)
        self.assertEqual(report["best_quadgram"], -3.3208)
        self.assertEqual(report["fourth_column"], 3)
        self.assertEqual(report["fourth_quadgram"], -3.6511)
        self.assertEqual(report["mode_dropped"], 6)
        self.assertEqual(report["mode_quadgram"], -3.5794)
        self.assertEqual(report["prose_quadgram"], -2.5185)
        self.assertFalse(report["reaches_prose"])
        self.assertEqual(report["draws"], 80)
        self.assertEqual(report["best_shuffles_as_high"], 12)
        self.assertEqual(report["fourth_shuffles_as_high"], 77)
        self.assertEqual(report["mode_shuffles_as_high"], 58)
        claim = consider_column_null()
        self.assertFalse(claim["column_null_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIsNone(claim["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
