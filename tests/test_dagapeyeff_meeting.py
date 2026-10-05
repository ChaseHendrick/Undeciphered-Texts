"""The most common cell's vertical run meets a horizontal run."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_meeting import meeting_report
from engine.solvers.dagapeyeff import consider_meeting


class DagapeyeffMeetingTest(unittest.TestCase):
    def test_the_runs_meet_under_a_kings_move(self) -> None:
        report = meeting_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["mode"], "81")
        self.assertEqual(report["meetings"], 1)
        self.assertEqual(report["vertical_column"], 9)
        self.assertEqual(report["vertical_top"], 4)
        self.assertEqual(report["vertical_bottom"], 6)
        self.assertEqual(report["cell"], "63")
        self.assertEqual(report["row"], 6)
        self.assertEqual(report["left"], 10)
        self.assertEqual(report["right"], 12)
        self.assertEqual(report["as_many"], 149)
        self.assertEqual(report["draws"], 20000)
        self.assertLess(report["as_many"] / report["draws"], 0.05)
        claim = consider_meeting()
        self.assertTrue(claim["meeting_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIn("Not a reading", claim["learned"])


if __name__ == "__main__":
    unittest.main()
