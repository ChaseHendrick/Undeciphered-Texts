"""The rare column is not a check digit. A planted sum is detected."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_check import best_match, check_report


class DagapeyeffCheckTest(unittest.TestCase):
    def test_a_planted_sum_is_found_and_the_real_column_is_not(self) -> None:
        planted = [[(row + column) % 5 for column in range(14)] for row in range(14)]
        for row in range(14):
            planted[row][13] = sum(planted[row][column] for column in range(13)) % 5
        self.assertEqual(best_match(planted), (14, 33))
        report = check_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["predictors"], 33)
        self.assertEqual(report["trials"], 1320000)
        self.assertEqual(report["row_best"], 6)
        self.assertEqual(report["row_as_high"], 20000)
        self.assertEqual(report["column_best"], 6)
        self.assertEqual(report["column_as_high"], 15059)


if __name__ == "__main__":
    unittest.main()
