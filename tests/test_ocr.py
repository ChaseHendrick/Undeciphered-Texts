"""Actual image OCR plus deterministic backend selection and error controls.

The integration draws a PNG and reads it using Tesseract or Apple Vision.
This is page OCR, not a test of an undeciphered script or a scroll.
"""

from __future__ import annotations

import contextlib
import hashlib
import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from engine.ocr import (
    available_backends,
    main,
    read_image,
    render_text_png,
    resolve_backend,
)

PHRASE = "THE HARBOR BELL RANG"
OCR_CERT_PATH = Path(__file__).resolve().parents[1] / "engine/data/ocr_certificate.json"


class OcrBackendTest(unittest.TestCase):
    def test_auto_prefers_tesseract_then_vision(self):
        with patch("engine.ocr.shutil.which", return_value="/tools/tesseract"):
            self.assertEqual(resolve_backend("auto"), "tesseract")
        with patch("engine.ocr.tesseract_bin", side_effect=FileNotFoundError("no Tesseract")), \
             patch("engine.ocr.vision_compiler", return_value="/tools/swiftc"):
            self.assertEqual(resolve_backend("auto"), "vision")
        with patch("engine.ocr.tesseract_bin", side_effect=FileNotFoundError("no Tesseract")), \
             patch("engine.ocr.vision_compiler", side_effect=FileNotFoundError("no Swift")):
            self.assertEqual(available_backends(), ())
            with self.assertRaisesRegex(FileNotFoundError, "Tesseract.*Vision"):
                resolve_backend("auto")

    def test_explicit_missing_backend_does_not_silently_switch(self):
        with patch("engine.ocr.tesseract_bin", side_effect=FileNotFoundError("no Tesseract")):
            with self.assertRaises(FileNotFoundError):
                resolve_backend("tesseract")
        with patch("engine.ocr.vision_compiler", side_effect=FileNotFoundError("no Swift")):
            with self.assertRaisesRegex(FileNotFoundError, "no Swift"):
                resolve_backend("vision")
        with self.assertRaises(ValueError):
            resolve_backend("cloud")

    def test_project_local_tesseract_is_detected_without_changing_path(self):
        from engine.ocr import tesseract_bin

        with tempfile.TemporaryDirectory() as directory:
            wrapper = Path(directory) / "tesseract"
            wrapper.write_text("#!/bin/sh\nexit 0\n")
            wrapper.chmod(0o700)
            with patch("engine.ocr.shutil.which", return_value=None), \
                 patch("engine.ocr._PORTABLE_TESSERACT", wrapper):
                self.assertEqual(tesseract_bin(), str(wrapper))
                self.assertEqual(resolve_backend("auto"), "tesseract")
            wrapper.chmod(0o600)
            with patch("engine.ocr.shutil.which", return_value=None), \
                 patch("engine.ocr._PORTABLE_TESSERACT", wrapper):
                with self.assertRaises(FileNotFoundError):
                    tesseract_bin()

    def test_tesseract_stdout_parameters_timeout_and_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            image = Path(directory) / "image.png"
            image.touch()
            with patch("engine.ocr.tesseract_bin", return_value="/tools/tesseract"), \
                 patch("engine.ocr.subprocess.run") as run:
                run.return_value = subprocess.CompletedProcess([], 0, "  READ TEXT\n", "")
                self.assertEqual(read_image(image, psm=6, backend="tesseract", timeout=3), "READ TEXT")
                command = run.call_args.args[0]
                self.assertIn(str(image.resolve()), command)
                self.assertEqual(command[-4:], ["--psm", "6", "-l", "eng"])
                self.assertEqual(run.call_args.kwargs["timeout"], 3)
                run.side_effect = subprocess.TimeoutExpired(command, 3)
                with self.assertRaisesRegex(RuntimeError, "timed out"):
                    read_image(image, backend="tesseract", timeout=3)
                run.side_effect = None
                run.return_value = subprocess.CompletedProcess([], 1, "", "broken image")
                with self.assertRaisesRegex(RuntimeError, "broken image"):
                    read_image(image, backend="tesseract")

    def test_vision_stdout_uses_local_helper_and_bounded_process(self):
        with tempfile.TemporaryDirectory() as directory:
            image = Path(directory) / "image.png"
            image.touch()
            runtime = SimpleNamespace(binary=Path(directory) / "vision-ocr")
            with patch("engine.ocr.vision_compiler", return_value="/tools/swiftc"), \
                 patch("engine.ocr._vision_runtime", return_value=runtime), \
                 patch("engine.ocr.subprocess.run") as run:
                run.return_value = subprocess.CompletedProcess([], 0, "READ TEXT\n", "")
                self.assertEqual(read_image(image, backend="vision", timeout=4), "READ TEXT")
                self.assertEqual(run.call_args.args[0], [str(runtime.binary), str(image.resolve())])
                self.assertEqual(run.call_args.kwargs["timeout"], 4)

    def test_vision_compile_errors_and_timeouts_are_explicit_and_not_cached(self):
        from engine.ocr import _vision_runtime

        _vision_runtime.cache_clear()
        with tempfile.TemporaryDirectory() as directory, \
             patch("engine.ocr.tempfile.gettempdir", return_value=directory), \
             patch("engine.ocr.vision_compiler", return_value="/tools/swiftc"), \
             patch("engine.ocr._swift_version", return_value="test Swift version"), \
             patch("engine.ocr.subprocess.run") as run:
            run.return_value = subprocess.CompletedProcess([], 1, "", "missing Vision framework")
            with self.assertRaisesRegex(RuntimeError, "compilation failed.*missing Vision"):
                _vision_runtime(2)
            self.assertEqual(_vision_runtime.cache_info().currsize, 0)
            self.assertGreater(run.call_args.kwargs["timeout"], 0)
            self.assertLessEqual(run.call_args.kwargs["timeout"], 2)
            self.assertIn("-module-cache-path", run.call_args.args[0])
            run.side_effect = subprocess.TimeoutExpired([], 2)
            with self.assertRaisesRegex(RuntimeError, "compilation timed out"):
                _vision_runtime(2)
            self.assertEqual(_vision_runtime.cache_info().currsize, 0)

    def test_invalid_image_and_timeout_inputs_are_rejected(self):
        with self.assertRaises(FileNotFoundError):
            read_image(Path("missing-image-file.png"))
        with tempfile.TemporaryDirectory() as directory:
            image = Path(directory) / "image.png"
            image.touch()
            for timeout in (0, -1, True, float("inf"), float("nan")):
                with self.subTest(timeout=timeout), self.assertRaises(ValueError):
                    read_image(image, timeout=timeout)
            for psm in (-1, 14, True, 1.5):
                with self.subTest(psm=psm), self.assertRaises(ValueError):
                    read_image(image, psm=psm)

    def test_cli_forwards_explicit_backend_and_empty_text_is_a_miss(self):
        with patch("engine.ocr.read_image", return_value="TEXT") as read, \
             contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(main(["image.png", "--backend", "vision", "--timeout", "8"]), 0)
            self.assertEqual(read.call_args.kwargs["backend"], "vision")
            self.assertEqual(read.call_args.kwargs["timeout"], 8)
        with patch("engine.ocr.read_image", return_value=""), \
             contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main(["image.png"]), 3)


@unittest.skipUnless(available_backends(), "neither Tesseract nor macOS Vision compiler is available")
class OcrDemoTest(unittest.TestCase):
    def test_generated_line_roundtrip(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ocr-line.png"
            render_text_png(PHRASE, path)
            self.assertTrue(path.read_bytes().startswith(bytes.fromhex("89504e47")))
            got = read_image(path, backend="auto", timeout=60).replace(" ", "").upper()
            self.assertEqual(got, PHRASE.replace(" ", ""))


class OcrCertificateTest(unittest.TestCase):
    def test_certificate_matches_known_text_hash(self):
        cert = json.loads(OCR_CERT_PATH.read_text(encoding="utf-8"))
        self.assertEqual(cert["tool_name"], "ocr")
        known = cert["known_text"]
        self.assertEqual(hashlib.sha256(known.encode("utf-8")).hexdigest(), cert["known_text_sha256"])
        self.assertEqual(known, cert["input"].replace(" ", ""))
        self.assertIn("not an unknown script", cert["note"].lower())


if __name__ == "__main__":
    unittest.main()
