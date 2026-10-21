"""Statistical screen for a homophonic-substitution hypothesis of the
Voynich manuscript, the first declared measurement of family 5.

Family 5 was declared open in the ledger on 21 October 2026, after
family 4's five measurements excluded the scoped one-to-one
substitution class by count at bigram and trigram resolution. This
module is declared here, in its own docstring, before any run of it,
and no number inside this module has been seen.

First declared measurement, the homophonic screen, declared in full
before the run: the identical frozen reference models as the
substitution family - the same add-one bigram table built from the
same two first reference proeses under the identical declared
processing (the pair table exactly as family 4's table_from_stream
declares it), the same frozen real transcriptions rendered to
streams, and the same frozen class members. What changes is the
cipher hypothesis and with it the search space: a homophonic mapping
allows several cipher symbols to share one plaintext letter while
every cipher symbol still names exactly one letter, so the search is
a declared reassignment climb over assignments from the cipher symbol
set onto the model's 27 letter tokens, not a permutation climb. The
mapped set is wider than family 4's, declared before the run: the
file's most frequent glyph characters up to 36, ranked by the same
(descending count, character) rule family 4 uses, plus the
word-boundary mark in the last position - 36 glyph slots over 26
letters with room for the surplus a homophonic cipher needs, every
file's glyph pool supplying at least 36 distinct characters. Word
divisions are carried: the word-boundary mark keeps the same declared
search freedom family 4 gave it, one more symbol whose label the
climb may move, and pairs across a boundary slot count exactly as
family 4's bigram counts count them.

Declared machinery, before the run: states are assignments f from the
37 cipher symbols (36 glyphs plus the boundary mark) onto the model's
27 letter tokens (26 letters plus the space token); the statistic is
the best mean nats per counted pair, the assignment score summed over
the symbol pair count matrix times the model table and divided by the
counted pairs. The climb is a greedy reassignment hill-climb: symbols
in index order, one full pass per sweep; for each symbol its 27
candidate labels are evaluated exactly from the running score (its
outbound pairs, its inbound pairs, and its diagonal removed once),
and a label is adopted only on a strict improvement beyond 1e-12,
otherwise the symbol stays put; ties of the argmax move nothing
because adoption needs the strict improvement. The best assignment
reached is returned with its exact re-evaluated score, so no
incremental drift reaches any stored number. Sweep cap 200 inherited,
restarts 16 inherited: restart 0 is the declared frequency-rank
initialisation with the surplus symbols wrapping (the k-th most
frequent symbol starts at the k-th most frequent letter, k modulo 27;
the boundary mark starts and moves like any symbol); restarts 1
onward start from a seeded permutation of the 27 letter tokens under
the same wrap rule; each restart consumes one deterministic
permutation draw in order. The add-one model is exploitable under the
richer assignment space - a pre-run design probe on the implementation
(found a climb from the planted configuration rising above the
planted key's own score, still improving at the declared cap), so
this family's declared machinery embraces the cap: the sweep cap is a
declared budget applied identically to the real, every plant, every
floor and every band draw, and each machinery call records whether
its best climb hit the cap. The comparison stays apples to apples:
both sides are scored through the identical declared climb at the
identical declared budget, and any under-convergence truncates both
sides' recoveries the same way.

Declared power instruments, all before the first real number is read:

- Plant parity through an encoder, not a decoder. Each plant is the
  truncated first reference stream encoded into the file's mapped
  cipher alphabet by a declared encoder: the truncation follows the
  standing rule (min of the real stream's total events and the
  reference stream's length); the encoder's partition rule, declared
  here, splits the 36 glyph slots over the letters present in the
  truncated stream - floor shares of frequency, one slot at least per
  present letter, remaining slots by largest fractional remainder
  with ties to the ascending letter index, groups laid out letter by
  letter in descending letter frequency so the most frequent letter
  receives the most frequent glyphs, a zero-share present letter
  taking one slot from the largest existing group. The encoder
  samples each plaintext position's cipher symbol by one uniform
  declared draw per position from its letter's group, in stream
  order; the boundary positions take the boundary mark without a
  draw. The anchor, resolved before the run: the plant's own
  true-key decoding score is algebraically the truncated reference
  stream's identity score under the same declared model whatever the
  sampled choices are, so the anchor per (file, language) cell is
  that identity value, recorded in the artifact. The declared pass
  rule, declared with the pre-run probe's finding in mind: a plant
  passes when its machinery best is at least the anchor minus 0.0001
  on its own data - exactly equal counts as parity, exactly as family
  4 planted parity was counted, and best above the anchor counts as
  parity with the excess recorded and disclosed as
  machinery-above-anchor, because the point of the instrument is the
  machinery finding the planted configuration's optimum and an exact
  higher value is the machinery working, not failing; a plant below
  the anchor by more than 0.0001 fails parity and is recorded - and
  under that rule a system of cap-truncated recoveries still states
  the instrument's truth, that the machinery recovers everything the
  planted assignment can achieve.
- Plant budget: five plants per (file, language), each with its own
  declared seed pair (one sampling rng, one machinery rng), drawn
  independently by plant index.
- Floors: five multiset floors per (file, language), the real
  stream's kept ids shuffled inside the kept positions by a declared
  per-floor-index rng, scored by the same machinery; every floor must
  land below the real.
- Cross band: the seven frozen class members of family 4's widened
  band - English (Frankenstein, Moby Dick, Le Morte d'Arthur volume
  1) and Latin (Caesar's De Bello Gallico I-IV, Vulgate Daniel,
  Colloquium heptaplomeres, De Rariorum Animalium atque Stirpium
  Historia) - each truncated by the standing rule and encoded under
  the same declared partition rule through a per-text sequential
  drawing scheme following family 4's widened scheme exactly: one
  sampling rng draws the five encodings of a text in order, one
  machinery rng runs the five climbs in order, the text position in
  the seed. Band membership for this family is unconditional and
  each member's band value is its five-draw machinery best, because
  the pre-run probe's finding put the noise of this family in kind
  and in place: the cap-truncated recoveries vary systematically
  above the members' identity anchors, disclosed and recorded, on
  both sides of the comparison - so the family 4 agreement gate is
  not carried over, the five draws of each member are recorded with
  their exact values and spread, and the smallest member value sets
  the band threshold for its cell. The special outcome
  machinery-noise-unresolved remains declared for a cell in which no
  member is recoverable at all, which cannot arise while class
  members exist; it is retained formally for completeness.

Declared seed kinds, before the run: the real recomputes from kind 1
under the standing seed scheme _seed = [20261020, cell, kind, lang,
index] with the SAME declared seed kind 1 the substitution family
uses, so the real's replay key stays comparable in spirit across
families while this artifact's own kinds are 24 to 29: homophonic
plant sampling 24, homophonic plant machinery 25 (the plant index);
homophonic floor permutation 26, homophonic floor machinery 27 (the
floor index); homophonic cross sampling 28, homophonic cross
machinery 29 (the text position in the seed). No number drawn by this
module's seeds is consumed by any other module's declared draws.

Declared verdict rule, before the run: the real at or above the
smallest member value is consistent-with-substitution; the real at
or below the largest floor is not-consistent; strictly between is
below-homophonic-band; and the formal special outcome
machinery-noise-unresolved is retained for a memberless band, which
cannot arise. Declared exclusion format, agreed here before the run:
if the real text stands below the smallest member value in all six
(file, language) cells with plant parity green and every floor below
the real, then the scoped homophonic class - several cipher symbols
per plaintext letter inside the declared 36-slot mapped alphabet,
word divisions carried, no abbreviation, no transposition, no nulls,
the sampled reference population - is excluded by count for the
manuscript's statistics as measured, and the family closes with that
wording plus the standing caveats (abbreviated scribal usage outside
the class, population sampled not exhaustive, nothing is a reading,
no mapping published). If any cell flips otherwise, the family stays
open with the disclosure, exactly as the ledger's family 4 arc
demanded before its own closure.

Second declared measurement, the held-out homophonic screen, declared
after the first screen's six consistent-with-substitution verdicts and
before its own run, and declared around two disclosed pre-run
findings.

Finding (a), disclosed: the first screen's climb was declared as an
exact candidate evaluation, but its implemented rule evaluates
candidates exactly at the current label only. For a symbol s with
self-pair count n = matrix[s, s] and current label c = f[s], its
implemented candidates for other labels l misstate the exact new
totals by n * (t[l, c] + t[c, l] - 2 * t[l, l]), t the declared
add-one table; a brute-force check on one random small matrix with
n = 1 measured candidate errors up to 16.9 nats, and the errors
compound across a climb's adoptions into drifting walk-time totals -
on that small matrix the walk-time total reached +23430 nats where the
returned assignment re-evaluated to -20520. Every stored number of the
first screen's artifact still stands: that module re-evaluates the
returned assignment exactly, so the recorded scores are exact scores
of real assignments, and the real, plants, floors and band were scored
through one shared machinery, so the recorded comparisons remain
comparisons through that machinery. The drift was a search-path
phenomenon; this measurement repairs the rule and measures again.

Finding (b), disclosed: the exact greedy reassignment climb, verified
against brute force to 9.1e-13 and run on the first screen's
instruments, keeps the disclosed exploitation of the add-one table
above a planted key alive while converging far before the declared
cap. Disclosed pre-run probes ran on ZL's truncated English and Latin
streams, three planted encodings per language, every encoding through
both the held-out call and the exact full-data side call, twelve
machinery calls, 204 exact climbs, none reaching the sweep cap.
English: the truncated plant stream is 218,662 plaintext pairs,
splitting to 109,331 climb and 109,331 score pairs; the identity score
is -5.1422 nats per pair over the full stream and -5.1430 over the
score half. The exact climb's bests on the full planted data ran from
-4.7533 to -4.7256, excesses +0.389 to +0.417 over the full-stream
identity, the same magnitude as the first screen's stored plant
excesses for this cell (0.4005 to 0.4166), so the first screen's
recorded exploitation measured a real exploit and not the drift; the
held-out values ran from -4.7514 to -4.6625, excesses +0.392 to +0.481
over the held-out anchor. Latin: identity -5.0742, held anchor
-5.0755; full-data exact bests from -4.5772 to -4.5764, excesses
+0.497 to +0.498; held-out values -4.5771 to -4.5775, excesses +0.498
for all three. The exploitation is systematic across the split: both
halves are drawn from one generated structure and the exploit rides
the model's shape, so the held-out statistic prices the data-specific
component only; that is the declared instrument's honest reach and
this artifact records it.

The held-out split, declared before the run: each side's counted pairs
are pooled as one flat ordered pair list - the real stream's occupied
adjacent pairs under the first screen's pair rule, every plant's and
every band member's full consecutive pairs of its encoded stream, and
every floor's occupied adjacent pairs after its declared shuffle -
then split by pair-index parity: even-index pairs form the climb half
the machinery may search, odd-index pairs the score half it may never
touch. The halves share no counted pair: every pair of the flat list
belongs to exactly one half, and within each half pairs two indices
apart share no symbol. Across the halves the pairs are interleaved
and every interior symbol position carries one climbed pair and one
scored pair, so the score half is fresh to the search at the pair
level but is not an independent sample of the stream; it prices the
chosen assignment once after the search and returns nothing of it to
the machinery. The split is deterministic, consumes no seed, and both
halves' sizes are recorded per cell.

The machinery, declared before the run: the exact greedy reassignment
climb of finding (b) - candidates the exact new totals, the running
best updated only by exact candidate values, adoption only on strict
improvement beyond 1e-12 - runs only on the climb half. Restart 0 is
the rank initialisation computed from the climb half under the
declared wrap rule; each later restart consumes one seeded permutation
of the 27 letter tokens under the same wrap rule; among the restarts
the best is the best exact climb-half total with ties to the first
restart, so every choice of the search reads only data its climbs
saw. The reported held-out number is the chosen assignment's mean nats
per scored pair on the score half, evaluated exactly, and the chosen
assignment's climb-half mean is recorded beside it for the real. No
assignment is returned, stored or published anywhere in this
artifact. Every machinery call records whether any of its climbs
reached the declared sweep cap 200, which finding (b) says does not
happen under the exact rule.

Seed sharing, declared before the run: this measurement consumes no
new seed kinds. The real recomputes from the standing kind 1 under the
standing seed scheme; the plants are the first screen's encodings
replayed from kinds 24 and 25, the floors its shuffles replayed from
kinds 26 and 27, the band members its encodings replayed from kinds 28
and 29, and every restart permutation is the first screen's declared
permutation draw for the same call, replayed in the same order; the
side instrument's separate rng object replays the same declared draws.
The split adds no draw; nothing is redrawn.

Anchors, declared before the run: a plant's anchor is its true
configuration's mean nats per pair on the score half - algebraically
the truncated plaintext stream's odd-half identity mean under the same
declared table, whatever the sampled choices are - recorded per cell
with the climb-half identity mean and both half sizes for context.
Band members carry the same anchor rule per member text. Plant parity
keeps the first screen's declared rule on the held-out statistic: a
plant passes at or above its anchor minus 0.0001, an exact pass counts
as parity, a best above the anchor counts as parity with the excess
recorded and disclosed as machinery-above-anchor, and a plant below
the anchor by more than 0.0001 fails parity and is recorded.

Floors, declared before the run: the first screen's destroyed-adjacency
multiset shuffles, redrawn from their declared seeds, split by the
same rule, each scored by the same held-out machinery; every floor
must land below the real's held-out value.

Band, declared before the run: the seven unconditional members of the
first screen - English (Frankenstein, Moby Dick, Le Morte d'Arthur
volume 1) and Latin (Caesar's De Bello Gallico I-IV, Vulgate Daniel,
Colloquium heptaplomeres, De Rariorum Animalium atque Stirpium
Historia) - each re-encoded under the first screen's per-text
sequential scheme from its declared kinds, each producing five draws;
all five held-out values, their climb-half means, their cap hits and
their spread are recorded, and the member's band value is the held-out
value of the draw whose exact climb-half total is best among the five,
ties to the first draw; the smallest member value sets the band
threshold for its cell; the special outcome machinery-noise-unresolved
is retained formally for a memberless band, which cannot arise.

A disclosed side instrument, declared before the run, attribution
only: the identical exact climb over the unsplit full data of each
cell's real, five plants and five floors, and of every band member's
five draws, all values and cap hits recorded beside the held-out ones,
so the first screen's two effects - the surrogate drift and the add-one
exploitation - can be attributed separately and the exact rule's
agreement with the first screen's stored magnitudes is measured on the
declared data in the artifact. No verdict is built on the side
instrument.

Declared verdict rule, before the run: the real's held-out value at or
above the smallest member band value is consistent-with-substitution;
the real's held-out value at or below the largest floor's held-out
value is not-consistent; strictly between is below-held-band.
Declared exclusion format, agreed here before the run: if the real
text stands below the smallest member band value in all six (file,
language) cells with plant parity green and every floor's held-out
value below the real, then the scoped homophonic class - several
cipher symbols per plaintext letter inside the declared 36-slot mapped
alphabet, word divisions carried, no abbreviation, no transposition,
no nulls, the sampled reference population - is excluded by count for
the manuscript's statistics as measured, and the family closes with
that wording plus the standing caveats (abbreviated scribal usage
outside the class, population sampled not exhaustive, nothing is a
reading, no mapping published). If any cell flips otherwise, the
family stays open with the disclosure, per the ledger's declared next
for family 5. The truthful question declared in advance: does the
direction of the verdicts reverse when the surrogate drift is repaired
and the data-specific part of the exploitation is priced out; if the
class is still not separated, the artifact says so and the family
stays open with the disclosure. A consistent verdict under the
held-out statistic is NOT read as a cipher identification, exactly as
in the first screen.

The standing limitations are inherited from the first screen: no
mapping is published anywhere in this artifact, no recovered
assignment is stored as a key, plaintext_recovered_percent stays 0,
the reference prose is modern printed text outside the manuscript's
century, and nothing here is a reading or a language claim.

Wording correction, recorded when the third measurement was declared
and before any run of it: the first measurement's declaration above
said the mapped set took the file's most frequent glyph characters
"every file's glyph pool supplying at least 36 distinct characters".
That supply clause is false for IT, whose glyph pool is 23 distinct
characters, ranking below the 36 slots; the implementation has always
taken ranked[:36] of whatever pool exists, so IT's mapped set has been
23 glyphs plus the mark (24 used cipher symbols, the remaining slots
riding zero pairs) in both frozen artifacts, and no number, seed draw
or comparison of either stored artifact involved the false clause.
The clause is corrected here; its correction affects no frozen value.

Third declared measurement, the surplus-capacity ladder, declared
after the held-out screen's six consistent-with-substitution verdicts
and before any run of it, around disclosed pre-run probes.

The declared design, before the run: the same six (file, language)
cells, the same frozen streams, references and add-one bigram models,
the same machinery, the same held-out split, the same restart and
sweep budgets, re-measured as the mapped budget steps down through
36, 33, 30 and 27 glyph slots plus the word-boundary mark - the word
boundary riding every rung. The truthful question, declared in
advance: does the real's margin above the band shrink as the surplus
is removed, and does any rung separate the real from the band; if
none does, the artifact says so and the family stays open with the
disclosure. The ladder prices the disclosed add-one exploitation
(the machinery narrows its reassignment space with every rung)
against the real's held-out margin, and adds no exclusion format of
its own: the family's declared exclusion keys to the 36-slot class,
so the rung verdicts are rung-level evidence on narrower subclass
encodings, and the family stays open unless the top rung itself
reverses.

The rung rules, declared before the run:

- The real's re-render rule at budget B: the file's most frequent
  glyph characters up to B, ranked by the declared (descending count,
  character) rule, plus the word-boundary mark in the last position.
  A glyph character outside the rung's set renders to the dropped
  event (id -1, never kept) and pairs across a dropped event do not
  count, exactly as the first screen's mapped-set rule renders
  characters beyond its count. IT's pool is 23 glyphs, so IT's real
  takes its full pool at every declared rung (24 used cipher symbols,
  its real stream unchanged across rungs) and the disclosed budget
  narrowing for IT lives wholly on the encoders' side.
- Plants and band members re-encode per rung through the same
  declared partition rule - floor shares of frequency, one slot at
  least per present letter, remaining slots by largest fractional
  remainder with ties to the ascending letter index, groups laid out
  letter by letter in descending letter frequency - each instrument
  replaying its declared seed kind per (rung, instrument, index),
  so identical seeds draw identically at identical budgets and the
  narrower rungs draw from the same declared seed values.
- Floors unchanged in declaration (floor shares stay 5 per cell, kind
  26 per floor index, the machinery kind 27 per floor index):
  destroyed-adjacency shuffles of the rung's real kept ids, scored by
  the same held-out machinery, every floor required below the rung's
  real. A floor has no plaintext, so nothing about it re-encodes;
  it rides the rung's stream because the stream is re-rendered.
- The machinery, split, anchors and budgets are rung-invariant in
  definition: the exact greedy reassignment climb on the even-index
  climb half and exact pricing on the odd-index score half, restart 0
  the rank initialisation from the climb half, restarts 1 onward the
  same seeded permutations of the 27 letter tokens, sweep cap 200,
  16 restarts at every rung and for every side. The models, the
  truncated streams and therefore the anchors are rung-invariant
  (an anchor is the truncated plaintext's odd-half identity mean
  under the unchanged table). The exact full-data side call is
  carried per rung beside every held-out value for attribution only
  and no verdict is built on it. No assignment is returned, stored
  or published anywhere.
- Verdict rule per rung, unchanged: the rung's real held-out at or
  above the rung's smallest member band value is
  consistent-with-substitution; at or below the rung's largest
  floor's held-out value is not-consistent; strictly between is
  below-held-band. Margins are computed from the stored rounded
  values: real held-out mean minus smallest member band value,
  rounded to four decimals.
- A reproduction gate, declared before the run and enforced in code:
  the rung at budget 36 must reproduce the frozen held-out artifact
  field for field - every cell field (real held-out, climb, full side
  and pair counts, plants, floors, excesses, cap flags, anchors,
  band members' every field, band minima and maxima, verdicts) and
  the declared language models - checked immediately after the top
  rung is measured and before any narrower rung runs; any
  divergence aborts the ladder and no artifact is written.

Pre-run probes, disclosed verbatim, on frozen data through the
declared implementation before the artifact run. Probe 1, the
partition rule at the narrow rungs on the truncated streams
(cell ZL's truncation, shared by the band): english 26 present
letters, budget 27 gives 26 groups sized 1 to 2 summing to 27 with
zero zero-share letters, budget 33 gives 26 groups sized 1 to 4
summing to 33; latin 25 present letters, budget 27 gives 25 groups
sized 1 to 3 summing to 27, budget 33 gives 25 groups sized 1 to 4
summing to 33. Probe 2, the top rung's real streams equal the frozen
streams field for field for all three files (event ids, kept mask,
mapped characters, total events). Probe 3, ZL english through the
declared machinery at the top rung: counted 218,415 (climb 109,208,
score 109,207), real held-out -4.4252, climb view -4.4313, cap
False, identical to the held-out artifact's frozen cell; at the
narrowest rung 27: counted 218,309 (climb 109,155, score 109,154),
real held-out -4.4259, climb view -4.4301, cap False, the real's
held-out number already seen to move by 0.0007 nats between the
top and narrowest rungs while the reassignment space narrows from 37
to 28 cipher symbols. The remaining numbers inside this module are
unseen until the declared runs.

The standing limitations are inherited from the held-out screen: no
mapping is published anywhere in this artifact, no recovered
assignment is stored as a key, plaintext_recovered_percent stays 0,
the reference prose is modern printed text outside the manuscript's
century, and nothing here is a reading or a language claim.

Fourth declared measurement, the shape-priced re-measure, declared
after the ladder's no-shrink, no-separation outcome put the score
table's shape under suspect and before any run of it, around disclosed
pre-run probes.

The declared design, before the run: the held-out screen's six (file,
language) cells, plants, floors and band re-measured at the top budget
with the mapped set (36 glyphs plus the word-boundary mark), streams,
held-out split, seed kinds, machinery, restart and sweep budgets
unchanged, and the declared score table rebuilt in an
exploitation-resistant leave-one-out form. The truthful question,
declared in advance: does the real's margin above the band survive a
model the climb cannot feed on - a yes says the margin rides the
manuscript's statistics, a no records which instrument carried it. The
family's declared exclusion format is not re-scoped by this artifact:
it keys to the declared 36-slot class under the inherited add-one
form exactly as the held-out screen declared it, so the verdicts
recorded here are shape-instrument evidence on the declared table
form, and the family stays open unless the declared exclusion fires.

The leave-one-out form, declared before the run: the inherited
add-one form of the reference pair table is log((n_ab + 1)/(N + 729))
with N the reference stream's total counted pairs; in the
leave-one-out form every pair type (a, b) present in the reference
pair table is scored with one occurrence of (a, b) removed from the
reference counts, log(n_ab/(N + 728)), and a type with no counted
occurrence keeps the inherited add-one entry log(1/(N + 729)) - every
occurring type is re-priced one occurrence more severely and the
unseen-type floor is unchanged. The letter marginals are the
reference's unigram counts, unchanged: the rank initialisation
consumes the same marginals and starts identically to the held-out
screen, and the declared conditional on re-deriving the matrix
arithmetic resolves as not needed - the model stays the reference's
aggregate and the score one fixed 27 x 27 table per language summed by
assignment aggregation (the sum over pair occurrences of table[first
label, second label]), so the declared matrix-product form survives
without re-derivation. The encodings and the floor shuffles are
byte-identical replays of the frozen measurement's declared draws:
only the scoring changes, and no new seed kind is consumed.

A bridge gate, declared before the run and enforced in code: before
the leave-one-out cells run, this measurement's full first cell (ZL
english: the real, its five plants, its five floors and its three band
members) computed under the inherited add-one table must equal the
held-out screen's own outputs field for field; any divergence aborts
and nothing is written. Each band member additionally records
draws_climb_exact, its five climb-half totals at full precision, as
the ladder's regenerated artifact disclosed, so the declared selection
stays re-derivable from the stored artifact. Verdict and margin rules
are the held-out screen's rules applied to the leave-one-out-scale
numbers; the verdict strings describe consistency under this
artifact's declared form and do not restate the add-one form's
verdicts, and the margin is computed from the stored rounded values as
the ladder's artifact declared.

Pre-run probes, disclosed verbatim, on frozen data through the
declared implementation before the artifact run. Probe 1, the
leave-one-out form's shape facts: english 490 pair types present of
729 over 692,526 counted pairs, the largest single-entry repricing
0.693146 nats (log 2, at any type counted once; highest at type
(0, 9), add-one -12.756020 to leave-one-out -13.449166), the mean
repricing over occurring types -0.065165 nats, and the reference
stream's clean identity mean moving -5.1311 to -5.1318 (a -0.0007
shift); latin 452 pair types present of 729 over 858,521 counted
pairs, the same 0.693146 largest single-entry repricing (type
(0, 10), -12.970668 to -13.663814), the mean repricing -0.083226, the
clean identity mean -5.0999 to -5.1004 (a -0.0005 shift). Probe 2,
the bridge gate rehearsed before the run: the shape instrument's full
first cell under the inherited table equals the held-out screen's own
outputs field for field (57 fields compared, no problem). Probe 3,
engine health under the leave-one-out table: ZL english's real
machinery call scores -4.4256 held-out (-4.4317 climb view, cap
False) against the frozen add-one -4.4252, and its anchor sits at
-5.1438; IT english's real call scores -4.3880 (-4.3914 climb view,
cap False) against the frozen add-one -4.3878, its anchor at -5.1439
- the real's held-out value moves at most 0.0004 nats under the
repricing while every occurring pair type is re-priced more severely.
The remaining numbers inside this module are unseen until the
declared runs.

The standing limitations are inherited from the held-out screen: no
mapping is published anywhere in this artifact, no recovered
assignment is stored as a key, plaintext_recovered_percent stays 0,
the reference prose is modern printed text outside the manuscript's
century, and nothing here is a reading or a language claim.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from engine import voynich_transcript_stats as base
from engine.voynich_compare import index_loci
from engine.voynich_ivtff import DATA_DIR, load
from engine.voynich_substitution import (
    BOUNDARY,
    BASE_SEED,
    CELL_ID,
    CROSS_REFERENCE_FILES,
    DATA_DIR,
    FILES,
    LANGS,
    LANG_ID,
    REFERENCE_FILES,
    WIDENED_REFERENCE_FILES,
    _reference_stream,
    _seed,
    table_from_stream,
)


# The declared wider mapped alphabet of this family: the file's most
# frequent glyph characters up to this count, plus the word-boundary
# mark in the last position.
MAPPED_HOMO = 36

N_PLANTS = 5
N_FLOORS = 5
SWEEP_CAP = 200        # inherited from the substitution family
N_RESTARTS = 16        # inherited from the substitution family

KIND_ID = {"real": 1,
           "homo_plant_enc": 24, "homo_plant_mach": 25,
           "homo_floor_perm": 26, "homo_floor_mach": 27,
           "homo_cross_enc": 28, "homo_cross_mach": 29}

HOMO_ARTIFACT_PATH = (
    Path(DATA_DIR).resolve().parent.parent.parent
    / "docs" / "research-notes" / "voynich-homophonic-screen.json"
)


# --------------------------------------------------------------------------
# The real streams at the homophonic alphabet
# --------------------------------------------------------------------------

_REAL_STREAMS: dict[str, dict] = {}


def _homo_real_stream(code: str) -> dict:
    """The real stream at the homophonic mapped set, one per file."""
    if code in _REAL_STREAMS:
        return _REAL_STREAMS[code]
    index = index_loci(load(code))
    loci = [
        (key, tuple(index[key].words))
        for key in base.used_keys()
        if key in index and index[key].words
    ]
    counts: dict[str, int] = {}
    word_count = 0
    for _key, words in loci:
        for word in words:
            for char in base._word_glyphs(word):
                counts[char] = counts.get(char, 0) + 1
            word_count += 1
    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    mapped_chars = tuple(char for char, _count in ranked[:MAPPED_HOMO]) + (
        BOUNDARY,
    )
    glyph_id = {char: position for position, char in enumerate(mapped_chars)}
    boundary_position = len(mapped_chars) - 1
    events: list[tuple[int, bool]] = []
    boundary_count = 0
    word_seen = 0
    for _key, words in loci:
        for word in words:
            if word_seen:
                events.append((boundary_position, True))
                boundary_count += 1
            word_seen += 1
            for char in base._word_glyphs(word):
                held = glyph_id.get(char)
                if held is None:
                    events.append((-1, False))
                    continue
                events.append((held, True))
    ids = np.array([value for value, _kept in events], dtype=np.int64)
    mask = np.array([kept for _value, kept in events], dtype=bool)
    stream = {
        "mapped_chars": mapped_chars,
        "event_ids": ids,
        "kept_ids": ids[mask],
        "kept_mask": mask,
        "total_events": len(events),
        "word_count": word_count,
        "boundary_count": boundary_count,
    }
    _REAL_STREAMS[code] = stream
    return stream


def _count_matrix_37(events_ids: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Pair counts over originally adjacent mapped positions, the
    alphabet 37 wide (36 glyphs plus the boundary mark)."""
    kept = np.where(mask)[0]
    values = events_ids[kept]
    adjacent = kept[1:] == kept[:-1] + 1
    first = values[:-1][adjacent]
    second = values[1:][adjacent]
    matrix = np.zeros((37, 37))
    np.add.at(matrix, (first, second), 1.0)
    return matrix


