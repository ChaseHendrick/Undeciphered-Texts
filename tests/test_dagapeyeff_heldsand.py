"""The sandwich stays rare when the rare cells are held still."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_heldsand import heldsand_report
from engine.solvers.dagapeyeff import consider_heldsand


class DagapeyeffHeldsandTest(unittest.TestCase):
    def test_the_sandwich_is_not_the_plain_gap(self) -> None:
        report = heldsand_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["pinned"], 8)
        self.assertEqual(report["low"], ["04", "71", "92", "93", "94"])
        self.assertEqual(report["mode"], "81")
        self.assertEqual(report["gaps"], 2)
        self.assertEqual(report["plain_gaps"], 4)
        self.assertEqual(report["draws"], 20000)
        self.assertEqual(report["as_many"], 543)
        self.assertLess(report["as_many"] / report["draws"], 0.05)
        self.assertEqual(report["plain_as_many"], 7488)
        self.assertGreaterEqual(report["plain_as_many"] / report["draws"], 0.05)
        self.assertEqual(report["also_aligned"], 60)
        self.assertEqual(report["aligned"], 528)
        self.assertIs(report["allowed"], True)
        claim = consider_heldsand()
        self.assertIs(claim["heldsand_allowed"], True)
        self.assertIs(claim["solved"], False)
        self.assertIn("Not a reading", claim["learned"])


if __name__ == "__main__":
    unittest.main()
