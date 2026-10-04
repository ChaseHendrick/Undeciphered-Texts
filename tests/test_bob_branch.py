"""The residual branch is alive and the shipped weights stay put."""

from __future__ import annotations

import unittest

from engine.bob_branch import bob_branch_report
from engine.solvers.dagapeyeff import consider_branch


class BobBranchTest(unittest.TestCase):
    def test_the_branch_is_used_and_the_weights_stay(self) -> None:
        report = bob_branch_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertFalse(report["weights_replaced"])
        self.assertTrue(report["weights_match_shipped"])
        self.assertEqual(report["weights_sha256"], "5c271f426812d6307f208a636b80f820201e25b3dc6778333e5d08d4d5aaaf4b")
        self.assertEqual(report["challenge_branch_share"], [0.5012, 0.5271, 0.5178])
        self.assertEqual(report["control_branch_share"], [0.4566, 0.4709, 0.4835])
        self.assertTrue(report["branch_alive"])
        claim = consider_branch()
        self.assertFalse(claim["branch_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIsNone(claim["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
