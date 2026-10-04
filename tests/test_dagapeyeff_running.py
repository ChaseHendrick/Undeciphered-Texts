"""A running key from the repo texts does not beat the period-4 search."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_running import running_report
from engine.solvers.dagapeyeff import consider_running_key


class DagapeyeffRunningTest(unittest.TestCase):
    def test_the_running_key_is_not_a_record(self) -> None:
        report = running_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["texts"], 5)
        self.assertEqual(report["alignments"], 94860)
        self.assertEqual(report["best_text"], "neural_audit_wells.txt")
        self.assertEqual(report["best_direction"], "key-minus-cell")
        self.assertEqual(report["best_quadgram"], -3.4945)
        self.assertEqual(report["prose_quadgram"], -2.5185)
        self.assertFalse(report["reaches_prose"])
        self.assertEqual(report["null_texts"], 8)
        self.assertEqual(report["shuffles_as_high"], 1)
        claim = consider_running_key()
        self.assertFalse(claim["running_key_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIsNone(claim["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
