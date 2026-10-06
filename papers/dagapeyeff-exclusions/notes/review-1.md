# Review 1: adversarial second reading, 6 October 2026

Scope: an independent in-project reader was given the manuscript, `numbers.tex`, the tables, `make_numbers.py`, the frozen results and the probe code, with the instruction to find errors in the proofs and in how the propositions are applied. Four reading lenses were planned (proofs, numbers, controls, claims); only the proofs lens completed before the session's usage limit, and its verification pass did not run. Every finding below was then checked by the author against the source before it was fixed; finding 1 was reproduced by a new frozen probe. This is an in-project review, not outside or journal peer review.

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Major | The abstract and Section 3 said four-square side counts are fixed by the plaintext alone. Proposition 3 removes only the cipher squares; the counts depend on the plain squares. With chosen plain squares held-out English reaches the cells' side counts. | Confirmed: `engine.dagapeyeff_fskeyed` reaches 13 and 18 in 15 of 15 held-out windows. Abstract, Sections 1, 3, 4, 6 and 7 corrected. The status ledger splits the family: four-square with standard plain squares stays closed; keyed four-square and two-square are open. The four-square note carries a correction. |
| 2 | Major | Two-square was said to inherit Proposition 3, but its cipher squares are its plain squares, so nothing drops out; and the search used standard plain squares only. | Confirmed and corrected with finding 1. |
| 3 | Major | The small-width paragraph printed bounds that do not separate across cases (planted at least 0.0345, cells at most 0.0698), compared planted texts with one shuffle and the cells with three, and said the result holds for any language. | Confirmed. The text now says the separation holds case by case, names the unequal shuffle counts, calls width 9 weak, and says the score is key-invariant with power shown for English and German. |
| 4 | Minor | Proposition 2 counts substitutions, while most of the book's faults are omissions. | Corrected: one sentence shows that a window of the intended passage differs from the surviving text by at most d + k substitutions, so the bound still applies. |
| 5 | Minor | The rare symbols as spaces give 8 words, not 9: the last cell is a rare symbol. | Corrected: 8 words, 23.5 letters a word, now computed from the cells in `make_numbers.py`. |
| 6 | Minor | Table 1's "Cells' best" takes the best over the printed cells and the regrouping together. | Corrected in the caption. |
| 7 | Minor | Five reorderings of each group of five keep all pairs on the square; the regrouping is the only one that also keeps the filler last. | Corrected in Section 2. |
| 8 | Minor | The abstract said the cells score like their shuffles in every case, but two comparisons (the short battery's best variant and the period-14 shift with 3 shuffles) put the cells above their shuffles. | Corrected: the abstract now says in all but two comparisons, which the text discusses. |

Remaining: the numbers, controls and claims lenses were not read independently.
