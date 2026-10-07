"""Esperanto against the cells' letter counts."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from engine.dagapeyeff_esperanto import BOOKS, body
from engine.dagapeyeff_screen import fold

_FROZEN = Path(__file__).resolve().parents[1] / "engine" / "data" / "swarm_cache" / "dagapeyeff-esperanto.json"


class DagapeyeffEsperantoTest(unittest.TestCase):
    def test_the_x_system_becomes_hats_and_hats_are_dropped(self) -> None:
        raw = "*** START OF X ***\nCxu vi sxatas mangxi? Jes. cxiuj\n*** END OF X ***\nlicense"
        self.assertEqual(fold(body(raw)), "CUVISATASMANGIIESCIUI")
        self.assertEqual(fold(body("ĉu ŝi ĝojas")), "CUSIGOIAS")

    def test_esperanto_is_no_closer_than_english(self) -> None:
        report = json.loads(_FROZEN.read_text(encoding="utf-8"))
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(len(report["book_letters"]), len(BOOKS))
        row = report["esperanto"]
        self.assertEqual(row["fewest_errors"], 9)
        self.assertEqual(row["median_errors"], 28.0)
        self.assertEqual(row["within_8"], 0)


if __name__ == "__main__":
    unittest.main()
