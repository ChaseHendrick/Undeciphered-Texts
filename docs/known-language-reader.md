# Known-language reader

`engine/known_language_reader.py` routes a short phrase to a reader for a language that is already known.

- English and German use a small lexicon in that module. Glosses are short English senses of the cited Wiktionary headword.
- Latin is delegated to `engine.latin_reader`, which glosses from the Dickinson College Commentaries lists.
- Egyptian sign codes are delegated to `engine.egyptian` when that module imports. It maps Gardiner codes in a sourced subset to transliteration and a gloss. If the module is absent, Egyptian is skipped and no sign values are invented.

German headwords stay in UTF-8: König, Töchter, schön, jüngste. The Grimm excerpt still spells daß with ß. That token is not in the lexicon, so it stays unglossed.

## What this is not

This reader glosses a few known languages from cited dictionaries. It does not decipher unknown languages or scripts, including Linear A, the Indus script, the Voynich manuscript, and rongorongo.

Passing Linear A, the Indus script, the Voynich manuscript, or rongorongo raises `UnknownScriptError` and returns no gloss. Those are not languages this router can read. It does not score them, align them, or propose a plaintext.

## Phrases the unit test fetches

`tests/test_known_language_reader.py` downloads one cited phrase per included language and glosses that phrase:

| Language | Phrase | Where it is fetched |
|---|---|---|
| English | Alice was beginning to get very tired of sitting by her sister on the bank | Lewis Carroll, *Alice's Adventures in Wonderland*, Project Gutenberg 11 |
| Latin | Gallia est omnis divisa in partes tres | Caesar, *De bello Gallico* 1.1, on Perseus |
| German | lebte ein König, dessen Töchter waren alle schön, aber die jüngste war so schön | Grimm, *Der Froschkönig oder der eiserne Heinrich*, Project Gutenberg 77905 |
| Egyptian | M17 Y5 N35, read as jmn | Wikipedia, *Amun* (wikihiero codes on that page) |

`tired` is glossed as in need of rest or sleep. `Gallia` is glossed as Gaul from the Dickinson commentary vocabulary. `König` is glossed as king. The Egyptian codes are glossed from the Gardiner subset, and the transliteration `jmn` has to occur in the fetched Amun article. None of that is a reading of an unsolved script.
