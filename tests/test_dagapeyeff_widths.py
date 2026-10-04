"""Only four column widths stay on the square, and they hurt the solved exercise."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_widths import widths_report
from engine.solvers.dagapeyeff import consider_widths


class DagapeyeffWidthsTest(unittest.TestCase):
    def test_the_other_legal_width_is_ordinary(self) -> None:
        report = widths_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["widths"], 392)
        self.assertEqual(report["fully_legal"], [1, 3, 131, 392])
        self.assertEqual(report["width_131_chi"], 10.63)
        self.assertEqual(report["re_pairings_as_flat"], 1227)
        self.assertEqual(report["draws"], 2000)
        self.assertEqual(report["control_printed_chi"], 4.14)
        self.assertEqual(report["control_width_3_chi"], 29.56)
        self.assertEqual(report["control_width_131_chi"], 42.13)
        claim = consider_widths()
        self.assertFalse(claim["widths_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIsNone(claim["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
