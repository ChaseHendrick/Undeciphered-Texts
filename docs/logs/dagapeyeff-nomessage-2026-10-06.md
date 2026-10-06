# Starting from no message, 6 October 2026

Not a reading. No letter string is stored.

Van Eykelen ([MsgTrail XV](https://msgtrail.com/posts/unmasking-the-dagapeyeff-cipher-xv-the-recipe-not-the-message)) found a hand procedure with no plaintext that reproduces fourteen statistics of the cells: tally 18 pairs with fixed counts, deal them onto the grid at random, and move a rare pair that lands mid-row to the end of its row. `engine.dagapeyeff_nomessage` takes the simplest form of that recipe as a null hypothesis and tries to reject it. The cells' own symbols are dealt at random, with the 8 rare cells held in their places in the last column. Under this null the letter counts are fixed, so only the order of the cells can tell a message from no message.

Thirty order statistics were declared before any score was read: the share of equal symbols at lags 1 to 14, the mutual information of symbols at lags 1 to 14, the number of different neighbouring pairs and the number of repeated triples. None is changed by a one-to-one key. Each gets a two-sided rank p-value against the null, and the family-wise p-value is the share of null draws whose smallest p-value is as small as the cells'.

**The cells.** Against 20,000 dealings the family-wise p-value is 0.2814. The smallest single p-value is mutual information at lag 3, 0.0138, then equality at lag 12, 0.0622. Lag 3 is the one trace van Eykelen reported surviving his models, so it was named before this test, but on the same cells; it does not survive the 30-statistic correction, and repeating his finding on the same data is not independent confirmation.

**Power.** The same test was run on 20 planted held-out English texts per system, each against 2,000 dealings of its own symbols. Flagged at p 0.05 or less:

| Message system | Flagged |
| --- | --- |
| Keyed square (any one-to-one key) | 19 of 20 |
| 14-column transposition, done | 19 of 20 |
| Repeating coordinate shift, period 2 to 14 | 10 of 20 |
| Turning grille, 14 by 14 | 3 of 20 |
| 14-column transposition, undone | 2 of 20 |
| Random transposition (a no-message dealing; calibration) | 1 of 20 |

**What follows.** The order of the cells is what a no-message dealing gives. A message under a keyed square or a done 14-column transposition would almost always have been caught, and was not. The systems this test cannot see are those that scramble order thoroughly: the turning grille and the undone 14-column transposition. The undone transposition is closed for English and Latin by the joint searches, so among the systems tried, the only message-bearing explanation the order still allows is a turning grille, or a system not yet tested that destroys order as thoroughly. No message remains the simplest explanation of the order; it is not proved.

Not a reading. No letter string is stored.
