"""The close Truppenschlüssel pairs are measured, not read."""

from __future__ import annotations

import unittest

from engine.ts_close_pairs import search_ts_close_pairs


class TsClosePairsTest(unittest.TestCase):
    def test_pairs_are_related_and_no_plaintext_is_claimed(self) -> None:
        report = search_ts_close_pairs()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        iasrz = report["iasrz"]
        self.assertEqual(iasrz["full_lengths"], (90, 52))
        self.assertEqual(iasrz["shared_prefix"], "IASRZEDSTB")
        self.assertEqual(iasrz["body_lengths"], (85, 47))
        self.assertIs(iasrz["bodies_even"], False)
        same = report["same_time"]
        self.assertEqual(same["ungapped_matches"], 11)
        self.assertEqual(same["ungapped_compared"], 53)
        self.assertEqual(same["alignment_matches"], 33)
        self.assertLess(same["null_max_matches"], 33)
        self.assertTrue(same["above_null"])
        self.assertEqual(report["shared_ending"]["shared_suffix"], "LMOTIYIZ")
        self.assertEqual(report["shared_ending"]["printed_lengths"], (60, 55))
        self.assertEqual(report["shared_ending"]["form_lengths"], (60, 50))


if __name__ == "__main__":
    unittest.main()
