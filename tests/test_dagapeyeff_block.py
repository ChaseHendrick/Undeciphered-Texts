"""The three cells that appear once, and whether they form a block. Not a reading."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_block import block_report
from engine.solvers.dagapeyeff import consider_block


class DagapeyeffBlockTest(unittest.TestCase):
    def test_the_named_three_are_consecutive_and_the_menu_is_not_rare(self) -> None:
        report = block_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["rows"], [6, 7, 8])
        self.assertIs(report["consecutive"], True)
        self.assertEqual((report["named_numerator"], report["named_denominator"]), (3, 91))
        self.assertEqual((report["union_numerator"], report["union_denominator"]), (984, 5005))
        self.assertLess(report["named_numerator"] / report["named_denominator"], 0.05)
        self.assertGreater(report["union_numerator"] / report["union_denominator"], 0.05)
        claim = consider_block()
        self.assertFalse(claim["block_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIn("Not a reading", claim["learned"])


if __name__ == "__main__":
    unittest.main()
