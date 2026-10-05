"""A barely rare diagonal is not a finding once the whole table is scored."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_modulo import modulo_report
from engine.solvers.dagapeyeff import consider_modulo


class DagapeyeffModuloTest(unittest.TestCase):
    def test_the_diagonal_loses_when_the_table_is_scored(self) -> None:
        report = modulo_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["alignments"], 20)
        self.assertEqual(report["hits"], 56)
        self.assertEqual(report["digit"], "row")
        self.assertEqual(report["axis"], "x")
        self.assertEqual(report["phase"], 0)
        self.assertEqual(report["early_draws"], 20000)
        self.assertEqual(report["early_as_high"], 975)
        self.assertEqual(report["draws"], 100000)
        self.assertEqual(report["as_high"], 4978)
        self.assertLess(report["as_high"] / report["draws"], 0.05)
        self.assertEqual(report["chi"], 19.5404)
        self.assertEqual(report["chi_draws"], 20000)
        self.assertEqual(report["chi_as_high"], 12780)
        self.assertGreaterEqual(report["chi_as_high"] / report["chi_draws"], 0.05)
        self.assertEqual(report["control_pairs"], 89)
        self.assertEqual(report["control_hits"], 29)
        self.assertEqual(report["control_as_high"], 1488)
        self.assertGreaterEqual(report["control_as_high"] / report["control_draws"], 0.05)
        self.assertIs(report["allowed"], False)
        claim = consider_modulo()
        self.assertIs(claim["modulo_allowed"], False)
        self.assertIs(claim["solved"], False)
        self.assertIn("Not a reading", claim["learned"])


if __name__ == "__main__":
    unittest.main()
