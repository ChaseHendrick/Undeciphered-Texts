"""A one-to-one pair cipher keeps the number of different pairs; the cells' count is ordinary."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_pairmap import different_pairs, pairmap_report
from engine.solvers.dagapeyeff import consider_pairmap


class DagapeyeffPairmapTest(unittest.TestCase):
    def test_counting_starts_at_the_stated_phase(self) -> None:
        self.assertEqual(different_pairs("ABABCD", 0), 2)
        self.assertEqual(different_pairs("ABABCD", 1), 2)
        self.assertEqual(different_pairs("XABABX", 1), 1)

    def test_the_cells_are_ordinary_and_the_regrouping_is_not(self) -> None:
        report = pairmap_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["windows"], 479051)
        self.assertEqual(report["kept_by_foursquare"], {"windows": 201, "count_moved": 0})
        cells = report["texts"]["cells"]
        self.assertEqual(cells["phase 0"], {"different_pairs": 79, "windows_as_many": 29336, "windows_as_few": 461936})
        self.assertEqual(cells["phase 1"], {"different_pairs": 80, "windows_as_many": 11539, "windows_as_few": 473085})
        regrouped = report["texts"]["regrouped"]
        self.assertEqual(regrouped["phase 0"]["different_pairs"], 85)
        self.assertEqual(regrouped["phase 0"]["windows_as_many"], 325)
        self.assertEqual(regrouped["phase 1"]["different_pairs"], 85)
        self.assertEqual(regrouped["phase 1"]["windows_as_many"], 161)
        claim = consider_pairmap()
        self.assertFalse(claim["pairmap_allowed"])


if __name__ == "__main__":
    unittest.main()
