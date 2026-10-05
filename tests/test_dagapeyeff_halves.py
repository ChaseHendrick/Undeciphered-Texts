"""The even and odd symbol gap is the private column counted again."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_halves import halves_report
from engine.solvers.dagapeyeff import consider_halves


class DagapeyeffHalvesTest(unittest.TestCase):
    def test_the_split_is_the_private_column(self) -> None:
        report = halves_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["even_support"], 13)
        self.assertEqual(report["odd_support"], 18)
        self.assertEqual(report["gap"], 5)
        self.assertEqual(report["draws"], 20000)
        self.assertEqual(report["as_high"], 146)
        self.assertLess(report["as_high"] / report["draws"], 0.05)
        self.assertEqual(report["private"], ["04", "71", "92", "93", "94"])
        self.assertEqual(report["residual_gap"], 0)
        self.assertEqual(report["residual_as_high"], 20000)
        self.assertGreaterEqual(report["residual_as_high"] / report["draws"], 0.05)
        self.assertEqual(report["period7_gap"], 6)
        self.assertEqual(report["period7_as_high"], 637)
        self.assertEqual(report["period7_residual_gap"], 3)
        self.assertEqual(report["period7_residual_as_high"], 9966)
        self.assertGreaterEqual(report["period7_residual_as_high"] / report["draws"], 0.05)
        self.assertIs(report["allowed"], False)
        claim = consider_halves()
        self.assertIs(claim["halves_allowed"], False)
        self.assertIs(claim["solved"], False)
        self.assertIn("Not a reading", claim["learned"])


if __name__ == "__main__":
    unittest.main()
