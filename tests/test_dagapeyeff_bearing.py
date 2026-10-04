"""The order depends on the last column, and still is not prose."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_bearing import bearing_report


class DagapeyeffBearingTest(unittest.TestCase):
    def test_only_the_last_column_carries_the_order(self) -> None:
        report = bearing_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["trials"], 140000)
        self.assertEqual(
            report["scores"],
            (
                0.614, 0.6636, 0.619, 0.5655, 0.5737, 0.6741, 0.6407,
                0.6019, 0.6227, 0.6046, 0.6103, 0.5975, 0.6025, 0.4514,
            ),
        )
        self.assertEqual(report["lowest_column"], 13)
        self.assertEqual(report["lowest_mi"], 0.4514)
        self.assertEqual(report["next_lowest_mi"], 0.5655)
        self.assertEqual(report["highest_column"], 5)
        self.assertEqual(report["full_mi"], 0.5706)
        self.assertEqual(report["english_mi"], 1.1264)
        self.assertEqual(report["as_low"], 0)
        self.assertEqual(report["gap_as_wide"], 0)
        self.assertLess(report["lowest_mi"], report["english_mi"])


if __name__ == "__main__":
    unittest.main()
