"""A turning grille search on the cells, with planted controls."""

from __future__ import annotations

import random
import unittest

from engine.dagapeyeff_grille import ORBITS, agreement, grille_encrypt, grille_order, grille_report
from engine.solvers.dagapeyeff import consider_grille


class DagapeyeffGrilleTest(unittest.TestCase):
    def test_a_grille_is_a_permutation_and_inverts(self) -> None:
        rng = random.Random(3)
        choice = [rng.randrange(4) for _ in range(ORBITS)]
        self.assertEqual(sorted(grille_order(choice)), list(range(196)))
        plain = [rng.randrange(26) for _ in range(196)]
        square = grille_encrypt(plain, choice)
        self.assertEqual([square[i] for i in grille_order(choice)], plain)
        turned = [(value + 1) & 3 for value in choice]
        self.assertEqual(agreement(turned, choice), ORBITS)

    def test_the_search_finds_nothing_the_shuffles_do_not(self) -> None:
        report = grille_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertGreater(report["information_found"], report["information_true"])
        self.assertLess(report["information_agreement"], ORBITS // 2)
        self.assertEqual(report["known_key_recovered"], 1)
        self.assertEqual([row["agreement"] for row in report["known_key"]], [49, 25, 47])
        self.assertEqual(report["joint_recovered"], 0)
        for row in report["joint"]:
            self.assertLess(row["found_per_letter"], row["true_per_letter"])
        self.assertAlmostEqual(report["cell_per_letter"], -3.1388, places=4)
        self.assertEqual(report["cell_shuffles_as_high"], 2)
        self.assertLess(report["unicity_letters"], report["cells"])
        claim = consider_grille()
        self.assertFalse(claim["grille_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIn("not closed", claim["learned"])


if __name__ == "__main__":
    unittest.main()
