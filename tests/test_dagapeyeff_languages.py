"""The cipher scored as other languages, each against its own text."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_languages import language_report


class DagapeyeffLanguagesTest(unittest.TestCase):
    def test_no_sourced_language_fits(self) -> None:
        report = language_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["trials"], 30000)
        self.assertEqual(report["closest"], "french")
        self.assertEqual(report["closest_chi"], 21.36)
        rows = report["languages"]
        self.assertEqual(rows["english"]["chi"], 34.23)
        self.assertEqual(rows["english"]["as_flat"], 0)
        self.assertEqual(rows["english"]["prose_chi"], 4.16)
        self.assertEqual(rows["english"]["prose_as_flat"], 1598)
        self.assertEqual(rows["french"]["as_flat"], 2)
        self.assertEqual(rows["german"]["chi"], 38.04)
        self.assertEqual(rows["german"]["as_flat"], 0)
        self.assertEqual(rows["spanish"]["as_flat"], 2)
        self.assertEqual(rows["italian"]["chi"], 23.18)
        self.assertEqual(rows["italian"]["as_flat"], 6)
        self.assertEqual(rows["italian"]["prose_as_flat"], 0)
        self.assertEqual(rows["portuguese"]["as_flat"], 2)
        self.assertEqual(rows["dutch"]["chi"], 47.29)
        self.assertEqual(rows["dutch"]["as_flat"], 1)
        self.assertEqual(report["esperanto"]["chi"], 27.75)
        self.assertEqual(report["esperanto"]["as_flat"], 0)
        self.assertIs(report["english_prose_inside"], True)


if __name__ == "__main__":
    unittest.main()
