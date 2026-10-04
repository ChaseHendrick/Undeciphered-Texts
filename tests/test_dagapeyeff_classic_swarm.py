"""Affine, Beaufort, and Porta all miss prose."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_classic_swarm import classic_swarm_report
from engine.solvers.dagapeyeff import consider_classic_swarm


class DagapeyeffClassicSwarmTest(unittest.TestCase):
    def test_the_classic_swarm_misses_prose(self) -> None:
        report = classic_swarm_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["letters"], 196)
        self.assertEqual(report["prose_per_quadgram"], -2.5185)
        self.assertEqual(report["affine_multiplier"], 1)
        self.assertEqual(report["affine_per_quadgram"], -3.7883)
        self.assertEqual(report["affine_draws"], 20)
        self.assertEqual(report["affine_shuffles_as_high"], 16)
        self.assertEqual(report["beaufort_period"], 5)
        self.assertEqual(report["beaufort_per_quadgram"], -3.7684)
        self.assertEqual(report["beaufort_draws"], 80)
        self.assertEqual(report["beaufort_shuffles_as_high"], 8)
        self.assertEqual(report["porta_period"], 4)
        self.assertEqual(report["porta_per_quadgram"], -3.9175)
        self.assertEqual(report["porta_draws"], 20)
        self.assertEqual(report["porta_shuffles_as_high"], 11)
        claim = consider_classic_swarm()
        self.assertFalse(claim["classic_swarm_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIsNone(claim["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
