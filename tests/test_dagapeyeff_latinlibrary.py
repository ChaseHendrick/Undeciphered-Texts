"""Every window of the fetched Latin Library pages against the cells' letter counts."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from engine.dagapeyeff_latinlibrary import _links, letters

_FROZEN = Path(__file__).resolve().parents[1] / "engine" / "data" / "swarm_cache" / "dagapeyeff-latinlibrary.json"


class DagapeyeffLatinLibraryTest(unittest.TestCase):
    def test_pages_are_read_as_latin_and_links_stay_on_the_site(self) -> None:
        page = "<html><head><title>x</title></head><body><p>Gallia est omnis divisa in partes tres, quarum unam incolunt Belgae</p><p>The notes are in English and of the editor</p></body></html>"
        self.assertEqual(letters(page), "GALLIAESTOMNISDIVISAINPARTESTRESQUARUMUNAMINCOLUNTBELGAE")
        links = _links("https://www.thelatinlibrary.com/caesar/", '<a href="gallic/gall1.shtml">I</a><a href="/ll1/x.html">c</a><a href="https://example.org/">e</a><a href="/cicero">C</a>')
        self.assertEqual(links, ["https://www.thelatinlibrary.com/caesar/gallic/gall1.shtml", "https://www.thelatinlibrary.com/cicero/"])

    def test_no_window_is_a_clean_source(self) -> None:
        report = json.loads(_FROZEN.read_text(encoding="utf-8"))
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertGreater(report["letters"], 50_000_000)
        self.assertEqual(report["fewest_errors"], 3)
        self.assertEqual(report["within_2"], 0)
        for item in report["closest"]:
            self.assertEqual(set(item), {"page", "offset", "errors"})


if __name__ == "__main__":
    unittest.main()
