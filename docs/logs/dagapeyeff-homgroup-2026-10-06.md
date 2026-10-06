# A homophonic key under any transposition, 6 October 2026

Not a reading. No letter string is stored.

A transposition keeps every letter count, and a homophonic key splits each letter's count among the symbols that stand for it. So a text can become the cells under some homophonic key and some transposition, a turning grille included, only if the cells' 18 symbol counts can be grouped, one group a letter, into exactly the text's letter counts. `engine.dagapeyeff_homgroup` checks every window of 196 letters at a stride of 59: it decides exactly, by backtracking, whether such a grouping exists, and finds by local search the fewest single-cell errors it can reach (an upper bound on the true fewest).

| Text | Windows | Fewest different letters | Windows with 18 or fewer letters | Exact groupings | Fewest errors found | Median | Within 4 errors |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Held-out Austen, Doyle, Wells | 608 | 19 | 0 | 0 | none possible | none | 0 |
| Latin (held-out Thomas, Perseus) | 6,113 | 15 | 1,668 | 0 | 3 | 19 | 1 |

No English window uses 18 letters or fewer, so no English window can become the cells under a homophonic key and any transposition without errors. No Latin window can either, exactly; the closest needs at most 3 errors, and only 1 of 6,113 comes within 4.

This closes the main count-flattening loophole for the [turning grille](dagapeyeff-grillec-2026-10-06.md) for English, and leaves Latin only with chosen errors. A grille can still carry a message under a key that is not homophonic (a pair code or a keyed square of pairs), with an unusual text, or with deliberate errors.

Not a reading. No letter string is stored.
