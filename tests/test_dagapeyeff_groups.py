"""Reordering the printed groups does not beat prose, or a shuffle."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_groups import group_report
from engine.solvers.dagapeyeff import consider_groups


class DagapeyeffGroupTest(unittest.TestCase):
    def test_the_group_routes_lose_to_a_shuffle(self) -> None:
        report = group_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["even_groups"], 39)
        self.assertEqual(report["odd_groups"], 39)
        self.assertEqual(report["routes"], 160)
        self.assertEqual(report["routes_on_square"], 160)
        self.assertEqual(report["best_route"], "rail-odd-6")
        self.assertEqual(report["best_quadgram"], -3.3582)
        self.assertEqual(report["prose_quadgram"], -2.5185)
        self.assertFalse(report["reaches_prose"])
        self.assertEqual(report["null_texts"], 40)
        self.assertEqual(report["shuffles_as_high"], 33)
        claim = consider_groups()
        self.assertFalse(claim["groups_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIsNone(claim["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
