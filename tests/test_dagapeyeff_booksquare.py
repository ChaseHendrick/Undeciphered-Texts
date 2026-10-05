"""The book's own square does not turn the cells into English counts."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_booksquare import align_exercise, booksquare_report
from engine.solvers.dagapeyeff import consider_booksquare


class DagapeyeffBooksquareTest(unittest.TestCase):
    def test_the_exercise_aligns_with_three_drops_and_one_wrong_pair(self) -> None:
        aligned = align_exercise()
        self.assertEqual(aligned["pairs"], 89)
        self.assertEqual(aligned["plaintext_letters"], 92)
        self.assertEqual(aligned["dropped"], [47, 52, 83])
        self.assertEqual(aligned["wrong"], [69])
        self.assertEqual(len(aligned["square"]), 22)

    def test_no_labeling_gives_english_counts(self) -> None:
        report = booksquare_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(len(report["labelings"]), 8)
        self.assertEqual(report["best_chi_square"], 362.87)
        self.assertEqual(report["english_chi_max"], 150.73)
        self.assertEqual(report["english_draws_as_high_as_best"], 0)
        self.assertEqual(report["exercise_chi_square"], 24.86)
        self.assertGreater(report["exercise_draws_as_high"], 100)
        claim = consider_booksquare()
        self.assertFalse(claim["booksquare_allowed"])
        self.assertIs(claim["solved"], False)


if __name__ == "__main__":
    unittest.main()
