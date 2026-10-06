"""The compiled grille search finds a grille only when the letter key is given."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_grille import grille_order
from engine.dagapeyeff_grillec import encrypt, grillec_report


class DagapeyeffGrillecTest(unittest.TestCase):
    def test_the_plaintext_goes_into_the_holes_in_turn(self) -> None:
        choice = [index % 4 for index in range(49)]
        cells, source = encrypt(list(range(196)), choice)
        self.assertEqual(sorted(cells), list(range(196)))
        order = grille_order(choice)
        self.assertEqual([cells[position] for position in order], list(range(196)))
        self.assertEqual(cells, source)

    def test_power_needs_the_key_and_the_cells_are_not_searched(self) -> None:
        report = grillec_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertFalse(report["cells_searched"])
        self.assertEqual(report["recovered"], {"known": [4, 4], "joint": [0, 4], "seeded": [0, 4]})
        for row in report["planted"]:
            if row["case"] != "known":
                self.assertLess(row["holes_right"], 25)


if __name__ == "__main__":
    unittest.main()
