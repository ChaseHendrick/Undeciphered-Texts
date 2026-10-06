"""Every double columnar transposition up to width 6: planted texts stand out, the cells do not."""

from __future__ import annotations

import random
import unittest

import numpy as np

from engine.dagapeyeff_double import _plant, double_report
from engine.dagapeyeff_exhaustive import _positions
from engine.solvers.dagapeyeff import consider_double


class DagapeyeffDoubleTest(unittest.TestCase):
    def test_two_passes_read_a_planted_text_back(self) -> None:
        rng = random.Random(4)
        plain = np.asarray([rng.randrange(25) for _ in range(196)], dtype=np.int64)
        outer = _positions("columnar-undone", 4, np.asarray([[1, 0, 3, 2]]))[0]
        inner = _positions("columnar-undone", 5, np.asarray([[4, 2, 0, 1, 3]]))[0]
        cipher = np.empty(196, dtype=np.int64)
        cipher[outer[inner]] = plain
        self.assertTrue(np.array_equal(cipher[outer][inner], plain))
        self.assertEqual(len(_plant("ABCDEFGHIK" * 20, 0, "columnar-done", 3, 6, random.Random(1))), 196)

    def test_the_cells_stay_below_every_planted_text(self) -> None:
        report = double_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["cases"], 50)
        self.assertEqual(report["cases_cells_below_planted"], 50)
        for row in report["rows"]:
            weakest = min(plant["excess"] for plant in row["planted"])
            self.assertGreater(weakest, 0)
            self.assertLess(row["cells"]["excess"], weakest)
        claim = consider_double()
        self.assertFalse(claim["double_allowed"])


if __name__ == "__main__":
    unittest.main()
