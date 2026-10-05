"""The short introduction wait needs the rare cells in the count."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_heldwait import heldwait_report
from engine.solvers.dagapeyeff import consider_heldwait


class DagapeyeffHeldwaitTest(unittest.TestCase):
    def test_the_short_wait_does_not_survive_without_the_rare_cells(self) -> None:
        report = heldwait_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["pinned"], 8)
        self.assertEqual(report["low"], ["04", "71", "92", "93", "94"])
        self.assertEqual(report["draws"], 20000)
        self.assertEqual(report["wait"], 22)
        self.assertEqual(report["as_short"], 118)
        self.assertLess(report["as_short"] / report["draws"], 0.05)
        self.assertEqual(report["skip_wait"], 39)
        self.assertEqual(report["skip_as_short"], 19186)
        self.assertGreaterEqual(report["skip_as_short"] / report["draws"], 0.05)
        self.assertIs(report["allowed"], False)
        claim = consider_heldwait()
        self.assertIs(claim["heldwait_allowed"], False)
        self.assertIs(claim["solved"], False)
        self.assertIn("Not a reading", claim["learned"])


if __name__ == "__main__":
    unittest.main()