def _full_matrix_37(stream_ids: np.ndarray) -> np.ndarray:
    matrix = np.zeros((37, 37))
    np.add.at(matrix, (stream_ids[:-1], stream_ids[1:]), 1.0)
    return matrix


def _stream_matrix_27(stream_ids: list[int]) -> np.ndarray:
    """The pair count matrix of a reference-letter stream (27 wide)."""
    ids = np.array(stream_ids, dtype=np.int64)
    matrix = np.zeros((27, 27))
    np.add.at(matrix, (ids[:-1], ids[1:]), 1.0)
    return matrix


# --------------------------------------------------------------------------
# The homophonic assignment search
# --------------------------------------------------------------------------


def _score(f: np.ndarray, matrix: np.ndarray, table: np.ndarray) -> float:
    """The assignment score summed over the symbol pair matrix."""
    decoded = table[f][:, f]
    return float((matrix * decoded).sum())


def _climb(
    matrix: np.ndarray,
    table: np.ndarray,
    f0: list[int],
) -> tuple[float, int]:
    """The declared greedy reassignment hill-climb.

    One pass per sweep walks the symbols in index order. For each
    symbol its 27 candidate labels are evaluated exactly from the
    running score (outbound pairs, inbound pairs, and its diagonal
    removed once); a label is adopted only on a strict improvement
    beyond 1e-12. The best assignment's exact re-evaluated score is
    returned with the sweep count.
    """
    f = np.array(f0, dtype=np.int64)
    best = _score(f, matrix, table)
    f_best = f.copy()
    diag_table = np.diag(table).copy()
    sweeps = 0
    improved = True
    while improved and sweeps < SWEEP_CAP:
        improved = False
        sweeps += 1
        for symbol in range(len(f)):
            outbound = table[:, f] @ matrix[symbol]
            inbound = matrix[:, symbol] @ table[f, :]
            current = f[symbol]
            hold = (outbound[current] + inbound[current]
                    - matrix[symbol, symbol] * table[current, current])
            candidates = (
                best
                + outbound
                + inbound
                - matrix[symbol, symbol] * diag_table
                - hold
            )
            # candidates[current] == best exactly by construction
            pick = int(np.argmax(candidates))
            value = float(candidates[pick])
            if value > best + 1e-12:
                best = value
                f[symbol] = pick
                f_best = f.copy()
                improved = True
    return _score(f_best, matrix, table), sweeps


