#!/usr/bin/env python3
"""Draw a known English line and OCR it. Not a Herculaneum reader."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.ocr import read_image, render_text_png

PHRASE = "THE HARBOR BELL RANG"


def main() -> int:
    image = ROOT / "docs" / "assets" / "ocr-demo.png"
    render_text_png(PHRASE, image)
    text = read_image(image)
    print(text)
    print(f"image {image}")
    return 0 if text.replace(" ", "").upper() == PHRASE.replace(" ", "") else 3


if __name__ == "__main__":
    raise SystemExit(main())
