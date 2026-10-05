"""The aligned runs still touch the rare seats, and the meeting does not clear."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_seats import seats_report
from engine.solvers.dagapeyeff import consider_seats


class DagapeyeffSeatsTest(unittest.TestCase):
    def test_contact_survives_and_the_meeting_does_not(self) -> None:
        report = seats_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["pinned"], 8)
        self.assertEqual(report["low"], ["04", "71", "92", "93", "94"])
        self.assertEqual(report["draws"], 20000)
        self.assertEqual(report["aligned"], 528)
        self.assertEqual(report["contact"], 9)
        self.assertLess(report["contact"] / report["aligned"], 0.05)
        self.assertEqual(report["vertical_runs"], 2842)
        self.assertEqual(report["meeting_given_vertical"], 185)
        self.assertGreaterEqual(report["meeting_given_vertical"] / report["vertical_runs"], 0.05)
        self.assertIs(report["allowed"], True)
        claim = consider_seats()
        self.assertIs(claim["seats_allowed"], True)
        self.assertIs(claim["solved"], False)
        self.assertIn("Not a reading", claim["learned"])


if __name__ == "__main__":
    unittest.main()
