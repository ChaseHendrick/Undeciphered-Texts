"""Every window of a larger Latin library against the cells' letter counts."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

import numpy as np

from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_errors import sorted_counts
from engine.dagapeyeff_foursquare import PLAIN
from engine.dagapeyeff_latinlib import BOOKS, TREEBANKS, errors_per_window, is_latin

_FROZEN = Path(__file__).resolve().parents[1] / "engine" / "data" / "swarm_cache" / "dagapeyeff-latinlib.json"


class DagapeyeffLatinLibraryTest(unittest.TestCase):
    def test_a_window_with_the_cells_counts_needs_no_errors(self) -> None:
        cells = _cells()
        letters = "".join(PLAIN[cell] for cell in cells)
        target = sorted_counts(cells).astype(np.int32)
        errors = errors_per_window("A" * 50 + letters + "A" * 50, target)
        self.assertEqual(int(errors[50]), 0)
        self.assertGreater(int(errors[0]), 0)

    def test_english_notes_are_left_out(self) -> None:
        self.assertTrue(is_latin("Gallia est omnis divisa in partes tres, quarum unam incolunt Belgae"))
        self.assertFalse(is_latin("The note on this line is that the and of the text is in doubt"))

    def test_no_latin_window_is_a_clean_source(self) -> None:
        report = json.loads(_FROZEN.read_text(encoding="utf-8"))
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(len(report["sources"]), len(TREEBANKS) + len(BOOKS))
        self.assertGreater(report["letters"], 8_000_000)
        self.assertEqual(report["fewest_errors"], 4)
        self.assertEqual(report["within_2"], 0)
        for item in report["closest"]:
            self.assertEqual(set(item), {"source", "offset", "errors"})


if __name__ == "__main__":
    unittest.main()
