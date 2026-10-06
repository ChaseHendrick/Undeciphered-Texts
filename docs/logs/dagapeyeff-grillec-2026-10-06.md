# A compiled turning-grille search: power only, 6 October 2026

Not a reading. No letter string is stored. The cells were not searched.

`engine.dagapeyeff_grille` (5 October) annealed a 14 by 14 Fleissner grille in Python. With the letter key given it recovered 1 of 3 planted grilles; with the key unknown, 0 of 2. `engine/dagapeyeff_grillec.c` compiles the same grille convention and `engine.dagapeyeff_grillec.grillec_report` gives it far more steps, under the default model with J folded into I, on held-out windows of 196 letters.

| Case | Search | Recovered |
| --- | --- | --- |
| Letter key given | 4 restarts of 2,000,000 steps | 4 of 4 grilles, every hole and every cell |
| Grille and key unknown, key from letter frequencies | 4 restarts of 8,000,000 steps | 0 of 4; 13 to 18 of 49 holes; found at -2.73 to -2.92 a letter |
| Key seeded without the grille, then held fixed | 4 restarts of 2,000,000 steps | 0 of 4; 15 to 20 of 49 holes |

The seed uses a fact about any turning grille read this way: two cells side by side in a row of the square are consecutive plaintext letters whenever their holes open in the same turn, about one time in four, whatever the grille. A key climbed on those pairs, and on pairs two and three apart, started with 13 to 49 percent of the cells right in this run. On four other texts in a scratch run it raised a frequency key's 17 to 34 percent to 31 to 59 percent. That was not enough. A scratch run held a seeded key with 59 percent of cells right and still found only 17 of 49 holes. The grille search needs a key that is very nearly right.

One of the four joint windows is Project Gutenberg header text, not prose: its true text scores -3.28 a letter. The other three are prose and were not recovered either.

The compiled grille search has power only with the key given. With grille and key both unknown at 196 letters it found 0 of the 7 planted prose grilles in the joint and seeded cases, so a grille on the cells is neither found nor excluded by searching. Scratch runs of single 64,000,000-step anneals also failed. A grille is a transposition, so the letter-count argument in the [corpus note](dagapeyeff-corpus-2026-10-05.md) still applies to it for ordinary English prose.

Not a reading. No letter string is stored.
