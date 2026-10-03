"""Tesseract must read a PNG this test draws. Not a scroll test."""

from __future__ import annotations

import shutil
import unittest
from pathlib import Path

from engine.ocr import read_image, render_text_png

PHRASE = "THE HARBOR BELL RANG"


@unittest.skipUnless(shutil.which("tesseract"), "tesseract binary not installed")
class OcrDemoTest(unittest.TestCase):
    def test_generated_line_roundtrip(self) -> None:
        path = Path(__file__).resolve().parent / "_ocr_line.png"
        try:
            render_text_png(PHRASE, path)
            got = read_image(path).replace(" ", "").upper()
            self.assertEqual(got, PHRASE.replace(" ", ""))
        finally:
            path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
