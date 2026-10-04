"""The two digits are glued. Neither stream has an order of its own."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_glue import glue_report


class DagapeyeffGlueTest(unittest.TestCase):
    def test_pairing_is_real_and_order_is_not(self) -> None:
        report = glue_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["trials"], 70000)
        self.assertEqual(report["association"], 77.36)
        self.assertEqual(report["association_as_high"], 0)
        self.assertEqual(report["pair_91"], 12)
        self.assertEqual(report["pair_61"], 0)
        self.assertEqual(report["row_mi"], 0.0275)
        self.assertEqual(report["column_mi"], 0.0428)
        self.assertEqual(report["row_as_high"], 15767)
        self.assertEqual(report["column_as_high"], 9044)
        self.assertEqual(report["row_best_lag"], 0.3526)
        self.assertEqual(report["column_best_lag"], 0.2554)
        self.assertEqual(report["row_lag_as_high"], 4205)
        self.assertEqual(report["column_lag_as_high"], 4150)


if __name__ == "__main__":
    unittest.main()
