"""Two count-moves cannot clear English. The solver remembers that."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_edits import edit_report
from engine.solvers.dagapeyeff import consider_frequency_claim


class DagapeyeffEditsTest(unittest.TestCase):
    def test_two_moves_stay_above_english_and_the_solver_refuses_them(self) -> None:
        report = edit_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["english_line"], 24.165)
        self.assertEqual(report["depth1_chi"], 30.65)
        self.assertEqual(report["depth2_chi"], 27.5)
        self.assertEqual(report["depth2_ball_hi"], 27.557769)
        self.assertFalse(report["depth2_clears"])
        self.assertEqual(report["greedy3_ball_hi"], 24.931425)
        self.assertEqual(report["greedy4_ball_hi"], 22.471061)
        self.assertTrue(report["greedy4_clears"])
        self.assertEqual(report["moves_required"], 3)
        too_few = consider_frequency_claim(2, 20.0)
        not_clear = consider_frequency_claim(3, 30.0)
        clears = consider_frequency_claim(4, 22.0)
        self.assertFalse(too_few["frequency_claim_allowed"])
        self.assertFalse(not_clear["frequency_claim_allowed"])
        self.assertTrue(clears["frequency_claim_allowed"])
        self.assertIs(too_few["solved"], False)
        self.assertIs(clears["solved"], False)
        self.assertIsNone(clears["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
