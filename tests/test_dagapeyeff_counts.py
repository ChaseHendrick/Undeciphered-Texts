"""The rare counts sit in order on the square."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_counts import counts_report
from engine.solvers.dagapeyeff import consider_counts


class DagapeyeffCountsTest(unittest.TestCase):
    def test_rare_counts_sit_in_order(self) -> None:
        report = counts_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["three"], ["92"])
        self.assertEqual(report["two"], ["93"])
        self.assertEqual(report["one"], ["04", "71", "94"])
        self.assertIs(report["ordered"], True)
        self.assertEqual(report["favorable"], 18480)
        self.assertEqual(report["placements"], 1062600)
        self.assertLess(report["favorable"] / report["placements"], 0.05)
        self.assertIs(report["allowed"], True)
        claim = consider_counts()
        self.assertIs(claim["counts_allowed"], True)
        self.assertIs(claim["solved"], False)
        self.assertIn("Not a reading", claim["learned"])


if __name__ == "__main__":
    unittest.main()
