"""Three-cell repeats in the challenge and the solved exercise. Not a reading."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_trigram import trigram_report
from engine.solvers.dagapeyeff import consider_trigram


class DagapeyeffTrigramTest(unittest.TestCase):
    def test_the_exercise_clears_and_the_challenge_does_not(self) -> None:
        report = trigram_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["control_repeated_trigrams"], 4)
        self.assertEqual(report["control_trigrams_as_high"], 59)
        self.assertEqual(report["repeated_trigrams"], 5)
        self.assertEqual(report["trigrams_as_high"], 7329)
        self.assertEqual(report["control_repeated_tetragrams"], 0)
        self.assertEqual(report["control_tetragrams_as_few"], 9656)
        self.assertEqual(report["draws"], 10000)
        rate = report["control_trigrams_as_high"] / report["draws"]
        self.assertLess(report["lengths_scored"] * rate, 0.05)
        self.assertGreater(report["trigrams_as_high"] / report["draws"], 0.05)
        claim = consider_trigram()
        self.assertTrue(claim["trigram_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIn("Not a reading", claim["learned"])


if __name__ == "__main__":
    unittest.main()
