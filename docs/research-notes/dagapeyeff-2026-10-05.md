# D'Agapeyeff challenge: measured structure, not a reading

<!--
index-id: dagapeyeff
index-title: D'Agapeyeff challenge
index-problem: 1939 digit challenge with no public reading; measured structure is not a plaintext
index-data: Wikipedia digit block used by the engine, plus the solved exercise as the control
index-next: Record a predeclared comparison only when it stays under 5 percent after its widening
-->

Source check: **2026-10-05**. Category: historical cipher. No reading is claimed.

The public digit block is the one on the English Wikipedia page for the D'Agapeyeff cipher. That page was fetched on 2026-10-02. It attributes the challenge to Alexander D'Agapeyeff, *Codes and Ciphers* (Oxford University Press, 1939), page 158, and says later editions dropped it. This note did not re-inspect the 1939 book. The engine uses that digit block. The solved Polybius exercise from the same page is the control, not a crib for the challenge. [Wikipedia](https://en.wikipedia.org/wiki/D%27Agapeyeff_cipher). [First inspection](../logs/dagapeyeff-2026-10-02.md).

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
- [The aligned runs sit next to rare cells](../logs/dagapeyeff-contact-2026-10-05.md)
- [A spaced triple is echoed](../logs/dagapeyeff-echo-2026-10-05.md)
- [Two copies outside the runs](../logs/dagapeyeff-extras-2026-10-05.md)
- [Even and odd are the private column](../logs/dagapeyeff-halves-2026-10-05.md)
- [A full row with an empty cell](../logs/dagapeyeff-heavy-2026-10-05.md)
- [The alignment is not the rare column](../logs/dagapeyeff-held-2026-10-05.md)
- [The sandwich is not the plain gap](../logs/dagapeyeff-heldsand-2026-10-05.md)
- [The short wait needs the rare cells](../logs/dagapeyeff-heldwait-2026-10-05.md)
- [The common cell meets the run of 63](../logs/dagapeyeff-meeting-2026-10-05.md)
- [The row digit does not track the column](../logs/dagapeyeff-modulo-2026-10-05.md)
- [The aligned runs are not the only copies in their rows](../logs/dagapeyeff-outside-2026-10-05.md)
- [Four cells share a count](../logs/dagapeyeff-quartet-2026-10-05.md)
- [The second run needs the long run](../logs/dagapeyeff-repeat-2026-10-05.md)
- [The order left after the rare column](../logs/dagapeyeff-residual-2026-10-05.md)
- [The mismatch is not one cell](../logs/dagapeyeff-rest-2026-10-05.md)
- [63 sits between two copies of 81](../logs/dagapeyeff-sandwich-2026-10-05.md)
- [The runs still touch the rare seats](../logs/dagapeyeff-seats-2026-10-05.md)
- [The sharpest cell](../logs/dagapeyeff-sharp-2026-10-05.md)
- [The exercise has an uneven line](../logs/dagapeyeff-spread-2026-10-05.md)
- [One tied cell prefers one color](../logs/dagapeyeff-squares-2026-10-05.md)
- [The two runs of three share a column](../logs/dagapeyeff-triples-2026-10-05.md)
- [Two spaced triples share a column](../logs/dagapeyeff-twospace-2026-10-05.md)
<!-- generated-logs:end -->

## Proposed next comparison

Do not record the four corners of the square as a new result. Those corners are the ends of the two diagonals already counted. A later comparison needs its own predeclared statistic, a widening written down before the count, and the solved exercise scored the same way.
