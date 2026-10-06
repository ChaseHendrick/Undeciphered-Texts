"""Every order up to width 9: planted texts stand out, the cells do not."""

from __future__ import annotations

import unittest

import numpy as np

from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_exhaustive import _positions, exhaustive_report, information
from engine.dagapeyeff_order import _mi
from engine.solvers.adfgvx import columnar_decrypt, columnar_encrypt
from engine.solvers.dagapeyeff import consider_exhaustive


class DagapeyeffExhaustiveTest(unittest.TestCase):
    def test_vectorized_readings_match_the_repository_transposition(self) -> None:
        cells = np.asarray(_cells())
        self.assertAlmostEqual(information(cells[None, :])[0], _mi(list(cells)), places=12)
        text = "".join(chr(65 + c) for c in cells)
        keyword = "ZEBRAS"
        order = np.asarray([sorted(range(6), key=lambda i: (keyword[i], i))])
        done = _positions("columnar-done", 6, order)[0]
        undone = _positions("columnar-undone", 6, order)[0]
        self.assertEqual("".join(text[p] for p in done), columnar_encrypt(text, keyword))
        self.assertEqual("".join(text[p] for p in undone), columnar_decrypt(text, keyword))

    def test_planted_texts_stand_out_and_the_cells_do_not(self) -> None:
        report = exhaustive_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(len(report["rows"]), 24)
        for row in report["rows"]:
            weakest = min(plant["excess"] for plant in row["planted"])
            self.assertGreater(weakest, 0)
            self.assertLess(row["cells"]["excess"], weakest)
            self.assertLess(row["regrouped"]["excess"], weakest)
        self.assertEqual(report["cells_highest_mi"], 0.7969)
        self.assertEqual(report["planted_lowest_true_mi"], 1.0102)
        claim = consider_exhaustive()
        self.assertFalse(claim["exhaustive_allowed"])


if __name__ == "__main__":
    unittest.main()
