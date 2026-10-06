"""Latin under a complete 14-column transposition does not read the cells."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

_FROZEN = Path(__file__).resolve().parents[1] / "engine" / "data" / "swarm_cache" / "dagapeyeff-latin14.json"


class DagapeyeffLatin14Test(unittest.TestCase):
    def test_planted_latin_comes_back_and_the_printed_cells_sit_in_their_shuffles(self) -> None:
        # Read the frozen file directly: rerunning would fetch the Latin text.
        report = json.loads(_FROZEN.read_text(encoding="utf-8"))
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["planted_recovered"], 8)
        self.assertEqual(len(report["planted"]), 8)
        for direction in ("undone", "done"):
            self.assertGreaterEqual(report["searched"][f"cells {direction}"]["shuffles_as_high"], 5)


if __name__ == "__main__":
    unittest.main()
