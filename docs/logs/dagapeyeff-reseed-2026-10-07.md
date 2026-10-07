# Four-square and the repeating shift under a second seed, 7 October 2026

Not a reading. No letter string is stored.

The paper's quality record (U2) asked for the four-square, repeating-shift and Latin searches to be run again under a second seed. `engine.dagapeyeff_reseed` calls each probe's own report function with its seed raised by 7,000,001, so every planted text, key, shuffle and search start is drawn afresh; the programs, budgets and recovery thresholds are unchanged. Only two probes finished before the session ended. Both agree with their first runs.

| Search | Seed | Planted recovered | Weakest recovered planted | Cells' best | Gap | Shuffle searches as high |
| --- | --- | --- | --- | --- | --- | --- |
| Four-square, standard plain squares (`dagapeyeff-foursquare`) | first | 4 of 6 | -1.9603 | -3.3427 | 1.38 | 58 of 80 |
| | second | 6 of 6 | -1.9929 | -3.3727 | 1.38 | 36 of 80 |
| Repeating shift, periods 2, 3, 4, 5, 7, 14 (`dagapeyeff-additive`) | first | 11 of 12 | -2.0789 | -3.3261 | 1.25 | 34 of 72 |
| | second | 11 of 12 | -2.4637 | -3.4080 | 0.94 | 37 of 72 |

Scores are quadgram log probabilities per letter in nats. The gap is the weakest recovered planted text's found score minus the cells' best over the printed cells and the regrouping. The shift's gap falls under one nat in the second run because a weaker planted window was drawn (its found score is -2.46), not because the cells rose.

Not yet rerun, listed in `PENDING` in the module: the shift at periods 6 and 8 to 13 (`shiftgap`), Latin at width 14 (`latin14`), Latin at widths 10 to 15 (`latinw`), Latin four-square and the capped homophonic key (`latinmore`), and the Latin shift (`latinshift`). Estimated at about two and a half hours on four cores in all, `latinw` most of it.

`engine.dagapeyeff_latinsmall` (Latin joint search at widths 2 to 9, both directions, a quarter of the wide-key budget) was written in the same session and not yet run. In a scratch check it recovered planted Latin at widths 3 and 8 with every cell right, about 10 seconds a search.

Not a reading. No letter string is stored.
