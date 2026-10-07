# Latin words in the cells' best decryptions, 7 October 2026

Not a reading. No letter string is stored.

A score per letter stops separating heavily mistaken Latin from noise. Planted Latin with 16 to 32 wrong cells is still recovered, but its found score falls to -3.3 to -4.0 a letter, where the cells' best decryptions also sit. Words can separate them. A decryption that is about 90 percent right keeps runs of real words, and a key fitted to noise does not.

`engine.dagapeyeff_latinwords` measures the share of letters covered by non-overlapping dictionary words of at least five letters, using the best cover. The vocabulary is 19,400 word forms, each seen at least twice in the training part of UD_Latin-ITTB or in UD_Latin-PROIEL. Planted texts come from the held-out ITTB tail and from UD_Latin-Perseus, which the vocabulary does not include.

**Planted Latin.** The texts were put under a keyed square or width-7 columns, given k wrong cells, and decrypted with the key the search found. There are 12 texts at each k.

| Wrong cells | Recovered (90 percent of clean cells) | Word coverage |
| --- | --- | --- |
| 0 | 12 of 12 | 42 to 84 percent |
| 8 | 12 of 12 | 26 to 62 percent |
| 16 | 11 of 12 | 11 to 46 percent |
| 24 | 7 of 12 | 17 to 40 percent |
| 32 | 11 of 12 | 17 to 31 percent |

**The cells.** The searches were the keyed square, the book's dummy rule (13 variants) and columnar widths 2 to 15 in both directions: 41 searches for each source. Each of 4 shuffles got the same 41 searches.

| Source | Best coverage | Best system | Shuffles as high (of 4) |
| --- | --- | --- | --- |
| Printed cells | 12.8 percent | columnar 8 undone | 3 |
| Regrouping | 10.2 percent | columnar 12 done | 3 |

59 of the 60 planted texts score above the printed cells. The one exception has 16 wrong cells and was not recovered. The cells' best is what shuffled cells reach.

Latin under these systems, with up to about one wrong cell in six, would have shown its words; the cells show none beyond chance. This closes "Latin with the author's mistakes" for the keyed square, the dummy rule and single columnar keys at widths 2 to 15, at error rates the quadgram score alone could not decide. It says nothing about a grille, double transposition or keyed four-square.

Not a reading. No letter string is stored.
