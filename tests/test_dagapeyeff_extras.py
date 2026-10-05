"""Two copies outside the aligned runs, with the rare cells held still."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_extras import extras_report
from engine.solvers.dagapeyeff import consider_extras


class DagapeyeffExtrasTest(unittest.TestCase):
    def test_two_copies_clear_and_one_copy_does_not(self) -> None:
        report = extras_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["pinned"], 8)
        self.assertEqual(report["low"], ["04", "71", "92", "93", "94"])
        self.assertEqual(report["outside"], 2)
        self.assertEqual(report["draws"], 20000)
        self.assertEqual(report["aligned"], 528)
        self.assertEqual(report["at_least_one"], 112)
        self.assertGreaterEqual(report["at_least_one"] / report["aligned"], 0.05)
        self.assertEqual(report["at_least_two"], 8)
        self.assertLess(report["at_least_two"] / report["aligned"], 0.05)
        self.assertEqual(report["also_touching"], 0)
        self.assertEqual(report["different_cells"], 506)
        self.assertEqual(report["exact_length"], 458)
        self.assertEqual(report["close_rows"], 298)
        self.assertIs(report["allowed"], True)
        claim = consider_extras()
        self.assertIs(claim["extras_allowed"], True)
        self.assertIs(claim["solved"], False)
        self.assertIn("Not a reading", claim["learned"])


if __name__ == "__main__":
    unittest.main()
