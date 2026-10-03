# Latin and Roman readers

Latin is a known language. These modules do not decipher unknown texts.

`engine/roman_text.py` rewrites Roman inscription spelling. `engine/latin_reader.py` looks up the resulting words in a small lexicon. A gloss is a quoted dictionary line, not a reading of Linear A, Etruscan, the Indus script, Rongorongo, or any other undeciphered writing. An unknown token stays unknown.

## What the Roman reader changes

Epigraphic form (`to_epigraphic`):

- letters become A–Z capitals
- U becomes V, and J becomes I
- inscription word-dots become spaces: `·` U+00B7, and the other dots listed in `INTERPUNCTS`
- macrons are removed (`dīvīsa` → `DIVISA`)

Classical form (`to_classical`):

- J becomes I
- QV becomes QU
- V before a consonant, or at the end of a word, becomes U (`SENATVS` → `SENATUS`, `IVLIVS` → `IULIUS`)
- V before a vowel stays V at the start of a word or between vowels (`VENI`, `DIVISA`)

ASCII `.` is not turned into a word space. `M.AGRIPPA` stays one token: the dot is dropped with other non-letters, and the result is `MAGRIPPA`, not `M` plus `AGRIPPA`.

Limit, on purpose: V after a consonant and before a vowel is left as V. `SERVARE` stays `SERVARE`. `PUER` would be left as `PVER`. Fixing that needs a dictionary, which this normalizer does not consult.

## Lexicon

`engine/data/latin_lexicon.json` is a short list, not a full dictionary.

Most headwords and English glosses are copied from the Dickinson College Commentaries Latin Core Vocabulary (Christopher Francese and the DCC team, CC BY-SA 3.0):

https://dcc.dickinson.edu/latin-core-list1

`Gallia` is not on that core list. Its gloss is copied from the vocabulary on the DCC Caesar commentary:

https://dcc.dickinson.edu/caesar/book-1/chapter-1-1

`forms` is only an index. `est` points at the headword `sum`, and `divisa` points at `dīvidō`. The gloss stored for those forms is still the headword gloss from the cited page. The reader does not generate case, gender, or a sentence translation.

A final `-que` is split only when both the stem and `que` are in the list (`POPVLVSQVE` → populus + que).

## Published line used in the test

Caesar, *De bello Gallico* 1.1, T. Rice Holmes (Oxford: Clarendon Press, 1914), as transcribed on Perseus. Checked 2026-10-02:

https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.02.0002:book=1:chapter=1

The clause before the comma is `Gallia est omnis divisa in partes tres`. The unit test feeds the same words with interpuncts (`GALLIA·EST·OMNIS·DIVISA·IN·PARTES·TRES`) and checks the classical string and the cited glosses.

The same opening is also printed, with macrons, by Dickinson College Commentaries:

https://dcc.dickinson.edu/caesar/book-1/chapter-1-1

## How to run

From the repository root:

```bash
python3 -m unittest tests.test_latin_roman_reader -v
```

A pass means the normalizer and the lexicon lookup agreed with that published clause. It does not mean an undeciphered text was read.
