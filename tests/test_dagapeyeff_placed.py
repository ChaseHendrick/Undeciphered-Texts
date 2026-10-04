"""Placing the count-matched edits does not make the order English."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_placed import placed_report
from engine.solvers.dagapeyeff import consider_placed


class DagapeyeffPlacedTest(unittest.TestCase):
    def test_the_placed_edits_match_a_shuffle(self) -> None:
        report = placed_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["targets"], 70)
        self.assertEqual(report["placements"], 2494800)
        self.assertEqual(report["best_quadgram"], -3.4263)
        self.assertEqual(report["prose_quadgram"], -2.5185)
        self.assertFalse(report["reaches_prose"])
        self.assertEqual(report["draws"], 20)
        self.assertEqual(report["shuffles_as_high"], 11)
        claim = consider_placed()
        self.assertFalse(claim["placed_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIsNone(claim["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
