# Stroke geometry

This page describes `engine/stroke_geometry.py`. The module measures pixels in a picture of ink.

It answers three narrow questions:

1. Are the strokes separated (`print`) or joined (`cursive`)?
2. Do the strokes lean right (`/` ), left (`\`), or upright?
3. Do two drawings share a letter shape?

That is stroke geometry. It is not a claim about a real person's handwriting. It is not a forensic identification of a writer. It is not a reading of an ancient manuscript. The pictures the unit tests draw are synthetic Pillow strokes on a white canvas, not photographs of anyone's hand and not a page from a manuscript.

## What the labels mean

| Label | Meaning | What it is not |
|---|---|---|
| `print` | Wide empty columns sit inside the ink span, or several separate components | A judgment that a person "prints" |
| `cursive` | One joined component and no wide pen-lift | A judgment that a person writes cursive |
| `right` | Per-stroke `dx/dy` is negative (image y grows downward), a lean like `/` | Right-handedness |
| `left` | Per-stroke `dx/dy` is positive, a lean like `\` | Left-handedness |
| `same_shape` | Occupancy grids of two drawings are close after crop, dilation, and resample | The same person twice |

`identifies_person` is always false. `left_handed` is always false. Slant is ink lean, not handedness.

## Flip and thin paper

`flip_horizontal` mirrors the picture left to right. A right lean becomes a left lean.

`thin_paper_reverse` is that same mirror. It stands for looking at ink through the back of a thin sheet. The lean reverses because the sheet is turned over, not because a different hand wrote it. A left lean on that reverse view is still not evidence that someone is left-handed, and it is not an identification of a person.

## Letter shapes

`letters_same_shape` compares two drawings. The tests draw the same letter twice (different stroke width and a small shift) and require a match, then draw different letters and require a mismatch. Matching letters are still not a forensic identification of a person. The disclaimer on `LetterMatch` says so.

## How to run

```bash
python3 -m unittest tests.test_stroke_geometry -v
```

Pillow is used only to draw the synthetic fixtures inside the test. The classical solvers do not import this module. Do not point it at a manuscript scan and treat the labels as a decipherment or as a writer.
