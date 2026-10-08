# Changes between drafts

## Second seeds, fourth reading, 7 October 2026

- U2 is closed. The shift at periods 6 and 8 to 13 and the five Latin searches were rerun under a second seed, joining four-square and the shift at periods 2 to 14. A new Table 2 gives both runs of all nine rows; Section 4's "A second seed" now reports them all, including the two weaker second-seed rows (the English shift at periods 6 and 8 to 13 closes by 0.75; Latin four-square recovers 2 of 3).
- The fourth reading (`review-4.md`): 13 findings, all verified and fixed. The Conclusion limits its English claim to one-to-one keys, keeps the "chosen errors" qualifier, gives the second-seed floor and the homophonic 0.88 separately, and moves the language claim into the interpretation, scoped to a one-to-one key, with Latin singled out and its daughter languages not. The abstract follows; its Latin range is now 0.45 to 0.97 in 5 of 6 Latin rows. Romanian is placed correctly (14th, not in Table 3). Figure 3 marks recovered and unrecovered texts; Figure 2 names its off-scale outlier.
- `build.sh` dates the PDF by the last commit to the paper's source, not counting the PDF.

## Conclusion, figures and layout, 7 October 2026

- A Conclusion (Section 8) states the owner's answer and bounds it. Two statements are results: the cells are not ordinary English under any one-to-one key, with or without a transposition, and Latin is the closest of the 98 languages screened, with Catalan, Old Occitan and Spanish, which descend from it, among the twelve closest. The third is labelled an interpretation: the challenge most likely carries no message. The challenge's omission from the editions of 1952 onward and the unsourced report that its author forgot the method are mentioned and given no weight, because they fit a lost key equally well.
- The abstract ends with the same reading in one sentence, labelled an interpretation, and is set in five paragraphs instead of one block; the README abstract, and so the Zenodo description, keep the paragraphs.
- Three figures, written by `code/make_numbers.py` from the frozen results like the tables, so `--check` covers them and LaTeX (pgfplots) draws them: Figure 1, the two scores of each row of Table 1; Figure 2, the median-window errors of all 98 screened languages; Figure 3, Latin word coverage of the planted texts by wrong cells against the cells' and shuffles' best.
- The title breaks at its phrases, so no word stands alone on a line. The date line reads 7 October 2026.

## Latin at small widths and the last column, 7 October 2026

- Latin under a turning grille (`engine.dagapeyeff_latingrille`) and under double transposition (`engine.dagapeyeff_latindouble`), Section 7, power only: the grille needs a key about 80 percent right; the double-transposition joint search has power only to 5 by 7.
- Latin words in the cells' best decryptions (`engine.dagapeyeff_latinwords`), Section 6, "Latin words": planted Latin with up to 32 wrong cells keeps more words than the cells (59 of 60), and the cells' best coverage is what shuffles reach.
- Latin under columnar transposition at widths 2 to 9 (`engine.dagapeyeff_latinsmall`): 48 of 48 planted Latin texts recovered, the cells' best -3.93 against the weakest recovered planted text at -2.96. Table 1 gains a row; the abstract, Section 6 and Section 7 now say Latin is closed at widths 2 to 15.
- The five last-column symbols (`engine.dagapeyeff_rarecolumn`), Section 3: as padding, the other 188 cells use 13 letters, fewer than any window of Latin or English; as real rare letters, they would have to cluster in one 14-letter stretch, which no window does.

## Preprint text, 7 October 2026

- The third reading (`review-3.md`): ten findings, all fixed. The language screen now accounts for the two treebanks too short to count; the abstract no longer says Latin is closest on every measure; Russian and Esperanto are sourced; "the author" no longer reads as d'Agapeyeff; the draft history is out of Section 4; sources are described by how they were read.
- A second seed for four-square and the repeating shift at periods 2 to 14 (Section 4, "A second seed").
- The companion repository is ChaseHendrick/dagapeyeff, defined in Section 9 with the development repository; data availability, funding, Use of AI and rights statements added; the date line reads "Preprint".
- The digit block was checked against two other public transcriptions.

## Draft 2, 6 October 2026

New results, each a frozen probe with a test and a dated log in `docs/logs/`:

- **Every language in Universal Dependencies** (`engine.dagapeyeff_alllanguages`): 98 languages with usable text, non-Latin alphabets romanized. Latin has the lowest median distance to the cells' counts of all and three times the next rate of close windows; Estonian matches only its single closest window. Table 2 now lists the twelve closest of the 98.
- **Russian under four transliterations** (`engine.dagapeyeff_russian`) and **Esperanto** (`engine.dagapeyeff_esperanto`): neither comes closer than English.
- **Latin at length** (`engine.dagapeyeff_latinlib`, `engine.dagapeyeff_latinlibrary`): every window of 59.8 million letters, The Latin Library included; none comes within 2 errors, the closest needs 3.
- **Latin under columnar transposition at widths 10 to 13 and 15** (`engine.dagapeyeff_latinw`): 39 of 40 planted Latin texts recovered; the cells score below them and inside their shuffles.
- **The repeating shift at periods 6 and 8 to 13**, English and Latin (`engine.dagapeyeff_shiftgap`), which draft 1 had wrongly included in "periods 2 to 14".

Corrections from the second reading, all seventeen findings of `review-2.md`: the shift periods; the no-message wording and its systems; counts against chance in place of "all but two comparisons"; the gaps under one nat named as weaker closures; the Romanian rerun; the Latin width-14 regrouping; the no-message caption; credit to Melichar, Gariazzo and the reader behind Pelling's Kerckhoffs finding; Proposition 1 labelled standard; small-width power limited to English and German; the 363 transforms described as the author's own; Pelling's 2014 post for the last column; the breakdown of the eight readings; the ADFGX blog as a proposal; the Ashley sentence; two confirmed titles; the novelty bound.

## Draft 1, 6 October 2026

First complete manuscript, with the proofs reading of `review-1.md` applied.
