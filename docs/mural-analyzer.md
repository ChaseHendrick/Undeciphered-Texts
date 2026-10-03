# Mural / painting analyzer (synthetic structure only)

`engine/mural_analyzer.py` measures flat RGB structure on a raster:

- **Dominant colors**, quantized RGB histogram
- **Connected regions**, 4-connected same-color components
- **Motif repeat**, whether two or more same-color regions share a shape signature

## What it does not do

**It does not read Teotihuacan glyphs or any ancient painting.** It does not OCR, decipher, transliterate, or claim a glyph reading. It is not a Mesoamerican epigraphy tool. Feed it a photo of an ancient mural and you still only get color buckets and blobs, not names, sounds, or meanings.

## Technique note (GENChase)

Connected-region labeling uses the classical one-pass union-find idea from site percolation (Hoshen-Kopelman). That family of cluster labeling is discussed on the percolation plate in [ChaseHendrick/GENChase](https://github.com/ChaseHendrick/GENChase). The Python here is a fresh implementation for RGB grids; no GENChase studio JavaScript is vendored.

## Dependencies

- Analysis: Python standard library only
- Optional: Pillow (`PIL`) to load or save PNG/JPEG files

## Commands

```bash
python3 -m engine.mural_analyzer --synthetic
python3 -m unittest tests.test_mural_analyzer -v
```

`--write-synthetic PATH` can emit a demo PNG. Do not point it at `docs/assets/readme-hero.jpg`.

Checked 2026-10-02 (ET). No ancient mural transcription is produced here.
