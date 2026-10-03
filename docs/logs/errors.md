# Error log

Append-only. One entry per real failure. Fields are **date**, **command**, **failure**, and **retried**.

The classical engine appends a new entry only when `python -m engine demo` fails a known-plaintext recovery (`engine/errors.py`). A green demo does not write here. Do not invent a failure to test the writer; `tests/test_errors.py` writes to a temporary file.

Times are America/New_York.

## Entries

### 2026-10-02 — JPEG stored as text by an MCP upload

- **date:** 2026-10-02 (ET)
- **command:** MCP GitHub file upload of the README hero JPEG (`docs/assets/readme-hero.jpg`). This session did not repeat that upload.
- **failure:** The upload path can store the JPEG as base64 text instead of a binary blob. A text file whose contents are the base64 alphabet is not an image: it does not start with the JPEG magic bytes `FF D8 FF`, and GitHub will not render it. The copy on this machine was checked on 2026-10-02: 53,643 bytes, header `FF D8 FF E0` then `JFIF`. README therefore links `docs/assets/readme-hero.svg`, which is text XML and renders without a binary upload.
- **retried:** No. The MCP upload was not tried again. The SVG is the rendering path. Do not “fix” a broken upload by pasting base64 into a `.jpg` file.

### 2026-10-02 — pip refused to install Pillow

- **date:** 2026-10-02 (ET)
- **command:** `python3 -m pip install --user pillow pytesseract`
- **failure:** Debian’s PEP 668 externally-managed environment blocked the install. `pytesseract` was not installed.
- **retried:** Yes, by a different command, not by `--break-system-packages`. `sudo apt-get install python3-pil` after `sudo dpkg --configure -a` (the first apt attempt had left dpkg interrupted). Pillow 11.1.0 imported. OCR calls the `tesseract` binary (5.5.0) directly and does not need the Python package.

### 2026-10-02 — `python` is not on PATH

- **date:** 2026-10-02 (ET)
- **command:** `python -m engine --help` (as the README writes it)
- **failure:** `python: command not found` on this box. `python3` is `/usr/bin/python3`.
- **retried:** Yes, the same commands with `python3`. Help, the seven recovery tests, and the OCR test were run that way. The README still says `python` because a normal venv provides that name. It is an environment gap, not a solver failure, and the engine did not write this entry itself.
