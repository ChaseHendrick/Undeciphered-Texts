"""The family router and the printed grid are not a reading."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_router_swarm import router_swarm_report
from engine.solvers.dagapeyeff import consider_router_swarm


class DagapeyeffRouterSwarmTest(unittest.TestCase):
    def test_the_router_and_the_grid_are_refused(self) -> None:
        report = router_swarm_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["families"], 20)
        self.assertEqual(report["top_family"], "substitution")
        self.assertEqual(report["top_probability"], 0.969)
        self.assertEqual(report["second_family"], "adfgvx")
        self.assertIs(report["uncertain"], False)
        self.assertEqual(report["router_draws"], 40)
        self.assertEqual(report["shuffles_same_family"], 40)
        self.assertEqual(report["shuffles_as_confident"], 25)
        self.assertEqual(report["row_ic"], 0.1319)
        self.assertEqual(report["column_ic"], 0.1868)
        self.assertEqual(report["column_index"], 3)
        self.assertEqual(report["column_top_count"], 6)
        self.assertEqual(report["grid_draws"], 200)
        self.assertEqual(report["row_shuffles_as_high"], 58)
        self.assertEqual(report["column_shuffles_as_high"], 6)
        claim = consider_router_swarm()
        self.assertFalse(claim["router_swarm_allowed"])
        self.assertTrue(claim["column_unusual"])
        self.assertFalse(claim["family_unusual"])
        self.assertIs(claim["solved"], False)
        self.assertIsNone(claim["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
