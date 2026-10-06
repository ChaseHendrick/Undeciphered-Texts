"""Straddling checkerboard and Nihilist substitution cannot give the cells' perfect digit alternation."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_digitcodes import alternation, digitcodes_report


class DagapeyeffDigitCodesTest(unittest.TestCase):
    def test_alternation(self) -> None:
        self.assertEqual(alternation("6172839405"), 1.0)
        self.assertLess(alternation("1111111111"), 1.0)

    def test_no_planted_text_reaches_the_cells(self) -> None:
        report = digitcodes_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["cells"], 1.0)
        for name, row in report["systems"].items():
            self.assertEqual(row["reaching_cells"], 0, name)
            self.assertLess(row["best"], 0.9, name)


if __name__ == "__main__":
    unittest.main()
