"""The prose score is the yardstick. The book's square does not reach it."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_yardstick import yardstick_report


class DagapeyeffYardstickTest(unittest.TestCase):
    def test_the_goal_is_prose_that_regenerates_the_cells(self) -> None:
        report = yardstick_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["cipher_mi"], 0.5706)
        self.assertEqual(report["english_mi"], 1.0658)
        self.assertEqual(report["german_mi"], 1.2)
        self.assertEqual(report["sorted_mi"], 2.3931)
        self.assertEqual(report["entropy"], 2.6692)
        self.assertEqual(report["index_of_coincidence"], 0.069702)
        self.assertEqual(report["book_orientations"], 8)
        self.assertEqual(report["book_best_mi"], 0.5706)
        self.assertEqual(report["book_best_blanks"], 15)
        self.assertEqual(report["book_worst_mi"], 0.4378)
        self.assertLess(report["cipher_mi"], report["english_mi"])
        self.assertGreater(report["sorted_mi"], report["english_mi"])


if __name__ == "__main__":
    unittest.main()
