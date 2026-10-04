"""The published chi-square, enclosed, and the one-cell repair past it."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_convert import convert_report


class DagapeyeffConvertTest(unittest.TestCase):
    def test_the_record_ball_is_passed_and_the_repair_is_not_english(self) -> None:
        report = convert_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertIs(report["quadgram_comparable"], False)
        self.assertTrue(report["below_published_chi"])
        self.assertTrue(report["above_worst_english"])
        self.assertTrue(report["ioc_inside_published"])
        self.assertEqual(round(report["our_ioc"], 6), 0.069702)
        self.assertEqual(round(report["our_chi"]["lo"], 6), 34.174639)
        self.assertEqual(round(report["our_chi"]["hi"], 6), 34.292468)
        self.assertLess(report["our_chi"]["lo"], 34.23)
        self.assertGreater(report["our_chi"]["hi"], 34.23)
        self.assertEqual(report["repair_index"], 97)
        self.assertEqual(report["repairs"], 24)
        self.assertEqual(report["repairs_tied"], 7)
        self.assertEqual(report["repairs_worse"], 17)
        self.assertEqual(report["repairs_better"], 0)
        self.assertFalse(report["any_repair_reaches_english"])
        self.assertEqual(report["suggested_repair"], "75")
        self.assertTrue(report["suggested_worse"])
        self.assertFalse(report["suggested_reaches_english"])
        self.assertTrue(report["suggested_order_still_below_english"])
        self.assertLess(report["suggested_mi"]["hi"], report["english_mi"]["lo"])


if __name__ == "__main__":
    unittest.main()
