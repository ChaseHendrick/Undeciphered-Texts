"""Keyed four-square and two-square: the search has no power at 196 letters, so the cells were not searched."""

from __future__ import annotations

import random
import unittest

from engine.dagapeyeff_keyedsquares import encrypt, keyedsquares_report, two_square


class DagapeyeffKeyedSquaresTest(unittest.TestCase):
    def test_encipherment_uses_rows_of_one_letter_and_columns_of_the_other(self) -> None:
        identity = list(range(25))
        self.assertEqual(encrypt("AG", identity, identity, identity, identity), [0 * 5 + 1, 1 * 5 + 0])
        self.assertEqual(len(two_square("AB" * 10, random.Random(1))), 20)

    def test_no_planted_text_comes_back(self) -> None:
        report = keyedsquares_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertIs(report["cells_searched"], False)
        self.assertEqual(report["planted_recovered"], 0)
        self.assertEqual(len(report["planted"]), 6)


if __name__ == "__main__":
    unittest.main()
