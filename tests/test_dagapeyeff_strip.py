"""Cutting out the private symbols does not uncover a reading."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_strip import strip_report


class DagapeyeffStripTest(unittest.TestCase):
    def test_removing_the_private_symbols_makes_the_rest_flatter(self) -> None:
        report = strip_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["removed"], ("04", "71", "92", "93", "94"))
        self.assertEqual(report["kept"], 188)
        self.assertEqual(report["full_mi"], 0.5706)
        self.assertEqual(report["kept_mi"], 0.4174)
        self.assertEqual(report["english_mi"], 1.0946)
        self.assertEqual(report["german_mi"], 1.2359)
        self.assertEqual(report["kept_as_high"], 8449)
        self.assertEqual(report["drop_as_high"], 10000)
        self.assertEqual(report["bundle_as_high"], 5000)
        self.assertEqual(report["trials"], 25000)
        self.assertLess(report["kept_mi"], report["english_mi"])


if __name__ == "__main__":
    unittest.main()
