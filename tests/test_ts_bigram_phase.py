"""The pair grid is a repeat count, not a reading."""

from __future__ import annotations

import unittest

from engine.ts_bigram_phase import search_ts_bigram_phase


class TsBigramPhaseTest(unittest.TestCase):
    def test_print_aligned_pairs_repeat_and_nothing_is_claimed(self) -> None:
        report = search_ts_bigram_phase()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        rows = {(row["message"], row["drop_designator"]): row for row in report["rows"]}
        self.assertEqual(rows[("IASRZ_129", False)]["extra_repeats"], 9)
        self.assertEqual(rows[("IASRZ_129", False)]["random_at_least"], 0)
        self.assertEqual(rows[("DSZPZ", False)]["extra_repeats"], 8)
        self.assertEqual(rows[("DSZPZ", False)]["random_at_least"], 0)
        self.assertEqual(rows[("SSKFV", False)]["extra_repeats"], 4)
        self.assertEqual(rows[("SSKFV", False)]["random_at_least"], 0)
        self.assertEqual(rows[("SSKFV", True)]["extra_repeats"], 0)
        self.assertEqual(rows[("SSKFV", True)]["random_at_least"], 400)
        self.assertGreater(rows[("HOHOX", False)]["random_at_least"], 0)
        german = rows[("IASRZ_129", False)]["german"]
        self.assertLessEqual(german["low"], 9)
        self.assertGreaterEqual(german["high"], 9)
        alignment = report["alignment"]
        self.assertEqual(alignment["alignment_matches"], 33)
        self.assertEqual(alignment["consecutive_duos"], 21)
        self.assertEqual(alignment["null_high"], 24)
        self.assertIs(alignment["tighter_than_null"], False)


if __name__ == "__main__":
    unittest.main()
