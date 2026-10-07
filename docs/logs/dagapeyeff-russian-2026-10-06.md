# Russian under four transliterations, 6 October 2026

Not a reading. No letter string is stored.

D'Agapeyeff was born in Russia, so Russian is the obvious second guess after English. The [language screen](dagapeyeff-screen-2026-10-06.md) used one transliteration, a plain British style, and Russian needed 13 errors at its closest window. A writer putting Russian on a 25-letter square has to choose a spelling, and digraphs such as ZH, KH and SHCH move the letter counts, so one spelling is not enough to set Russian aside.

`engine.dagapeyeff_russian` repeats the count of the screen (the fewest single-cell errors that turn a 196-letter window into the cells' counts, under any one-to-one key and any order) for four spellings: the British style, one Latin letter for each Cyrillic letter (ISO 9 with accents removed, so Ч is C and Ш is S), a German style (SCH, TSCH, W) and a French style (OU, TCH, CH). Three Universal Dependencies treebanks supply the text, two of them with about eight million letters.

| Treebank | British | One letter | German | French | Medians |
| --- | --- | --- | --- | --- | --- |
| Russian-GSD | 13 | 12 | 10 | 13 | 30 to 33 |
| Russian-SynTagRus | 11 | 9 | 10 | 12 | 29 to 34 |
| Russian-Taiga | 10 | 9 | 9 | 12 | 29 to 34 |

The table gives the fewest errors at the closest window. No window of any spelling comes within 8 errors. Latin needs 4 at its closest window, with a median of 22 and 294 windows within 8; English needs 8, with a median of 28 ([corpus](dagapeyeff-corpus-2026-10-05.md)).

The spelling changes the closest window by up to four errors, but never brings Russian near Latin, and no spelling beats English. Under a one-to-one key, Russian is not a better lead than English. This says nothing about Russian under a system that changes the counts.

Not a reading. No letter string is stored.
