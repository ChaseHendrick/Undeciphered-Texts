"""The mismatch remains after the sharpest cell is set aside."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_rest import rest_report
from engine.solvers.dagapeyeff import consider_rest


class DagapeyeffRestTest(unittest.TestCase):
    def test_the_leftover_still_clears(self) -> None:
        report = rest_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["chi"], 77.36)
        self.assertEqual(report["sharp"], 26.55)
        self.assertEqual(report["second_cell"], "61")
        self.assertEqual(report["second"], 9.43)
        self.assertEqual(report["rest"], 50.81)
        self.assertEqual(report["as_large"], 0)
        self.assertEqual(report["peak"], 38.0)
        self.assertEqual(report["control_rest"], 35.26)
        self.assertEqual(report["control_as_large"], 0)
        self.assertEqual(report["control_peak"], 35.12)
        self.assertEqual(report["draws"], 20000)
        claim = consider_rest()
        self.assertTrue(claim["rest_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIn("Not a reading", claim["learned"])


if __name__ == "__main__":
    unittest.main()
