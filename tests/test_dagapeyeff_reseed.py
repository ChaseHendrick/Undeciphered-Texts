"""The second-seed reruns of four-square and the repeating shift agree with the first runs."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from engine.dagapeyeff_reseed import PENDING, PROBES

_FROZEN = Path(__file__).resolve().parents[1] / "engine" / "data" / "swarm_cache" / "dagapeyeff-reseed.json"


class DagapeyeffReseedTest(unittest.TestCase):
    def test_both_seeds_recover_planted_text_and_the_cells_stay_below(self) -> None:
        report = json.loads(_FROZEN.read_text(encoding="utf-8"))
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual([row["probe"] for row in report["rows"]], [name for name, _, _ in PROBES])
        self.assertTrue(report["cells_below_weakest_both"])
        for row in report["rows"]:
            self.assertNotEqual(row["first_seed"], row["second_seed"])
            for run in ("first", "second"):
                self.assertGreaterEqual(row[run]["recovered"], row[run]["planted"] - 2)
                self.assertGreater(row[run]["gap"], 0.9)
                self.assertLess(row[run]["shuffles_as_high"], row[run]["shuffles"])

    def test_the_rest_is_listed_as_pending(self) -> None:
        self.assertEqual(len(PENDING), 5)
        self.assertFalse({name for name, _, _ in PENDING} & {name for name, _, _ in PROBES})


if __name__ == "__main__":
    unittest.main()
