"""Rails and regular deletions. The short-text rise is not a reading."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_routes import route_report


class DagapeyeffRoutesTest(unittest.TestCase):
    def test_every_other_cell_does_not_reach_prose(self) -> None:
        report = route_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["trials"], 20000)
        self.assertEqual(report["best_rail_period"], 3)
        self.assertEqual(report["best_rail_mi"], 0.7017)
        self.assertEqual(report["rail_14_mi"], 0.6684)
        self.assertEqual(report["best_diagonal_mi"], 0.6582)
        self.assertEqual(report["run_mi"], 2.4135)
        self.assertEqual(report["period2_phase0_mi"], 1.0556)
        self.assertEqual(report["period2_phase1_mi"], 0.6934)
        self.assertEqual(report["english_98_mi"], 1.2922)
        self.assertEqual(report["german_98_mi"], 1.5715)
        self.assertEqual(report["phase0_as_high"], 963)
        self.assertEqual(report["best_phase_as_high"], 1930)
        self.assertEqual(report["closest_deletion"]["period"], 2)
        self.assertLess(report["period2_phase0_mi"], report["english_98_mi"])


if __name__ == "__main__":
    unittest.main()
