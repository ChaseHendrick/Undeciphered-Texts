"""A coordinate delay and a progressive shift both miss prose."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_delay import delay_report
from engine.solvers.dagapeyeff import consider_delay


class DagapeyeffDelayTest(unittest.TestCase):
    def test_neither_delay_nor_progression_reaches_prose(self) -> None:
        report = delay_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["delays"], 196)
        self.assertEqual(report["best_delay"], 79)
        self.assertEqual(report["delay_quadgram"], -3.2652)
        self.assertEqual(report["delay_draws"], 200)
        self.assertEqual(report["delay_shuffles_as_high"], 3)
        self.assertEqual(report["progressive_rule"], "sub")
        self.assertEqual(report["progressive_quadgram"], -3.6491)
        self.assertEqual(report["progressive_draws"], 200)
        self.assertEqual(report["progressive_shuffles_as_high"], 4)
        self.assertEqual(report["prose_quadgram"], -2.5185)
        self.assertFalse(report["reaches_prose"])
        claim = consider_delay()
        self.assertFalse(claim["delay_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIsNone(claim["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
