"""The wait for a new cell. Not a reading."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_intro import intro_report
from engine.solvers.dagapeyeff import consider_intro


class DagapeyeffIntroTest(unittest.TestCase):
    def test_the_wait_is_short_and_the_exercise_is_too(self) -> None:
        report = intro_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["longest_wait"], 22)
        self.assertEqual(report["as_short"], 304)
        self.assertEqual(report["hole_as_short"], 199)
        self.assertEqual(report["draws"], 10000)
        self.assertEqual(report["control_longest_wait"], 8)
        self.assertEqual(report["control_as_short"], 429)
        self.assertLess(report["as_short"] / report["draws"], 0.05)
        self.assertLess(report["hole_as_short"] / report["draws"], 0.05)
        self.assertLess(report["control_as_short"] / report["draws"], 0.05)
        claim = consider_intro()
        self.assertTrue(claim["intro_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIn("Not a reading", claim["learned"])


if __name__ == "__main__":
    unittest.main()
