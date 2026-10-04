"""Caesar, Vigenere, and substitution all lose to a shuffle."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_solver_swarm import solver_swarm_report
from engine.solvers.dagapeyeff import consider_solver_swarm


class DagapeyeffSolverSwarmTest(unittest.TestCase):
    def test_the_solver_swarm_loses_to_shuffles(self) -> None:
        report = solver_swarm_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["letters"], 196)
        self.assertEqual(report["caesar_per_letter"], -3.4459)
        self.assertEqual(report["caesar_prose_per_letter"], -2.9415)
        self.assertEqual(report["caesar_draws"], 40)
        self.assertEqual(report["caesar_shuffles_as_high"], 33)
        self.assertEqual(report["vigenere_max_period"], 8)
        self.assertEqual(report["vigenere_period"], 3)
        self.assertEqual(report["vigenere_per_letter"], -3.7393)
        self.assertEqual(report["vigenere_prose_per_letter"], -2.4363)
        self.assertEqual(report["vigenere_draws"], 20)
        self.assertEqual(report["vigenere_shuffles_as_high"], 7)
        self.assertEqual(report["substitution_steps"], 400)
        self.assertEqual(report["substitution_per_letter"], -3.0858)
        self.assertEqual(report["substitution_prose_per_letter"], -2.6585)
        self.assertIs(report["substitution_reading"], False)
        self.assertEqual(report["substitution_draws"], 8)
        self.assertEqual(report["substitution_shuffles_as_high"], 8)
        claim = consider_solver_swarm()
        self.assertFalse(claim["solver_swarm_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIsNone(claim["claimed_plaintext"])
        self.assertNotIn("plaintext", report)


if __name__ == "__main__":
    unittest.main()
