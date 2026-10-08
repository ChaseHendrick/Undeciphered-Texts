# Four-square, the repeating shift and the Latin searches under a second seed, 7 October 2026

Not a reading. No letter string is stored.

The paper's quality record (U2) asked for the four-square, repeating-shift and Latin searches to be run again under a second seed. `engine.dagapeyeff_reseed` calls each probe's own report function with its seed raised by 7,000,001, so every planted text, key, shuffle and search start is drawn afresh; the programs, budgets and recovery thresholds are unchanged. Two probes finished first; the other five followed the same day. All agree with their first runs.

| Search | Seed | Planted recovered | Weakest recovered planted | Cells' best | Gap | Shuffle searches as high |
| --- | --- | --- | --- | --- | --- | --- |
| Four-square, standard plain squares | first (20261006) | 4 of 6 | -1.9603 | -3.3427 | 1.38 | 58 of 80 |
|  | second (27261007) | 6 of 6 | -1.9929 | -3.3727 | 1.38 | 36 of 80 |
| Repeating shift, periods 2, 3, 4, 5, 7, 14 | first (20261006) | 11 of 12 | -2.0789 | -3.3261 | 1.25 | 34 of 72 |
|  | second (27261007) | 11 of 12 | -2.4637 | -3.4080 | 0.94 | 37 of 72 |
| Repeating shift, periods 6, 8 to 13 | first (20261021) | 26 of 28 | -2.1614 | -3.3917 | 1.23 | 42 of 87 |
|  | second (27261022) | 25 of 28 | -2.6208 | -3.3664 | 0.75 | 35 of 87 |
| Latin, repeating shift, periods 6, 8 to 13 | first (20261021) | 25 of 28 | -2.7836 | -4.0202 | 1.24 | 45 of 87 |
|  | second (27261022) | 23 of 28 | -2.7527 | -4.0078 | 1.26 | 40 of 87 |
| Latin, columnar width 14 | first (20261014) | 8 of 8 | -3.2581 | -3.7074 | 0.45 | 16 of 40 |
|  | second (27261015) | 8 of 8 | -3.2217 | -3.7315 | 0.51 | 19 of 40 |
| Latin, columnar widths 10 to 13 and 15 | first (20261020) | 39 of 40 | -2.9462 | -3.5746 | 0.63 | 117 of 200 |
|  | second (27261021) | 38 of 40 | -2.8506 | -3.6042 | 0.75 | 114 of 200 |
| Latin, four-square | first (20261017) | 3 of 3 | -3.2681 | -3.9372 | 0.67 | 10 of 16 |
|  | second (27261018) | 2 of 3 | -2.4542 | -3.9596 | 1.51 | 13 of 16 |
| Latin, capped homophonic key | first (20261017) | 2 of 3 | -1.7716 | -2.7430 | 0.97 | 11 of 16 |
|  | second (27261018) | 2 of 3 | -1.8489 | -2.7375 | 0.89 | 12 of 16 |
| Latin, repeating shift, periods 2, 3, 4, 5, 7, 14 | first (20261017) | 15 of 18 | -2.7261 | -3.9855 | 1.26 | 66 of 111 |
|  | second (27261018) | 16 of 18 | -3.0690 | -4.0353 | 0.97 | 57 of 111 |

Scores are quadgram log probabilities per letter in nats. The gap is the weakest recovered planted text's found score minus the cells' best over the printed cells and the regrouping. The shift's gap falls under one nat in the second run because a weaker planted window was drawn (its found score is -2.46), not because the cells rose.

The shift at periods 6 and 8 to 13 (`shiftgap`, English and Latin), Latin at width 14 (`latin14`), Latin at widths 10 to 15 (`latinw`), Latin four-square with the capped homophonic key (`latinmore`) and the Latin shift (`latinshift`) followed later on 7 October, about two hours on four cores, `latinw` most of it (55 minutes). The table above has all nine rows. `PENDING` is empty. The five new rows were appended to the frozen file by the module's own `summarise`; the four-square and shift rows frozen earlier are unchanged byte for byte, because their raw second runs were not kept and rerunning them would only repeat the result.

All nine rows agree with their first runs: under both seeds the cells stay below the weakest recovered planted text, and recovery differs by at most two planted texts. Two second-seed rows are weaker than their first runs. The English shift at periods 6 and 8 to 13 closes by 0.75, because a weaker planted window was drawn (found at -2.62); the cells' best is -3.37, against -3.39 at the first seed. Latin four-square recovers 2 of 3. The latinmore and latinshift reports share a module seed (`latinshift` draws from it plus 1 in both runs), so the table gives both the same seed number.

`engine.dagapeyeff_latinsmall` (Latin joint search at widths 2 to 9, both directions, a quarter of the wide-key budget) was written in the same session and not yet run. In a scratch check it recovered planted Latin at widths 3 and 8 with every cell right, about 10 seconds a search.

Not a reading. No letter string is stored.
