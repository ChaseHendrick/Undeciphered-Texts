"""Three count-moves cannot reach the English line."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_depth3 import depth3_report
from engine.solvers.dagapeyeff import consider_depth3, consider_frequency_claim


class DagapeyeffDepth3Test(unittest.TestCase):
    def test_three_moves_stay_above_english(self) -> None:
        report = depth3_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["moves"], 3)
        self.assertEqual(report["states"], 2321645)
        self.assertEqual(report["best_chi"], 24.8811)
        self.assertEqual(report["ball_lo"], 24.83087)
        self.assertEqual(report["ball_hi"], 24.931425)
        self.assertEqual(report["english_line"], 24.165)
        self.assertFalse(report["clears"])
        claim = consider_depth3()
        self.assertFalse(claim["depth3_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIsNone(claim["claimed_plaintext"])
        three = consider_frequency_claim(3, 22.0)
        four = consider_frequency_claim(4, 22.0)
        self.assertFalse(three["frequency_claim_allowed"])
        self.assertEqual(three["moves_required"], 4)
        self.assertTrue(four["frequency_claim_allowed"])
        self.assertIs(four["solved"], False)


if __name__ == "__main__":
    unittest.main()
