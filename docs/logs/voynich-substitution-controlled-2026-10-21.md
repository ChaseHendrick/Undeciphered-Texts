Voynich MS: the noise-controlled trigram band - 21 October 2026

Tenth execution step for the Voynich case, and family 4's fifth and
final measurement, declared after the trigram pass's split verdicts and
its disclosed search pathology, and before this run: the identical
streams, model and search re-measured under a raised restart budget as
a declared parameter of this measurement, plus a declared per-text
convergence criterion that decides band membership from draw agreement
on identical data. The declared purpose, also declared before the run:
the exclusion format that this artifact either triggers or declines,
spelled out in the module docstring in advance.

## Declared design of this run

- Restart budget: 48 restarts (one rank initialisation plus 47 seeded
  permutations), sweep cap unchanged at 200, applied identically to
  the real, every plant and every floor - one budget rule for real and
  instruments alike.
- Convergence criterion: a cross text enters the band of its cell only
  when its five plant draws agree to within 0.0001 nats per trigram;
  a text whose draws disagree is recorded with its recovered best and
  spread, does not set the band threshold, and the disclosure names
  the runs.
- Seed kinds, declared before the run: controlled plant permutation
  18 and machinery 19 (the plant index); controlled floor permutation
  20 and machinery 21 (the floor index); controlled cross permutation
  22 and machinery 23 (the text position, sequential scheme of one
  permutation rng and one machinery rng per (file, language, text)).
- Verdict rule declared in advance: real at or above the smallest
  entered-band value is consistent-with-substitution; real at or
  below the largest floor is not-consistent; strictly between is
  below-controlled-band; an empty entered band is
  band-unresolvable-noise.
- Exclusion format declared in advance: if the real stands below the
  smallest entered-band value in all six (file, language) cells, the
  scoped class is excluded by count for the measured statistics, with
  the standing caveats; otherwise the family stays open.

## The measured controlled-band facts

- Plant parity survives the raised budget: all 30 self-parity plants
  converged to exactly their cell's truncated-anchor value (30 of 30
  at four decimals), and the 0.0001 straggler of the trigram pass
  either vanished or stayed inside the declared less-than-or-equal
  rule.
- Real re-measured under the identical budget, seed kind 1 by replay:
  two cells improved - ZL english from -3.0925 to -3.0514 and GC latin
  from -2.9182 to -2.8934 - the declared consequence of the shared
  budget rule; four cells' values were already the budget's optimum.
- The convergence pathology under the 16-restart budget (six stuck
  draws) shrank to four stuck draws at 48 restarts, and Moby Dick
  entered ZL's band with all five draws at exactly -2.0449, but three
  text-draw sets still failed the criterion (disclosed below) and took
  no part in setting the threshold, exactly as declared.

## The table

Real best (nats per counted trigram), the cell's anchor, floor
maximum, the entered band's smallest value, and the verdict per the
declared rule:

| File | Language | Real | Anchor | Floor max | Entered band bests | Excluded members (stuck draws) | Band min | Margin to band | Verdict |
|------|----------|------|--------|-----------|---------------------|-------------------------------|----------|----------------|---------|
| ZL | english | -3.0514 | -1.8109 | -3.4880 | -1.9327 (Frankenstein), -2.0449 (Moby Dick), -1.9337 (Malory) | none | -2.0449 | -1.0065 | below-controlled-band |
| GC | english | -2.9878 | -1.8146 | -3.5182 | -1.9398 (Malory) | Frankenstein spread 1.4974 (one stuck draw), Moby Dick spread 1.3785 (two stuck draws) | -1.9398 | -1.0480 | below-controlled-band |
| IT | english | -3.1210 | -1.8107 | -3.4842 | -1.9327 (Frankenstein), -1.9331 (Malory) | Moby Dick spread 1.3808 (one stuck draw) | -1.9331 | -1.1879 | below-controlled-band |
| ZL | latin   | -2.8468 | -1.9129 | -3.4128 | -2.0592, -2.0809, -2.0676, -2.1587 (all four Latin texts) | none | -2.1587 | -0.6881 | below-controlled-band |
| GC | latin   | -2.8934 | -1.9138 | -3.4378 | all four Latin texts | none | -2.1587 | -0.7347 | below-controlled-band |
| IT | latin   | -2.6908 | -1.9127 | -3.4093 | all four Latin texts | none | -2.1587 | -0.5321 | below-controlled-band |

Margins above the floor maximum before rounding differences: 0.4366 to
0.7185 nats per trigram (0.36 to 0.72), so the not-consistent branch
was never triggered and the real is again established above the
destroyed-adjacency controls at both resolutions.

## The exclusion condition, measured in all six cells

The declared exclusion format's condition is satisfied: the real text
stands below the smallest entered-band value in all six (file,
language) cells, by 1.0065 (ZL english), 1.0480 (GC english), 1.1879
(IT english), 0.6881 (ZL latin), 0.7347 (GC latin) and 0.5321 (IT
latin) nats per counted trigram. Note the honest tightening this run
brought: the raised budget improved the real's own statistic in two
cells, and the margins above are computed from the re-measured real
against the criterion-clean band, not from the trigram pass's stale
numbers.

## Statement of the result, and its limits

Per the exclusion format declared before this run: the scoped class -
one-to-one substitution of a known language, word divisions carried,
no abbreviation, no transposition, no nulls, within the sampled
population of seven reference proeses - is excluded by count for the
manuscript's statistics as measured, at bigram and trigram resolution
alike, with the power instruments exact (30 of 30 self-plants at
parity, floors below the real, cross bands recomputed clean of search
noise). The instrument failures were disclosed as measured behaviour
and neutralised by the criterion; they are not claimed as a mechanism.

Limits, unchanged from the declaration: abbreviated scribal usage lies
outside the scoped class; the population is sampled, not exhaustive;
the reference texts are modern printed proeses; no mapping is
published; nothing here is a reading; plaintext_recovered_percent
remains 0. Not covered by the family's exclusion: homophonic or
polyalphabetic substitution, word-level ciphers, transposition
systems, and null or abbreviation-based schemes.

## Where the case stands

Family 4 closes as excluded-by-count on five shipped measurements
(the screen, the crossband, the widened band, the trigram pass, the
noise-controlled band), each with its declared power controls and its
dated log. Family 5 opens in the same ship: is it a homophonic
substitution of a known language? Its declared scope and instruments
(alphabet partition rule, assignment sampler, plants, floors,
cross-text band) are to be written to the module docstring of
engine/voynich_homophonic.py before that family's first run; family
4's artifacts stand as the measured exclusion the new family does not
cover.
