"""The best count repairs share one loss. Neighbor edits are not rare."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_repair import repair_report
from engine.solvers.dagapeyeff import consider_repair


class DagapeyeffRepairTest(unittest.TestCase):
    def test_every_best_repair_reduces_the_same_symbol(self) -> None:
        report = repair_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["targets"], 70)
        self.assertEqual(report["touched_each"], 6)
        self.assertTrue(report["touched_same"])
        self.assertEqual(report["union"], 10)
        self.assertEqual(report["intersection"], 1)
        self.assertEqual(report["shared_symbol"], "72")
        self.assertEqual(report["shared_role"], "loss")
        self.assertEqual(report["loss_symbols"], 3)
        self.assertEqual(report["gain_symbols"], 7)
        self.assertEqual(report["transfer"], 4)
        self.assertEqual(report["neighbor_quadgram"], -3.1449)
        self.assertEqual(report["neighbor_shuffles_as_high"], 6)
        self.assertEqual(report["neighbor_draws"], 80)
        self.assertEqual(report["free_quadgram"], -3.1235)
        self.assertEqual(report["free_shuffles_as_high"], 7)
        self.assertEqual(report["free_draws"], 40)
        self.assertEqual(report["one_quadgram"], -3.3034)
        self.assertEqual(report["one_shuffles_as_high"], 13)
        self.assertEqual(report["one_draws"], 80)
        self.assertEqual(report["prose_quadgram"], -2.5185)
        self.assertFalse(report["reaches_prose"])
        claim = consider_repair()
        self.assertFalse(claim["repair_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIsNone(claim["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
