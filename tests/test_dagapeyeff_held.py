"""The aligned runs stay rare when the rare cells are held still."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_held import held_report
from engine.solvers.dagapeyeff import consider_held


class DagapeyeffHeldTest(unittest.TestCase):
    def test_the_alignment_is_not_the_rare_column(self) -> None:
        report = held_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["pinned"], 8)
        self.assertEqual(report["low"], ["04", "71", "92", "93", "94"])
        self.assertEqual(report["shared_starts"], 2)
        self.assertEqual(report["runs"], 2)
        self.assertEqual(report["draws"], 20000)
        self.assertEqual(report["as_aligned"], 528)
        self.assertLess(report["as_aligned"] / report["draws"], 0.05)
        self.assertEqual(report["as_many_runs"], 4149)
        self.assertGreaterEqual(report["as_many_runs"] / report["draws"], 0.05)
        self.assertIs(report["allowed"], True)
        claim = consider_held()
        self.assertIs(claim["held_allowed"], True)
        self.assertIs(claim["solved"], False)
        self.assertIn("Not a reading", claim["learned"])


if __name__ == "__main__":
    unittest.main()
