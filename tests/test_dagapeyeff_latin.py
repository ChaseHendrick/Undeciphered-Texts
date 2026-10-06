"""Latin, the closest language by counts, does not read the cells under a one-to-one key."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from engine.dagapeyeff_latin import variants
from engine.solvers.dagapeyeff import consider_latin

_FROZEN = Path(__file__).resolve().parents[1] / "engine" / "data" / "swarm_cache" / "dagapeyeff-latin.json"


class DagapeyeffLatinTest(unittest.TestCase):
    def test_the_variants_are_the_square_and_the_book_dummy_rule(self) -> None:
        names = variants(list(range(196)))
        self.assertEqual(len(names), 13)
        self.assertEqual(len(names["nulls 3:1"]), 131)

    def test_planted_latin_comes_back_and_the_cells_do_not_beat_their_shuffles(self) -> None:
        # Read the frozen file directly so the test never needs the network.
        report = json.loads(_FROZEN.read_text(encoding="utf-8"))
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["planted_recovered"], 6)
        self.assertEqual(report["planted_with_errors_recovered"], 6)
        for label in ("cells", "regrouped"):
            row = report["searched"][label]
            self.assertGreaterEqual(row["shuffle_bests_as_high"], 6, label)
        self.assertEqual(sum(row["reaching_cells"] for row in report["random_slips"]), 0)
        claim = consider_latin()
        self.assertFalse(claim["latin_allowed"])


if __name__ == "__main__":
    unittest.main()
