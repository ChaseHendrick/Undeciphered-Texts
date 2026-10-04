# Truppenschlüssel pair climbs, 4 October 2026

Not solved. No plaintext is stored. No key is claimed.

The previous note measured three pairs and did not search a square. This pass runs a local two-square climb on the windows whose lengths are even. A dropped endpoint is the same rule used for the odd Hill windows: one letter is removed, nothing is invented. The designator-included IASRZ strings are already even, so that window drops nothing.

The scorer is trigram counts from the Grimm excerpt in `engine/data/german_excerpt.txt`. It is not a military language model. Each window is climbed for 4 restarts and 6 kicks, seed 20261004, then climbed again on a shuffle of the same letters. Both halves stay even, so a bigram does not cross the join. One trigram at the join does.

| Window | Lengths | Real score | Shuffled score |
| --- | ---: | ---: | ---: |
| IASRZ, designator included | 90 + 52 | 362 | 332 |
| IASRZ, drop the first body letter | 84 + 46 | 448 | 324 |
| IASRZ, drop the last body letter | 84 + 46 | 414 | 382 |
| SSKFV plus HOHOX, drop HOHOX's first letter | 60 + 54 | 379 | 278 |
| SSKFV plus HOHOX, drop HOHOX's last letter | 60 + 54 | 304 | 292 |
| 1735 pair, drop the first body letter | 56 + 52 | 559 | 415 |
| 1735 pair, drop the last body letter | 56 + 52 | 578 | 355 |

All seven real scores are higher than their shuffle. That does not choose a window. Dropping the first letter and dropping the last letter cannot both be the transmitted text, and both beat the shuffle. The pairs are more repetitive than a shuffle, which the alignment note already showed, and this scorer follows that repetition. It does not identify a square.

`solved` stays false and `claimed_plaintext` stays null.
