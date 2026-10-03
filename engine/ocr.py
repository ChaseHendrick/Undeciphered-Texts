"""Read a Latin-letter image with the system Tesseract binary.

This is page OCR of a picture of text. It is not ink detection, not virtual
unwrapping, and not a reading of a Herculaneum scroll or an undeciphered script.
Rendering uses Pillow when it is installed. The classical solvers do not import
this module.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

DEFAULT_FONT = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")


def tesseract_bin() -> str:
    found = shutil.which("tesseract")
    if not found:
        raise FileNotFoundError(
            "tesseract is not on PATH. Install the tesseract-ocr package. "
            "This module does not download weights and does not call a vision API."
        )
    return found


def render_text_png(text: str, path: Path, font_path: Path = DEFAULT_FONT) -> Path:
    """Draw `text` in black on white. Refuses to invent glyphs for a photo."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError as exc:
        raise RuntimeError(
            "Pillow is not installed, so this demo cannot draw a text image. "
            "The OCR interface can still read an existing PNG via read_image()."
        ) from exc
    if not font_path.is_file():
        raise FileNotFoundError(f"font not found: {font_path}")
    font = ImageFont.truetype(str(font_path), 48)
    probe = Image.new("RGB", (8, 8), "white")
    draw = ImageDraw.Draw(probe)
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    width = max(32, right - left + 80)
    height = max(32, bottom - top + 80)
    image = Image.new("RGB", (width, height), "white")
    ImageDraw.Draw(image).text((40, 30), text, fill="black", font=font)
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, format="PNG")
    return path


def read_image(path: Path, psm: int = 7) -> str:
    """Return Tesseract stdout. Empty stdout is a miss, not a decipherment."""
    if not path.is_file():
        raise FileNotFoundError(path)
    proc = subprocess.run(
        [tesseract_bin(), str(path), "stdout", "--psm", str(psm), "-l", "eng"],
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        err = (proc.stderr or "").strip() or f"tesseract exit {proc.returncode}"
        raise RuntimeError(err)
    return proc.stdout.strip()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m engine.ocr",
        description="OCR one Latin-letter image with Tesseract. Not a scroll reader.",
    )
    parser.add_argument("image", nargs="?", help="PNG or other image Tesseract can open")
    parser.add_argument("--render", metavar="TEXT", help="draw TEXT to a PNG, then OCR it")
    parser.add_argument("--out", default="docs/assets/ocr-demo.png")
    args = parser.parse_args(argv)
    if args.render:
        image = render_text_png(args.render, Path(args.out))
        print(f"wrote {image.resolve()}")
        text = read_image(image)
    elif args.image:
        text = read_image(Path(args.image))
    else:
        parser.error("give an image path or --render TEXT")
    if not text:
        print("ocr returned no text", file=sys.stderr)
        return 3
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
