"""The five last-column symbols as padding or as rare letters."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_rarecolumn import private_symbols, rare_letters

_FROZEN = Path(__file__).resolve().parents[1] / "engine" / "data" / "swarm_cache" / "dagapeyeff-rarecolumn.json"


class DagapeyeffRareColumnTest(unittest.TestCase):
    def test_the_private_symbols_are_the_five_known_cells(self) -> None:
        cells = _cells()
        private = private_symbols(cells)
        self.assertEqual(len(private), 5)
        self.assertEqual(sum(cells.count(s) for s in private), 8)
        self.assertEqual(len({x for x in cells if x not in private}), 13)

    def test_a_packed_window_is_counted(self) -> None:
        text = "AB" * 91 + "XXXYYZQW" + "AB" * 3
        self.assertEqual(rare_letters(text, 8)["rare_in_one_stretch"], 1)
        spread = "XAB" * 3 + "AB" * 80 + "YYZQW" + "AB" * 11
        self.assertEqual(rare_letters(spread, 8)["rare_in_one_stretch"], 0)

    def test_neither_reading_fits_latin_or_english(self) -> None:
        report = json.loads(_FROZEN.read_text(encoding="utf-8"))
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["symbols_without_private"], 13)
        for row in report["padding"].values():
            self.assertGreaterEqual(row["fewest"], 14)
            self.assertEqual(row["at_most"], 0)
        for row in report["rare_letters"].values():
            self.assertGreater(row["five_or_more_rare"], row["windows"] // 3)
            self.assertEqual(row["rare_in_one_stretch"], 0)


if __name__ == "__main__":
    unittest.main()
