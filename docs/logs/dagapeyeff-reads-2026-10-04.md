# Column keys and digit reads

4 October 2026. 50,000 seeded trials. No letter string is stored.

Letter counts cannot be changed by rearranging the 196 cells. They can be changed by splitting the cells back into digits and pairing the digits again. Both were tried.

## Column keys

Ten thousand random orders of the 14 columns, read across and read down.

The printed across-reading has 65 repeated neighbors. 7,883 of the 10,000 keys repeat at least that often, so the printed order is on the low side, not a hidden key. The best across-key in that draw repeats 84 times. A second draw of 10,000, different seed, best is 81. The winner of a search is just the top of the same pile.

Reading straight down the columns repeats 74 times. 2,531 of 10,000 down-keys do at least that well. The best down-key is 77 in both draws. No column key stands out.

## Digit reads

Writing the 392 digits across and reading down:

| Width | Legal pairs out of 196 | Same pairs as the original |
| --- | --- | --- |
| 2 | 0 | 0 |
| 4 | 0 | 0 |
| 14 | 0 | 0 |
| 3 | 196 | 153 |

Even widths put row-digits in one column and column-digits in the next, so every new pair is illegal. From widths 2 through 28, the only read that stays entirely on the square is width 3. It rewrites 43 pairs. Its letter-count score falls from 34.23 to 11.73, and 1,067 of 10,000 English strings are at least that flat, so the new counts are inside English.

That fall is not evidence for width 3. Ungluing the digits at random, 10,000 times, has a median score of 9.86. 7,473 of those random re-pairings score 11.73 or better. Width 3 is an ordinary way to undo the original pairs. The flatness lives in the original gluing. Destroying it makes the counts look more like English no matter how you destroy it.

The common symbols, everything that appears more than twice, are not piled into columns. Their concentration is 44, and 529 of 10,000 shuffles are at least that piled. The rare-symbol column already measured is still the only placement fact.

No letter string is stored.
