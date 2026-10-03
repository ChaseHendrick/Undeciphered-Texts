# Elder Futhark lookup (not a decipherment)

This repository ships a **sourced lookup** of the 24-rune Elder Futhark
inventory. It is **not** a decipherment of unknown inscriptions.

## What this is

- A table of already-published Elder Futhark glyphs, transliterations,
  reconstructed Proto-Germanic names, and short glosses.
- A small Python helper (`engine/elder_futhark.py`) that loads
  `engine/data/elder_futhark.json` and returns the matching row for a
  known Unicode rune.

## What this is not

- Not a crack of an undeciphered text.
- Not a claim that any unreadable inscription has been read.
- Not a solver for Younger Futhark, Anglo-Saxon futhorc, or invented
  "runic" puzzles beyond the published Elder Futhark alphabet.

Elder Futhark itself was deciphered in the nineteenth century; the
values here are the conventional published inventory, not a new reading.

## Source

- URL: <https://en.wikipedia.org/wiki/Elder_Futhark>
- Retrieved: 2026-10-02 (America/New_York)
- Fields taken from the article's transliteration / phoneme tables and
  the "Rune names" table (Unicode code points, transliteration, IPA,
  Proto-Germanic name, short meaning).

## Known value used in tests

Wikipedia lists rune **ᚠ** (U+16A0) with transliteration **f**, name
`*fehu`, meaning "cattle", "wealth". The unit test asserts that lookup
returns those sourced fields.

## Usage

```python
from engine.elder_futhark import lookup, transliterate, SOURCE_URL

print(SOURCE_URL)
print(lookup("ᚠ"))
print(transliterate("ᚠᚢᚦ"))  # -> "fuþ"
```

## Files

| Path | Role |
| --- | --- |
| `engine/data/elder_futhark.json` | UTF-8 sourced inventory |
| `engine/elder_futhark.py` | Lookup API |
| `tests/test_elder_futhark.py` | Unit test of one fetched rune |
| `docs/elder-futhark-lookup.md` | This note |
