"""Latin under double columnar transposition: power by size."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from engine.dagapeyeff_latindouble import N, encrypt, read_map

_FROZEN = Path(__file__).resolve().parents[1] / "engine" / "data" / "swarm_cache" / "dagapeyeff-latindouble.json"


class DagapeyeffLatinDoubleTest(unittest.TestCase):
    def test_both_read_outs_keep_every_symbol(self) -> None:
        self.assertEqual(sorted(read_map(9, list(range(9)))), list(range(N)))
        cells, origin = encrypt(list(range(N)), [2, 0, 1, 3], 4, [4, 3, 2, 1, 0], 5)
        self.assertEqual(sorted(cells), list(range(N)))
        self.assertEqual(cells, origin)

    def test_power_is_shown_only_at_small_sizes(self) -> None:
        report = json.loads(_FROZEN.read_text(encoding="utf-8"))
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertIs(report["cells_searched"], False)
        small = report["by_size"]["4x5"]
        self.assertEqual(small["recovered"], small["of"])


if __name__ == "__main__":
    unittest.main()
