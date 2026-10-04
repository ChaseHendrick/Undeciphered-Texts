"""Reorderings of the 1939 cells versus same-length prose. Not a reading."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_order import order_report


class DagapeyeffOrderTest(unittest.TestCase):
    def test_no_reordering_reaches_prose(self) -> None:
        report = order_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["trials"], 45000)
        self.assertEqual(report["printed_mi"], 0.5706)
        self.assertEqual(report["down_mi"], 0.6684)
        self.assertEqual(report["best_row_key_mi"], 0.7657)
        self.assertEqual(report["best_down_key_mi"], 0.7141)
        self.assertEqual(report["random_max_mi"], 0.7556)
        self.assertEqual(report["random_at_least_printed"], 4164)
        self.assertEqual(report["english_mi"], 1.0658)
        self.assertEqual(report["english_relabel_mi"], 1.0658)
        self.assertEqual(report["german_mi"], 1.2)
        self.assertEqual(report["book_letters"], 92)
        self.assertEqual(report["book_mi"], 1.5282)
        self.assertLess(report["best_row_key_mi"], report["english_mi"])


if __name__ == "__main__":
    unittest.main()
