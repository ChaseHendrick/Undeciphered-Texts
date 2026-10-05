# Real prose windows against the cells' counts, 5 October 2026

Nick Pelling proposed on Cipher Mysteries, 1 May 2021, sliding a 196-letter window over a large body of real text and comparing each window's sorted letter counts with the cells'. Jim Melichar reported a similar passage search in a 2014 comment there and found nothing that matched. Earlier passes here drew letters independently at English rates, and 0 of 10,000 such draws were as flat as the cells. Real passages vary more: names, repeated words and subject all move the counts.

`engine.dagapeyeff_corpus` counts every fourth 196-letter window of the 1,916,398-letter public training file, 479,051 windows, with J folded into I. Each window gets the best-assignment chi-square the swarm gives the cells, its number of distinct letters, and its largest count.

94 windows are as flat as the cells' 34.23. That is about 1 in 5,000, so real text can be that flat where independent draws almost never are. 192 windows use 18 letters or fewer. 37,008 have no letter more than 20 times. No window has all three at once. The closest window's sorted counts differ from the cells' by 16 in total; the median window differs by 56.

The windows overlap, so they are not 479,051 independent passages. The result still says that ordinary prose of this length very rarely looks like the cells' counts, and that none of it here does in every respect at once. A transposition cannot change counts.

Not a reading. No letter string is stored.
