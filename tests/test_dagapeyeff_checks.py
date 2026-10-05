"""Frozen scores claim nothing, order does not change chi, and the zero is forced."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_checks import checks_report
from engine.dagapeyeff_foresight import after_training


class DagapeyeffChecksTest(unittest.TestCase):
    def test_the_zero_is_forced_and_the_cache_claims_nothing(self) -> None:
        report = checks_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertTrue(report["sound"])
        self.assertEqual(report["cache"], {"files": 90, "claiming_a_reading": []})
        self.assertEqual(report["order"]["pairs"], 196)
        self.assertEqual(report["order"]["forward_chi"], 34.23)
        self.assertEqual(report["order"]["reversed_chi"], 34.23)
        self.assertFalse(report["order"]["order_changes_chi"])
        parity = report["parity"]
        self.assertEqual(parity["groups"], 79)
        self.assertEqual(parity["interior_breaks"], 0)
        self.assertEqual(parity["both_ends_on_square"], 0)
        self.assertTrue(parity["last_group_left_on_square"])
        self.assertFalse(parity["last_group_right_on_square"])
        self.assertTrue(parity["forced_by_odd_groups"])
        self.assertEqual(parity["shuffles_as_low"], 1)
        self.assertEqual(parity["shuffle_draws"], 2000)
        self.assertFalse(parity["shuffle_is_evidence"])
        trained = after_training()
        self.assertEqual(trained["accepted"], ["end-pairs"])
        self.assertEqual(report["trained_accepted"], ["end-pairs"])
        by_job = {item["id"]: [reason["member"] for reason in item["by"]] for item in trained["rejected"]}
        self.assertIn("budget", by_job["group-digit"])
        self.assertIs(trained["solved"], False)
        self.assertIsNone(trained["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