def _rank_init(matrix: np.ndarray, letter_counts: np.ndarray) -> list[int]:
    """Declared frequency-rank initialisation with surplus wrapping.

    The k-th most frequent symbol starts at the k-th most frequent
    letter token, k modulo 27; the boundary mark starts and moves like
    any symbol.
    """
    totals = matrix.sum(axis=1) + matrix.sum(axis=0)
    symbol_rank = np.argsort(-totals, kind="stable")
    letter_rank = np.argsort(-letter_counts, kind="stable")
    f = [0] * len(totals)
    for k, symbol in enumerate(symbol_rank):
        f[int(symbol)] = int(letter_rank[k % 27])
    return f


def machinery_best(
    matrix: np.ndarray,
    table: np.ndarray,
    letter_counts: np.ndarray,
    rng: np.random.Generator,
    restarts: int = N_RESTARTS,
) -> tuple[float, bool]:
    """Best mean nats per counted pair over the declared restarts.

    Restart 0 is the rank initialisation; each later restart consumes
    one seeded permutation of the 27 letter tokens (wrapped across the
    symbol list) deterministically, in order. Returns the best score
    and whether any climb hit the declared sweep cap.
    """
    symbols = matrix.shape[0]
    best, sweeps = _climb(matrix, table, _rank_init(matrix, letter_counts))
    cap_hit = sweeps >= SWEEP_CAP
    for _index in range(restarts - 1):
        permutation = list(rng.permutation(27))
        start = [permutation[symbol % 27] for symbol in range(symbols)]
        score, sweeps = _climb(matrix, table, start)
        cap_hit = cap_hit or sweeps >= SWEEP_CAP
        best = max(best, score)
    return best / matrix.sum(), cap_hit


# --------------------------------------------------------------------------
# The declared encoder and its partition rule
# --------------------------------------------------------------------------


def _partition_groups(
    truncated: list[int],
    glyph_count: int,
) -> list[list[int]]:
    """The declared partition of the glyph slots over present letters.

    Floor shares of frequency, one slot at least per present letter,
    remaining slots by largest fractional remainder with ties to the
    ascending letter index, groups laid out letter by letter in
    descending letter frequency so the most frequent letter receives
    the most frequent glyph ids, a zero-share present letter taking
    one slot from the largest existing group. Returns one group per
    letter token 0 to 26 (the boundary token's group is empty).
    """
    letters = [value for value in truncated if value != 26]
    counts = np.bincount(np.array(letters, dtype=np.int64), minlength=26)
    present = [index for index in range(26) if counts[index] > 0]
    present.sort(key=lambda index: (-int(counts[index]), index))
    total = int(counts[present].sum())
    raw = {index: glyph_count * counts[index] / total for index in present}
    floored = {index: int(raw[index]) for index in present}
    remainder = {index: raw[index] - floored[index] for index in present}
    tokens = glyph_count - sum(floored.values())
    ordered = sorted(present, key=lambda index: (-remainder[index], index))
    for extra in range(tokens):
        floored[ordered[extra]] += 1
    zero = [index for index in present if floored[index] == 0]
    for index in zero:
        donor = max(
            (k for k in present if floored[k] > 1),
            key=lambda k: (-floored[k], k),
        )
        floored[donor] -= 1
        floored[index] = 1
    groups = {index: [] for index in present}
    glyphs = 0
    for index in present:
        groups[index] = list(range(glyphs, glyphs + floored[index]))
        glyphs += floored[index]
    return [groups.get(index, []) for index in range(27)]


def _encode(
    truncated: list[int],
    groups: list[list[int]],
    rng: np.random.Generator,
    glyph_count: int,
) -> np.ndarray:
    """The declared encoder: one uniform draw per plaintext position
    from its letter's group; boundary positions take the boundary
    mark without a draw."""
    symbols = np.empty(len(truncated), dtype=np.int64)
    for position, value in enumerate(truncated):
        if value == 26:
            symbols[position] = glyph_count
            continue
        group = groups[value]
        symbols[position] = group[int(rng.integers(len(group)))]
    return symbols


def _truncated_reference(
    code: str, language: str, file: str | None = None,
) -> list[int]:
    """The reference stream cut to the standing truncation rule."""
    total = int(_homo_real_stream(code)["total_events"])
    stream = _reference_stream(language, file=file)
    return stream[: min(total, len(stream))]


def _identity_score(
    truncated: list[int], table: np.ndarray,
) -> tuple[float, int]:
    """The truncated stream's identity score under the declared table,
    with its counted pair total."""
    matrix = _stream_matrix_27(truncated)
    total = int(matrix.sum())
    value = float((matrix * table).sum()) / total
    return value, total


# --------------------------------------------------------------------------
# The held-out split and the held-out machinery
# --------------------------------------------------------------------------


def _kept_pairs(
    events_ids: np.ndarray, mask: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """The stream's occupied adjacent pairs as flat (first, second)
    arrays over mapped symbol ids, the pair source of the real and
    floor matrices."""
    kept = np.where(mask)[0]
    values = events_ids[kept]
    adjacent = kept[1:] == kept[:-1] + 1
    first = values[:-1][adjacent]
    second = values[1:][adjacent]
    return first, second


def _full_pairs(stream_ids: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """A full stream's consecutive pairs as flat (first, second)
    arrays, the pair source of the plant and band matrices."""
    ids = np.asarray(stream_ids, dtype=np.int64)
    return ids[:-1], ids[1:]


def _split_pairs(
    first: np.ndarray, second: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """The declared split of a stream's counted pairs by pair-index
    parity: even-index pairs form the climb half the machinery may
    search, odd-index pairs the score half it may never touch. The
    halves share no counted pair and together they are the flat list;
    within each half pairs two indices apart share no symbol, while
    across the halves adjacent pairs share a symbol position by
    construction."""
    even = np.arange(len(first)) % 2 == 0
    return first[even], second[even], first[~even], second[~even]


def _matrix_from_pairs(
    first: np.ndarray, second: np.ndarray,
) -> np.ndarray:
    matrix = np.zeros((37, 37))
    np.add.at(matrix, (first, second), 1.0)
    return matrix


def _held_climb(
    matrix: np.ndarray,
    table: np.ndarray,
    f0: list[int],
) -> tuple[float, int, np.ndarray]:
    """The declared exact greedy reassignment climb.

    For every symbol s with self-pair count n = matrix[s, s] and
    current label c = f[s], each candidate label l is evaluated as the
    exact new total of s's pairs under l:
    candidates[l] = best - hold + outbound[l] + inbound[l]
                    - n * (table[l, c] + table[c, l] - table[l, l]),
    where outbound[l] and inbound[l] count the symbol's pairs into and
    out of every symbol under candidate label l (the j = s term
    included), and hold is the symbol's exact current contribution
    outbound[c] + inbound[c] - n * table[c, c]. The candidate at the
    current label is best by construction. A label is adopted only on
    a strict improvement beyond 1e-12 against the running best, which
    is itself updated only by these exact values, so no incremental
    drift reaches the search or any stored number; the returned total
    is the exact re-evaluation of the tracked best assignment.
    """
    f = np.array(f0, dtype=np.int64)
    best = _score(f, matrix, table)
    f_best = f.copy()
    diag_table = np.diag(table).copy()
    sweeps = 0
    improved = True
    while improved and sweeps < SWEEP_CAP:
        improved = False
        sweeps += 1
        for symbol in range(len(f)):
            outbound = table[:, f] @ matrix[symbol]
            inbound = matrix[:, symbol] @ table[f, :]
            current = f[symbol]
            n = matrix[symbol, symbol]
            hold = outbound[current] + inbound[current] - n * table[
                current, current
            ]
            candidates = (
                best
                + outbound
                + inbound
                - hold
                - n * table[:, current]
                - n * table[current, :]
                + n * diag_table
            )
            candidates[current] = best
            pick = int(np.argmax(candidates))
            if candidates[pick] > best + 1e-12:
                best = float(candidates[pick])
                f[symbol] = pick
                f_best = f.copy()
                improved = True
    return _score(f_best, matrix, table), sweeps, f_best


def machinery_exact_full(
    matrix: np.ndarray,
    table: np.ndarray,
    letter_counts: np.ndarray,
    rng: np.random.Generator,
    restarts: int = N_RESTARTS,
) -> tuple[float, bool]:
    """The declared exact climb over one unsplit matrix, the
    attribution side instrument of the held-out measurement.

    Restart 0 is the rank initialisation; each later restart consumes
    one seeded permutation of the 27 letter tokens under the same wrap
    rule, in the same order as the first screen's machinery. Returns
    the best exact mean nats per counted pair over the unsplit matrix
    and whether any climb hit the declared sweep cap.
    """
    symbols = matrix.shape[0]
    best, sweeps, _assignment = _held_climb(
        matrix, table, _rank_init(matrix, letter_counts)
    )
    cap_hit = sweeps >= SWEEP_CAP
    for _index in range(restarts - 1):
        permutation = list(rng.permutation(27))
        start = [permutation[symbol % 27] for symbol in range(symbols)]
        score, sweeps, _assignment = _held_climb(matrix, table, start)
        cap_hit = cap_hit or sweeps >= SWEEP_CAP
        best = max(best, score)
    return best / matrix.sum(), bool(cap_hit)


def machinery_best_held(
    climb_matrix: np.ndarray,
    score_matrix: np.ndarray,
    table: np.ndarray,
    letter_counts: np.ndarray,
    rng: np.random.Generator,
    restarts: int = N_RESTARTS,
) -> tuple[float, float, bool]:
    """The held-out machinery: climb on the climb half, price the best
    assignment exactly on the score half.

    Restart 0 is the rank initialisation computed from the climb half;
    each later restart consumes one seeded permutation of the 27 letter
    tokens under the same wrap rule, consumed in the same order as the
    first screen's machinery. Among the restarts the best is the best
    exact climb-half total, ties resolved to the first restart, so the
    search's every choice reads only data its climbs saw. Returns the
    chosen assignment's mean nats per scored pair on the score half,
    its mean nats per climb pair on the climb half, and whether any
    climb hit the declared sweep cap. No assignment is returned and
    none is stored: the recovered mapping is never published.
    """
    symbols = climb_matrix.shape[0]
    climb_total, sweeps, f_best = _held_climb(
        climb_matrix, table, _rank_init(climb_matrix, letter_counts)
    )
    cap_hit = sweeps >= SWEEP_CAP
    for _index in range(restarts - 1):
        permutation = list(rng.permutation(27))
        start = [permutation[symbol % 27] for symbol in range(symbols)]
        score, sweeps, f = _held_climb(climb_matrix, table, start)
        cap_hit = cap_hit or sweeps >= SWEEP_CAP
        if score > climb_total + 1e-12:
            climb_total = score
            f_best = f
    climb_pairs = climb_matrix.sum()
    score_pairs = score_matrix.sum()
    climb_mean = float(climb_total) / float(climb_pairs)
    held_mean = (
        float((score_matrix * table[f_best][:, f_best]).sum())
        / float(score_pairs)
    )
    return held_mean, climb_mean, bool(cap_hit)


def _identity_half_means(
    truncated: list[int], table: np.ndarray,
) -> tuple[float, float, int, int]:
    """The truncated plaintext stream's identity means under the
    declared table, per half: the climb-half mean (the machinery's own
    view of its true configuration), the score-half mean (the true
    configuration's held-out anchor), and both half sizes. Boundary
    pairs are counted exactly as every counted pair of the stream."""
    ids = np.asarray(truncated, dtype=np.int64)
    first, second = ids[:-1], ids[1:]
    first_c, second_c, first_s, second_s = _split_pairs(first, second)
    climb_pairs = len(first_c)
    score_pairs = len(first_s)
    climb_mean = float(table[first_c, second_c].sum()) / climb_pairs
    held_mean = float(table[first_s, second_s].sum()) / score_pairs
    return held_mean, climb_mean, climb_pairs, score_pairs


# --------------------------------------------------------------------------
# The screen
# --------------------------------------------------------------------------


def _cell_facts(code: str, language: str) -> dict:
    """Real, plants with their anchor, and floors for one cell, all
    under the declared machinery at the declared budget."""
    table, letter_counts = table_from_stream(
        _reference_stream(language)
    )
    real_stream = _homo_real_stream(code)
    matrix = _count_matrix_37(
        real_stream["event_ids"], real_stream["kept_mask"]
    )
    real_rng = np.random.default_rng(
        _seed(CELL_ID[code], KIND_ID["real"], LANG_ID[language], 0)
    )
    value, hit = machinery_best(
        matrix, table, letter_counts, real_rng, restarts=N_RESTARTS
    )
    real = round(value, 4)
    real_hit = bool(hit)
    truncated = _truncated_reference(code, language)
    anchor, _anchor_total = _identity_score(truncated, table)
    anchor = round(anchor, 4)
    plants = []
    plants_hits = []
    for index in range(N_PLANTS):
        groups = _partition_groups(truncated, MAPPED_HOMO)
        rng_enc = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["homo_plant_enc"],
                  LANG_ID[language], index)
        )
        plant = _encode(truncated, groups, rng_enc, MAPPED_HOMO)
        plant_matrix = _full_matrix_37(plant)
        rng_mach = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["homo_plant_mach"],
                  LANG_ID[language], index)
        )
        value, hit = machinery_best(
            plant_matrix, table, letter_counts, rng_mach,
            restarts=N_RESTARTS,
        )
        plants.append(round(value, 4))
        plants_hits.append(bool(hit))
    floors = []
    floors_hits = []
    for index in range(N_FLOORS):
        rng_perm = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["homo_floor_perm"],
                  LANG_ID[language], index)
        )
        values = real_stream["kept_ids"].copy()
        rng_perm.shuffle(values)
        full = real_stream["event_ids"].copy()
        full[real_stream["kept_mask"]] = values
        floor_matrix = _count_matrix_37(full, real_stream["kept_mask"])
        rng_mach = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["homo_floor_mach"],
                  LANG_ID[language], index)
        )
        value, hit = machinery_best(
            floor_matrix, table, letter_counts, rng_mach,
            restarts=N_RESTARTS,
        )
        floors.append(round(value, 4))
        floors_hits.append(bool(hit))
    return {
        "real": real,
        "real_sweep_budget_hit": real_hit,
        "counted": int(matrix.sum()),
        "anchor": anchor,
        "plants": plants,
        "plants_hits": plants_hits,
        "floors": floors,
        "floors_hits": floors_hits,
    }


