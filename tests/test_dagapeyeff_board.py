"""The swarm board says what was refused, and what not to repeat."""

from __future__ import annotations

import unittest
from pathlib import Path

from engine.dagapeyeff_board import board, board_text, search_board

_PAGE = Path(__file__).resolve().parents[1] / "docs" / "logs" / "swarm-board-2026-10-04.md"


class DagapeyeffBoardTest(unittest.TestCase):
    def test_every_swarm_is_refused_and_searchable(self) -> None:
        data = board()
        self.assertEqual(data["schema"], "swarm-board-1")
        self.assertIs(data["solved"], False)
        self.assertIsNone(data["claimed_plaintext"])
        self.assertEqual(len(data["records"]), 10)
        self.assertTrue(all(record["verdict"] == "refuse" for record in data["records"]))
        self.assertTrue(all(record["solved"] is False for record in data["records"]))
        self.assertTrue(all(record["claimed_plaintext"] is None for record in data["records"]))
        self.assertIn("-2.5185", data["bar"])
        period = search_board("period-4")
        self.assertEqual(
            [record["id"] for record in period],
            ["period-4", "word-score", "running-key"],
        )
        self.assertEqual(
            [record["id"] for record in search_board("01432")],
            ["regrouping", "column-key", "language-model"],
        )
        self.assertEqual(search_board(""), [])
        self.assertEqual(_PAGE.read_text(encoding="utf-8"), board_text())


if __name__ == "__main__":
    unittest.main()
