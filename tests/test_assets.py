"""README hero bytes. A base64-as-text JPEG fails this."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JPEG = ROOT / "docs" / "assets" / "readme-hero.jpg"
SVG = ROOT / "docs" / "assets" / "readme-hero.svg"
README = ROOT / "README.md"


class HeroAssetTest(unittest.TestCase):
    def test_jpeg_magic(self) -> None:
        blob = JPEG.read_bytes()
        self.assertTrue(blob.startswith(bytes.fromhex("ffd8ff")), blob[:16])
        self.assertGreater(len(blob), 1000)
        # base64 text of a JPEG starts with an ASCII character, not 0xFF
        self.assertFalse(blob[:4].isascii())

    def test_svg_is_svg_and_readme_links_it(self) -> None:
        text = SVG.read_text(encoding="utf-8")
        self.assertTrue(text.lstrip().startswith("<svg"))
        readme = README.read_text(encoding="utf-8")
        self.assertIn("docs/assets/readme-hero.svg", readme)


if __name__ == "__main__":
    unittest.main()
