"""Column keys and digit reads. Neither one is a reading."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_reads import read_report


class DagapeyeffReadsTest(unittest.TestCase):
    def test_keys_do_not_stand_out_and_width_3_is_ordinary_ungluing(self) -> None:
        report = read_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["trials"], 50000)
        self.assertEqual(report["printed_digrams"], 65)
        self.assertEqual(report["down_digrams"], 74)
        self.assertEqual(report["row_keys_at_least_printed"], 7883)
        self.assertEqual(report["down_keys_at_least_straight"], 2531)
        self.assertEqual(report["row_best"], 84)
        self.assertEqual(report["replica_row_best"], 81)
        self.assertEqual(report["down_best"], 77)
        self.assertEqual(report["replica_down_best"], 77)
        self.assertEqual(report["legal_widths"], (3,))
        self.assertEqual(report["even_width_legal"], {2: 0, 4: 0, 14: 0})
        self.assertEqual(report["width_3_chi"], 11.73)
        self.assertEqual(report["width_3_overlap"], 153)
        self.assertEqual(report["repair_median_chi"], 9.86)
        self.assertEqual(report["repairs_as_good"], 7473)
        self.assertEqual(report["english_as_flat_as_width_3"], 1067)
        self.assertEqual(report["common_concentration"], 44)
        self.assertEqual(report["common_as_high"], 529)


if __name__ == "__main__":
    unittest.main()
