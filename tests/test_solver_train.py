"""A longer substitution search does not beat the default on fresh windows."""

from __future__ import annotations

import unittest

from engine.solver_train import solver_train_report
from engine.solvers.dagapeyeff import consider_solver_train


class SolverTrainTest(unittest.TestCase):
    def test_the_longer_search_is_not_promoted(self) -> None:
        report = solver_train_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertFalse(report["weights_replaced"])
        self.assertFalse(report["default_changed"])
        self.assertEqual(report["windows"], 6)
        self.assertEqual(report["width"], 200)
        self.assertEqual(report["default_exact"], 0)
        self.assertEqual(report["long_steps"], 8000)
        self.assertEqual(report["long_restarts"], 16)
        self.assertEqual(report["long_exact"], 0)
        self.assertTrue(report["certificate_default_exact"])
        self.assertTrue(report["certificate_long_exact"])
        self.assertFalse(report["promoted"])
        claim = consider_solver_train()
        self.assertFalse(claim["solver_train_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIsNone(claim["claimed_plaintext"])
        self.assertIn("Not a reading", claim["learned"])


if __name__ == "__main__":
    unittest.main()
