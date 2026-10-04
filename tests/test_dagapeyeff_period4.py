"""A period-4 shift paints counts and does not reach prose."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_period4 import period4_report
from engine.solvers.dagapeyeff import consider_period4


class DagapeyeffPeriod4Test(unittest.TestCase):
    def test_the_long_repeat_does_not_reach_prose(self) -> None:
        report = period4_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["keys"], 390625)
        self.assertEqual(report["null_texts"], 40)
        self.assertEqual(report["trials"], 16015625)
        self.assertEqual(report["chi"], 3.86)
        self.assertEqual(report["quadgram"], -3.4759)
        self.assertEqual(report["prose_quadgram"], -2.5185)
        self.assertEqual(report["chi_as_low"], 32)
        self.assertEqual(report["quad_as_high"], 3)
        self.assertFalse(report["reaches_prose"])
        claim = consider_period4()
        self.assertFalse(claim["period4_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIsNone(claim["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
