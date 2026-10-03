# Synthetic glyph reader

`glyph_reader.py` draws a sheet of simple marks, splits the ink into connected components, and compares each component to a small inventory defined in that file.

It does **not** decipher Linear A, the Indus script, or Teotihuacan signs. Those writing systems are not in the inventory. A match is the nearest synthetic template (`bar`, `stem`, `corner`, `cross`, `ring`, `peak`), not a phonetic value, a word, or a catalog number from a real sign list.

## What it does

1. **Draw.** If Pillow is installed, each inventory id is painted with `ImageDraw` into its own cell on a white canvas. Cells are separated so marks do not touch. The same id uses the same drawer, so repeats are the same mark.
2. **Segment.** Pixels darker than the midpoint are ink. Eight-connected components smaller than a few pixels are dropped. What remains is one glyph.
3. **Describe.** Each glyph records a bounding box `(x, y, width, height)` and an ink-pixel count. A 16×16 occupancy grid, normalized to that box, is the template key.
4. **Match.** The grid is compared to one isolated drawing of every inventory sign. The label is the minimum Hamming distance. Distance `0` means the planted mark and the template occupied the same cells.

Reading order is rows by vertical center, then left to right inside a row.

## What it does not do

- It does not decipher Linear A.
- It does not decipher the Indus script.
- It does not decipher Teotihuacan signs, murals, or any Mesoamerican catalog.
- It does not assign sound values, language, or plaintext.
- It does not read a photograph of a real inscription. The only sheet it knows how to build is the one it draws.
- It does not replace `engine/ocr.py` (Latin letters via Tesseract) or `engine/mural_analyzer.py` (flat color regions).

## Commands

```bash
python3 -m glyph_reader
python3 -m unittest tests.test_glyph_reader -v
```

The unit test plants a sheet that repeats several inventory ids and requires those labels back, in order, with a bounding box and an ink count on every glyph. That is a check that segmentation and template matching agree with the drawing code. It is not evidence about an undeciphered script.

Pillow is imported when the sheet is drawn (`PIL.Image`, `PIL.ImageDraw`). Without Pillow the renderer raises `RuntimeError` and does not guess labels.
