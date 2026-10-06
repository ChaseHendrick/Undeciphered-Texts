"""Latin under columnar transposition at widths 10 to 13 and 15 with a letter key."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from engine.dagapeyeff_columnarw import WIDTHS, encrypt, lengths

_FROZEN = Path(__file__).resolve().parents[1] / "engine" / "data" / "swarm_cache" / "dagapeyeff-latinw.json"


class DagapeyeffLatinWidthsTest(unittest.TestCase):
    def test_a_short_last_row_keeps_every_symbol(self) -> None:
        self.assertEqual(sum(lengths(13)), 196)
        cells, source = encrypt(list(range(196)), list(range(13)), 13, "undone")
        self.assertEqual(sorted(cells), list(range(196)))
        self.assertEqual(cells, [source[i] for i in range(196)])

    def test_planted_latin_comes_back_and_the_cells_do_not_read(self) -> None:
        report = json.loads(_FROZEN.read_text(encoding="utf-8"))
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["planted"], 40)
        self.assertEqual(report["planted_recovered"], 39)
        self.assertEqual({row["width"] for row in report["rows"]}, set(WIDTHS))
        for row in report["rows"]:
            weakest_found = max(p["found_per_letter"] for p in row["planted"] if p["cells_right"] >= 0.9)
            self.assertLess(row["cells"]["per_letter"], -3.5)
            self.assertLess(row["cells"]["per_letter"], weakest_found)
            self.assertGreaterEqual(row["cells"]["shuffles_as_high"], 1)


if __name__ == "__main__":
    unittest.main()
