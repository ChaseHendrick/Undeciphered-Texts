Voynich MS: the trigram resolution pass - 21 October 2026

Ninth execution step for the Voynich case, and family 4's fourth
measurement, declared after the widened band's six below-widened-band
verdicts and before this run: the identical declared streams, mapped
set and greedy swap search, re-scored at trigram resolution under the
declared add-one trigram model of the first reference prose. The
declared purpose: a real text below the widened band at trigram
resolution as well as bigram resolution makes the class exclusion
declinable in its own declared format.

## Declared design of this run

Language model: P(third | first, second) = (n(first, second, third) +
1) / (n(first, second) + 27), built once from each frozen first
reference (Pride and Prejudice, the Confessiones) under the identical
declared processing. Counts: three consecutive counted positions, gaps
exactly as the bigram counts exclude them; the statistic is the best
mean nats per counted trigram. The search machinery is identical down
to the rank initialisation and the 16 seeded restarts, over the
trigram count tensor. Power instruments at this resolution: five
self-parity plants per (file, language), five multiset floors per
(file, language), and the widened cross band recomputed with five
plants per (file, language, text) under freshly declared seed kinds
12 to 17. Plant anchors: the design probe executed before the run
resolved that the plants are truncated streams, so the parity anchor
per cell is the truncated stream's own identity score, recorded in the
artifact; the probe also confirmed the machinery call cost at this
resolution is under one second. The real statistic recomputes from
the same declared seed as the first screen, kind 1.

## The measured resolution facts

- Clean identity anchors per counted trigram: English -1.7939 (Pride
  and Prejudice), Latin -1.9243 (the Confessiones). Both worth about
  three times the corresponding bigram values per symbol, consistent
  with genuinely sharper conditioning.
- Plant parity: ALL 30 self-parity plants converged to exactly their
  cell's truncated-anchor value (30 of 30 at four decimals). The plant
  instrument is exact at this resolution.
- Floors: every floor draw sits below its real value by 0.36 to 0.72
  nats per trigram; the destroyed-adjacency control works at trigram
  resolution too.

## The table

Real best (nats per counted trigram), the cell's anchor, floor maximum,
each band member's recovered best, and the verdict per the declared
rule:

| File | Language | Real | Anchor | Floor max | Band recovered bests (Frankenstein / Moby Dick / Malory; Caesar / Daniel / Heptaplomeres / Rariorum) | Verdict |
|------|----------|------|--------|-----------|-------------------------------------------------------------------------------------------------------|---------|
| ZL | english | -3.0925 | -1.8109 | -3.4881 | -1.9327 / -2.0449 / -1.9337 | consistent-with-substitution |
| GC | english | -2.9878 | -1.8146 | -3.5191 | -1.9358 / -2.0487 / -1.9398 | consistent-with-substitution |
| IT | english | -3.1210 | -1.8107 | -3.4843 | -1.9327 / -2.0447 / -1.9331 | consistent-with-substitution |
| ZL | latin   | -2.8468 | -1.9129 | -3.4132 | -2.0592 / -2.0809 / -2.0676 / -2.1587 | below-trigram-band |
| GC | latin   | -2.9182 | -1.9138 | -3.4387 | -2.0592 / -2.0809 / -2.0687 / -2.1587 | below-trigram-band |
| IT | latin   | -2.6908 | -1.9127 | -3.4104 | -2.0592 / -2.0809 / -2.0677 / -2.1587 | below-trigram-band |

## The disclosed search pathology, measured before it is interpreted

Three English cells carried the verdict consistent-with-substitution,
and the honest reason is machinery noise, not membership. The Moby
Dick band draws refused to converge in the three English cells: five
of fifteen Moby draws (plus one stuck Frankenstein draw in GC)
recovered scores of -3.4271 to -3.4451, essentially the floors' region
(-3.41 to -3.52), while the same text's other draws recovered -2.04 to
-2.05. Frankenstein and Malory converged perfectly in every English
cell, as did every Latin text (within 0.0001, one 0.0001 straggler),
and all thirty self-plants converged exactly. So the declared rule's
lower anchor in the English cells was reached through stuck draws
whose scores are demonstrably search outcomes rather than member
statistics: they sit just above the multiset floors, they vary by
draw on identical data, and the same text's healthy draws recover a
completely different value.

## The honest reading

- The robust comparison, computed from converged (best-recovered)
  member values only: the real text sits BELOW every best-recovered
  band member in all six cells, by 1.0476 (ZL english), 0.9391 (GC
  english), 1.0763 (IT english), 0.6881 (ZL latin), 0.7595 (GC latin)
  and 0.5321 (IT latin) nats per counted trigram.
- The measured cross-text penalty at trigram resolution - recovered
  best minus the anchor - is 0.1212 to 0.1218 nats per trigram
  (Frankenstein under the Pride and Prejudice model) and 0.1454 to
  0.1465 (Caesar under the Confessiones model). The real text's
  shortfalls above are 7.7 to 8.8 times the English penalty and 3.6 to
  5.2 times the Latin penalty. At bigram resolution the analogous
  multiple was 2 to 10x of a much smaller penalty; at trigram
  resolution the class signature neither narrows nor vanishes - the
  manuscript keeps the same structural position against its class at
  every resolution measured so far.
- What cannot be claimed from this artifact: the family's exclusion,
  because the declared rule's own English outcomes were reached
  through disclosed noise; and no additional exception either, because
  the Latin cells' below-trigram-band verdicts are clean and the
  English recovered values leave the real text far below them.

## Statement of the result, and its limits

It is measured, so stated: within the declared substitution class as
scoped and under the declared trigram model, thirty self-plants reach
their anchors exactly, every floor stays below the real, and the real
text stands below every best-recovered member of the seven-text
sampled band in all six cells by 0.53 to 1.08 nats per trigram
(3.6 to 8.8 times the measured cross-text penalties), while the
declared rule's verdict strings split three to three for a disclosed
machinery reason (stuck draws of one English text near the floors).
The class is not excluded by this artifact's rule alone; the family
stays open.

Limits: population as the third measurement's (three English and four
Latin proeses); abbreviated scribal usage outside the class as
declared in the first screen; the search pathology is disclosed as
measured behaviour of the greedy restarts at this resolution, without
a claimed mechanism; no mapping is published, and nothing here is a
reading.

## The declared next measurement

Fifth declared measurement, to be declared in its own docstring before
its run: a noise-controlled trigram band. Same streams, same model,
and the same search, with the restart budget raised as a declared
parameter of that measurement and a declared per-text convergence
criterion: a band member enters the band only when its plant draws
agree to within 0.0001 nats; failing texts are recorded as such and do
not set the threshold. If the real text stays below that band's
recovered members in all six cells, the exclusion of the scoped class
becomes declinable in its own declared format, with the bigram and
trigram artifacts behind it. Family 4 remains open, priority 1, with
four shipped measurements.
