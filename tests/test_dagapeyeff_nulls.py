"""Dummy letters from the book. The friendliest schedule is still not English."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_nulls import schedules, search_nulls, worker_report


class DagapeyeffNullsTest(unittest.TestCase):
    def test_menu_and_one_worker(self) -> None:
        self.assertEqual(len(schedules()), 495)
        first = worker_report(0)
        self.assertEqual(first["period"], 2)
        self.assertEqual(first["phase"], 0)
        self.assertEqual(first["chi"], 11.33)
        self.assertIsNone(first["claimed_plaintext"])

    def test_best_schedule_loses_to_english(self) -> None:
        report = search_nulls()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["schedules"], 495)
        self.assertEqual(report["best_period"], 2)
        self.assertEqual(report["best_phase"], 0)
        self.assertEqual(report["best_kept"], 98)
        self.assertEqual(report["best_chi"], 11.33)
        self.assertEqual(report["book"]["3"]["chi"], 18.49)
        self.assertEqual(report["book"]["4"]["chi"], 18.77)
        self.assertEqual(report["book"]["5"]["phase"], 3)
        self.assertEqual(report["book"]["5"]["chi"], 20.26)
        self.assertEqual(report["english_cherry_draws"], 80)
        self.assertEqual(report["english_cherry_median"], 3.61)
        self.assertEqual(report["english_as_high"], 0)
        self.assertEqual(report["digit_deletions_still_a_square"], 0)
        self.assertEqual(report["control_best_chi"], 2.2)


if __name__ == "__main__":
    unittest.main()
