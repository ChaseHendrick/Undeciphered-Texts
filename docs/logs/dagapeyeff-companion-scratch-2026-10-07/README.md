# D'Agapeyeff challenge: Latin attacks

Not a reading. No plaintext is claimed and no letter string is stored.

This repo continues the D'Agapeyeff work in
[Undeciphered-Texts](https://github.com/ChaseHendrick/Undeciphered-Texts), now aimed only at **Latin**.
Latin is the closest of the 98 screened languages to the cells' letter counts, but no Latin window in
59.8 million letters matches them with fewer than 3 wrong cells. So the open hypothesis is
**Latin with a few author mistakes under some system**, set against **no message at all**.

The code imports the Undeciphered-Texts engine (cells, Latin quadgram model fitted on the first 90 percent of
UD_Latin-ITTB, kernels). Clone it next to this repo, or set `UNDECIPHERED_TEXTS` to its path.

## Results, 7 October 2026

### 1. Latin under columnar transposition, widths 2 to 9: closed with power

`engine.dagapeyeff_latinsmall` from Undeciphered-Texts was written earlier but never run. It anneals the column order
and letter key together, both directions, short last row allowed. Frozen output: `results/latin_small_widths.json`.

- Planted held-out Latin was recovered **48 of 48** times: Thomistic, classical, and 8-wrong-cell texts, with at least 90 percent of cells right.
- The weakest recovered planted text scored **-2.96** a letter. The cells' best was **-3.93**, at width 9 undone.
- The cells beat all 5 shuffles in 4 of 32 cases; chance gives about 5.

Together with the earlier widths 10 to 15, **Latin under any single columnar key, widths 2 to 15, does not read the cells.**

### 2. How many author mistakes can the Latin searches absorb? (`latin/latin_errors.py`)

Planted Latin under a random key had k cells replaced at random. The table shows recovery, out of 6 each.

| Wrong cells (of 196) | Keyed square | Width-7 columnar |
| --- | --- | --- |
| 0 | 6 | 6 |
| 8 (4%) | 6 | 5 |
| 16 (8%) | 6 | 6 |
| 24 (12%) | 5 | 5 |
| 32 (16%) | 4 | 3 |
| 48 (24%) | 2 | 0 |

The searches still find Latin when about one cell in eight is wrong. So "Latin with mistakes" under these systems is
excluded up to roughly a 10 percent error rate.

Caveat: past about 16 errors, a correctly recovered text scores only -3.3 to -4.0 a letter, which overlaps the cells'
best scores. The score gap alone therefore stops separating heavily mistaken Latin from noise. A word-level check of the
best decryptions is the next test.

### 3. Turning grille (14 by 14) under Latin: still no power (`latin/latin_grille.py`, `latin/latin_grille.c`)

Frozen output: `results/latin_grille.json`. The cells were not searched, because a search without power closes nothing.

- **Key held fixed:** an exact key recovers 4 of 4 planted Latin grilles. A key with 77 to 82 percent of cells right recovers 1 of 4. A key with 65 to 69 percent recovers 0 of 4.
- **Joint search, new:** the letter key is re-solved by a quadgram climb at every grille move. It recovered 0 of 4, settling at 15 to 22 of 49 holes and -2.8 to -3.0 a letter, against true scores of about -1.7.
- **Scratch runs, not frozen:**
  - Nesting the key under a letter-pair model also failed. Wrong grilles with tuned keys score as well as or better than the truth under pairs (for example -449 found against -467 true), so pairs overfit.
  - 80 independent 1M-step joint restarts found neither planted grille, at most 22 holes.
  - Starting the joint search from the exact key, with the key free to move, drifts to about -2.5 and loses the grille.

The grille search needs a key that is about 80 percent right or better. Every key-only method so far reaches at most
59 percent (Undeciphered-Texts, `dagapeyeff-grillec`). A turning grille with a Latin plaintext therefore stays
**open**: neither found nor excluded.

### 4. Double columnar transposition under Latin: partial power only (`latin/latin_double.py`, scratch)

The joint anneal of both orders and the key recovered planted Latin at 4x5 and 5x7, but not at 7x9 (even with 2 x 30M
steps). A two-phase version, which first sets the orders by a key-invariant repeat count, failed even at 5x7. Its score
has spurious maxima: a found 215 against a true 209. Nothing is closed here.

## Where this leaves Latin

Closed with shown Latin power:
- keyed square, with or without the dummy rule
- single columnar transposition, widths 2 to 15
- repeating coordinate shift
- four-square with standard squares

Open:
- a turning grille
- double transposition
- keyed four-square
- a "Latin" that is free composition with no message

The "no message" hypothesis still fits every statistic measured.
