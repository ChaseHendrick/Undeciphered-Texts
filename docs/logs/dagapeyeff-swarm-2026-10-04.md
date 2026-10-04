# D'Agapeyeff swarm, 4 October 2026

Not solved. This is not Kryptos and not a German army message.

The target is the challenge on the last page of Alexander D'Agapeyeff's *Codes and Ciphers* (first edition, 1939). He dropped it from later editions and said he could no longer read it. The digits used here are the block printed on the Wikipedia transcription of that page.

It is the closest non-German, non-K4 item in the usual short list because the first layer is already identified. After the terminal `000`, there are 196 pairs. Every first digit is in `6 7 8 9 0` and every second digit is in `1 2 3 4 5`. That is the 5 by 5 square his own book teaches. The 196 cells fill a 14 by 14 grid. Only 18 of the 25 cells are used.

The swarm then asks whether those cells can be English. Letter counts do not care about column order, so the best assignment of cells to letters is the whole test. Matched against the repo's published English rates, with I and J added together, the challenge scores 34.23. The Polybius exercise printed earlier in the same book, whose plaintext is already public, scores 4.14 under the same rule. The challenge is the worse of the two.

Adjacent cells repeat 65 times. Two hundred shuffles of the same cells, seed 20261004, average 67.84. The challenge sits 0.74 standard deviations below that mean, not above it.

A transposition of a single Polybius reading cannot cross this gap. A second cipher on top, or a mistake in the encipherment, is not ruled out. No plaintext is stored. A hill-climb that spells a few words in some language is not a confirmation, and none was run.

## Same length, then repairs

The book's example is 89 cells. Chi-square grows with length, so 4.14 against 34.23 was only a direction. The comparison that counts is 2,000 strings of 196 letters drawn from the same English rates, seed 20261004.

None of those 2,000 scored 34.23 or worse. The worst of them scored 24.17. Their median was 7.44. None used 18 or fewer distinct letters. The narrowest used 19.

Changing one cell, whichever change improves the count the most, only moves the challenge from 34.23 to 30.65. It takes 4 such changes to get inside the worst English draw, and 14 to reach the median. Those changed cells are not kept. Four slips is not the one mistake a tired author makes, and a count that has been edited until it looks English is not a reading.

## Two hundred slices

The printed grid was then scored against 2,457 alphabets: English, French, German, Spanish, Italian, Portuguese, and Dutch, and for each language every way to merge two letters into one cell or to drop a letter. A 5 by 5 square has room for 25 letters. Esperanto has 28, so it was not treated as one letter per cell. The 2,457 shapes were split across 200 workers.

The friendliest shape is Italian with M and U in one cell, score 14.05. English's friendliest shape, also M with U, scores 23.96. Real English text of 196 letters, allowed to shop the same 2,457 shapes, has a median best score of 2.84. None of 200 such texts scored 14.05 or worse. Shopping for an alphabet does not make the printed grid ordinary.

Of 120 ways to rearrange the five digits inside every printed group, only two stay on his square. The printed order scores 34.23. Reversing the last three digits of each group scores 8.86, which does look like an English count. The same 120 rearrangements were applied to the solved example earlier in the book. There the printed order scores 4.14 and is the best of the 120. Reversing the last three digits makes that example worse, 21.56. The rearrangement that flatters the challenge is not the grouping he used when the plaintext is known. It is not adopted.

The cells are peaked (index of coincidence 0.0697), so this is not a flattened repeating-key cipher. The strongest column rhythm is matched by 20 of 200 shuffles of the same cells. No period is claimed. No plaintext is stored.

## Dummy letters, his own rule

The book says a dummy may be every third, fourth, or fifth letter. The swarm tried every period from 2 through 31 and every phase: 495 schedules. Each schedule was one worker process. Eighteen bands rechecked all 495 and agreed on the winner.

Dropping every second cell (period 2, phase 0) leaves 98 cells and scores 11.33. That is the friendliest of the 495. The book's own three periods score 18.49, 18.77, and 20.26. English text of 196 letters, allowed to pick the friendliest of the same 495 deletions, has a median best score of 3.61. None of 80 such texts was as flat as 11.33. The solved example in the book, given the same menu, still scores 2.20.

Deleting every kth digit, then repairing the pairs, never stays on the 5 by 5 square: 0 of 495. A dummy digit knocks the row alphabet into the column alphabet. No letter string is stored.

## What if he did not use that rule

The deletion swarm assumed the rule and then scored what remained. That is the wrong order. A dummy every third, fourth, or fifth cell would show up as one residue made of a single symbol. Twelve workers, one per book residue, each wrote that prediction down before counting.

None of the twelve is a filler. The narrowest uses 12 symbols in 49 cells (period 4, phase 0). Shuffling the same cells, 214 of 400 draws are that narrow or narrower. The most repetitive residue is only 20.4 percent one symbol, and 116 of 400 shuffles match it. The solved example in the book, which was not written with dummies, also has no one-symbol residue. Its narrowest class has 8 symbols.

So the rule is not in the digits. The rival stands: the 196 cells are the cipher. The flatness already measured on those 196 cells is not an English message hiding behind deleted letters. No letter string is stored.



