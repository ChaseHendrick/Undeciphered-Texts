"""A keyword dictionary attack on the book's transpositions."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_keywords import _square, keyword_report, readings
from engine.solvers.dagapeyeff import consider_keywords


class DagapeyeffKeywordsTest(unittest.TestCase):
    def test_every_reading_is_a_permutation_and_the_square_inverts(self) -> None:
        text = ("ABCDEFGHIKLMNOPQRSTUVWXYZ" * 8)[:196]
        for keyword in ("SCHUVALOW", "CRYPTOGRAPHERS"):
            for _name, reading in readings(text, keyword):
                self.assertEqual(sorted(reading), sorted(text))
        keyword = "NMLKIHGFEDCBAZ"
        self.assertEqual(_square(_square(text, keyword, undo=False), keyword, undo=True), text)

    def test_planted_keywords_surface_and_the_cells_do_not(self) -> None:
        report = keyword_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["keywords"], 379521)
        self.assertEqual(report["orders_scored"], 2208702)
        self.assertEqual(report["plants_ranked_first"], 4)
        for plant in report["plants"]:
            self.assertGreaterEqual(plant["top_mi"], plant["true_mi"])
            self.assertGreater(plant["top_mi"], max(report["null_best_mi"]))
        self.assertEqual(report["cells_best_mi"], 0.8161)
        self.assertLess(report["cells_best_mi"], max(report["null_best_mi"]))
        for row in report["top_solved"]:
            self.assertLess(row["per_letter"], -3.5)
        claim = consider_keywords()
        self.assertFalse(claim["keywords_allowed"])


if __name__ == "__main__":
    unittest.main()
