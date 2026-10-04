"""Outside claims about column 14, reduced to counts. Not a reading."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_column import column_report


class DagapeyeffColumnTest(unittest.TestCase):
    def test_column_14_holds_the_rare_cells_and_is_the_worst_to_drop(self) -> None:
        report = column_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["missing"], ("61", "73", "95", "01", "02", "03", "05"))
        self.assertEqual(report["distinct"], 18)
        self.assertEqual(report["ic"], 0.069702)
        self.assertEqual(report["singletons"], 3)
        self.assertEqual(report["singletons_in_column_14"], 3)
        self.assertAlmostEqual(report["p_singletons"], 2.946e-4, places=6)
        self.assertEqual(report["cells_at_most_two"], 5)
        self.assertEqual(report["at_most_two_in_column_14"], 5)
        self.assertAlmostEqual(report["p_at_most_two"], 8.744e-7, places=9)
        self.assertEqual(report["pelling_cells"], 4)
        self.assertEqual(report["pelling_in_column_14"], 4)
        self.assertEqual(report["worst_drop_column"], 13)
        self.assertEqual(report["worst_drop_chi"], 45.57)
        self.assertEqual(report["best_drop_chi"], 26.23)
        self.assertEqual(report["english_as_flat"], 0)


if __name__ == "__main__":
    unittest.main()
