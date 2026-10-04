"""Members refuse a closed job. The one they allow fails the square."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_board import board
from engine.dagapeyeff_foresight import foresight


class DagapeyeffForesightTest(unittest.TestCase):
    def test_only_the_group_digit_job_is_allowed_and_it_fails(self) -> None:
        report = foresight()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["accepted"], ["group-digit"])
        self.assertEqual(report["verdict"], "refuse")
        self.assertEqual(report["groups"], 79)
        self.assertEqual(report["phases_on_square"], 0)
        self.assertEqual(report["fewest_off_square"], 79)
        self.assertEqual(
            [phase["off_square"] for phase in report["phases"]],
            [80, 119, 79, 118, 79],
        )
        by_job = {item["id"]: [reason["member"] for reason in item["by"]] for item in report["rejected"]}
        self.assertIn("class-guard", by_job["period-5"])
        self.assertIn("budget", by_job["period-5"])
        self.assertIn("class-guard", by_job["column-order"])
        self.assertIn("closer", by_job["column-order"])
        opened = [dict(record) for record in board()["records"]]
        for record in opened:
            if record["id"] == "word-score":
                record["verdict"] = "open"
        again = foresight(opened)
        again_by = {item["id"]: [reason["member"] for reason in item["by"]] for item in again["rejected"]}
        self.assertNotIn("class-guard", again_by["period-5"])
        self.assertIn("budget", again_by["period-5"])
        self.assertEqual(again["accepted"], ["group-digit"])
        self.assertIs(again["solved"], False)
        self.assertIsNone(again["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
