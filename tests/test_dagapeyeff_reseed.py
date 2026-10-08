"""The second-seed reruns of four-square, the repeating shift and the Latin searches agree with the first runs."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from engine.dagapeyeff_reseed import PENDING, PROBES, _PARTS

_FROZEN = Path(__file__).resolve().parents[1] / "engine" / "data" / "swarm_cache" / "dagapeyeff-reseed.json"


class DagapeyeffReseedTest(unittest.TestCase):
    def test_both_seeds_recover_planted_text_and_the_cells_stay_below(self) -> None:
        report = json.loads(_FROZEN.read_text(encoding="utf-8"))
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        expected = [name if part is None else f"{name} {part}"
                    for name, _, _ in PROBES for part in _PARTS.get(name, (None,))]
        self.assertEqual([row["probe"] for row in report["rows"]], expected)
        self.assertTrue(report["cells_below_weakest_both"])
        for row in report["rows"]:
            with self.subTest(probe=row["probe"]):
                self.assertNotEqual(row["first_seed"], row["second_seed"])
                first, second = row["first"], row["second"]
                self.assertEqual(first["planted"], second["planted"])
                self.assertGreaterEqual(second["recovered"], first["recovered"] - 2)
                for run in (first, second):
                    self.assertGreater(run["gap"], 0)
                    self.assertLess(run["shuffles_as_high"], run["shuffles"])

    def test_every_search_the_paper_reruns_has_two_seeds(self) -> None:
        self.assertEqual(PENDING, ())
        self.assertEqual(len(PROBES), 7)


if __name__ == "__main__":
    unittest.main()