def _band_for(code: str, language: str, seed_index: int) -> dict:
    """Five homophonic encodings of one class-member text, their
    machinery bests, and the member's own anchor, under the declared
    per-text sequential scheme (one sampling rng draws the five
    encodings in order, one machinery rng runs the five climbs in
    order)."""
    table, letter_counts = table_from_stream(
        _reference_stream(language)
    )
    name, ebook = (
        [CROSS_REFERENCE_FILES[language]]
        + list(WIDENED_REFERENCE_FILES[language])
    )[seed_index][:2]
    truncated = _truncated_reference(code, language, file=name)
    anchor, _total = _identity_score(truncated, table)
    anchor = round(anchor, 4)
    rng_enc = np.random.default_rng(
        _seed(CELL_ID[code], KIND_ID["homo_cross_enc"],
              LANG_ID[language], seed_index)
    )
    rng_mach = np.random.default_rng(
        _seed(CELL_ID[code], KIND_ID["homo_cross_mach"],
              LANG_ID[language], seed_index)
    )
    draws = []
    draw_hits = []
    for _index in range(N_PLANTS):
        groups = _partition_groups(truncated, MAPPED_HOMO)
        encoded = _encode(truncated, groups, rng_enc, MAPPED_HOMO)
        encoded_matrix = _full_matrix_37(encoded)
        value, hit = machinery_best(
            encoded_matrix, table, letter_counts, rng_mach,
            restarts=N_RESTARTS,
        )
        draws.append(round(value, 4))
        draw_hits.append(bool(hit))
    spread = round(max(draws) - min(draws), 4)
    return {
        "file": name,
        "ebook": ebook,
        "plant_length": len(truncated),
        "anchor": anchor,
        "draws": draws,
        "draw_cap_hits": draw_hits,
        "recovered_best": max(draws),
        "spread": spread,
    }


def substitution_homophonic_screen() -> dict:
    """The declared homophonic screen: all three files, both
    languages, plants, floors, and the seven-text cross band."""
    artifact: dict = {
        "what": "The declared homophonic screen: several cipher symbols "
        "may share one plaintext letter while every cipher symbol names "
        "exactly one letter, on the same frozen streams, mapped sets "
        "(widened to 36 glyphs plus the word boundary mark), references "
        "and add-one bigram models as the substitution family, scored by "
        "a declared greedy reassignment climb with the inherited restart "
        "and sweep budgets. Plants are encodings of the truncated "
        "references by a declared partition rule; the cross band encodes "
        "the seven class members of the widened band; membership is "
        "unconditional and each member's value is its five-draw "
        "machinery best, with the declared cap truncation disclosed on "
        "both sides. No mapping is published; nothing here is a reading.",
        "declared": {
            "base_seed": BASE_SEED,
            "mapped_glyph_budget_comment": "the mapped set is the file's "
            "most frequent glyph characters up to 36 plus the "
            "word-boundary mark; letters 26 plus the boundary token",
            "mapped": MAPPED_HOMO,
            "restarts": N_RESTARTS,
            "sweep_cap": SWEEP_CAP,
            "plants_per_cell": N_PLANTS,
            "floors": N_FLOORS,
            "band_membership_rule": "membership is unconditional; each "
            "member's band value is its five-draw machinery best; all "
            "five draws and their spread are recorded, and the smallest "
            "member value sets the band threshold for its cell; the "
            "declaration of the sweep-cap disclosure applies to both "
            "sides of every comparison",
            "seed_kinds": {
                "real": KIND_ID["real"],
                "homo_plant": [KIND_ID["homo_plant_enc"],
                               KIND_ID["homo_plant_mach"]],
                "homo_floor": [KIND_ID["homo_floor_perm"],
                               KIND_ID["homo_floor_mach"]],
                "homo_cross": [KIND_ID["homo_cross_enc"],
                               KIND_ID["homo_cross_mach"]],
            },
            "models": {},
            "verdict_rule": "real at or above the smallest member value "
            "is consistent-with-substitution; real at or below the "
            "largest floor is not-consistent; strictly between is "
            "below-homophonic-band; machinery-noise-unresolved is "
            "retained formally for a memberless band, which cannot "
            "arise",
            "exclusion_rule": "if the real text stands below the "
            "smallest member value in all six cells with plant parity "
            "green and every floor below the real, the scoped "
            "homophonic class is excluded by count for the measured "
            "statistics, with the standing caveats",
        },
        "files": {},
    }
    for language in LANGS:
        name, ebook = REFERENCE_FILES[language]
        stream = _reference_stream(language)
        matrix = _stream_matrix_27(stream)
        artifact["declared"]["models"][language] = {
            "file": name,
            "ebook": ebook,
            "clean_identity_mean_nats_per_pair": round(
                float((matrix * table_from_stream(stream)[0]).sum())
                / float(matrix.sum()),
                4,
            ),
        }
    for code in FILES:
        cell: dict = {}
        for language in LANGS:
            facts = _cell_facts(code, language)
            members = []
            if language == "english":
                positions = (0, 1, 2)
            else:
                positions = (0, 1, 2, 3)
            for seed_index in positions:
                members.append(_band_for(code, language, seed_index))
            member_values = [member["recovered_best"] for member in members]
            floor_max = max(facts["floors"])
            band_min = min(member_values)
            band_max = max(member_values)
            if facts["real"] >= band_min:
                verdict = "consistent-with-substitution"
            elif facts["real"] <= floor_max:
                verdict = "not-consistent"
            else:
                verdict = "below-homophonic-band"
            parity = [
                bool(value >= facts["anchor"] - 0.0001)
                for value in facts["plants"]
            ]
            above_anchor = [
                round(value - facts["anchor"], 4)
                for value in facts["plants"]
                if value > facts["anchor"] + 0.0001
            ]
            cell[language] = {
                "real_best_mean_nats": facts["real"],
                "real_sweep_budget_hit": facts["real_sweep_budget_hit"],
                "counted_pairs": facts["counted"],
                "plant_parity_anchor_mean_nats": facts["anchor"],
                "self_plants_best_mean_nats": facts["plants"],
                "self_plants_at_parity": parity,
                "self_plants_sweep_budget_hits": facts["plants_hits"],
                "machinery_above_anchor_excesses": above_anchor,
                "floors_best_mean_nats": facts["floors"],
                "floors_sweep_budget_hits": facts["floors_hits"],
                "band": members,
                "band_min": band_min,
                "band_max": band_max,
                "verdict": verdict,
            }
        artifact["files"][code] = cell
    return artifact


def main() -> None:
    artifact = substitution_homophonic_screen()
    HOMO_ARTIFACT_PATH.write_text(json.dumps(artifact, indent=2) + "\n")
    print(HOMO_ARTIFACT_PATH)


# --------------------------------------------------------------------------
# The held-out screen, the second declared measurement
# --------------------------------------------------------------------------


HELD_ARTIFACT_PATH = (
    Path(DATA_DIR).resolve().parent.parent.parent
    / "docs" / "research-notes" / "voynich-homophonic-heldout.json"
)


def _held_cell_facts(code: str, language: str) -> dict:
    """Real, plants with their held-out anchor, and floors for one
    cell, each under the declared split, the exact reassignment climb
    on the climb half and the exact pricing on the score half, with
    the exact full-data side call recorded beside each score."""
    table, letter_counts = table_from_stream(
        _reference_stream(language)
    )
    real_stream = _homo_real_stream(code)
    first, second = _kept_pairs(
        real_stream["event_ids"], real_stream["kept_mask"]
    )
    climb_first, climb_second, score_first, score_second = _split_pairs(
        first, second
    )
    climb_matrix = _matrix_from_pairs(climb_first, climb_second)
    score_matrix = _matrix_from_pairs(score_first, score_second)
    full_matrix = _count_matrix_37(
        real_stream["event_ids"], real_stream["kept_mask"]
    )
    counted = int(full_matrix.sum())
    climb_pairs = int(climb_matrix.sum())
    score_pairs = int(score_matrix.sum())
    real_rng = np.random.default_rng(
        _seed(CELL_ID[code], KIND_ID["real"], LANG_ID[language], 0)
    )
    held_value, climb_value, cap_hit = machinery_best_held(
        climb_matrix, score_matrix, table, letter_counts, real_rng,
        restarts=N_RESTARTS,
    )
    real_held = round(held_value, 4)
    real_climb = round(climb_value, 4)
    real_hit = bool(cap_hit)
    full_rng = np.random.default_rng(
        _seed(CELL_ID[code], KIND_ID["real"], LANG_ID[language], 0)
    )
    full_value, full_hit = machinery_exact_full(
        full_matrix, table, letter_counts, full_rng, restarts=N_RESTARTS
    )
    real_full = round(full_value, 4)
    truncated = _truncated_reference(code, language)
    anchor, anchor_climb, _climb_half, _score_half = _identity_half_means(
        truncated, table
    )
    anchor = round(anchor, 4)
    anchor_climb = round(anchor_climb, 4)
    plants_held = []
    plants_full = []
    plants_hits = []
    plants_full_hits = []
    for index in range(N_PLANTS):
        groups = _partition_groups(truncated, MAPPED_HOMO)
        rng_enc = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["homo_plant_enc"],
                  LANG_ID[language], index)
        )
        plant = _encode(truncated, groups, rng_enc, MAPPED_HOMO)
        plant_first, plant_second = _full_pairs(plant)
        p_climb_first, p_climb_second, p_score_first, p_score_second = (
            _split_pairs(plant_first, plant_second)
        )
        p_climb = _matrix_from_pairs(p_climb_first, p_climb_second)
        p_score = _matrix_from_pairs(p_score_first, p_score_second)
        p_full = _full_matrix_37(plant)
        rng_mach = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["homo_plant_mach"],
                  LANG_ID[language], index)
        )
        value, _view, hit = machinery_best_held(
            p_climb, p_score, table, letter_counts, rng_mach,
            restarts=N_RESTARTS,
        )
        plants_held.append(round(value, 4))
        plants_hits.append(bool(hit))
        rng_full = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["homo_plant_mach"],
                  LANG_ID[language], index)
        )
        value_full, hit_full = machinery_exact_full(
            p_full, table, letter_counts, rng_full, restarts=N_RESTARTS
        )
        plants_full.append(round(value_full, 4))
        plants_full_hits.append(bool(hit_full))
    floors_held = []
    floors_full = []
    floors_hits = []
    floors_full_hits = []
    for index in range(N_FLOORS):
        rng_perm = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["homo_floor_perm"],
                  LANG_ID[language], index)
        )
        values = real_stream["kept_ids"].copy()
        rng_perm.shuffle(values)
        full = real_stream["event_ids"].copy()
        full[real_stream["kept_mask"]] = values
        floor_full = _count_matrix_37(full, real_stream["kept_mask"])
        floor_first, floor_second = _kept_pairs(
            full, real_stream["kept_mask"]
        )
        f_climb_first, f_climb_second, f_score_first, f_score_second = (
            _split_pairs(floor_first, floor_second)
        )
        f_climb = _matrix_from_pairs(f_climb_first, f_climb_second)
        f_score = _matrix_from_pairs(f_score_first, f_score_second)
        rng_mach = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["homo_floor_mach"],
                  LANG_ID[language], index)
        )
        value, _view, hit = machinery_best_held(
            f_climb, f_score, table, letter_counts, rng_mach,
            restarts=N_RESTARTS,
        )
        floors_held.append(round(value, 4))
        floors_hits.append(bool(hit))
        rng_full = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["homo_floor_mach"],
                  LANG_ID[language], index)
        )
        value_full, hit_full = machinery_exact_full(
            floor_full, table, letter_counts, rng_full, restarts=N_RESTARTS
        )
        floors_full.append(round(value_full, 4))
        floors_full_hits.append(bool(hit_full))
    return {
        "real_held": real_held,
        "real_climb": real_climb,
        "real_hit": real_hit,
        "real_full": real_full,
        "real_full_hit": bool(full_hit),
        "counted": counted,
        "climb_pairs": climb_pairs,
        "score_pairs": score_pairs,
        "anchor": anchor,
        "anchor_climb": anchor_climb,
        "plants_held": plants_held,
        "plants_full": plants_full,
        "plants_hits": plants_hits,
        "plants_full_hits": plants_full_hits,
        "floors_held": floors_held,
        "floors_full": floors_full,
        "floors_hits": floors_hits,
        "floors_full_hits": floors_full_hits,
    }


