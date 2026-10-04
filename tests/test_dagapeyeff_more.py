"""Wider D'Agapeyeff swarm: alphabets, group order, and period. Not a reading."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_more import language_slice, search_more


class DagapeyeffMoreTest(unittest.TestCase):
    def test_swarm_does_not_find_a_reading(self) -> None:
        report = search_more()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["workers"], 200)
        merger = report["merger"]
        self.assertEqual(merger["hypotheses"], 2457)
        self.assertEqual(merger["challenge_best_chi"], 14.05)
        self.assertEqual(merger["challenge_language"], "italian")
        self.assertEqual(merger["challenge_rule"], "merge MU")
        self.assertEqual(merger["null_draws"], 200)
        self.assertEqual(merger["null_as_bad"], 0)
        self.assertEqual(merger["null_median"], 2.84)
        groups = report["groups"]
        self.assertEqual(groups["reorders"], 120)
        self.assertEqual(groups["still_a_square"], 2)
        self.assertEqual(groups["best_reorder"], "01432")
        self.assertEqual(groups["best_legal_chi"], 8.86)
        self.assertEqual(groups["control"]["printed_chi"], 4.14)
        self.assertEqual(groups["control"]["flipped_chi"], 21.56)
        self.assertEqual(groups["control"]["better_than_printed"], 0)
        self.assertEqual(report["periods"]["overall_ic"], 0.0697)
        self.assertEqual(report["periods"]["shuffles_as_high"], 20)
        self.assertEqual(report["languages"]["english"]["chi"], 23.96)
        winner = language_slice(41)
        self.assertEqual(winner["best_chi"], 14.05)
        self.assertEqual(winner["rule"], "merge MU")


if __name__ == "__main__":
    unittest.main()
