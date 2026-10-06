"""Width 14: the compiled search finds every planted text, and the cells stay with their shuffles."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_columnar14c import columnar14c_report, encrypt
from engine.solvers.dagapeyeff import consider_columnar14c


class DagapeyeffColumnar14cTest(unittest.TestCase):
    def test_each_direction_places_the_columns_as_stated(self) -> None:
        symbols = list(range(196))
        order = [3, 0, 13, 7, 1, 12, 2, 11, 4, 10, 5, 9, 6, 8]
        undone, source = encrypt(symbols, order, "undone")
        self.assertEqual(sorted(undone), symbols)
        self.assertEqual(undone, [symbols[i] for i in source])
        self.assertEqual(undone[order[0] * 14:order[0] * 14 + 3], [0, 14, 28])
        done, _ = encrypt(symbols, order, "done")
        self.assertEqual(done[:3], [order[0] * 14, order[1] * 14, order[2] * 14])

    def test_power_is_shown_and_the_cells_do_not_rise(self) -> None:
        report = columnar14c_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["planted_recovered"], {
            "undone errors 0": [6, 6],
            "undone errors 8": [3, 3],
            "done errors 0": [6, 6],
            "done errors 8": [3, 3],
        })
        weakest = min(row["found_per_letter"] for row in report["planted"])
        self.assertGreater(weakest, -2.7)
        for row in report["searched"].values():
            self.assertLess(row["per_letter"], weakest - 0.5)
            self.assertGreaterEqual(row["shuffles_as_high"], 5)
        claim = consider_columnar14c()
        self.assertFalse(claim["columnar14c_allowed"])


if __name__ == "__main__":
    unittest.main()
