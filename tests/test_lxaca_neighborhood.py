"""LXACA neighborhood stays a supplied-key check, not a claimed reading."""

from __future__ import annotations

import unittest

from engine.lxaca_neighborhood import search_lxaca_neighborhood


class LxacaNeighborhoodTest(unittest.TestCase):
    def test_controls_match_and_no_plaintext_is_claimed(self) -> None:
        report = search_lxaca_neighborhood()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        controls = report["controls"]
        self.assertEqual(controls["derop_start"], "WER")
        self.assertTrue(controls["derop_prefix_matches_control"])
        self.assertEqual(controls["weuwy_corrected_start"], "SPE")
        self.assertEqual(controls["weuwy_printed_start"], "SPF")
        by_date = {row["date"]: row for row in report["published_days"]}
        self.assertEqual(by_date["1941-07-05"]["start"], "LXI")
        self.assertEqual(len(report["published_days"]), 6)
        self.assertEqual(report["july5_indicator_edits"], 152)
        self.assertEqual(report["edits_beating_control"], 1)
        self.assertEqual(report["best_edit"]["machine_output"], "WOYUCFRSONAGVWOPOABE")
        self.assertNotIn("BETRIEB", report["best_edit"]["machine_output"])


if __name__ == "__main__":
    unittest.main()
