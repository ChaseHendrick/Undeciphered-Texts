"""Each aligned run has two further copies in its row."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_outside import outside_report
from engine.solvers.dagapeyeff import consider_outside


class DagapeyeffOutsideTest(unittest.TestCase):
    def test_outside_copies_clear_once_the_alignment_is_given(self) -> None:
        report = outside_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["cells"], ["75", "63"])
        self.assertEqual(report["rows"], [2, 6])
        self.assertEqual(report["columns"], [10, 10])
        self.assertEqual(report["lengths"], [3, 3])
        self.assertEqual(report["outside"], 2)
        self.assertEqual(report["places"], [
            {"row": 2, "column": 1, "cell": "75"},
            {"row": 2, "column": 6, "cell": "75"},
            {"row": 6, "column": 0, "cell": "63"},
            {"row": 6, "column": 6, "cell": "63"},
        ])
        self.assertEqual(report["shared"], 2)
        self.assertEqual(report["draws"], 40000)
        self.assertEqual(report["aligned"], 866)
        self.assertEqual(report["spare"], 14)
        self.assertLess(report["spare"] / report["aligned"], 0.05)
        claim = consider_outside()
        self.assertTrue(claim["outside_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIn("Not a reading", claim["learned"])


if __name__ == "__main__":
    unittest.main()
