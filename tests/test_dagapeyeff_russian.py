"""Russian under four transliterations against the cells' letter counts."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from engine.dagapeyeff_russian import SCHEMES, TREEBANKS, fold

_FROZEN = Path(__file__).resolve().parents[1] / "engine" / "data" / "swarm_cache" / "dagapeyeff-russian.json"


class DagapeyeffRussianTest(unittest.TestCase):
    def test_the_spellings_differ_where_they_should(self) -> None:
        self.assertEqual(fold("Щука и ёж", "british"), "SHCHUKAIEZH")
        self.assertEqual(fold("Щука и ёж", "one-letter"), "SUKAIEZ")
        self.assertEqual(fold("Щука и ёж", "german"), "SCHTSCHUKAIESCH")
        self.assertEqual(fold("Щука и ёж", "french"), "CHTCHOUKAIEI")

    def test_no_spelling_brings_russian_near_latin(self) -> None:
        # Read the frozen file directly so the test never needs the network.
        report = json.loads(_FROZEN.read_text(encoding="utf-8"))
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(len(report["rows"]), len(TREEBANKS) * len(SCHEMES))
        self.assertEqual(report["fewest_errors"], 9)
        self.assertEqual(report["windows_within_8"], 0)
        self.assertGreaterEqual(min(row["median_errors"] for row in report["rows"].values()), 29.0)


if __name__ == "__main__":
    unittest.main()
