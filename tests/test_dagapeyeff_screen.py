"""A key-free screen of 39 languages by the fewest errors that reach the cells' letter counts."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from engine.dagapeyeff_screen import fold

_FROZEN = Path(__file__).resolve().parents[1] / "engine" / "data" / "swarm_cache" / "dagapeyeff-screen.json"


class DagapeyeffScreenTest(unittest.TestCase):
    def test_letters_are_folded_and_russian_is_transliterated(self) -> None:
        self.assertEqual(fold("Straße Þórr Łódź"), "STRASSETHORRLODZ")
        self.assertEqual(fold("Щука и ёж"), "SHCHUKAIEZH")
        self.assertEqual(fold("Jacopo"), "IACOPO")

    def test_latin_is_the_closest_language(self) -> None:
        # Read the frozen file directly so the test never needs the network.
        report = json.loads(_FROZEN.read_text(encoding="utf-8"))
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(len(report["languages"]), 39)
        self.assertEqual(report["ranked"][0], "Latin-ITTB")
        latin = report["languages"]["Latin-ITTB"]
        self.assertEqual(latin["fewest_errors"], 4)
        self.assertEqual(latin["median_errors"], 22.0)
        self.assertLessEqual(report["languages"]["Latin-Perseus"]["median_errors"],
                             min(row["median_errors"] for name, row in report["languages"].items()
                                 if not name.startswith("Latin")))


if __name__ == "__main__":
    unittest.main()
