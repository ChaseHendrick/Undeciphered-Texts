"""A homophonic key under any transposition cannot give the cells' counts from English or Latin."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from engine.dagapeyeff_homgroup import exact_grouping

_CACHE = Path(__file__).resolve().parents[1] / "engine" / "data" / "swarm_cache"


class DagapeyeffHomgroupTest(unittest.TestCase):
    def test_exact_grouping(self) -> None:
        self.assertTrue(exact_grouping([5, 3, 2, 2], [7, 5]))
        self.assertFalse(exact_grouping([5, 3, 2, 2], [6, 6]))
        self.assertFalse(exact_grouping([5, 3], [4, 2, 2]))

    def test_no_window_groups_exactly(self) -> None:
        # Read the frozen file directly: rerunning would fetch the Latin text.
        data = json.loads((_CACHE / "dagapeyeff-homgroup.json").read_text(encoding="utf-8"))
        self.assertIs(data["solved"], False)
        self.assertIsNone(data["claimed_plaintext"])
        self.assertEqual(data["symbols"], 18)
        self.assertEqual(data["english"]["windows_within_18_letters"], 0)
        self.assertGreaterEqual(data["english"]["fewest_letters"], 19)
        self.assertEqual(data["latin"]["exact_groupings"], 0)
        self.assertGreaterEqual(data["latin"]["fewest_errors_found"], 1)


if __name__ == "__main__":
    unittest.main()
