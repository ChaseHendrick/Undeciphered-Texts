Voynich MS: the cross-text calibration of the substitution screen - 20 October 2026

Seventh execution step for the Voynich case, and family 4's second
measurement, declared after the first screen's six indeterminate
verdicts and before this run: the cross-text calibration band, which
turns the self-parity plant of the first screen into the band a genuine
class member occupies when it is scored against a model of a different
prose of the same language.

## What the first screen left open

The first screen's plants were self-parity: the reference prose encoded
and decoded under a model of the same prose. A member of the declared
class - another prose of the language - would sit somewhat below
self-parity by an unmeasured cross-text penalty, and that unmeasured
penalty plausibly covered the first screen's margins. This unit
measured it.

## The declared second references, frozen before the run

English: Frankenstein (Mary Shelley), Project Gutenberg ebook 84,
407,795 processed symbols, 18.5 percent space. Latin: C. Iuli Caesaris
De Bello Gallico I-IV (the Latin original), Project Gutenberg ebook 218,
143,947 processed symbols, 14.3 percent space. Identical declared
processing to the first references (body between the Gutenberg markers,
ligatures expanded, case-fold, non-letters to space, space runs
collapsed), frozen in engine/data, sha256 recorded in the artifact.

## Declared design of this run

Cross plants: 5 per (file, language); the second text's processed stream
encoded through a seeded permutation of the mapped positions, truncated
to min(the file's stream length, the second text's processed length),
scored by the identical machinery under the first language's table. A
cross plant is exactly what the class says the manuscript could be:
another prose of the language under substitution, fairly scored. Floors:
recomputed from their declared seeds, and the tests pin them equal to
the first artifact's floor values. Seed kinds: cross permutation 6,
cross machinery 7, declared before the run. Verdict rule, declared
before the run: real at or above the smallest cross plant is
consistent-with-substitution; real at or below the largest floor is
not-consistent; real strictly between is below-cross-band.

## The table

Real best (nats per counted pair), the converged cross-plant value, and
the verdict per the declared rule:

| File | Language | Real | Cross plants (5x) | Cross plant length | Real to band | Verdict |
|------|----------|------|-------------------|--------------------|--------------|---------|
| ZL | english | -5.2832 | -5.1603 | 218,663 | -0.1229 | below-cross-band |
| ZL | latin   | -5.3162 | -5.1345 | 143,947 | -0.1817 | below-cross-band |
| GC | english | -5.3536 | -5.1646 | 186,708 | -0.1890 | below-cross-band |
| GC | latin   | -5.3883 | -5.1345 | 143,947 | -0.2538 | below-cross-band |
| IT | english | -5.2541 | -5.1603 | 220,532 | -0.0938 | below-cross-band |
| IT | latin   | -5.2933 | -5.1345 | 143,947 | -0.1588 | below-cross-band |

All cross plants converged to exactly one value per (file, language)
cell - twenty of twenty again at parity - so the machinery again
demonstrates it recognizes a substitution when the material is one.

## The honest reading

- The cross-text penalty is now measured on two real cross pairs, not
  speculated: English, Pride and Prejudice self-parity -5.1422 against
  Frankenstein cross-parity -5.1603, a penalty of 0.018 nats per pair.
  Latin, Augustine (Confessiones) self-parity -5.0742 against Caesar
  cross-parity -5.1345, a penalty of 0.060 nats per pair. Both are far
  smaller than the first screen's margins speculated.
- Against those measured penalties, the manuscript's real position is
  stark: it sits 0.094 to 0.189 nats per pair (English cells) and 0.159
  to 0.254 nats per pair (Latin cells) BELOW the cross band - roughly 2
  to 10 times the measured cross penalty of the English pair and 2.6 to
  4.2 times the Latin pair's, cumulatively on the order of tens of
  thousands of nats below what substituted Frankenstein or substituted
  Caesar achieve in the same machinery.
- A length asymmetry that favors the real text is disclosed: the Latin
  cross plants are cut to 143,947 symbols because Caesar's text is the
  shorter, versus the real streams' 218,663 (ZL) to 220,532 (IT)
  positions. The shorter count matrix should, if anything, handicap the
  plants; they still score above the real text in every Latin cell. The
  English cross plants are cut to the real streams' own lengths, so no
  asymmetry applies there at all.
- What the below-band verdict is, by the rule declared before the run:
  the real text is not explained at the level of the class as sampled.
  It is not, by itself, the family's closure: the band is five
  permutation draws of two proeses per language, and the honest caveat
  stands that the population of "proses of a language" - in particular
  period styles of the manuscript's century - is wider than the sample.
  Abbreviated scribal usage was declared outside the class in the first
  screen and remains outside it; members with such usage are not within
  this class's scope and can score below the band without contradicting
  the measurement.

## Statement of the result, and its limits

It is measured, so stated: within the declared substitution class as
scoped - one-to-one, word divisions carried, no abbreviation, no
transposition, no nulls - and at bigram resolution with this machinery,
the manuscript's text scores below every calibrated member of the class
sampled so far, in all six (file, language) cells, by margins that
exceed the measured cross-text penalty from both sampled cross pairs.
The class as scoped now has its measurer standing ready and its band
calibrated; what remains before any exclusion claim is population
coverage, which is machinery-independent and declared next.

Limits: two proeses per language; bigram resolution; the band's
population tail unmeasured; no conclusion about language, cipher or
meaning beyond this scoped instrument. Nothing here is a reading, no
mapping is published, and the family question stays open until the
widened band is declared and run.

Family 4 remains open with power instruments green and the band
calibrated. Next: widen the cross-text population (a declared third and
further reference prose per language, including period-appropriate
styles), then a declared trigram-resolution pass; if the real text still
stands below a widened band, the exclusion is there to be written in its
own declared format.
