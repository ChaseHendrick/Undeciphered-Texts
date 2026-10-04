"""The rare window was chosen after looking. Every window of that height is not rare."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_clump import clump_report
from engine.solvers.dagapeyeff import consider_clump


class DagapeyeffClumpTest(unittest.TestCase):
    def test_the_window_was_chosen_after_looking(self) -> None:
        report = clump_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["symbol"], "72")
        self.assertEqual(report["count"], 9)
        self.assertEqual(report["fixed_count"], 6)
        self.assertTrue(report["fixed_chosen_after_looking"])
        self.assertEqual(report["fixed_shuffles_as_high"], 35)
        self.assertEqual(report["every_window_count"], 6)
        self.assertEqual(report["every_window_shuffles_as_high"], 268)
        self.assertEqual(report["draws"], 2000)
        claim = consider_clump()
        self.assertFalse(claim["clump_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIsNone(claim["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
