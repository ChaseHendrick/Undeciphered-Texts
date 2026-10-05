"""Spiral, snake and zigzag routes do not beat shuffled cells."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_spiral import routes, spiral_report
from engine.solvers.dagapeyeff import consider_spiral


class DagapeyeffSpiralTest(unittest.TestCase):
    def test_every_route_visits_every_cell_once(self) -> None:
        table = routes()
        self.assertEqual(len(table), 16)
        for path in table.values():
            self.assertEqual(sorted(path), list(range(196)))

    def test_the_best_route_is_ordinary(self) -> None:
        report = spiral_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["readings"], 32)
        self.assertEqual(report["best_mi"], 0.686)
        self.assertEqual(report["shuffles_as_high"], 567)
        self.assertLess(report["best_mi"], report["english_mi"])
        claim = consider_spiral()
        self.assertFalse(claim["spiral_allowed"])
        self.assertIs(claim["solved"], False)


if __name__ == "__main__":
    unittest.main()
