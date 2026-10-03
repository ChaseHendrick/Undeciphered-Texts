# Ancient Greek letter and word lookup

This is a **lookup**, not a decipherment.

It repeats two things that are already published:

- the Greek-alphabet letter alpha, as named on the Unicode 18.0.0 names list
- one Liddell-Scott-Jones gloss of the Classical Greek word ἄνθρωπος

**It does not decipher Linear B.** Linear B is a separate Mycenaean syllabary. This table has no Linear B signs, no syllabic values, and no tablet readings. A query that is not a single catalog key returns nothing.

**It does not decipher unknown Greek.** Linear A, Cypro-Minoan, and any other unread or disputed Greek-related script are out of scope. This module does not assign Greek letters or Greek words to undeciphered signs, and a match against this table is not a reading of an undeciphered text. The rest of this repository studies undeciphered texts. Do not cite this file as a solution of one of those texts.

The Greek alphabet and LSJ lemmas are already-known Classical Greek. Returning a row from this file is dictionary lookup only.

## What was fetched

On 2026-10-02 the Unicode 18.0.0 Greek and Coptic names list at <https://unicode.org/Public/18.0.0/charts/nameslist/0370/> prints:

- `0391` `Α` `GREEK CAPITAL LETTER ALPHA`
- `03B1` `α` `GREEK SMALL LETTER ALPHA`

The ancient name of that letter is the LSJ headword ἄλφα (τό, indeclinable) at <https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.04.0057:entry=a)/lfa> (Henry George Liddell, Robert Scott, *A Greek-English Lexicon*, revised and augmented by Sir Henry Stuart Jones with the assistance of Roderick McKenzie, Oxford: Clarendon Press, 1940, via the Perseus Digital Library).

The same lexicon’s entry for ἄνθρωπος, sense A, says:

> man, both as a generic term and of individuals

Source: <https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.04.0057:entry=a)/nqrwpos>

The JSON file is UTF-8 because ἄνθρωπος and ἄλφα are not ASCII. ἄνθρωπος begins with U+1F04 GREEK SMALL LETTER ALPHA WITH PSILI AND OXIA.

| Kind | Key | Gloss or name | Source |
|---|---|---|---|
| letter | U+0391 Α | GREEK CAPITAL LETTER ALPHA; ancient name ἄλφα | <https://unicode.org/Public/18.0.0/charts/nameslist/0370/> |
| letter | U+03B1 α | GREEK SMALL LETTER ALPHA; ancient name ἄλφα | <https://unicode.org/Public/18.0.0/charts/nameslist/0370/> |
| word | ἄνθρωπος | man, both as a generic term and of individuals | <https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.04.0057:entry=a)/nqrwpos> |

## Code

- `engine/data/ancient_greek_lookup.json` holds the rows and the source URLs.
- `engine/ancient_greek_lookup.py` loads that file. `lookup_word("ἄνθρωπος")` returns the gloss. `lookup_letter("Α")` returns the letter. A multi-word string returns `None`.
- `tests/test_ancient_greek_lookup.py` checks the fetched ἄνθρωπος gloss.

```bash
python3 -m unittest tests.test_ancient_greek_lookup -v
```
