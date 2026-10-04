"""Splitting a crowded cell does not create a reading."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_split import split_report


class DagapeyeffSplitTest(unittest.TestCase):
    def test_splitting_the_crowded_cells_stays_below_prose(self) -> None:
        report = split_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["trials"], 75000)
        self.assertEqual(report["best_cell"], "81")
        self.assertEqual(report["best_mi"], 0.7002)
        self.assertEqual(report["cells"]["91"]["best_mi"], 0.6542)
        self.assertEqual(report["cells"]["75"]["best_mi"], 0.6807)
        self.assertEqual(report["cells"]["81"]["count"], 20)
        self.assertEqual(report["null_as_high"], 15)
        self.assertEqual(report["english_mi"], 1.0658)
        self.assertLess(report["best_mi"], report["english_mi"])


if __name__ == "__main__":
    unittest.main()
