"""63 sits between two copies of the most common cell."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_sandwich import sandwich_report
from engine.solvers.dagapeyeff import consider_sandwich


class DagapeyeffSandwichTest(unittest.TestCase):
    def test_the_gap_clears_with_a_vertical_count_included(self) -> None:
        report = sandwich_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["mode"], "81")
        self.assertEqual(report["middle"], "63")
        self.assertEqual(report["gaps"], 2)
        self.assertEqual(report["places"], [
            {"row": 1, "column": 7, "axis": "row"},
            {"row": 3, "column": 4, "axis": "row"},
        ])
        self.assertEqual(report["as_many"], 427)
        self.assertEqual(report["draws"], 20000)
        self.assertLess(report["as_many"] / report["draws"], 0.05)
        claim = consider_sandwich()
        self.assertTrue(claim["sandwich_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIn("Not a reading", claim["learned"])


if __name__ == "__main__":
    unittest.main()
