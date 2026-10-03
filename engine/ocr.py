"""Read a local image with Tesseract or macOS Apple Vision.

Automatic selection prefers system or project-local Tesseract and falls back
to Apple's local Vision when a Swift compiler is available. Image data stays
on this computer. This is page OCR, not ink detection, virtual unwrapping, or
an interpretation of an undeciphered script. Drawing a demo requires Pillow.
"""

from __future__ import annotations

import argparse
import hashlib
import math
import os
import platform
import shutil
import stat
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

DEFAULT_FONT = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
FONT_CANDIDATES = (
    DEFAULT_FONT,
    Path("/System/Library/Fonts/Supplemental/Arial.ttf"),
    Path("/System/Library/Fonts/Helvetica.ttc"),
    Path("/Library/Fonts/Arial.ttf"),
)
_VISION_SOURCE = Path(__file__).resolve().parent / "data" / "vision_ocr.swift"
_PORTABLE_TESSERACT = Path(__file__).resolve().parent.parent / "work" / "ocr-runtime" / "bin" / "tesseract"


def tesseract_bin() -> str:
    """Prefer PATH, then the optional reversible runtime in project work/."""
    found = shutil.which("tesseract")
    if found:
        return found
    if _PORTABLE_TESSERACT.is_file() and os.access(_PORTABLE_TESSERACT, os.X_OK):
        return str(_PORTABLE_TESSERACT)
    raise FileNotFoundError("Tesseract is not on PATH and no project-local runtime is installed.")


def vision_compiler() -> str:
    """Find a local compiler; actual framework availability is checked at compile."""
    if sys.platform != "darwin":
        raise FileNotFoundError("Apple Vision OCR requires macOS and a Swift compiler.")
    developer_compiler = Path("/Library/Developer/CommandLineTools/usr/bin/swiftc")
    if developer_compiler.is_file():
        return str(developer_compiler)
    found = shutil.which("swiftc")
    if not found:
        raise FileNotFoundError("Apple Vision OCR requires an installed Swift compiler.")
    return found


def available_backends() -> tuple[str, ...]:
    """Return locally detected backend tools, without compiling or running OCR."""
    found = []
    try:
        tesseract_bin()
    except FileNotFoundError:
        pass
    else:
        found.append("tesseract")
    try:
        vision_compiler()
    except FileNotFoundError:
        pass
    else:
        found.append("vision")
    return tuple(found)


def resolve_backend(backend: str = "auto") -> str:
    if backend not in ("auto", "tesseract", "vision"):
        raise ValueError("backend must be auto, tesseract, or vision")
    if backend == "tesseract":
        tesseract_bin()
        return backend
    if backend == "vision":
        vision_compiler()
        return backend
    detected = available_backends()
    if detected:
        return detected[0]
    raise FileNotFoundError(
        "No local OCR backend is available. Tesseract needs its binary on PATH; "
        "Apple Vision needs macOS and an installed Swift compiler."
    )


def _run(command: list[str], timeout: float, operation: str) -> subprocess.CompletedProcess:
    try:
        process = subprocess.run(command, check=False, capture_output=True, text=True,
                                 timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"{operation} timed out after {timeout:g} seconds") from exc
    if process.returncode != 0:
        error = (process.stderr or "").strip() or f"exit {process.returncode}"
        raise RuntimeError(f"{operation} failed: {error}")
    return process


@dataclass
class _VisionRuntime:
    binary: Path
    directory: Path


@lru_cache(maxsize=1)
def _swift_version(compiler: str, timeout: float) -> str:
    process = _run([compiler, "--version"], timeout, "Swift compiler version check")
    return process.stdout + process.stderr


def _private_cache_root() -> Path:
    root = Path(tempfile.gettempdir()) / f"undeciphered-vision-ocr-{os.getuid()}"
    root.mkdir(mode=0o700, exist_ok=True)
    metadata = root.lstat()
    if (not stat.S_ISDIR(metadata.st_mode) or metadata.st_uid != os.getuid()
            or stat.S_IMODE(metadata.st_mode) & 0o077):
        raise RuntimeError("Apple Vision helper cache must be a private owned directory")
    return root


