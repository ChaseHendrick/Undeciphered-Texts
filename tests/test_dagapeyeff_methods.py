"""Rank measurements by whether their own null can see the challenge."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_methods import method_report


class DagapeyeffMethodsTest(unittest.TestCase):
    def test_two_methods_see_it_and_three_do_not(self) -> None:
        report = method_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["trials"], 37000)
        self.assertEqual(report["column_width"], 14)
        self.assertEqual(report["column_index"], 13)
        self.assertEqual(report["column_draws"], 10000)
        self.assertEqual(report["column_as_extreme"], 0)
        self.assertEqual(report["digram_excess"], 65)
        self.assertEqual(report["digram_shuffle_at_least"], 8076)
        self.assertEqual(report["challenge_chi"], 34.23)
        self.assertEqual(report["english_max_chi"], 32.65)
        self.assertEqual(report["english_as_flat"], 0)
        self.assertEqual(report["control_chi"], 4.14)
        self.assertEqual(report["first_half_chi"], 15.61)
        self.assertEqual(report["second_half_chi"], 17.24)
        self.assertEqual(report["first_half_as_flat"], 61)
        self.assertEqual(report["second_half_as_flat"], 31)
        self.assertEqual(report["regular_symbol"], "64")
        self.assertEqual(report["gap_as_regular"], 228)
        self.assertEqual(report["works"], ("rare-column search", "full-length letter counts"))
        self.assertEqual(report["does_not_work"], ("printed-order digrams", "either half alone", "symbol spacing"))


if __name__ == "__main__":
    unittest.main()
