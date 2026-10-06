"""The old leads, rerun with a strong solver and family-wise shuffles, point nowhere."""

from __future__ import annotations

import random
import unittest

from engine.dagapeyeff_direction import (
    _column_order, _rail_order, delay, direction_report, do, drop, undelay, undo,
)
from engine.solvers.dagapeyeff import consider_direction


class DagapeyeffDirectionTest(unittest.TestCase):
    def test_every_transform_has_an_inverse(self) -> None:
        rng = random.Random(1)
        cells = [rng.randrange(25) for _ in range(196)]
        for d in (1, 79, 195):
            self.assertEqual(delay(undelay(cells, d), d), cells)
        for rails in (2, 7, 14):
            order = _rail_order(196, rails)
            self.assertEqual(undo(do(cells, order), order), cells)
        for width in (10, 19, 28):
            order = _column_order(196, width)
            self.assertEqual(undo(do(cells, order), order), cells)
        self.assertEqual(len(drop(cells, 3, 1)), 131)

    def test_no_family_beats_its_shuffles(self) -> None:
        report = direction_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["search"]["transforms"], 363)
        self.assertEqual(report["planted_recovered"], 4)
        floor = report["planted_lowest_true"]
        for name, family in report["families"].items():
            self.assertGreaterEqual(family["shuffle_bests_as_high"], 7, name)
            self.assertLess(family["cells_best"], floor - 1.0)
        claim = consider_direction()
        self.assertFalse(claim["direction_allowed"])


if __name__ == "__main__":
    unittest.main()
