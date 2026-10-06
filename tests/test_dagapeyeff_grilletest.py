"""A grille-specific order statistic has weak power, and the cells look like a no-message dealing on it."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_grilletest import grilletest_report


class DagapeyeffGrilleTestTest(unittest.TestCase):
    def test_weak_power_and_the_cells_among_their_dealings(self) -> None:
        report = grilletest_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(len(report["planted"]), 12)
        self.assertEqual(report["planted_above_all_dealings"], 4)
        self.assertGreaterEqual(report["cells"]["dealings_as_high"], 10)


if __name__ == "__main__":
    unittest.main()
