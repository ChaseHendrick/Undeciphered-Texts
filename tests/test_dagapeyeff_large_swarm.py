"""A large deletion search and a large gap search both miss."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_large_swarm import large_swarm_report
from engine.solvers.dagapeyeff import consider_large_swarm


class DagapeyeffLargeSwarmTest(unittest.TestCase):
    def test_the_large_searches_match_shuffles(self) -> None:
        report = large_swarm_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["cells"], 196)
        self.assertEqual(report["pairs"], 19110)
        self.assertEqual(report["deletion_quadgram"], -3.3437)
        self.assertEqual(report["prose_quadgram"], -2.5185)
        self.assertFalse(report["reaches_prose"])
        self.assertEqual(report["deletion_draws"], 40)
        self.assertEqual(report["deletion_shuffles_as_high"], 21)
        self.assertEqual(report["gap_periods"], "2-28")
        self.assertEqual(report["gap_count"], 178)
        self.assertEqual(report["gap_peak_z"], 0.7495)
        self.assertEqual(report["gap_draws"], 5000)
        self.assertEqual(report["gap_shuffles_as_high"], 1505)
        claim = consider_large_swarm()
        self.assertFalse(claim["large_swarm_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIsNone(claim["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
