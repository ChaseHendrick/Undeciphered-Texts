# Truppenschlüssel pair grid, 4 October 2026

Not solved. No square was searched. No plaintext is claimed.

This cipher encrypts letters in pairs. The same plaintext pair always comes out as the same ciphertext pair, so a German-like message should repeat pairs about as often as German does. Random letters of this length barely repeat any. The designator is five letters. Dropping it shifts every pair by one.

`extra` is the number of pairs that copy an earlier pair. `random` is how many of 400 J-free strings repeated at least that often. The Grimm column is the low, median, and high of slices of the same length.

| Message | Grid | Length | Extra repeats | Random strings | Grimm low / median / high |
| --- | --- | ---: | ---: | ---: | --- |
| IASRZ 129 | from the first printed letter | 90 | 9 | 0 / 400 | 4 / 9 / 12 |
| IASRZ 129 | designator removed | 85 | 5 | 4 / 400 | 2 / 8 / 11 |
| IASRZ 130 | from the first printed letter | 52 | 2 | 39 / 400 | 1 / 3 / 9 |
| IASRZ 130 | designator removed | 47 | 0 | 400 / 400 | 0 / 3 / 6 |
| DSZPZ | from the first printed letter | 62 | 8 | 0 / 400 | 1 / 4 / 12 |
| DSZPZ | designator removed | 57 | 5 | 0 / 400 | 1 / 4 / 9 |
| DEZPS | from the first printed letter | 58 | 4 | 1 / 400 | 1 / 4 / 11 |
| DEZPS | designator removed | 53 | 3 | 3 / 400 | 1 / 3 / 9 |
| SSKFV | from the first printed letter | 60 | 4 | 0 / 400 | 1 / 4 / 11 |
| SSKFV | designator removed | 55 | 0 | 400 / 400 | 0 / 3 / 9 |
| HOHOX | from the first printed letter | 55 | 2 | 44 / 400 | 0 / 3 / 9 |
| HOHOX | designator removed | 50 | 1 | 148 / 400 | 0 / 3 / 9 |

The long messages repeat pairs about as often as the Grimm sample, and random letters do not, when pairs start on the first printed letter. SSKFV is the clean contrast: remove the five-letter designator and the excess drops from 4 to 0. HOHOX and the short IASRZ message do not separate from random on either grid. DEZPS omits the printed dash, so its pairs are off by one slot at that point.

The earlier 1735 alignment has 33 agreeing letters and 21 of those sit next to another agreement. A random set of 33 letters out of 57 produces up to 24 such neighbors (200 draws, median 19). The clump is not tighter than that chance. Agreement is real. Pair-clumping inside the alignment is not extra evidence.

`solved` stays false and `claimed_plaintext` stays null.
