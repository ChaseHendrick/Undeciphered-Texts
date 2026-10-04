"""The board closes a class only when every card it cites is a refusal."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_board import board
from engine.dagapeyeff_infer import infer


class DagapeyeffInferTest(unittest.TestCase):
    def test_three_classes_close_and_one_open_card_reopens_one(self) -> None:
        drawn = infer()
        self.assertIs(drawn["solved"], False)
        self.assertIsNone(drawn["claimed_plaintext"])
        self.assertTrue(drawn["all_listed_closed"])
        self.assertEqual([item["id"] for item in drawn["classes"]], ["counts", "same-cells", "short-keys"])
        self.assertTrue(all(item["status"] == "closed" for item in drawn["classes"]))
        known = {record["id"] for record in board()["records"]}
        for item in drawn["classes"]:
            self.assertTrue(set(item["supports"]) <= known)
        self.assertIn("-2.5185", drawn["required"])
        self.assertIn("not a reading", drawn["required"])
        opened = [dict(record) for record in board()["records"]]
        for record in opened:
            if record["id"] == "word-score":
                record["verdict"] = "open"
        again = infer(opened)
        by_id = {item["id"]: item["status"] for item in again["classes"]}
        self.assertEqual(by_id["short-keys"], "open")
        self.assertEqual(by_id["counts"], "closed")
        self.assertEqual(by_id["same-cells"], "closed")
        self.assertFalse(again["all_listed_closed"])
        self.assertIs(again["solved"], False)
        self.assertIsNone(again["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
