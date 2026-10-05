"""Repeated digraphs in the challenge and the solved exercise. Not a reading."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_digraph import digraph_report
from engine.solvers.dagapeyeff import consider_digraph


class DagapeyeffDigraphTest(unittest.TestCase):
    def test_the_variety_clears_and_the_two_measures_do_not(self) -> None:
        report = digraph_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["repeated_digraphs"], 48)
        self.assertEqual(report["repeated_as_high"], 6924)
        self.assertEqual(report["control_repeated_digraphs"], 15)
        self.assertEqual(report["control_repeated_as_high"], 165)
        self.assertEqual(report["control_either_as_high"], 1270)
        self.assertEqual(report["draws"], 10000)
        self.assertLess(report["control_repeated_as_high"] / report["draws"], 0.05)
        self.assertGreater(report["control_either_as_high"] / report["draws"], 0.05)
        self.assertGreater(report["repeated_as_high"] / report["draws"], 0.05)
        claim = consider_digraph()
        self.assertFalse(claim["digraph_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIn("Not a reading", claim["learned"])


if __name__ == "__main__":
    unittest.main()
