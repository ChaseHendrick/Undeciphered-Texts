"""Periodic independent alphabets: no English window comes within 8 errors of the cells' per-phase counts."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_phases import phase_errors, phases_report
from engine.dagapeyeff_errors import sorted_counts


class DagapeyeffPhasesTest(unittest.TestCase):
    def test_phase_errors_sum_over_phases(self) -> None:
        text = [0, 1, 0, 1, 0, 1]
        targets = [sorted_counts([5, 5, 5]), sorted_counts([6, 7, 6])]
        self.assertEqual(phase_errors(text, targets, 2), 1)

    def test_no_window_within_eight_errors(self) -> None:
        report = phases_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        for row in report["rows"]:
            self.assertEqual(row["within_8"], 0, row["period"])
            self.assertGreaterEqual(row["fewest"], 13, row["period"])


if __name__ == "__main__":
    unittest.main()
