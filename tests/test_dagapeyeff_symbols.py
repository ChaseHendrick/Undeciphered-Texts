"""One cell repeating is ordinary. Several rare cells in one column is not."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_symbols import symbol_report


class DagapeyeffSymbolsTest(unittest.TestCase):
    def test_the_repeat_is_not_the_pile(self) -> None:
        report = symbol_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["trials"], 195000)
        self.assertEqual(report["owner"], "82")
        self.assertEqual(report["owner_pile"], 6)
        self.assertEqual(report["owner_as_high"], 738)
        self.assertEqual(report["rare_pile"], 5)
        self.assertEqual(report["rare_as_high"], 0)
        self.assertEqual(report["longest_vertical_run"], 3)
        self.assertEqual(report["vertical_as_long"], 10855)
        self.assertEqual(report["rare_rows"], (2, 6, 7, 8, 9))
        self.assertEqual(report["row_run"], 4)
        self.assertEqual(report["rows_as_bunched"], 100)
        self.assertEqual(report["closest_width"], 14)
        self.assertEqual(report["closest_width_tail"], 187)


if __name__ == "__main__":
    unittest.main()
