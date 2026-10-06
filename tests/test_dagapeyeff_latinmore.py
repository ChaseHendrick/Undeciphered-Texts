"""Latin across a repeating shift, a homophonic key and four-square."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

_CACHE = Path(__file__).resolve().parents[1] / "engine" / "data" / "swarm_cache"


class DagapeyeffLatinMoreTest(unittest.TestCase):
    def test_the_count_leaves_the_shift_open_and_the_searches_find_nothing(self) -> None:
        # Read the frozen files directly: rerunning would fetch the Latin text.
        more = json.loads((_CACHE / "dagapeyeff-latinmore.json").read_text(encoding="utf-8"))
        shift = json.loads((_CACHE / "dagapeyeff-latinshift.json").read_text(encoding="utf-8"))
        for data in (more, shift):
            self.assertIs(data["solved"], False)
            self.assertIsNone(data["claimed_plaintext"])
        self.assertEqual(sum(row["reaching_cells"] for row in more["shift_counts"]["rows"]), 1)
        self.assertEqual(more["foursquare"]["planted_recovered"], 3)
        self.assertEqual(more["homophone"]["planted_recovered"], 2)
        for family in ("foursquare", "homophone"):
            self.assertGreaterEqual(more[family]["searched"]["cells"]["shuffles_as_high"], 5, family)
        self.assertGreaterEqual(shift["planted_recovered"], 15)


if __name__ == "__main__":
    unittest.main()
