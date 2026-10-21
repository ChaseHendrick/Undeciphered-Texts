Voynich MS: the widened substitution band - 21 October 2026

Eighth execution step for the Voynich case, and family 4's third
measurement, declared after the cross screen's six below-cross-band
verdicts and before this run: the band is widened from two cross texts
per language to three (English) and four (Latin) class members, so the
population caveat that stopped the cross screen short of an exclusion
claim is now answered at bigram resolution by a sampled, wider band.

## What the cross band left open

The cross screen measured the cross-text penalty on two real cross
pairs - 0.018 nats per pair (Frankenstein under the Pride and Prejudice
model) and 0.060 (Caesar under the Confessiones model) - and the real
text sat 2 to 10 times those penalties below the band. But the band
held one member per language beyond the model itself; the honest
verdict was below-cross-band, not-consistent only with the sampled
population, and the declared next step was population coverage. This
unit is that step.

## The declared second-wave references, frozen before the run

English adds Moby Dick (Herman Melville, Project Gutenberg ebook 2701,
1,174,300 processed symbols, 18.7 percent space) and Le Morte D'Arthur
volume 1 (Thomas Malory, the 1485 Caxton prose - the population's
period-appropriate member, ebook 1251, 854,142 processed symbols, 19.9
percent space). Latin adds Vulgate Daniel (ebook 828, late-antique
biblical prose, 77,572 processed symbols, 15.7 percent space),
Colloquium heptaplomeres (Jean Bodin's Renaissance philosophical
dialogue, ebook 17859, 938,855 processed symbols, 14.4 percent space),
and De Rariorum Animalium atque Stirpium Historia (early-modern
natural-history Latin, ebook 27655, 77,529 processed symbols, 15.1
percent space). Identical declared processing (body between the
Gutenberg markers, ligatures expanded, case-fold, non-letters to space,
space runs collapsed), frozen in engine/data with sha256 recorded in
the artifact. Rejected for cause, recorded here: the English school
editions and glossed school readers carry English-language apparatus
into the Latin files, and a same-volume Caesar continuation (V-VIII)
adds an author already in the band without a new century of prose.

## Declared design of this run

The band holds every declared cross text: the cross screen's two own
texts (Frankenstein, Caesar De Bello Gallico I-IV) plus the five
additions above. Plants: 5 per (file, language, text). The cross
screen's own texts replay their declared per-plant seeds (kinds 6 and
7, the plant index in the seed) and so recompute their cross-artifact
values exactly; the added texts draw five permutations sequentially from
one rng per (file, language, text) and run the five machinery calls in
plant order from one rng (kinds 10 and 11, the text position in the
seed), declared before the run. Plant length: min(the file's stream
length, the text's processed length), recorded per entry. Floors:
recomputed from their declared seeds, pinned by the tests equal to the
first artifact's values. Verdict rule, declared before the run: real at
or above the smallest band best is consistent-with-substitution; real
at or below the largest floor is not-consistent; strictly between is
below-widened-band.

## The table

Real best (nats per counted pair), the per-text converged bests in band
order, the band's weakest and strongest edges, and the verdict per the
declared rule. Every per-text plant set converged to exactly one value
at four decimals (35 of 35 plants at convergence), and the two legacy
entries reproduce the cross artifact's stored values exactly.

| File | Language | Real | Band bests (cross screen text first, then the additions) | Real to weakest | Verdict |
|------|----------|------|-----------------------------------------------------------|-----------------|---------|
| ZL | english | -5.2832 | -5.1603 (Frankenstein), -5.1893 (Moby Dick), -5.1004 (Malory) | -0.0939 | below-widened-band |
| ZL | latin   | -5.3162 | -5.1345 (Caesar), -5.1439 (Daniel), -5.1682 (Heptaplomeres), -5.2063 (Rariorum) | -0.1099 | below-widened-band |
| GC | english | -5.3536 | -5.1646, -5.1887, -5.1083 | -0.1649 | below-widened-band |
| GC | latin   | -5.3883 | -5.1345, -5.1439, -5.1662, -5.2063 | -0.1820 | below-widened-band |
| IT | english | -5.2541 | -5.1603, -5.1905, -5.0999 | -0.0636 | below-widened-band |
| IT | latin   | -5.2933 | -5.1345, -5.1439, -5.1683, -5.2063 | -0.0870 | below-widened-band |

Band edges moved exactly as widening should: the English band's weakest
member went from -5.1603 (Frankenstein alone) to -5.1893 (Moby Dick),
the Latin band's from -5.1345 (Caesar) to -5.2063 (Rariorum); widening
pulled the weakest member's score toward the real and roughly halved
the shortfall edges, from 0.094-0.189 (English, before) and 0.159-0.254
(Latin, before) to 0.064-0.165 and 0.087-0.182 now, while the real
stays 1.17 to 1.33 nats per pair ABOVE the recomputed floor noise, far
from both edges but strictly below the band in all six cells.

## The honest reading

- The class's sampled members are now three proeses under the English
  model plus its own text, and four under the Latin model plus its own.
  Every one of the 35 converged plant values across the six cells sits
  above the corresponding real value. The verdict strings below stand
  per the rule declared before the run; no cell flipped to
  consistent-with-substitution.
- The period-appropriate member does not rescue the class in the
  direction it was expected to: Malory's 1485 Caxton prose - archaic,
  closest in time to the manuscript - scores the STONGEST plant values
  (about -5.10), not the weakest. Archaic style does not explain the
  manuscript's gap at bigram resolution; if anything, the gap to the
  weakest members is style-stable.
- The band's weakest edge is set by the two short Latin members (Daniel
  77,572 and Rariorum 77,529 processed symbols). Their plants run at a
  massive length handicap - under 78 thousand symbols against the real
  streams' 218,663 to 220,532 - and still score above the real text in
  every Latin cell. The Latin asymmetry disclosed at the cross screen
  (Caesar truncated at 143,947) is joined by a larger one here, and it
  again favors the real text.
- What the last open question of the class needs is a resolution jump,
  not more prose: the shortfall is a stable fraction of band position
  (roughly 1.3 to 3.5 percent of the nats magnitude) and it persisted
  in direction and rough size through two calibrations. The declared
  next instrument is the trigram-resolution pass: if the real text
  stands below a widened band at trigram resolution too, the exclusion
  is there to be written in its own declared format, and the widened
  band's per-text margins would carry the population caveat only as far
  as it is measured to go.

## Statement of the result, and its limits

It is measured, so stated: within the declared substitution class as
scoped - one-to-one, word divisions carried, no abbreviation, no
transposition, no nulls - and at bigram resolution with this machinery,
the manuscript's text scores below every one of 35 seeded plants of 7
proeses per language counted across the six cells, after a band
widening that was declared before this run and whose weakest member
itself scores under a length handicap favoring the real text. The
verdict is below-widened-band in all six (file, language) cells; the
class is not excluded by this measurement alone, and no conclusion
about language, cipher or meaning is drawn here. Nothing is a reading,
no mapping is published, and the family stays open.

Limits: three English and four Latin proeses sampled, not the
population; bigram resolution; the band's tail unmeasured; abbreviated
scribal usage still outside the class as declared in the first screen.
Power instruments: floors recompute their frozen values (tests pin them
to the first artifact), all 35 plants converged, and the legacy replays
reproduce the cross artifact exactly.

Family 4 remains open, priority 1, with three shipped measurements.
Next: the declared trigram-resolution pass over the same declared
streams; a real text below a widened band at trigram resolution converts
the population caveat into the measured form its own instrument needs.