def _held_band_for(code: str, language: str, seed_index: int) -> dict:
    """Five encodings of one class-member text under the first
    screen's per-text sequential scheme, each scored by the held-out
    machinery and by the exact full-data side call, with the member's
    held-out anchor, climb-half identity, the selected draw's index
    and the member's band value."""
    table, letter_counts = table_from_stream(
        _reference_stream(language)
    )
    name, ebook = (
        [CROSS_REFERENCE_FILES[language]]
        + list(WIDENED_REFERENCE_FILES[language])
    )[seed_index][:2]
    truncated = _truncated_reference(code, language, file=name)
    anchor, anchor_climb, _climb_half, _score_half = _identity_half_means(
        truncated, table
    )
    anchor = round(anchor, 4)
    anchor_climb = round(anchor_climb, 4)
    rng_enc = np.random.default_rng(
        _seed(CELL_ID[code], KIND_ID["homo_cross_enc"],
              LANG_ID[language], seed_index)
    )
    draws_held = []
    draws_climb = []
    draws_full = []
    draw_hits = []
    draw_full_hits = []
    climb_totals = []
    for _index in range(N_PLANTS):
        groups = _partition_groups(truncated, MAPPED_HOMO)
        encoded = _encode(truncated, groups, rng_enc, MAPPED_HOMO)
        enc_first, enc_second = _full_pairs(encoded)
        e_climb_first, e_climb_second, e_score_first, e_score_second = (
            _split_pairs(enc_first, enc_second)
        )
        e_climb = _matrix_from_pairs(e_climb_first, e_climb_second)
        e_score = _matrix_from_pairs(e_score_first, e_score_second)
        e_full = _full_matrix_37(encoded)
        rng_mach = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["homo_cross_mach"],
                  LANG_ID[language], seed_index)
        )
        value, climb_view, hit = machinery_best_held(
            e_climb, e_score, table, letter_counts, rng_mach,
            restarts=N_RESTARTS,
        )
        rng_full = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["homo_cross_mach"],
                  LANG_ID[language], seed_index)
        )
        value_full, hit_full = machinery_exact_full(
            e_full, table, letter_counts, rng_full, restarts=N_RESTARTS
        )
        draws_held.append(round(value, 4))
        draws_climb.append(round(climb_view, 4))
        draws_full.append(round(value_full, 4))
        draw_hits.append(bool(hit))
        draw_full_hits.append(bool(hit_full))
        climb_totals.append(climb_view)
    selected = 0
    best_climb = climb_totals[0]
    for position, total in enumerate(climb_totals):
        if total > best_climb + 1e-12:
            best_climb = total
            selected = position
    spread = round(max(draws_held) - min(draws_held), 4)
    return {
        "file": name,
        "ebook": ebook,
        "plant_length": len(truncated),
        "anchor": anchor,
        "anchor_climb": anchor_climb,
        "draws": draws_held,
        "draws_climb": draws_climb,
        "draws_full": draws_full,
        "draw_sweep_budget_hits": draw_hits,
        "draw_full_sweep_budget_hits": draw_full_hits,
        "selected_draw_index": selected,
        "recovered_best": draws_held[selected],
        "spread": spread,
    }


def substitution_homophonic_heldout() -> dict:
    """The declared held-out homophonic screen: all three files, both
    languages, plants, floors, and the seven-text cross band, every
    side split by pair-index parity into a climb half and a score
    half, every assignment searched on the climb half under the exact
    reassignment rule and priced exactly on the score half."""
    artifact: dict = {
        "what": "The declared held-out homophonic screen: the counted "
        "pairs of every stream - the real, the plants, the floors and "
        "the seven band members of the first screen - are split by "
        "declared pair-index parity into a climb half the machinery "
        "may search and a score half it may never touch. The search is "
        "the exact greedy reassignment climb, declared when the first "
        "screen's candidate rule was found inexact away from the "
        "current label; its add-one exploitation is disclosed as "
        "systematic across the split, so this instrument prices the "
        "data-specific component only, and an exact full-data side "
        "call is recorded for attribution. The declared seeds of the "
        "first screen are replayed unchanged; nothing is redrawn and "
        "no mapping is published; nothing here is a reading.",
        "declared": {
            "base_seed": BASE_SEED,
            "mapped": MAPPED_HOMO,
            "restarts": N_RESTARTS,
            "sweep_cap": SWEEP_CAP,
            "plants_per_cell": N_PLANTS,
            "floors": N_FLOORS,
            "split_rule": "the counted pairs of each side, in stream "
            "order, split by pair-index parity: even indices form the "
            "climb half the machinery may search, odd indices the "
            "score half it may never touch; the halves share no "
            "counted pair and together they are the flat list, while "
            "across the halves adjacent pairs share a symbol position "
            "by construction (every interior position carries one "
            "climbed pair and one scored pair), so the score half is "
            "fresh to the search in the pair sense but not an "
            "independent sample of the stream; the split is "
            "deterministic and consumes no seed; both halves' sizes "
            "are recorded per cell",
            "machinery_rule": "the exact greedy reassignment climb: "
            "candidates are the exact new totals with the symbol's "
            "self-pair correction included, the running best is itself "
            "exact, and adoption needs a strict improvement beyond "
            "1e-12; the climb runs only on the climb half, restart 0 "
            "the rank initialisation computed from the climb half, "
            "restarts 1 onward seeded permutations of the 27 letter "
            "tokens under the wrap rule, the best restart the best "
            "exact climb-half total with ties to the first restart; "
            "the held-out number is the chosen assignment's mean nats "
            "per scored pair on the score half, evaluated exactly; no "
            "assignment is stored",
            "seed_kinds": {
                "real": KIND_ID["real"],
                "homo_plant": [KIND_ID["homo_plant_enc"],
                               KIND_ID["homo_plant_mach"]],
                "homo_floor": [KIND_ID["homo_floor_perm"],
                               KIND_ID["homo_floor_mach"]],
                "homo_cross": [KIND_ID["homo_cross_enc"],
                               KIND_ID["homo_cross_mach"]],
            },
            "seed_sharing": "no new kinds are consumed; the first "
            "screen's declared draws are replayed from the declared "
            "kinds and the split adds no draw",
            "anchor_rule": "a plant's or member's anchor is its true "
            "configuration's mean nats per pair on the score half, "
            "algebraically the truncated stream's odd-half identity "
            "mean under the declared table, recorded with the "
            "climb-half identity mean",
            "plant_rule": "a plant passes at or above its anchor minus "
            "0.0001 on the held-out statistic; an exact pass counts as "
            "parity; best above the anchor counts as parity with the "
            "excess recorded as machinery-above-anchor; a plant below "
            "the anchor by more than 0.0001 fails parity",
            "band_rule": "membership is unconditional as the first "
            "screen; a member's band value is the held-out value of "
            "the draw whose exact climb-half total is best among its "
            "five draws, ties to the first draw; the smallest member "
            "value sets the band threshold for its cell",
            "side_instrument": "the identical exact climb over the "
            "unsplit full data, recorded for attribution; no verdict "
            "is built on it",
            "verdict_rule": "real held-out at or above the smallest "
            "member band value is consistent-with-substitution; real "
            "held-out at or below the largest floor's held-out value "
            "is not-consistent; strictly between is below-held-band; "
            "machinery-noise-unresolved is retained formally for a "
            "memberless band, which cannot arise",
            "exclusion_rule": "if the real text stands below the "
            "smallest member band value in all six cells with plant "
            "parity green and every floor's held-out value below the "
            "real, the scoped homophonic class is excluded by count "
            "for the measured statistics, with the standing caveats",
            "models": {},
        },
        "files": {},
    }
    for language in LANGS:
        name, ebook = REFERENCE_FILES[language]
        stream = _reference_stream(language)
        table, _counts = table_from_stream(stream)
        held_mean, climb_mean, _cp, _sp = _identity_half_means(
            stream, table
        )
        full_matrix = _stream_matrix_27(stream)
        artifact["declared"]["models"][language] = {
            "file": name,
            "ebook": ebook,
            "clean_identity_mean_nats_per_pair": round(
                float((full_matrix * table).sum())
                / float(full_matrix.sum()),
                4,
            ),
            "identity_climb_half_mean_nats_per_pair": round(climb_mean, 4),
            "identity_score_half_mean_nats_per_pair": round(held_mean, 4),
        }
    for code in FILES:
        cell: dict = {}
        for language in LANGS:
            facts = _held_cell_facts(code, language)
            members = []
            if language == "english":
                positions = (0, 1, 2)
            else:
                positions = (0, 1, 2, 3)
            for seed_index in positions:
                members.append(_held_band_for(code, language, seed_index))
            member_values = [
                member["recovered_best"] for member in members
            ]
            floor_max = max(facts["floors_held"])
            band_min = min(member_values)
            band_max = max(member_values)
            if facts["real_held"] >= band_min:
                verdict = "consistent-with-substitution"
            elif facts["real_held"] <= floor_max:
                verdict = "not-consistent"
            else:
                verdict = "below-held-band"
            parity = [
                bool(value >= facts["anchor"] - 0.0001)
                for value in facts["plants_held"]
            ]
            above_anchor = [
                round(value - facts["anchor"], 4)
                for value in facts["plants_held"]
                if value > facts["anchor"] + 0.0001
            ]
            cell[language] = {
                "real_held_mean_nats": facts["real_held"],
                "real_climb_mean_nats": facts["real_climb"],
                "real_sweep_budget_hit": facts["real_hit"],
                "real_full_exact_mean_nats": facts["real_full"],
                "real_full_sweep_budget_hit": facts["real_full_hit"],
                "counted_pairs": facts["counted"],
                "climb_pairs": facts["climb_pairs"],
                "score_pairs": facts["score_pairs"],
                "plant_parity_anchor_mean_nats": facts["anchor"],
                "plant_climb_identity_mean_nats": facts["anchor_climb"],
                "self_plants_held_mean_nats": facts["plants_held"],
                "self_plants_full_exact_mean_nats": facts["plants_full"],
                "self_plants_at_parity": parity,
                "self_plants_sweep_budget_hits": facts["plants_hits"],
                "self_plants_full_sweep_budget_hits": (
                    facts["plants_full_hits"]
                ),
                "machinery_above_anchor_excesses": above_anchor,
                "floors_held_mean_nats": facts["floors_held"],
                "floors_full_exact_mean_nats": facts["floors_full"],
                "floors_sweep_budget_hits": facts["floors_hits"],
                "floors_full_sweep_budget_hits": (
                    facts["floors_full_hits"]
                ),
                "band": members,
                "band_min": band_min,
                "band_max": band_max,
                "verdict": verdict,
            }
        artifact["files"][code] = cell
    return artifact


def main_heldout() -> None:
    artifact = substitution_homophonic_heldout()
    HELD_ARTIFACT_PATH.write_text(json.dumps(artifact, indent=2) + "\n")
    print(HELD_ARTIFACT_PATH)


# --------------------------------------------------------------------------
# The surplus-capacity ladder, the family's third declared measurement
# --------------------------------------------------------------------------


LADDER_ARTIFACT_PATH = (
    Path(DATA_DIR).resolve().parent.parent.parent
    / "docs" / "research-notes" / "voynich-homophonic-ladder.json"
)

# The declared budget rungs, top first: 36 glyph slots is the held-out
# screen's mapped budget, then the surplus steps down twice and lands
# one glyph slot above the model's 26 letters.
LADDER_BUDGETS = (36, 33, 30, 27)

_LADDER_RAW: dict[str, dict] = {}


def _ladder_raw_stream(code: str) -> dict:
    """The file's raw glyph walk, run once and cached: every glyph
    character ranked by the declared (descending count, character)
    rule, plus the full event list before any budget mapping."""
    if code in _LADDER_RAW:
        return _LADDER_RAW[code]
    index = index_loci(load(code))
    loci = [
        (key, tuple(index[key].words))
        for key in base.used_keys()
        if key in index and index[key].words
    ]
    counts: dict[str, int] = {}
    events: list[str] = []
    word_count = 0
    boundary_count = 0
    word_seen = 0
    for _key, words in loci:
        for word in words:
            if word_seen:
                events.append(BOUNDARY)
                boundary_count += 1
            word_seen += 1
            for char in base._word_glyphs(word):
                events.append(char)
                counts[char] = counts.get(char, 0) + 1
    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    raw = {
        "ranked": ranked,
        "events": events,
        "word_count": word_count,
        "boundary_count": boundary_count,
        "total_events": len(events),
    }
    _LADDER_RAW[code] = raw
    return raw


def _ladder_real_stream(
    code: str, budget: int,
) -> dict:
    """The real stream re-rendered at one rung's mapped budget: the
    file's most frequent glyph characters up to the budget, ranked by
    the declared (descending count, character) rule, plus the
    word-boundary mark in the last position. A glyph character outside
    the rung's set renders to the dropped event and pairs across a
    dropped event do not count, exactly as the first screen's
    mapped-set rule renders characters beyond its count."""
    raw = _ladder_raw_stream(code)
    mapped = tuple(
        char for char, _count in raw["ranked"][:budget]
    ) + (BOUNDARY,)
    glyph_id = {char: position for position, char in enumerate(mapped)}
    ids = np.array(
        [glyph_id.get(char, -1) for char in raw["events"]],
        dtype=np.int64,
    )
    mask = ids >= 0
    return {
        "mapped_chars": mapped,
        "event_ids": ids,
        "kept_ids": ids[mask],
        "kept_mask": mask,
        "total_events": raw["total_events"],
        "word_count": raw["word_count"],
        "boundary_count": raw["boundary_count"],
    }


def _ladder_matrix_from_pairs(
    first: np.ndarray, second: np.ndarray, width: int,
) -> np.ndarray:
    """The rung-width pair count matrix: one row and column per cipher
    symbol of the rung's mapped budget (glyph slots plus the boundary
    mark), built from the same flat pair arrays as the held-out
    screen."""
    matrix = np.zeros((width, width))
    np.add.at(matrix, (first, second), 1.0)
    return matrix


def _ladder_full_matrix(
    stream_ids: np.ndarray, width: int,
) -> np.ndarray:
    """The rung-width matrix of a full encoded stream's consecutive
    pairs."""
    ids = np.asarray(stream_ids, dtype=np.int64)
    return _ladder_matrix_from_pairs(ids[:-1], ids[1:], width)


