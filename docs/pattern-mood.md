# Pattern-and-mood reader

`engine/pattern_mood.py` looks at a sign stream or a simple drawn sheet and reports visual structure:

- **Repeat rhythm**, the best fraction of marks that show up again one step to the right or below. Empty cells do not count, so a blank page is not "rhythmic" just because the background matches.
- **Symmetry**, the fraction of marks that also sit on the left-right mirror or the top-bottom mirror, whichever axis is stronger.
- **Spacing**, the mean distance from each mark to its nearest neighbor, in cell units.
- **Mood**, a label computed only from those measurements.

| Mood | Rule | What it suggests |
|---|---|---|
| `dense/rhythmic` | rhythm ≥ 0.75 and spacing ≤ 2.5 | tight repeats, neighbors close together |
| `open` | spacing ≥ 8 and symmetry ≤ 0.25 | wide sparse marks, no mirror balance |
| `mixed` | anything else | neither of the above |
| `empty` | no marks | nothing to measure |

A sign stream is the same idea in one row. Space, `.`, `_`, and `-` are gaps. Every other token is only a mark. The tokens are not returned.

## What this is not

This describes **art and pattern**. It is **not a decipherment** of the Voynich manuscript, rongorongo, or any unsolved text. It does not transliterate, decrypt, or output linguistic plaintext. A mood label is not a reading, a language, or a claim that a mark means anything.

The same limits apply if the input happens to look like an unsolved script. The tool still returns rhythm, symmetry, spacing, and a mood. It does not name a plaintext.

## Commands

```bash
python3 -m engine.pattern_mood --tight
python3 -m engine.pattern_mood --sparse
python3 -m engine.pattern_mood --signs 'AB AB  AB'
python3 -m unittest tests.test_pattern_mood -v
```

The unit test draws two synthetic sheets. The tight lattice must score `dense/rhythmic`. The sparse asymmetric sheet must score `open`.

Checked 2026-10-02 (ET). No Voynich, rongorongo, or other unsolved-text reading is produced here.
