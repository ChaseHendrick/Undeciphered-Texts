# Width-14 columnar with a letter key, compiled, 6 October 2026

Not a reading. No letter string is stored.

The cells are 196 symbols, exactly 14 rows of 14. A Polybius substitution followed by a complete 14-column transposition is the plainest large-key hypothesis. Tiago Rodrigues (Cipher Mysteries, 2014) reported needing about 240 letters for a 14-column key with a substitution. The Python joint search in `engine.dagapeyeff_columnar` recovered 0 of 3 planted texts at this width, so the class was open.

`engine/dagapeyeff_columnar14c.c` anneals the column order and the letter key together under the default model with J folded into I. `engine.dagapeyeff_columnar14c.columnar14c_report` runs 8 restarts of 16,000,000 steps at temperature 12 for every text, on four threads. A scratch sweep before the frozen run found one restart of 1,000,000 steps finds a planted key about 1 time in 40, 4,000,000 steps about 1 in 7, and 16,000,000 steps about 2 in 5. Eight long restarts were chosen from that.

Both directions are searched. Undone: the plaintext was written in rows of 14 and the columns copied out in key order. Done: the cells are what that copying gives when run backwards, the direction the book's own double-transposition example numbers its key in (Pelling, 5 March 2017). In the done direction the plaintext is 14 runs of 14 letters whose order only shows at 13 joins, so recovery is counted by the key: at least 90 percent of the cells get their true letter, whatever the column order. Planted texts with 8 wrong cells, about the book's own error rate over 196 letters, show what enciphering mistakes cost. Most of the book's faults were dropped pairs, not wrong cells; a dropped pair would break a complete 14 by 14 rectangle, which this hypothesis assumes.

| Run | Result |
| --- | --- |
| Planted, undone, clean (6) | 6 recovered; 5 exact, 1 at 99 percent of cells |
| Planted, undone, 8 wrong cells (3) | 3 recovered, 95 to 96 percent of cells; found at -2.43 to -2.63 a letter |
| Planted, done, clean (6) | 6 recovered, every cell right |
| Planted, done, 8 wrong cells (3) | 3 recovered, 93 to 97 percent of cells; found at -2.14 to -2.41 a letter |
| Printed cells, undone | -3.2526 a letter; 7 of 20 shuffles as high |
| Printed cells, done | -3.5409 a letter; 12 of 20 shuffles as high |
| Regrouping, undone | -3.3892 a letter; 5 of 20 shuffles as high |
| Regrouping, done | -3.6429 a letter; 11 of 20 shuffles as high |

Clean planted English is found at -1.83 to -2.03 a letter. The weakest planted text, with 8 wrong cells, is found at -2.632. The cells' best, -3.2526, is more than 0.6 a letter below that and sits inside its own shuffles. In the done direction several planted texts were found slightly above their true score, with the runs in another order; the letters were all right.

A complete 14-column transposition over a one-to-one letter key, in either direction, with up to about 8 enciphering errors, does not read the cells or the regrouping as English. This was already unlikely for ordinary prose from the letter counts alone ([corpus note](dagapeyeff-corpus-2026-10-05.md)); this search shows it with a method that finds every planted case. It says nothing about a transposition with nulls, an incomplete rectangle, or a plaintext in another language.

Not a reading. No letter string is stored.
