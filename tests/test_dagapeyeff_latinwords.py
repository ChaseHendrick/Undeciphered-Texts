"""Latin word coverage of the cells' best decryptions against planted Latin with errors."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from engine.dagapeyeff_latinwords import MIN_WORD, coverage

_FROZEN = Path(__file__).resolve().parents[1] / "engine" / "data" / "swarm_cache" / "dagapeyeff-latinwords.json"


class DagapeyeffLatinWordsTest(unittest.TestCase):
    def test_coverage_counts_only_long_words(self) -> None:
        self.assertEqual(MIN_WORD, 5)
        self.assertEqual(coverage("QQQQQQQQQQ"), 0.0)

    def test_planted_latin_keeps_its_words_and_the_cells_do_not(self) -> None:
        report = json.loads(_FROZEN.read_text(encoding="utf-8"))
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        cells = report["searched"]["cells"]
        self.assertGreaterEqual(cells["shuffles_as_high"], 1)
        self.assertGreaterEqual(report["planted_above_cells"], report["planted"] - 3)
        self.assertGreater(min(report["planted_by_errors"]["0"]["coverage"]), cells["best_coverage"])
        for row in report["rows"]:
            self.assertNotIn("text", row)


if __name__ == "__main__":
    unittest.main()
