"""Five short attacks: nulls by place, rare symbols as spaces, column digits alone, and the cells reversed."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_quick import coincidence, drop_phase, quick_report, rare_symbols
from engine.solvers.dagapeyeff import consider_quick


class DagapeyeffQuickTest(unittest.TestCase):
    def test_helpers(self) -> None:
        self.assertEqual(drop_phase([0, 1, 2, 3, 4, 5], 3, 1), [0, 2, 3, 5])
        self.assertEqual(coincidence([1, 1, 2, 2]), 2 * 2 / 12)
        self.assertEqual(sorted(rare_symbols(_cells())), [5, 16, 17, 18, 23])

    def test_no_short_attack_reads_as_english(self) -> None:
        report = quick_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["planted_recovered"], len(report["planted"]))
        floor = report["planted_lowest_true"]
        self.assertLess(report["searched_best"]["per_letter"], floor - 1.0)
        spaces = report["spaces"]
        self.assertEqual((spaces["separators"], spaces["distinct_letters"]), (8, 13))
        self.assertGreater(spaces["mean_word_length"], 2 * spaces["english_longest_mean_word"])
        self.assertGreater(spaces["english_fewest_distinct"], spaces["distinct_letters"])
        for row in report["column_digits"].values():
            self.assertEqual(row["english_at_or_below"], 0)
        claim = consider_quick()
        self.assertFalse(claim["quick_allowed"])


if __name__ == "__main__":
    unittest.main()
