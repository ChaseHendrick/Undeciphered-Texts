"""Columnar transposition under a letter key, with planted controls."""

from __future__ import annotations

import random
import unittest

from engine.dagapeyeff_columnar import columnar_encrypt, columnar_report, read_positions
from engine.solvers.dagapeyeff import consider_columnar


class DagapeyeffColumnarTest(unittest.TestCase):
    def test_reading_undoes_the_encryption(self) -> None:
        rng = random.Random(5)
        plain = [rng.randrange(26) for _ in range(196)]
        for width in (1, 2, 4, 7, 14):
            order = list(range(width))
            rng.shuffle(order)
            cipher = columnar_encrypt(plain, width, order)
            inverse = [order.index(column) for column in range(width)]
            self.assertEqual([cipher[i] for i in read_positions(width, inverse)], plain)

    def test_small_widths_have_power_and_the_cells_do_not_read(self) -> None:
        report = columnar_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        rows = {row["width"]: row for row in report["rows"]}
        for width in (1, 2, 4, 7):
            self.assertEqual(rows[width]["planted_recovered"], 2)
            self.assertLess(rows[width]["cells_per_letter"], -3.8)
            self.assertGreaterEqual(rows[width]["shuffles_as_high"], 1)
        self.assertEqual(rows[14]["planted_recovered"], 0)
        self.assertEqual(rows[14]["cells_per_letter"], -3.4168)
        self.assertLess(report["best_cells_per_letter"], report["lowest_planted_true_per_letter"] - 1.0)
        claim = consider_columnar()
        self.assertFalse(claim["columnar_allowed"])
        self.assertIs(claim["solved"], False)


if __name__ == "__main__":
    unittest.main()
