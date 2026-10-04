# The solver now refuses a flat order

4 October 2026. No letter string for the 1939 challenge is stored.

Renaming symbols cannot make one symbol predict the next. The substitution solver now records that fact. `reading` is true only when fewer than one shuffle in twenty of the ciphertext is at least as dependent as the real order. On a known English substitution, the score is 0.7991 before and after decryption, and 0 of 200 shuffles match it, so the solver still returns that reading. On the 1939 pairs the score is 0.5706, and 170 of 200 shuffles match it, so the same rule refuses them. The anneal may still emit a best candidate for a text that passes the gate. A false gate means that candidate is not a solution.

The cells that are too crowded were then split, in case one label was hiding two letters. Five thousand random ways of cutting each of cells 91, 75, and 81:

| Cell | Times it appears | Best score after a cut |
| --- | --- | --- |
| 91 | 12 | 0.6542 |
| 75 | 17 | 0.6807 |
| 81 | 20 | 0.7002 |

Same-length English prose scores 1.0658. The best cut, of cell 81, is 0.7002. Fifteen of twenty shuffled copies of the cells, each given the same kind of cut, do at least that well. Splitting the crowded cell does not create a reading.

No letter string is stored.
