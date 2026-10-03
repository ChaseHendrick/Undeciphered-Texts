# Dudley 60-position combination reducer

This note records a published arithmetic reduction for the Dudley dial
with 60 marks. It is checked against one pair that a published worked
example already prints. It is not instructions for a specific physical
lock and not a claim about Nr. 86.

## Source

James Howell, "Hack a Dudley combination lock in 10 minutes" (2010):

https://jameshowell.wordpress.com/2010/09/04/hack-a-dudley-lock-in-10-minutes/

Fetched 2026-10-02. The page says three unrestricted numbers on a
60-mark dial are 60 times 60 times 60, which is 216,000. The worked
example uses only 10 positions, found by starting at 2 and adding 6:

2, 8, 14, 20, 26, 32, 38, 44, 50, 56.

It then keeps pairs whose second number is lower than the first. The
page adds 9 + 8 + 7 + 6 + 5 + 4 + 3 + 2 + 1 and states that this is 45
combinations. The printed list begins 8-2 and ends 56-50. The page
does not mark one of those pairs as the combination that opened the
lock.

## What the certificate stores

The reducer in `engine/solvers/dudley_lock.py` builds that pair list
from the first position. The certificate at
`engine/data/dudley_lock_certificate.json` stores the method name, the
pair string `8-2`, the first position 2, the candidate count 45, the
source URL, and the SHA-256 of the string `8-2`.

## What this does not do

The code takes a first position and lists the 45 pairs. It does not
search all 216,000 dial triples. It does not describe how to operate
a physical lock, and it does not say anything about army message
Nr. 86 or any other undeciphered text.
