# Combination locks and safe dials

This note records two published arithmetic reductions and the published
size of a Group 2 safe-lock combination space. It cites pages fetched
on 2026-10-02. It is not instructions for opening a physical lock or
an installed safe, and it is not a claim about Nr. 86.

## Master Lock 1500 dial residue

The reducer already in the tree is `engine/solvers/master_lock.py`
(`reduce_master_lock`, `first_numbers`, `second_numbers`). The same
arithmetic is written up in `docs/master-lock-1500.md` and checked in
`engine/data/master_lock_certificate.json` against the combination
string `7-9-19`.

Source: Jon Westfall, *Recovering Master Lock Combinations: Guide &
Combination List* (2007; portions from Liam Bowen):

https://jonwestfall.com/wp-content/uploads/2007/08/mlock1.pdf

The guide says a Master dial has 64,000 possible combinations, because
each of three numbers is one of 40 positions, 0 through 39. Given the
third number, the reduction keeps one residue class modulo 4:

- The first number is one of the 10 positions with the same remainder
  as the third number modulo 4.
- The second number is each of those first numbers plus 2, wrapping
  from 39 back through 0 (the guide's example starts the wrap at 0,
  not at 1).
- The third number stays fixed.

The guide states that product as 10 times 10 times 1, which is 100
candidates, not a pass over 64,000 triples.

Worked case in the guide: third number 19, and 19 divided by 4 leaves
remainder 3. First numbers: 3, 7, 11, 15, 19, 23, 27, 31, 35, 39.
Second numbers: 5, 9, 13, 17, 21, 25, 29, 33, 37, 1. The guide marks
7-9-19 as the actual combination of that example. The in-repo function
`reduce_master_lock(19)` builds that same set of 100 triples.

The module takes a third number that is already known and lists the
residue class. This note does not repeat any physical dialing steps
from the guide.

## Another published combination code: Group 2 spacing

A different published reduction applies to three-number Group 2 safe
locks, not to the 40-position Master padlock above. It is a code
rule on which triples count, not a residue class of a padlock dial.

Source: Matt Blaze, *Safecracking for the computer scientist* (draft
7 December 2004, revised 21 December 2004), section 1.3.1:

https://www.mattblaze.org/papers/safelocks.pdf

Blaze reports a Sargent and Greenleaf recommendation for three-number
locks, citing Brian Costley, *Sargent and Greenleaf Mechanical Safe
Lock Guide* (2001). The recommendation, as Blaze states it, is:

- The combination as a whole is not a monotonically increasing series
  and not a monotonically decreasing series.
- Adjacent numbers differ by at least ten graduations.
- 25 percent of the dial is avoided for the final number.

Blaze gives the sizes that follow from those rules. He writes that the
Group 2 Sargent and Greenleaf R6730 has a usable combination keyspace
of roughly 282,807 distinct combinations under its mechanical
specifications (dialing tolerance plus or minus 0.75, and 94 percent
of the dial usable for the last number). Of those, he says only
111,139 are considered good under the recommendation. For locks that
use the full plus or minus 1.25 dialing tolerance allowed under UL
Group 2, he says the same recommendations leave only 22,330 distinct
good combinations, which he describes as less than 2.5 percent of the
apparent keyspace of 1,000,000. He also notes that the mechanism
itself on S&G locks requires avoiding only 6 percent of the dial for
the last number, against the 25 percent in the recommendation.

Those counts are Blaze's published figures. This note does not add a
count he does not state, and it does not describe how to dial, probe,
or search a mounted lock.

## Published Group 2 combination space

The same Blaze section states the nominal space before those cuts.
Most safe and vault dials he discusses are divided into 100
graduations, with three dialed numbers, which he writes as 100 cubed,
or 1,000,000 possible combinations. A four-number lock is 100 to the
fourth, or 100,000,000. On certification, he writes that UL rating
standards for Group 2 safe locks specify at least 1,000,000 different
combinations, and a dialing tolerance of at most plus or minus 1.25.

Sargent and Greenleaf's own Group 2 product page says the same nominal
size for the three-wheel models. Fetched the same day:

https://sargentandgreenleaf.com/product/6700-series/

That page lists the 6730 Series Three-Wheel and the 6741 Series as
UL-Listed Group 2, and it states "1 million possible combinations" for
each of those two. The model 6741 datasheet, also UL-Listed Group 2,
states "1 million possible combinations":

https://sargentandgreenleaf.com/wp-content/uploads/2021/03/SG-LIT-SEL-6741.pdf

The published Group 2 combination space in these sources is therefore
1,000,000 (one million) for the three-number locks they describe. The
smaller figures in the previous section are Blaze's account of usable
or recommended subsets, not a replacement for that published space.

## What this does not do

Nothing here is a procedure for opening a specific padlock, a mounted
safe, or any other physical container. The Master Lock section only
restates the residue arithmetic already implemented from Westfall's
guide. The Group 2 sections only restate published sizes and a
published code rule. Neither section is about army message Nr. 86 or
any other undeciphered text.
