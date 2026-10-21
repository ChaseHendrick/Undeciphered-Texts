Voynich MS: the held-out homophonic screen - 21 October 2026

Twelfth execution step for the Voynich case, and family 5's second
measurement, declared in `engine/voynich_homophonic.py`'s docstring
before any run of the module. The first screen's disclosed exploitation
question was answered no by direction (the margin did not reverse when
exploitation's data-specific volume was priced), and the family stays
exactly where the exclusion format puts it: open, nothing excluded.

## Declared design of this run

- The identical frozen streams, references, mapped set (36 glyphs plus
  the word-boundary mark, 37 cipher symbols over 27 letter tokens),
  plants, floors, seven-member band and seed kinds as the first
  screen. No new seed kind is consumed anywhere; the first screen's
  plant and band draws replay unchanged, and the split consumes no
  seed.
- Finding (a), disclosed in the docstring before the run: the first
  screen's candidate rule evaluated exactly at the current label only.
  For any other label it errs by n times (table[l, c] + table[c, l] -
  2 table[l, l]), where n is the symbol's own self-pair count (a
  symbol swerves onto itself under a boundary mark). The probe
  measured the drift: on one plant, running climb-time totals of
  +23430 against -20520 exact for the same assignment, and up to 16.9
  nats of candidate error at n = 1. The first screen's stored numbers
  are untouched by this (it re-evaluated the best assignment exactly;
  the drift lived in the search path alone). This measurement repairs
  the rule.
- The repaired machinery, declared before the run: an exact greedy
  reassignment climb. For every symbol with self-pair count n and
  current label c, each candidate label l is evaluated as the exact
  new total of the symbol's pairs, with the self-pair correction
  included (candidates[l] = best - hold + outbound[l] + inbound[l] -
  n table[l, c] - n table[c, l] + n table[l, l], hold the symbol's
  exact current contribution), adoption only on strict improvement
  beyond 1e-12 against the running best, the running best updated
  only by exact candidate values, and the returned total the exact
  re-evaluation of the tracked assignment. Verified against brute
  force to 9.1e-13 on the probe's matrices and again in the tests.
- The held-out split, declared before the run: each side's counted
  pairs are pooled as one flat ordered pair list in stream order and
  split by pair-index parity - even-index pairs form the climb half
  the machinery may search, odd-index pairs the score half it may
  never touch. The truthful structure statement, corrected between
  this artifact's first generation and its frozen form with the
  numbers verified unchanged (see the section at the end): the halves
  share no counted pair and together they are the flat list; within
  each half, pairs two indices apart share no symbol; across the
  halves, adjacent pairs share a symbol position by construction
  (every interior position carries one climbed pair and one scored
  pair), so the score half is fresh to the search at the pair level
  but is not an independent sample of the stream. Both halves' sizes
  are recorded per cell (ZL 109208 + 109207 of 218415 counted; GC
  91600 + 91599 of 183199; IT 110266 + 110265 of 220531).
- Held-out machinery: the climb runs only on the climb half (rank
  initialisation from the climb half under the declared wrap, restarts
  1 to 15 seeded permutations, best among restarts the best exact
  climb-half total with ties to the first restart). The reported
  number is the chosen assignment's mean nats per scored pair on the
  score half, evaluated exactly; the chosen assignment's climb-half
  mean is recorded beside it for the real. No assignment is returned,
  stored or published anywhere.
- Anchors and rules: the planted anchor is the true configuration's
  score-half identity, algebraically the truncated stream's
  odd-half identity mean; plant parity unchanged (at or above anchor
  minus 0.0001 passes, above counts as parity with the excess recorded
  as machinery-above-anchor); floors redrawn from the declared seeds
  must stay below the real; the band keeps the same seven unconditional
  members, a member's value being the held-out value of the draw whose
  exact climb-half total is best (ties to the first draw), its five
  draws, climb-half and full-data side values and spreads all recorded,
  the smallest member value setting the threshold.
- A side instrument, declared before the run: the same exact climb
  over the unsplit full data for the real, every plant, every floor
  and every member's five draws, recorded for attribution only - to
  show what the first screen's stored values look like under the
  repaired rule - and no verdict is built on it.
- Verdict rule and exclusion format carried unchanged from the first
  screen, now on the held-out values: real at or above the smallest
  member value is consistent-with-substitution; real below it is
  below-held-band; real at or below the largest floor is
  not-consistent; an exclusion needs the real below the smallest
  member value in all six cells with plant parity green and every
  floor below the real.
