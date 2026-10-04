"""The flattering regrouping loses to a shuffle and hurts the solved example."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_regroup import regroup_report
from engine.solvers.dagapeyeff import consider_regrouping


class DagapeyeffRegroupTest(unittest.TestCase):
    def test_the_flattering_regrouping_is_refused(self) -> None:
        report = regroup_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["reorder"], "01432")
        self.assertEqual(report["chi_lo"], 8.8291)
        self.assertEqual(report["chi_hi"], 8.889665)
        self.assertTrue(report["frequency_clears_english_worst"])
        self.assertEqual(report["order_mi"], 0.7801)
        self.assertEqual(report["printed_mi"], 0.5706)
        self.assertEqual(report["english_mi"], 1.0658)
        self.assertTrue(report["order_still_below_english"])
        self.assertEqual(report["down_mi"], 0.8735)
        self.assertEqual(report["draws"], 10000)
        self.assertEqual(report["row_shuffles_as_high"], 9700)
        self.assertEqual(report["down_shuffles_as_high"], 2216)
        self.assertEqual(report["control_printed_chi"], 4.14)
        self.assertEqual(report["control_flipped_chi"], 21.56)
        claim = consider_regrouping()
        self.assertFalse(claim["regrouping_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIsNone(claim["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
