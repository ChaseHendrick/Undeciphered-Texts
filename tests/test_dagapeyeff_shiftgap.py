"""The repeating coordinate shift at periods 6 and 8 to 13, English and Latin."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from engine.dagapeyeff_shiftgap import PERIODS

_FROZEN = Path(__file__).resolve().parents[1] / "engine" / "data" / "swarm_cache" / "dagapeyeff-shiftgap.json"


class DagapeyeffShiftGapTest(unittest.TestCase):
    def test_the_missing_periods_are_the_ones_searched(self) -> None:
        self.assertEqual(sorted(set(range(2, 15)) - {2, 3, 4, 5, 7, 14}), list(PERIODS))

    def test_planted_texts_come_back_and_the_cells_do_not_read(self) -> None:
        report = json.loads(_FROZEN.read_text(encoding="utf-8"))
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        english, latin = report["english"], report["latin"]
        self.assertEqual(english["planted_recovered"], 26)
        self.assertEqual(latin["planted_recovered"], 25)
        self.assertEqual(sum(row["reaching_cells"] for row in english["counts"]), 0)
        self.assertGreaterEqual(min(row["fewest_distinct"] for row in english["counts"]), 23)
        for x in (english, latin):
            weakest = min(p["found_per_letter"] for p in x["planted"] if p["letters_right"] >= 0.9)
            self.assertLess(x["searched_best"]["per_letter"], weakest - 1)
            self.assertLessEqual(x["cases_cells_above_all_shuffles"], len(x["searched"]) // 4)


if __name__ == "__main__":
    unittest.main()