@lru_cache(maxsize=1)
def _vision_runtime(timeout: float) -> _VisionRuntime:
    """Reuse an atomic helper cache keyed by source, Swift version, and host.

Only the helper and compiler modules live in a private system-temp cache.
No image data, project binaries, or installed packages are written there.
    """
    import fcntl

    deadline = time.monotonic() + timeout
    compiler = vision_compiler()
    if not _VISION_SOURCE.is_file():
        raise FileNotFoundError(f"Apple Vision OCR helper source is missing: {_VISION_SOURCE}")
    version = _swift_version(compiler, timeout)
    identity = "\0".join((compiler, version, sys.platform, platform.machine(), platform.release()))
    digest = hashlib.sha256(_VISION_SOURCE.read_bytes() + identity.encode()).hexdigest()
    directory = _private_cache_root() / digest
    directory.mkdir(mode=0o700, exist_ok=True)
    binary = directory / "vision-ocr"
    with (directory / "compile.lock").open("a+b") as lock:
        while True:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if time.monotonic() >= deadline:
                    raise RuntimeError("Apple Vision helper cache lock timed out")
                time.sleep(0.05)
        if not binary.is_file():
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise RuntimeError("Apple Vision helper preparation timed out")
            descriptor, output = tempfile.mkstemp(prefix="compile-", dir=directory)
            os.close(descriptor)
            temporary = Path(output)
            try:
                _run([compiler, str(_VISION_SOURCE), "-o", str(temporary), "-module-cache-path",
                      str(directory / "module-cache")], remaining,
                     "Apple Vision helper compilation")
                temporary.chmod(0o700)
                temporary.replace(binary)
            finally:
                temporary.unlink(missing_ok=True)
    return _VisionRuntime(binary, directory)


def _font_path(explicit: Path | None) -> Path:
    candidates = (Path(explicit),) if explicit is not None else FONT_CANDIDATES
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    if explicit is not None:
        raise FileNotFoundError(f"font not found: {explicit}")
    raise FileNotFoundError("No supported demo font found. Pass an explicit font_path.")


def render_text_png(text: str, path: Path, font_path: Path | None = None) -> Path:
    """Draw supplied text in black on white using a Linux or macOS font."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError as exc:
        raise RuntimeError(
            "Pillow is not installed, so this demo cannot draw a text image. "
            "read_image() can still read an existing image."
        ) from exc
    font = ImageFont.truetype(str(_font_path(font_path)), 48)
    probe = Image.new("RGB", (8, 8), "white")
    draw = ImageDraw.Draw(probe)
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    image = Image.new("RGB", (max(32, right - left + 80), max(32, bottom - top + 80)), "white")
    ImageDraw.Draw(image).text((40 - left, 40 - top), text, fill="black", font=font)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, format="PNG")
    return path


def read_image(
    path: Path,
    psm: int = 7,
    *,
    backend: str = "auto",
    timeout: float = 60,
) -> str:
    """Return local OCR text. Empty output is a miss, not a decipherment.

The timeout bounds each subprocess: initial Vision compilation if needed,
and the OCR call. Tesseract's page segmentation mode applies only to that
backend. Explicit backend selection never silently switches after an error.
    """
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(path)
    if (not isinstance(timeout, (int, float)) or isinstance(timeout, bool)
            or not math.isfinite(timeout) or timeout <= 0):
        raise ValueError("timeout must be a positive finite number of seconds")
    if not isinstance(psm, int) or isinstance(psm, bool) or not 0 <= psm <= 13:
        raise ValueError("psm must be an integer from 0 through 13")
    chosen = resolve_backend(backend)
    if chosen == "tesseract":
        command = [tesseract_bin(), str(path.resolve()), "stdout", "--psm", str(psm), "-l", "eng"]
    else:
        runtime = _vision_runtime(timeout)
        command = [str(runtime.binary), str(path.resolve())]
    return _run(command, timeout, f"{chosen} OCR").stdout.strip()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m engine.ocr",
        description="OCR a local image with Tesseract or Apple Vision. Not a scroll reader.",
    )
    parser.add_argument("image", nargs="?", help="local image path")
    parser.add_argument("--render", metavar="TEXT", help="draw TEXT to a PNG, then OCR it")
    parser.add_argument("--out", default="docs/assets/ocr-demo.png")
    parser.add_argument("--backend", choices=("auto", "tesseract", "vision"), default="auto")
    parser.add_argument("--psm", type=int, default=7, help="Tesseract page segmentation mode")
    parser.add_argument("--timeout", type=float, default=60, help="timeout for each local subprocess")
    args = parser.parse_args(argv)
    try:
        if args.render:
            image = render_text_png(args.render, Path(args.out))
            print(f"wrote {image.resolve()}")
        elif args.image:
            image = Path(args.image)
        else:
            parser.error("give an image path or --render TEXT")
        text = read_image(image, backend=args.backend, psm=args.psm, timeout=args.timeout)
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"ocr failed: {exc}", file=sys.stderr)
        return 2
    if not text:
        print("ocr returned no text", file=sys.stderr)
        return 3
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
