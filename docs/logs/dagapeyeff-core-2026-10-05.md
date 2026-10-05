# The common cells are a fair die

5 October 2026. Not a reading. No letter string is stored.

Sorted, the 196 cell counts are 20, 17, 17, 17, 17, 16, 15, 14, 12, 12, 11, 11, 9, then 3, 2, 1, 1, 1. The largest drop between neighbors, by ratio, is after the thirteenth cell. Those 13 cells hold 188 of 196.

They are as even as a fair die. Their chi-square against a fair 13-sided die is 8.6596. Of 20,000 throws of such a die, 188 times each, 5,442 are at least that flat. That also explains the index of coincidence. 0.0697 is close to English, and it is also close to what 13 equal cells give, about 0.071. The repo already knew the counts were not English. This says what shape they have instead.

The statistic was chosen after looking at the counts. The widening is that every other text picks its own cliff, the k with the largest drop, and is scored at that k. A core matches when it holds at least 188 of 196 and is no less even than 8.6596.

- 20,000 windows of 196 letters from the public-domain English corpus: 987 are as flat at their own cliff, and 0 are both as flat and as full.
- The book's solved exercise has its cliff at 19 cells of 89, with a chi-square of 32.8605. It looks like English, not like a die.

Then 21 ways of making 196 cells, 2,000 draws each. Plaintext is English from the same corpus, with I and J merged.

| Family | Flat, full core |
| --- | --- |
| Any transposition of a Polybius, including the diagonal routes | 0 |
| Vigenere, period 2, 3, 5 | 0, 0, 0 |
| Vigenere, period 7, 14 | 1, 8 |
| Running key from more English | 13 |
| Plaintext autokey | 0 |
| Both coordinates shifted, period 2 and 7 | 0, 1 |
| Column coordinate shifted, period 5 | 0 |
| Bifid, period 7 and the whole text | 1, 0 |
| The digit stream re-paired one place late | 0 |
| Twenty nulls from three cells | 0 |
| The six most common letters split into two cells | 0 |
| Playfair with a random square | 0 |
| Two cells per letter from 13 symbols | 1 |
| Letters merged into 13 classes | 1 |
| Two cells per letter from 13 symbols, then a period-7 key on those symbols | 130 |
| 13 equal cells and a rare tail, no language | 485 |

No family that enciphers English in this sweep reaches 5 percent, except the one built to flatten a 13-symbol channel, at 6.5 percent. Random cells drawn evenly from 13, with a tail of 5, reach 24 percent.

If a key flattened a 13-symbol channel, a short repeating key should leave a stride. On the 188 core cells, periodic index of coincidence was taken at every stride from 2 to 49. The best is 40, at 0.1051. Of 2,000 shuffles, each allowed its own best stride, 831 reach it. There is no stride.

What this narrows: a transposition of a Polybius, the published diagonal route included, cannot make these counts, and neither can a short periodic key, autokey, bifid, Playfair, nulls, or a simple homophone. What survives is a long or non-periodic key on a channel of about 13 symbols, or cells that do not carry language. Neither is a reading. Do not search a running key and call the best score a text.
