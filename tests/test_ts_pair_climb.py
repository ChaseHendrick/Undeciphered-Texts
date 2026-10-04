"""Joint climbs may beat a shuffle and still not be a reading."""

from __future__ import annotations

import unittest

from engine.ts_pair_climb import search_ts_pair_climb

_SCORES = {
    "iasrz_designator_included": (362, 332),
    "iasrz_drop_first": (448, 324),
    "iasrz_drop_last": (414, 382),
    "ending_drop_first": (379, 278),
    "ending_drop_last": (304, 292),
    "time_1735_drop_first": (559, 415),
    "time_1735_drop_last": (578, 355),
}


class TsPairClimbTest(unittest.TestCase):
    def test_every_window_beats_its_shuffle_and_none_is_claimed(self) -> None:
        report = search_ts_pair_climb()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["lanes_beating_null"], 7)
        by_name = {lane["name"]: lane for lane in report["lanes"]}
        self.assertEqual(set(by_name), set(_SCORES))
        for name, (real, null) in _SCORES.items():
            self.assertEqual(by_name[name]["real_score"], real)
            self.assertEqual(by_name[name]["null_score"], null)
            self.assertTrue(by_name[name]["beat_null"])
            self.assertNotIn("plaintext", by_name[name])
        self.assertTrue(by_name["iasrz_drop_first"]["beat_null"])
        self.assertTrue(by_name["iasrz_drop_last"]["beat_null"])


if __name__ == "__main__":
    unittest.main()
