"""A thousand attacks. The hits are the pile and the glue, nothing else."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_battery import battery_report


class DagapeyeffBatteryTest(unittest.TestCase):
    def test_only_the_pile_and_the_glue_hit(self) -> None:
        report = battery_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["attacks"], 1000)
        self.assertEqual(report["shuffles"], 500)
        self.assertEqual(report["trials"], 1000000)
        self.assertEqual(
            report["order_hit_labels"],
            (
                "width 7, at most 2",
                "width 7, at most 3",
                "width 7, at most 4",
                "width 7, at most 5",
                "width 14, at most 2",
                "width 14, at most 3",
                "width 14, at most 4",
                "width 14, at most 5",
                "width 28, at most 3",
                "width 28, at most 4",
                "width 28, at most 5",
            ),
        )
        self.assertEqual(report["pile_14_tail"], 0)
        self.assertEqual(report["lag1_pair_tail"], 100)
        self.assertEqual(report["association_order_tail"], 500)
        self.assertEqual(report["association_repair_tail"], 0)
        self.assertEqual(
            report["repair_families"],
            {"pile": 3, "window": 55, "cross": 1, "association": 1},
        )
        self.assertEqual(report["repair_hit_count"], 60)


if __name__ == "__main__":
    unittest.main()
