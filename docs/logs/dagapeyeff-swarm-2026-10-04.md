# D'Agapeyeff swarm, 4 October 2026

Not solved. This is not Kryptos and not a German army message.

The target is the challenge on the last page of Alexander D'Agapeyeff's *Codes and Ciphers* (first edition, 1939). He dropped it from later editions and said he could no longer read it. The digits used here are the block printed on the Wikipedia transcription of that page.

It is the closest non-German, non-K4 item in the usual short list because the first layer is already identified. After the terminal `000`, there are 196 pairs. Every first digit is in `6 7 8 9 0` and every second digit is in `1 2 3 4 5`. That is the 5 by 5 square his own book teaches. The 196 cells fill a 14 by 14 grid. Only 18 of the 25 cells are used.

The swarm then asks whether those cells can be English. Letter counts do not care about column order, so the best assignment of cells to letters is the whole test. Matched against the repo's published English rates, with I and J added together, the challenge scores 34.23. The Polybius exercise printed earlier in the same book, whose plaintext is already public, scores 4.14 under the same rule. The challenge is the worse of the two.

Adjacent cells repeat 65 times. Two hundred shuffles of the same cells, seed 20261004, average 67.84. The challenge sits 0.74 standard deviations below that mean, not above it.

A transposition of a single Polybius reading cannot cross this gap. A second cipher on top, or a mistake in the encipherment, is not ruled out. No plaintext is stored. A hill-climb that spells a few words in some language is not a confirmation, and none was run.
