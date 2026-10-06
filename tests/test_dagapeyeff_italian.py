"""Italian under a one-to-one key, with or without errors at the book's rate, does not read the cells."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from engine.dagapeyeff_italian import COMMIT, fold
from engine.solvers.dagapeyeff import consider_italian

_FROZEN = Path(__file__).resolve().parents[1] / "engine" / "data" / "swarm_cache" / "dagapeyeff-italian.json"


class DagapeyeffItalianTest(unittest.TestCase):
    def test_accents_are_removed_and_j_is_folded(self) -> None:
        self.assertEqual(fold("Perché già Jacopo"), "PERCHEGIAIACOPO")

    def test_the_frozen_result_closes_italian_under_a_one_to_one_key(self) -> None:
        # Read the frozen file directly so the test never needs the network.
        report = json.loads(_FROZEN.read_text(encoding="utf-8"))
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["source"]["commit"], COMMIT)
        counts = report["counts"]
        self.assertEqual(counts["windows_within_8"], 0)
        self.assertGreaterEqual(counts["fewest_errors"], 9)
        self.assertEqual(sum(row["reaching_cells"] for row in counts["random_slips"]), 0)
        self.assertEqual(report["planted_recovered"], 4)
        self.assertEqual(report["planted_with_errors_recovered"], 4)
        self.assertGreater(report["planted_with_errors_lowest_found"], report["cells_per_letter"] + 1.0)
        self.assertGreaterEqual(report["shuffles_as_high"], 3)
        claim = consider_italian()
        self.assertFalse(claim["italian_allowed"])


if __name__ == "__main__":
    unittest.main()
