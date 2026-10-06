"""Every Universal Dependencies language against the cells' letter counts."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from engine.dagapeyeff_alllanguages import TREEBANKS, letters, script

_FROZEN = Path(__file__).resolve().parents[1] / "engine" / "data" / "swarm_cache" / "dagapeyeff-alllanguages.json"


class DagapeyeffAllLanguagesTest(unittest.TestCase):
    def test_scripts_are_named_and_alphabets_are_romanized(self) -> None:
        self.assertEqual(script("Gallia est omnis"), "LATIN")
        self.assertEqual(script("Ψυχή"), "GREEK")
        self.assertEqual(script("שלום"), "HEBREW")
        self.assertEqual(script("123"), "NONE")
        self.assertEqual(letters("Jacopo", "LATIN"), "IACOPO")

    def test_latin_stands_out_among_every_language(self) -> None:
        report = json.loads(_FROZEN.read_text(encoding="utf-8"))
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        rows = report["languages"]
        self.assertEqual(len(rows) + len(report["skipped"]), len(TREEBANKS))
        self.assertEqual(len(rows), 98)
        self.assertEqual(report["ranked"][0], "Latin-ITTB")
        latin = rows["Latin-ITTB"]
        others = [row for name, row in rows.items() if name != "Latin-ITTB"]
        self.assertLess(latin["median_errors"], min(row["median_errors"] for row in others))
        self.assertGreater(latin["within_8_per_million_windows"], 3 * max(row["within_8_per_million_windows"] for row in others))
        self.assertEqual(min(row["fewest_errors"] for row in others), 4)


if __name__ == "__main__":
    unittest.main()
