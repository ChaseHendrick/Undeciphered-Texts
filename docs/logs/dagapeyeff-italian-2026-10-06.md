# Italian under a one-to-one key, with errors, 6 October 2026

Not a reading. No letter string is stored.

An early pass let each of seven languages choose a merged pair of letters and liked Italian best, with M and U in one cell ([swarm](dagapeyeff-swarm-2026-10-04.md)); a later check found that rule fails on the book's own solved English sentence, and letter rates alone put Italian draws on the cells' flatness 6 times in 2,000 ([languages](dagapeyeff-languages-2026-10-04.md)). Neither used real Italian text or allowed enciphering errors. `engine.dagapeyeff_italian` does both.

The text is Manzoni's I promessi sposi in its 1827 edition, as aligned at sentence level by Sprugnoli and Sartor ([repository](https://github.com/RacheleSprugnoli/Sentence_Alignment_Manzoni), commit `e0eedb6`). The repository states no licence for its digital text, so the text is not copied here: the probe fetches it into the ignored `work/` folder when rerun. Accents are removed and J is folded into I, leaving 1,026,120 letters in 37 chapters.

**Counts.** Over 256,482 windows of 196 letters, the fewest errors that turn a window's counts into the cells' counts is 9, the median 28; none is within 8. Italian often uses 18 letters or fewer (13,681 windows), but its commonest letter usually exceeds the cells' 20 (only 153 windows stay at or under 20, and 8 have both). With 4, 8 or 16 random digit slips, 5,290 draws each, no draw reaches the cells and at least 13 errors are always still needed. English needs at least 8 errors at its closest ([errors](dagapeyeff-errors-2026-10-06.md)), so Italian is no closer.

**Search.** A quadgram model was fit on chapters 1 to 30. Planted Italian from chapters 31 to 37 under a random keyed square comes back 4 of 4 with every letter right (-1.74 to -1.87 a letter), and 4 of 4 with 8 digit slips (94 to 96 percent of letters right, found at -2.15 to -2.60). The cells under the Italian model score -4.5563 a letter; 5 of 8 shuffles score as high.

Italian under a one-to-one key, with or without errors at the book's rate, does not read the cells.

Not a reading. No letter string is stored.
