"""Clerk habits are counted. They are not a reading."""

from __future__ import annotations

import unittest

from engine.ts_clerk import search_ts_clerk


class TsClerkTest(unittest.TestCase):
    def test_habits_and_the_extra_group_do_not_yield_a_reading(self) -> None:
        report = search_ts_clerk()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["iasrz_second_group"], "EDSTB")
        self.assertTrue(report["iasrz_openings_match"])
        self.assertEqual(report["f8y_second_groups"], ("EGDOK", "WSWGG"))
        self.assertEqual(report["f8y_shared_tail"], "LMOTIYIZ")
        hearing = report["hearing"]
        self.assertEqual(hearing["same"], 33)
        self.assertEqual(hearing["substituted"], 20)
        self.assertEqual(hearing["gaps"], 4)
        self.assertEqual(hearing["opening_matches_in_10"], 8)
        self.assertEqual(len(report["hohox_drops"]), 11)
        self.assertEqual(report["hohox_max_extra_repeats"], 2)
        self.assertTrue(all(row["random_at_least"] > 0 for row in report["hohox_drops"]))
        self.assertEqual(report["hohox_drops"][1]["random_at_least"], 26)


if __name__ == "__main__":
    unittest.main()
