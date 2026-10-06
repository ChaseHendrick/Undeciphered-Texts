"""Enciphering errors at the book's rate cannot hide English under a one-to-one key."""

from __future__ import annotations

import random
import unittest

from engine.dagapeyeff_errors import corrupt, errors_report, fewest_errors, slip, sorted_counts
from engine.solvers.dagapeyeff import consider_errors


class DagapeyeffErrorsTest(unittest.TestCase):
    def test_the_fewest_errors_is_half_the_sorted_distance(self) -> None:
        target = sorted_counts([0, 0, 1, 1])
        self.assertEqual(fewest_errors([5, 5, 6, 6], target), 0)
        self.assertEqual(fewest_errors([5, 5, 5, 6], target), 1)
        self.assertEqual(fewest_errors([5, 5, 5, 5], target), 2)
        rng = random.Random(3)
        for _ in range(50):
            moved = slip(12, rng)
            self.assertNotEqual(moved, 12)
            self.assertTrue(moved // 5 == 2 or moved % 5 == 2)
        self.assertEqual(sum(a != b for a, b in zip(corrupt(list(range(25)) * 4, 7, rng, "slip"), list(range(25)) * 4)), 7)

    def test_errors_do_not_reach_the_cells(self) -> None:
        report = errors_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        counts = report["counts"]
        self.assertEqual(counts["best_case_at_most_8"], 0)
        self.assertGreaterEqual(counts["best_case_fewest"], 9)
        self.assertEqual(sum(row["reaching_cells"] for row in counts["random"]), 0)
        self.assertGreater(min(row["fewest_remaining"] for row in counts["random"]), 8)
        eight = report["by_errors"]["8"]
        self.assertGreater(eight["found_low"], report["cells_per_letter"] + 1.0)
        self.assertGreaterEqual(eight["letters_right_low"], 0.95)
        self.assertGreaterEqual(report["fewest_errors_at_cells_level"], 32)
        claim = consider_errors()
        self.assertFalse(claim["errors_allowed"])


if __name__ == "__main__":
    unittest.main()
