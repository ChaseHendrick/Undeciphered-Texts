"""The best word score over every period-4 shift still misses prose."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_word import word_report
from engine.solvers.dagapeyeff import consider_word_score


class DagapeyeffWordTest(unittest.TestCase):
    def test_the_word_search_does_not_reach_prose(self) -> None:
        report = word_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["keys"], 390625)
        self.assertEqual(report["null_texts"], 8)
        self.assertEqual(report["trials"], 3515625)
        self.assertEqual(report["best_quadgram"], -3.2713)
        self.assertEqual(report["prose_quadgram"], -2.5185)
        self.assertFalse(report["reaches_prose"])
        self.assertEqual(report["shuffles_as_high"], 4)
        claim = consider_word_score()
        self.assertFalse(claim["word_score_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIsNone(claim["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
