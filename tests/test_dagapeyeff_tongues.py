"""Catalan and Romanian under a keyed square do not read the cells; a Romanian edge at 8 shuffles goes at 40."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

_CACHE = Path(__file__).resolve().parents[1] / "engine" / "data" / "swarm_cache"


class DagapeyeffTonguesTest(unittest.TestCase):
    def test_planted_texts_come_back_and_the_cells_sit_in_their_shuffles(self) -> None:
        # Read the frozen files directly: rerunning would fetch the treebanks.
        report = json.loads((_CACHE / "dagapeyeff-tongues.json").read_text(encoding="utf-8"))
        wide = json.loads((_CACHE / "dagapeyeff-romanian-wide.json").read_text(encoding="utf-8"))
        for data in (report, wide):
            self.assertIs(data["solved"], False)
            self.assertIsNone(data["claimed_plaintext"])
        for name, row in report["languages"].items():
            self.assertEqual(row["planted_recovered"], 3, name)
            self.assertEqual(row["planted_with_errors_recovered"], 3, name)
        self.assertGreaterEqual(report["languages"]["Catalan-AnCora"]["searched"]["cells"]["shuffle_bests_as_high"], 6)
        self.assertEqual(wide["shuffles"], 40)
        for label in ("cells", "regrouped"):
            self.assertGreaterEqual(wide["searched"][label]["shuffle_bests_as_high"], 8, label)


if __name__ == "__main__":
    unittest.main()
