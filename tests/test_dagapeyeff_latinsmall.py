"""Latin under columnar transposition at widths 2 to 9 with a letter key."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from engine.dagapeyeff_latinsmall import WIDTHS

_FROZEN = Path(__file__).resolve().parents[1] / "engine" / "data" / "swarm_cache" / "dagapeyeff-latinsmall.json"


class DagapeyeffLatinSmallTest(unittest.TestCase):
    def test_planted_latin_comes_back_and_the_cells_do_not_read(self) -> None:
        report = json.loads(_FROZEN.read_text(encoding="utf-8"))
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["planted"], 48)
        self.assertEqual(report["planted_recovered"], 48)
        self.assertEqual({row["width"] for row in report["rows"]}, set(WIDTHS))
        self.assertLess(report["searched_best"], report["weakest_recovered_found"] - 0.9)
        self.assertLessEqual(report["cases_cells_above_all_shuffles"], 6)


if __name__ == "__main__":
    unittest.main()
