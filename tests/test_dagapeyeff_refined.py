"""The most surprising neighbor pair appears once, like a shuffle."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_refined import refined_report
from engine.solvers.dagapeyeff import consider_refined


class DagapeyeffRefinedTest(unittest.TestCase):
    def test_one_pair_is_not_a_pattern(self) -> None:
        report = refined_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["cells"], 196)
        self.assertEqual(report["peak_z"], 3.9957)
        self.assertEqual(report["peak_count"], 1)
        self.assertEqual(report["draws"], 2000)
        self.assertEqual(report["shuffles_as_high"], 1637)
        claim = consider_refined()
        self.assertFalse(claim["refined_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIsNone(claim["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
