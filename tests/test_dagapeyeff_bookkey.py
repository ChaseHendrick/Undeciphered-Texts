"""The book's solved exercise does not unlock the challenge."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_bookkey import bookkey_report
from engine.solvers.dagapeyeff import consider_bookkey


class DagapeyeffBookkeyTest(unittest.TestCase):
    def test_the_exercise_is_not_the_key(self) -> None:
        report = bookkey_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["faithful_length"], 89)
        self.assertEqual(report["gloss_length"], 92)
        self.assertEqual(report["best_use"], "slide-faithful-sub")
        self.assertEqual(report["best_quadgram"], -3.389)
        self.assertEqual(report["prose_quadgram"], -2.5185)
        self.assertFalse(report["reaches_prose"])
        self.assertEqual(report["null_texts"], 100)
        self.assertEqual(report["shuffles_as_high"], 61)
        claim = consider_bookkey()
        self.assertFalse(claim["bookkey_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIsNone(claim["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