def _ladder_cell_facts(
    code: str, language: str, budget: int,
) -> dict:
    """Real, plants and floors for one cell at one rung's budget, each
    under the declared split and the exact machinery unchanged from the
    held-out screen, with the exact full-data side call recorded beside
    each held-out value."""
    width = budget + 1
    table, letter_counts = table_from_stream(
        _reference_stream(language)
    )
    real_stream = _ladder_real_stream(code, budget)
    first, second = _kept_pairs(
        real_stream["event_ids"], real_stream["kept_mask"]
    )
    climb_first, climb_second, score_first, score_second = _split_pairs(
        first, second
    )
    climb_matrix = _ladder_matrix_from_pairs(
        climb_first, climb_second, width
    )
    score_matrix = _ladder_matrix_from_pairs(
        score_first, score_second, width
    )
    full_matrix = _ladder_matrix_from_pairs(first, second, width)
    counted = int(full_matrix.sum())
    climb_pairs = int(climb_matrix.sum())
    score_pairs = int(score_matrix.sum())
    real_rng = np.random.default_rng(
        _seed(CELL_ID[code], KIND_ID["real"], LANG_ID[language], 0)
    )
    held_value, climb_value, cap_hit = machinery_best_held(
        climb_matrix, score_matrix, table, letter_counts, real_rng,
        restarts=N_RESTARTS,
    )
    real_held = round(held_value, 4)
    real_climb = round(climb_value, 4)
    real_hit = bool(cap_hit)
    full_rng = np.random.default_rng(
        _seed(CELL_ID[code], KIND_ID["real"], LANG_ID[language], 0)
    )
    full_value, full_hit = machinery_exact_full(
        full_matrix, table, letter_counts, full_rng, restarts=N_RESTARTS
    )
    real_full = round(full_value, 4)
    truncated = _truncated_reference(code, language)
    anchor, anchor_climb, _climb_half, _score_half = _identity_half_means(
        truncated, table
    )
    anchor = round(anchor, 4)
    anchor_climb = round(anchor_climb, 4)
    plants_held = []
    plants_full = []
    plants_hits = []
    plants_full_hits = []
    for index in range(N_PLANTS):
        groups = _partition_groups(truncated, budget)
        rng_enc = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["homo_plant_enc"],
                  LANG_ID[language], index)
        )
        plant = _encode(truncated, groups, rng_enc, budget)
        plant_first, plant_second = _full_pairs(plant)
        p_climb_first, p_climb_second, p_score_first, p_score_second = (
            _split_pairs(plant_first, plant_second)
        )
        p_climb = _ladder_matrix_from_pairs(
            p_climb_first, p_climb_second, width
        )
        p_score = _ladder_matrix_from_pairs(
            p_score_first, p_score_second, width
        )
        p_full = _ladder_full_matrix(plant, width)
        rng_mach = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["homo_plant_mach"],
                  LANG_ID[language], index)
        )
        value, _view, hit = machinery_best_held(
            p_climb, p_score, table, letter_counts, rng_mach,
            restarts=N_RESTARTS,
        )
        plants_held.append(round(value, 4))
        plants_hits.append(bool(hit))
        rng_full = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["homo_plant_mach"],
                  LANG_ID[language], index)
        )
        value_full, hit_full = machinery_exact_full(
            p_full, table, letter_counts, rng_full, restarts=N_RESTARTS
        )
        plants_full.append(round(value_full, 4))
        plants_full_hits.append(bool(hit_full))
    floors_held = []
    floors_full = []
    floors_hits = []
    floors_full_hits = []
    for index in range(N_FLOORS):
        rng_perm = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["homo_floor_perm"],
                  LANG_ID[language], index)
        )
        values = real_stream["kept_ids"].copy()
        rng_perm.shuffle(values)
        full = real_stream["event_ids"].copy()
        full[real_stream["kept_mask"]] = values
        floor_first, floor_second = _kept_pairs(full, real_stream[
            "kept_mask"
        ])
        f_climb_first, f_climb_second, f_score_first, f_score_second = (
            _split_pairs(floor_first, floor_second)
        )
        f_climb = _ladder_matrix_from_pairs(
            f_climb_first, f_climb_second, width
        )
        f_score = _ladder_matrix_from_pairs(
            f_score_first, f_score_second, width
        )
        f_full = _ladder_matrix_from_pairs(floor_first, floor_second, width)
        rng_mach = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["homo_floor_mach"],
                  LANG_ID[language], index)
        )
        value, _view, hit = machinery_best_held(
            f_climb, f_score, table, letter_counts, rng_mach,
            restarts=N_RESTARTS,
        )
        floors_held.append(round(value, 4))
        floors_hits.append(bool(hit))
        rng_full = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["homo_floor_mach"],
                  LANG_ID[language], index)
        )
        value_full, hit_full = machinery_exact_full(
            f_full, table, letter_counts, rng_full, restarts=N_RESTARTS
        )
        floors_full.append(round(value_full, 4))
        floors_full_hits.append(bool(hit_full))
    return {
        "real_held": real_held,
        "real_climb": real_climb,
        "real_hit": real_hit,
        "real_full": real_full,
        "real_full_hit": bool(full_hit),
        "counted": counted,
        "climb_pairs": climb_pairs,
        "score_pairs": score_pairs,
        "anchor": anchor,
        "anchor_climb": anchor_climb,
        "plants_held": plants_held,
        "plants_full": plants_full,
        "plants_hits": plants_hits,
        "plants_full_hits": plants_full_hits,
        "floors_held": floors_held,
        "floors_full": floors_full,
        "floors_hits": floors_hits,
        "floors_full_hits": floors_full_hits,
    }


def _ladder_band_for(
    code: str, language: str, seed_index: int, budget: int,
) -> dict:
    """Five encodings of one class-member text at one rung's budget
    under the first screen's per-text sequential scheme, each scored by
    the held-out machinery and by the exact full-data side call, with
    the member's rung-invariant held-out anchor, climb-half identity,
    the selected draw's index and the member's band value."""
    width = budget + 1
    table, letter_counts = table_from_stream(
        _reference_stream(language)
    )
    name, ebook = (
        [CROSS_REFERENCE_FILES[language]]
        + list(WIDENED_REFERENCE_FILES[language])
    )[seed_index][:2]
    truncated = _truncated_reference(code, language, file=name)
    anchor, anchor_climb, _climb_half, _score_half = _identity_half_means(
        truncated, table
    )
    anchor = round(anchor, 4)
    anchor_climb = round(anchor_climb, 4)
    rng_enc = np.random.default_rng(
        _seed(CELL_ID[code], KIND_ID["homo_cross_enc"],
              LANG_ID[language], seed_index)
    )
    draws_held = []
    draws_climb = []
    climbs_exact = []
    draws_full = []
    draw_hits = []
    draw_full_hits = []
    climb_totals = []
    for _index in range(N_PLANTS):
        groups = _partition_groups(truncated, budget)
        encoded = _encode(truncated, groups, rng_enc, budget)
        enc_first, enc_second = _full_pairs(encoded)
        e_climb_first, e_climb_second, e_score_first, e_score_second = (
            _split_pairs(enc_first, enc_second)
        )
        e_climb = _ladder_matrix_from_pairs(
            e_climb_first, e_climb_second, width
        )
        e_score = _ladder_matrix_from_pairs(
            e_score_first, e_score_second, width
        )
        e_full = _ladder_full_matrix(encoded, width)
        rng_mach = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["homo_cross_mach"],
                  LANG_ID[language], seed_index)
        )
        value, climb_view, hit = machinery_best_held(
            e_climb, e_score, table, letter_counts, rng_mach,
            restarts=N_RESTARTS,
        )
        rng_full = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["homo_cross_mach"],
                  LANG_ID[language], seed_index)
        )
        value_full, hit_full = machinery_exact_full(
            e_full, table, letter_counts, rng_full, restarts=N_RESTARTS
        )
        draws_held.append(round(value, 4))
        draws_climb.append(round(climb_view, 4))
        climbs_exact.append(float(climb_view))
        draws_full.append(round(value_full, 4))
        draw_hits.append(bool(hit))
        draw_full_hits.append(bool(hit_full))
        climb_totals.append(climb_view)
    selected = 0
    best_climb = climb_totals[0]
    for position, total in enumerate(climb_totals):
        if total > best_climb + 1e-12:
            best_climb = total
            selected = position
    spread = round(max(draws_held) - min(draws_held), 4)
    return {
        "file": name,
        "ebook": ebook,
        "plant_length": len(truncated),
        "anchor": anchor,
        "anchor_climb": anchor_climb,
        "draws": draws_held,
        "draws_climb": draws_climb,
        "draws_climb_exact": climbs_exact,
        "draws_full": draws_full,
        "draw_sweep_budget_hits": draw_hits,
        "draw_full_sweep_budget_hits": draw_full_hits,
        "selected_draw_index": selected,
        "recovered_best": draws_held[selected],
        "spread": spread,
    }


def _ladder_rung_block(budget: int) -> dict:
    """One rung of the ladder: all six (file, language) cells
    re-measured at the rung's mapped budget under the declared
    machinery, verdict and side-instrument rules."""
    block = {"budget_glyphs": budget, "files": {}}
    for code in FILES:
        cell: dict = {}
        for language in LANGS:
            facts = _ladder_cell_facts(code, language, budget)
            members = []
            if language == "english":
                positions = (0, 1, 2)
            else:
                positions = (0, 1, 2, 3)
            for seed_index in positions:
                members.append(
                    _ladder_band_for(code, language, seed_index, budget)
                )
            member_values = [
                member["recovered_best"] for member in members
            ]
            floor_max = max(facts["floors_held"])
            band_min = min(member_values)
            band_max = max(member_values)
            if facts["real_held"] >= band_min:
                verdict = "consistent-with-substitution"
            elif facts["real_held"] <= floor_max:
                verdict = "not-consistent"
            else:
                verdict = "below-held-band"
            parity = [
                bool(value >= facts["anchor"] - 0.0001)
                for value in facts["plants_held"]
            ]
            above_anchor = [
                round(value - facts["anchor"], 4)
                for value in facts["plants_held"]
                if value > facts["anchor"] + 0.0001
            ]
            cell[language] = {
                "budget_glyphs": budget,
                "real_held_mean_nats": facts["real_held"],
                "real_climb_mean_nats": facts["real_climb"],
                "real_sweep_budget_hit": facts["real_hit"],
                "real_full_exact_mean_nats": facts["real_full"],
                "real_full_sweep_budget_hit": facts["real_full_hit"],
                "counted_pairs": facts["counted"],
                "climb_pairs": facts["climb_pairs"],
                "score_pairs": facts["score_pairs"],
                "plant_parity_anchor_mean_nats": facts["anchor"],
                "plant_climb_identity_mean_nats": facts["anchor_climb"],
                "self_plants_held_mean_nats": facts["plants_held"],
                "self_plants_full_exact_mean_nats": facts["plants_full"],
                "self_plants_at_parity": parity,
                "self_plants_sweep_budget_hits": facts["plants_hits"],
                "self_plants_full_sweep_budget_hits": (
                    facts["plants_full_hits"]
                ),
                "machinery_above_anchor_excesses": above_anchor,
                "floors_held_mean_nats": facts["floors_held"],
                "floors_full_exact_mean_nats": facts["floors_full"],
                "floors_sweep_budget_hits": facts["floors_hits"],
                "floors_full_sweep_budget_hits": (
                    facts["floors_full_hits"]
                ),
                "band": members,
                "band_min": band_min,
                "band_max": band_max,
                "real_margin_over_band_min": round(
                    facts["real_held"] - band_min, 4
                ),
                "verdict": verdict,
            }
        block["files"][code] = cell
    return block


def _compare_rung_to_frozen_held(rung: dict) -> tuple[list[str], int]:
    """The declared reproduction gate: every field of the frozen
    held-out artifact's six cells, their band members and the declared
    language models must equal the top rung's same-named fields. Any
    divergence is a problem; a problem list must abort the ladder
    before any narrower rung is accepted."""
    frozen = json.loads(HELD_ARTIFACT_PATH.read_text())
    problems: list[str] = []
    fields = 0

    def check(path: str, frozen_value: object, rung_value: object) -> None:
        nonlocal fields
        fields += 1
        if frozen_value != rung_value:
            problems.append(
                f"{path}: frozen {frozen_value!r} vs rung {rung_value!r}"
            )

    for language in LANGS:
        for key, value in frozen["declared"]["models"][language].items():
            fresh = _declared_models_block()
            check(f"models/{language}/{key}", value, fresh[language][key])
    for code in FILES:
        for language in LANGS:
            frozen_cell = frozen["files"][code][language]
            rung_cell = rung["files"][code][language]
            for key, value in frozen_cell.items():
                if key == "band":
                    for index, member in enumerate(value):
                        rung_member = rung_cell["band"][index]
                        for member_key, member_value in member.items():
                            check(
                                f"{code}/{language}/band/{index}/"
                                f"{member_key}",
                                member_value,
                                rung_member[member_key],
                            )
                else:
                    check(
                        f"{code}/{language}/{key}",
                        value,
                        rung_cell[key],
                    )
    return problems, fields


def _declared_models_block() -> dict:
    """The declared language models with their identity means, identical
    at every rung because the models and the truncated streams are
    rung-invariant; recorded once and compared by the reproduction
    gate."""
    models: dict = {}
    for language in LANGS:
        name, ebook = REFERENCE_FILES[language]
        stream = _reference_stream(language)
        table, _counts = table_from_stream(stream)
        held_mean, climb_mean, _cp, _sp = _identity_half_means(
            stream, table
        )
        full_matrix = _stream_matrix_27(stream)
        models[language] = {
            "file": name,
            "ebook": ebook,
            "clean_identity_mean_nats_per_pair": round(
                float((full_matrix * table).sum())
                / float(full_matrix.sum()),
                4,
            ),
            "identity_climb_half_mean_nats_per_pair": round(climb_mean, 4),
            "identity_score_half_mean_nats_per_pair": round(held_mean, 4),
        }
    return models