- Finding (b), the pre-run design probe disclosed verbatim in the
  docstring: 12 machinery calls and 204 exact climbs, zero cap hits.
  English (identity -5.1422, held-out anchor -5.1430): full-exact
  bests -4.7533 to -4.7256 (identity plus 0.389 to 0.417), held-out
  -4.7514 to -4.6625 (plus 0.392 to 0.481); the first screen's stored
  excesses had the same magnitude, so its exploit was real, not search
  drift. Latin (identity -5.0742, held-out anchor -5.0755): full
  -4.5772 to -4.5764 (plus 0.497 to 0.498), held-out -4.5771 to
  -4.5775 (plus 0.498). Exploitation is systematic across the split;
  the held-out statistic prices the data-specific component only.

## The measured facts

- Plant parity survives the repair: all 30 plants pass (30 of 30),
  held-out excesses 0.391 to 0.499 nats per scored pair. Zero cap hits
  anywhere.
- Floors: every one of the 30 floors stays below its cell's real
  held-out value, by 0.736 to 0.879 nats per scored pair.
- The real's held-out values: -4.4252 (ZL english), -4.3743 (ZL
  latin), -4.3534 (GC english), -4.4318 (GC latin), -4.3878 (IT
  english), -4.3707 (IT latin). Band minimum and maximum per cell:
  ZL english -4.6997 to -4.6712; ZL latin -4.6081 to -4.5788; GC
  english -4.6989 to -4.6362; GC latin -4.6081 to -4.5788; IT english
  -4.6992 to -4.6354; IT latin -4.6081 to -4.5788.
- The verdicts per the declared rule: all six (file, language) cells
  consistent-with-substitution. The real's held-out value stands ABOVE
  the smallest member value everywhere, by 0.2745 (ZL english), 0.2338
  (ZL latin), 0.3455 (GC english), 0.1763 (GC latin), 0.3114 (IT
  english) and 0.2374 (IT latin) nats per scored pair.
- Machinery budget: 342 machinery calls in the frozen run, 16 exact
  restarts each (5,472 exact greedy climbs), and not one call or
  climb hit the declared cap of 200 - the repaired exact rule simply
  converges, so no stored number is a budget truncation this time.
- Side instrument: the real's full-data exact values -4.3527 to
  -4.4437; the plants' full-data exact values sit in the first
  screen's stored region (ZL english plants -4.7411, -4.7256, -4.6595,
  -4.7256, -4.7256 against the first screen's stored -4.7417, -4.7256,
  -4.7411, -4.7256, -4.7256: four of five equal to four decimals and
  one higher), consistent with the first screen's drift having lived
  in the search path only and not manufacturing its stored excesses.

## The exclusion format's outcome, stated exactly

The declared exclusion required the real's held-out value below the
smallest member value in all six cells. The measured outcome is the
opposite direction everywhere, so the format's condition is not met:
family 5 stays open. No cell is excluded and no cell is closed. The
direction question the first handoff posed - does the verdict reverse
when the exploitation is priced out - is answered no by the measurement.

## The disclosure the verdicts ride on

The held-out statistic was designed to stop paying the search's
exploitation, and it did not stop the real: under the repaired exact
rule every side still climbs past its own truth configuration, the
planted encodings by 0.391 to 0.499 and the first screen's disclosed
systematic shape carries across the split intact. What the held-out
pricing isolates is therefore only the data-specific component, and on
that component the real still stands 0.176 to 0.346 above the band in
all six cells. Within this instrument the screen cannot separate the
manuscript's statistics from homophonic encodings of the sampled
English and Latin proeses: the class is NOT excluded by this artifact,
and no positive identification of a cipher is claimed either. The
score half is not an independent sample of the stream (the declared
interleaving structure above); it is fresh to the search in the pair
sense, which is the property the instrument actually uses.
plaintext_recovered_percent stays 0, no mapping is published, nothing
here is a reading.

## Between the first generation and the frozen artifact

The artifact was generated once under the declared design (41.6
seconds), and its declared split_rule wording then claimed the halves
share no symbol position - which is false across halves for adjacent
pairs. The module's declared wording (docstring paragraph, split
helper's docstring and the split_rule string) was corrected to the
truthful pair-level statement above, and the artifact was regenerated
from the corrected module: every number and every other string
reproduced exactly, the wording alone changed, and the regenerated
artifact is the frozen one. The measurement itself never changed.

## Next

Family 5 stays open at priority 1. The measured next question this
artifact hands to the ledger: price the disclosed add-one exploitation
against the surplus capacity that feeds it - a surplus-capacity ladder,
declared before any run, re-measuring the same six cells with the
mapped budget stepped down through 36, 33, 30 and 27 glyphs plus the
boundary mark (plants and band members re-encoded per budget through
the same declared partition rule from the same declared kinds, floors
unchanged), so the machinery's reassignment space narrows with every
rung. Truthful question declared in advance: does the real's margin
above the band shrink as the surplus is removed, and does any rung
separate the real from the band; if none does, say so and keep the
family open with the disclosure. Family 4's exclusion stands untouched
by this artifact's outcome.
