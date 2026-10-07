"""Latin under a turning grille: how right the key must be, and the nested search."""

from __future__ import annotations

import json
import random
import unittest
from pathlib import Path

from engine.dagapeyeff_grille import ORBITS
from engine.dagapeyeff_latingrille import spoil

_FROZEN = Path(__file__).resolve().parents[1] / "engine" / "data" / "swarm_cache" / "dagapeyeff-latingrille.json"


class DagapeyeffLatinGrilleTest(unittest.TestCase):
    def test_spoiling_keeps_a_permutation(self) -> None:
        key = list(range(25))
        cells = [i % 18 for i in range(196)]
        spoiled = spoil(key, cells, 0.3, random.Random(1))
        self.assertEqual(sorted(spoiled), key)
        self.assertNotEqual(spoiled, key)

    def test_power_needs_a_nearly_right_key(self) -> None:
        report = json.loads(_FROZEN.read_text(encoding="utf-8"))
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertIs(report["cells_searched"], False)
        exact = report["fixed_by_spoiled"]["0.0"]
        self.assertEqual(exact["recovered"], exact["of"])
        self.assertEqual(report["fixed_by_spoiled"]["0.3"]["recovered"], 0)
        self.assertEqual(report["nested_recovered"], 0)
        self.assertLess(report["nested_holes_high"], ORBITS)


if __name__ == "__main__":
    unittest.main()