def substitution_homophonic_ladder() -> dict:
    """The declared surplus-capacity ladder: the six (file, language)
    cells re-measured at the mapped budgets 36, 33, 30 and 27 glyph
    slots plus the word-boundary mark, the real re-rendered per budget
    through the declared top-B rule, plants and band members re-encoded
    per budget through the declared partition rule from their declared
    seed kinds, floors replayed per rung on the rung's real stream from
    their declared kinds, the machinery, split, anchors, budgets and
    verdict rule unchanged from the held-out screen, and the rung-36
    block checked field for field against the frozen held-out artifact
    immediately after it is measured and before the narrower rungs
    run."""
    artifact: dict = {
        "what": "The declared surplus-capacity ladder for the held-out "
        "homophonic screen: the same six (file, language) cells, the "
        "same exact reassignment machinery on the same declared "
        "climb/score split, re-measured as the mapped budget steps down "
        "through 36, 33, 30 and 27 glyph slots plus the word-boundary "
        "mark. The real is re-rendered per budget through the declared "
        "top-B rule; plants and band members are re-encoded per budget "
        "through the declared partition rule from their declared seed "
        "kinds; floors replay per rung on the rung's real stream from "
        "their declared kinds; the models, truncated streams and "
        "anchors are rung-invariant. The rung at budget 36 must "
        "reproduce the held-out artifact field for field before the "
        "narrower rungs are accepted. The declared truthful question: "
        "does the real's margin above the band shrink as the surplus is "
        "removed, and does any rung separate the real from the band; if "
        "none does, say so and keep the family open with the "
        "disclosure. No mapping is published; nothing here is a "
        "reading.",
        "declared": {
            "base_seed": BASE_SEED,
            "rungs": list(LADDER_BUDGETS),
            "budget_rule": "the mapped set at rung B is the file's most "
            "frequent glyph characters up to B, ranked by the declared "
            "(descending count, character) rule, plus the word-boundary "
            "mark in the last position; a glyph character outside the "
            "rung's set renders to the dropped event and pairs across a "
            "dropped event do not count, exactly as the first screen's "
            "mapped-set rule drops characters beyond its count; IT's "
            "glyph pool is 23, so IT's real takes its full pool at "
            "every declared rung and the matrices stay rung-width with "
            "the unfilled slots riding zero pairs",
            "partition_rule": "plants and band members re-encode the "
            "same truncated streams through the same declared partition "
            "rule at each rung's budget (floor shares of frequency, one "
            "slot at least per present letter, remaining slots by "
            "largest fractional remainder with ties to the ascending "
            "letter index, groups laid out letter by letter in "
            "descending letter frequency), each instrument replaying "
            "its declared seed kinds per (rung, instrument, index)",
            "floor_rule": "floors unchanged in declaration: the five "
            "destroyed-adjacency shuffles per cell from the declared "
            "kinds at every rung, shuffling the rung's real kept ids, "
            "scored by the same held-out machinery, every floor "
            "required below the rung's real",
            "machinery_rule": "unchanged from the held-out screen: the "
            "exact greedy reassignment climb on the climb half, exact "
            "pricing on the score half, the split by pair-index parity "
            "consuming no seed, restart 0 the rank initialisation from "
            "the climb half, restarts 1 onward the same seeded "
            "permutations of the 27 letter tokens, sweep cap 200 and 16 "
            "restarts at every rung and for every side",
            "models_and_anchors_rule": "the language models, the "
            "truncated streams and therefore the anchors are "
            "rung-invariant: an anchor is the truncated plaintext "
            "stream's odd-half identity mean under the unchanged table"
            ", identical at every rung and recorded per rung",
            "seed_kinds": {
                "real": KIND_ID["real"],
                "homo_plant": [KIND_ID["homo_plant_enc"],
                               KIND_ID["homo_plant_mach"]],
                "homo_floor": [KIND_ID["homo_floor_perm"],
                               KIND_ID["homo_floor_mach"]],
                "homo_cross": [KIND_ID["homo_cross_enc"],
                               KIND_ID["homo_cross_mach"]],
            },
            "seed_sharing": "no new seed kinds are consumed; every "
            "(rung, instrument, index) replays its declared seed value "
            "afresh, so identical seeds draw identically at identical "
            "budgets and the narrower rungs draw from the same seed "
            "values declared here; the ladder consumes none of any "
            "other module's declared draws",
            "reproduction_check_rule": "the rung at budget 36 must "
            "reproduce the frozen held-out artifact field for field "
            "(every cell field, every band member field and the "
            "declared models), checked immediately after the top rung "
            "is measured and before the narrower rungs run; a "
            "divergence aborts the ladder and no artifact is written",
            "side_instrument": "the exact full-data climb is carried "
            "per rung beside every held-out value for attribution "
            "only; no verdict is built on it",
            "band_record_rule": "membership, selection, ties and "
            "spreads are declared unchanged from the held-out screen; "
            "each member additionally records draws_climb_exact, its "
            "five climb-half totals at full precision, so the declared "
            "selection (best exact climb-half total, strict beyond "
            "1e-12, ties to the first draw) is re-derivable from the "
            "stored artifact, because four-decimal rounded totals can "
            "coincide where exact totals differ",
            "verdict_rule": "unchanged from the held-out screen, scored "
            "per rung: the rung's real held-out at or above the rung's "
            "smallest member band value is consistent-with-substitution"
            "; at or below the rung's largest floor's held-out value is "
            "not-consistent; strictly between is below-held-band",
            "margin_rule": "every margin is computed from the stored "
            "rounded values: the real held-out mean minus the smallest "
            "member band value, rounded to four decimals",
            "exclusion_rule": "the family's exclusion format is not "
            "re-scoped by this artifact: it keys to the declared "
            "36-slot class exactly as the held-out screen declared it, "
            "so the ladder adds no exclusion of its own; a rung's "
            "verdicts are rung-level evidence on the narrower subclass "
            "encodings that rung's budget defines, and the family "
            "stays open unless the top rung itself reverses",
            "truthful_question": "declared in advance: does the real's "
            "margin above the band shrink as the surplus is removed, "
            "and does any rung separate the real from the band; if "
            "none does, say so and keep the family open with the "
            "disclosure",
            "models": {},
        },
        "rungs": {},
        "files": {},
        "rung_36_reproduction_check": {},
    }
    artifact["declared"]["models"] = _declared_models_block()
    rungs = artifact["rungs"]
    rung36 = _ladder_rung_block(LADDER_BUDGETS[0])
    problems, fields = _compare_rung_to_frozen_held(rung36)
    if problems:
        raise RuntimeError(
            "the rung-36 reproduction check failed: "
            + "; ".join(problems[:12])
        )
    rungs[str(LADDER_BUDGETS[0])] = rung36
    for budget in LADDER_BUDGETS[1:]:
        rungs[str(budget)] = _ladder_rung_block(budget)
    artifact["rung_36_reproduction_check"] = {
        "status": "verified",
        "fields_compared": fields,
    }
    for code in FILES:
        rollup: dict = {}
        for language in LANGS:
            margins = {}
            verdicts = {}
            for budget in LADDER_BUDGETS:
                cell = rungs[str(budget)]["files"][code][language]
                margins[str(budget)] = cell["real_margin_over_band_min"]
                verdicts[str(budget)] = cell["verdict"]
            steps = {}
            for before, after in zip(
                LADDER_BUDGETS[:-1], LADDER_BUDGETS[1:]
            ):
                steps[f"{before}_to_{after}"] = round(
                    margins[str(after)] - margins[str(before)], 4
                )
            floors_ok = all(
                value < rungs[str(budget)]["files"][code][language][
                    "real_held_mean_nats"
                ]
                for budget in LADDER_BUDGETS
                for value in rungs[str(budget)]["files"][code][language][
                    "floors_held_mean_nats"
                ]
            )
            parity_ok = all(
                flag
                for budget in LADDER_BUDGETS
                for flag in rungs[str(budget)]["files"][code][language][
                    "self_plants_at_parity"
                ]
            )
            separated = [
                str(budget) for budget in LADDER_BUDGETS
                if verdicts[str(budget)] != "consistent-with-substitution"
            ]
            rollup[language] = {
                "margins_over_band_min": margins,
                "margin_steps": steps,
                "verdicts": verdicts,
                "floors_below_real_all_rungs": floors_ok,
                "plant_parity_all_rungs": parity_ok,
                "rungs_separated_from_the_band": separated,
                "any_rung_separates": bool(separated),
            }
        artifact["files"][code] = rollup
    return artifact


def main_ladder() -> None:
    artifact = substitution_homophonic_ladder()
    LADDER_ARTIFACT_PATH.write_text(json.dumps(artifact, indent=2) + "\n")
    print(LADDER_ARTIFACT_PATH)


# --------------------------------------------------------------------------
# The shape-priced re-measure, the family's fourth declared measurement
# --------------------------------------------------------------------------


SHAPE_ARTIFACT_PATH = (
    Path(DATA_DIR).resolve().parent.parent.parent
    / "docs" / "research-notes" / "voynich-homophonic-shape-priced.json"
)

_SHAPE_MODELS: dict[str, dict] = {}


def _shape_table(language: str) -> dict:
    """The declared leave-one-out form of the reference bigram table.

    The inherited add-one form of the reference pair table is
    log((n_ab + 1) / (N + 729)) with N the reference stream's total
    counted pairs. In the leave-one-out form every pair type (a, b)
    present in the reference pair table has its probability computed
    with one occurrence of (a, b) removed from the reference counts,
    log(n_ab / (N - 1 + 729)) = log(n_ab / (N + 728)), and a type with
    no counted occurrence keeps the inherited add-one entry
    log(1 / (N + 729)): the leave-one-out form re-prices every
    occurring pair type one occurrence more severely and leaves the
    unseen-type floor unchanged. The letter marginals are the
    reference's unigram counts, unchanged: the leave-one-out form
    re-prices pair types, not the letter alphabet, so the rank
    initialisation starts identically to the held-out screen and the
    declared conditional on re-deriving the matrix arithmetic resolves
    as not needed, the model staying the reference's aggregate."""
    if language in _SHAPE_MODELS:
        return _SHAPE_MODELS[language]
    stream = _reference_stream(language)
    add_one, letter_counts = table_from_stream(stream)
    ids = np.array(stream, dtype=np.int64)
    matrix = np.zeros((27, 27))
    np.add.at(matrix, (ids[:-1], ids[1:]), 1.0)
    total = int(matrix.sum())
    table = add_one.copy()
    present = matrix >= 1.0
    table[present] = np.log(matrix[present] / float(total + 728.0))
    delta = table - add_one
    argmax = np.unravel_index(
        int(np.argmax(np.abs(delta))), delta.shape
    )
    model = {
        "table": table,
        "letter_counts": letter_counts,
        "add_one_table": add_one,
        "pair_types_present": int(present.sum()),
        "total_pairs": total,
        "max_abs_entry_delta": round(float(np.abs(delta).max()), 6),
        "max_delta_type": [int(argmax[0]), int(argmax[1])],
        "mean_entry_delta_over_present": round(
            float(delta[present].mean()), 6
        ),
    }
    _SHAPE_MODELS[language] = model
    return model


def _shape_cell_facts(
    code: str, language: str,
    table: np.ndarray, letter_counts: np.ndarray,
) -> dict:
    """Real, plants with their held-out anchor, and floors for one
    cell, each under the declared split, the exact reassignment climb
    on the climb half and the exact pricing on the score half, with
    the exact full-data side call recorded beside each score: the
    held-out screen's cell facts with the scoring table supplied
    instead of fetched."""
    real_stream = _homo_real_stream(code)
    first, second = _kept_pairs(
        real_stream["event_ids"], real_stream["kept_mask"]
    )
    climb_first, climb_second, score_first, score_second = _split_pairs(
        first, second
    )
    climb_matrix = _matrix_from_pairs(climb_first, climb_second)
    score_matrix = _matrix_from_pairs(score_first, score_second)
    full_matrix = _count_matrix_37(
        real_stream["event_ids"], real_stream["kept_mask"]
    )
    counted = int(full_matrix.sum())
    climb_pairs = int(climb_matrix.sum())
    score_pairs = int(score_matrix.sum())
    real_rng = np.random.default_rng(
        _seed(CELL_ID[code], KIND_ID["real"], LANG_ID[language], 0)
    )
    held_value, climb_value, cap_hit = machinery_best_held(
        climb_matrix, score_matrix, table, letter_counts, real_rng,
        restarts=N_RESTARTS,
    )
    real_held = round(held_value, 4)
    real_climb = round(climb_value, 4)
    real_hit = bool(cap_hit)
    full_rng = np.random.default_rng(
        _seed(CELL_ID[code], KIND_ID["real"], LANG_ID[language], 0)
    )
    full_value, full_hit = machinery_exact_full(
        full_matrix, table, letter_counts, full_rng, restarts=N_RESTARTS
    )
    real_full = round(full_value, 4)
    truncated = _truncated_reference(code, language)
    anchor, anchor_climb, _climb_half, _score_half = _identity_half_means(
        truncated, table
    )
    anchor = round(anchor, 4)
    anchor_climb = round(anchor_climb, 4)
    plants_held = []
    plants_full = []
    plants_hits = []
    plants_full_hits = []
    for index in range(N_PLANTS):
        groups = _partition_groups(truncated, MAPPED_HOMO)
        rng_enc = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["homo_plant_enc"],
                  LANG_ID[language], index)
        )
        plant = _encode(truncated, groups, rng_enc, MAPPED_HOMO)
        plant_first, plant_second = _full_pairs(plant)
        p_climb_first, p_climb_second, p_score_first, p_score_second = (
            _split_pairs(plant_first, plant_second)
        )
        p_climb = _matrix_from_pairs(p_climb_first, p_climb_second)
        p_score = _matrix_from_pairs(p_score_first, p_score_second)
        p_full = _full_matrix_37(plant)
        rng_mach = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["homo_plant_mach"],
                  LANG_ID[language], index)
        )
        value, _view, hit = machinery_best_held(
            p_climb, p_score, table, letter_counts, rng_mach,
            restarts=N_RESTARTS,
        )
        plants_held.append(round(value, 4))
        plants_hits.append(bool(hit))
        rng_full = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["homo_plant_mach"],
                  LANG_ID[language], index)
        )
        value_full, hit_full = machinery_exact_full(
            p_full, table, letter_counts, rng_full, restarts=N_RESTARTS
        )
        plants_full.append(round(value_full, 4))
        plants_full_hits.append(bool(hit_full))
    floors_held = []
    floors_full = []
    floors_hits = []
    floors_full_hits = []
    for index in range(N_FLOORS):
        rng_perm = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["homo_floor_perm"],
                  LANG_ID[language], index)
        )
        values = real_stream["kept_ids"].copy()
        rng_perm.shuffle(values)
        full = real_stream["event_ids"].copy()
        full[real_stream["kept_mask"]] = values
        floor_full = _count_matrix_37(full, real_stream["kept_mask"])
        floor_first, floor_second = _kept_pairs(
            full, real_stream["kept_mask"]
        )
        f_climb_first, f_climb_second, f_score_first, f_score_second = (
            _split_pairs(floor_first, floor_second)
        )
        f_climb = _matrix_from_pairs(f_climb_first, f_climb_second)
        f_score = _matrix_from_pairs(f_score_first, f_score_second)
        rng_mach = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["homo_floor_mach"],
                  LANG_ID[language], index)
        )
        value, _view, hit = machinery_best_held(
            f_climb, f_score, table, letter_counts, rng_mach,
            restarts=N_RESTARTS,
        )
        floors_held.append(round(value, 4))
        floors_hits.append(bool(hit))
        rng_full = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["homo_floor_mach"],
                  LANG_ID[language], index)
        )
        value_full, hit_full = machinery_exact_full(
            floor_full, table, letter_counts, rng_full, restarts=N_RESTARTS
        )
        floors_full.append(round(value_full, 4))
        floors_full_hits.append(bool(hit_full))
    return {
        "real_held": real_held,
        "real_climb": real_climb,
        "real_hit": real_hit,
        "real_full": real_full,
        "real_full_hit": bool(full_hit),
        "counted": counted,
        "climb_pairs": climb_pairs,
        "score_pairs": score_pairs,
        "anchor": anchor,
        "anchor_climb": anchor_climb,
        "plants_held": plants_held,
        "plants_full": plants_full,
        "plants_hits": plants_hits,
        "plants_full_hits": plants_full_hits,
        "floors_held": floors_held,
        "floors_full": floors_full,
        "floors_hits": floors_hits,
        "floors_full_hits": floors_full_hits,
    }


