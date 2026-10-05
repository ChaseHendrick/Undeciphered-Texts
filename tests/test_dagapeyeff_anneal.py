"""A longer swarm on the cells does not beat shuffled cells."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_anneal import anneal_swarm_report
from engine.solvers.dagapeyeff import consider_anneal_swarm


class DagapeyeffAnnealTest(unittest.TestCase):
    def test_the_cells_do_not_win(self) -> None:
        report = anneal_swarm_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["letters"], 196)
        self.assertEqual(report["reader_family"], "substitution")
        self.assertTrue(report["reader_withheld"])
        self.assertFalse(report["reader_consistent"])
        self.assertEqual(report["draws"], 6)
        self.assertEqual(report["caesar_shuffles_as_high"], 6)
        self.assertEqual(report["vigenere_shuffles_as_high"], 4)
        self.assertEqual(report["substitution_steps"], 2000)
        self.assertEqual(report["substitution_restarts"], 4)
        self.assertEqual(report["substitution_shuffles_as_high"], 6)
        self.assertFalse(report["substitution_reading"])
        self.assertFalse(report["promoted"])
        self.assertAlmostEqual(report["caesar_per_letter"], -3.4459, places=4)
        self.assertAlmostEqual(report["substitution_per_letter"], -3.09, places=4)
        self.assertAlmostEqual(report["vigenere_per_letter"], -3.7393, places=4)
        claim = consider_anneal_swarm()
        self.assertFalse(claim["anneal_swarm_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIsNone(claim["claimed_plaintext"])
        self.assertNotIn("plaintext", claim["learned"].lower())


if __name__ == "__main__":
    unittest.main()
