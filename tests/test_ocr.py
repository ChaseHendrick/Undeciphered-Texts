"""Tesseract must read a PNG this test draws. Not a scroll test."""

from __future__ import annotations

import shutil
import unittest
import hashlib
import json
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



OCR_CERT_PATH = Path(__file__).resolve().parents[1] / "engine" / "data" / "ocr_certificate.json"


class OcrCertificateTest(unittest.TestCase):
    """Certificate checks the synthetic OCR phrase, not an unknown script."""

    def test_certificate_matches_known_text_hash(self) -> None:
        cert = json.loads(OCR_CERT_PATH.read_text(encoding="utf-8"))
        self.assertEqual(cert["tool_name"], "ocr")
        known = cert["known_text"]
        digest = hashlib.sha256(known.encode("utf-8")).hexdigest()
        self.assertEqual(digest, cert["known_text_sha256"])
        self.assertEqual(known, cert["input"].replace(" ", ""))
        self.assertIn("not an unknown script", cert["note"].lower())


if __name__ == "__main__":
    unittest.main()
