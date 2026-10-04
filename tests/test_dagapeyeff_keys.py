"""A column order of the regrouped cells does not beat repeated shuffles."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_keys import key_report
from engine.solvers.dagapeyeff import consider_column_key


class DagapeyeffKeysTest(unittest.TestCase):
    def test_one_shuffle_sample_is_not_a_win(self) -> None:
        report = key_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["reorder"], "01432")
        self.assertEqual(report["draws"], 20000)
        self.assertEqual(report["repeats"], 20)
        self.assertEqual(report["best_row_mi"], 1.0033)
        self.assertEqual(report["best_down_mi"], 0.9427)
        self.assertEqual(report["shuffle_max_mi"], 0.9925)
        self.assertEqual(report["english_mi"], 1.0658)
        self.assertTrue(report["one_sample_higher"])
        self.assertEqual(report["repeats_as_high"], 13)
        self.assertFalse(report["key_reaches_english"])
        claim = consider_column_key()
        self.assertFalse(claim["column_key_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIsNone(claim["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
