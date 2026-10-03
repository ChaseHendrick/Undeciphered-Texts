# Coptic letter reader

`engine/coptic_letters.py` names Unicode Coptic letters and looks up three published headwords. It is a letter inventory plus a pocket lexicon. It is not a decipherment tool.

## What a hit means

A hit means the spelling is one of the three rows below, copied from a public page. It does not mean an unknown script has been read. Characters that are not Unicode Coptic letters come back as unread. They are not assigned a sound.

## Letters

Names are the Unicode character names.

- Coptic block: https://www.unicode.org/charts/PDF/U2C80.pdf
- Coptic letters still encoded in the Greek and Coptic block (U+03E2-U+03EF): https://www.unicode.org/charts/PDF/U0370.pdf

## Lexicon

Checked against the live pages on 2026-10-02 (ET).

| Spelling | Code points | Romanization | Gloss | Source |
|---|---|---|---|---|
| ⲣⲱⲙⲉ | U+2CA3 U+2CB1 U+2C99 U+2C89 | rōme | human, person (noun) | https://en.wiktionary.org/wiki/ⲣⲱⲙⲉ |
| ⲁⲛⲟⲕ | U+2C81 U+2C9B U+2C9F U+2C95 | anok | I (pronoun) | https://en.wiktionary.org/wiki/ⲁⲛⲟⲕ |
| ⲥⲛⲁⲩ | U+2CA5 U+2C9B U+2C81 U+2CA9 | snau | two (numeral) | https://en.wiktionary.org/wiki/ⲥⲛⲁⲩ |

Wiktionary points ⲣⲱⲙⲉ at Crum 1939, page 294, and ⲁⲛⲟⲕ at page 11:

- http://coptot.manuscriptroom.com/crum-coptic-dictionary/?pageID=294
- http://coptot.manuscriptroom.com/crum-coptic-dictionary/?pageID=11

Those links are bibliography. This module does not OCR the scan.

## Test

```bash
python3 -m unittest tests.test_coptic_letters -v
```

`test_rome_letters_and_gloss` requires the four letter names of ⲣⲱⲙⲉ (RO, OOU, MI, EIE) and the gloss "human, person".

## What this does not do

It does not read Linear A, Indus, Rongorongo, Voynich, or any undeciphered script. It does not transcribe a manuscript photograph. It does not claim the Coptic stage of Egyptian is unsolved; Coptic is a known alphabet, which is why a dictionary lookup is possible.
