"""The manuscript's numbers are generated from the frozen results and are current."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

import importlib.util

_HERE = Path(__file__).resolve().parents[1] / "papers" / "dagapeyeff-exclusions"
_SPEC = importlib.util.spec_from_file_location("make_numbers", _HERE / "code" / "make_numbers.py")
make_numbers = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(make_numbers)


class DagapeyeffPaperTest(unittest.TestCase):
    def test_generated_files_are_current(self) -> None:
        for name, text in make_numbers.render().items():
            self.assertEqual((_HERE / "paper" / name).read_text(encoding="utf-8"), text, name)

    def test_every_macro_used_is_defined(self) -> None:
        defined = set(re.findall(r"\\newcommand\{\\([A-Za-z]+)\}", (_HERE / "paper" / "numbers.tex").read_text()))
        used = set()
        for name in ("dagapeyeff-exclusions.tex", "abstract.tex"):
            used |= set(re.findall(r"\\([a-z][A-Za-z]+)\{\}", (_HERE / "paper" / name).read_text()))
        self.assertEqual(sorted(used - defined - {"date"}), [])

    def test_no_dash_characters_and_no_reading_claimed(self) -> None:
        for name in ("dagapeyeff-exclusions.tex", "abstract.tex"):
            text = (_HERE / "paper" / name).read_text(encoding="utf-8")
            self.assertNotIn("\u2014", text)
            self.assertNotIn("\u2013", text)
        self.assertIn("No reading of the cells is claimed", (_HERE / "paper" / "dagapeyeff-exclusions.tex").read_text())


if __name__ == "__main__":
    unittest.main()
