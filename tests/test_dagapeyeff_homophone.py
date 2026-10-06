"""A many-to-one key, capped so it cannot collapse onto one letter, finds nothing on the cells."""

from __future__ import annotations

import random
import unittest
from collections import Counter

from engine.dagapeyeff_homophone import homophone_report, homophonic
from engine.solvers.dagapeyeff import consider_homophone


class DagapeyeffHomophoneTest(unittest.TestCase):
    def test_a_homophonic_key_uses_every_symbol_and_decodes_one_way(self) -> None:
        text = "THEQUICKBROWNFOXIUMPSOVERTHELAZYDOG" * 3
        cipher = homophonic(text, random.Random(1))
        self.assertEqual(len(set(cipher)), 25)
        meaning = {}
        for symbol, ch in zip(cipher, text):
            self.assertEqual(meaning.setdefault(symbol, ch), ch)
        self.assertEqual(Counter(meaning.values())["O"] >= 1, True)

    def test_the_cells_do_not_beat_their_shuffles(self) -> None:
        report = homophone_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["planted_recovered"], 6)
        self.assertEqual(report["search"]["letter_cap"], 36)
        floor = report["planted_lowest_true"]
        for row in report["searched"].values():
            self.assertLess(row["per_letter"], floor - 0.8)
            self.assertGreaterEqual(row["shuffles_as_high"], 3)
        claim = consider_homophone()
        self.assertFalse(claim["homophone_allowed"])


if __name__ == "__main__":
    unittest.main()
