"""The yardstick gaps stay open after the radii are enclosed."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_balls import ball_report


class DagapeyeffBallsTest(unittest.TestCase):
    def test_the_balls_do_not_meet(self) -> None:
        report = ball_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["terms"], 30)
        self.assertTrue(report["cipher_below_english"])
        self.assertTrue(report["cipher_below_german"])
        self.assertTrue(report["sorted_above_english"])
        self.assertEqual(report["highest_column"], 13)
        self.assertEqual(report["second_column"], 12)
        self.assertTrue(report["highest_above_second"])
        self.assertTrue(report["second_above_rest"])
        self.assertLess(report["cipher"]["rad"], 1e-20)
        self.assertLess(report["english"]["rad"], 1e-20)
        self.assertLess(report["outgoing_rad_max"], 1e-20)
        self.assertEqual(round(report["cipher"]["lo"], 4), 0.5706)
        self.assertEqual(round(report["cipher"]["hi"], 4), 0.5706)
        self.assertEqual(round(report["english"]["lo"], 4), 1.0658)
        self.assertEqual(round(report["german"]["lo"], 4), 1.2)
        self.assertEqual(round(report["sorted"]["lo"], 4), 2.3931)


if __name__ == "__main__":
    unittest.main()