def _shape_band_for(
    code: str, language: str, seed_index: int,
    table: np.ndarray, letter_counts: np.ndarray,
) -> dict:
    """Five encodings of one class-member text under the first
    screen's per-text sequential scheme, each scored by the held-out
    machinery and by the exact full-data side call, with the member's
    held-out anchor, climb-half identity, the selected draw's index
    and the member's band value: the held-out screen's band facts with
    the scoring table supplied instead of fetched, and the member's
    five climb-half totals additionally recorded at full precision so
    the declared selection is re-derivable from the stored artifact."""
    name, ebook = (
        [CROSS_REFERENCE_FILES[language]]
        + list(WIDENED_REFERENCE_FILES[language])
    )[seed_index][:2]
    truncated = _truncated_reference(code, language, file=name)
    anchor, anchor_climb, _climb_half, _score_half = _identity_half_means(
        truncated, table
    )
    anchor = round(anchor, 4)
    anchor_climb = round(anchor_climb, 4)
    rng_enc = np.random.default_rng(
        _seed(CELL_ID[code], KIND_ID["homo_cross_enc"],
              LANG_ID[language], seed_index)
    )
    draws_held = []
    draws_climb = []
    climbs_exact = []
    draws_full = []
    draw_hits = []
    draw_full_hits = []
    climb_totals = []
    for _index in range(N_PLANTS):
        groups = _partition_groups(truncated, MAPPED_HOMO)
        encoded = _encode(truncated, groups, rng_enc, MAPPED_HOMO)
        enc_first, enc_second = _full_pairs(encoded)
        e_climb_first, e_climb_second, e_score_first, e_score_second = (
            _split_pairs(enc_first, enc_second)
        )
        e_climb = _matrix_from_pairs(e_climb_first, e_climb_second)
        e_score = _matrix_from_pairs(e_score_first, e_score_second)
        e_full = _full_matrix_37(encoded)
        rng_mach = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["homo_cross_mach"],
                  LANG_ID[language], seed_index)
        )
        value, climb_view, hit = machinery_best_held(
            e_climb, e_score, table, letter_counts, rng_mach,
            restarts=N_RESTARTS,
        )
        rng_full = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["homo_cross_mach"],
                  LANG_ID[language], seed_index)
        )
        value_full, hit_full = machinery_exact_full(
            e_full, table, letter_counts, rng_full, restarts=N_RESTARTS
        )
        draws_held.append(round(value, 4))
        draws_climb.append(round(climb_view, 4))
        climbs_exact.append(float(climb_view))
        draws_full.append(round(value_full, 4))
        draw_hits.append(bool(hit))
        draw_full_hits.append(bool(hit_full))
        climb_totals.append(climb_view)
    selected = 0
    best_climb = climb_totals[0]
    for position, total in enumerate(climb_totals):
        if total > best_climb + 1e-12:
            best_climb = total
            selected = position
    spread = round(max(draws_held) - min(draws_held), 4)
    return {
        "file": name,
        "ebook": ebook,
        "plant_length": len(truncated),
        "anchor": anchor,
        "anchor_climb": anchor_climb,
        "draws": draws_held,
        "draws_climb": draws_climb,
        "draws_climb_exact": climbs_exact,
        "draws_full": draws_full,
        "draw_sweep_budget_hits": draw_hits,
        "draw_full_sweep_budget_hits": draw_full_hits,
        "selected_draw_index": selected,
        "recovered_best": draws_held[selected],
        "spread": spread,
    }


def _compare_shape_cell_to_heldout() -> tuple[list[str], int]:
    """The declared bridge gate: the shape instrument's full first cell
    (ZL english: the real, its five plants, its five floors and its
    three band members) computed through this measurement's code under
    the inherited add-one table must equal the held-out screen's own
    outputs field for field, so the leave-one-out artifact's only
    difference from the frozen measurement is the scoring table. Any
    divergence aborts with nothing written."""
    problems: list[str] = []
    fields = 0
    code, language = "ZL", "english"
    stream = _reference_stream(language)
    table, letter_counts = table_from_stream(stream)
    shape_facts = _shape_cell_facts(
        code, language, table, letter_counts
    )
    held_facts = _held_cell_facts(code, language)
    for key, value in held_facts.items():
        fields += 1
        if shape_facts[key] != value:
            problems.append(
                f"cell/{key}: held {value!r} vs shape {shape_facts[key]!r}"
            )
    for seed_index in (0, 1, 2):
        shape_member = _shape_band_for(
            code, language, seed_index, table, letter_counts
        )
        held_member = _held_band_for(code, language, seed_index)
        for key, value in held_member.items():
            fields += 1
            if shape_member[key] != value:
                problems.append(
                    f"band/{seed_index}/{key}: held {value!r} vs shape "
                    f"{shape_member[key]!r}"
                )
    return problems, fields


def substitution_homophonic_shape_priced() -> dict:
    """The declared shape-priced re-measure: the held-out screen's six
    (file, language) cells, plants, floors and band re-measured at the
    top budget with every stream, split, seed kind and machinery rule
    unchanged and the declared score table rebuilt in its
    exploitation-resistant leave-one-out form, after the bridge gate
    proves this measurement's code reproduces the frozen measurement
    field for field under the inherited table."""
    problems, fields = _compare_shape_cell_to_heldout()
    if problems:
        raise RuntimeError(
            "the bridge gate failed: " + "; ".join(problems[:12])
        )
    artifact: dict = {
        "what": "The declared shape-priced re-measure: the held-out "
        "homophonic screen's six (file, language) cells re-measured "
        "with the mapped set, streams, split, seeds, machinery, "
        "restarts, sweep cap, plants, floors and band unchanged and "
        "the declared score table rebuilt in its leave-one-out form, "
        "so the climb searches the same space against a table whose "
        "occurring pair types carry one occurrence more severity. The "
        "bridge gate re-derived the frozen measurement under the "
        "inherited table through this measurement's code before the "
        "leave-one-out cells ran. The declared truthful question: "
        "does the real's margin above the band survive a model the "
        "climb cannot feed on - a yes says the margin rides the "
        "manuscript's statistics, a no records which instrument "
        "carried it. No mapping is published; nothing here is a "
        "reading.",
        "declared": {
            "base_seed": BASE_SEED,
            "mapped": MAPPED_HOMO,
            "restarts": N_RESTARTS,
            "sweep_cap": SWEEP_CAP,
            "plants_per_cell": N_PLANTS,
            "floors": N_FLOORS,
            "loo_rule": "the declared score table rebuilt: the "
            "inherited add-one form is log((n_ab + 1) / (N + 729)) "
            "with N the reference stream's total counted pairs; in "
            "the leave-one-out form every pair type (a, b) present in "
            "the reference pair table is scored with one occurrence "
            "of (a, b) removed from the reference counts, "
            "log(n_ab / (N + 728)), and a type with no counted "
            "occurrence keeps the inherited add-one entry "
            "log(1 / (N + 729)); every occurring type is re-priced "
            "one occurrence more severely and the unseen-type floor "
            "is unchanged; the declared conditional on re-deriving "
            "the matrix arithmetic resolves as not needed, the model "
            "staying the reference's aggregate and the score one "
            "fixed 27 x 27 table per language summed by assignment "
            "aggregation (the sum over pair occurrences of "
            "table[first label, second label])",
            "letter_counts_rule": "the model's letter marginals are "
            "the reference unigram counts, unchanged by the "
            "leave-one-out re-pricing, so the rank initialisation "
            "consumes the same marginals and starts identically to "
            "the held-out screen",
            "measured_facts_rule": "the mapped set, streams, split, "
            "seeds, machinery, restarts, sweep cap, plants, floors "
            "and band are the held-out screen's declarations replayed "
            "unchanged; the encodings and shuffles are byte-identical "
            "replays of the frozen measurement's draws and only the "
            "scoring changes; each side's exact full-data side call "
            "is recorded beside its held-out value for attribution "
            "only",
            "split_rule": "the counted pairs of each side, in stream "
            "order, split by pair-index parity: even indices the "
            "climb half, odd indices the score half it may never "
            "touch; deterministic, consuming no seed, as the held-out "
            "screen declared",
            "machinery_rule": "unchanged from the held-out screen: "
            "the exact greedy reassignment climb on the climb half, "
            "exact pricing on the score half, restart 0 the rank "
            "initialisation from the climb half, restarts 1 onward "
            "the seeded permutations of the 27 letter tokens under "
            "the wrap rule, the best restart the best exact "
            "climb-half total with ties to the first; no assignment "
            "is stored",
            "seed_kinds": {
                "real": KIND_ID["real"],
                "homo_plant": [KIND_ID["homo_plant_enc"],
                               KIND_ID["homo_plant_mach"]],
                "homo_floor": [KIND_ID["homo_floor_perm"],
                               KIND_ID["homo_floor_mach"]],
                "homo_cross": [KIND_ID["homo_cross_enc"],
                               KIND_ID["homo_cross_mach"]],
            },
            "seed_sharing": "no new seed kinds are consumed; the "
            "declared draws are replayed from the declared kinds and "
            "this measurement consumes none of any other module's "
            "declared draws",
            "bridge_gate": "before the leave-one-out cells run, the "
            "shape instrument's full first cell (ZL english: the "
            "real, its five plants, its five floors and its three "
            "band members) is computed through this measurement's "
            "code under the inherited add-one table and compared "
            "field for field against the held-out screen's own "
            "outputs; any divergence aborts with nothing written",
            "band_record_rule": "membership, selection, ties and "
            "spreads are declared unchanged from the held-out screen "
            "(a member's band value the held-out value of the draw "
            "whose exact climb-half total is best, strict beyond "
            "1e-12, ties to the first draw); each member additionally "
            "records draws_climb_exact, its five climb-half totals at "
            "full precision, so the declared selection is "
            "re-derivable from the stored artifact, because "
            "four-decimal rounded totals can coincide where exact "
            "totals differ",
            "verdict_rule": "unchanged from the held-out screen and "
            "applied to the leave-one-out-scale numbers: the real "
            "held-out at or above the smallest member band value is "
            "consistent-with-substitution, at or below the largest "
            "floor's held-out value is not-consistent, strictly "
            "between is below-held-band; the strings describe "
            "consistency under this artifact's declared leave-one-out "
            "form and do not restate the add-one form's verdicts",
            "margin_rule": "the margin is computed from the stored "
            "rounded values: the real held-out mean minus the "
            "smallest member band value, rounded to four decimals",
            "exclusion_rule": "the family's declared exclusion format "
            "is not re-scoped by this artifact: it keys to the "
            "declared 36-slot class under the inherited add-one form "
            "exactly as the held-out screen declared it, so a "
            "leave-one-out verdict is shape-instrument evidence and "
            "the ladder-arc verdicts stand untouched by this "
            "artifact's numbers",
            "truthful_question": "declared in advance: does the "
            "real's margin above the band survive a model the climb "
            "cannot feed on - a yes says the margin rides the "
            "manuscript's statistics, a no records which instrument "
            "carried it; if the margin does not survive, record "
            "which instrument carried it",
            "models": {},
        },
        "bridge_gate": {},
        "files": {},
    }
    for language in LANGS:
        name, ebook = REFERENCE_FILES[language]
        stream = _reference_stream(language)
        model = _shape_table(language)
        table = model["table"]
        held_mean, climb_mean, _cp, _sp = _identity_half_means(
            stream, table
        )
        full_matrix = _stream_matrix_27(stream)
        add_one_held, add_one_climb, _acp, _asp = _identity_half_means(
            stream, model["add_one_table"]
        )
        artifact["declared"]["models"][language] = {
            "file": name,
            "ebook": ebook,
            "clean_identity_mean_nats_per_pair": round(
                float((full_matrix * table).sum())
                / float(full_matrix.sum()),
                4,
            ),
            "identity_climb_half_mean_nats_per_pair": round(climb_mean, 4),
            "identity_score_half_mean_nats_per_pair": round(held_mean, 4),
            "add_one_identity_score_half_mean_nats_per_pair": round(
                add_one_held, 4
            ),
            "pair_types_present": model["pair_types_present"],
            "total_pairs": model["total_pairs"],
            "max_abs_entry_delta": model["max_abs_entry_delta"],
            "max_delta_type": model["max_delta_type"],
            "mean_entry_delta_over_present": (
                model["mean_entry_delta_over_present"]
            ),
        }
    for code in FILES:
        cell: dict = {}
        for language in LANGS:
            model = _shape_table(language)
            facts = _shape_cell_facts(
                code, language, model["table"], model["letter_counts"]
            )
            members = []
            if language == "english":
                positions = (0, 1, 2)
            else:
                positions = (0, 1, 2, 3)
            for seed_index in positions:
                members.append(
                    _shape_band_for(
                        code, language, seed_index,
                        model["table"], model["letter_counts"],
                    )
                )
            member_values = [
                member["recovered_best"] for member in members
            ]
            floor_max = max(facts["floors_held"])
            band_min = min(member_values)
            band_max = max(member_values)
            if facts["real_held"] >= band_min:
                verdict = "consistent-with-substitution"
            elif facts["real_held"] <= floor_max:
                verdict = "not-consistent"
            else:
                verdict = "below-held-band"
            parity = [
                bool(value >= facts["anchor"] - 0.0001)
                for value in facts["plants_held"]
            ]
            above_anchor = [
                round(value - facts["anchor"], 4)
                for value in facts["plants_held"]
                if value > facts["anchor"] + 0.0001
            ]
            cell[language] = {
                "real_held_mean_nats": facts["real_held"],
                "real_climb_mean_nats": facts["real_climb"],
                "real_sweep_budget_hit": facts["real_hit"],
                "real_full_exact_mean_nats": facts["real_full"],
                "real_full_sweep_budget_hit": facts["real_full_hit"],
                "counted_pairs": facts["counted"],
                "climb_pairs": facts["climb_pairs"],
                "score_pairs": facts["score_pairs"],
                "plant_parity_anchor_mean_nats": facts["anchor"],
                "plant_climb_identity_mean_nats": facts["anchor_climb"],
                "self_plants_held_mean_nats": facts["plants_held"],
                "self_plants_full_exact_mean_nats": facts["plants_full"],
                "self_plants_at_parity": parity,
                "self_plants_sweep_budget_hits": facts["plants_hits"],
                "self_plants_full_sweep_budget_hits": (
                    facts["plants_full_hits"]
                ),
                "machinery_above_anchor_excesses": above_anchor,
                "floors_held_mean_nats": facts["floors_held"],
                "floors_full_exact_mean_nats": facts["floors_full"],
                "floors_sweep_budget_hits": facts["floors_hits"],
                "floors_full_sweep_budget_hits": (
                    facts["floors_full_hits"]
                ),
                "band": members,
                "band_min": band_min,
                "band_max": band_max,
                "real_margin_over_band_min": round(
                    facts["real_held"] - band_min, 4
                ),
                "verdict": verdict,
            }
        artifact["files"][code] = cell
    artifact["bridge_gate"] = {
        "status": "verified",
        "fields_compared": fields,
    }
    return artifact


def main_shape_priced() -> None:
    artifact = substitution_homophonic_shape_priced()
    SHAPE_ARTIFACT_PATH.write_text(json.dumps(artifact, indent=2) + "\n")
    print(SHAPE_ARTIFACT_PATH)
