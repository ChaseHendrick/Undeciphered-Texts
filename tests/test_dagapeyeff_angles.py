"""A step, a row of holes, and a Playfair ban all fail their controls."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_angles import angle_report
from engine.solvers.dagapeyeff import consider_angles


class DagapeyeffAngleTest(unittest.TestCase):
    def test_three_new_angles_are_refused(self) -> None:
        report = angle_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["steps"], 195)
        self.assertEqual(report["step_quadgram"], -3.8542)
        self.assertEqual(report["prose_quadgram"], -2.5185)
        self.assertFalse(report["reaches_prose"])
        self.assertEqual(report["shuffles_as_high"], 23)
        self.assertEqual(report["unused_cells"], 7)
        self.assertEqual(report["most_in_one_row"], 4)
        self.assertEqual(report["placements"], 480700)
        self.assertEqual(report["placements_as_crowded"], 29450)
        self.assertEqual(report["digraphs"], 98)
        self.assertEqual(report["identical_digraphs"], 10)
        self.assertEqual(report["digraph_draws"], 400)
        self.assertEqual(report["shuffles_as_few_identical"], 363)
        claim = consider_angles()
        self.assertFalse(claim["angles_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIsNone(claim["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
