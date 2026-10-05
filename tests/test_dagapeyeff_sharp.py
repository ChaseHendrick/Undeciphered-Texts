"""The sharpest cell still leads after every cell is allowed to compete."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_sharp import sharp_report
from engine.solvers.dagapeyeff import consider_sharp


class DagapeyeffSharpTest(unittest.TestCase):
    def test_cell_91_is_sharper_than_every_re_pairing(self) -> None:
        report = sharp_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["cell"], "91")
        self.assertEqual(report["observed"], 12)
        self.assertEqual(report["as_sharp"], 0)
        self.assertEqual(report["draws"], 20000)
        self.assertEqual(report["chi"], 77.36)
        self.assertEqual(report["correlation"], 0.609)
        self.assertEqual(report["control_cell"], "CC")
        self.assertEqual(report["control_as_sharp"], 1383)
        self.assertLess(report["control_as_sharp"] / report["draws"], 0.1)
        self.assertGreater(report["control_as_sharp"] / report["draws"], 0.05)
        claim = consider_sharp()
        self.assertTrue(claim["sharp_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIn("Not a reading", claim["learned"])


if __name__ == "__main__":
    unittest.main()
