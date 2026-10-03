# Image reading: OCR, ink detection, and virtual unwrapping

Three different jobs get called “reading an image.” This repository does only the first, and only for a clean picture of Latin letters. It does not read Herculaneum scrolls, and it does not copy Chase Hendrick’s Blackletter desk.

Checked 2026-10-02 (ET). No scroll transcription is produced here.

## The three jobs

| Job | Input | What “a letter” is | This repo |
|---|---|---|---|
| **Page OCR** | A photograph or rendering of an alphabet you already know | A glyph in a trained Latin (or other) model | Optional. `engine/ocr.py` calls the `tesseract` binary |
| **Ink detection** | A CT slice or a surface rendering where carbon ink barely differs from carbonized papyrus | A pixel labeled ink or not. The model is not trained on character identity | Not implemented. See [vesuvius-scrolls.md](vesuvius-scrolls.md) |
| **Virtual unwrapping** | A 3D volume of a crushed roll | A sheet surface, flattened. Still not a transcription | Not implemented. Geometry, then ink, then a papyrologist |

OCR on a heatmap of PHerc. 1667 is the wrong tool. The 2026 preprint says the ink models are visibility amplifiers: they are not trained on character identities, words, transcriptions, OCR targets, or lexical labels. Eight papyrologists transcribed PHerc. 1667. Source: [arXiv:2606.29085](https://arxiv.org/html/2606.29085v1), announcement [scrollprize.org/firstscroll](https://scrollprize.org/firstscroll).

## What is already possible, and what is not

Possible, and shipped as a small demo:

- Draw a known English line with Pillow (DejaVu Sans, black on white) and read it back with Tesseract 5.5.0, LSTM, English, page-segmentation mode 7 (a single line).
- Read an existing PNG you already have, if Tesseract can open it.

Not possible with this module:

- Carbon ink in a CT volume. Tesseract never sees the volume.
- Greek papyri, Iberian, Meroitic, or any undeciphered script. The English model will emit Latin letters anyway. That string is a forced fit, the same failure mode as running the substitution solver on Voynich.
- A “reading” when stdout is empty. Empty is a miss (`exit 3`), not a supplement.
- Blackletter’s screenshot path. That program is a private Canvas desk, not a cipher engine. See below. Nothing from it is vendored.

Libraries, in the order to try them:

1. **Tesseract** (`tesseract` on `PATH`, package `tesseract-ocr`). This is what the demo uses. No weights are downloaded at runtime. Version on the box that built the test: 5.5.0, Leptonica 1.84.1.
2. **Pillow** (`python3-pil`), only to *draw* the demo image. `pip install pillow` failed on this machine (PEP 668). `apt install python3-pil` worked. See [logs/errors.md](logs/errors.md).
3. **pytesseract** was not installed. The module shells out to the binary so the classical engine stays free of that dependency.
4. **EasyOCR** was not installed. It needs a neural net and a GPU-or-CPU weight download. Do not add it in order to “read” a scroll.

If `tesseract` is absent, `read_image` raises `FileNotFoundError` with that fact. It does not fall back to a language model and pretend the fallback is OCR.

## Commands

```bash
python3 -m engine.ocr --render "THE HARBOR BELL RANG" --out docs/assets/ocr-demo.png
python3 scripts/ocr_demo.py
python3 -m unittest tests.test_ocr -v
```

`--render` draws the phrase and prints Tesseract’s text. `scripts/ocr_demo.py` exits 3 if the letters do not match. The PNG is a generated witness, not an artifact from a manuscript.

## What Blackletter actually does (inspiration only)

Repository: private `ChaseHendrick/blackletter`, default branch `main`, tree `57dbabef11e5c16db075ae734a7ed5affd667973` (read 2026-10-02 via the GitHub API). `BLACKLETTER.md` describes a personal Canvas desk. It is not a historical-cipher project. Do not copy the injector, the course packs, or the auto-apply path into this repo. Those are out of scope here, and this file does not reproduce them.

The screen-reading order in `inject-src/03-net.js`, as of that tree, is worth stealing as a *policy*, not as code:

1. **Text you can already see comes first.** The page’s own text (`innerText` of the question region, whitespace collapsed, length-capped) is the primary transcript. OCR is a failsafe when that text is missing, short, or the frame is not readable.
2. **Raster only a region.** An existing `img` or `canvas` is drawn to an offscreen canvas, longest side capped at 1280, and encoded as JPEG. A full-tab screenshot is cropped with `getBoundingClientRect` times `devicePixelRatio` before the same cap. Cropping is the part that makes OCR less wrong. A full desktop is not a line of type.
3. **Do not OCR text you already hold.** One function paints a string the page already extracted onto a white canvas (18px sans-serif, wrapped) and sends that JPEG on. That is a transport picture of known text. It is not evidence that a photograph was read. This repository’s demo is the same kind of object, and it is labeled as one.
4. **The “reader” of a hard screenshot is not Tesseract.** The desk posts the transcript and the JPEG to its own solve endpoint. There is no `tesseract` dependency in `package.json`. A vision-model guess is not a diplomatic transcription, and it is not reused here.
5. **Empty or tiny images are dropped.** The raster helper returns nothing when the data URL is under a few thousand characters or the rectangle is under about 120 by 60. Silence beats a hallucinated line.

What to reuse, and it is small: prefer a transcription you already have; crop to the line; cap the longest side; treat empty OCR as failure; never send a generated picture of known text to a model and call the model’s reply a new reading. What not to reuse: anything that clicks, fills, or answers a page.

## How this differs from the Vesuvius pipeline

PHerc. 1667 (Scroll 4), preprint June 2026:

- Scan: ESRF BM18, 2.4 µm voxels, about 78 keV, 22 cm propagation. A reconstructed volume is on the order of 20 TB before the compressed release. Tesseract cannot open that.
- Surface: a quad mesh in the CT volume, then a flattened image. “Complete unwrapping” means the preserved surface is meshed, not that the lost outer layers came back. The roll is about 8 cm of an original height of 19–24 cm. Diameter was reduced from 4.9 cm to 2 cm by mechanical attempts (nineteenth century, Fackelmann in November 1969, Oslo method in the 1980s). Weight went from 14 g to about 6 g. The title, if it sat in the lost upper part, is gone.
- Reading: 22 columns or column-equivalents, about 860 cm² of preserved writing surface, 31 wraps and 1231 cm² of papyrus surface in the unwrapping statistic. Untranscribed on purpose: the surviving bits of the first three columns, 33 cm², where the ink is too fragmentary. Square brackets are restored letters, not recovered ones. Underdots are uncertain letters.
- Still unread besides that core: the destroyed outer and upper papyrus; PHerc. Paris 4 as a book (the 2026 scan confirms the 2023 grand-prize region in 3D ink, it does not publish a full edition); PHerc. 139 beyond the title *On Gods* book 8 and a handful of phrases; PHerc. 172 beyond its title and a partial unwrap; hundreds of unscanned Naples rolls. Two bottlenecks the preprint names: crushed geometry, and ink that the scan does not show.

Details and URLs: [vesuvius-scrolls.md](vesuvius-scrolls.md).

## Limits to put on any future adapter

- A Latin OCR string is not a decipherment of the image’s script.
- Do not train or prompt a model on “what the scroll should say.”
- Do not commit a PNG of a real manuscript unless the rights are clear. The demo PNG is generated.
- Keep OCR out of `engine/solvers/`. A cipher solver that calls Tesseract will hide a bad attack behind a bad transcript.
