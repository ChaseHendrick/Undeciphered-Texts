# Every language in Universal Dependencies, 6 October 2026

Not a reading. No letter string is stored.

The [language screen](dagapeyeff-screen-2026-10-06.md) took 39 languages. `engine.dagapeyeff_alllanguages` takes every language that Universal Dependencies lists with at least 5,000 tokens, one treebank each: the largest of at most 1.5 million tokens, as listed on universaldependencies.org on 6 October 2026. That is 134 languages. The count is the same: the fewest single-cell errors that turn a 196-letter window into the cells' letter counts, under any one-to-one key and any order.

Latin-alphabet text is folded as before. Cyrillic, Greek, Armenian, Georgian and Coptic text is romanized letter by letter with the `unidecode` package. Scripts that write no separate vowels, or that write syllables or words (Arabic, Hebrew, the Indic scripts, Chinese, Japanese, Korean, Thai, Ethiopic, Mongolian), are skipped, because a romanization would invent the letters being counted. Twelve treebanks carry no sentence text and two have under 20,000 letters. 98 languages are screened: 77 in the Latin alphabet, 13 Cyrillic, 3 Armenian, 2 Greek, 2 Georgian and 1 Coptic.

| Language (treebank) | Fewest errors | Median | Windows within 8 per million |
| --- | --- | --- | --- |
| Latin (ITTB) | 4 | 22 | 1,201 |
| Estonian (EDT) | 4 | 28 | 112 |
| Catalan (AnCora) | 5 | 28 | 33 |
| Old Occitan (CorAG) | 5 | 32 | 218 |
| Armenian (ArmTDP), romanized | 6 | 27 | 69 |
| Spanish (AnCora) | 6 | 27 | 21 |
| Buryat (BDT), romanized | 6 | 30 | 394 |
| Icelandic (IcePaHC) | 7 | 25 | 69 |
| Western Armenian (ArmTDP), romanized | 7 | 27 | 91 |
| Old East Slavic (TOROT), romanized | 7 | 32 | 22 |
| Welsh, Manx, Norwegian, Romanian (nonstandard) | 8 | 26 to 31 | 9 to 47 |
| Every other language | 9 or more | 25 or more | 0 |

Latin stands out on both measures that describe a whole language rather than one lucky window. Its median, 22, is the lowest of all 98; the next are Icelandic and Faroese at 25. Its rate of windows within 8 errors, 1,201 per million, is three times the next (Buryat, 394, from a corpus of only 58,624 letters) and over ten times that of any large corpus. Only its single closest window is matched: Estonian's EDT treebank also reaches 4, with a median of 28.

So the letter counts still point to Latin, now against every language with usable text in Universal Dependencies. Across 59.8 million letters of Latin ([library](dagapeyeff-latinlib-2026-10-06.md), [Latin Library](dagapeyeff-latinlibrary-2026-10-06.md)) the best windows need 3 errors. This is a reason to search Latin under the systems still open, not a reading.

Not a reading. No letter string is stored.
