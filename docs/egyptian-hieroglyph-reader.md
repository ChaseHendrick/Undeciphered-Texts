# Egyptian hieroglyph reader (known-script lookup)

Egyptian hieroglyphs are a **known, deciphered script**. This repository module
does **not** claim a new decipherment. It looks up a small subset of Gardiner
signs and returns traditional Egyptological transliteration plus a short gloss.

## Source

Sign rows (Gardiner code, Unicode when present, transliteration, meaning) are
taken from:

- https://en.wikipedia.org/wiki/List_of_Egyptian_hieroglyphs

Supporting checks for phonetic values and the verification phrase:

- https://en.wikipedia.org/wiki/Egyptian_biliteral_signs (Y5 = *mn*)
- https://en.wikipedia.org/wiki/Egyptian_triliteral_signs (S34 = *ꜥnḫ*)
- https://en.wiktionary.org/wiki/jmn (Amun: hieroglyphic spelling *i-mn:n* = M17 Y5 N35, reading **jmn**)
- https://en.wikipedia.org/wiki/Amun (Ancient Egyptian: *jmn*)
- https://en.wikipedia.org/wiki/Tutankhamun (Ancient Egyptian: *twt-ꜥnḫ-jmn*)

Unicode code points also match the Unicode Egyptian Hieroglyphs block names
(`EGYPTIAN HIEROGLYPH …`) in the Unicode Character Database.

## Files

| Path | Role |
| --- | --- |
| `engine/egyptian.py` | Reader: Gardiner codes or Unicode → transliteration + gloss |
| `engine/data/gardiner_signs.json` | Sourced subset table |
| `tests/test_egyptian.py` | Sign-table tests + verified Amun phrase |

## Usage

```python
from engine.egyptian import read_hieroglyphs

# Gardiner codes (Manuel de Codage style identifiers)
reading = read_hieroglyphs("M17 Y5 N35")
assert reading.transliteration == "jmn"  # Amun; see Wiktionary jmn

# Same phrase as Unicode hieroglyphs
reading = read_hieroglyphs("𓇋𓏠𓈖")
assert reading.transliteration == "jmn"
```

The reader concatenates each sign's table transliteration. If the next value is already a suffix of the reading (a phonetic complement), it is not repeated. That is why M17 + Y5 + N35 (`j` + `mn` + `n`) reads **jmn**, matching the sources above, rather than `jmnn`.

## Limits (read carefully)

1. **Known-sign lookup only.** The reader returns values stored in
   `gardiner_signs.json`. It does not infer readings for signs outside that
   table.
2. **Not a new decipherment.** Champollion and later Egyptology already read
   this script. Shipping a dictionary here is bookkeeping, not a breakthrough.
3. **No damaged or unknown inscriptions.** Gaps, lacunae, uncertain signs,
   Linear A, Indus, Rongorongo, Voynich, and other undeciphered corpora are out
   of scope. Do not feed photographs or damaged text into this API and treat the
   output as a reading of that object.
4. **Subset, not Gardiner’s full list.** Only the bundled rows are available.
5. **No grammar / no OCR.** The module concatenates phonetic values; it does
   not parse Middle Egyptian syntax or recognize signs from images.

## Verification phrase

Unit tests compare the sequence **M17 + Y5 + N35** (Unicode 𓇋𓏠𓈖) to the
transliteration **jmn** letter-for-letter against
[Wiktionary *jmn*](https://en.wiktionary.org/wiki/jmn) (head spelling
`i-mn:n`, reading `jmn`) and [Wikipedia *Amun*](https://en.wikipedia.org/wiki/Amun).
