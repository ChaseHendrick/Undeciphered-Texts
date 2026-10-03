# Local OCR backends

`engine/ocr.py` reads local images using Tesseract or Apple's Vision framework. `auto` prefers Tesseract on `PATH`, then the optional project-local runtime at `work/ocr-runtime/bin/tesseract`; on macOS it otherwise uses Vision through a small Swift helper. Explicit `tesseract` or `vision` selection never silently switches after an error.

The Vision helper uses `VNRecognizeTextRequest` in accurate mode with English recognition and language correction disabled, so dictionary suggestions do not replace observed cipher words. Apple's [text-recognition tutorial](https://developer.apple.com/documentation/vision/recognizing-text-in-images) and [request reference](https://developer.apple.com/documentation/vision/vnrecognizetextrequest), inspected on 2026-10-03, describe the local API. Apple states that Vision's processing takes place on the user's device. This helper has no network calls and sends no image to an external service.

```bash
python3 -m engine.ocr image.png --backend auto
python3 -m engine.ocr image.png --backend vision --timeout 60
python3 -m engine.ocr image.png --backend tesseract --psm 7
python3 -m engine.ocr --render "THE HARBOR BELL RANG" --out work/ocr-line.png
```

The API preserves the existing `read_image(path, psm=7)` call and adds keyword arguments `backend` and `timeout`. Tesseract's page segmentation mode applies only to Tesseract. `available_backends()` detects local tools without invoking OCR; actual framework or image failures remain errors at execution time.

Vision requires macOS 10.15 or newer, an installed Swift compiler, and the local Vision framework. The helper compiles into a private system temporary directory. Its cache identity includes the helper source, Swift compiler version, operating system, and processor architecture. A bounded file lock and atomic replacement prevent concurrent calls from reading an unfinished executable. Later processes reuse that cached helper. The cache contains the executable and compiler modules, with no image data or recovered text.

The default timeout is 60 seconds. Compiler preparation, cache-lock waits, and OCR execution are bounded. Empty OCR output remains a miss. Compiler failures, native-framework errors, and timeouts propagate through the API; the CLI prints them and exits with status 2. Some execution sandboxes restrict native inference, which can cause a Vision framework error even when compilation succeeds. That error is reported rather than turned into a successful OCR check.

On this desktop on 2026-10-03, the Vision helper compiled successfully but its real inference failed with a native Foundation error under the execution sandbox. A targeted call outside that sandbox timed out after 60 seconds. Vision therefore remains an optional backend whose recognition is unvalidated here.

To enable actual OCR on this desktop, the continuation extracted [Homebrew's official Tesseract 5.5.3 bottle](https://formulae.brew.sh/formula/tesseract) and only its required shared-library packages into `work/ocr-runtime`. Every downloaded bottle matched the SHA-256 in the official formula API. Dynamic-library paths were relocated locally and the modified executables were signed with local ad hoc signatures. The bottle includes English and orientation language data. No Homebrew installation or system-directory change was made. These runtime files stay outside version control, and can be removed by deleting that project-local directory. They are specific to this Mac's architecture and operating system.

The real PNG integration passed with this project-local Tesseract under the normal execution sandbox, with no OCR skip. That demonstrates recovery of the constructed phrase, not recognition quality on arbitrary manuscript images.

`render_text_png` requires Pillow and automatically selects an installed DejaVu, Arial, or Helvetica font on Linux or macOS. An explicit `font_path` remains supported. Tesseract remains the portable option on other platforms.

```bash
python3 -m unittest tests.test_ocr -v
```

The integration test draws a real PNG containing `THE HARBOR BELL RANG` and requires the selected OCR backend to read those letters. It skips only when neither backend's tools are detected. A detected backend that fails inference makes the test fail. Separate tests cover automatic and explicit selection, subprocess timeouts, compilation errors, and empty output. The existing phrase certificate still checks the constructed fixture's SHA-256; it does not certify recognition of arbitrary images.

This is ordinary page OCR. It does not detect hidden ink, unwrap a scroll, or interpret an undeciphered script. The Python module itself performs no installation or model download; it detects available local backends.
