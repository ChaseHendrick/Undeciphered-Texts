# Maya glyph lookup

This is a small catalog lookup for **one already published** Classic Maya sign reading. It is not a decipherment tool.

**It does not decipher undeciphered Maya passages.**

Giving it a block, a collocation, a codex sentence, or any string that is not a single catalog key returns nothing. It does not segment signs, propose phonetic complements, or guess readings for signs that are still unread. Classic Maya is largely deciphered as a script; particular signs, spellings, and passages are still disputed or unread. Those are out of scope here. The rest of this repository studies undeciphered texts. This table must not be cited as a reading of one of those texts.

## What was fetched

On 2026-10-02 the Learner's Maya Glyph Guide grid at <https://mayaglyphs.org/CMGGgrid.html> (Sim Lee and John Pedersen, April 2026; HTML version of Sim Lee, *Classic Maya Glyph Guide*, Amsterdam: self-published, 2023–2026) labels the sign **K'IN** and lists Thompson numbers **T544**, T755, and T1010abc on that same label. The grid writes the glottal as the HTML character reference `&#x27;` (U+0027 APOSTROPHE).

The linked entry <https://mayaglyphs.org/CWLhtml/K%27INlogo.html> says, in the Translation line:

> day; sun; calendar unit k’in, 1st (lowest) position in the LC = 1 day

Part of speech: Noun. In that gloss the vowel of *k’in* is U+2019 RIGHT SINGLE QUOTATION MARK, which is why the JSON file is UTF-8 and not ASCII.

| Key | Reading | Gloss | Source |
|---|---|---|---|
| T544 | K'IN | day; sun; calendar unit k’in, 1st (lowest) position in the LC = 1 day | <https://mayaglyphs.org/CWLhtml/K%27INlogo.html> |

## Code

- `engine/data/maya_glyph_lookup.json` holds the row and the source URL.
- `engine/maya_glyph_lookup.py` loads that file. `lookup("T544")` returns the row. `lookup` of a multi-word passage returns `None`.
- `tests/test_maya_glyph_lookup.py` checks the T544 reading and gloss against the strings fetched above.

```bash
python3 -m unittest tests.test_maya_glyph_lookup -v
```
