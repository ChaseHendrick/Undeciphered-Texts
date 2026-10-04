"""Distance from a published chi-square, and from English. Not a reading."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_record import record_report


class DagapeyeffRecordTest(unittest.TestCase):
    def test_the_cells_beat_a_published_chi_and_still_miss_english(self) -> None:
        report = record_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["our_chi"], 34.23)
        self.assertEqual(report["published_chi"], 49.23)
        self.assertEqual(report["ahead_of_published_chi"], 15.0)
        self.assertEqual(report["english_worst_chi"], 24.17)
        self.assertEqual(report["english_median_chi"], 7.44)
        self.assertEqual(report["above_worst_english"], 10.06)
        self.assertEqual(report["above_median_english"], 26.79)
        self.assertEqual(report["flatter_than_challenge"], 0)
        self.assertEqual(report["legal_reorder"], "01432")
        self.assertEqual(report["legal_reorder_chi"], 8.86)
        self.assertEqual(report["legal_reorder_above_median"], 1.42)
        self.assertEqual(report["cipher_mi"], 0.5706)
        self.assertEqual(report["english_mi"], 1.0658)
        self.assertEqual(report["order_gap"], 0.4952)
        self.assertEqual(report["order_gap_closed"], 0)


if __name__ == "__main__":
    unittest.main()
