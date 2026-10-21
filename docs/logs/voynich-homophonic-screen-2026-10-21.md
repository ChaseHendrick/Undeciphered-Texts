Voynich MS: the homophonic screen - 21 October 2026

Eleventh execution step for the Voynich case, and family 5's first
measurement, declared in `engine/voynich_homophonic.py`'s docstring
before any run of the module. The family question: is it a homophonic
substitution of a known language - several cipher symbols sharing one
plaintext letter - after family 4's five measurements excluded the
scoped one-to-one substitution class by count at bigram and trigram
resolution?

## Declared design of this run

- The identical frozen streams, references and add-one bigram table as
  the substitution family; the mapped set widened before the run from
  26 glyphs plus the word-boundary mark to the file's most frequent
  glyph characters up to 36 plus the mark (37 cipher symbols over the
  model's 27 letter tokens), because a homophonic cipher needs surplus
  symbols, and every file's glyph pool supplies well over 36 distinct
  characters. Word divisions carried; pairs across a boundary slot
  counted exactly as family 4's bigram counts count them.
- The search changed shape with the hypothesis: a declared greedy
  reassignment hill-climb over assignments from the 37 cipher symbols
  onto the 27 letter tokens (one pass per sweep in symbol order, 27
  exact candidate-label deltas per symbol from the running score,
  adoption only on strict improvement beyond 1e-12, the best
  assignment's score re-evaluated exactly so no incremental drift
  reaches any stored number), sweep cap 200 and restarts 16 inherited,
  restart 0 the frequency-rank initialisation with surplus symbols
  wrapping (k modulo 27), restarts 1 onward seeded permutations under
  the same wrap rule.
- A pre-run design probe on the implementation, disclosed in the
  docstring before the run and decisive for the declared pass rule: on
  a planted encoding, a climb started at the planted configuration's
  own key rises ABOVE that key's score - the add-one model is
  exploitable under the richer assignment space - and keeps improving
  at the declared cap. Consequences declared in advance: the sweep cap
  is a declared budget applied identically to the real, every plant,
  every floor and every band draw; each machinery call records whether
  its best climb hit the cap; a plant passes when its best is at least
  its anchor minus 0.0001, with best-above-anchor counted as parity
  and the excess recorded as machinery-above-anchor.
- Plants: five per (file, language), each the truncated first
  reference stream encoded by a declared partition rule (floor shares
  of frequency, one slot at least per present letter, remainder by
  largest fractional remainder with ties to the ascending letter
  index, groups laid out by descending letter frequency so the most
  frequent letter receives the most frequent glyphs) and sampled by
  one uniform draw per position from its letter's group, boundary
  positions taking the mark without a draw. The anchor per cell is the
  truncated reference stream's identity score under the same model,
  algebraically the plant's own true-key decoding score whatever the
  sampled choices are.
- Floors: five per (file, language), the real stream's kept ids
  shuffled inside the kept positions.
- Cross band: the seven class members of family 4's widened band,
  each truncated by the standing rule and encoded under the same
  partition rule, five encodings per text through the declared
  sequential scheme (one sampling rng draws the five encodings in
  order, one machinery rng runs the five climbs in order, the text
  position in the seed). Band membership for this family declared
  unconditional: a member's value is its five-draw machinery best,
  all draws and spreads recorded, the smallest member value setting
  the band threshold. The family 4 agreement gate was deliberately
  not carried over, because this family's noise is systematic
  cap-truncation shared by both sides, not the stuck-draw pathology
  the gate was built for.
- Seed kinds declared before the run: real from kind 1 exactly as the
  substitution family declares it, homophonic plant sampling 24 and
  machinery 25 (the plant index), floor permutation 26 and machinery
  27 (the floor index), cross sampling 28 and machinery 29 (the text
  position); the base seed [20261020, cell, kind, lang, index]
  unchanged, kinds 24 to 29 consumed by no other module.
- Verdict rule declared before the run: real at or above the smallest
  member value is consistent-with-substitution; real at or below the
  largest floor is not-consistent; strictly between is
  below-homophonic-band; machinery-noise-unresolved retained formally
  for a memberless band, which cannot arise. Exclusion format
  declared before the run: an exclusion needs the real below the
  smallest member value in all six cells with plant parity green and
  every floor below the real; any other outcome keeps the family
  open with the disclosure.

## The measured facts

- Plant parity survives the richer search: all 30 self-parity plants
  are at or above their anchors (30 of 30 pass), with the disclosed
  machinery-above-anchor excess of 0.3922 to 0.4970 nats per counted
  pair - the systematic shape the pre-run probe predicted. All 30
  plant machinery calls hit the declared sweep cap.
- Floors: every one of the 30 floors stays below its cell's real
  value, by 0.69 to 0.99 nats per counted pair (real above the
  largest floor).
- The real re-measured under the wider alphabet and the reassignment
  search: -4.4149 (ZL english), -4.5125 (ZL latin), -4.3527 (GC
  english), -4.3896 (GC latin), -4.4136 (IT english), -4.5027 (IT
  latin). Every one of the six real machinery calls hit the declared
  cap; the counts (218415, 183199, 220531 counted pairs per file)
  reflect the wider mapped set.
- The band: member values -4.5826 to -4.7021 per cell (all 35 band
  draws recorded with their spreads, drawn values -4.5774 to
  -4.7552), each member's value 0.46 to 0.62 above its own anchor -
  the same systematic excess the plants carry.
- The verdicts per the declared rule: all six (file, language) cells
  consistent-with-substitution. The real's best stands ABOVE the
  smallest member value everywhere, by 0.1061 to 0.3494 nats per
  counted pair.

## The exclusion format's outcome, stated exactly

The declared exclusion required the real below the smallest member
value in all six cells. The measured outcome is the opposite direction
everywhere, so the format's condition is not met: family 5 stays open.
No cell is excluded and no cell is closed.

## The disclosure the verdicts ride on

The consistent verdicts are measured behaviour of the declared
machinery, and the machinery's systematic property is disclosed in the
artifact and here: under the homophonic assignment space the add-one
model is exploitable, every climb reaches past its data's own identity
score (plants 0.39 to 0.50 above their anchors, band members 0.46 to
0.62 above theirs), and the real text gained more from the freedom
than the class did - against family 4's bigram-screen real values of
-5.2541 to -5.3883, the same streams through the same models under the
wider alphabet and reassignment search gained 0.79 to 1.00 nats per
counted pair. All 101 machinery calls of the frozen run hit the
declared sweep cap, so every stored number is a declared-budget
truncation, identical in kind on both sides of every comparison. What
the rule's consistent verdicts therefore establish: under this
machinery and its disclosed excess, the screen cannot separate the
manuscript's statistics from homophonic encodings of the sampled
English and Latin proeses - the class is NOT excluded by this
artifact, and no positive identification of a cipher is claimed
either. plaintext_recovered_percent stays 0, no mapping is published,
nothing here is a reading.

## Next

Family 5 stays open at priority 1. The measured next question this
artifact hands to the ledger: separate class-shaped exploitation from
text-like structure inside the homophonic machinery - the declared
path is a held-out scoring variant that scores each recovered
assignment on data the climb did not see, so the add-one exploitation
no longer pays, and to re-measure the same six cells under it before
any real value is read. Family 4's exclusion stands untouched by this
artifact's outcome.
