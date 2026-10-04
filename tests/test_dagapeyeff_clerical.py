"""Check digits and the tallest line. Not a reading."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_clerical import clerical_report
from engine.solvers.dagapeyeff import consider_clerical


class DagapeyeffClericalTest(unittest.TestCase):
    def test_the_line_does_not_clear_five_percent(self) -> None:
        report = clerical_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["rule_hits"], [6, 6, 11, 12, 8, 0, 0])
        self.assertEqual(report["first_digit_as_high"], 156)
        self.assertEqual(report["family_as_high"], 742)
        self.assertEqual(report["check_draws"], 2000)
        self.assertEqual((report["row_mode"], report["column_mode"]), (5, 6))
        self.assertEqual(report["column_as_high"], 357)
        self.assertEqual(report["line_as_high"], 720)
        self.assertEqual(report["line_draws"], 10000)
        self.assertLess(report["column_as_high"] / report["line_draws"], 0.05)
        self.assertGreater(report["line_as_high"] / report["line_draws"], 0.05)
        claim = consider_clerical()
        self.assertFalse(claim["clerical_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIn("Refuse the line", claim["learned"])


if __name__ == "__main__":
    unittest.main()
