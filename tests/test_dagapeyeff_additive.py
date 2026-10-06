"""A repeating coordinate shift on a keyed square: excluded by a count, and the joint search finds nothing English."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_additive import PLAIN, additive_report, encrypt
from engine.solvers.dagapeyeff import consider_additive


class DagapeyeffAdditiveTest(unittest.TestCase):
    def test_the_shift_moves_row_and_column_modulo_five(self) -> None:
        square = list(range(25))
        a_cell = PLAIN.index("A")
        self.assertEqual(encrypt("AA", square, [(0, 0), (1, 2)]), [a_cell, (1 * 5 + 2)])
        self.assertEqual(encrypt("Z", square, [(1, 1)]), [((4 + 1) % 5) * 5 + (4 + 1) % 5])

    def test_no_english_draw_reaches_the_cells_and_the_search_finds_nothing(self) -> None:
        report = additive_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        counts = report["counts"]
        self.assertEqual(counts["cells"], {"distinct": 18, "top_three_rows": 177})
        self.assertEqual(sum(row["draws"] for row in counts["rows"]), 16470)
        self.assertEqual(sum(row["reaching_cells"] for row in counts["rows"]), 0)
        self.assertEqual(min(row["fewest_distinct"] for row in counts["rows"]), 20)
        self.assertEqual(report["planted_recovered"], 11)
        self.assertEqual(len(report["planted"]), 12)
        self.assertLess(report["searched_best"], report["planted_lowest_true"] - 1.0)
        claim = consider_additive()
        self.assertFalse(claim["additive_allowed"])


if __name__ == "__main__":
    unittest.main()
