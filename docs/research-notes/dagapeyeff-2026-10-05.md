# D'Agapeyeff challenge: measured structure, not a reading

<!--
index-id: dagapeyeff
index-title: D'Agapeyeff challenge
index-problem: 1939 digit challenge with no public reading; measured structure is not a plaintext
index-data: Wikipedia digit block used by the engine, plus the solved exercise as the control
index-next: Search Catalan, Romanian and Latin under a 14-column key and under keyed four-square once a method with power exists; screen further languages
-->

Source check: **2026-10-05**. Category: historical cipher. No reading is claimed.

The public digit block is the one on the English Wikipedia page for the D'Agapeyeff cipher. That page was fetched on 2026-10-02. It attributes the challenge to Alexander D'Agapeyeff, *Codes and Ciphers* (Oxford University Press, 1939), page 158, and says later editions dropped it. This note did not re-inspect the 1939 book. The engine uses that digit block. The solved Polybius exercise from the same page is the control, not a crib for the challenge. [Wikipedia](https://en.wikipedia.org/wiki/D%27Agapeyeff_cipher). [First inspection](../logs/dagapeyeff-2026-10-02.md).

<!-- generated-status:start -->
## How close is this to solved?

**Unsolved. Plaintext recovered: 0 percent. 28 of 34 hypothesis families listed (82 percent) are closed with shown power or excluded by a count; 6 are open. Reviewed through 2026-10-06.**

Progress here means ruling hypotheses out, not reading part of a message. The percentage is a share of the families listed below, which is not every possible cipher, and a hand construction with no message fits every statistic measured so far. It is not a measure of distance to a reading.

| Status | Families | Share |
| --- | --- | --- |
| Open | 6 | 18 percent |
| Tested without shown power | 0 | 0 percent |
| Excluded by a count | 12 | 35 percent |
| Closed with shown power | 16 | 47 percent |

### Open (6)

| Family | Evidence |
| --- | --- |
| A plaintext in another language under a large transposition, or in a language not screened | 39 languages were screened by letter counts; Latin is closest, then Catalan and Romanian. Italian and Latin under a one-to-one key are closed; Latin under a 14-column key is closed; the grille has no power in any language. [log](../logs/dagapeyeff-screen-2026-10-06.md), [log](../logs/dagapeyeff-languages-2026-10-04.md) |
| 14 by 14 turning grille with a letter key | The compiled search finds 4 of 4 planted grilles with the key given and 0 of 4 with it unknown, and order tests barely tell a grille message from no message (3 of 20; 4 of 12). A grille is a transposition, so under a one-to-one key the letter counts still need at least 8 chosen errors in English and 4 in Latin, and random errors never reach them; a grille stays open mainly with a count-flattening key or an unusual text. A homophonic key cannot flatten the counts either: no English window of 196 letters uses 18 letters or fewer, and no Latin window groups exactly into the cells' 18 symbol counts (the closest needs at most 3 errors). [log](../logs/dagapeyeff-grillec-2026-10-06.md), [log](../logs/dagapeyeff-nomessage-2026-10-06.md), [log](../logs/dagapeyeff-errors-2026-10-06.md), [log](../logs/dagapeyeff-homgroup-2026-10-06.md) |
| No message (a hand construction) | Against random dealings of the cells' own symbols the order gives a family-wise p of 0.28, with a test that flags 19 of 20 keyed-square and done-columnar messages but only 3 of 20 grille messages; a grille-specific statistic has weak power (4 of 12) and the cells sit among their dealings (25 of 40). A message now needs an order-destroying transposition and either a non-homophonic count-flattening key, chosen errors or an unusual text. [log](../logs/dagapeyeff-nomessage-2026-10-06.md), [log](../logs/dagapeyeff-prior-work-2026-10-05.md) |
| A general pair table (2 by 2 Hill, any 625-pair code) | The different-pair count does not exclude a general pair table; a 2 by 2 Hill matrix drawn at random spreads English over at least 23 symbols (0 of 1,110 draws reach the cells' 18), so random Hill keys are excluded, but a chosen 625-pair table is not. [log](../logs/dagapeyeff-pairmap-2026-10-06.md), [log](../logs/dagapeyeff-mixing-2026-10-06.md) |
| Transposition beyond the searched widths, or with nulls and an incomplete rectangle | The key-invariant method has no power past width 10; double transposition is closed only to width 6. [log](../logs/dagapeyeff-exhaustive-2026-10-05.md), [log](../logs/dagapeyeff-double-2026-10-05.md) |
| Four-square with keyed plain squares, and two-square | With chosen plain squares 15 of 15 held-out English windows reach the cells' side counts; a search annealing all four squares recovers 0 of 6 planted texts at 196 letters, so it has no power yet. [log](../logs/dagapeyeff-foursquare-2026-10-06.md), [log](../logs/dagapeyeff-keyedsquares-2026-10-06.md) |

### Excluded by a count (12)

| Family | Evidence |
| --- | --- |
| Any transposition of ordinary English prose under a one-to-one letter key | A transposition keeps letter counts; none of 479,051 prose windows has the cells' flatness, few letters and rare column together. [log](../logs/dagapeyeff-corpus-2026-10-05.md) |
| Playfair | 10 of 98 pairs repeat a cell, which Playfair never does. [log](../logs/dagapeyeff-angles-2026-10-04.md) |
| A fixed code giving each letter one pair of cells | Such a code has at most 25 different pairs; the cells have 79 and 80. [log](../logs/dagapeyeff-pairmap-2026-10-06.md) |
| The five rare symbols as word spaces | Words would average 20.89 letters; held-out English never exceeds 8.5. [log](../logs/dagapeyeff-quick-2026-10-06.md) |
| Only the column digit carries the message | The paired column digits are less coincident than any of 373 English windows. [log](../logs/dagapeyeff-quick-2026-10-06.md) |
| Eight published readings | None passes as a full-length reading against the counts the cells force; three fail their own stated method. [log](../logs/dagapeyeff-prior-work-2026-10-05.md) |
| Periodic independent alphabets (a different one-to-one key at each place modulo p, p from 2 to 14) | Applied phase by phase, the error count needs at least 13 chosen errors for any held-out English window at every period; none of 1,558 windows comes within 8. [log](../logs/dagapeyeff-phases-2026-10-06.md) |
| Straddling checkerboard and Nihilist substitution (digit codes not made of fixed pairs) | The cells' 392 digits alternate perfectly between two classes of five digits; 300 planted texts per system under random keys reach at most 0.65 to 0.85 of that alternation, none all of it. [log](../logs/dagapeyeff-digitcodes-2026-10-06.md) |
| Bifid | Under random squares bifid of every period spreads English over at least 22 symbols; the cells use 18 (0 of 7,770 draws). [log](../logs/dagapeyeff-mixing-2026-10-06.md), [log](../logs/dagapeyeff-bifid-2026-10-04.md) |
| Autokey on the square | Under random squares autokey spreads English over at least 23 symbols; the cells use 18 (0 of 1,110 draws). [log](../logs/dagapeyeff-mixing-2026-10-06.md), [log](../logs/dagapeyeff-autokey-2026-10-04.md) |
| Running key from texts in the repository, and the book's exercise as a key | An English running key spreads English over at least 24 symbols; the cells use 18 (0 of 1,110 draws). The book's exercise is such a key. [log](../logs/dagapeyeff-mixing-2026-10-06.md), [log](../logs/dagapeyeff-running-2026-10-04.md), [log](../logs/dagapeyeff-bookkey-2026-10-04.md) |
| Caesar, Vigenere, Beaufort, Porta and affine on the cells as letters | Caesar and affine are one-to-one keys, covered by the corpus count; Vigenere modulo 25 on a keyed alphabet at periods 2 to 14 spreads English over at least 20 symbols (0 of 6,660 draws reach 18). Beaufort behaves the same way; Porta was not screened separately. [log](../logs/dagapeyeff-mixing-2026-10-06.md), [log](../logs/dagapeyeff-solver-swarm-2026-10-04.md), [log](../logs/dagapeyeff-classic-swarm-2026-10-04.md) |

### Closed with shown power (16)

| Family | Evidence |
| --- | --- |
| A keyed Polybius square alone (one-to-one letter key) | Planted texts come back; the cells score -3.82 to -3.97 a letter against about -2 for English, also read backwards. [log](../logs/dagapeyeff-columnar-2026-10-05.md), [log](../logs/dagapeyeff-quick-2026-10-06.md) |
| Columnar and periodic transposition, every order at widths 2 to 9 (and width 10 done), any language | A key-invariant score; planted English and German beat their shuffles by more than the cells in all 24 cases. [log](../logs/dagapeyeff-exhaustive-2026-10-05.md) |
| Complete 14-column transposition with a letter key | 18 of 18 planted texts recovered, both directions; the cells score -3.25 to -3.64 a letter, inside their shuffles. [log](../logs/dagapeyeff-columnar14c-2026-10-06.md) |
| Double transposition, every pair of orders at widths 2 to 6 | In 50 of 50 cases the cells beat their shuffles by less than planted English and German. [log](../logs/dagapeyeff-double-2026-10-05.md) |
| Keyword transpositions (379,521 keywords, single, double and square) | Planted keywords surface near English; the cells' best is under shuffled cells. [log](../logs/dagapeyeff-keywords-2026-10-05.md) |
| Four-square with standard plain squares | Excluded by the side count (0 of 7,400 English draws with random plain squares reach the cells) and searched: 4 of 6 planted texts recovered, the cells inside their shuffles. [log](../logs/dagapeyeff-foursquare-2026-10-06.md) |
| Nulls by place (every 3rd, 4th, 5th cell, or one grid column) | 6 of 6 planted texts recovered; the cells' best is -3.28 a letter against -2.14 or better for English. [log](../logs/dagapeyeff-quick-2026-10-06.md) |
| Homophonic key (several symbols for one letter) | 6 of 6 planted homophonic texts recovered; the cells and the regrouping sit inside their shuffles. [log](../logs/dagapeyeff-homophone-2026-10-06.md) |
| A repeating shift on a keyed square (Vigenere-like), periods 2 to 14 | No English draw of 16,470 reaches the cells' 18 symbols; the joint search recovers 11 of 12 planted texts and the cells' best is -3.33 a letter against -2.08 or better for English. [log](../logs/dagapeyeff-additive-2026-10-06.md), [log](../logs/dagapeyeff-add-2026-10-04.md), [log](../logs/dagapeyeff-period4-2026-10-04.md) |
| Enciphering errors at the book's rate under a one-to-one key, with or without a transposition | No held-out English window reaches the cells' counts with fewer than 15 chosen errors, random errors never do, and with 8 slips planted English still scores -2.49 a letter or better against the cells' -3.90. [log](../logs/dagapeyeff-errors-2026-10-06.md), [log](../logs/dagapeyeff-corpus-2026-10-05.md) |
| Italian under a one-to-one key, with or without errors at the book's rate | Manzoni's Italian needs at least 9 chosen errors to reach the cells' counts; planted Italian comes back 4 of 4, also with 8 slips, and the cells score -4.56 a letter under an Italian model, inside their shuffles. [log](../logs/dagapeyeff-italian-2026-10-06.md), [log](../logs/dagapeyeff-languages-2026-10-04.md), [log](../logs/dagapeyeff-swarm-2026-10-04.md) |
| Delays, nulls by place (periods 2 to 14), rails and plain column reads | 363 transforms solved as a keyed square; planted English comes back 4 of 4, and in every family 7 or 8 of 8 shuffles reach the cells' best; the old delay-79 lead is not in the top twelve. [log](../logs/dagapeyeff-direction-2026-10-06.md), [log](../logs/dagapeyeff-delay-2026-10-04.md), [log](../logs/dagapeyeff-digit-routes-2026-10-04.md) |
| Latin under a one-to-one key, with or without the book's dummy rule and errors | Latin is the closest of 39 languages by letter counts (4 errors at its closest window), but planted Latin comes back 6 of 6, also with 8 slips, and 7 of 8 shuffles reach the cells' best under a Latin model. [log](../logs/dagapeyeff-latin-2026-10-06.md), [log](../logs/dagapeyeff-screen-2026-10-06.md) |
| Latin under a complete 14-column transposition with a letter key | 8 of 8 planted Latin texts recovered in both directions, also classical Latin and with 8 wrong cells; the printed cells sit inside their shuffles (8 and 6 of 10 as high). [log](../logs/dagapeyeff-latin14-2026-10-06.md) |
| Catalan and Romanian under a one-to-one key, with or without the book's dummy rule and errors | Planted text comes back 3 of 3 in each, also with 8 slips; the cells sit inside their shuffles (Catalan 7 of 8; Romanian 13 of 40 after an edge at 8 shuffles vanished). [log](../logs/dagapeyeff-tongues-2026-10-06.md) |
| Latin under a repeating coordinate shift, and under four-square with standard plain squares | The shift count does not exclude Latin (1 of 9,774 draws reaches the cells), but the joint search recovers 15 of 18 planted Latin texts and the cells sit with their shuffles; four-square recovers 3 of 3 with the cells inside their shuffles. A capped homophonic key recovers only 2 of 3. [log](../logs/dagapeyeff-latinmore-2026-10-06.md) |

Generated from [`dagapeyeff-status.json`](dagapeyeff-status.json) by `tools/refresh_docs.py`.
<!-- generated-status:end -->

## What the measurements support

The scores below are frozen in the logs. None of them is a plaintext, and none of them changes the case to solved.

The two digits in a cell are not an independent pairing of the two alphabets. The mismatch score is 77.36, and 0 of 20,000 re-pairings match it. The order of either digit stream, taken alone, is ordinary. [Pairing](../logs/dagapeyeff-glue-2026-10-04.md).

Five symbols never leave the last column of the 14 by 14 grid. 0 of 20,000 shuffles match. [Column](../logs/dagapeyeff-private-2026-10-04.md).

The longest wait before a new cell is 22. 304 of 10,000 shuffles are that short, and 199 of 10,000 remain that short when the known hole is held fixed. The solved exercise is also steady: 429 of 10,000. [Introduction](../logs/dagapeyeff-intro-2026-10-04.md).

The solved exercise repeats three-cell sequences in a way the challenge does not. The exercise has 4 such sequences, and 59 of 10,000 shuffles match the two lengths together. The challenge's 5 sequences are 7,329 of 10,000. [Trigrams](../logs/dagapeyeff-trigram-2026-10-04.md).

One row of the square has counts 12, 3, 2, 1, 0. 1,432 of 100,000 re-pairings have a strict row. If a column may step, 5,768 of 100,000 do, which is not under 5 percent. [Staircase](../logs/dagapeyeff-monotone-2026-10-04.md).

Four successive counts in that row differ by one. 1,237 of 100,000 re-pairings match, and columns add none. The exercise has a straight of the same length, but 5,113 of 100,000 of its re-pairings do too, which is not under 5 percent. [Unit steps](../logs/dagapeyeff-straight-2026-10-04.md).

The main diagonal has 2 empty cells and the other diagonal has 1. 1,193 of 100,000 re-pairings have a diagonal at least that empty. The sums of the diagonals do not survive both directions: 21,907 of 100,000. The exercise has the same empty-cell counts, and 3,357 of 100,000 of its re-pairings do. [Diagonals](../logs/dagapeyeff-diagonal-2026-10-04.md).

The row digit matches the column of the grid, modulo 5, in 56 cells. That is the best of twenty alignments. 975 of 20,000 shuffles reach it, and 4,978 of 100,000 do. The same pairs scored as whole tables are ordinary: 12,780 of 20,000. A diagonal of an ordinary table is not a finding. [Modulo](../logs/dagapeyeff-modulo-2026-10-05.md).

Even positions use 13 symbols and odd positions use 18. 146 of 20,000 shuffles match that gap. The five extra symbols are the five that never leave the last column, and that column is always an odd index. Leave them out and the gap is 0. A period of 7 looks rare only until those five are left out. [Halves](../logs/dagapeyeff-halves-2026-10-05.md).

One column holds a run of three and a separate run of two of the same cell. 956 of 20,000 shuffles have such a line, just under 5 percent. Every such line already has a long run. Inside the shuffles that already have one, the rate is not under 5 percent. [Repeat](../logs/dagapeyeff-repeat-2026-10-05.md).

The five symbols that appear at most three times can be held in their seats while the other cells are shuffled. Two runs still share a starting column in 528 of 20,000 draws. A plain count of two runs does not clear. The alignment is not the rare column. [Held](../logs/dagapeyeff-held-2026-10-05.md).

Of those 528, 9 also have both runs next to a rare cell. That is 1.70 percent. The meeting was scored on the same draws and does not clear: 185 of 2,842 grids that already have a vertical run of the common cell also meet a different run. [Seats](../logs/dagapeyeff-seats-2026-10-05.md).

Of the same 528, 112 have at least one further copy of the run's cell in its row, which does not clear. 8 have two further copies. That is 1.52 percent. None of those 8 is one of the 9 that touch a rare cell. [Extras](../logs/dagapeyeff-extras-2026-10-05.md).

543 of 20,000 draws, with those rare cells held still, still have the common cell on both sides of a cell that also has a run of three. A plain gap of that shape is 7,488 of 20,000 and does not clear. 60 of the 543 also have the aligned runs, so this is not that alignment. [Held sandwich](../logs/dagapeyeff-heldsand-2026-10-05.md).

The same seats were held for the introduction wait. Counted with the rare cells, a wait of 22 is matched by 118 of 20,000 draws. Leave the rare cells out of the count and the wait is 39, matched by 19,186 of 20,000. The short wait does not survive. [Held wait](../logs/dagapeyeff-heldwait-2026-10-05.md).

Four cells, 62, 75, 82 and 85, each appear 17 times. No row holds more than 6 of them. The fullest column holds 8. Taking the more even direction, 4,643 of 100,000 scrambles are that even. The most common cell, and the four cells 64, 74, 81 and 83, are not spread in this way. [Quartet](../logs/dagapeyeff-quartet-2026-10-05.md).

Of those four, 62 has 3 copies on the even squares of the grid and 14 on the odd squares. A scramble may pick the most uneven of the four. 3.615 percent of 20,000 match that split. A straight run alternates the colors, so the runs do not cause it. [Squares](../logs/dagapeyeff-squares-2026-10-05.md).

Column 2 holds three copies of 82, at rows 0, 6 and 12, and three copies of 85, at rows 5, 8 and 11. Each triple is equally spaced, and neither is three adjacent cells. A scramble may use any row or any column, and any cells. 740 of 20,000 scrambles have such a line. [Two spaced triples](../logs/dagapeyeff-twospace-2026-10-05.md).

Row 11 holds 62 at columns 6, 8 and 10, and row 5 repeats it at columns 6 and 8. Column 2 holds 82 at rows 0, 6 and 12, and column 7 repeats it at rows 6 and 12. Neither triple is three adjacent cells. A scramble may use any cell and any row or column. 932 of 20,000 scrambles have two such echoes. [Echo](../logs/dagapeyeff-echo-2026-10-05.md).

Those two rows, 5 and 11, are also two seats of 85 in column 2, whose seats are rows 5, 8 and 11. A scramble may use any cell for either triple. 335 of 20,000 scrambles have such a pair of lines. An echo on its own is ordinary. [Ride](../logs/dagapeyeff-ride-2026-10-05.md).

Columns 6 through 10 of row 0 read 91, 64, 81, 64, 91, the same forwards and backwards. Those are the columns from the first to the last seat of 62 in row 11, at columns 6, 8 and 10. The triple is not three adjacent cells. A scramble may use any cell and any row or column. 782 of 20,000 scrambles have such a span. [Span](../logs/dagapeyeff-span-2026-10-05.md).

The cells that appear once are 04, 71 and 94, already known to share column 13. They sit at rows 6, 7 and 8, which are successive. Given the shared column, 12 of 364 choices of rows are successive. [Successive rows](../logs/dagapeyeff-successive-2026-10-05.md).

92 appears three times, 93 appears twice, and 94 appears once. On the square those three are successive in one row, so the counts read three, then two, then one. Either order, a row or a column, and a step of one or two are all counted. 18480 of 1,062,600 placements do that. [Counts](../logs/dagapeyeff-counts-2026-10-05.md).

Rows 12 and 13 hold two neighboring blocks, 85, 84 over 75, 74 and 84, 75 over 74, 85. Both are the square's 2 by 2 on row digits 7 and 8 and column digits 4 and 5. The blocks may sit anywhere. 743 of 20,000 shuffles have two or more. [Tile](../logs/dagapeyeff-tile-2026-10-05.md).

A score that clears 5 percent only before a second direction or a second measure is counted is a refusal. Sharing a property with the solved exercise, or failing to share one, is not a decryption.

## Log index

The list below is rewritten from `docs/logs/dagapeyeff*.md` on every push to main, oldest date first. It is an index, not a new measurement.

<!-- generated-logs:start -->
- [D'Agapeyeff cipher, 2026-10-02 (EDT)](../logs/dagapeyeff-2026-10-02.md)
- [Repeating shifts, and why that is not a solution](../logs/dagapeyeff-add-2026-10-04.md)
- [Three angles](../logs/dagapeyeff-angles-2026-10-04.md)
- [Autokey](../logs/dagapeyeff-autokey-2026-10-04.md)
- [The gaps survive a ball](../logs/dagapeyeff-balls-2026-10-04.md)
- [A thousand attacks](../logs/dagapeyeff-battery-2026-10-04.md)
- [The order sits in the last column](../logs/dagapeyeff-bearing-2026-10-04.md)
- [Bifid periods on the coordinate stream](../logs/dagapeyeff-bifid-2026-10-04.md)
- [Three consecutive rows](../logs/dagapeyeff-block-2026-10-04.md)
- [The book's exercise as a key](../logs/dagapeyeff-bookkey-2026-10-04.md)
- [The rare column is not a check digit](../logs/dagapeyeff-check-2026-10-04.md)
- [Affine, Beaufort, Porta](../logs/dagapeyeff-classic-swarm-2026-10-04.md)
- [Check digits, and the tall line](../logs/dagapeyeff-clerical-2026-10-04.md)
- [The window was chosen after looking](../logs/dagapeyeff-clump-2026-10-04.md)
- [Column as filler](../logs/dagapeyeff-column-null-2026-10-04.md)
- [Reading orders and dictionary shapes](../logs/dagapeyeff-columns-2026-10-04.md)
- [The published score, as a ball](../logs/dagapeyeff-convert-2026-10-04.md)
- [Delay and progressive shift](../logs/dagapeyeff-delay-2026-10-04.md)
- [Three moves are not enough](../logs/dagapeyeff-depth3-2026-10-04.md)
- [The fourth move, from the best three](../logs/dagapeyeff-depth4-2026-10-04.md)
- [Empty cells on the diagonals](../logs/dagapeyeff-diagonal-2026-10-04.md)
- [Digit routes](../logs/dagapeyeff-digit-routes-2026-10-04.md)
- [Repeated digraphs](../logs/dagapeyeff-digraph-2026-10-04.md)
- [At least three count-moves](../logs/dagapeyeff-edits-2026-10-04.md)
- [No language assumed](../logs/dagapeyeff-frames-2026-10-04.md)
- [The glue is real. The order is not.](../logs/dagapeyeff-glue-2026-10-04.md)
- [Printed groups](../logs/dagapeyeff-groups-2026-10-04.md)
- [The frequency hole, and a period that is not there](../logs/dagapeyeff-hole-2026-10-04.md)
- [The wait for a new cell](../logs/dagapeyeff-intro-2026-10-04.md)
- [The order is on the last column's joins](../logs/dagapeyeff-joins-2026-10-04.md)
- [Column orders of the regrouped cells](../logs/dagapeyeff-keys-2026-10-04.md)
- [Column as a key](../logs/dagapeyeff-keystream-2026-10-04.md)
- [What if it is not English](../logs/dagapeyeff-languages-2026-10-04.md)
- [Large swarm](../logs/dagapeyeff-large-swarm-2026-10-04.md)
- [Alexander d'Agapeyeff, the man, 4 October 2026](../logs/dagapeyeff-life-2026-10-04.md)
- [Which measurements can see this cipher](../logs/dagapeyeff-methods-2026-10-04.md)
- [The language model does not like the flattering counts](../logs/dagapeyeff-model-2026-10-04.md)
- [One row steps down](../logs/dagapeyeff-monotone-2026-10-04.md)
- [Why a substitution of these cells is not a reading](../logs/dagapeyeff-order-2026-10-04.md)
- [What others found, and what the digits do with it](../logs/dagapeyeff-others-2026-10-04.md)
- [Count each pair once](../logs/dagapeyeff-outgoing-2026-10-04.md)
- [Dictionary shapes](../logs/dagapeyeff-patterns-2026-10-04.md)
- [Every period-4 shift](../logs/dagapeyeff-period4-2026-10-04.md)
- [The edits, put back on the cells](../logs/dagapeyeff-placed-2026-10-04.md)
- [One digit place](../logs/dagapeyeff-places-2026-10-04.md)
- [Five symbols never leave the last column](../logs/dagapeyeff-private-2026-10-04.md)
- [Hashes for the cells and the scores](../logs/dagapeyeff-provenance-2026-10-04.md)
- [Column keys and digit reads](../logs/dagapeyeff-reads-2026-10-04.md)
- [How far from the published score](../logs/dagapeyeff-record-2026-10-04.md)
- [Refined swarm](../logs/dagapeyeff-refined-2026-10-04.md)
- [The flattering regrouping](../logs/dagapeyeff-regroup-2026-10-04.md)
- [The repairs share one loss](../logs/dagapeyeff-repair-2026-10-04.md)
- [Router and grid](../logs/dagapeyeff-router-swarm-2026-10-04.md)
- [Rails, diagonals, and the every-other-cell trap](../logs/dagapeyeff-routes-2026-10-04.md)
- [Running keys from texts already in the repo](../logs/dagapeyeff-running-2026-10-04.md)
- [Solver swarm](../logs/dagapeyeff-solver-swarm-2026-10-04.md)
- [The solver now refuses a flat order](../logs/dagapeyeff-split-2026-10-04.md)
- [Counts that differ by one](../logs/dagapeyeff-straight-2026-10-04.md)
- [The private symbols are not filler](../logs/dagapeyeff-strip-2026-10-04.md)
- [D'Agapeyeff swarm, 4 October 2026](../logs/dagapeyeff-swarm-2026-10-04.md)
- [One cell repeating is not the column](../logs/dagapeyeff-symbols-2026-10-04.md)
- [Three cells in a row](../logs/dagapeyeff-trigram-2026-10-04.md)
- [The other legal column width](../logs/dagapeyeff-widths-2026-10-04.md)
- [The best word score, not the friendliest counts](../logs/dagapeyeff-word-2026-10-04.md)
- [The score a reading has to beat](../logs/dagapeyeff-yardstick-2026-10-04.md)
- [A longer swarm on the cells, 5 October 2026](../logs/dagapeyeff-anneal-2026-10-05.md)
- [Seven cells of the square are empty](../logs/dagapeyeff-blank-2026-10-05.md)
- [The 13 common symbols look uniform, 5 October 2026](../logs/dagapeyeff-body-2026-10-05.md)
- [The book's own square on the cells, 5 October 2026](../logs/dagapeyeff-booksquare-2026-10-05.md)
- [Columnar transposition under a letter key, 5 October 2026](../logs/dagapeyeff-columnar-2026-10-05.md)
- [The aligned runs sit next to rare cells](../logs/dagapeyeff-contact-2026-10-05.md)
- [Real prose windows against the cells' counts, 5 October 2026](../logs/dagapeyeff-corpus-2026-10-05.md)
- [Rare counts sit in order on the square](../logs/dagapeyeff-counts-2026-10-05.md)
- [Every double transposition up to width 6, any language, 5 October 2026](../logs/dagapeyeff-double-2026-10-05.md)
- [A spaced triple is echoed](../logs/dagapeyeff-echo-2026-10-05.md)
- [Every column order up to width 9, any language, 5 October 2026](../logs/dagapeyeff-exhaustive-2026-10-05.md)
- [Two copies outside the runs](../logs/dagapeyeff-extras-2026-10-05.md)
- [A turning grille on the cells, 5 October 2026](../logs/dagapeyeff-grille-2026-10-05.md)
- [Even and odd are the private column](../logs/dagapeyeff-halves-2026-10-05.md)
- [A full row with an empty cell](../logs/dagapeyeff-heavy-2026-10-05.md)
- [The alignment is not the rare column](../logs/dagapeyeff-held-2026-10-05.md)
- [The sandwich is not the plain gap](../logs/dagapeyeff-heldsand-2026-10-05.md)
- [The short wait needs the rare cells](../logs/dagapeyeff-heldwait-2026-10-05.md)
- [A keyword dictionary attack on the book's transpositions, 5 October 2026](../logs/dagapeyeff-keywords-2026-10-05.md)
- [The common cell meets the run of 63](../logs/dagapeyeff-meeting-2026-10-05.md)
- [The row digit does not track the column](../logs/dagapeyeff-modulo-2026-10-05.md)
- [The aligned runs are not the only copies in their rows](../logs/dagapeyeff-outside-2026-10-05.md)
- [What others have tried on the 1939 challenge, and how close anyone is](../logs/dagapeyeff-prior-work-2026-10-05.md)
- [Four cells share a count](../logs/dagapeyeff-quartet-2026-10-05.md)
- [The second run needs the long run](../logs/dagapeyeff-repeat-2026-10-05.md)
- [The order left after the rare column](../logs/dagapeyeff-residual-2026-10-05.md)
- [The mismatch is not one cell](../logs/dagapeyeff-rest-2026-10-05.md)
- [An echo rides on a spaced triple](../logs/dagapeyeff-ride-2026-10-05.md)
- [63 sits between two copies of 81](../logs/dagapeyeff-sandwich-2026-10-05.md)
- [The runs still touch the rare seats](../logs/dagapeyeff-seats-2026-10-05.md)
- [The sharpest cell](../logs/dagapeyeff-sharp-2026-10-05.md)
- [A palindrome fills a spaced span](../logs/dagapeyeff-span-2026-10-05.md)
- [Spirals, snakes and zigzags on the cells, 5 October 2026](../logs/dagapeyeff-spiral-2026-10-05.md)
- [The exercise has an uneven line](../logs/dagapeyeff-spread-2026-10-05.md)
- [One tied cell prefers one color](../logs/dagapeyeff-squares-2026-10-05.md)
- [Three successive rows in the private column](../logs/dagapeyeff-successive-2026-10-05.md)
- [Two blocks copy a square](../logs/dagapeyeff-tile-2026-10-05.md)
- [The two runs of three share a column](../logs/dagapeyeff-triples-2026-10-05.md)
- [Two spaced triples share a column](../logs/dagapeyeff-twospace-2026-10-05.md)
- [A repeating shift on a keyed square, 6 October 2026](../logs/dagapeyeff-additive-2026-10-06.md)
- [Width-14 columnar with a letter key, compiled, 6 October 2026](../logs/dagapeyeff-columnar14c-2026-10-06.md)
- [Digit ciphers other than Polybius pairs, 6 October 2026](../logs/dagapeyeff-digitcodes-2026-10-06.md)
- [A direction swarm: the old leads rerun, 6 October 2026](../logs/dagapeyeff-direction-2026-10-06.md)
- [Enciphering errors cannot hide English under a one-to-one key, 6 October 2026](../logs/dagapeyeff-errors-2026-10-06.md)
- [Four-square on the cells, 6 October 2026](../logs/dagapeyeff-foursquare-2026-10-06.md)
- [A compiled turning-grille search: power only, 6 October 2026](../logs/dagapeyeff-grillec-2026-10-06.md)
- [A homophonic key under any transposition, 6 October 2026](../logs/dagapeyeff-homgroup-2026-10-06.md)
- [A many-to-one key, 6 October 2026](../logs/dagapeyeff-homophone-2026-10-06.md)
- [Italian under a one-to-one key, with errors, 6 October 2026](../logs/dagapeyeff-italian-2026-10-06.md)
- [Keyed four-square and two-square: power only, 6 October 2026](../logs/dagapeyeff-keyedsquares-2026-10-06.md)
- [Latin under a one-to-one key, 6 October 2026](../logs/dagapeyeff-latin-2026-10-06.md)
- [Latin under a 14-column transposition, 6 October 2026](../logs/dagapeyeff-latin14-2026-10-06.md)
- [Latin under a repeating shift, a homophonic key and four-square, 6 October 2026](../logs/dagapeyeff-latinmore-2026-10-06.md)
- [Ciphers that mix letters, 6 October 2026](../logs/dagapeyeff-mixing-2026-10-06.md)
- [Starting from no message, 6 October 2026](../logs/dagapeyeff-nomessage-2026-10-06.md)
- [Different pairs under any one-to-one pair cipher, 6 October 2026](../logs/dagapeyeff-pairmap-2026-10-06.md)
- [Periodic independent alphabets, 6 October 2026](../logs/dagapeyeff-phases-2026-10-06.md)
- [Five short attacks, 6 October 2026](../logs/dagapeyeff-quick-2026-10-06.md)
- [Which languages could give the cells' letter counts, 6 October 2026](../logs/dagapeyeff-screen-2026-10-06.md)
- [Catalan and Romanian under a keyed square, 6 October 2026](../logs/dagapeyeff-tongues-2026-10-06.md)
<!-- generated-logs:end -->

## Next steps

<!-- generated-next:start -->
Open families, in the order they are planned:

1. **A plaintext in another language under a large transposition, or in a language not screened.** Search Catalan, Romanian and Latin under a 14-column key and under keyed four-square once a method with power exists; screen further languages.
2. **14 by 14 turning grille with a letter key.** A joint method that recovers planted grilles with the key unknown, before the cells are searched; the count-flattening key left to test is a pair code or keyed squares, since a homophonic key is excluded by counts.
3. **No message (a hand construction).** Find an order statistic that separates a turning-grille message from a no-message dealing at 196 letters, with planted texts, since the grille is the main message system the order still allows.
4. **A general pair table (2 by 2 Hill, any 625-pair code).** Search 2 by 2 Hill over a keyed square with planted texts.
5. **Transposition beyond the searched widths, or with nulls and an incomplete rectangle.** A joint search with a letter key, as for width 14, at widths 11 to 13 and for double transposition above width 6.
6. **Four-square with keyed plain squares, and two-square.** A search with power for keyed squares at 196 letters, for example fixing the Polybius labelling from the cells' structure or using a stronger model, before the cells are searched.

Generated from [`dagapeyeff-status.json`](dagapeyeff-status.json) by `tools/refresh_docs.py`.
<!-- generated-next:end -->
