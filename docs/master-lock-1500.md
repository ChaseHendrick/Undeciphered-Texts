# Master Lock 1500-style combination reducer

This note records a published arithmetic reduction for the Master Lock
dial family with 40 positions (0 through 39), the layout used by the
1500 series and similar three-number Master padlocks. It is checked
against one combination that a published guide already prints. It is
not instructions for a specific physical lock and not a claim about
Nr. 86.

## Source

Jon Westfall, *Recovering Master Lock Combinations: Guide & Combination
List* (2007; portions from Liam Bowen):

https://jonwestfall.com/wp-content/uploads/2007/08/mlock1.pdf

Fetched 2026-10-02. The guide says a Master dial has 64,000 possible
combinations (40 times 40 times 40). Given the third number, it keeps
only the numbers that share a remainder modulo 4:

- The first number is one of the 10 positions with the same remainder
  as the third number modulo 4.
- The second number is one of the 10 positions found by adding 2 to
  those first numbers, wrapping from 39 back to 0.
- The third number stays fixed.

That product is 10 times 10 times 1, which is 100 candidates, not a
full pass over 64,000 triples.

## Published known combination

Westfall's worked example uses third number 19. He lists first numbers
3, 7, 11, 15, 19, 23, 27, 31, 35, and 39, and second numbers 5, 9, 13,
17, 21, 25, 29, 33, 37, and 1. In that list he marks 7-9-19 as the
actual combination.

The reducer in `engine/solvers/master_lock.py` builds that same set
from the third number. The certificate at
`engine/data/master_lock_certificate.json` stores the method name, the
known combination string `7-9-19`, the third number 19, the candidate
count 100, the source URL, and the SHA-256 of the combination string
`7-9-19`.

## What this does not do

The code takes a third number that is already known and lists the
residue class. It does not search all 64,000 dial triples. It does not
describe how to operate a physical lock, and it does not say anything
about army message Nr. 86 or any other undeciphered text.
