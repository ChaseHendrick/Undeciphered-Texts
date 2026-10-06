# Latin under a repeating shift, a homophonic key and four-square, 6 October 2026

Not a reading. No letter string is stored.

Latin is the closest language to the cells' letter counts and is already closed under a keyed square and a 14-column key ([Latin](dagapeyeff-latin-2026-10-06.md), [width 14](dagapeyeff-latin14-2026-10-06.md)). `engine.dagapeyeff_latinmore` runs three more families under the same Latin quadgram model, with planted held-out Latin (the Thomistic tail and classical Latin) for power.

**The repeating-shift count does not exclude Latin.** The count that excludes English ([additive](dagapeyeff-additive-2026-10-06.md)) was repeated with held-out Latin windows under random squares and shift keys, 9,774 draws in all. Latin uses few letters, so draws reach as few as 16 different symbols, and 1 draw (a column shift of period 2) matches the cells' 18 symbols with 177 cells in the three busiest rows. So `latinshift_report` searches it: the square and the shifts annealed together under the Latin model at periods 2, 3, 4, 5, 7 and 14, shifting both coordinates, the column only or the row only, 4 restarts of 4,000,000 steps. Planted Latin came back 15 of 18 times; the three misses (both coordinates at periods 4 and 7, rows at period 4) are search failures, where the found key scores far below the true one. On the cells and the regrouping, in 36 cases with 3 shuffles each, the best is -3.9855 (the cells, both coordinates, period 14), with 1 of 3 shuffles as high. In 5 of the 36 cases the cells beat all three shuffles, where chance alone gives about 9.

**A homophonic key** capped at 42 places a letter, the most one letter takes in a 196-letter window of held-out Latin: planted Latin homophonic texts came back 2 of 3 (the third at 23 percent). The cells score -2.9825 with 6 of 8 shuffles as high, the regrouping -2.743 with 5 of 8. Power here is partial.

**Four-square with standard plain squares**: planted Latin came back 3 of 3. The cells score -4.1002 with 7 of 8 shuffles as high, the regrouping -3.9372 with 3 of 8.

Latin under a repeating coordinate shift and under four-square with standard plain squares does not read the cells. The homophonic result is weaker, with 2 of 3 planted texts recovered.

Not a reading. No letter string is stored.
