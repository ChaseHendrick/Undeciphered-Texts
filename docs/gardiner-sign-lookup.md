# Gardiner sign lookup (known-sign table)

Egyptian hieroglyphs are a **known, deciphered script**. This module does
**not** claim a new decipherment. It looks up a tiny Gardiner-code subset
and returns the Unicode character plus a short gloss from the cited chart.

## Source

- https://www.unicode.org/charts/PDF/U13000.pdf

Unicode character names encode Gardiner catalog numbers (for example
`EGYPTIAN HIEROGLYPH A001` = Gardiner **A1** = U+13000).

## Files

| Path | Role |
| --- | --- |
| `engine/gardiner_sign_lookup.py` | Code or Unicode → subset row |
| `engine/data/gardiner_sign_subset.json` | Tiny sourced table |
| `tests/test_gardiner_sign_lookup.py` | A1 seated-man lookup |

## Limits

1. **Known-sign lookup only.** Values come from `gardiner_sign_subset.json`.
2. **Not a new decipherment.** Champollion and later Egyptology already read
   this script.
3. **No phrase verification in this module.** Unit tests check single-sign
   A1 only. A multi-sign phrase is not asserted here.
4. **No OCR / no grammar / no damaged text.**

## Verification

Unit tests compare Gardiner **A1** to Unicode **U+13000** (`EGYPTIAN
HIEROGLYPH A001`, seated man) letter-for-glyph against the Unicode chart
above.
