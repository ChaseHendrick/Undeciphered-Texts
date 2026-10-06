"""Four-square: the side counts exclude it on the cells, and the search finds nothing English."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_foursquare import PLAIN, encrypt, foursquare_report, sides
from engine.solvers.dagapeyeff import consider_foursquare


class DagapeyeffFoursquareTest(unittest.TestCase):
    def test_each_side_depends_only_on_rows_and_columns(self) -> None:
        identity = list(range(25))
        h_row, h_column = divmod(PLAIN.index("H"), 5)
        e_row, e_column = divmod(PLAIN.index("E"), 5)
        self.assertEqual(encrypt("HE", identity, identity), [h_row * 5 + e_column, e_row * 5 + h_column])
        self.assertEqual(sides([0, 1, 0, 2, 3, 2]), (2, 2))

    def test_the_cells_are_excluded_by_count_and_do_not_score_as_english(self) -> None:
        report = foursquare_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        counts = report["counts"]
        self.assertEqual(counts["texts"]["cells"]["pairs-from-first"], [13, 18])
        self.assertEqual(counts["texts"]["regrouped"]["pairs-from-first"], [21, 19])
        self.assertEqual(counts["keyed_draws"], 7400)
        self.assertEqual(counts["keyed_fewest_larger_side"], 20)
        self.assertEqual(counts["keyed_reaching_cells"], 0)
        self.assertEqual(counts["standard_reaching_cells"], 0)
        self.assertEqual(report["planted_recovered"], 4)
        self.assertEqual(len(report["planted"]), 6)
        floor = report["planted_lowest_true"]
        for row in report["searched"].values():
            self.assertLess(row["per_letter"], floor - 1.0)
            self.assertGreaterEqual(row["shuffles_as_high"], 9)
        claim = consider_foursquare()
        self.assertFalse(claim["foursquare_allowed"])


if __name__ == "__main__":
    unittest.main()
