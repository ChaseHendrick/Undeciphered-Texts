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

Fifth declared measurement, the block-fold split, declared after the
shape-priced re-measure exonerated the add-one table's shape and
before any run of it, around disclosed pre-run probes.

The declared design, before the run: the shape measurement's six
(file, language) cells, plants, floors and band re-measured at the top
budget under the leave-one-out table with the mapped set, streams,
seed kinds, machinery, restart and sweep budgets unchanged, and the
declared split replaced by the contiguous block fold: each side's
counted pairs, in stream order, split at the midpoint, the first
floor(N/2) pairs the climb half the machinery may search, the
remaining pairs the score half it may never touch, for an odd count
the climb half taking the smaller first block; the halves share no
counted pair and every identity anchor's halves fold by the same
rule. The truthful question, declared in advance: does the real's
held-out score-half value still stand above the band when the scored
pairs are fresh to the search in the span sense, not only the pair
sense - a yes extends the separation beyond the parity geometry, a no
records that the margin was carried by the parity geometry's
interleaving. The family's declared exclusion format is not re-scoped
by this artifact: it keys to the declared 36-slot class under the
inherited add-one form exactly as the held-out screen declared it, so
the verdicts recorded here are split-geometry evidence, and the
family stays open unless the declared exclusion fires.

The split's disclosed residual, priced here: the held-out screen's
pair-index-parity halves share no counted pair, but every interior
position carries one climbed pair and one scored pair, so the score
half is fresh to the search in the pair sense and not an independent
spatial sample; the parity geometry lets the climb-half exploitation
ride pair types identical to the score half's while the block fold
prices the chosen assignment on pairs drawn from the other span. The
leave-one-out table is carried forward unchanged from the shape
measurement (every occurring pair type scored with one occurrence
removed, the unseen-type floor unchanged, the letter marginals and
rank initialisation unchanged); the encodings and the floor shuffles
are byte-identical replays of the frozen measurement's declared
draws, so only the split changes, and no new seed kind is consumed.

A bridge gate, declared before the run and enforced in code: before
the block-fold cells run, this measurement's full first cell (ZL
english: the real, its five plants, its five floors and its three band
members) computed under the inherited pair-index-parity split must
equal the shape measurement's own outputs field for field; any
divergence aborts and nothing is written. Each band member records
draws_climb_exact, its five climb-half totals at full precision, as
the ladder and shape artifacts declared, so the declared selection
stays re-derivable from the stored artifact. Verdict and margin rules
are the held-out screen's rules applied to the block-fold-scale
numbers; the strings describe consistency under this artifact's
declared split and do not restate the parity geometry's verdicts, and
the margin is computed from the stored rounded values.

Pre-run probes, disclosed verbatim, on frozen data through the
declared implementation before the artifact run. Probe 1, the block
fold's shape facts: each real stream's counted pairs split as
218,415 into 109,207 climb and 109,208 score pairs (ZL), 183,199 into
91,599 and 91,600 (GC), 220,531 into 110,265 and 110,266 (IT), and the
six cells' identity anchors move under the block fold by +0.0015 to
+0.0107 nats against the frozen parity anchors (ZL english -5.1397
against -5.1438, ZL latin -5.0686 against -5.0760, GC english -5.1436
against -5.1451, GC latin -5.0658 against -5.0765, IT english -5.1398
against -5.1439, IT latin -5.0681 against -5.0757), every block score
half the more favourable. Probe 2, the bridge gate rehearsed before
the run: the block instrument's full first cell under the parity
split equals the shape measurement's own outputs field for field (60
fields compared, no problem). Probe 3, engine health under the block
fold and the leave-one-out table: ZL english's real machinery call
scores -4.4245 held-out (-4.4431 climb view, cap False) against the
frozen parity -4.4256, IT english's real call scores -4.3735 (-4.4071
climb view, cap False) against the frozen parity -4.3880, GC latin's
real call scores -4.4002 (-4.4199 climb view, cap False) against the
frozen parity -4.4035 - the real's held-out value moves favourably in
all three probes' cells under the span-fresh pricing. The remaining
numbers inside this module are unseen until the declared runs.

The standing limitations are inherited from the held-out screen: no
mapping is published anywhere in this artifact, no recovered
assignment is stored as a key, plaintext_recovered_percent stays 0,
the reference prose is modern printed text outside the manuscript's
century, and nothing here is a reading or a language claim.

Sixth declared measurement, the widened band population, declared
after the block-fold split answered its question and before any run
of it beyond the probes it discloses.

The declared design, before the run: the block-fold measurement's six
(file, language) cells re-measured at the top budget under the
leave-one-out table with the mapped set, streams, seed kinds,
machinery, restart and sweep budgets, plants, floors and block split
carried forward unchanged, and each cell's band extended with
declared widened members, english from three to seven members and
latin from four to eight, so the real is priced above a wider
population of the declared class. The truthful question, declared in
advance: does the real's held-out score-half value still stand above
the band as the band's population grows - a yes extends the
separation across the corpus breadth, a no records that the margin
rode the band's small population. The family's declared exclusion
format is not re-scoped by this artifact: it keys to the declared
36-slot class under the inherited add-one form exactly as the
held-out screen declared it, so the verdicts recorded here are
corpus-breadth evidence, and the family stays open unless the
declared exclusion fires.

Corpus discipline, declared and disclosed before the run. The
widened members are modern printed prose frozen under the declared
corpus rules: each candidate fetched from the standing members' plain
text source at
https://www.gutenberg.org/cache/epub/<id>/pg<id>.txt, the fetch first
verified byte-identical by re-fetching the standing english2 file and
matching its recorded sha256 (7810cd483cffcf2cc8..), each accepted
file stored raw under engine/data with its Gutenberg markers and
processed by the standing declared processing with no new step, and
a sha256 recorded for every accepted file. Candidates were probed in
their marker spans before acceptance: an english common-word probe
(the, and, with, from) against the body, the processed stream through
the declared loader (length, letter and boundary tokens, token types
present), and mid-span samples read. The standing members themselves
measure 0 to 52 common-word hits of english transcriber scaffolding
in their spans (the cipher chronicle's cross latin 0, the standing
Vulgate Daniel 52, Bodin 40, De Rariorum 25, the Augustine reference
2), so the declared bar: a candidate whose span interleaves english
translations, glossed school notes or collation apparatus through the
body, or whose english scaffolding runs beyond the standing
transcriber-note scale, is rejected with cause as family 4 rejected
its school editions and glossed readers. Rejected with cause,
verbatim: pg47001 Cicero De Officiis, an english translation
interleaved through the span (6,686 hits; mid-span in english: "they
fall into the other: they are traitors to social life"); pg7402
Sallust De Bello Catilinario et Jugurthino, the translator's glosses
inline through the span (4,056 hits: "That is, in the year B.C. 64,
or 690 after the building of the city.", "_Necessitudo_, 'a close
connection' or 'friendship'"); pg21827 Quintilian institutionis
oratoriae liber decimus, an english introduction and school notes
dominating the span (10,826 hits; mid-span english prose); pg13316
Boethius Theological Tractates and Consolation of Philosophy, a
bilingual Loeb edition with the english translation interleaved
(5,087 hits; mid-span in english); pg54243 Sinistrari Demoniality,
an english translation interleaved (3,277 hits; mid-span in
english); pg51812 Vitruvius De architectura libri decem, collation
apparatus interleaved through the text with manuscript sigla and
subscript editorial readings inside the verses ("sub(p _S^{c} G^{c}_)
ponentur _GS_: suppona(e _H^{c}_)ntur _H_", "(_ubi in m. G^{c}_");
pg69275 Haririus latinus, the translator's english bibliographic
apparatus beyond the standing scale (109 hits against the standing
members' 0 to 52, 104 of them in a trailing english critical-notes
block: "vert. Ouseley, p. 157 dicit: Maragha is nearly of the same
size as Ardebil"); and pg19635 Biblia Sacra Vulgata Psalmi XXII, not
accessible at the declared source (the cache returned the 404 page,
6,559 bytes, the same six first probes' error-page hash
6b781feba1fc6878).

The accepted widened members, with their measured facts, verbatim.
English: substref_english5_pg174.txt, The Picture of Dorian Gray
(Wilde), sha256 38f36b510417177a.., body 429,326 bytes, stream
412,038 tokens (331,550 letters, 80,488 boundary), all 27 types
present; substref_english6_pg1400.txt, Great Expectations (Dickens),
sha256 9a637118af8e953e.., body 994,627, stream 951,754 (762,700
letters), all 27 types; substref_english7_pg120.txt, Treasure Island
(Stevenson), sha256 5bc08275eacea8640.., body 364,531, stream
346,442 (275,943 letters), all 27 types; substref_english8_pg158.txt,
Emma (Austen), sha256 532b122b4e6a76cc.., body 880,438, stream
847,001 (684,896 letters), all 27 types. The apparatus probe is
defined on latin spans and was not applied to the english members:
the four are modern english prose, their marker spans carry the
producers' ordinary english scaffolding, and the artifact records
the probe's value only where it has meaning. Latin:
substref_latin6_pg23306.txt, Meditationes de prima philosophia
(Descartes), sha256 d6fea49898f02970.., body 139,717, stream 132,608
(111,769 letters), all 27 types, 2 english hits;
substref_latin7_pg28233.txt, Philosophiae Naturalis Principia
Mathematica (Newton), sha256 a734045637deef5f.., body 809,459,
stream 748,514 (631,467 letters), all 27 types, 19 english hits;
substref_latin8_pg826.txt, Vulgata Esther, sha256 f9c5959d2d2c6638..,
body 51,138, stream 45,491 (38,563 letters), all 27 types, 52
english hits - the same producer format and scaffolding scale as the
standing Vulgate Daniel; substref_latin9_pg58528.txt, Evagatorium
volumen primum (Fabri), sha256 2bdd3dd588b0deaa.., body 1,054,379,
stream 1,008,988 (857,357 letters), all 27 types, 12 english hits
distributed 5 head and 6 trailing with one mid-span transcription
-note occurrence (transcriber scaffolding inside the standing scale,
disclosed rather than hidden). Full sha256 strings are recorded in
the artifact at run time.

Mechanics, declared: the extended member list is the standing list
first, then the widened members declared above in the order listed;
the extended positions beyond every earlier measurement's declared
positions (english 3 to 6, latin 4 to 7) reward the declared homo
cross kinds (28 and 29) at those positions per cell; the standing
positions replay the frozen block-fold artifact's declared draws
byte-identically (same seeds, same files, same streams); the real,
plants and floors replay unchanged. Membership stays unconditional:
every widened member enters its band, no convergence criterion is
applied, each member's five draws are the declared scheme's draws and
the member records draws_climb_exact as every band record does.
Verdict and margin rules are the held-out screen's rules applied to
the wider band; the strings describe consistency under this
artifact's declared corpus breadth and do not restate the block-fold
measurement's verdicts.

A bridge gate, declared before the run and enforced in code, with the
difference that this measurement's first cell is compared against the
frozen block-fold artifact's own first cell: before the widened cells
run, the widened instrument's full first cell (ZL english: the real,
its five plants, its five floors and its three standing band
members) computed through this measurement's code with the extended
member list supplied must equal the frozen block-fold artifact's
stored first cell field for field; any divergence aborts and nothing
is written.

Pre-run probes, disclosed verbatim, on frozen data through the
declared implementation before the artifact run. Probe 1, the bridge
gate rehearsed: the widened instrument's full first cell through the
extended member list equals the frozen block-fold artifact's first
cell field for field (60 fields compared: the 18 cell facts and the
three standing members' 14 record keys each, no problem). Probe 2,
the latin standing replay at full band width: the latin standing
band's last position (De Rariorum, position 3) drawn through the
extended list matches the frozen artifact's stored record field for
field (no problem; its five draws -4.5825, the frozen band value).
Probe 3, the widened members' first records, drawn from the declared
kinds at their new positions amid the frozen machinery: latin
position 4 (Descartes) draws 5 deep at -4.5999 held (climb views
equal, spread 0.0, anchor -5.1442, climb-view anchor -5.1556,
plant_length 132,608, every cap flag false), and english position 3
(Dorian Gray) draws 5 deep at -4.6859 held (climb views -4.6927,
spread 0.0, anchor -5.1340, climb-view anchor -5.1570, plant_length
218,663, full-data side values -4.7326 to -4.6893, every cap flag
false). The remaining numbers inside this module are unseen until
the declared runs.

The standing limitations are inherited from the held-out screen: no
mapping is published anywhere in this artifact, no recovered
assignment is stored as a key, plaintext_recovered_percent stays 0,
the reference prose is modern printed text outside the manuscript's
century, and nothing here is a reading or a language claim.

Seventh declared measurement, the alternate reference corpora,
declared after the widened band held its margins and before any run
of it beyond the probes it discloses.

The declared design, before the run: the widened band measurement's
six (file, language) cells re-scored at the top budget with the
mapped set, streams, seed kinds, machinery, restart and sweep
budgets, floors, block split and band population carried forward
unchanged, and every scored table rebuilt from a single declared
alternate reference outside the band, one per language: english
substref_english9_pg76.txt, Adventures of Huckleberry Finn (Twain),
ebook 76, and latin substref_latin10_pg60772.txt, Evagatorium
volumen secundum (Fabri), ebook 60772. The leave-one-out form is
carried exactly onto the alternate reference's counts, present pair
types log(n_ab / (N + 728)) and absent types the add-one floor
log(1 / (N + 729)), with the alternate reference's letter marginals
driving the rank initialisation; each cell's five plants become
encodings of the declared alternate reference text truncated to the
declared length, from the declared plant kinds 24 and 25 at the
declared positions 0 to 4; the real, the floors and every band
member's encodings are byte-identical replays of the frozen
artifacts' declared draws. The truthful question, declared in
advance: does the real's held-out score-half value still stand above
the band when the scored tables are rebuilt from single alternate
references outside the band - a yes extends the separation across
the reference scope, a no records that the margin rode the standing
references' single choice. The family's declared exclusion format is
not re-scoped by this artifact: it keys to the declared 36-slot
class under the inherited add-one form exactly as the held-out
screen declared it, so the verdicts recorded here are reference
-scope evidence, the widened band's verdicts stand untouched, and
the family stays open unless the declared exclusion fires.

Corpus discipline, declared and disclosed before the run. The
alternate references live outside every standing reference, cross
reference, widened and extended band membership list, one per
language, frozen under the declared corpus rules: each candidate
fetched from the standing members' plain text source in cache form,
each accepted file stored raw under engine/data with its Gutenberg
markers and processed by the standing declared processing with no
new step, a sha256 recorded, and candidates probed in their marker
spans before acceptance with the sixth measurement's probes (the
apparatus probe on latin spans, the processed stream and mid-span
samples). English: substref_english9_pg76.txt, Adventures of
Huckleberry Finn (Twain), sha256
d617a37aa7ae1e1a93dcde2634db2bccb86824e31e29a55230bdbf77d6872d59,
file 622,460 bytes, body 583,036, stream 545,629 tokens (427,847
letters, 117,782 boundary), all 27 types present; modern printed
english prose in a vernacular first-person American register, a
declared register contrast with the standing english reference's
prose, and the declared design freezes one alternate per language.
Latin: substref_latin10_pg60772.txt, Evagatorium volumen secundum
(Fabri), sha256
579e27d7d1f944ab38355276e566f9e7c5a214754d8614bc9decba94bf0c68b2,
file 1,223,255 bytes, body 1,202,888, stream 1,138,187 tokens
(968,923 letters, 169,264 boundary), all 27 types present, 12
english common-word hits distributed 6 head, then 2 and 4 trailing
(deciles 6, 0, 0, 0, 0, 0, 0, 0, 2, 4) - the same producer format
and scaffolding scale as the accepted latin members. One
circumstance disclosed rather than resolved by another swap:
pg60772 is volume two of the same printed travel account whose
volume one, pg58528, is the widened band's latin9 member; the
remaining probed candidates were rejected with cause or terse in
form and the design keeps the declared single alternate. Rejected
with cause, verbatim: pg9090 Germania and Agricola (Tacitus),
english school commentary interleaved through the span (5,109 hits
in every decile; mid-span in english: "But _referantur_ is the
reading of all the MSS., and needs no emendation"); pg66595
Monumentum Ancyranum: The Deeds of Augustus, the editor's english
bibliographic apparatus through the span (2,813 hits in every
decile; mid-span a bibliography list: "enal, Decimus Junius (Juv.)
=: _Satirae (Sat.)_. =Livius, Titus (Livy)=: _Annales_;"); pg16400
De M. Terenti Varronis Libris Grammaticis (Varro), a mid-span
english transcriber note disclosing the fragment fabric:
"Most fragments have three elements: --original text, shown with
line numbers; --commentary and testimonia, indented in the same way
as footnotes; --critical apparatus keyed to line numbers in the
text" (24 hits, 8 of them at sixth-decile notes of this kind,
against the accepted members' zero mid-span english). Probed clean
and not selected by the declared design: pg345 Dracula (Stoker), a
clean modern english prose span (body 861,410 bytes, stream 806,705
tokens, all 27 types), the one-per-language design keeping pg76 as
english's declared alternate; pg20771 Species Plantarum, Sections
I-III (Linnaeus), inside the standing scaffold scale (49 hits: 14
in a head sidenote-format transcriber block, 35 trailing) and not
selected on form: terse nominal taxonomic description rather than
connected prose, with Linnaeus's own inline citations
("_T. Scheuchz. gram. 354._") through the descriptions.

Mechanics, declared: the bridge gate first - before the alternate
cells run, this measurement's full first cell (ZL english: the
real, its five plants of the standing reference text, its five
floors and all seven widened band members) computed through this
measurement's code with the standing reference supplied must equal
the frozen widened-band artifact's own first cell field for field;
any divergence aborts and nothing is written. The band re-scores
its same members, same encodings and same draws under the alternate
table at the same positions (english 0 to 6, latin 0 to 7); verdict
and margin rules are the held-out screen's rules applied to the
reference-scope numbers; the strings describe consistency under
this artifact's declared reference scope and do not restate the
widened band's verdicts.

Pre-run probes, disclosed verbatim, on frozen data through the
declared implementation before the artifact run. Probe 1, the
bridge gate rehearsed: the alternate instrument's full first cell
through the standing reference equals the frozen widened-band
artifact's first cell field for field (116 fields compared: the 18
cell facts and all seven members' 14 record keys each, no
problem). Probe 2, the alternate references' facts: english file
622,460 bytes, body 583,036, stream 545,629 tokens (427,847
letters), all 27 types; latin file 1,223,255 bytes, body 1,202,888,
stream 1,138,187 tokens (968,923 letters), all 27 types, 12 english
hits. Probe 3, the alternate tables' facts: english 501 pair types
present of 729 over 545,628 counted pairs, max entry delta
0.693145 over add-one at type [1, 12], mean delta over present
types -0.0824, the reference's full-stream identity -5.0189 nats
per pair (block halves -5.0386 climb and -4.9993 score, add-one
parity -5.0181); latin 490 types present over 1,138,186 counted
pairs, max delta 0.693146 at type [0, 10], mean delta -0.093635,
full-stream identity -5.116 (block halves -5.1208 and -5.1112,
add-one parity -5.1153). Probe 4, the first cell's real under the
alternate tables ahead of the run: ZL english real_held -4.3116
(climb -4.3127, full -4.3114, no cap hit), anchor -5.0298, plants
-4.6427 to -4.6997 encodings of the alternate reference text,
floors -5.185, -5.1849, -5.3511, -5.1847, -5.3442. The band values
under the alternate tables are unseen until the declared run.

The standing limitations are inherited from the held-out screen: no
mapping is published anywhere in this artifact, no recovered
assignment is stored as a key, plaintext_recovered_percent stays 0,
the reference prose is modern printed text outside the manuscript's
century, and nothing here is a reading or a language claim.

Eighth declared measurement, the split's ratio, declared after the
alternate reference corpora held their margins and before any run of
it beyond the probes it discloses.

The declared design, before the run: the widened band measurement's
six (file, language) cells re-measured at the top budget with the
mapped set, streams, seed kinds, machinery, restart and sweep
budgets, plants, floors, widened band population (seven english and
eight latin members), reference texts and leave-one-out tables
carried forward unchanged, and each side's counted pairs re-folded
under the declared 25/75 block split: the climb part the first
floor(N/4) pairs of each side in stream order, the score part the
remaining pairs the search may never touch, the block fold's own
first-block convention (the smaller share on a remainder) at one
quarter of the pairs, consuming no seed. Every identity anchor's
halves fold by the same rule. The real, every plant and every band
member's encodings are byte-identical replays of the frozen widened
artifact's declared draws; only the split's ratio changes, so the
machinery re-climbs on the smaller climb part and prices three
quarters of each side's pairs fresh. The truthful question, declared
in advance: does the real's held-out score-half value still stand
above the band when the climb part shrinks to a quarter of each
side's counted pairs - a yes extends the separation to a smaller
search freedom, a no records that the margin rode the climb half's
size. The family's declared exclusion format is not re-scoped by
this artifact: it keys to the declared 36-slot class under the
inherited add-one form exactly as the held-out screen declared it,
so the verdicts recorded here are split-geometry evidence, the
widened band's verdicts stand untouched, and the family stays open
unless the declared exclusion fires.

Corpus discipline: no new corpus files and no new candidates - the
band population is the frozen widened band's declared roster and the
references are the standing references' frozen files, all stored raw
with their markers and processed by the standing declared
processing.

Mechanics, declared: the bridge gate first - before the ratio cells
run, this measurement's full first cell (ZL english: the real, its
five plants, its five floors and all seven widened band members)
computed through this measurement's code with the block fold's
standing split supplied must equal the frozen widened-band
artifact's own first cell field for field; any divergence aborts and
nothing is written. The band re-scores its same members, same
encodings and same draws at the same positions (english 0 to 6,
latin 0 to 7) under the ratio split; the selection rule re-prices
the five exact climb-half totals and may pick a new best draw;
verdict and margin rules are the held-out screen's rules applied to
the split-ratio numbers; the strings describe consistency under
this artifact's declared split ratio and do not restate the widened
band's verdicts.

Pre-run probes, disclosed verbatim, on frozen data through the
declared implementation before the artifact run. Probe 1, the
bridge gate rehearsed: the split-ratio instrument's full first cell
through the standing split equals the frozen widened-band
artifact's first cell field for field (116 fields compared: the 18
cell facts and all seven members' 14 record keys each, no
problem). Probe 2, the ratio split's halves' counts: the real
streams' counted pairs re-fold at 54,603 climb and 163,812 score
(ZL's 218,415), 45,799 and 137,400 (GC's 183,199), 55,132 and
165,399 (IT's 220,531), against the block fold's half-and-half
splits. Probe 3, the re-folded english anchors: ZL's truncated
reference anchor -5.1391 at half sizes 54,665 and 163,997 (the
block fold's -5.1397), GC's -5.1373 at 46,676 and 140,031 (the
block fold's -5.1436), IT's -5.1392 at 55,132 and 165,399 (the
block fold's -5.1398). Probe 4, the first cell's real under the
ratio split ahead of the run: ZL english real_held -4.3841 (climb
-4.4171, full -4.444, no cap hit), climb pair columns 54,603 against
score 163,812, anchor -5.1391, plants -4.7409, -4.7229, -4.6645,
-4.7229, -4.7229 (no cap hits, above the anchor), floors -5.233,
-5.2371, -5.2357, -5.233, -5.236. The band values under the ratio
split and the other five cells are unseen until the declared run.

The standing limitations are inherited from the held-out screen: no
mapping is published anywhere in this artifact, no recovered
assignment is stored as a key, plaintext_recovered_percent stays 0,
the reference prose is modern printed text outside the manuscript's
century, and nothing here is a reading or a language claim.

Ninth declared measurement, the restart budget, declared after the
split's ratio held its margins and before any run of it beyond the
probes it discloses.

The declared design, before the run: the widened band measurement's
six (file, language) cells re-measured at the top budget with the
mapped set, streams, seed kinds, machinery, sweep cap, standing block
fold (the split's ratio's 25/75 variant is not this measurement's
split), plants, floors, widened band population (seven english and
eight latin members), reference texts and leave-one-out tables carried
forward unchanged, and every machinery call's restart count raised
from the inherited 16 to the declared 48: one rank initialisation
plus 47 seeded permutations, the extra restarts continuing each
call's declared machinery kind's permutation stream (restarts 1 to 15
replay the inherited budget's permutation draws exactly and restarts
16 to 47 draw the next 32 permutations of the same stream at the same
declared kind and position), consuming no new seed kind and no new
position, so only the restart budget's depth changes and every
recorded inherited-budget value re-prices only if a later restart
strictly beats the running best beyond 1e-12, ties to the first
restart. Every machinery call's 48 restarts record their exact
means at full precision, and each call records family 4's declared
convergence lens (the restarts agreeing to within 0.0001 mean nats
per pair) as a recorded status that gates nothing: no verdict,
margin, membership or exclusion depends on any flag, and band
membership stays unconditional exactly as the held-out screen
declared. The truthful question, declared in advance: does the
real's held-out score-half value still stand above the band when
every machinery call draws three times the inherited restart budget
- a yes extends the separation to a deeper search, a no records that
the margin rode the inherited budget's depth. The family's declared
exclusion format is not re-scoped by this artifact: it keys to the
declared 36-slot class under the inherited add-one form exactly as
the held-out screen declared it, so the verdicts recorded here are
search-depth evidence and the widened band's verdicts stand
untouched, and the family stays open unless the declared exclusion
fires.

Corpus discipline: no new corpus files and no new candidates - the
band population is the frozen widened band's declared roster and the
references are the standing references' frozen files, all stored raw
with their markers and processed by the standing declared
processing.

Mechanics, declared: the bridge gate first - before the deeper cells
run, this measurement's full first cell (ZL english: the real, its
five plants, its five floors and all seven widened band members)
computed through this measurement's code with the inherited 16
restarts supplied and every call's restarts recorded must equal the
frozen widened-band artifact's own first cell field for field; any
divergence aborts and nothing is written. The band re-scores its same
members, same encodings and same draws at the same positions under
the deeper budget; the deepen select rule re-prices the five exact
climb-half totals (now the best of 48 recorded restarts each) and may
pick a new best draw; verdict and margin rules are the held-out
screen's rules applied to the restart-budget numbers; the strings
describe consistency under this artifact's declared restart budget
and do not restate the widened band's verdicts.

Pre-run probes, disclosed verbatim, on frozen data through the
declared implementation before the artifact run. Probe 1, the
bridge gate rehearsed: the restart-budget instrument's full first
cell through the inherited 16 restarts equals the frozen
widened-band artifact's first cell field for field (116 fields
compared, no problem). Probe 2, the first cell's real under the 48
restart budget ahead of the run: ZL english real_held -4.3747 (climb
-4.4096, full -4.4282, no cap hit), its best restart index 46 of the
48 (a late restart wins the climb), the 48 restarts' spread
0.318299 mean nats per climb pair (the lens' flag false), anchor
-5.1397, plants -4.6573, -4.7234, -4.6573, -4.7234, -4.7234 (no cap
hits; restart spreads 0.360728, 0.246894, 0.312352, 0.197159 and
0.18017, all flags false), floors -5.2332, -5.2353, -5.2441,
-5.2323, -5.2361 (restart spreads 0.195404, 0.286865, 0.197602,
0.187249 and 0.283267, all flags false), and the real's full-data
side call spread 0.278468 (flag false). Probe 3, one band member at
48 ahead of the run: ZL english member 0 (substref_english2_pg84)
draws -4.6997, -4.651, -4.6997, -4.651, -4.651, selected draw 1,
recovered_best -4.651, five-draw spread 0.0487, every draw's restart
spread 0.222457 to 0.320722 with every flag false. Probe 4: none;
the split-ratio artifact's and the rest of the widened band's
members' values at the deeper budget and the five remaining cells
are unseen until the declared run.

The standing limitations are inherited from the held-out screen: no
mapping is published anywhere in this artifact, no recovered
assignment is stored as a key, plaintext_recovered_percent stays 0,
the reference prose is modern printed text outside the manuscript's
century, and nothing here is a reading or a language claim.

Tenth declared measurement, the search-free invariant instrument,
the user-directed new instrument declared after the restart budget
held its margins at triple the inherited search depth and before any
run of it beyond the probes it discloses.

The disclosed background, declared in advance: every number the band
instruments have produced across seven declared changes passes
through a hill-climb whose exploitation of the declared tables is
disclosed in every artifact, and the real's margin survived all
seven. This instrument removes the search entirely: it contains no
assignment search anywhere, no candidate evaluation, no restarts, no
sweep cap, no convergence flags, no score table, no split - it prices
the manuscript's raw pair-count structure directly against the
simulated encodings' raw pair-count structure, so that no number here
can ride any search's exploitation or its budget's depth.

The declared design, before the run: for each of the six (file,
language) cells the instrument records and prices profiles. The real
side: the manuscript's kept-adjacent mapped pair-count matrix over
the 37 symbol alphabet (36 glyphs plus the word-boundary mark;
unmapped events break adjacency and are not counted), its profile
one per file and shared by both language cells of that file. The
simulated side: every widened band member's selected-draw encoding,
replayed byte-identically through the declared partition and encoder
at the frozen homo_cross_enc kind and position (the selected draw
read from the frozen restart-budget artifact rather than re-derived,
because re-derivation is machinery), plus the five plant encodings
per cell at the standing homo_plant_enc kinds and the five
destroyed-adjacency floors per cell at the standing
homo_floor_perm kinds, replayed, not re-derived by any machinery.
The controls: each cell records the truncated standing reference's
own plaintext stream profile, computed by the same formulas on its
own 27-type state (729 types), a control whose width differs by
declaration and that takes no part in any envelope.

The declared invariant list, fixed in advance, every summary a
relabeling invariant of a pair-count matrix (invariant under any
permutation of the symbols, the diagonal mapping to itself): the
sorted symbol marginals (row sums) stored sorted descending as
counts and as shares of the profile's own total; the sorted
pair-count multiset over the full state space (1369 ordered types
for the 37-symbol profiles, 729 for the plaintext controls) stored
the same way; the empty type count (types with zero counted
occurrences); the self-pair share (the diagonal sum over the total);
the top-k pair concentration at the declared k values 1, 10 and 50
(the share of the total carried by the k largest pair counts); and
the pair entropy (the natural entropy of the pair distribution in
nats per counted pair). Shares and entropy round to the declared 6
decimals in a closed definition applied to every side. The state
note declared beside them: the real's profile prices kept-adjacent
mapped pairs while an encoding's prices every adjacent pair of its
full stream, the two totals differ for that structural reason and
every share-valued invariant normalises by its own total, while the
empty type count is a raw count tied to its own total and recorded
in that context; the latin band's members are the roster's own
truncated texts whose totals range from 45,490 to the full standing
length, standing property of the roster disclosed in every prior
artifact, so the latin envelopes are size-mixed by the roster's own
declared construction.

The declared verdict rule, fixed in advance, strict-all: a cell is
shape-consistent-with-homophonic-encoding only when every declared
invariant of the real's profile sits inside the closed range of that
cell's simulated band's profiles - the two vector summaries term by
term inside the band's per-position envelope, the scalar summaries
inside [min, max] at the stored rounding - and any outside invariant
makes the cell shape-outside-analogues, with every outside entry
recorded by position with its band range so that a miss is audited,
not summarized. No scalar margin is formed: this instrument's
question is inside or outside per invariant, and the recorded
distances are the outside entries' band ranges themselves. A confirm
is structure evidence under a search-free instrument, not an
identification: no mapping is published, no assignment is stored,
and the family's declared exclusion format is not re-scoped by this
artifact - it keys to the declared 36-slot class under the inherited
add-one form exactly as the held-out screen declared it, so the band
instruments' verdicts stand untouched by this artifact's numbers.

Corpus discipline: no new corpus files and no new candidates - the
band population is the frozen widened band's declared roster, the
plants and the plaintext controls are the standing references'
frozen files, all stored raw with their markers and processed by the
standing declared processing. No score table is built or used: the
instrument prices count structure only, so the standing add-one and
leave-one-out tables play no part anywhere in this artifact.

Mechanics, declared: the bridge gate first - before any profile is
priced, every fact this instrument re-derives fresh that the frozen
restart-budget artifact already recorded must equal that stored
value field for field: the six cells' counted pairs, all 45
members' file, ebook and plant_length records, and the 30 floors'
pair totals; the plants' totals are verified inside every cell
instead because their standing source lengths were never stored
frozen (each cell records its standing source's truncated length
and a plants_at_source_identity boolean); any divergence aborts and
nothing is written.

Pre-run probes, disclosed verbatim, on frozen data through the
declared implementation before the artifact run. Probe 1, the
bridge gate rehearsed: the first declared gate anchored the plants'
totals against the frozen band's first member's stored length, and
its latin rows failed - the standing latin reference's own
truncated length was never stored frozen, so a gate row cannot
anchor to it; the repair is declared here (the plant totals moved
into the cells as the plants_at_source_identity identity with the
standing source lengths recorded as new declared facts, the floors
and the streams and the members' identity fields keeping the gate)
and the repaired gate ran at 171 fields compared, no problem.
Probe 2, the real profiles ahead of the run: ZL events 218,663,
kept 218,537, unmapped 126, pairs 218,415, state 1369, empty types
943, self-pair share 0.045162, top shares 0.066625, 0.355937 and
0.859602 at k 1, 10 and 50, entropy 4.203; its sorted symbol-share
head 0.157027, 0.110643, 0.088767, 0.078502, 0.078351, 0.063709
(counts head 34,297, 24,166, 19,388, 17,146, 17,113, 13,915) and
its sorted pair-share head 0.066625, 0.048339, 0.03671, 0.036028,
0.030314, 0.029412. GC events 186,708, kept 184,939, unmapped
1,769, pairs 183,199, empty 645, self 0.009722, top shares
0.078745, 0.352327, 0.789781, entropy 4.500206; symbol-share head
0.194281, 0.127681, 0.090726, 0.072604, 0.070595, 0.05684 (counts
head 35,592, 23,391, 16,621, 13,301, 12,933, 10,413); pair-share
head 0.078745, 0.043799, 0.031731, 0.031157, 0.030257, 0.02899. IT
events 220,532, kept 220,532, unmapped 0, pairs 220,531, empty
1012, self 0.044039, top shares 0.067451, 0.356453, 0.867039,
entropy 4.180814; symbol-share head 0.165238, 0.110891, 0.087262,
0.077708, 0.077282, 0.062046 (counts head 36,440, 24,455, 19,244,
17,137, 17,043, 13,683); pair-share head 0.067451, 0.047998,
0.037342, 0.035455, 0.030086, 0.029955. Probe 3, the first cell's
declared verdict ahead of the run, ZL english:
shape-outside-analogues with every one of the eight invariant tests
outside - symbol_shares 37 of 37 sorted positions outside (position
0 real 0.157027 against the band [0.183123, 0.204027]; position 1
0.110643 against [0.051385, 0.070849]), pair_shares 902 of 1369
positions outside (position 0 real 0.066625 against
[0.021142, 0.028199]), empty_type_count 943 against [325, 447],
self_pair_share 0.045162 against [0.012192, 0.01645], top_1_share
0.066625 against [0.021142, 0.028199], top_10_share 0.355937
against [0.140788, 0.173894], top_50_share 0.859602 against
[0.414205, 0.443301], pair_entropy 4.203 against [5.7732,
5.904914]; the seven members' totals 218,662 each (their entropies
5.7732 to 5.904914), the five plants' totals 218,662 each, the five
floors' totals 218,415 each (the real's own counted pairs). Probe
4, the plaintext controls recorded not tested: the ZL english
truncated plaintext stream's profile has 218,662 pairs on 729
types, empty 260, self 0.019404, top_1 0.033115, top_50 0.567854,
entropy 5.139035; the ZL latin one has 218,662 pairs, empty 339,
self 0.013775, top_1 0.026671, top_50 0.569404, entropy 5.06327.
Probe 5, the first latin cell's declared verdict ahead of the run,
ZL latin: shape-outside-analogues with every one of the eight
invariant tests outside - symbol_shares 34 of 37 outside, pair
shares 838 of 1369 outside, empty_type_count 943 against
[241, 510], self_pair_share 0.045162 against
[0.009823, 0.01644], top_1_share 0.066625 against
[0.021489, 0.034072], top_10_share 0.355937 against
[0.129611, 0.15643], top_50_share 0.859602 against
[0.341177, 0.378328], pair_entropy 4.203 against
[5.923406, 6.050813]; the eight members' totals 45,490 to 218,662
(the roster's own truncated lengths recorded) with entropies
5.923406 to 6.050813, the plants' identity true with totals
218,662 each. Probe 6: none; the four remaining cells are unseen
until the declared run. The probes' disclosed first-cell verdicts
do not decide the artifact: the artifact run prices all six cells
through the same declared code, and the disclosure's honest
question is recorded over all of them.

The standing limitations are inherited from the held-out screen: no
mapping is published anywhere in this artifact, no recovered
assignment is stored as a key, plaintext_recovered_percent stays 0,
the reference prose is modern printed text outside the manuscript's
century, and nothing here is a reading or a language claim.

Eleventh declared measurement, the boundary-mark re-instrument,
declared after the search-free instrument answered no in all six
cells and before any run of it beyond the probes it discloses.

The disclosed background, declared in advance: the search-free
instrument's eight invariant tests sit outside in every cell, and
its recorded directions point at two suspects. The boundary mark is
each profile's most frequent symbol in every cell, and the english
and latin cells' first sorted positions ran in opposite directions,
so this instrument isolates the mark's role with one declared
change: the word-boundary mark's symbol's row and column are
excluded from every profile's state space on both sides - every
profile is the mark-excluded block of its pair-count matrix, 1296
ordered types, and every pair whose first or second symbol is the
mark is removed from the real's kept-adjacent matrix and from every
simulated encoding's full-stream matrix the same way. The declared
question: do the search-free outsides ride the mark's own
concentration, or does the interior pair structure miss of itself.

The declared design, before the run: the same five sides per cell as
the search-free instrument, replayed byte-identically at the same
frozen kinds and positions (the members' selected draws through
homo_cross_enc at their member position read, not re-derived, from
the frozen restart-budget artifact; the plants at their
homo_plant_enc kinds; the floors at their homo_floor_perm kinds;
the truncated standing reference's plaintext control), with every
profile reduced to its mark-excluded block, 1296 types, the mark's
own symbol located in each matrix's own alphabet (36 in every
simulated encoding's alphabet; the real stream's own last mapped
position, and the alphabet width is a standing disclosed fact: ZL
and GC rank to the full 36 glyph slots plus the mark, IT's
transcription ranks only 23 glyph types plus the mark, so IT's
block keeps 13 always-empty glyph slots on the real side that the
simulated encodings' saturated alphabets do not have). Each profile
records the full width's total beside its block facts so the
removed carried mass is disclosed and gate-anchored; the real cell
records boundary_carried_pairs (the full width minus the block) and
real_full_width_total_pairs beside the excluded profile, with the
mark's own self-pair count riding in the removed carried mass and
disclosed at zero in the real's counts ahead of the run. The
plaintext control's state is the 27 reference letters alone (729
types), which carries no boundary mark: each control is unchanged
by the exclusion, its totals gate-anchored against the frozen
search-free artifact's stored controls, and it takes no part in any
envelope.

The declared invariant list is the search-free instrument's six
summaries over the new widths, every summary still a relabeling
invariant of a pair-count matrix: the 36 sorted mark-excluded
glyph marginals as counts and shares (glyph occurrences inside
glyph-pair counts only, the mark's occurrence share not counted
anywhere), the sorted mark-excluded pair multiset over 1296 ordered
types as counts and shares, the block's empty type count, the
block's self-pair share over the profile's glyph-pair total, the
top-k pair concentration at the declared k values 1, 10 and 50, and
the pair entropy in nats per counted glyph pair; shares and entropy
round to the declared 6 decimals in a closed definition applied to
every side. The state note carries the standing caveats: the
real's glyph-pair total prices kept-adjacent mark-excluded pairs
while an encoding's prices every mark-excluded pair of its full
stream; every share normalises by its own glyph-pair total; the
empty count is a raw count tied to its own total and the IT cells'
empty comparisons carry the alphabet-width asymmetry disclosed
above; the latin envelopes are size-mixed by the roster's own
declared construction disclosed in every prior artifact.

The declared verdict rule is the search-free instrument's, fixed in
advance and strict-all with no scalar margin: a cell is
shape-consistent-with-homophonic-encoding only when every declared
invariant of the real's block profile sits inside the closed range
of that cell's simulated band's block profiles - the two vector
summaries term by term inside the band's per-position envelope over
36 sorted positions, the scalar summaries inside [min, max] at the
stored rounding - and any outside invariant makes the cell
shape-outside-analogues, with every outside entry recorded by
position with its band range so that a miss is audited, not
summarized. A confirm here is interior-structure evidence under a
search-free instrument, not an identification: no mapping is
published, no assignment is stored, plaintext_recovered_percent
stays 0, and the family's declared exclusion format is not
re-scoped by this artifact - it keys to the declared 36-slot class
under the inherited add-one form exactly as the held-out screen
declared it.

Corpus discipline is the search-free instrument's: no new corpus
files and no new candidates, the band population the frozen widened
band's declared roster, the plants and the plaintext controls the
standing references' frozen files. No score table is built or used.

Mechanics, declared: the bridge gate first, against two frozen
sources - the restart-budget artifact's 171 anchor fields exactly
as the search-free instrument declared them (the six cells' counted
pairs, all 45 members' file, ebook and plant_length records, and
the 30 floors' pair totals) and the frozen search-free artifact's
117 anchor fields (per cell, every full-width profile total this
instrument re-derives from the same replays - the real's, each
member's, each plant's, each floor's and the plaintext control's -
equal to that artifact's stored totals, so every block profile here
is verified as the declared block of the same encodings that
artifact measured): 288 fields total; the plants' full-width
identities are verified inside every cell as well; any divergence
aborts with nothing written.

Pre-run probes, disclosed verbatim, on frozen data through the
declared implementation before the artifact run. Probe 1, the
bridge gate rehearsed: the gate ran at 288 fields compared, no
problem. Probe 2, the boundary mass ahead of the run: ZL alphabet
37 wide (mark at position 36), kept pairs 218,415, block pairs
149,799, boundary-carried 68,616, words 34,354, marks 34,353; GC
alphabet 37 wide (mark at 36), kept pairs 183,199, block pairs
111,815, boundary-carried 71,384, words 36,232, marks 36,231; IT
alphabet 24 wide (mark at 23; its transcription's glyph inventory
holds only 23 ranked glyph types), kept pairs 220,531, block pairs
147,651, boundary-carried 72,880, words 36,441, marks 36,440; the
mark's self-pair count 0 in every file's real counts, disclosed
here because it rides in every removed carried mass. Probe 3, the
first cell's declared verdict ahead of the run, ZL english:
shape-outside-analogues with every one of the eight invariant tests
outside - symbol_shares 35 of 36 sorted positions outside,
pair_shares 845 of 1296 positions outside, empty_type_count 928
against [323, 443], self_pair_share 0.065848 against
[0.020192, 0.026741], top_1_share 0.070481 against
[0.018196, 0.035886], top_10_share 0.424435 against
[0.111613, 0.132192], top_50_share 0.893671 against
[0.318571, 0.345689], pair_entropy 4.010179 against
[5.947039, 6.102864]; the seven members' block totals 129,435 to
138,578 (their block entropies 5.947039 to 6.102864), the five
plants' full-width totals 218,662 each with the identity true, the
five floors' block totals 155,062 to 155,329 against the real's
block 149,799. Probe 4, the first latin cell's declared verdict
ahead of the run, ZL latin: shape-outside-analogues with every one
of the eight invariant tests outside - symbol_shares 36 of 36,
pair_shares 784 of 1296, empty_type_count 928 against [240, 503],
self_pair_share 0.065848 against [0.014311, 0.023974],
top_1_share 0.070481 against [0.017923, 0.02536], top_10_share
0.424435 against [0.114705, 0.131916], top_50_share 0.893671
against [0.300616, 0.336503], pair_entropy 4.010179 against
[5.980168, 6.104489]; the eight members' block totals 31,635 to
155,874 (the roster's own truncated lengths reduced) with block
entropies 5.980168 to 6.104489, the plants' full-width identity
true, the floors' block totals 155,145 to 155,274. Probe 5, the
plaintext control recorded unchanged: every control's profile
equals its frozen search-free counterpart field for field - ZL
english entropy 5.139035, ZL latin 5.06327, GC english 5.139139,
GC latin 5.063406, IT english 5.139068, IT latin 5.062979, all on
their 729-type states, unchanged by the exclusion because the
state carries no boundary mark. Probe 6: none; the four remaining
cells are unseen until the declared run. The probes' disclosed
first-cell verdicts do not decide the artifact: the artifact run
prices all six cells through the same declared code, and the
disclosure's honest question is recorded over all of them.

The standing limitations are inherited from the held-out screen: no
mapping is published anywhere in this artifact, no recovered
assignment is stored as a key, plaintext_recovered_percent stays 0,
the reference prose is modern printed text outside the manuscript's
century, and nothing here is a reading or a language claim.

Twelfth declared measurement, the corpus-breadth search-free
instrument, declared after the boundary-mark re-instrument answered
no in all six cells and before any run of it beyond the probes it
discloses.

The disclosed background, declared in advance: the interior miss
survived the mark's exclusion in every cell (the boundary-mark
instrument's eight invariant tests outside in five cells, seven of
eight in the GC latin cell with its self-pair share the recorded
entry into its band), and the real's recorded directions sit in its
own pair-count structure's cuts - the concentrated first sorted
positions, the concentrated top pairs, the shared self-pair mass
and the low entropy - so the one untested declared axis of the
search-free design left standing is the roster's own extent. The
standing bands are seven english and eight latin members of one
declared roster, and a band's closed ranges are extrema over its
membership, so this instrument widens the band population across
the corpus breadth and re-asks the search-free question unchanged
otherwise. The declared truth about the arithmetic, recorded as
design: adding members to a band can only widen the band's closed
ranges and per-position envelopes (each extremum is taken over more
members), so every widened test is weakly wider than its standing
counterpart and an inside verdict becomes the easier outcome; the
only verdict change this design can produce is a cell reporting
inside under the widened band, and the declared question is
whether any does. With the band population widened across the
corpus breadth under the declared draw rules, does the real's
mark-excluded profile sit inside the extended band's range on every
declared invariant in every (file, language) cell, or is at least
one invariant outside - the measured test of whether the interior's
separation holds as the roster grows.

The declared design, before the run: the boundary-mark
re-instrument's state space and verdict rule unchanged - every
profile the mark-excluded block of its pair-count matrix, 1296
ordered types, the mark's row and column excluded on both sides
exactly as declared there, the same six relabeling-invariant
summaries priced under the same declared strict-all no-margin rule
- with the band population widened: the standing roster's
selected-draw encodings replayed byte-identically (the selected
draw read from the frozen restart-budget artifact, not re-derived)
and the declared breadth members' encodings added at their listed
positions (english 7 to 11, latin 8 to 10), each breadth member
taking draw 0 of the declared homo_cross_enc kind at its listed
position, the stream's first encoding, declared in advance with no
selection performed and no machinery; the kind's position axis
extends, no new seed kind is consumed. The roster's declared floor:
each breadth member's processed stream must reach the standing
roster's smallest member stream length (45,491 tokens, Vulgata
Esther), and every accepted candidate clears it. The membership
stays unconditional at twelve english and eleven latin member
profiles per cell (the standing seven english and eight latin plus
the breadth five english and three latin), and the plants, the
floors and the plaintext controls replay exactly as the
boundary-mark instrument declared them.

Corpus discipline, declared and disclosed before the run. Five
declared english slots (an early modern scriptural register, an
eighteenth century satirical prose register, a verse register, a
civic polemical register and a scientific non-fiction register) and
three declared latin slots (classical epic verse, classical prose
history and classical oratory) fill the new positions; every
candidate fetched from the standing members' plain text source at
the declared cache form, probed in its marker span before
acceptance (the english common-word probe the, and, with, from over
the body in deciles against the standing transcriber-note scale's 0
to 52 hits, the processed stream through the declared loader, and
mid-span samples read), accepted files stored raw under engine/data
with their Gutenberg markers, processed by the standing declared
processing with no new step, and a sha256 recorded. The fetch
verification was rehearsed: the cache serves the standing english2
marker span byte-identical (447,911 bytes, span sha256
7f95a6c0484513216cffa7d9e1e0314896faa21cb5a713d65c125a86f1f43695)
at the same byte counts, with a two-line title capitalization drift
upstream in the header metadata (the modern prometheus to The
modern Prometheus, differing bytes at positions 49, 60, 555 and 566
before the START marker), recorded as metadata drift the marker
span does not carry, so the standing freeze stands. The accepted
roster: ebook 10 the King James Version of the Bible, ebook 829
Gulliver's Travels (Swift), ebook 1041 Shakespeare's Sonnets, ebook
1404 The Federalist Papers, ebook 1228 On the Origin of Species
(Darwin); ebook 227 Aeneidos (Virgil), ebook 18837 Commentarii de
Bello Gallico libri V-VIII (Caesar), ebook 226 Cicero's Orations;
the rejections and their verbatim causes are recorded in the
artifact and disclosed here in summary: ebook 21765 an english
translation carries the marker span (17,181 common-word hits in
every decile, mid-span in english), ebook 14945 the editor's
english school notes interleave (3,916), ebook 16564 a bilingual
edition's render and apparatus (5,083), ebook 20732 a bilingual
interleave whose title page states the design (4,330), ebook 25861
an english reader (2,719), ebooks 20771 and 63139 above the
standing scale (54 and 55 common-word hits, head and trailing
scaffolding, no mid-span), and ebook 19635 the 404 page again; two
further english candidates (ebook 3207 Leviathan, ebook 148 the
Autobiography of Benjamin Franklin) probed clean and are not
selected by the roster's declared five-slot design, recorded with
the artifact.

Mechanics, declared: the bridge gate first, against three frozen
sources - the boundary-mark instrument's 288 anchor fields exactly
as that instrument declared them (the restart-budget artifact's 171
anchors and the frozen search-free artifact's 117 full-width
totals), then per cell the standing rows' mark-excluded profiles
verified as replay-equal against the frozen boundary-mark
artifact's stored rows (each standing member's file, ebook,
plant_length, selected_draw_index, full-width total and block
profile as one row check each; each plant's block profile; each
floor's block profile; each plaintext control's profile): 111
profile checks total, 18 per english cell and 19 per latin cell
times 3 files, 399 fields all told; the breadth members carry no
frozen counterpart, their encodings take the declared draw-0 rule
and their facts ride on the declared roster with sha256 records;
any divergence aborts with nothing written.

Pre-run probes, disclosed verbatim, on frozen data through the
declared implementation before the artifact run. Probe 1, the
bridge gate rehearsed: the gate ran at 399 fields compared, no
problem. Probe 2, the corpus freeze facts ahead of the run: ebook
10 at 4,455,950 bytes with stream 4,018,128 tokens (letters
3,225,940, boundary 792,188), ebook 829 at 613,946 bytes with
stream 564,687 (459,023, 105,664), ebook 1041 at 119,936 bytes
with stream 91,745 (73,444, 18,301), ebook 1404 at 1,186,849 bytes
with stream 1,122,186 (929,847, 192,339), ebook 1228 at 970,611
bytes with stream 906,068 (750,086, 155,982), ebook 227 at 495,876
bytes with stream 431,388 (367,595, 63,793), ebook 18837 at 255,543
bytes with stream 225,036 (194,148, 30,888), ebook 226 at 112,390
bytes with stream 87,917 (74,709, 13,208); every stream clears the
45,491-token floor with the header-declared token types 27, 27, 27,
27, 27, 25, 24 and 24, and the fetch verification stands as
declared above. Probe 3, the first cell's declared verdict ahead of
the run, ZL english: shape-outside-analogues with every one of the
eight invariant tests outside - symbol_shares 35 of 36 sorted
positions outside, pair_shares 834 of 1296 positions outside,
empty_type_count 928 against [323, 454], self_pair_share 0.065848
against [0.0187, 0.026741], top_1_share 0.070481 against
[0.018196, 0.035886], top_10_share 0.424435 against
[0.106088, 0.148336], top_50_share 0.893671 against
[0.305696, 0.355739], pair_entropy 4.010179 against
[5.928491, 6.102864]; the twelve members' full widths 91,744 to
218,662 (their block totals 55,143 to 144,510, block entropies
5.928491 to 6.102864), the plants' identity true, the floors' block
totals 155,062 to 155,329 against the real's block 149,799.
Probe 4, the first latin cell's declared verdict ahead of the run,
ZL latin: shape-outside-analogues with every one of the eight
invariant tests outside - symbol_shares 36 of 36, pair_shares 780
of 1296, empty_type_count 928 against [240, 503], self_pair_share
0.065848 against [0.011829, 0.023974], top_1_share 0.070481 against
[0.013483, 0.02536], top_10_share 0.424435 against
[0.09782, 0.131916], top_50_share 0.893671 against
[0.268516, 0.336503], pair_entropy 4.010179 against
[5.980168, 6.252046]; the eleven members' full widths 45,490 to
218,662 with block entropies 5.980168 to 6.252046 (the breadth's
classical members extend the standing latin band's entropy top end
upward from 6.104489 to 6.252046 while the real's sits at
4.010179), the plants' identity true, the floors' block totals
155,145 to 155,274. Probe 5, the plaintext control recorded
unchanged: every control's profile equals its frozen boundary-mark
counterpart field for field - ZL english entropy 5.139035, ZL latin
5.06327, GC english 5.139139, GC latin 5.063406, IT english
5.139068, IT latin 5.062979, all on their 729-type states.
Probe 6: none; the four remaining cells are unseen until the
declared run. The probes' disclosed first-cell verdicts do not
decide the artifact: the artifact run prices all six cells through
the same declared code, and the disclosure's honest question is
recorded over all of them.

The standing limitations are inherited from the held-out screen: no
mapping is published anywhere in this artifact, no recovered
assignment is stored as a key, plaintext_recovered_percent stays 0,
the reference prose is modern printed text outside the manuscript's
century, and nothing here is a reading or a language claim.

Thirteenth declared measurement, the matched-truncation
interior-shape instrument, declared after the corpus-breadth
instrument widened every band across the corpus's written registers
and no cell reported the inside verdict that widening made easier,
and before any run of it beyond the probes it discloses.

The disclosed background, declared in advance: the interior's
separation held as the roster grew, but every search-free artifact
in this family carries its disclosed size caveat - the real's
profile prices kept-adjacent pairs of a stream whose unmapped
events break adjacency (126 unmapped events inside ZL's 218,663,
1,769 inside GC's 186,708, none inside IT's 220,532), while every
simulated encoding prices a full stream's pairs. The standing band
encodings sell their summaries on full-stream masses (218,662
pairs ZL, 186,707 GC, 220,531 IT) while the real prices 218,415,
183,199 and 220,531 kept-adjacent pairs, so a skeptically read
inside-or-outside question can be re-asked on the real's own
scale: cut every simulated encoding to the real's own counted
pair mass and re-price the same declared question unchanged.
The declared truth about the arithmetic, recorded as design: this
cut can move a band's closed ranges both ways - a cut tail removes
pair mass the standing profile priced, so matched extremes can sit
below or above their standing counterparts per invariant, and both
verdict directions are open in this design (a cell can newly
report inside its matched band, and an invariant standing inside
can leave its matched band); the artifact records every movement
and the question is asked over all of them. The
declared truthful question: with the band's streams matched to
the real's own counted pair mass under the declared cut, does the
real's mark-excluded profile sit inside the matched band's range
on every declared invariant in every (file, language) cell, or is
at least one invariant outside - the measured test of whether the
interior's separation is a length artifact of the real's own
counted mass or holds as the masses match.

The declared design, before the run: the corpus-breadth
instrument's roster, state space and verdict rule unchanged -
the same twelve english and eleven latin members per cell, every
profile still the mark-excluded block of its pair-count matrix
(1296 ordered types, the mark's row and column excluded on both
sides exactly as declared there, the same six
relabeling-invariant summaries priced under the declared
strict-all no-margin rule, the standing alphabet-width disclosure
carried) - with every simulated stream cut to the declared basis:
the cell's real counted pair total + 1 tokens (ZL 218,416, GC
183,200, IT 220,532), the standing truncated reference's first
basis tokens, so a cut stream's full width equals the real's
counted pair total exactly (ZL 218,415, GC 183,199, IT 220,531),
the same mass the floors already price by construction, while a
stream at or below the basis stays whole. Each band member's
encoding and every plant re-runs its frozen chain (the standing
members' frozen selected-draw counts replayed, the breadth
members' declared draw 0) over the matched stream, and each row
carries its standing-basis anchors beside its matched facts
(file, ebook, plant_length, selected_draw_index, draw_rule, and
the standing encoding's own full width, gate-anchored to the
frozen corpus-breadth rows; then matched_length, its matched
total, the row's full width at exactly matched length - 1, and
matched_profile). The floors replay unchanged (a floor's shuffled
kept-adjacency already prices exactly the real's counted pair
total), the plaintext control records its standing profile and
its matched cut beside it, the real stands unchanged, and the
envelope runs the real's unchanged mark-excluded profile against
the matched band's profiles under the strict-all rule.

The roster's disposition, declared before the run: no new corpus
files, no re-fetch, no re-probe, no re-hash - the corpus-breadth
roster's eight accepted files, rejected candidates, sha256
records, floor and fetch verification stand as that instrument
declared and recorded them, taken by reference here. The cut's
disposition of the roster per cell: eleven members cut and the
Sonnets whole in every english cell of the ZL and GC files, five
members cut and six whole in every latin cell (the below-basis
whole members at 45,491, 77,529, 77,572, 87,917, 132,608 and
143,947 tokens price their standing totals unchanged), the IT
cells cut nothing anywhere because their real transcriptions
hold no unmapped events, the plants cut everywhere in the ZL and
GC cells and nowhere in IT, and the floors never re-cut. The
removed masses are bounded by the cut's own size: ZL 247 tokens
of a standing 218,663 (247 of its 218,662 full-width pairs,
0.11296 percent), GC 3,508 of 186,708 (3,508 of 186,707,
1.87888 percent), IT 0.

Mechanics, declared: the bridge gate first, against three frozen
sources - the corpus-breadth instrument's 399 anchor fields
exactly as that instrument declared them (the boundary-mark
gate's 288 anchors and the 111 standing profile checks), then
per cell the frozen corpus-breadth rows' standing replays
verified against fresh re-derivations (each member row's file,
ebook, plant_length, selected_draw_index, draw_rule, full-width
total and block profile one row check each through its declared
chain; each plant row's index, length, full-width total and
block profile; each floor row's index, full-width total and
block profile; each plaintext control's standing profile; each
cell's real record's eight declared fields), 24 row checks per
english cell and 23 per latin cell, 540 fields all told; the
matched facts carry no frozen counterpart and ride on the
declared roster; any divergence aborts with nothing written.

Pre-run probes, disclosed verbatim, on frozen data through the
declared implementation before the artifact run. Probe 1, the
bridge gate rehearsed: the gate ran at 540 fields compared, no
problem. Probe 2, the matched basis ahead of the run: the real's
counted pair totals 218,415 (ZL), 183,199 (GC) and 220,531 (IT)
make the bases 218,416, 183,200 and 220,532 tokens; the cut
takes the standing streams' trailing tokens only - ZL 247 tokens
of a standing 218,663 (247 of its 218,662 full-width pairs,
0.11296 percent), GC 3,508 of 186,708 (3,508 of 186,707,
1.87888 percent), IT 0 (no cut possible, its basis equal to its
standing length) - and the roster's whole streams sit below the
bases (the Sonnets' 91,745-token english stream in the ZL and GC
cells; the latin cells' below-basis members 45,491, 77,529,
77,572, 87,917, 132,608 and 143,947 tokens), and the floors
already price the real's own masses exactly (ZL 218,415, GC
183,199, IT 220,531 full widths). Probe 3, the first cell's
declared verdict ahead of the run, ZL english:
shape-outside-analogues with every one of the eight invariant
tests outside - symbol_shares 35 of 36 sorted positions outside,
pair_shares 834 of 1296 positions outside, empty_type_count 928
against [323, 454], self_pair_share 0.065848 against
[0.018692, 0.026719], top_1_share 0.070481 against
[0.018187, 0.035877], top_10_share 0.424435 against
[0.106088, 0.148334], top_50_share 0.893671 against
[0.305696, 0.355757], pair_entropy 4.010179 against
[5.928491, 6.102985]; the twelve matched members ran 11 cut and
the Sonnets whole (matched full widths 91,744 to 218,415 with
block totals 55,143 to 144,349 and block entropies 5.928491 to
6.102985), the plants cut 218,662 to 218,415 full widths with
block totals 137,339 (identity true at both lengths), the
floors' block totals 155,062 to 155,329 replayed against the
real's block 149,799 (standing 218,663, basis 218,416), and the
plaintext control's standing entropy 5.139035 with the matched
control at 5.13911. Probe 4, the first latin cell's declared
verdict ahead of the run, ZL latin: shape-outside-analogues
with every one of the eight invariant tests outside -
symbol_shares 36 of 36, pair_shares 780 of 1296,
empty_type_count 928 against [240, 503], self_pair_share
0.065848 against [0.011829, 0.023974], top_1_share 0.070481
against [0.013486, 0.02536], top_10_share 0.424435 against
[0.09782, 0.132009], top_50_share 0.893671 against
[0.268516, 0.336674], pair_entropy 4.010179 against
[5.980168, 6.252]; the eleven matched members ran 5 cut and 6
whole (the below-basis whole members price their totals
unchanged at 45,490, 77,528, 77,571, 87,916, 132,607 and
143,946, the cut rows at 218,415) with matched block totals
31,635 to 158,458 and block entropies 5.980168 to 6.252, the
plants cut with block totals 150,839 (identity true at both
lengths), the floors' block totals 155,145 to 155,274, and the
plaintext control's standing entropy 5.06327 with the matched
control at 5.063378; the matched bands moved both ways as the
declared design said they could - the latin entropy ceiling
eased down from the standing 6.252046 to 6.252 while the ZL
english cell's top-1 floor eased down (0.018196 to 0.018187)
and self-pair floor eased down (0.0187 to 0.018692) with its
top-50 ceiling up (0.355739 to 0.355757) and entropy ceiling up
(6.102864 to 6.102985), the ZL latin cell's empty-type band
unchanged [240, 503] and its top-1 floor up a hair (0.013483 to
0.013486). Probe 5, the plaintext controls recorded ahead: all
six standing controls' profiles unchanged field for field
(5.139035, 5.139139 and 5.139068 english, 5.06327, 5.063406 and
5.062979 latin on their 729-type states) with the matched
controls re-cut to the bases recorded beside them (5.13911,
5.139014 and 5.139068 english, 5.063378, 5.063275 and 5.062979
latin, the IT controls identical by the degenerate case).
Probe 6: none; the four remaining cells are unseen until the
declared run. The probes' disclosed first-cell verdicts do not
decide the artifact: the artifact run prices all six cells
through the same declared code, and the disclosure's honest
question is recorded over all of them.

The standing limitations are inherited from the held-out screen: no
mapping is published anywhere in this artifact, no recovered
assignment is stored as a key, plaintext_recovered_percent stays 0,
the reference prose is modern printed text outside the manuscript's
century, and nothing here is a reading or a language claim.

Fourteenth declared measurement, the matched-basis ladder,
declared after the matched-truncation instrument cut every
simulated stream to the real's own counted pair mass and no cell
reported the inside verdict that matching granted, and before any
run of it beyond the probes it discloses.

The disclosed background, declared in advance: the matched
truncation priced one basis - the real's own mass anchor - and its
verdicts held with the cut's movements recorded both ways, but one
anchor answers only the question the anchor asks; a band whose
streams carry a different mass can reprice its closed ranges
either way, so the honest next question is the ladder: sweep the
basis at declared rungs, re-price the roster's bands at each rung,
hold the real's profile unchanged everywhere, and ask whether any
rung's mass admits the real's interior profile inside on every
declared invariant or every rung stands outside, with every scalar
movement against the anchor rung's bands readable and recorded
both ways.

The declared design, before the run: the matched-truncation
instrument's roster, state space, six relabeling-invariant
summaries and strict-all no-margin verdict rule unchanged, with
the truncation basis swept at declared rungs - the anchor rung
first, the cell's real counted pair total + 1 tokens (ZL 218,416,
GC 183,200, IT 220,532), then three descended rungs at floor(p x
the anchor basis) tokens for p 0.75, 0.50 and 0.25 (ZL 163,812,
109,208 and 54,604; GC 137,400, 91,600 and 45,800; IT 165,399,
110,266 and 55,133); at every rung each of the roster's encodings
re-runs its own frozen chain (the standing members' selected
draws replayed, the breadth members' declared draw 0) over the
standing truncated reference's first rung tokens, a stream above
the rung cut accordingly and a stream at or below it stays whole,
every cut row pricing its rung basis - 1 pairs full width (the
exact identity, matched length - 1); the declared truth about the
arithmetic is the matched-truncation instrument's restated: a cut
can move a band's closed ranges both ways, both verdict
directions are open at every rung, and the artifact prices every
rung's bands beside the anchor rung's so every scalar movement is
readable both ways; the real is priced once and never re-cut, so
below the anchor rung the real's full-mass profile is compared
against bands whose streams price the rung's descending mass and
the ladder reads the bands' movements, not a mass match, at those
rungs; the floors replay unchanged (a floor's shuffled
kept-adjacency already prices exactly the real's counted pair
total), the standing plant width and the standing plaintext
profile are recorded once each as rung-independent facts, the
plaintext control's matched re-cut is recorded per rung beside
its standing profile, the IT cells are degenerate only at the
anchor rung (their basis there equals the standing truncated
length because the real transcription holds no unmapped events)
and at the lower rungs their streams cut like every other cell's,
and the rung-cell verdicts are asked together over all 24.

Mechanics, declared: the bridge gate first, in two stages - the
matched-truncation instrument's gate exactly as that instrument
declared it (the corpus-breadth instrument's 399 anchor fields
and the 141 standing-row replay checks, 540 fields), then the
anchor rung's six cells verified equal to the frozen
matched-truncation artifact's six cells field for field (each
anchor member row's matched block, each anchor plant row's
matched block, each anchor matched plaintext control, each
anchor's basis with its cut counts, and each anchor's envelope
result, 20 checks per english cell and 19 per latin cell, 117
checks total), 657 fields all told; the three descended rungs
carry no frozen counterpart and ride on the declared rung rule;
any divergence aborts with nothing written.

Pre-run probes, disclosed verbatim, on frozen data through the
declared implementation before the artifact run. Probe 1, the
bridge gate rehearsed: the gate ran at 657 fields compared, no
problem. Probe 2, the rung bases and the roster's cuts ahead of
the run: the anchors 218,416 (ZL), 183,200 (GC) and 220,532 (IT)
make the rung bases ZL 218,416, 163,812, 109,208 and 54,604; GC
183,200, 137,400, 91,600 and 45,800; IT 220,532, 165,399,
110,266 and 55,133 (anchor, 75, 50 and 25 percent); the members
cut per rung: ZL english 11, 11, 11, 12 (the Sonnets whole until
the 25 percent rung cuts it too); ZL latin 5, 5, 7, 10; GC
english 11, 11, 12, 12; GC latin 5, 6, 7, 10; IT english and IT
latin 0 at the anchor (the degenerate case, nothing to cut) and
thereafter 11, 11, 12 english and 5, 7, 10 latin; the plants cut
5 at every rung in every cell of ZL and GC and 0 at the anchor
then 5, 5 and 5 in the IT cells; the floors never re-cut. Probe
3, the first english cell's declared portraits ahead of the run,
ZL english: every rung's verdict shape-outside-analogues with
every one of the eight invariant tests outside - the anchor
rung's bands the matched-truncation artifact's bands exactly
(empty_type_count 928 against [323, 454], self_pair_share
0.065848 against [0.018692, 0.026719], top_1_share 0.070481
against [0.018187, 0.035877], top_10_share 0.424435 against
[0.106088, 0.148334], top_50_share 0.893671 against
[0.305696, 0.355757], pair_entropy 4.010179 against
[5.928491, 6.102985]); the 75 percent rung's bands [318, 464],
[0.01884, 0.027095], [0.018173, 0.035196], [0.106088, 0.157183],
[0.305696, 0.368859] and [5.92046, 6.115742]; the 50 percent
rung's [341, 495], [0.01878, 0.027796], [0.015177, 0.034405],
[0.100396, 0.157691], [0.305696, 0.370604] and
[5.90532, 6.108939]; the 25 percent rung's [376, 505],
[0.018805, 0.027025], [0.014518, 0.03463], [0.100414, 0.160534],
[0.309486, 0.372217] and [5.883769, 6.098317]; the scalar band
ends moved against the anchor rung both ways: 4 down and 6 up
with 2 stayed at 75 percent, 4 down and 7 up with 1 stayed at 50,
5 down and 7 up with 0 stayed at 25. Probe 4, the first latin
cell's declared portraits ahead of the run, ZL latin: every
rung's verdict shape-outside-analogues with every one of the
eight invariant tests outside - the anchor rung's bands
[240, 503], [0.011829, 0.023974], [0.013486, 0.02536],
[0.09782, 0.132009], [0.268516, 0.336674] and [5.980168, 6.252];
the 75 percent rung's [283, 503], [0.012506, 0.023974],
[0.01335, 0.02536], [0.097045, 0.134341], [0.268516, 0.339127]
and [5.980168, 6.254451]; the 50 percent rung's [360, 503],
[0.013366, 0.024518], [0.013618, 0.025917], [0.09782, 0.132131],
[0.268516, 0.335977] and [5.980168, 6.250767]; the 25 percent
rung's [399, 537], [0.013527, 0.021909], [0.013764, 0.025031],
[0.098316, 0.138755], [0.272333, 0.348076] and
[5.951767, 6.248471]; the scalar band ends moved against the
anchor rung 2 down and 5 up with 5 stayed at 75 percent, 2 down
and 6 up with 4 stayed at 50, 4 down and 8 up with 0 stayed at
25. Probe 5, the matched plaintext controls recorded ahead at
the four rungs against their standing profiles: ZL english
5.13911, 5.13898, 5.138153 and 5.139435 against 5.139035; ZL
latin 5.063378, 5.063174, 5.068902 and 5.077888 against 5.06327;
GC english 5.139014, 5.138704, 5.135251 and 5.144321 against
5.139139; GC latin 5.063275, 5.061239, 5.07202 and 5.078094
against 5.063406; IT english 5.139068, 5.138764, 5.138225 and
5.139379 against 5.139068 (identical at the anchor by the
degenerate case); IT latin 5.062979, 5.063274, 5.068993 and
5.077053 against 5.062979 (identical at the anchor). Probe 6:
none; the four remaining cells are unseen until the declared
run. The probes' disclosed portraits do not decide the artifact:
the artifact run prices all 24 rung-cells through the same
declared code, and the disclosure's honest question is recorded
over all of them.

The standing limitations are inherited from the held-out screen:
no mapping is published anywhere in this artifact, no recovered
assignment is stored as a key, plaintext_recovered_percent stays
0, the reference prose is modern printed text outside the
manuscript's century, and nothing here is a reading or a
language claim.

Fifteenth declared measurement, the real-at-basis ladder, declared
after the matched-basis ladder swept the truncation basis over the
anchor rung and its 75, 50 and 25 percent rungs and read only the
bands' movements at every descended rung, and before any run of it
beyond the probes it discloses.

The disclosed background, declared in advance: the matched-basis
ladder priced the bands' sides of the descending masses and left the
real's side priced once, so its anchor rung's comparison was
mass-matched and its descended rungs' were not - the honest next
question is the real's own side of the sweep: take the real's own
kept-adjacent pair sequence, cut it to each declared rung's mass like
every simulated stream, re-price it through the same mark-excluded
block and the same six summaries, and set it beside each rung's
re-priced bands, so every rung's comparison is mass-matched on both
sides for the first time in this family, and the declared question
becomes whether the real's own descending profile tracks the bands'
descension or stays apart down the ladder, the question the
matched-basis ladder disclosed but could not ask.

The declared design, before the run: the matched-basis ladder's
roster, state space (1296 ordered types, the boundary mark's row and
column excluded on both sides), six relabeling-invariant summaries,
strict-all no-margin verdict rule and four declared rungs unchanged -
the anchor rung the cell's real counted pair total + 1 tokens (ZL
218,416, GC 183,200, IT 220,532), then floor(p x the anchor basis)
rungs at p 0.75, 0.50 and 0.25 (ZL 163,812, 109,208 and 54,604; GC
137,400, 91,600 and 45,800; IT 165,399, 110,266 and 55,133); the
rung bands the frozen matched-basis ladder's rung facts taken by
reference, their own measurements verified under that instrument's
gate and tests, no encoding re-run on the band side anywhere; at
every rung the real prices its first basis - 1 kept-adjacent pairs
(the exact ordered pairs _count_matrix_37 counts, ordered along the
original stream, the unmapped events breaking the adjacency exactly
as disclosed since the interior instrument) through the same
mark-excluded block; the declared truth about the arithmetic is the
family's restated plus one new identity: the real's cut can move its
own profile both ways exactly as a band's cut moves a band's closed
ranges both ways, and the real's rung mass equals every one of the
rung's cut rows' full-width masses exactly - the mass-match identity
verified against the frozen rung's rows before any envelope is
formed, a rung's whole rows keeping their standing masses inside
the envelope, the same disclosed mix the anchor rung carried; the
anchor rung's re-priced profile is the real's unchanged
matched-basis ladder profile exactly and every descended rung's is
fresh; the rung-cell verdicts asked together over all 24.

Mechanics, declared: the bridge gate first, in two stages - the
matched-basis ladder's gate exactly as that instrument declared it
(the matched-truncation instrument's 540 anchor and replay fields
plus the 117 anchor-rung replay checks, 657 fields), then per cell
the fresh real record verified against the frozen matched-basis
ladder's cell record (its eight declared fields), the four rung
bases' identities, and the anchor rung's fresh envelope equal to
the frozen anchor rung's envelope result, 6 checks per cell, 36
checks total, 693 fields all told; the three descended rungs'
envelopes carry no frozen counterpart and ride on the declared rung
rule, whose mass-match identity aborts on any divergence; any
divergence aborts with nothing written.

Pre-run probes, disclosed verbatim, on frozen data through the
declared implementation before the artifact run. Probe 1, the
standing ladder gate rehearsed: the gate ran at 657 fields compared,
no problem. Probe 2, the real's pair sequences ahead of the run:
ZL's kept-adjacent pair sequence counts 218,415 ordered pairs, GC's
183,199 and IT's 220,531, each recounting its _count_matrix_37 matrix
exactly, each full sequence pricing the frozen real profile exactly
(at the anchor rung the prefix is the whole sequence), with
68,616 (ZL), 71,384 (GC) and 72,880 (IT) of those pairs carried by
the boundary mark's row and column and excluded from every block.
Probe 3, the first english cell's declared portrait ahead of the
run, ZL english: every rung's verdict shape-outside-analogues with
every one of the eight invariant tests outside - the anchor rung's
re-priced profile the frozen real profile exactly (empty_type_count
928 against [323, 454], self_pair_share 0.065848 against
[0.018692, 0.026719], top_1_share 0.070481 against
[0.018187, 0.035877], top_10_share 0.424435 against
[0.106088, 0.148334], top_50_share 0.893671 against
[0.305696, 0.355757], pair_entropy 4.010179 against
[5.928491, 6.102985]); the 75 percent rung's masses 163,811 pairs
with the re-priced profile 950 empties, self 0.068229, top_1
0.073934, top_10 0.418115, top_50 0.892615 and entropy 4.014465
against its bands; the 50 percent rung's 109,207 pairs, 980
empties, self 0.073015, top_1 0.076343, top_10 0.432937, top_50
0.899851 and entropy 3.982947; the 25 percent rung's 54,603 pairs,
1028 empties, self 0.083007, top_1 0.06476, top_10 0.463045,
top_50 0.914338 and entropy 3.904198 - the real's own descent
against its anchor scalars 5 down and 13 up with 0 stayed, the
vector outsides (symbols, pairs) 35 and 834, 33 and 824, 33 and
793, 36 and 787 across the four rungs. Probe 4, the first latin
cell's declared portrait ahead of the run, ZL latin: every rung's
verdict shape-outside-analogues with every one of the eight
invariant tests outside, the same re-priced real profile at every
rung (the real is the same stream and the bands differ by the
roster's language), members cut 5, 5, 7 and 10 across the
rungs, the vector outsides 36 and 780, 34 and 779, 32 and 782, 35
and 746. Probe 5, the honest sweep ahead of the run: all 24
rung-cell verdicts shape-outside-analogues; GC latin's
self_pair_share, the family's one standing inside invariant,
inside at its three upper rungs (0.015928 against
[0.011979, 0.023941], 0.016822 against [0.012489, 0.023941],
0.016628 against [0.013329, 0.023837]) and outside at its 25
percent rung (0.021604 against [0.01295, 0.021521]) - the
standing inside invariant departs its band exactly where the
mass-match first deepens; GC english's self_pair_share carries the
counterpart motion, outside below its band at its three upper
rungs (0.015928 against [0.018513, 0.027183], 0.016822 against
[0.018404, 0.027769], 0.016628 against [0.018849, 0.027852]) and
inside at its 25 percent rung (0.021604 against
[0.018382, 0.025854]); every other cell's every rung stays
all-eight-outside; the real's own descents against the anchor
scalars: ZL english and ZL latin 5 down and 13 up with 0 stayed,
GC english and GC latin 7 down and 11 up with 0 stayed, IT english
and IT latin 5 down and 13 up with 0 stayed. Probe 6: none; the
declared run prices every cell itself through the artifact. The
probes' disclosed portraits do not decide the artifact: the
artifact run prices all 24 rung-cells through the same declared
code, and the disclosure's honest question is recorded over all of
them.

The standing limitations are inherited from the held-out screen:
no mapping is published anywhere in this artifact, no recovered
assignment is stored as a key, plaintext_recovered_percent stays
0, the reference prose is modern printed text outside the
manuscript's century, and nothing here is a reading or a
language claim.

Sixteenth declared measurement, the cut-geometry attribution
instrument, declared after the real-at-basis ladder mass-matched
every rung's comparison on both sides and read the real's own
descent, and before any run of it beyond the probes it discloses.

The disclosed background, declared in advance: the real-at-basis
ladder left one question open - its descended rungs showed the
real's concentration deepening as its mass is cut, and a similar
deepening appears in every cut sequence, so the ladder's record
cannot tell whether the real's deepening is a function of the
mass alone or of the real's own ordering; the honest next
question is attribution: take the real's own kept-adjacent pair
sequence, cut it at the same frozen rung masses under declared
geometries that differ only in which positions the cut keeps
(the standing prefix cut the real-at-basis ladder priced, a
suffix cut keeping the last mass positions, and declared seeded
random submasses keeping a seed's first mass positions of a
declared permutation), re-price every geometry row through the
same mark-excluded block and the same six summaries, and price
every row against the same frozen rung bands under the same
strict-all rule, so same-mass cuts that differ only in geometry
can be compared row against row: do they re-price the real the
same way, so the deepening is mass alone, or do they disagree,
so the real's own ordering carries it.

The declared design, before the run: the real-at-basis ladder's
roster, state space (1296 ordered types, the boundary mark's row
and column excluded on both sides), six relabeling-invariant
summaries, strict-all no-margin verdict rule and four declared
rungs unchanged; the rung bands the frozen matched-basis
ladder's rung member profiles taken by reference, no encoding
re-run on the band side anywhere, and the real-at-basis
ladder's own rung records re-derived fresh and verified field
for field against its frozen artifact in the gate; the real's
own kept-adjacent pair sequence cut at each rung's mass (the
rung's basis - 1 pairs, the exact full-width mass every one of
the frozen rung's cut rows prices) under six declared
geometries recorded as design before any pricing: the prefix
cut prices the sequence's first mass positions (the
real-at-basis ladder's own row, verified in the gate), the
suffix cut prices the sequence's last mass positions, and each
of four random rows prices a declared seed's permutation of the
sequence's positions at its first mass positions; the declared
new seed kind homo_cut_geom (id 30), positions 0 to 3, per file
with the language slot fixed at 0 because the real's side is
identical for both languages of a file, each seed one
np.random.default_rng(_seed(CELL_ID, KIND_ID["homo_cut_geom"],
0, index)) permutation of the sequence's positions, so one
seed's rung submasses are nested subsets across the rungs and
no selection is performed over seeds; every row prices its
rung's mass exactly (the mass-match identity, enforced in code
on every row before any envelope is formed); a random submass
of the real's own pair multiset samples the multiset's relative
frequencies with sampling noise alone, so its expected profile
is the whole sequence's profile and not the prefix cut's, and
this is the declared attribution arithmetic the row verdicts
are read against; at the anchor rung every geometry's submass
is the whole sequence and its profile the frozen real-at-basis
ladder's whole-sequence profile exactly (the degenerate
identity, enforced in the row builder); the rung-cell verdicts
asked over all 144 geometry rung-cells together (24 rung-cells
times the six geometries, the anchor rung's 24 the declared
degenerate identity cases).

Mechanics, declared: the bridge gate first, in two stages - the
real-at-basis ladder's gate exactly as that instrument declared
it (the matched-basis ladder's 657 fields plus the
real-at-basis ladder's 36 per-cell checks, 693 fields), then
per cell the fresh real-at-basis rung records verified against
the frozen real-at-basis ladder artifact's rungs field for
field (each rung's mass, its boundary-carried pairs, its
prefix profile, its envelope result and its verdict, 5 checks
per rung, 20 per cell, 120 checks total), 813 fields all
told; the suffix and random rows carry no frozen counterpart
and ride on the declared geometry rule, whose mass-match and
degenerate anchor identities abort on any divergence; any
divergence aborts with nothing written.

Pre-run probes, disclosed verbatim, on frozen data through the
declared implementation before the artifact run. Probe 1, the
cut-geometry gate rehearsed: the gate ran at 0 problems, 813
fields compared. Probe 2, the degenerate anchor identity: ZL,
GC and IT each price the frozen whole-sequence profile exactly
for all six geometries at the anchor rung (anchor degenerate
identity for all six geometries True per file). Probe 3, the
declared nesting: seed 0's rung submasses nested subsets True
per file. Probe 4, the first english cell's declared portraits
ahead of the run, ZL english, every geometry row against its
rung's frozen band: at the anchor rung every geometry's row is
the degenerate identity (68,616 carried, 928 empties, self
0.065848, top_1 0.070481, top_10 0.424435, top_50 0.893671,
entropy 4.010179, every row verdict shape-outside-analogues
with all eight tests outside); at the 75 percent rung (mass
163,811) the suffix row carries 52,045 pairs and prices 942
empties, self 0.060009, top_1 0.072428, top_10 0.415296,
top_50 0.888714 and entropy 4.031522, and the four random rows
carry 51,362 to 51,568 pairs and price 946 to 950 empties,
self 0.065567 to 0.066341, top_1 0.069977 to 0.070957, top_10
0.42441 to 0.425183, top_50 0.893071 to 0.893971 and entropy
4.007986 to 4.009743; at the 50 percent rung (mass 109,207)
the suffix row carries 34,516 pairs and prices 963 empties,
self 0.058642, top_1 0.064586, top_10 0.419354, top_50
0.890629 and entropy 4.024671, and the four random rows carry
34,184 to 34,384 pairs and price 971 to 979 empties, self
0.065835 to 0.066272, top_1 0.07024 to 0.070757, top_10
0.423537 to 0.425658, top_50 0.892854 to 0.894713 and entropy
4.005017 to 4.009556; at the 25 percent rung (mass 54,603)
the suffix row carries 17,176 pairs and prices 1,020 empties,
self 0.058701, top_1 0.060117, top_10 0.448099, top_50
0.900713 and entropy 3.97606, and the four random rows carry
16,984 to 17,266 pairs and price 1,005 to 1,013 empties, self
0.065402 to 0.067815, top_1 0.071013 to 0.071633, top_10
0.424298 to 0.428514, top_50 0.892359 to 0.894601 and entropy
3.998056 to 4.009569; every probed row verdict
shape-outside-analogues with all eight tests outside. The
probes' disclosed attribution arithmetic, recorded before the
run: the random rows' scalars stay at the anchor's neighborhood
down the whole ladder (self near 0.066, entropy near 4.0 nats)
while the prefix row's self rises 0.065848, 0.068229, 0.073015
and 0.083007 down the rungs with entropy 4.010179, 4.014465,
3.982947 and 3.904198, and the suffix row's self falls to
0.060009, 0.058642 and 0.058701 with entropy 4.031522, 4.024671
and 3.97606 - same-mass cuts already disagreeing in both
directions away from the mass-only expectation at this cell,
which is exactly what the declared question prices, and the
artifact run asks it over all 144 geometry rung-cells. Probe 5:
none; the five remaining cells are unseen until the declared
run. The probes' disclosed portraits do not decide the
artifact: the artifact run prices all 144 geometry rung-cells
through the same declared code, and the disclosure's honest
question is recorded over all of them.

The standing limitations are inherited from the held-out screen:
no mapping is published anywhere in this artifact, no recovered
assignment is stored as a key, plaintext_recovered_percent stays
0, the reference prose is modern printed text outside the
manuscript's century, and nothing here is a reading or a
language claim.

Seventeenth declared measurement, the stream-position instrument,
declared after the cut-geometry attribution instrument attributed
the real-at-basis ladder's deepening to the real's own ordering
and located the ordering effect in the stream's opening pairs,
and before any run of it beyond the probes it discloses.

The disclosed background, declared in advance: the cut-geometry
instrument held the mass fixed and moved only the cut's geometry,
and the geometry turned out to carry the deepening: in ZL english
the prefix cut's self-pair share rises 0.065848, 0.068229,
0.073015 and 0.083007 down the rungs while the suffix cut's falls
to 0.060009, 0.058642 and 0.058701 and the four seeded random
cuts hold the whole-sequence neighborhood (0.065402 to 0.067815
at the 25 percent rung), so same-mass cuts disagree in both
directions while the random rows sit exactly where sampling noise
alone puts them, and every geometry's row priced shape-outside-
analogues against its frozen rung band (all 144 geometry
rung-cells), so the separation the search-free instruments found
is in the counts and the deepening the mass-matched ladder
measured is in the ordering. What that record leaves open is
position within the stream: is the real's concentration a smooth
function of stream position, or do particular spans of the stream
carry it? The honest next question is the span question, not more
mass-matched cuts: divide the real's own kept-adjacent pair
sequence into four declared equal-count consecutive segments,
price each segment's profile fresh, record the four segment
profiles beside each other and beside the whole-sequence profile,
and answer by which segments' scalars sit above the whole-sequence
values and which below.

The declared design, before the run: the corpus-breadth roster,
the state space (1296 ordered types, the boundary mark's row and
column excluded on both sides) and the six relabeling-invariant
summaries unchanged; the real's own ordered kept-adjacent pair
sequence divided into four declared equal-count consecutive
segments, the boundaries placed by the standing basis arithmetic
the rungs already use - the first three boundaries sit at
int(quarter x the anchor basis) positions with the anchor basis
the kept pair total + 1, at the quarters 0.25, 0.5 and 0.75, and
the last boundary is the sequence's end; every file's kept pair
total is three over a multiple of four, so each file's first
three segments are the same size and the remainder lands on the
last segment, the four sizes being, for ZL, 54,604, 54,604,
54,604 and 54,603 kept-adjacent pairs, for GC 45,800, 45,800,
45,800 and 45,799, and for IT 55,133, 55,133, 55,133 and 55,132;
each segment prices every kept-adjacent pair of its own
consecutive interval, no pair dropped, no pair synthesized, so
the four segments partition the whole sequence exactly, and each
segment's profile is priced fresh through the same mark-excluded
block (the segment's own matrix carries its own mark's row and
column excluded) and the same six summaries; the four segment
profiles are recorded beside each other and beside the
whole-sequence profile, the real's side identical for both
languages of a file, so every cell prices the same segment
records; no band is loaded, no envelope is formed, no rung band
side, no verdict and no scalar margin is produced anywhere: the
declared question is answered by direction, and each segment
records, for each of the six scalar summaries it shares with the
whole profile (the empty type count, the self-pair share, the
top-k shares at k 1, 10 and 50, and the pair entropy), whether
its value sits above, below or equal to the whole sequence's
value at the stored 6-decimal rounding, every entry recorded and
no selection performed over anything.

Mechanics, declared: the bridge gate first, per cell: the fresh
whole-sequence profile verified field for field against the
frozen real-at-basis ladder's anchor profile, the four boundaries
recomputed from the declared rule and verified, the four segment
sizes verified, each segment's block-total identity verified (the
segment's profile total equals its own kept pairs minus its own
boundary-carried pairs, the standing identity), the two partition
verified (the four segments' block totals sum to the whole
profile's block total, and their boundary-carried counts sum to
the whole's), the four segments' kept pairs' sum verified against
the whole's, and the whole's own block-total identity verified,
17 fields per cell, 102 fields all told; any divergence
aborts with nothing written.

Pre-run probes, disclosed verbatim, on frozen data through the
declared implementation before the artifact run. Probe 1, the
stream-position gate rehearsed: the gate ran at 0 problems, 102
fields compared. Probe 2, the declared boundaries and sizes per
file, printed in order: ZL's end positions 54,604, 109,208,
163,812 and 218,415 give the four sizes 54,604, 54,604, 54,604
and 54,603; GC's 45,800, 91,600, 137,400 and 183,199 give
45,800, 45,800, 45,800 and 45,799; IT's 55,133, 110,266, 165,399
and 220,531 give 55,133, 55,133, 55,133 and 55,132. Probe 3, the
partition identities per file: the four segments' kept pairs sum
to the whole's (218,415, 183,199 and 220,531), their block totals
sum to the whole's (149,799, 111,815 and 147,651) and their
boundary-carried counts sum to the whole's (68,616, 71,384 and
72,880), all True per the probe. Probe 4, the first file's
declared portraits ahead of the run, beside the whole-sequence
profile (kept 218,415, carried 68,616, empties 928, self
0.065848, top_1 0.070481, top_10 0.424435, top_50 0.893671,
entropy 4.010179): the opening segment (54,604 pairs, 16,571
carried) prices empties 1,028, self 0.083007, top_1 0.06476,
top_10 0.463045, top_50 0.914338 and entropy 3.904198 (above,
above, below, above, above and below); the second segment (54,604
pairs, 17,529 carried) prices empties 1,015, self 0.062765,
top_1 0.088227, top_10 0.437141, top_50 0.891247 and entropy
4.005492 (above, below, above, above, below and below); the
third segment (54,604 pairs, 17,340 carried) prices empties
1,007, self 0.058582, top_1 0.069075, top_10 0.397112, top_50
0.88721 and entropy 4.051398 (above, below, below, below, below
and above); the closing segment (54,603 pairs, 17,176 carried)
prices empties 1,020, self 0.058701, top_1 0.060117, top_10
0.448099, top_50 0.900713 and entropy 3.97606 (above, below,
below, above, above and below) - the directions already fan out
in both directions per summary, and the artifact run records
them for every cell. Probe 5: none; the remaining files are
unseen until the declared run. The probes' disclosed portraits do
not decide the artifact: the artifact run prices every segment of
every cell through the same declared code, and the disclosure's
honest question is recorded over all of them.

The standing limitations are inherited from the held-out screen:
no mapping is published anywhere in this artifact, no recovered
assignment is stored as a key, plaintext_recovered_percent stays
0, the reference prose is modern printed text outside the
manuscript's century, and nothing here is a reading or a
language claim.

Eighteenth declared measurement, the boundary-walk instrument,
declared after the stream-position instrument attributed the
real's concentration to particular spans - the opening span
pricing above-whole self in every file with below-whole entropy,
the second span carrying the top_1 peak in ZL and IT while GC's
is its flattest, the third span flattest with above-whole
entropy, the closing span re-concentrating the wide pool - and
before any run of it beyond the probes it discloses.

The disclosed background, declared in advance: the
stream-position instrument recorded that the direction tables
flip sign at declared boundaries instead of drifting, so the
concentration turns on and off between spans. What that record
leaves open is where along the stream each flip happens: a
boundary between two spans locates the flip only to within a
quarter of the stream. The honest next question is the walk:
move one declared boundary head along declared positions between
the stream's first and second declared boundaries, price the two
spans beside the head fresh at every position, and record every
position's direction tables, so the flips acquire declared
locations: where the second span's top_1 spike begins and ends
along the stream, and whether the opening span's above-whole
concentration turns off at a declared location or drifts
smoothly across positions.

The declared design, before the run: the corpus-breadth roster,
the state space (1296 ordered types, the boundary mark's row and
column excluded on both sides) and the six relabeling-invariant
summaries unchanged; more mass-matched cuts are refused: the
window mass is fixed at the standing basis arithmetic's first
boundary (the int(quarter x the anchor basis) positions the
stream-position instrument already declared, so the window mass
is ZL 54,604, GC 45,800 and IT 55,133 kept-adjacent pairs - one
pair more than the 25 percent rung's mass, whose profile the
stream-position instrument's fresh prices already confluence
with) and the head is walked at int(step x the anchor basis)
positions for the declared steps j / 100 with j running
25 to 50 inclusive, 26 heads per file (ZL heads 54,604 to
109,208, GC 45,800 to 91,600, IT 55,133 to 110,266). At every
head the two spans beside the head are the window-mass span
ending at the head and the window-mass span starting at the
head, each priced fresh through the same mark-excluded block
(the span's own matrix carries its own mark's row and column
excluded) and the same six summaries, no pair dropped, no pair
synthesized, so the two spans beside the head share the head
exactly and each span carries the same declared mass; the first
head's two spans are exactly the stream-position instrument's
first and second segments and the last head's two spans exactly
its second and third segments (the declared confluence,
verified in the gate against that instrument's frozen stored
profiles); no band is loaded, no envelope is formed, no verdict
and no scalar margin is produced anywhere in this artifact: the
declared question is answered by direction, and each span
records, for each of the six scalar summaries it shares with
the whole profile, whether its value sits above, below or equal
to the whole sequence's value at the stored 6-decimal rounding,
every entry recorded and no selection performed over anything;
the real's side is identical for both languages of a file, so
every cell prices the same walk records.

Mechanics, declared: the bridge gate first, per cell: the fresh
whole-sequence profile verified field for field against the
frozen real-at-basis ladder's anchor profile, the 26 heads
recomputed from the declared rule and verified one field each,
the four declared stream-position boundaries and sizes verified
against that instrument's frozen records, the two window sizes
verified at every head one field each, the first head's two
span profiles verified against the stream-position instrument's
stored first and second segments and the last head's two span
profiles against its stored second and third segments, and the
whole's own block-total identity verified, 86 fields per cell,
516 fields all told; any divergence aborts with nothing written.

Pre-run probes, disclosed verbatim, on frozen data through the
declared implementation before the artifact run. Probe 1, the
boundary-walk gate rehearsed: 0 problems, 516 fields compared,
the declared 86 per cell, no divergence in any of them. Probe 2,
the declared heads and window sizes per file, printed in order
at the first and last heads with the head count: ZL window
54,604, 26 heads, first 54,604, last 109,208; GC window 45,800,
26 heads, first 45,800, last 91,600; IT window 55,133, 26 heads,
first 55,133, last 110,266. Probe 3, the declared confluence
heads verified against the frozen stream-position records per
file: all four marks true in every file, ZL True/True/True/True,
GC True/True/True/True, IT True/True/True/True. Probe 4, the
first file's declared portraits ahead of the run: the ZL whole
row anchors them (kept 218,415 pairs, 68,616 whole
boundary-carried pairs, 928 empty types, self 0.065848, top_1
0.070481, top_10 0.424435, top_50 0.893671, entropy 4.010179),
and the 26 heads tell this story. The left span's self runs
above for 23 heads (0.083007 at the first head 54,604, peaking
0.085542 at 63,340) and below at the last three (0.065626 at
104,839 down to 0.062765 at 109,208), so the opening span's
above-whole self is still above through 102,655 and is gone by
104,839: it turns off between two declared heads rather than
drifting across them. The left span's top_1 runs below at the
first six heads, above at the seventh and eighth (0.071009 at
67,708 and 0.071104 at 69,893), below at the ninth (0.069494 at
72,077), and above for the remaining seventeen (0.070542 at
74,261 rising to 0.089319 at 104,839, 0.088887 at 107,023 and
0.088227 at 109,208), its top_10 above at all 26 heads, its
top_50 above for 23 heads then below for 3, and its entropy
below at all 26 heads. The right span's self runs below at all
26 heads, its top_1 above for 23 heads (peaking 0.092363 at
61,156) then below at the last three (0.070293 at 104,839), its
top_10 above for the first 13 heads then below for the last 13,
its top_50 below at all 26 heads, and its entropy below at the
first five heads, above at 65,524, below again at 67,708, and
above for the remaining nineteen. No equal entry appears
anywhere in the walk's direction records, matching the standing
expectation, and the left self's flip and the right top_1's flip
sit between the same two declared heads, 102,655 and 104,839.
Probe 5: none; the remaining files are unseen until the declared
run. The probes' disclosed portraits do not decide the artifact:
the artifact run prices every span beside every head through the
same declared code, and the disclosure's honest question is
recorded over all of them.

The standing limitations are inherited from the held-out screen:
no mapping is published anywhere in this artifact, no recovered
assignment is stored as a key, plaintext_recovered_percent stays
0, the reference prose is modern printed text outside the
manuscript's century, and nothing here is a reading or a
language claim.

Nineteenth declared measurement, the finer-resolution walk
instrument, declared after the boundary-walk instrument located
the direction flips in gaps between consecutive declared
hundredth heads - not one of its 1,872 direction entries records
equal, and its flips turn between two consecutive heads for most
of the tracked records rather than drifting across them - and
before any run of it beyond the probes it discloses.

The disclosed background, declared in advance: the
boundary-walk instrument walked the declared hundredth heads
between the stream's first and second boundaries and recorded
the direction tables at every head. What that record leaves
open is the position inside each gap: the walk prices nothing
between two consecutive hundredth heads, so each flip's
location is only as fine as a hundredth of the stream. The
honest next question is the finer walk: re-walk the same
declared head at declared finer steps inside the located gaps,
price the two spans beside the head fresh at every finer
position, and record every position's direction tables, so
each tracked flip acquires a finer declared location: at which
finer position it turns, whether it turns once or splits into
more than one turn, or whether any of them drifts smoothly
across the gap.

The declared design, before the run: the corpus-breadth roster,
the state space (1296 ordered types, the boundary mark's row and
column excluded on both sides) and the six relabeling-invariant
summaries unchanged; more mass-matched cuts are refused: the
window mass is fixed at the standing basis arithmetic's first
boundary (the int(quarter x the anchor basis) positions, so the
window mass is ZL 54,604, GC 45,800 and IT 55,133 kept-adjacent
pairs) and the head is walked at int(step x the anchor basis)
positions for the declared steps j / 1000 with j running over
the three declared gaps exactly as the boundary-walk instrument
located them: ZL j 470 to 480 inclusive, GC j 430 to 440
inclusive, IT j 480 to 490 inclusive, 11 heads per file, the
first and last heads of each gap exactly the boundary-walk
instrument's recorded heads at that gap's two hundredth steps
(the declared confluence, verified in the gate against that
instrument's frozen stored head records). The tracked flips are
the side and summary direction records the frozen boundary-walk
artifact records as changing across each gap's two hundredth
steps, computed mechanically from the frozen stored directions
and listed in the artifact, no hand selection performed over
them; at every finer head the two spans beside the head are the
window-mass span ending at the head and the window-mass span
starting at the head, each priced fresh through the same
mark-excluded block (the span's own matrix carries its own
mark's row and column excluded) and the same six summaries, no
pair dropped, no pair synthesized, so the two spans beside the
head share the head exactly and each span carries the same
declared mass; no band is loaded, no envelope is formed, no
verdict and no scalar margin is produced anywhere in this
artifact: the declared question is answered by direction, and
each span records, for each of the six scalar summaries it
shares with the whole profile, whether its value sits above,
below or equal to the whole sequence's value at the stored
6-decimal rounding, every entry recorded and no selection
performed over anything; the real's side is identical for both
languages of a file, so every cell prices the same fine-walk
records.

Mechanics, declared: the bridge gate first, per cell: the fresh
whole-sequence profile verified field for field against the
frozen real-at-basis ladder's anchor profile, the fresh window
mass verified against the frozen boundary-walk record, the 11
heads recomputed from the declared rule and verified one field
each, the two window sizes verified at every head one field
each, the four endpoint span profiles verified field for field
against the frozen boundary-walk instrument's stored profiles at
the gap's two hundredth steps, the two endpoint head positions
verified against the frozen stored head positions, and the
whole's own block-total identity verified, 42 fields per cell,
252 fields all told; any divergence aborts with nothing written.

Pre-run probes, disclosed verbatim, on frozen data through the
declared implementation before the artifact run. Probe 1, the
fine-walk gate rehearsed: 0 problems, 252 fields compared, the declared 42 per cell, no divergence in any of them.. Probe 2, the declared
heads and window sizes per file, printed in order at the first
and last heads with the head count: ZL gap j 470 to 480, window 54,604, 11 heads, first 102,655, last 104,839; GC gap j 430 to 440, window 45,800, 11 heads, first 78,776, last 80,608; IT gap j 480 to 490, window 55,133, 11 heads, first 105,855, last 108,060.. Probe 3,
the tracked flips per file as the mechanical rule computes them
from the frozen boundary-walk records: ZL 3 tracked flips: left self above to below, left top_50 above to below, right top_1 above to below; GC 1 tracked flip: left self above to below; IT 3 tracked flips: left self above to below, left top_50 above to below, right top_1 above to below.. Probe 4,
the declared confluence heads verified against the frozen
boundary-walk records per file: all four endpoint marks true in every file, ZL True/True/True/True, GC True/True/True/True, IT True/True/True/True.. Probe 5, the
first file's declared portraits ahead of the run:
the ZL whole row anchors them (kept 218,415 pairs, 68,616 whole boundary-carried pairs, 928 empty types, self 0.065848, top_1 0.070481, top_10 0.424435, top_50 0.893671, entropy 4.010179), and the 11 finer heads tell this story. The left span's self runs above for the first ten heads (0.067744 at the first head 102,655 down to 0.065864 at 104,621) and below at the last head (0.065626 at 104,839), so the tracked flip turns at the gap's last switch, between 104,621 and 104,839, rather than drifting across the gap. The left span's top_50 runs above at the first head (0.893832) and below at the remaining ten (0.893639 at 102,873 through 0.893005 at 104,839), so its tracked flip turns at the gap's first switch, between 102,655 and 102,873. The right span's top_1 runs above for the first ten heads (0.071656 at 102,655 through 0.070487 at 104,621) and below at the last head (0.070293 at 104,839), so its tracked flip lands between the same two heads that close the left self's run. The left span's top_1 runs above at all 11 heads (0.087480 at 102,655 and 0.089319 at 104,839), its top_10 above at all 11 and its entropy below at all 11; the right span's self runs below at all 11 heads, its top_10 below at all 11, its top_50 below at all 11 and its entropy above at all 11. No equal entry appears anywhere in the ZL fine walk's direction records, and the gap's three tracked flips turn at exactly two declared finer switches, the first switch and the last switch, none splitting and none drifting. Probe 6: none; the remaining files are unseen
until the declared run. The probes' disclosed portraits do not
decide the artifact: the artifact run prices every span beside
every finer head through the same declared code, and the
disclosure's honest question is recorded over all of them.

The standing limitations are inherited from the held-out screen:
no mapping is published anywhere in this artifact, no recovered
assignment is stored as a key, plaintext_recovered_percent stays
0, the reference prose is modern printed text outside the
manuscript's century, and nothing here is a reading or a
language claim.

Twentieth declared measurement, the switch walk instrument, declared
after the finer-resolution walk instrument walked the eleven declared
thousandth heads inside each located gap and read its seven tracked
flips' turns off the recorded direction tables - not one of its 792
direction entries records equal, and every tracked turn landed
between two consecutive declared thousandth heads, two flips turning
together across one band in ZL (the left self and the right top_1)
and again in IT (the left self and the left top_50), none splitting
and none drifting at that declared resolution - and before any run of
it beyond the probes it discloses.

The disclosed background, declared in advance: the finer-resolution
walk instrument re-walked the boundary-walk instrument's three
located gaps at the declared thousandth steps and recorded the
direction tables at every head. What that record leaves open is the
position inside each switch: the fine walk prices nothing between two
consecutive thousandth heads, so each flip's location is only as fine
as a thousandth of the stream, and the two files whose paired flips
share one switch band (ZL's left self and right top_1 across the
104,621 to 104,839 band, IT's left self and left top_50 across the
106,296 to 106,516 band) could turn apart at finer positions or
together. The honest next question is the switch walk: re-walk the
same declared head at declared finer steps across each of the five
located switch bands, price the two spans beside the head fresh at
every finer position, and record every position's direction tables,
so each tracked flip acquires a finer declared location: at which
finer position it turns, whether it turns once or splits into more
than one turn, whether the shared bands' paired flips stay together
or separate, or whether any of them drifts smoothly across the band.

The declared design, before the run: the corpus-breadth roster, the
state space (1296 ordered types, the boundary mark's row and column
excluded on both sides) and the six relabeling-invariant summaries
unchanged; more mass-matched cuts are refused: the window mass is
fixed at the standing basis arithmetic's first boundary (the
int(quarter x the anchor basis) positions, so the window mass is ZL
54,604, GC 45,800 and IT 55,133 kept-adjacent pairs) and the head is
walked at int(step x the anchor basis) positions for the declared
steps j / 10000 with j running over the five declared switch bands
exactly as the finer-resolution walk instrument located them: ZL j
4700 to 4710 inclusive and j 4790 to 4800 inclusive, GC j 4370 to
4380 inclusive, IT j 4820 to 4830 inclusive and j 4890 to 4900
inclusive, 11 heads per switch band, the first and last heads of
each band exactly the finer-resolution walk instrument's stored
heads at that band's two boundary thousandth steps (the declared
confluence, matched by head position and verified in the gate
against that instrument's frozen stored head records, no float step
equality asserted anywhere). The tracked flips are the side and
summary direction records the frozen finer-walk artifact records as
changing across each band's two boundary heads, computed
mechanically from the frozen stored directions and listed in the
artifact band by band, no hand selection performed over them; at
every finer head the two spans beside the head are the window-mass
span ending at the head and the window-mass span starting at the
head, each priced fresh through the same mark-excluded block (the
span's own matrix carries its own mark's row and column excluded)
and the same six summaries, no pair dropped, no pair synthesized, so
the two spans beside the head share the head exactly and each span
carries the same declared mass; no band is loaded, no envelope is
formed, no verdict and no scalar margin is produced anywhere in this
artifact: the declared question is answered by direction, and each
span records, for each of the six scalar summaries it shares with
the whole profile, whether its value sits above, below or equal to
the whole sequence's value at the stored 6-decimal rounding, every
entry recorded and no selection performed over anything; the real's
side is identical for both languages of a file, so every cell prices
the same switch-walk records.

Mechanics, declared: the bridge gate first, per cell: the fresh
whole-sequence profile verified field for field against the frozen
real-at-basis ladder's anchor profile, the fresh window mass
verified against the frozen finer-walk record, and the whole's own
block-total identity verified; then per switch band the 11 heads
recomputed from the declared rule and verified one field each, the
two window sizes verified at every head one field each, the four
endpoint span profiles verified field for field against the frozen
finer-walk instrument's stored profiles at the band's two boundary
steps, and the two endpoint head positions verified against the
frozen stored head positions by position: 81 fields per ZL or IT
cell (two switch bands), 42 fields per GC cell (one switch band),
408 fields all told; any divergence aborts with nothing written.

Pre-run probes, disclosed verbatim, on frozen data through the
declared implementation before the artifact run. Probe 1, the
switch-walk gate rehearsed: 0 problems, 408 fields compared, the
declared 81 per ZL or IT cell and 42 per GC cell, no divergence in
any of them. Probe 2, the declared
bands and window sizes per file, printed in order at the first and
last heads with the head count: ZL band j 4700 to 4710, window
54,604, 11 heads, first 102,655, last 102,873; ZL band j 4790 to
4800, window 54,604, 11 heads, first 104,621, last 104,839; GC band
j 4370 to 4380, window 45,800, 11 heads, first 80,058, last 80,241;
IT band j 4820 to 4830, window 55,133, 11 heads, first 106,296,
last 106,516; IT band j 4890 to 4900, window 55,133, 11 heads,
first 107,840, last 108,060. Probe 3,
the tracked flips per band as the mechanical rule computes them
from the frozen finer-walk records: ZL band j 4700 to 4710, 1
tracked flip: left top_50 above to below; ZL band j 4790 to 4800,
2 tracked flips: left self above to below and right top_1 above to
below; GC band j 4370 to 4380, 1 tracked flip: left self above to
below; IT band j 4820 to 4830, 2 tracked flips: left self above to
below and left top_50 above to below; IT band j 4890 to 4900, 1
tracked flip: right top_1 above to below. Probe 4,
the declared confluence heads verified against the frozen
finer-walk records per band: every band's endpoint positions and
span profiles all true in every file, ZL, GC and IT, and the six
fresh cells' direction records total 1,320 entries, none equal. Probe 5, the
first file's declared portraits ahead of the run:
the ZL whole row anchors them (kept 218,415 pairs, 68,616 whole
boundary-carried pairs, 928 empty types, self 0.065848, top_1
0.070481, top_10 0.424435, top_50 0.893671, entropy 4.010179), and
the two switch bands' 22 finer heads tell this story. In the first
band (j 4700 to 4710, heads 102,655 to 102,873) the left span's
top_50 runs above at the band's first ten heads (0.893832 at
102,655 through 0.893692 at 102,852) and below at the last
(0.893639 at 102,873), so its tracked flip turns once, between j
4709 and j 4710, at the band's closing step; the left span's self
holds above across the band (0.067744 at 102,655 through 0.067641
at 102,873), its top_1 above (0.087480 through 0.087618), its
top_10 above (0.437639 through 0.437663), its empties above at
1,015 at every step and its entropy below (3.991647 through
3.991904), while the right span's empties hold above at 1,004 at
every step, its self runs below (0.055391 through 0.055547), its
top_1 above (0.071656 through 0.071432), its top_10 below (0.389460
through 0.389445), its top_50 below (0.883967 through 0.883791) and
its entropy above (4.080312 through 4.080280). In the second band
(j 4790 to 4800, heads 104,621 to 104,839) the two tracked flips
separate: the right span's top_1 turns first, above only at the
band's first head (0.070487 at 104,621) and below at the remaining
heads (0.070460 at 104,643 through 0.070293 at 104,839), so it
turns between j 4790 and j 4791; the left span's self holds above
two heads (0.065864 at 104,621 and 0.065886 at 104,643) and turns
between j 4791 and j 4792, below from 0.065811 at 104,664 down to
0.065626 at 104,839, one declared ten-thousandth step behind the
right top_1; the left span's top_1 holds above across the band
(0.089100 at 104,621 through 0.089319 at 104,839), its top_10 above
(0.440394 through 0.440176), its top_50 below (0.893494 through
0.893005), its entropy below (3.990789 through 3.992262) and its
empties above (1,015 at the band's opening head and 1,016 at its
closing head), while the right span's empties hold above at 1,004
at every step, its self runs below (0.056443 through 0.056520), its
top_10 below (0.390153 through 0.390122), its top_50 below (0.883804
through 0.883948) and its entropy above (4.077394 through
4.076501). No equal entry appears anywhere in the ZL switch walk's
direction records: the gap's three tracked flips each turn once at
the finer steps, none splitting and none drifting, and the two
flips that shared the second band at the finer walk's thousandth
steps separate, the right top_1 turning one declared ten-thousandth
step before the left self. Probe 6: none; the remaining files are
unseen until the declared run. The probes' disclosed portraits do
not decide the artifact: the artifact run prices every span beside
every finer head through the same declared code, and the
disclosure's honest question is recorded over all of them.

The standing limitations are inherited from the held-out screen: no
mapping is published anywhere in this artifact, no recovered
assignment is stored as a key, plaintext_recovered_percent stays 0,
the reference prose is modern printed text outside the manuscript's
century, and nothing here is a reading or a language claim.
"""

from __future__ import annotations

import hashlib
import re

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
           "homo_cross_enc": 28, "homo_cross_mach": 29,
           "homo_cut_geom": 30}

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


# --------------------------------------------------------------------------
# The block-fold split, the family's fifth declared measurement
# --------------------------------------------------------------------------


BLOCK_ARTIFACT_PATH = (
    Path(DATA_DIR).resolve().parent.parent.parent
    / "docs" / "research-notes" / "voynich-homophonic-block-fold.json"
)


def _block_pairs(
    first: np.ndarray, second: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """The declared block-fold split of a stream's counted pairs: the
    pairs kept in stream order split into contiguous blocks at the
    midpoint, the first floor(N/2) pairs the climb half the machinery
    may search and the remaining pairs the score half it may never
    touch; for an odd count the climb half takes the smaller first
    block. The halves share no counted pair, no pair of the climb half
    lies in the scored block's index range, and the scored pairs are
    fresh to the search in the span sense, not only the pair sense."""
    mid = len(first) // 2
    return first[:mid], second[:mid], first[mid:], second[mid:]


def _block_identity_half_means(
    truncated: list[int],
    table: np.ndarray,
    split_pairs=_block_pairs,
) -> tuple[float, float, int, int]:
    """The truncated plaintext stream's identity means under the
    declared table and the declared split, per half: the climb-half
    mean (the machinery's own view of its true configuration), the
    score-half mean (the true configuration's held-out anchor), and
    both half sizes, the held-out screen's identity halves with the
    split supplied instead of the parity rule."""
    ids = np.asarray(truncated, dtype=np.int64)
    first, second = ids[:-1], ids[1:]
    first_c, second_c, first_s, second_s = split_pairs(first, second)
    climb_pairs = len(first_c)
    score_pairs = len(first_s)
    climb_mean = float(table[first_c, second_c].sum()) / climb_pairs
    held_mean = float(table[first_s, second_s].sum()) / score_pairs
    return held_mean, climb_mean, climb_pairs, score_pairs


def _block_cell_facts(
    code: str, language: str,
    table: np.ndarray, letter_counts: np.ndarray,
    split_pairs=_block_pairs,
    reference_file: str | None = None,
) -> dict:
    """Real, plants with their held-out anchor, and floors for one
    cell, each under the declared split, the exact reassignment climb
    on the climb half and the exact pricing on the score half, with
    the exact full-data side call recorded beside each score: the
    shape measurement's cell facts with the split supplied instead of
    the parity rule. The reference_file parameter supplies a declared
    reference text outside the standing reference as the source of the
    anchor and the plants, None meaning the standing reference and
    every earlier caller unchanged."""
    real_stream = _homo_real_stream(code)
    first, second = _kept_pairs(
        real_stream["event_ids"], real_stream["kept_mask"]
    )
    climb_first, climb_second, score_first, score_second = (
        split_pairs(first, second)
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
    truncated = _truncated_reference(code, language, file=reference_file)
    anchor, anchor_climb, _climb_half, _score_half = (
        _block_identity_half_means(truncated, table, split_pairs)
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
            split_pairs(plant_first, plant_second)
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
            split_pairs(floor_first, floor_second)
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


def _block_band_for(
    code: str, language: str, seed_index: int,
    table: np.ndarray, letter_counts: np.ndarray,
    split_pairs=_block_pairs,
    members: list[tuple[str, int]] | None = None,
) -> dict:
    """Five encodings of one class-member text under the first
    screen's per-text sequential scheme, each scored by the held-out
    machinery under the declared split and by the exact full-data side
    call, with the member's held-out anchor, climb-half identity, the
    selected draw's index and the member's band value, plus the
    member's five climb-half totals at full precision: the shape
    measurement's band facts with the split and the member list
    supplied instead of the parity rule (the standing list by
    default)."""
    if members is None:
        members = (
            [CROSS_REFERENCE_FILES[language]]
            + list(WIDENED_REFERENCE_FILES[language])
        )
    name, ebook = members[seed_index]
    truncated = _truncated_reference(code, language, file=name)
    anchor, anchor_climb, _climb_half, _score_half = (
        _block_identity_half_means(truncated, table, split_pairs)
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
            split_pairs(enc_first, enc_second)
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


def _compare_block_to_shape() -> tuple[list[str], int]:
    """The declared bridge gate: the block instrument's full first cell
    (ZL english: the real, its five plants, its five floors and its
    three band members) computed through this measurement's code under
    the inherited pair-index-parity split must equal the shape
    measurement's own outputs field for field, so this artifact's only
    difference from the frozen shape measurement is the split. Any
    divergence aborts with nothing written."""
    problems: list[str] = []
    fields = 0
    code, language = "ZL", "english"
    model = _shape_table(language)
    shape_facts = _shape_cell_facts(
        code, language, model["table"], model["letter_counts"]
    )
    block_facts = _block_cell_facts(
        code, language, model["table"], model["letter_counts"],
        split_pairs=_split_pairs,
    )
    for key, value in shape_facts.items():
        fields += 1
        if block_facts[key] != value:
            problems.append(
                f"cell/{key}: shape {value!r} vs block {block_facts[key]!r}"
            )
    for seed_index in (0, 1, 2):
        shape_member = _shape_band_for(
            code, language, seed_index,
            model["table"], model["letter_counts"],
        )
        block_member = _block_band_for(
            code, language, seed_index,
            model["table"], model["letter_counts"],
            split_pairs=_split_pairs,
        )
        for key, value in shape_member.items():
            fields += 1
            if block_member[key] != value:
                problems.append(
                    f"band/{seed_index}/{key}: shape {value!r} vs block "
                    f"{block_member[key]!r}"
                )
    return problems, fields


def substitution_homophonic_block_fold() -> dict:
    """The declared block-fold split: the shape measurement's six
    (file, language) cells, plants, floors and band re-measured at the
    top budget under the leave-one-out table with every stream, seed
    kind and machinery rule unchanged and the declared split replaced
    by the contiguous block fold, after the bridge gate proves this
    measurement's code reproduces the shape measurement field for
    field under the parity split."""
    problems, fields = _compare_block_to_shape()
    if problems:
        raise RuntimeError(
            "the bridge gate failed: " + "; ".join(problems[:12])
        )
    artifact: dict = {
        "what": "The declared block-fold split: the shape measurement's "
        "six (file, language) cells re-measured with the mapped set, "
        "streams, seeds, machinery, restarts, sweep cap, plants, floors "
        "and band unchanged, the leave-one-out table carried forward, "
        "and the declared split replaced by the contiguous block fold, "
        "so the score half is fresh to the search in the span sense and "
        "not only the pair sense. The bridge gate re-derived the shape "
        "measurement under the parity split through this measurement's "
        "code before the block cells ran. The declared truthful "
        "question: does the real's held-out score-half value still "
        "stand above the band when the scored pairs are fresh to the "
        "search in the span sense - a yes extends the separation beyond "
        "the parity geometry, a no records that the margin was carried "
        "by the parity geometry's interleaving. No mapping is "
        "published; nothing here is a reading.",
        "declared": {
            "base_seed": BASE_SEED,
            "mapped": MAPPED_HOMO,
            "restarts": N_RESTARTS,
            "sweep_cap": SWEEP_CAP,
            "plants_per_cell": N_PLANTS,
            "floors": N_FLOORS,
            "split_rule": "the counted pairs of each side, in stream "
            "order, split into contiguous blocks at the midpoint: the "
            "first floor(N/2) pairs the climb half the machinery may "
            "search, the remaining pairs the score half it may never "
            "touch; for an odd count the climb half takes the smaller "
            "first block; the halves share no counted pair and every "
            "identity anchor's halves fold by the same rule; "
            "deterministic, consuming no seed",
            "loo_rule": "the shape measurement's leave-one-out table "
            "carried forward unchanged: the inherited add-one form is "
            "log((n_ab + 1) / (N + 729)) with N the reference stream's "
            "total counted pairs; every pair type (a, b) present in the "
            "reference pair table is scored with one occurrence of "
            "(a, b) removed from the reference counts, "
            "log(n_ab / (N + 728)), and a type with no counted "
            "occurrence keeps the inherited add-one entry "
            "log(1 / (N + 729)); the letter marginals and rank "
            "initialisation unchanged, the matrix arithmetic needing "
            "no re-derivation as the shape measurement declared",
            "measured_facts_rule": "the mapped set, streams, seeds, "
            "machinery, restarts, sweep cap, plants, floors and band "
            "are the held-out screen's and shape measurement's "
            "declarations replayed unchanged; the encodings and "
            "shuffles are byte-identical replays of the frozen "
            "measurement's draws and only the split changes; each "
            "side's exact full-data side call is recorded beside its "
            "held-out value for attribution only",
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
            "bridge_gate": "before the block-fold cells run, the "
            "block instrument's full first cell (ZL english: the "
            "real, its five plants, its five floors and its three "
            "band members) is computed through this measurement's "
            "code under the inherited pair-index-parity split and "
            "compared field for field against the shape "
            "measurement's own outputs; any divergence aborts with "
            "nothing written",
            "band_record_rule": "membership, selection, ties and "
            "spreads are declared unchanged from the held-out screen "
            "(a member's band value the held-out value of the draw "
            "whose exact climb-half total is best, strict beyond "
            "1e-12, ties to the first draw); each member records "
            "draws_climb_exact, its five climb-half totals at full "
            "precision, so the declared selection is re-derivable "
            "from the stored artifact",
            "verdict_rule": "unchanged from the held-out screen and "
            "applied to the block-fold-scale numbers: the real "
            "held-out at or above the smallest member band value is "
            "consistent-with-substitution, at or below the largest "
            "floor's held-out value is not-consistent, strictly "
            "between is below-held-band; the strings describe "
            "consistency under this artifact's declared split and do "
            "not restate the parity split's verdicts",
            "margin_rule": "the margin is computed from the stored "
            "rounded values: the real held-out mean minus the "
            "smallest member band value, rounded to four decimals",
            "exclusion_rule": "the family's declared exclusion format "
            "is not re-scoped by this artifact: it keys to the "
            "declared 36-slot class under the inherited add-one form "
            "exactly as the held-out screen declared it, so a "
            "block-fold verdict is split-geometry evidence and the "
            "shape measurement's verdicts stand untouched by this "
            "artifact's numbers",
            "truthful_question": "declared in advance: does the "
            "real's held-out score-half value still stand above the "
            "band when the scored pairs are fresh to the search in "
            "the span sense, not only the pair sense - a yes extends "
            "the separation beyond the parity geometry, a no records "
            "that the margin was carried by the parity geometry's "
            "interleaving",
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
        full_matrix = _stream_matrix_27(stream)
        block_held, block_climb, _bcp, _bsp = _block_identity_half_means(
            stream, table
        )
        add_one_held, _acm, _acp, _asp = _identity_half_means(
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
            "block_climb_half_mean_nats_per_pair": round(block_climb, 4),
            "block_score_half_mean_nats_per_pair": round(block_held, 4),
            "add_one_parity_score_half_mean_nats_per_pair": round(
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
            facts = _block_cell_facts(
                code, language, model["table"], model["letter_counts"]
            )
            members = []
            if language == "english":
                positions = (0, 1, 2)
            else:
                positions = (0, 1, 2, 3)
            for seed_index in positions:
                members.append(
                    _block_band_for(
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


def main_block_fold() -> None:
    artifact = substitution_homophonic_block_fold()
    BLOCK_ARTIFACT_PATH.write_text(json.dumps(artifact, indent=2) + "\n")
    print(BLOCK_ARTIFACT_PATH)


# --------------------------------------------------------------------------
# Measurement 6: the widened band population
# --------------------------------------------------------------------------

WIDENED_BAND_ARTIFACT_PATH = (
    Path(DATA_DIR).resolve().parent.parent.parent
    / "docs" / "research-notes" / "voynich-homophonic-widened-band.json"
)

EXTENDED_WIDENED_REFERENCE_FILES: dict[str, list[tuple[str, int, str]]] = {
    "english": [
        ("substref_english5_pg174.txt", 174, "The Picture of Dorian Gray (Wilde)"),
        ("substref_english6_pg1400.txt", 1400, "Great Expectations (Dickens)"),
        ("substref_english7_pg120.txt", 120, "Treasure Island (Stevenson)"),
        ("substref_english8_pg158.txt", 158, "Emma (Austen)"),
    ],
    "latin": [
        ("substref_latin6_pg23306.txt", 23306, "Meditationes de prima philosophia (Descartes)"),
        ("substref_latin7_pg28233.txt", 28233, "Philosophiae Naturalis Principia Mathematica (Newton)"),
        ("substref_latin8_pg826.txt", 826, "Vulgata Esther"),
        ("substref_latin9_pg58528.txt", 58528, "Evagatorium volumen primum (Fabri)"),
    ],
}

REJECTED_EXTENDED_CANDIDATES: list[dict] = [
    {"ebook": 47001, "label": "De Officiis (Cicero)",
     "cause": "an english translation interleaved through the marker "
     "span (6,686 english common-word hits; mid-span in english: "
     "\"they fall into the other: they are traitors to social "
     "life\")"},
    {"ebook": 7402, "label": "De Bello Catilinario et Jugurthino (Sallust)",
     "cause": "the translator's glosses inline through the span "
     "(4,056 hits: \"That is, in the year B.C. 64, or 690 after the "
     "building of the city.\", \"_Necessitudo_, 'a close "
     "connection' or 'friendship'\")"},
    {"ebook": 21827, "label": "Institutionis oratoriae liber decimus (Quintilian)",
     "cause": "an english introduction and school notes dominate the "
     "span (10,826 hits; mid-span english prose)"},
    {"ebook": 13316, "label": "Theological Tractates and Consolation of Philosophy (Boethius)",
     "cause": "a bilingual Loeb edition: the english translation "
     "interleaved with the latin through the span (5,087 hits; "
     "mid-span in english)"},
    {"ebook": 54243, "label": "Demoniality (Sinistrari)",
     "cause": "an english translation interleaved with the latin "
     "through the span (3,277 hits; mid-span in english)"},
    {"ebook": 51812, "label": "De architectura libri decem (Vitruvius)",
     "cause": "collation apparatus interleaved through the text: "
     "manuscript sigla and subscript editorial readings inside the "
     "verses (\"sub(p _S^{c} G^{c}_)ponentur _GS_: suppona(e "
     "_H^{c}_)ntur _H_\", \"(_ubi in m. G^{c}_\")"},
    {"ebook": 69275, "label": "Haririus latinus (Hariri)",
     "cause": "the translator's english bibliographic apparatus runs "
     "beyond the standing transcriber-note scale (109 common-word "
     "hits against the standing members' 0 to 52, 104 of them in a "
     "trailing english critical-notes block: \"vert. Ouseley, p. "
     "157 dicit: Maragha is nearly of the same size as "
     "Ardebil\")"},
    {"ebook": 19635, "label": "Biblia Sacra Vulgata - Psalmi XXII",
     "cause": "not accessible at the declared fetch source: the cache "
     "returned the 404 page for this ebook (6,559 bytes)"},
]

_CELL_FIELD_MAP: dict[str, str] = {
    "real_held": "real_held_mean_nats",
    "real_climb": "real_climb_mean_nats",
    "real_hit": "real_sweep_budget_hit",
    "real_full": "real_full_exact_mean_nats",
    "real_full_hit": "real_full_sweep_budget_hit",
    "counted": "counted_pairs",
    "climb_pairs": "climb_pairs",
    "score_pairs": "score_pairs",
    "anchor": "plant_parity_anchor_mean_nats",
    "anchor_climb": "plant_climb_identity_mean_nats",
    "plants_held": "self_plants_held_mean_nats",
    "plants_full": "self_plants_full_exact_mean_nats",
    "plants_hits": "self_plants_sweep_budget_hits",
    "plants_full_hits": "self_plants_full_sweep_budget_hits",
    "floors_held": "floors_held_mean_nats",
    "floors_full": "floors_full_exact_mean_nats",
    "floors_hits": "floors_sweep_budget_hits",
    "floors_full_hits": "floors_full_sweep_budget_hits",
}


def _extended_reference_members(language: str) -> list[tuple[str, int]]:
    """The widened band's member texts, the standing list first."""
    standing = (
        [CROSS_REFERENCE_FILES[language]]
        + list(WIDENED_REFERENCE_FILES[language])
    )
    return (
        [entry[:2] for entry in standing]
        + [entry[:2] for entry in EXTENDED_WIDENED_REFERENCE_FILES[language]]
    )


def _extended_band_positions(language: str) -> tuple[int, ...]:
    """The extended member list's positions."""
    return tuple(range(len(_extended_reference_members(language))))


def _compare_widened_to_block() -> tuple[list[str], int]:
    """The declared bridge gate: the widened instrument's full first
    cell (ZL english: the real, its five plants, its five floors and
    its three standing band members) computed through this
    measurement's code with the extended member list supplied must
    equal the frozen block-fold artifact's own first cell field for
    field, so the only difference from the frozen block measurement is
    the band's population. Any divergence aborts with nothing
    written."""
    problems: list[str] = []
    fields = 0
    code, language = "ZL", "english"
    frozen = json.loads(BLOCK_ARTIFACT_PATH.read_text())
    stored = frozen["files"][code][language]
    model = _shape_table(language)
    facts = _block_cell_facts(
        code, language, model["table"], model["letter_counts"]
    )
    for key, value in facts.items():
        fields += 1
        if stored[_CELL_FIELD_MAP[key]] != value:
            problems.append(
                f"cell/{key}: stored {stored[_CELL_FIELD_MAP[key]]!r} vs "
                f"fresh {value!r}"
            )
    members = _extended_reference_members(language)
    for seed_index in (0, 1, 2):
        fresh = _block_band_for(
            code, language, seed_index,
            model["table"], model["letter_counts"], members=members,
        )
        stored_member = stored["band"][seed_index]
        for key, value in fresh.items():
            fields += 1
            if stored_member[key] != value:
                problems.append(
                    f"band/{seed_index}/{key}: stored {stored_member[key]!r} "
                    f"vs fresh {value!r}"
                )
    return problems, fields


def substitution_homophonic_widened_band() -> dict:
    """The declared widened band population: the block-fold
    measurement's six (file, language) cells with their real, plants,
    floors, split, leave-one-out table and standing machinery replayed
    unchanged, and each cell's band extended with the declared widened
    members, re-measured at the top budget after the bridge gate proves
    this measurement's code reproduces the frozen block-fold artifact's
    first cell field for field through the extended member list."""
    problems, fields = _compare_widened_to_block()
    if problems:
        raise RuntimeError(
            "the bridge gate failed: " + "; ".join(problems[:12])
        )
    artifact: dict = {
        "what": "The declared widened band population: the block-fold "
        "measurement's six (file, language) cells re-measured with the "
        "mapped set, streams, seeds, machinery, restarts, sweep cap, "
        "plants, floors, block-fold split and leave-one-out table "
        "carried forward unchanged, and each cell's band extended with "
        "the declared widened members, so the real is priced above a "
        "band of seven members per english cell and eight per latin "
        "cell. The bridge gate re-derived the frozen block-fold "
        "artifact's first cell through the extended member list before "
        "the widened cells ran. The declared truthful question: does "
        "the real's held-out score-half value still stand above the "
        "band as the band's population grows. No mapping is published; "
        "nothing here is a reading.",
        "declared": {
            "base_seed": BASE_SEED,
            "mapped": MAPPED_HOMO,
            "restarts": N_RESTARTS,
            "sweep_cap": SWEEP_CAP,
            "plants_per_cell": N_PLANTS,
            "floors": N_FLOORS,
            "band_positions": {
                language: len(_extended_reference_members(language))
                for language in LANGS
            },
            "split_rule": "the counted pairs of each side, in stream "
            "order, split into contiguous blocks at the midpoint: the "
            "first floor(N/2) pairs the climb half the machinery may "
            "search, the remaining pairs the score half it may never "
            "touch; for an odd count the climb half takes the smaller "
            "first block; the halves share no counted pair and every "
            "identity anchor's halves fold by the same rule; "
            "deterministic, consuming no seed",
            "loo_rule": "the shape measurement's leave-one-out table "
            "carried forward unchanged: the inherited add-one form is "
            "log((n_ab + 1) / (N + 729)) with N the reference stream's "
            "total counted pairs; every pair type (a, b) present in the "
            "reference pair table is scored with one occurrence of "
            "(a, b) removed from the reference counts, "
            "log(n_ab / (N + 728)), and a type with no counted "
            "occurrence keeps the inherited add-one entry "
            "log(1 / (N + 729)); the letter marginals and rank "
            "initialisation unchanged, the matrix arithmetic needing "
            "no re-derivation as the shape measurement declared",
            "measured_facts_rule": "the mapped set, streams, seeds, "
            "machinery, restarts, sweep cap, plants, floors and split "
            "are the held-out screen's and block-fold measurement's "
            "declarations carried unchanged; the real, plants, floors "
            "and standing band members are byte-identical replays of "
            "the frozen block-fold artifact's declared draws and only "
            "the band's population changes; each member records "
            "draws_climb_exact, its five climb-half totals at full "
            "precision; each side's exact full-data side call is "
            "recorded beside its held-out value for attribution only",
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
            "seed_sharing": "no new seed kinds are consumed: the "
            "real, plants, floors and standing members replay the "
            "block-fold measurement's declared draws from the declared "
            "kinds at the declared positions, and the widened members "
            "consume the declared cross kinds at seed positions beyond "
            "every earlier measurement's declared positions (english "
            "3 to 6, latin 4 to 7), consuming none of any other "
            "module's declared draws",
            "bridge_gate": "before the widened cells run, the widened "
            "instrument's full first cell (ZL english: the real, its "
            "five plants, its five floors and its three standing band "
            "members) is computed through this measurement's code with "
            "the extended member list supplied and compared field for "
            "field against the frozen block-fold artifact's own first "
            "cell; any divergence aborts with nothing written",
            "corpus_source_rule": "the widened members are fetched "
            "from the standing members' declared source in the same "
            "plain text form; the fetch was first verified "
            "byte-identical by refetching the standing english2 file "
            "and matching its recorded sha256, and each widened "
            "member's file is stored raw under engine/data with its "
            "Gutenberg markers and processed by the standing declared "
            "processing (the body extracted between the markers, the "
            "ligatures joined, NFD plus casefold, letters to 0 to 25 "
            "and non-letter runs to the single boundary token), with "
            "the sha256 recorded below",
            "corpus_rule": "widened members are modern printed prose "
            "under the declared corpus rules: marker spans keeping "
            "only transcriber-note scale english scaffolding (the "
            "standing members' scale is 0 to 52 english common-word "
            "hits), with candidates whose span interleaves english "
            "translations, glossed school notes or collation "
            "apparatus through the body, or whose english scaffolding "
            "runs beyond that standing scale, rejected with cause as "
            "family 4 rejected its school editions and glossed "
            "readers",
            "rejected_candidates": REJECTED_EXTENDED_CANDIDATES,
            "band_record_rule": "membership, selection, ties and "
            "spreads are declared unchanged from the held-out screen "
            "(a member's band value the held-out value of the draw "
            "whose exact climb-half total is best, strict beyond "
            "1e-12, ties to the first draw); each member records "
            "draws_climb_exact, its five climb-half totals at full "
            "precision, so the declared selection is re-derivable "
            "from the stored artifact; extended membership "
            "unconditional: every widened member enters the band "
            "unconditionally and no convergence criterion is applied "
            "to any member",
            "verdict_rule": "unchanged from the held-out screen and "
            "applied to the block-fold-scale numbers: the real "
            "held-out at or above the smallest member band value is "
            "consistent-with-substitution, at or below the largest "
            "floor's held-out value is not-consistent, strictly "
            "between is below-held-band; the strings describe "
            "consistency under this artifact's declared split and do "
            "not restate the parity split's verdicts",
            "margin_rule": "the margin is computed from the stored "
            "rounded values: the real held-out mean minus the "
            "smallest member band value, rounded to four decimals",
            "exclusion_rule": "the family's declared exclusion format "
            "is not re-scoped by this artifact: it keys to the "
            "declared 36-slot class under the inherited add-one form "
            "exactly as the held-out screen declared it, so a "
            "widened-band verdict is corpus-breadth evidence and the "
            "block-fold measurement's verdicts stand untouched by "
            "this artifact's numbers",
            "truthful_question": "declared in advance: does the "
            "real's held-out score-half value still stand above the "
            "band as the band's population grows beyond the standing "
            "members - a yes extends the separation across the corpus "
            "breadth, a no records that the margin rode the band's "
            "small population",
            "corpus_facts": {},
            "models": {},
        },
        "bridge_gate": {},
        "files": {},
    }
    for language in LANGS:
        stream = _reference_stream(language)
        model = _shape_table(language)
        table = model["table"]
        full_matrix = _stream_matrix_27(stream)
        block_held, block_climb, _bcp, _bsp = _block_identity_half_means(
            stream, table
        )
        add_one_held, _acm, _acp, _asp = _identity_half_means(
            stream, model["add_one_table"]
        )
        artifact["declared"]["models"][language] = {
            "file": REFERENCE_FILES[language][0],
            "ebook": REFERENCE_FILES[language][1],
            "clean_identity_mean_nats_per_pair": round(
                float((full_matrix * table).sum())
                / float(full_matrix.sum()),
                4,
            ),
            "block_climb_half_mean_nats_per_pair": round(block_climb, 4),
            "block_score_half_mean_nats_per_pair": round(block_held, 4),
            "add_one_parity_score_half_mean_nats_per_pair": round(
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
    for language in LANGS:
        roster = []
        for name, ebook, label in (
            EXTENDED_WIDENED_REFERENCE_FILES[language]
        ):
            path = Path(DATA_DIR).resolve().parent / name
            raw = path.read_bytes()
            text = raw.decode("utf-8", "replace")
            start = text.find("START OF THE PROJECT GUTENBERG")
            end = text.find("END OF THE PROJECT GUTENBERG")
            body = text[text.find("\n", start):end]
            if language == "latin":
                # the apparatus probe is defined on latin spans; english
                # members are modern english prose and carry no foreign
                # apparatus category
                hits: int | None = len(
                    re.findall(r"\b(the|and|with|from)\b", body)
                )
            else:
                hits = None
            members_stream = _reference_stream(language, file=name)
            letter_tokens = sum(
                members_stream.count(i) for i in range(26)
            )
            roster.append({
                "file": name,
                "ebook": ebook,
                "label": label,
                "sha256": hashlib.sha256(raw).hexdigest(),
                "file_bytes": len(raw),
                "body_bytes": len(body),
                "stream_length": len(members_stream),
                "letter_tokens": letter_tokens,
                "boundary_tokens": len(members_stream) - letter_tokens,
                "types_present": len(set(members_stream)),
                "english_scaffold_hits": hits,
            })
        artifact["declared"]["corpus_facts"][language] = roster
    for code in FILES:
        cell: dict = {}
        for language in LANGS:
            model = _shape_table(language)
            facts = _block_cell_facts(
                code, language, model["table"], model["letter_counts"]
            )
            positions = _extended_band_positions(language)
            members = [
                _block_band_for(
                    code, language, seed_index,
                    model["table"], model["letter_counts"],
                    members=_extended_reference_members(language),
                )
                for seed_index in positions
            ]
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


def main_widened_band() -> None:
    artifact = substitution_homophonic_widened_band()
    WIDENED_BAND_ARTIFACT_PATH.write_text(
        json.dumps(artifact, indent=2) + "\n"
    )
    print(WIDENED_BAND_ARTIFACT_PATH)


# --------------------------------------------------------------------------
# The alternate reference measurement, the seventh declared measurement
# --------------------------------------------------------------------------


ALTERNATE_ARTIFACT_PATH = (
    Path(DATA_DIR).resolve().parent.parent.parent
    / "docs" / "research-notes" / "voynich-homophonic-alternate-reference.json"
)

ALTERNATE_REFERENCE_FILES: dict[str, tuple[str, int, str]] = {
    "english": (
        "substref_english9_pg76.txt", 76,
        "Adventures of Huckleberry Finn (Twain)",
    ),
    "latin": (
        "substref_latin10_pg60772.txt", 60772,
        "Evagatorium volumen secundum (Fabri)",
    ),
}

REJECTED_ALTERNATE_CANDIDATES: list[dict] = [
    {"ebook": 9090, "label": "Germania and Agricola (Tacitus)",
     "cause": "english school commentary interleaved through the span "
     "(5,109 english common-word hits in every decile; mid-span in "
     "english: \"But _referantur_ is the reading of all the MSS., "
     "and needs no emendation\")"},
    {"ebook": 66595, "label": "Monumentum Ancyranum: The Deeds of "
     "Augustus",
     "cause": "the editor's english bibliographic apparatus runs "
     "through the span (2,813 english common-word hits in every "
     "decile; mid-span a bibliography list: \"enal, Decimus Junius "
     "(Juv.)=: _Satirae (Sat.)_. =Livius, Titus (Livy)=: "
     "_Annales_;\")"},
    {"ebook": 16400, "label": "De M. Terenti Varronis Libris "
     "Grammaticis (Varro)",
     "cause": "a mid-span transcriber note in english discloses the "
     "fragment fabric interleaved with the text: \"Most fragments "
     "have three elements: --original text, shown with line numbers; "
     "--commentary and testimonia, indented in the same way as "
     "footnotes; --critical apparatus keyed to line numbers in the "
     "text\" (24 english hits against the accepted members' zero "
     "mid-span english, 8 of them at sixth-decile notes of this "
     "kind)"},
]

PROBED_NOT_SELECTED_ALTERNATES: list[dict] = [
    {"ebook": 345, "label": "Dracula (Stoker)",
     "cause": "probed clean under the declared processing (body "
     "861,410 bytes, stream 806,705 tokens, all 27 types) and not "
     "selected: the declared design freezes one alternate reference "
     "per language and the english alternate declared this "
     "measurement is pg76"},
    {"ebook": 20771, "label": "Species Plantarum, Sections I-III "
     "(Linnaeus)",
     "cause": "probed inside the standing english scaffold scale (49 "
     "hits: 14 in a head sidenote-format transcriber block, 35 in a "
     "trailing english essay: \"Most of their citations would today "
     "be listed as \"personal communication\".\") and not selected on "
     "form: the body is terse nominal taxonomic description rather "
     "than connected prose, with Linnaeus's own inline citations "
     "(\"_T. Scheuchz. gram. 354._\") through the descriptions, and "
     "the declared latin alternate bar wants latin prose"},
]

_ALTERNATE_MODELS: dict[str, dict] = {}


def _alternate_table(language: str) -> dict:
    """The declared leave-one-out form of the alternate reference's
    bigram table: the shape measurement's leave-one-out form built
    from the declared alternate reference's stream instead of the
    standing reference's, with the same inherited add-one backing
    table and the alternate's letter marginals for the rank
    initialisation."""
    if language in _ALTERNATE_MODELS:
        return _ALTERNATE_MODELS[language]
    name, _ebook, _label = ALTERNATE_REFERENCE_FILES[language]
    stream = _reference_stream(language, file=name)
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
    _ALTERNATE_MODELS[language] = model
    return model


def _compare_alternate_to_widened() -> tuple[list[str], int]:
    """The declared bridge gate: the alternate instrument's full first
    cell (ZL english: the real, its five plants, its five floors and
    all seven widened band members) computed through this
    measurement's code with the standing reference supplied must equal
    the frozen widened-band artifact's own first cell field for
    field, so the only difference from the frozen widened measurement
    is the scored reference. Any divergence aborts with nothing
    written."""
    problems: list[str] = []
    fields = 0
    code, language = "ZL", "english"
    frozen = json.loads(WIDENED_BAND_ARTIFACT_PATH.read_text())
    stored = frozen["files"][code][language]
    model = _shape_table(language)
    facts = _block_cell_facts(
        code, language, model["table"], model["letter_counts"]
    )
    for key, value in facts.items():
        fields += 1
        if stored[_CELL_FIELD_MAP[key]] != value:
            problems.append(
                f"cell/{key}: stored {stored[_CELL_FIELD_MAP[key]]!r} vs "
                f"fresh {value!r}"
            )
    members = _extended_reference_members(language)
    for seed_index in _extended_band_positions(language):
        fresh = _block_band_for(
            code, language, seed_index,
            model["table"], model["letter_counts"], members=members,
        )
        stored_member = stored["band"][seed_index]
        for key, value in fresh.items():
            fields += 1
            if stored_member[key] != value:
                problems.append(
                    f"band/{seed_index}/{key}: stored "
                    f"{stored_member[key]!r} vs fresh {value!r}"
                )
    return problems, fields


def substitution_homophonic_alternate_reference() -> dict:
    """The declared alternate reference corpora: the widened band
    measurement's six (file, language) cells with their real, plants,
    floors, split, band population, seeds and machinery replayed
    unchanged, re-scored under leave-one-out tables rebuilt from
    single alternate references declared outside the band, one per
    language, after the bridge gate proves this measurement's code
    reproduces the frozen widened-band artifact's first cell field
    for field through the standing reference."""
    problems, fields = _compare_alternate_to_widened()
    if problems:
        raise RuntimeError(
            "the bridge gate failed: " + "; ".join(problems[:12])
        )
    artifact: dict = {
        "what": "The declared alternate reference corpora: the "
        "widened band measurement's six (file, language) cells "
        "re-scored with the mapped set, streams, seeds, machinery, "
        "restarts, sweep cap, plants, floors, block-fold split and "
        "band population carried forward unchanged and every scored "
        "table rebuilt from single declared alternate references "
        "outside the band (english pg76 Twain, latin pg60772 Fabri "
        "volumen secundum), so the real is priced against the same "
        "band under a reference scope no longer the standing "
        "references' single choice. The bridge gate re-derived the "
        "frozen widened-band artifact's first cell through the "
        "standing reference before the alternate cells ran. The "
        "declared truthful question: does the real's held-out "
        "score-half value still stand above the band when the "
        "scored tables are rebuilt from the alternate references. "
        "No mapping is published; nothing here is a reading.",
        "declared": {
            "base_seed": BASE_SEED,
            "mapped": MAPPED_HOMO,
            "restarts": N_RESTARTS,
            "sweep_cap": SWEEP_CAP,
            "plants_per_cell": N_PLANTS,
            "floors": N_FLOORS,
            "band_positions": {
                language: len(_extended_reference_members(language))
                for language in LANGS
            },
            "split_rule": "the counted pairs of each side, in stream "
            "order, split into contiguous blocks at the midpoint: the "
            "first floor(N/2) pairs the climb half the machinery may "
            "search, the remaining pairs the score half it may never "
            "touch; for an odd count the climb half takes the smaller "
            "first block; the halves share no counted pair and every "
            "identity anchor's halves fold by the same rule; "
            "deterministic, consuming no seed",
            "loo_rule": "the shape measurement's leave-one-out form "
            "carried exactly onto the declared alternate reference's "
            "counts: the inherited add-one backing form is "
            "log((n_ab + 1) / (N + 729)) with N the declared "
            "alternate reference stream's total counted pairs; every "
            "pair type (a, b) present in the alternate reference "
            "pair table is scored with one occurrence of (a, b) "
            "removed from the alternate reference counts, "
            "log(n_ab / (N + 728)), and a type with no counted "
            "occurrence keeps the inherited add-one entry "
            "log(1 / (N + 729)); the letter marginals are the "
            "alternate reference's unigram counts and the rank "
            "initialisation mechanics unchanged, the matrix "
            "arithmetic needing no re-derivation as the shape "
            "measurement declared",
            "measured_facts_rule": "the mapped set, streams, seeds, "
            "machinery, restarts, sweep cap, floors, split and band "
            "population are the held-out screen's, block-fold "
            "measurement's and widened band's declarations carried "
            "unchanged; the real, the floors and every band member's "
            "encodings are byte-identical replays of the frozen "
            "artifacts' declared draws, and each cell's five plants "
            "are encodings of the declared alternate reference text "
            "truncated to the same declared length, from the "
            "declared plant kinds at the declared positions; only "
            "the scored tables change: every machinery call prices "
            "its matrices under the declared alternate reference's "
            "leave-one-out table with the alternate's letter "
            "marginals for the rank initialisation; each side's "
            "exact full-data side call is recorded beside its "
            "held-out value for attribution only",
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
            "seed_sharing": "no new seed kinds are consumed: the "
            "real, floors and band members replay the declared "
            "draws from the declared kinds at the declared "
            "positions exactly as the frozen artifacts consumed "
            "them; each cell's plants consume the declared plant "
            "kinds 24 and 25 at positions 0 to 4 against the "
            "alternate reference text, the same kind and position "
            "consumption the frozen artifacts declared for their "
            "plants of the standing reference text; the band "
            "members consume the declared cross kinds at positions "
            "english 0 to 6 and latin 0 to 7 exactly as the frozen "
            "widened band consumed them; consuming none of any "
            "other module's declared draws",
            "bridge_gate": "before the alternate cells run, the "
            "alternate instrument's full first cell (ZL english: "
            "the real, its five plants of the standing reference "
            "text, its five floors and its seven widened band "
            "members) is computed through this measurement's code "
            "with the standing reference supplied and compared "
            "field for field against the frozen widened-band "
            "artifact's own first cell; any divergence aborts with "
            "nothing written",
            "corpus_source_rule": "the alternate references are "
            "fetched from the standing members' declared source in "
            "the same plain text form; each alternate's file is "
            "stored raw under engine/data with its Gutenberg "
            "markers and processed by the standing declared "
            "processing (the body extracted between the markers, "
            "the ligatures joined, NFD plus casefold, letters to 0 "
            "to 25 and non-letter runs to the single boundary "
            "token), with the sha256 recorded below",
            "corpus_rule": "alternate references are declared per "
            "language, one each, under the declared corpus rules: "
            "the english alternate a modern printed english prose "
            "text outside the band's membership list; the latin "
            "alternate a latin prose text outside the band's "
            "membership list keeping the standing members' "
            "transcriber-note english scaffold scale (0 to 52 "
            "common-word hits, zero mid-span english in every "
            "accepted member); candidates interleaving english "
            "translations, glossed school notes, critical apparatus "
            "or scholarly bibliographies through the span, or whose "
            "form is other than connected prose, rejected with "
            "cause",
            "same_work_family_rule": "the declared latin alternate "
            "pg60772 is volume two of the same printed travel "
            "account whose volume one is widened band member "
            "pg58528: the circumstance is disclosed and the design "
            "keeps the declared single alternate rather than "
            "swapping to another candidate, because the remaining "
            "probed candidates were rejected with cause or terse in "
            "form; the reference scope stays a single alternate "
            "choice outside the band membership list",
            "rejected_candidates": REJECTED_ALTERNATE_CANDIDATES,
            "probed_not_selected": PROBED_NOT_SELECTED_ALTERNATES,
            "band_record_rule": "membership, selection, ties and "
            "spreads are declared unchanged from the held-out screen "
            "(a member's band value the held-out value of the draw "
            "whose exact climb-half total is best, strict beyond "
            "1e-12, ties to the first draw); each member records "
            "draws_climb_exact, its five climb-half totals at full "
            "precision, so the declared selection is re-derivable "
            "from the stored artifact; membership unconditional: "
            "every band member enters the band under the alternate "
            "tables exactly as under the standing tables and no "
            "convergence criterion is applied to any member",
            "verdict_rule": "unchanged from the held-out screen and "
            "applied to the reference-scope numbers: the real "
            "held-out at or above the smallest member band value is "
            "consistent-with-substitution, at or below the largest "
            "floor's held-out value is not-consistent, strictly "
            "between is below-held-band; the strings describe "
            "consistency under this artifact's declared reference "
            "scope and do not restate the widened band's verdicts",
            "margin_rule": "the margin is computed from the stored "
            "rounded values: the real held-out mean minus the "
            "smallest member band value, rounded to four decimals",
            "exclusion_rule": "the family's declared exclusion format "
            "is not re-scoped by this artifact: it keys to the "
            "declared 36-slot class under the inherited add-one form "
            "exactly as the held-out screen declared it, so an "
            "alternate-reference verdict is reference-scope evidence "
            "and the widened band's verdicts stand untouched by this "
            "artifact's numbers",
            "truthful_question": "declared in advance: does the "
            "real's held-out score-half value still stand above the "
            "band when the scored tables are rebuilt from single "
            "alternate references outside the band - a yes extends "
            "the separation across the reference scope, a no "
            "records that the margin rode the standing references' "
            "single choice",
            "corpus_facts": {},
            "models": {},
        },
        "bridge_gate": {},
        "files": {},
    }
    for language in LANGS:
        name, ebook, _label = ALTERNATE_REFERENCE_FILES[language]
        stream = _reference_stream(language, file=name)
        model = _alternate_table(language)
        table = model["table"]
        full_matrix = _stream_matrix_27(stream)
        block_held, block_climb, _bcp, _bsp = _block_identity_half_means(
            stream, table
        )
        add_one_held, _acm, _acp, _asp = _identity_half_means(
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
            "block_climb_half_mean_nats_per_pair": round(block_climb, 4),
            "block_score_half_mean_nats_per_pair": round(block_held, 4),
            "add_one_parity_score_half_mean_nats_per_pair": round(
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
    for language in LANGS:
        name, ebook, label = ALTERNATE_REFERENCE_FILES[language]
        path = Path(DATA_DIR).resolve().parent / name
        raw = path.read_bytes()
        text = raw.decode("utf-8", "replace")
        start = text.find("START OF THE PROJECT GUTENBERG")
        end = text.find("END OF THE PROJECT GUTENBERG")
        body = text[text.find("\n", start):end]
        if language == "latin":
            # the apparatus probe is defined on latin spans; english
            # members are modern english prose and carry no foreign
            # apparatus category
            hits: int | None = len(
                re.findall(r"\b(the|and|with|from)\b", body)
            )
        else:
            hits = None
        members_stream = _reference_stream(language, file=name)
        letter_tokens = sum(
            members_stream.count(i) for i in range(26)
        )
        artifact["declared"]["corpus_facts"][language] = [{
            "file": name,
            "ebook": ebook,
            "label": label,
            "sha256": hashlib.sha256(raw).hexdigest(),
            "file_bytes": len(raw),
            "body_bytes": len(body),
            "stream_length": len(members_stream),
            "letter_tokens": letter_tokens,
            "boundary_tokens": len(members_stream) - letter_tokens,
            "types_present": len(set(members_stream)),
            "english_scaffold_hits": hits,
        }]
    for code in FILES:
        cell: dict = {}
        for language in LANGS:
            name, _ebook, _label = ALTERNATE_REFERENCE_FILES[language]
            model = _alternate_table(language)
            facts = _block_cell_facts(
                code, language, model["table"], model["letter_counts"],
                reference_file=name,
            )
            positions = _extended_band_positions(language)
            members = [
                _block_band_for(
                    code, language, seed_index,
                    model["table"], model["letter_counts"],
                    members=_extended_reference_members(language),
                )
                for seed_index in positions
            ]
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


def main_alternate_reference() -> None:
    artifact = substitution_homophonic_alternate_reference()
    ALTERNATE_ARTIFACT_PATH.write_text(
        json.dumps(artifact, indent=2) + "\n"
    )
    print(ALTERNATE_ARTIFACT_PATH)


# --------------------------------------------------------------------------
# The split ratio measurement, the eighth declared measurement
# --------------------------------------------------------------------------


RATIO_ARTIFACT_PATH = (
    Path(DATA_DIR).resolve().parent.parent.parent
    / "docs" / "research-notes" / "voynich-homophonic-split-ratio.json"
)


def _quarter_pairs(
    first: np.ndarray, second: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """The declared split-ratio split of a stream's counted pairs: the
    pairs kept in stream order split into contiguous blocks at the
    quarter mark, the first floor(N/4) pairs the climb part the
    machinery may search and the remaining pairs the score part it
    may never touch, the block fold's own first-block convention (the
    smaller share on a remainder) at one quarter of the pairs. The
    halves share no counted pair, no pair of the climb part lies in
    the scored block's index range, and the scored pairs stay fresh
    to the search in the span sense."""
    climb_len = len(first) // 4
    return (first[:climb_len], second[:climb_len],
            first[climb_len:], second[climb_len:])


def _compare_ratio_to_widened() -> tuple[list[str], int]:
    """The declared bridge gate: the split-ratio instrument's full
    first cell (ZL english: the real, its five plants, its five
    floors and all seven widened band members) computed through this
    measurement's code with the block fold's standing split supplied
    must equal the frozen widened-band artifact's own first cell
    field for field, so the only difference from the frozen widened
    measurement is the split's ratio. Any divergence aborts with
    nothing written."""
    problems: list[str] = []
    fields = 0
    code, language = "ZL", "english"
    frozen = json.loads(WIDENED_BAND_ARTIFACT_PATH.read_text())
    stored = frozen["files"][code][language]
    model = _shape_table(language)
    facts = _block_cell_facts(
        code, language, model["table"], model["letter_counts"],
        split_pairs=_block_pairs,
    )
    for key, value in facts.items():
        fields += 1
        if stored[_CELL_FIELD_MAP[key]] != value:
            problems.append(
                f"cell/{key}: stored {stored[_CELL_FIELD_MAP[key]]!r} vs "
                f"fresh {value!r}"
            )
    members = _extended_reference_members(language)
    for seed_index in _extended_band_positions(language):
        fresh = _block_band_for(
            code, language, seed_index,
            model["table"], model["letter_counts"],
            split_pairs=_block_pairs, members=members,
        )
        stored_member = stored["band"][seed_index]
        for key, value in fresh.items():
            fields += 1
            if stored_member[key] != value:
                problems.append(
                    f"band/{seed_index}/{key}: stored "
                    f"{stored_member[key]!r} vs fresh {value!r}"
                )
    return problems, fields


def substitution_homophonic_split_ratio() -> dict:
    """The declared split's ratio: the widened band measurement's six
    (file, language) cells with their real, plants, floors, band
    population, seeds, machinery, leave-one-out tables and reference
    texts replayed unchanged, re-measured under the declared 25/75
    block split - the climb part the first quarter of each side's
    counted pairs, the score part the remaining pairs the search may
    never touch - after the bridge gate proves this measurement's
    code reproduces the frozen widened-band artifact's first cell
    field for field through the standing split."""
    problems, fields = _compare_ratio_to_widened()
    if problems:
        raise RuntimeError(
            "the bridge gate failed: " + "; ".join(problems[:12])
        )
    artifact: dict = {
        "what": "The declared split's ratio: the widened band "
        "measurement's six (file, language) cells re-measured with "
        "the mapped set, streams, seeds, machinery, restarts, sweep "
        "cap, plants, floors, block population and leave-one-out "
        "tables carried forward unchanged, and each side's counted "
        "pairs re-fold under the declared 25/75 block split, so the "
        "real is priced above the same band with the machinery's "
        "climb freedom shrunk to a quarter of each side's pairs. The "
        "bridge gate re-derived the frozen widened-band artifact's "
        "first cell through the standing split before the ratio cells "
        "ran. The declared truthful question: does the real's "
        "held-out score-half value still stand above the band when "
        "the climb part shrinks to a quarter of each side's pairs. "
        "No mapping is published; nothing here is a reading.",
        "declared": {
            "base_seed": BASE_SEED,
            "mapped": MAPPED_HOMO,
            "restarts": N_RESTARTS,
            "sweep_cap": SWEEP_CAP,
            "plants_per_cell": N_PLANTS,
            "floors": N_FLOORS,
            "band_positions": {
                language: len(_extended_reference_members(language))
                for language in LANGS
            },
            "split_rule": "the counted pairs of each side, in stream "
            "order, split into contiguous blocks at the quarter mark: "
            "the first floor(N/4) pairs the climb part the machinery "
            "may search, the remaining pairs the score part it may "
            "never touch; the block fold's own first-block convention "
            "(the smaller share on a remainder) at one quarter of the "
            "pairs; the halves share no counted pair and every "
            "identity anchor's halves fold by the same rule; "
            "deterministic, consuming no seed",
            "loo_rule": "the shape measurement's leave-one-out table "
            "carried forward unchanged: the inherited add-one form is "
            "log((n_ab + 1) / (N + 729)) with N the standing "
            "reference stream's total counted pairs; every pair type "
            "(a, b) present in the reference pair table is scored "
            "with one occurrence of (a, b) removed from the reference "
            "counts, log(n_ab / (N + 728)), and a type with no "
            "counted occurrence keeps the inherited add-one entry "
            "log(1 / (N + 729)); the letter marginals and rank "
            "initialisation unchanged, the matrix arithmetic needing "
            "no re-derivation as the shape measurement declared",
            "measured_facts_rule": "the mapped set, streams, seeds, "
            "machinery, restarts, sweep cap, plants, floors, band "
            "population and reference texts are the held-out "
            "screen's, block-fold measurement's and widened band's "
            "declarations carried unchanged; the real, plants, "
            "floors and every band member's encodings are "
            "byte-identical replays of the frozen widened-band "
            "artifact's declared draws and only the split's ratio "
            "changes: every side's counted pairs re-fold at the "
            "quarter mark, every identity anchor's halves fold by "
            "the same rule, and the machinery re-climbs on the "
            "smaller climb part with ties to the first restart; each "
            "member records draws_climb_exact, its five climb-half "
            "totals at full precision; each side's exact full-data "
            "side call is recorded beside its held-out value for "
            "attribution only",
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
            "seed_sharing": "no new seed kinds are consumed: the "
            "real, plants, floors and band members replay the "
            "declared draws from the declared kinds at the declared "
            "positions exactly as the frozen widened band consumed "
            "them, and the split consumes no seed; consuming none of "
            "any other module's declared draws",
            "bridge_gate": "before the ratio cells run, the "
            "split-ratio instrument's full first cell (ZL english: "
            "the real, its five plants, its five floors and its "
            "seven widened band members) is computed through this "
            "measurement's code with the block fold's standing "
            "split supplied and compared field for field against "
            "the frozen widened-band artifact's own first cell; any "
            "divergence aborts with nothing written",
            "corpus_source_rule": "no new corpus files: this "
            "measurement declares no candidates and records no "
            "corpus roster; the band population is the frozen "
            "widened band's declared roster and the references are "
            "the standing references' frozen files, all stored raw "
            "with their Gutenberg markers and processed by the "
            "standing declared processing",
            "band_record_rule": "membership, selection, ties and "
            "spreads are declared unchanged from the held-out screen "
            "(a member's band value the held-out value of the draw "
            "whose exact climb-half total is best, strict beyond "
            "1e-12, ties to the first draw); each member records "
            "draws_climb_exact, its five climb-half totals at full "
            "precision, so the declared selection is re-derivable "
            "from the stored artifact; membership unconditional: "
            "every band member enters the band under the ratio "
            "split exactly as under the block fold and no "
            "convergence criterion is applied to any member",
            "verdict_rule": "unchanged from the held-out screen and "
            "applied to the split-ratio numbers: the real held-out "
            "at or above the smallest member band value is "
            "consistent-with-substitution, at or below the largest "
            "floor's held-out value is not-consistent, strictly "
            "between is below-held-band; the strings describe "
            "consistency under this artifact's declared split ratio "
            "and do not restate the widened band's verdicts",
            "margin_rule": "the margin is computed from the stored "
            "rounded values: the real held-out mean minus the "
            "smallest member band value, rounded to four decimals",
            "exclusion_rule": "the family's declared exclusion format "
            "is not re-scoped by this artifact: it keys to the "
            "declared 36-slot class under the inherited add-one form "
            "exactly as the held-out screen declared it, so a "
            "split-ratio verdict is split-geometry evidence and the "
            "widened band's verdicts stand untouched by this "
            "artifact's numbers",
            "truthful_question": "declared in advance: does the "
            "real's held-out score-half value still stand above the "
            "band when the climb part shrinks to a quarter of each "
            "side's counted pairs - a yes extends the separation to "
            "a smaller search freedom, a no records that the margin "
            "rode the climb half's size",
            "corpus_facts": {},
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
        full_matrix = _stream_matrix_27(stream)
        block_held, block_climb, _bcp, _bsp = _block_identity_half_means(
            stream, table
        )
        add_one_held, _acm, _acp, _asp = _identity_half_means(
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
            "block_climb_half_mean_nats_per_pair": round(block_climb, 4),
            "block_score_half_mean_nats_per_pair": round(block_held, 4),
            "add_one_parity_score_half_mean_nats_per_pair": round(
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
            facts = _block_cell_facts(
                code, language, model["table"], model["letter_counts"],
                split_pairs=_quarter_pairs,
            )
            positions = _extended_band_positions(language)
            members = [
                _block_band_for(
                    code, language, seed_index,
                    model["table"], model["letter_counts"],
                    split_pairs=_quarter_pairs,
                    members=_extended_reference_members(language),
                )
                for seed_index in positions
            ]
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


def main_split_ratio() -> None:
    artifact = substitution_homophonic_split_ratio()
    RATIO_ARTIFACT_PATH.write_text(
        json.dumps(artifact, indent=2) + "\n"
    )
    print(RATIO_ARTIFACT_PATH)


# --------------------------------------------------------------------------
# The restart budget measurement, the ninth declared measurement
# --------------------------------------------------------------------------


RESTART_BUDGET = 48
CONVERGENCE_TOLERANCE = 0.0001
RESTART_BUDGET_ARTIFACT_PATH = (
    Path(DATA_DIR).resolve().parent.parent.parent
    / "docs" / "research-notes" / "voynich-homophonic-restart-budget.json"
)


def machinery_best_held_recorded(
    climb_matrix: np.ndarray,
    score_matrix: np.ndarray,
    table: np.ndarray,
    letter_counts: np.ndarray,
    rng: np.random.Generator,
    restarts: int = N_RESTARTS,
) -> tuple[float, float, bool, list[float]]:
    """The declared held-out machinery with every restart's exact
    climb-half total recorded.

    The declared held-out machinery otherwise: restart 0 the rank
    initialisation computed from the climb half, restarts 1 onward one
    seeded permutation of the 27 letter tokens under the same wrap
    rule consumed in the same order, the best restart the best exact
    climb-half total with ties to the first restart, and the chosen
    assignment priced exactly on the score half. Returns the chosen
    assignment's mean nats per scored pair, its mean nats per climb
    pair, whether any climb hit the declared sweep cap, and the
    restarts' exact climb-half means in restart order at full
    precision list. No assignment is returned and none is stored: the
    recovered mapping is never published."""
    symbols = climb_matrix.shape[0]
    climb_pairs = climb_matrix.sum()
    climb_total, sweeps, f_best = _held_climb(
        climb_matrix, table, _rank_init(climb_matrix, letter_counts)
    )
    restart_totals = [float(climb_total) / float(climb_pairs)]
    cap_hit = sweeps >= SWEEP_CAP
    for _index in range(restarts - 1):
        permutation = list(rng.permutation(27))
        start = [permutation[symbol % 27] for symbol in range(symbols)]
        score, sweeps, f = _held_climb(climb_matrix, table, start)
        cap_hit = cap_hit or sweeps >= SWEEP_CAP
        restart_totals.append(float(score) / float(climb_pairs))
        if score > climb_total + 1e-12:
            climb_total = score
            f_best = f
    climb_mean = float(climb_total) / float(climb_pairs)
    held_mean = (
        float((score_matrix * table[f_best][:, f_best]).sum())
        / float(score_matrix.sum())
    )
    return held_mean, climb_mean, bool(cap_hit), restart_totals


def machinery_exact_full_recorded(
    matrix: np.ndarray,
    table: np.ndarray,
    letter_counts: np.ndarray,
    rng: np.random.Generator,
    restarts: int = N_RESTARTS,
) -> tuple[float, bool, list[float]]:
    """The declared exact full-data climb with every restart's exact
    total recorded, otherwise the attribution side machinery of the
    held-out measurement: restart 0 the rank initialisation, restarts
    1 onward one seeded permutation each under the wrap rule, the best
    the maximum exact total. Returns the best exact mean nats per
    counted pair over the unsplit matrix, whether any climb hit the
    declared sweep cap, and the restarts' exact means in restart order
    at full precision."""
    symbols = matrix.shape[0]
    pairs = matrix.sum()
    best, sweeps, _assignment = _held_climb(
        matrix, table, _rank_init(matrix, letter_counts)
    )
    restart_totals = [float(best) / float(pairs)]
    cap_hit = sweeps >= SWEEP_CAP
    for _index in range(restarts - 1):
        permutation = list(rng.permutation(27))
        start = [permutation[symbol % 27] for symbol in range(symbols)]
        score, sweeps, _assignment = _held_climb(matrix, table, start)
        cap_hit = cap_hit or sweeps >= SWEEP_CAP
        restart_totals.append(float(score) / float(pairs))
        best = max(best, score)
    return best / pairs, bool(cap_hit), restart_totals


def _restart_convergence(totals: list[float]) -> bool:
    """The declared convergence lens on one machinery call's recorded
    restarts: family 4's declared agree-to-within-0.0001 precision
    applied to the restarts' recorded exact means - the flag true when
    the distance between the best and the worst recorded restart is at
    most 0.0001 mean nats per pair. A recorded status only: no
    verdict, margin, membership or exclusion depends on any flag."""
    return (max(totals) - min(totals)) <= CONVERGENCE_TOLERANCE


def _restart_cell_facts(
    code: str, language: str,
    table: np.ndarray, letter_counts: np.ndarray,
    restarts: int = RESTART_BUDGET,
) -> dict:
    """Real, plants with their held-out anchor, and floors for one
    cell under the standing block fold and the declared restart
    budget, every machinery call's restarts recorded: the block fold's
    cell facts with the restart count supplied and every call's
    recorded restart totals and convergence flags added."""
    real_stream = _homo_real_stream(code)
    first, second = _kept_pairs(
        real_stream["event_ids"], real_stream["kept_mask"]
    )
    climb_first, climb_second, score_first, score_second = (
        _block_pairs(first, second)
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
    held_value, climb_value, cap_hit, real_totals = (
        machinery_best_held_recorded(
            climb_matrix, score_matrix, table, letter_counts, real_rng,
            restarts=restarts,
        )
    )
    real_held = round(held_value, 4)
    real_climb = round(climb_value, 4)
    real_hit = bool(cap_hit)
    full_rng = np.random.default_rng(
        _seed(CELL_ID[code], KIND_ID["real"], LANG_ID[language], 0)
    )
    full_value, full_hit, real_full_totals = machinery_exact_full_recorded(
        full_matrix, table, letter_counts, full_rng, restarts=restarts
    )
    real_full = round(full_value, 4)
    truncated = _truncated_reference(code, language)
    anchor, anchor_climb, _climb_half, _score_half = (
        _block_identity_half_means(truncated, table)
    )
    anchor = round(anchor, 4)
    anchor_climb = round(anchor_climb, 4)
    plants_held = []
    plants_full = []
    plants_hits = []
    plants_full_hits = []
    plants_totals = []
    plants_full_totals = []
    plants_convergence = []
    plants_full_convergence = []
    for index in range(N_PLANTS):
        groups = _partition_groups(truncated, MAPPED_HOMO)
        rng_enc = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["homo_plant_enc"],
                  LANG_ID[language], index)
        )
        plant = _encode(truncated, groups, rng_enc, MAPPED_HOMO)
        plant_first, plant_second = _full_pairs(plant)
        p_climb_first, p_climb_second, p_score_first, p_score_second = (
            _block_pairs(plant_first, plant_second)
        )
        p_climb = _matrix_from_pairs(p_climb_first, p_climb_second)
        p_score = _matrix_from_pairs(p_score_first, p_score_second)
        p_full = _full_matrix_37(plant)
        rng_mach = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["homo_plant_mach"],
                  LANG_ID[language], index)
        )
        value, _view, hit, totals = machinery_best_held_recorded(
            p_climb, p_score, table, letter_counts, rng_mach,
            restarts=restarts,
        )
        plants_held.append(round(value, 4))
        plants_hits.append(bool(hit))
        plants_totals.append(totals)
        plants_convergence.append(_restart_convergence(totals))
        rng_full = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["homo_plant_mach"],
                  LANG_ID[language], index)
        )
        value_full, hit_full, totals_full = (
            machinery_exact_full_recorded(
                p_full, table, letter_counts, rng_full,
                restarts=restarts,
            )
        )
        plants_full.append(round(value_full, 4))
        plants_full_hits.append(bool(hit_full))
        plants_full_totals.append(totals_full)
        plants_full_convergence.append(_restart_convergence(totals_full))
    floors_held = []
    floors_full = []
    floors_hits = []
    floors_full_hits = []
    floors_totals = []
    floors_full_totals = []
    floors_convergence = []
    floors_full_convergence = []
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
            _block_pairs(floor_first, floor_second)
        )
        f_climb = _matrix_from_pairs(f_climb_first, f_climb_second)
        f_score = _matrix_from_pairs(f_score_first, f_score_second)
        rng_mach = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["homo_floor_mach"],
                  LANG_ID[language], index)
        )
        value, _view, hit, totals = machinery_best_held_recorded(
            f_climb, f_score, table, letter_counts, rng_mach,
            restarts=restarts,
        )
        floors_held.append(round(value, 4))
        floors_hits.append(bool(hit))
        floors_totals.append(totals)
        floors_convergence.append(_restart_convergence(totals))
        rng_full = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["homo_floor_mach"],
                  LANG_ID[language], index)
        )
        value_full, hit_full, totals_full = machinery_exact_full_recorded(
            floor_full, table, letter_counts, rng_full, restarts=restarts
        )
        floors_full.append(round(value_full, 4))
        floors_full_hits.append(bool(hit_full))
        floors_full_totals.append(totals_full)
        floors_full_convergence.append(_restart_convergence(totals_full))
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
        "real_totals": real_totals,
        "real_convergence": _restart_convergence(real_totals),
        "real_full_totals": real_full_totals,
        "real_full_convergence": _restart_convergence(real_full_totals),
        "plants_totals": plants_totals,
        "plants_convergence": plants_convergence,
        "plants_full_totals": plants_full_totals,
        "plants_full_convergence": plants_full_convergence,
        "floors_totals": floors_totals,
        "floors_convergence": floors_convergence,
        "floors_full_totals": floors_full_totals,
        "floors_full_convergence": floors_full_convergence,
    }


def _restart_band_for(
    code: str, language: str, seed_index: int,
    table: np.ndarray, letter_counts: np.ndarray,
    members: list[tuple[str, int]] | None = None,
    restarts: int = RESTART_BUDGET,
) -> dict:
    """One widened band member under the standing block fold and the
    declared restart budget, every machinery call's restarts recorded:
    the block fold's band facts with the restart count supplied, each
    draw's restart totals and convergence flag recorded."""
    if members is None:
        members = _extended_reference_members(language)
    name, ebook = members[seed_index]
    truncated = _truncated_reference(code, language, file=name)
    anchor, anchor_climb, _climb_half, _score_half = (
        _block_identity_half_means(truncated, table)
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
    draws_totals = []
    draws_full_totals = []
    draws_convergence = []
    draws_full_convergence = []
    for _index in range(N_PLANTS):
        groups = _partition_groups(truncated, MAPPED_HOMO)
        encoded = _encode(truncated, groups, rng_enc, MAPPED_HOMO)
        enc_first, enc_second = _full_pairs(encoded)
        e_climb_first, e_climb_second, e_score_first, e_score_second = (
            _block_pairs(enc_first, enc_second)
        )
        e_climb = _matrix_from_pairs(e_climb_first, e_climb_second)
        e_score = _matrix_from_pairs(e_score_first, e_score_second)
        e_full = _full_matrix_37(encoded)
        rng_mach = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["homo_cross_mach"],
                  LANG_ID[language], seed_index)
        )
        value, climb_view, hit, draw_totals = (
            machinery_best_held_recorded(
                e_climb, e_score, table, letter_counts, rng_mach,
                restarts=restarts,
            )
        )
        rng_full = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["homo_cross_mach"],
                  LANG_ID[language], seed_index)
        )
        value_full, hit_full, draw_full_totals = (
            machinery_exact_full_recorded(
                e_full, table, letter_counts, rng_full,
                restarts=restarts,
            )
        )
        draws_held.append(round(value, 4))
        draws_climb.append(round(climb_view, 4))
        climbs_exact.append(float(climb_view))
        draws_full.append(round(value_full, 4))
        draw_hits.append(bool(hit))
        draw_full_hits.append(bool(hit_full))
        climb_totals.append(climb_view)
        draws_totals.append(draw_totals)
        draws_convergence.append(_restart_convergence(draw_totals))
        draws_full_totals.append(draw_full_totals)
        draws_full_convergence.append(
            _restart_convergence(draw_full_totals)
        )
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
        "draws_restart_totals": draws_totals,
        "draws_convergence": draws_convergence,
        "draws_full_restart_totals": draws_full_totals,
        "draws_full_convergence": draws_full_convergence,
    }


def _compare_restart_to_ratio() -> tuple[list[str], int]:
    """The declared bridge gate: the restart-budget instrument's full
    first cell (ZL english: the real, its five plants, its five floors
    and all seven widened band members) computed through this
    measurement's code with the inherited 16 restarts supplied and
    every call's restarts recorded must equal the frozen widened-band
    artifact's own first cell field for field, so the only difference
    from the frozen widened-band measurement is the restart budget's
    depth. Any divergence aborts with nothing written."""
    problems: list[str] = []
    fields = 0
    code, language = "ZL", "english"
    frozen = json.loads(WIDENED_BAND_ARTIFACT_PATH.read_text())
    stored = frozen["files"][code][language]
    model = _shape_table(language)
    facts = _restart_cell_facts(
        code, language, model["table"], model["letter_counts"],
        restarts=N_RESTARTS,
    )
    for key, cell_key in _CELL_FIELD_MAP.items():
        fields += 1
        if facts[key] != stored[cell_key]:
            problems.append(
                f"cell/{key}: stored {stored[cell_key]!r} vs fresh "
                f"{facts[key]!r}"
            )
    members = _extended_reference_members(language)
    for seed_index in _extended_band_positions(language):
        fresh = _restart_band_for(
            code, language, seed_index,
            model["table"], model["letter_counts"],
            members=members, restarts=N_RESTARTS,
        )
        stored_member = stored["band"][seed_index]
        for key, value in stored_member.items():
            fields += 1
            if fresh[key] != value:
                problems.append(
                    f"band/{seed_index}/{key}: stored {value!r} vs "
                    f"fresh {fresh[key]!r}"
                )
    return problems, fields


def substitution_homophonic_restart_budget() -> dict:
    """The declared restart budget: the widened band measurement's six
    (file, language) cells with their real, plants, floors, band
    population, seeds, machinery, sweep payouts, split, leave-one-out
    tables and reference texts replayed unchanged, and every machinery
    call's restart count raised from the inherited 16 to the declared
    48 with each call's restarts recorded and family 4's declared
    convergence lens applied, after the bridge gate proves this
    measurement's code reproduces the frozen widened-band artifact's
    first cell field for field through the inherited budget."""
    problems, fields = _compare_restart_to_ratio()
    if problems:
        raise RuntimeError(
            "the bridge gate failed: " + "; ".join(problems[:12])
        )
    artifact: dict = {
        "what": "The declared restart budget: the widened band "
        "measurement's six (file, language) cells re-measured with the "
        "mapped set, streams, seeds, machinery, sweep cap, block "
        "split, plants, floors, band population and leave-one-out "
        "tables carried forward unchanged, and each machinery call's "
        "restart count raised from the inherited 16 to the declared "
        "48, so every side searches three times the inherited depth "
        "under the same instrument. The bridge gate re-derived the "
        "frozen widened-band artifact's first cell through the "
        "inherited budget before the deeper cells ran. The declared "
        "truthful question: does the real's held-out score-half value "
        "still stand above the band when every machinery call draws "
        "three times the inherited restart budget. No mapping is "
        "published; nothing here is a reading.",
        "declared": {
            "base_seed": BASE_SEED,
            "mapped": MAPPED_HOMO,
            "restarts": RESTART_BUDGET,
            "restarts_inherited": N_RESTARTS,
            "sweep_cap": SWEEP_CAP,
            "plants_per_cell": N_PLANTS,
            "floors": N_FLOORS,
            "band_positions": {
                language: len(_extended_reference_members(language))
                for language in LANGS
            },
            "restarts_rule": "the declared restart budget 48 per "
            "machinery call (one rank initialisation plus 47 seeded "
            "permutations), up from the inherited 16; the extra "
            "restarts continue each call's declared machinery kind's "
            "permutation stream, restarts 1 to 15 replaying the "
            "inherited budget's permutation draws exactly and "
            "restarts 16 to 47 drawing the next 32 permutations of "
            "the same stream at the same declared kind and position, "
            "consuming no new seed kind and no new position; every "
            "recorded inherited-budget value re-prices only if a "
            "later restart strictly beats the running best beyond "
            "1e-12, ties to the first restart, so the first 16 "
            "restarts of every call are byte-identical replays of "
            "the frozen widened band's declared draws and only the "
            "restart budget's depth changes; deterministic, "
            "consuming no new seed",
            "convergence_rule": "every machinery call records its "
            "restarts at full precision, the exact climb-half means "
            "for the held-out machinery and the exact full-data means "
            "for the full side machinery, and each call records a "
            "declared convergence lens, family 4's declared "
            "agree-to-within-0.0001 precision applied to the "
            "restarts' recorded means: a call's flag true when the "
            "distance between its best and its worst recorded "
            "restart is at most 0.0001 mean nats per pair. The flags "
            "are recorded facts; no verdict, margin, membership or "
            "exclusion depends on any flag, and band membership "
            "stays unconditional exactly as the held-out screen "
            "declared",
            "loo_rule": "the shape measurement's leave-one-out table "
            "carried forward unchanged: the inherited add-one form is "
            "log((n_ab + 1) / (N + 729)) with N the standing "
            "reference stream's total counted pairs; every pair type "
            "(a, b) present in the reference pair table is scored "
            "with one occurrence of (a, b) removed from the reference "
            "counts, log(n_ab / (N + 728)), and a type with no "
            "counted occurrence keeps the inherited add-one entry "
            "log(1 / (N + 729)); the letter marginals and rank "
            "initialisation unchanged, the matrix arithmetic needing "
            "no re-derivation as the shape measurement declared",
            "split_rule": "the block fold's split carried unchanged "
            "from the widened band: the counted pairs of each side, "
            "in stream order, split at the midpoint, the first "
            "floor(N/2) pairs the climb half the machinery may "
            "search and the remaining pairs the score half it may "
            "never touch; the split's ratio's 25/75 variant is not "
            "this measurement's split, and every identity anchor's "
            "halves fold by the standing block rule; deterministic, "
            "consuming no seed",
            "measured_facts_rule": "the mapped set, streams, seeds, "
            "machinery, sweep cap, block split, plants, floors, band "
            "population and reference texts are the held-out "
            "screen's, block-fold measurement's and widened band's "
            "declarations carried unchanged; every machinery call "
            "climbs the declared 48 restarts by continuing the "
            "frozen widened-band draws' permutation streams, so "
            "only the restart budget's depth changes and every "
            "recorded inherited-budget value re-prices only on "
            "strict improvement beyond 1e-12, ties to the first "
            "restart; the per-restart recording is new to this "
            "artifact at full precision and each call's exact "
            "full-data side call stays recorded beside its held-out "
            "value for attribution only",
            "machinery_rule": "unchanged from the held-out screen, "
            "recorded: the exact greedy reassignment climb on the "
            "climb half, exact pricing on the score half, restart 0 "
            "the rank initialisation from the climb half, restarts "
            "1 to 47 the seeded permutations of the 27 letter tokens "
            "under the wrap rule, the best restart the best exact "
            "climb-half total with ties to the first; every "
            "restart's exact total recorded; no assignment is "
            "stored",
            "seed_kinds": {
                "real": KIND_ID["real"],
                "homo_plant": [KIND_ID["homo_plant_enc"],
                               KIND_ID["homo_plant_mach"]],
                "homo_floor": [KIND_ID["homo_floor_perm"],
                               KIND_ID["homo_floor_mach"]],
                "homo_cross": [KIND_ID["homo_cross_enc"],
                               KIND_ID["homo_cross_mach"]],
            },
            "seed_sharing": "no new seed kinds are consumed: the "
            "real, plants, floors and band members replay the "
            "declared draws from the declared kinds at the declared "
            "positions exactly as the frozen widened band consumed "
            "them, the extra restarts drawing continuations "
            "of the same machinery streams, the split consuming no "
            "seed; consuming none of any other module's declared "
            "draws",
            "bridge_gate": "before the deeper cells run, the "
            "restart-budget instrument's full first cell (ZL "
            "english: the real, its five plants, its five floors "
            "and its seven widened band members) is computed through "
            "this measurement's code with the inherited 16 restarts "
            "supplied and every call's restarts recorded, and "
            "compared field for field against the frozen "
            "widened-band artifact's own first cell; any divergence "
            "aborts with nothing written",
            "corpus_source_rule": "no new corpus files: this "
            "measurement declares no candidates and records no "
            "corpus roster; the band population is the frozen "
            "widened band's declared roster and the references are "
            "the standing references' frozen files, all stored raw "
            "with their Gutenberg markers and processed by the "
            "standing declared processing",
            "band_record_rule": "membership, selection, ties and "
            "spreads are declared unchanged from the held-out screen "
            "(a member's band value the held-out value of the draw "
            "whose exact climb-half total is best, strict beyond "
            "1e-12, ties to the first draw); each member records "
            "draws_climb_exact, its five climb-half totals at full "
            "precision, now the best of each draw's 48 recorded "
            "restarts, every draw's restart totals at full "
            "precision and every draw's convergence flag; "
            "membership unconditional: every band member enters the "
            "band under the declared restart budget exactly as "
            "under the inherited budget and no convergence "
            "criterion is applied to any member",
            "verdict_rule": "unchanged from the held-out screen and "
            "applied to the restart-budget numbers: the real "
            "held-out at or above the smallest member band value is "
            "consistent-with-substitution, at or below the largest "
            "floor's held-out value is not-consistent, strictly "
            "between is below-held-band; the strings describe "
            "consistency under this artifact's declared restart "
            "budget and do not restate the widened band's verdicts",
            "margin_rule": "the margin is computed from the stored "
            "rounded values: the real held-out mean minus the "
            "smallest member band value, rounded to four decimals",
            "exclusion_rule": "the family's declared exclusion format "
            "is not re-scoped by this artifact: it keys to the "
            "declared 36-slot class under the inherited add-one form "
            "exactly as the held-out screen declared it, so a "
            "restart-budget verdict is search-depth evidence and "
            "the widened band's verdicts stand untouched by this "
            "artifact's numbers",
            "truthful_question": "declared in advance: does the "
            "real's held-out score-half value still stand above the "
            "band when every machinery call draws three times the "
            "inherited restart budget - a yes extends the "
            "separation to a deeper search, a no records that the "
            "margin rode the inherited budget's depth",
            "corpus_facts": {},
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
        full_matrix = _stream_matrix_27(stream)
        block_held, block_climb, _bcp, _bsp = _block_identity_half_means(
            stream, table
        )
        add_one_held, _acm, _acp, _asp = _identity_half_means(
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
            "block_climb_half_mean_nats_per_pair": round(block_climb, 4),
            "block_score_half_mean_nats_per_pair": round(block_held, 4),
            "add_one_parity_score_half_mean_nats_per_pair": round(
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
            facts = _restart_cell_facts(
                code, language, model["table"], model["letter_counts"],
                restarts=RESTART_BUDGET,
            )
            positions = _extended_band_positions(language)
            members = [
                _restart_band_for(
                    code, language, seed_index,
                    model["table"], model["letter_counts"],
                    members=_extended_reference_members(language),
                    restarts=RESTART_BUDGET,
                )
                for seed_index in positions
            ]
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
                "real_restart_totals": facts["real_totals"],
                "real_convergence": facts["real_convergence"],
                "real_full_restart_totals": facts["real_full_totals"],
                "real_full_convergence": (
                    facts["real_full_convergence"]
                ),
                "plants_restart_totals": facts["plants_totals"],
                "plants_convergence": facts["plants_convergence"],
                "plants_full_restart_totals": (
                    facts["plants_full_totals"]
                ),
                "plants_full_convergence": (
                    facts["plants_full_convergence"]
                ),
                "floors_restart_totals": facts["floors_totals"],
                "floors_convergence": facts["floors_convergence"],
                "floors_full_restart_totals": (
                    facts["floors_full_totals"]
                ),
                "floors_full_convergence": (
                    facts["floors_full_convergence"]
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


def main_restart_budget() -> None:
    artifact = substitution_homophonic_restart_budget()
    RESTART_BUDGET_ARTIFACT_PATH.write_text(
        json.dumps(artifact, indent=2) + "\n"
    )
    print(RESTART_BUDGET_ARTIFACT_PATH)


# --------------------------------------------------------------------------
# The tenth measurement: the search-free invariant instrument
# --------------------------------------------------------------------------

SEARCH_FREE_ARTIFACT_PATH = (
    Path(DATA_DIR).resolve().parent.parent.parent
    / "docs" / "research-notes" / "voynich-homophonic-search-free.json"
)
SEARCH_FREE_TOP_K = (1, 10, 50)
SEARCH_FREE_SHARES = 6


def _profile_facts(matrix: np.ndarray) -> dict:
    """The declared relabeling-invariant profile of one pair-count
    matrix, every summary a function of the matrix's count structure
    alone and invariant under any relabeling of the symbols: the
    sorted symbol marginals as counts and shares, the sorted
    pair-count multiset as counts and shares, the empty type count,
    the self-pair share (the diagonal sum over the total, itself
    permuted to itself under any relabeling), the top-k pair
    concentration at the declared k values and the pair entropy in
    nats per counted pair. Shares and entropy round to the declared
    6 decimals; the total and the state width are recorded beside
    them because the real's matrix prices kept-adjacent mapped pairs
    while an encoding's matrix prices every adjacent pair of its
    full stream."""
    total = int(round(matrix.sum()))
    symbols = matrix.sum(axis=1).astype(np.int64)
    counts = matrix.astype(np.int64).flatten()
    sorted_symbols = sorted(int(value) for value in symbols)[::-1]
    sorted_counts = sorted(int(value) for value in counts)[::-1]
    positive = np.array([value for value in sorted_counts if value > 0],
                        dtype=float)
    shares = positive / total
    top = {}
    for k in SEARCH_FREE_TOP_K:
        top[f"top_{k}_share"] = round(
            sum(sorted_counts[:k]) / total, SEARCH_FREE_SHARES
        )
    return {
        "total_pairs": total,
        "state_types": int(matrix.size),
        "symbol_counts": sorted_symbols,
        "symbol_shares": [
            round(value / total, SEARCH_FREE_SHARES)
            for value in sorted_symbols
        ],
        "pair_counts": sorted_counts,
        "pair_shares": [
            round(value / total, SEARCH_FREE_SHARES)
            for value in sorted_counts
        ],
        "empty_type_count": sum(
            1 for value in sorted_counts if value == 0
        ),
        "self_pair_share": round(
            float(np.trace(matrix)) / total, SEARCH_FREE_SHARES
        ),
        **top,
        "pair_entropy": round(
            -float((shares * np.log(shares)).sum()), SEARCH_FREE_SHARES
        ),
    }


def _search_free_envelope(
    real_profile: dict, member_facts: list[dict],
) -> dict:
    """The declared inside/outside record for one real profile against
    its simulated band's profiles: every declared invariant tested
    inside the band's closed range at the stored rounding, the two
    vector summaries by position envelope and the scalar summaries by
    their band's [min, max], with every outside entry recorded with
    its band range."""
    record: dict = {}
    for key in ("symbol_shares", "pair_shares"):
        vectors = [member["profile"][key] for member in member_facts]
        value = real_profile[key]
        lows = [
            min(vector[position] for vector in vectors)
            for position in range(len(value))
        ]
        highs = [
            max(vector[position] for vector in vectors)
            for position in range(len(value))
        ]
        outside = [
            {"position": position, "real": value[position],
             "band_low": lows[position], "band_high": highs[position]}
            for position in range(len(value))
            if value[position] < lows[position]
            or value[position] > highs[position]
        ]
        record[key] = {"inside": not outside, "outside": outside}
    for key in ("empty_type_count", "self_pair_share", "top_1_share",
                "top_10_share", "top_50_share", "pair_entropy"):
        values = [member["profile"][key] for member in member_facts]
        value = real_profile[key]
        low, high = min(values), max(values)
        record[key] = {
            "inside": low <= value <= high,
            "real": value, "band_low": low, "band_high": high,
        }
    return record


def _search_free_cell_facts(code: str, language: str) -> dict:
    """One cell's search-free facts: the real's own profile, every
    widened band member's selected-draw encoding profile replayed
    through the declared encoder at its frozen draw seed, the five
    plant encodings' profiles, the five destroyed-adjacency floors'
    profiles and the truncated standing reference's own plaintext
    control profile, with the inside/outside record and the cell's
    verdict under the declared strict-all rule. No machinery anywhere:
    no assignment search, no split, no cap, no convergence flags."""
    frozen = json.loads(RESTART_BUDGET_ARTIFACT_PATH.read_text())
    stored_band = frozen["files"][code][language]["band"]
    real = _homo_real_stream(code)
    real_matrix = _count_matrix_37(real["event_ids"], real["kept_mask"])
    real_profile = _profile_facts(real_matrix)
    members = _extended_reference_members(language)
    member_facts = []
    for position in _extended_band_positions(language):
        name, ebook = members[position]
        truncated = _truncated_reference(code, language, file=name)
        groups = _partition_groups(truncated, MAPPED_HOMO)
        rng_enc = np.random.default_rng(_seed(
            CELL_ID[code], KIND_ID["homo_cross_enc"],
            LANG_ID[language], position,
        ))
        selected = stored_band[position]["selected_draw_index"]
        encoded: np.ndarray | None = None
        for _draw in range(selected + 1):
            encoded = _encode(truncated, groups, rng_enc, MAPPED_HOMO)
        member_facts.append({
            "file": name,
            "ebook": ebook,
            "plant_length": len(truncated),
            "selected_draw_index": selected,
            "profile": _profile_facts(_full_matrix_37(encoded)),
        })
    standing_truncated = _truncated_reference(code, language)
    standing_groups = _partition_groups(standing_truncated, MAPPED_HOMO)
    plant_facts = []
    for index in range(N_PLANTS):
        rng_enc = np.random.default_rng(_seed(
            CELL_ID[code], KIND_ID["homo_plant_enc"],
            LANG_ID[language], index,
        ))
        encoded = _encode(
            standing_truncated, standing_groups, rng_enc, MAPPED_HOMO
        )
        plant_facts.append({
            "index": index,
            "plant_length": len(standing_truncated),
            "profile": _profile_facts(_full_matrix_37(encoded)),
        })
    floor_facts = []
    for index in range(N_FLOORS):
        rng_perm = np.random.default_rng(_seed(
            CELL_ID[code], KIND_ID["homo_floor_perm"],
            LANG_ID[language], index,
        ))
        values = real["kept_ids"].copy()
        rng_perm.shuffle(values)
        full = real["event_ids"].copy()
        full[real["kept_mask"]] = values
        floor_facts.append({
            "index": index,
            "profile": _profile_facts(
                _count_matrix_37(full, real["kept_mask"])
            ),
        })
    plaintext = _profile_facts(_stream_matrix_27(standing_truncated))
    tests = _search_free_envelope(real_profile, member_facts)
    outside = [key for key, test in tests.items() if not test["inside"]]
    verdict = (
        "shape-consistent-with-homophonic-encoding" if not outside
        else "shape-outside-analogues"
    )
    return {
        "stream_events": real["total_events"],
        "kept_pairs": int(real_matrix.sum()),
        "unmapped_events": (
            real["total_events"] - int(real["kept_mask"].sum())
        ),
        "real_profile": real_profile,
        "standing_plant_length": len(standing_truncated),
        "plants_at_source_identity": all(
            plant["profile"]["total_pairs"]
            == plant["plant_length"] - 1
            for plant in plant_facts
        ),
        "members_profiles": member_facts,
        "plants_profiles": plant_facts,
        "floors_profiles": floor_facts,
        "plaintext_profile": plaintext,
        "invariants": tests,
        "outside_invariants": outside,
        "verdict": verdict,
    }


def _compare_search_free_to_frozen() -> tuple[list[str], int]:
    """The declared bridge gate: every fact this instrument re-derives
    fresh that a frozen predecessor artifact already recorded must
    equal that stored value field for field before any profile is
    priced - the six cells' counted pairs, all 45 members' file,
    ebook and plant_length records, and the 30 floors' pair totals
    (each equal to its cell's counted pairs by the shuffle's
    structure). The plants' totals are not gate-anchored against a
    frozen scalar because the standing references' own truncated
    lengths were never stored frozen; they are verified inside every
    cell instead (each plant's total equal to its declared source
    length minus one). The band's selected-draw indexes are read from
    the frozen restart-budget artifact, not re-derived, because their
    re-derivation is machinery and this instrument contains none. Any
    divergence aborts with nothing written."""
    problems: list[str] = []
    fields = 0
    frozen = json.loads(RESTART_BUDGET_ARTIFACT_PATH.read_text())
    for code in FILES:
        real = _homo_real_stream(code)
        matrix = _count_matrix_37(real["event_ids"], real["kept_mask"])
        for language in LANGS:
            cell = frozen["files"][code][language]
            fields += 1
            if int(matrix.sum()) != cell["counted_pairs"]:
                problems.append(
                    f"streams/{code}/{language}: stored "
                    f"{cell['counted_pairs']} vs fresh "
                    f"{int(matrix.sum())}"
                )
            members = _extended_reference_members(language)
            for position in _extended_band_positions(language):
                stored = cell["band"][position]
                truncated = _truncated_reference(
                    code, language, file=members[position][0]
                )
                for key, value in (
                    ("file", members[position][0]),
                    ("ebook", members[position][1]),
                    ("plant_length", len(truncated)),
                ):
                    fields += 1
                    if stored[key] != value:
                        problems.append(
                            f"member/{code}/{language}/{position}/{key}:"
                            f" stored {stored[key]!r} vs fresh "
                            f"{value!r}"
                        )
            for index in range(N_FLOORS):
                rng_perm = np.random.default_rng(_seed(
                    CELL_ID[code], KIND_ID["homo_floor_perm"],
                    LANG_ID[language], index,
                ))
                values = real["kept_ids"].copy()
                rng_perm.shuffle(values)
                full = real["event_ids"].copy()
                full[real["kept_mask"]] = values
                total = int(
                    _count_matrix_37(
                        full, real["kept_mask"]
                    ).sum()
                )
                fields += 1
                if total != cell["counted_pairs"]:
                    problems.append(
                        f"floor/{code}/{language}/{index}: stored "
                        f"{cell['counted_pairs']} vs fresh {total}"
                    )
    return problems, fields


def substitution_homophonic_search_free() -> dict:
    """The declared search-free invariant instrument: the manuscript's
    raw pair-count profiles priced against the frozen widened band's
    selected-draw encodings, the plant encodings, the destroyed
    floors and the plaintext controls, with no assignment search
    anywhere in the instrument. The bridge gate runs first; any
    divergence aborts with nothing written."""
    problems, fields = _compare_search_free_to_frozen()
    if problems:
        raise AssertionError(
            "search-free bridge gate failed: " + "; ".join(problems)
        )
    artifact = {
        "what": "The declared search-free invariant instrument: the "
        "manuscript's raw pair-count profiles priced against the "
        "simulated homophonic encodings under the declared partition "
        "and encoder rule, the destroyed-adjacency floors and the "
        "plaintext controls, using only relabeling-invariant "
        "summaries of the pair matrices, so that no number here "
        "passes through any assignment search. The declared truthful "
        "question: do the manuscript's raw pair profiles sit inside "
        "the range of the simulated encodings on every declared "
        "invariant in every (file, language) cell, or is at least one "
        "invariant outside. No mapping is published; nothing here is "
        "a reading.",
        "declared": {
            "base_seed": BASE_SEED,
            "mapped": MAPPED_HOMO,
            "invariants": {
                "sorted_symbol_marginals": "the 37 symbol marginals "
                "(row sums) as a multiset, stored sorted descending as "
                "counts and as shares of the profile's own total, the "
                "two vector summaries envelope-tested by sorted "
                "position",
                "sorted_pair_multiset": "the 1369 pair counts as a "
                "multiset, stored sorted descending as counts and as "
                "shares of the profile's own total, envelope-tested "
                "by sorted position",
                "empty_type_count": "the number of the state space's "
                "pair types with zero counted occurrences, a scalar "
                "tested inside the band's [min, max] and recorded "
                "beside both totals because the count is tied to the "
                "profile's size",
                "self_pair_share": "the diagonal sum over the total",
                "top_k_shares": "the share of the total carried by "
                "the k largest pair counts, at the declared k values "
                "1, 10 and 50",
                "pair_entropy": "the natural entropy of the pair "
                "distribution over the 1369 types in nats per "
                "counted pair",
            },
            "state_note": "the real's profile prices its "
            "transcription's kept-adjacent mapped pairs (unmapped "
            "events break adjacency and are not counted), while an "
            "encoding's profile prices every adjacent pair of its "
            "full stream; the two totals are disclosed beside every "
            "cell and every share-valued invariant normalises by its "
            "own total; the empty type count is a raw count tied to "
            "its own total and its verdict position is recorded in "
            "that context; the latin band's members are the roster's "
            "own truncated texts (every member's total recorded with "
            "it), standing property of the roster disclosed in every "
            "prior artifact, so the latin envelopes are size-mixed "
            "by the roster's own declared construction",
            "machinery_rule": "this instrument contains no assignment "
            "search anywhere: no candidate evaluation, no restarts, "
            "no sweep cap, no convergence flags; the standing budgets "
            "are not applicable and no machinery recording appears "
            "for that reason",
            "split_rule": "no split applies: a profile uses every "
            "counted pair of its stream, the real's kept-adjacent "
            "structure and the encodings' full-stream structure; the "
            "climb and score halves of the band instruments have no "
            "counterpart here",
            "seed_kinds": "the declared encoding and floor kinds "
            "replay at their frozen positions: the members' selected "
            "draws through the homo_cross_enc kind at their member "
            "position, the plants through the homo_plant_enc kind at "
            "their index and the floors through the homo_floor_perm "
            "kind at their index; no new seed kind and no new "
            "position",
            "seed_sharing": "no machinery streams exist in this "
            "instrument and none are consumed; every encoding is a "
            "byte-identical replay of its declared frozen draw from "
            "the frozen widened band's and the standing cells' own "
            "seed kinds",
            "band_record_rule": "the simulated band is the frozen "
            "widened roster's 45 selected-draw encodings (7 english "
            "and 8 latin per language cell): each member's profile is "
            "its selected draw's encoding replayed through the "
            "declared encoder and partition, the selected draw read "
            "from the frozen artifact rather than re-derived because "
            "re-derivation is machinery; membership unconditional "
            "exactly as declared before",
            "plants_rule": "the 30 plant encodings (5 per cell, the "
            "standing first references through the declared partition "
            "and encoder at the standing kinds) recorded as the "
            "instrument's own simulated calibration set, each cell "
            "recording its standing source's truncated length (a "
            "fact the predecessors never stored frozen, disclosed as "
            "new here) and a plants_at_source_identity boolean "
            "checking every plant's total equals its source length "
            "minus one; no parity rule applies because there is no "
            "anchor geometry to exceed: the plant's profile is its "
            "own encoding's matrix",
            "floors_rule": "the 30 destroyed-adjacency floors "
            "recorded with their profiles; their declared role is the "
            "shuffled-structure control recorded beside the verdict, "
            "not part of any envelope",
            "plaintext_rule": "each cell records the truncated "
            "standing reference's own plaintext stream profile "
            "computed by the same formulas on its own 27-type state "
            "(729 types), as the prose control beside the verdict; "
            "its state width differs by declaration and it takes no "
            "part in any envelope",
            "verdict_rule": "declared strict-all: a cell is "
            "shape-consistent-with-homophonic-encoding only when "
            "every declared invariant of the real's profile sits "
            "inside the closed range of that cell's simulated band's "
            "profiles (the two vector summaries term by term inside "
            "the band's per-position envelope, the scalar summaries "
            "inside [min, max] at the stored 6-decimal rounding); "
            "any outside invariant makes the cell "
            "shape-outside-analogues, and every outside entry is "
            "recorded with its band range so the miss is audited not "
            "summarized",
            "closure_rule": "no scalar margin is formed: this "
            "instrument's question is inside or outside per "
            "invariant, and the recorded distances are the outside "
            "entries' band ranges themselves",
            "exclusion_rule": "the family's declared exclusion format "
            "is not re-scoped by this artifact: it keys to the "
            "declared 36-slot class under the inherited add-one form "
            "exactly as the held-out screen declared it, so a "
            "search-free verdict is structure evidence and the band "
            "instruments' verdicts stand untouched by this "
            "artifact's numbers",
            "bridge_gate": "before any profile is priced, every fact "
            "this instrument re-derives fresh that the frozen "
            "restart-budget artifact already recorded must equal that "
            "stored value field for field: the six cells' counted "
            "pairs, all 45 members' file, ebook and plant_length "
            "records, and the 30 floors' pair totals; the plants' "
            "totals are verified inside every cell instead because "
            "their standing source lengths were never stored frozen; "
            "the selected-draw indexes are read, not re-derived; any "
            "divergence aborts with nothing written",
            "corpus_source_rule": "no new corpus files and no new "
            "candidates: the band population is the frozen widened "
            "band's declared roster, the plants and plaintext "
            "controls are the standing references' frozen files, all "
            "stored raw with their markers and processed by the "
            "standing declared processing",
            "models_rule": "no score table is built or used: the "
            "instrument prices count structure only, so the standing "
            "add-one and leave-one-out tables play no part anywhere "
            "in this artifact",
            "corpus_facts": {},
        },
        "bridge_gate": {
            "status": "verified",
            "fields_compared": fields,
        },
        "files": {},
    }
    for code in FILES:
        cell = {}
        for language in LANGS:
            cell[language] = _search_free_cell_facts(code, language)
        artifact["files"][code] = cell
    return artifact


def main_search_free() -> None:
    artifact = substitution_homophonic_search_free()
    SEARCH_FREE_ARTIFACT_PATH.write_text(
        json.dumps(artifact, indent=2) + "\n"
    )
    print(SEARCH_FREE_ARTIFACT_PATH)


SEARCH_FREE_BM_ARTIFACT_PATH = (
    Path(DATA_DIR).resolve().parent.parent.parent
    / "docs" / "research-notes"
    / "voynich-homophonic-boundary-mark.json"
)


def _glyph_block_matrix(matrix: np.ndarray, mark_index: int) -> np.ndarray:
    """The glyph block of a 37 by 37 pair-count matrix: the word
    boundary mark's symbol's row and column removed from the state
    space, wherever that symbol sits in the matrix's alphabet (36 in
    every simulated encoding's alphabet; the real stream's own last
    mapped position). Every pair whose first or second symbol is the
    mark is removed and the state space keeps 1296 ordered types."""
    return np.delete(
        np.delete(matrix, mark_index, axis=0), mark_index, axis=1
    )


def _boundary_carried_pairs(matrix: np.ndarray, mark_index: int) -> int:
    """The pair counts this instrument's exclusion removes: the full
    matrix's total minus its glyph block's total, the boundary-carried
    pairs of any profile."""
    block = _glyph_block_matrix(matrix, mark_index)
    return int(round(matrix.sum())) - int(round(block.sum()))


def _search_free_bm_cell_facts(code: str, language: str) -> dict:
    """One cell's boundary-mark facts: the same replays the search-free
    instrument's cell facts replay (the real's kept-adjacent matrix,
    the band members' selected-draw encodings, the plants, the floors,
    the plaintext control), with one declared change - every profile
    is the mark-excluded block of its pair-count matrix (the word
    boundary mark's symbol's row and column removed, wherever that
    symbol sits in the matrix's own alphabet), so 1296 ordered types.
    The real and the floors carry the real stream's own mark position;
    the members' and plants' encodings carry their own alphabet's last
    position (symbol 36). The full width's total is recorded beside
    every profile for the gate's anchor against the frozen search-free
    artifact; the plaintext control's state is the reference letters
    alone (27 types, 729), which carries no boundary mark, so it is
    unchanged by the exclusion and recorded as such. No machinery
    anywhere."""
    frozen = json.loads(RESTART_BUDGET_ARTIFACT_PATH.read_text())
    stored_band = frozen["files"][code][language]["band"]
    real = _homo_real_stream(code)
    real_mark = len(real["mapped_chars"]) - 1
    real_matrix = _count_matrix_37(real["event_ids"], real["kept_mask"])
    real_profile = _profile_facts(
        _glyph_block_matrix(real_matrix, real_mark)
    )
    members = _extended_reference_members(language)
    member_facts = []
    for position in _extended_band_positions(language):
        name, ebook = members[position]
        truncated = _truncated_reference(code, language, file=name)
        groups = _partition_groups(truncated, MAPPED_HOMO)
        rng_enc = np.random.default_rng(_seed(
            CELL_ID[code], KIND_ID["homo_cross_enc"],
            LANG_ID[language], position,
        ))
        selected = stored_band[position]["selected_draw_index"]
        encoded: np.ndarray | None = None
        for _draw in range(selected + 1):
            encoded = _encode(truncated, groups, rng_enc, MAPPED_HOMO)
        full = _full_matrix_37(encoded)
        member_facts.append({
            "file": name,
            "ebook": ebook,
            "plant_length": len(truncated),
            "selected_draw_index": selected,
            "full_width_total_pairs": int(round(full.sum())),
            "profile": _profile_facts(
                _glyph_block_matrix(full, MAPPED_HOMO)
            ),
        })
    standing_truncated = _truncated_reference(code, language)
    standing_groups = _partition_groups(standing_truncated, MAPPED_HOMO)
    plant_facts = []
    for index in range(N_PLANTS):
        rng_enc = np.random.default_rng(_seed(
            CELL_ID[code], KIND_ID["homo_plant_enc"],
            LANG_ID[language], index,
        ))
        encoded = _encode(
            standing_truncated, standing_groups, rng_enc, MAPPED_HOMO
        )
        full = _full_matrix_37(encoded)
        plant_facts.append({
            "index": index,
            "plant_length": len(standing_truncated),
            "full_width_total_pairs": int(round(full.sum())),
            "profile": _profile_facts(
                _glyph_block_matrix(full, MAPPED_HOMO)
            ),
        })
    floor_facts = []
    for index in range(N_FLOORS):
        rng_perm = np.random.default_rng(_seed(
            CELL_ID[code], KIND_ID["homo_floor_perm"],
            LANG_ID[language], index,
        ))
        values = real["kept_ids"].copy()
        rng_perm.shuffle(values)
        full = real["event_ids"].copy()
        full[real["kept_mask"]] = values
        floor_full = _count_matrix_37(full, real["kept_mask"])
        floor_facts.append({
            "index": index,
            "full_width_total_pairs": int(round(floor_full.sum())),
            "profile": _profile_facts(
                _glyph_block_matrix(floor_full, real_mark)
            ),
        })
    plaintext = _profile_facts(_stream_matrix_27(standing_truncated))
    tests = _search_free_envelope(real_profile, member_facts)
    outside = [key for key, test in tests.items() if not test["inside"]]
    verdict = (
        "shape-consistent-with-homophonic-encoding" if not outside
        else "shape-outside-analogues"
    )
    return {
        "stream_events": real["total_events"],
        "kept_pairs": int(real_matrix.sum()),
        "unmapped_events": (
            real["total_events"] - int(real["kept_mask"].sum())
        ),
        "boundary_carried_pairs": _boundary_carried_pairs(
            real_matrix, real_mark
        ),
        "real_profile": real_profile,
        "real_full_width_total_pairs": int(real_matrix.sum()),
        "standing_plant_length": len(standing_truncated),
        "plants_at_source_identity": all(
            plant["full_width_total_pairs"]
            == plant["plant_length"] - 1
            for plant in plant_facts
        ),
        "members_profiles": member_facts,
        "plants_profiles": plant_facts,
        "floors_profiles": floor_facts,
        "plaintext_profile": plaintext,
        "invariants": tests,
        "outside_invariants": outside,
        "verdict": verdict,
    }


def _compare_search_free_bm_to_frozen() -> tuple[list[str], int]:
    """The declared bridge gate with two frozen sources: the
    restart-budget artifact's 171 anchor fields exactly as the
    search-free instrument declared them (the six cells' counted pairs,
    all 45 members' file, ebook and plant_length records, and the 30
    floors' pair totals), and the frozen search-free artifact's 117
    anchor fields: per cell, every full-width profile total this
    instrument re-derives from the same replays - the real's, each
    member's (7 english and 8 latin), each plant's (5), each floor's
    (5) and the plaintext control's (the 27-type state carries no
    boundary mark, so its profile is unchanged by declaration) - must
    equal the frozen search-free artifact's stored totals, so every
    glyph-block profile here is verified as the declared block of the
    same encodings that artifact measured. Any divergence aborts with
    nothing written."""
    problems, fields = _compare_search_free_to_frozen()
    frozen_sf = json.loads(SEARCH_FREE_ARTIFACT_PATH.read_text())
    for code in FILES:
        real = _homo_real_stream(code)
        real_total = int(
            _count_matrix_37(real["event_ids"], real["kept_mask"]).sum()
        )
        for language in LANGS:
            cell = frozen_sf["files"][code][language]
            fields += 1
            if real_total != cell["real_profile"]["total_pairs"]:
                problems.append(
                    f"real/{code}/{language}: stored "
                    f"{cell['real_profile']['total_pairs']} vs fresh "
                    f"{real_total}"
                )
            members = _extended_reference_members(language)
            for position in _extended_band_positions(language):
                name, _ebook = members[position]
                truncated = _truncated_reference(code, language, file=name)
                groups = _partition_groups(truncated, MAPPED_HOMO)
                rng_enc = np.random.default_rng(_seed(
                    CELL_ID[code], KIND_ID["homo_cross_enc"],
                    LANG_ID[language], position,
                ))
                selected = cell["members_profiles"][position][
                    "selected_draw_index"
                ]
                encoded: np.ndarray | None = None
                for _draw in range(selected + 1):
                    encoded = _encode(
                        truncated, groups, rng_enc, MAPPED_HOMO
                    )
                total = int(round(_full_matrix_37(encoded).sum()))
                stored = cell["members_profiles"][position]["profile"][
                    "total_pairs"
                ]
                fields += 1
                if total != stored:
                    problems.append(
                        f"member/{code}/{language}/{position}: stored "
                        f"{stored} vs fresh {total}"
                    )
            standing_truncated = _truncated_reference(code, language)
            standing_groups = _partition_groups(
                standing_truncated, MAPPED_HOMO
            )
            plaintext_total = int(round(
                _stream_matrix_27(standing_truncated).sum()
            ))
            fields += 1
            if plaintext_total != cell["plaintext_profile"]["total_pairs"]:
                problems.append(
                    f"plaintext/{code}/{language}: stored "
                    f"{cell['plaintext_profile']['total_pairs']} vs "
                    f"fresh {plaintext_total}"
                )
            for index in range(N_PLANTS):
                rng_enc = np.random.default_rng(_seed(
                    CELL_ID[code], KIND_ID["homo_plant_enc"],
                    LANG_ID[language], index,
                ))
                encoded = _encode(
                    standing_truncated, standing_groups, rng_enc,
                    MAPPED_HOMO,
                )
                total = int(round(_full_matrix_37(encoded).sum()))
                stored = cell["plants_profiles"][index]["profile"][
                    "total_pairs"
                ]
                fields += 1
                if total != stored:
                    problems.append(
                        f"plant/{code}/{language}/{index}: stored "
                        f"{stored} vs fresh {total}"
                    )
            for index in range(N_FLOORS):
                rng_perm = np.random.default_rng(_seed(
                    CELL_ID[code], KIND_ID["homo_floor_perm"],
                    LANG_ID[language], index,
                ))
                values = real["kept_ids"].copy()
                rng_perm.shuffle(values)
                full = real["event_ids"].copy()
                full[real["kept_mask"]] = values
                total = int(round(
                    _count_matrix_37(full, real["kept_mask"]).sum()
                ))
                stored = cell["floors_profiles"][index]["profile"][
                    "total_pairs"
                ]
                fields += 1
                if total != stored:
                    problems.append(
                        f"floor/{code}/{language}/{index}: stored "
                        f"{stored} vs fresh {total}"
                    )
    return problems, fields


def substitution_homophonic_boundary_mark() -> dict:
    """The declared boundary-mark re-instrument: the search-free
    invariant instrument re-run with the word-boundary mark's symbol
    excluded from every profile's state space on both sides. The
    bridge gate runs first; any divergence aborts with nothing
    written."""
    problems, fields = _compare_search_free_bm_to_frozen()
    if problems:
        raise AssertionError(
            "boundary-mark bridge gate failed: " + "; ".join(problems)
        )
    artifact = {
        "what": "The declared boundary-mark re-instrument: the "
        "search-free invariant instrument re-run with the "
        "word-boundary mark's symbol excluded from every profile's "
        "state space on both sides, the real's kept-adjacent pair "
        "matrix and every simulated encoding recomputed with the "
        "mark's row and column removed from the state space (1296 "
        "ordered types, boundary-carried pairs removed from both "
        "sides the same way), priced by the same six "
        "relabeling-invariant summaries under the same declared "
        "strict-all verdict rule, with no assignment search anywhere "
        "in the instrument. The declared truthful question: with the "
        "boundary mark excluded on both sides, do the manuscript's "
        "remaining raw pair profiles sit inside the range of the "
        "simulated encodings' remaining profiles on every declared "
        "invariant in every (file, language) cell, or is at least one "
        "invariant outside - the measured test of whether the "
        "search-free instrument's outsides ride the boundary mark's "
        "own concentration or the interior pair structure. No "
        "mapping is published; nothing here is a reading.",
        "declared": {
            "base_seed": BASE_SEED,
            "mapped": MAPPED_HOMO,
            "boundary_rule": "the word-boundary mark is each side's "
            "own mapped alphabet's last position (symbol 36 in every "
            "simulated encoding's alphabet, and the manuscript "
            "file's own last mapped position in the real's matrix), "
            "and its symbol's row and column are excluded from every "
            "profile's state space on both sides: every profile is "
            "the mark-excluded block of its pair-count matrix, 1296 "
            "ordered types, and every pair whose first or second "
            "symbol is the mark is removed from the real's "
            "kept-adjacent matrix and from every simulated encoding's "
            "full-stream matrix the same way; each profile records "
            "the full width's total beside its block facts so the "
            "removed carried mass is disclosed and gate-anchored, "
            "the real cell records boundary_carried_pairs (the full "
            "width minus the block) and real_full_width_total_pairs "
            "beside the excluded profile, and no boundary-adjusted "
            "marginal appears anywhere; the alphabet width is a "
            "standing disclosure: the ZL and GC real transcriptions "
            "rank to the full 36 glyph slots plus the mark, while "
            "the IT real transcription's glyph inventory holds only "
            "23 ranked glyph types plus the mark, so its mark sits "
            "at block position 23 and 13 of the block's 36 glyph "
            "slots are empty by alphabet width alone on the real "
            "side (the simulated encodings' alphabets are saturated "
            "at 36 in every cell), a width asymmetry the state note "
            "carries and the empty type count's interpretation "
            "rides with, disclosed to audit the miss not to hide "
            "it",
            "invariants": {
                "sorted_symbol_marginals": "the 36 mark-excluded "
                "glyph marginals (row sums of the mark-excluded "
                "block) as a multiset, stored sorted descending as "
                "counts and as shares of the profile's own "
                "glyph-pair total, the two vector summaries "
                "envelope-tested by sorted position over 36 "
                "positions",
                "sorted_pair_multiset": "the 1296 mark-excluded "
                "pair counts as a multiset, stored sorted "
                "descending as counts and as shares of the "
                "profile's own glyph-pair total, envelope-tested "
                "by sorted position",
                "empty_type_count": "the number of the block's "
                "mark-excluded pair types with zero counted "
                "occurrences, a scalar tested inside the band's "
                "[min, max] and recorded beside both totals because "
                "the count is tied to the profile's size; the IT "
                "real cells carry the alphabet-width asymmetry "
                "disclosed in the boundary rule",
                "self_pair_share": "the block's diagonal sum "
                "over the profile's glyph-pair total (the mark's "
                "own self-pair count rides in the removed carried "
                "mass)",
                "top_k_shares": "the share of the glyph-pair "
                "total carried by the k largest mark-excluded "
                "pair counts, at the declared k values 1, 10 "
                "and 50",
                "pair_entropy": "the natural entropy of the "
                "mark-excluded pair distribution over the 1296 "
                "types in nats per counted glyph pair",
            },
            "state_note": "every profile here is the mark-excluded "
            "block of the same pair-count matrix its search-free "
            "counterpart priced: the real's kept-adjacent mapped "
            "pairs and the encodings' full streams keep their "
            "structural difference, the two totals differ for that "
            "reason and every share-valued invariant normalises by "
            "its own glyph-pair total, while the empty type count is "
            "a raw count tied to its own total and recorded in that "
            "context; the boundary mark's exclusion is symmetric on "
            "both sides by declaration, the plaintext controls' "
            "state is the 27 reference letters alone (729 types), "
            "which carries no boundary mark, so each control is "
            "unchanged by the exclusion and its totals are "
            "gate-anchored against the frozen search-free artifact; "
            "the alphabet width disclosure rides on every real "
            "profile (the boundary rule sets it out: the IT real "
            "transcription ranks only 23 glyph types plus the mark, "
            "so 13 of its block's 36 glyph slots are empty by width "
            "alone while the simulated alphabets are saturated at "
            "36 in every cell); the latin band's members are the "
            "roster's own truncated texts whose totals range from "
            "45,490 to the full standing length, standing property "
            "of the roster disclosed in every prior artifact, so "
            "the latin envelopes are size-mixed by the roster's own "
            "declared construction",
            "machinery_rule": "this instrument contains no assignment "
            "search anywhere: no candidate evaluation, no restarts, "
            "no sweep cap, no convergence flags; the standing budgets "
            "are not applicable and no machinery recording appears "
            "for that reason",
            "split_rule": "no split applies: a profile uses every "
            "counted pair of its stream after the declared exclusion, "
            "the real's kept-adjacent glyph-glyph structure and the "
            "encodings' full-stream glyph-glyph structure; the climb "
            "and score halves of the band instruments have no "
            "counterpart here",
            "seed_kinds": "the declared encoding and floor kinds "
            "replay at their frozen positions exactly as the "
            "search-free instrument replayed them: the members' "
            "selected draws through the homo_cross_enc kind at their "
            "member position, the plants through the homo_plant_enc "
            "kind at their index and the floors through the "
            "homo_floor_perm kind at their index; no new seed kind "
            "and no new position",
            "seed_sharing": "no machinery streams exist in this "
            "instrument and none are consumed; every encoding is a "
            "byte-identical replay of its declared frozen draw, and "
            "each glyph-block profile is verified by the gate as the "
            "declared block of the same full-width encodings the "
            "frozen search-free artifact measured",
            "band_record_rule": "the simulated band is the frozen "
            "widened roster's 45 selected-draw encodings (7 english "
            "and 8 latin per language cell): each member's profile is "
            "its selected draw's encoding streaming through the "
            "declared encoder and partition, then reduced to its "
            "glyph block, the selected draw read from the frozen "
            "artifact rather than re-derived because re-derivation is "
            "machinery; membership unconditional exactly as declared "
            "before",
            "plants_rule": "the 30 plant encodings (5 per cell, the "
            "standing first references through the declared partition "
            "and encoder at the standing kinds) recorded as the "
            "instrument's own simulated calibration set, each "
            "reduced to its glyph block with the full width's total "
            "recorded beside it, each cell recording its standing "
            "source's truncated length and a "
            "plants_at_source_identity boolean checking every "
            "plant's full-width total equals its source length minus "
            "one; no parity rule applies because there is no anchor "
            "geometry to exceed: the plant's profile is its own "
            "encoding's glyph block",
            "floors_rule": "the 30 destroyed-adjacency floors "
            "recorded with their glyph-block profiles and their "
            "full-width totals; their declared role is the "
            "shuffled-structure control recorded beside the verdict, "
            "not part of any envelope",
            "plaintext_rule": "each cell records the truncated "
            "standing reference's own plaintext stream profile "
            "computed by the same formulas on its own 27-type state "
            "(729 types), as the prose control beside the verdict; "
            "the state carries no boundary mark, so the control is "
            "unchanged by the exclusion (every control's totals are "
            "gate-anchored against the frozen search-free artifact's "
            "stored controls); its state width differs by "
            "declaration and it takes no part in any envelope",
            "verdict_rule": "declared strict-all: a cell is "
            "shape-consistent-with-homophonic-encoding only when "
            "every declared invariant of the real's glyph-block "
            "profile sits inside the closed range of that cell's "
            "simulated band's glyph-block profiles (the two vector "
            "summaries term by term inside the band's per-position "
            "envelope over 36 sorted positions, the scalar summaries "
            "inside [min, max] at the stored 6-decimal rounding); "
            "any outside invariant makes the cell "
            "shape-outside-analogues, and every outside entry is "
            "recorded with its band range so the miss is audited not "
            "summarized",
            "closure_rule": "no scalar margin is formed: this "
            "instrument's question is inside or outside per "
            "invariant, and the recorded distances are the outside "
            "entries' band ranges themselves",
            "exclusion_rule": "the family's declared exclusion format "
            "is not re-scoped by this artifact: it keys to the "
            "declared 36-slot class under the inherited add-one form "
            "exactly as the held-out screen declared it, so a "
            "search-free verdict is structure evidence and the band "
            "instruments' verdicts stand untouched by this "
            "artifact's numbers",
            "bridge_gate": "before any profile is priced, every fact "
            "this instrument re-derives fresh that a frozen "
            "predecessor already recorded must equal that stored "
            "value field for field against two frozen sources: the "
            "restart-budget artifact's 171 anchor fields exactly as "
            "the search-free instrument declared them (the six "
            "cells' counted pairs, all 45 members' file, ebook and "
            "plant_length records, and the 30 floors' pair totals), "
            "and the frozen search-free artifact's 117 anchor fields "
            "(per cell: the full-width totals of the real, all 45 "
            "members, all 30 plants, all 30 floors and the 6 "
            "plaintext controls re-derived from the same byte-identical "
            "replays, every one equal to that artifact's stored "
            "totals); the plants' full-width identities are verified "
            "inside every cell as well (each plant's full-width "
            "total equals its declared source length minus one); "
            "the selected-draw indexes are read, not re-derived; any "
            "divergence aborts with nothing written",
            "corpus_source_rule": "no new corpus files and no new "
            "candidates: the band population is the frozen widened "
            "band's declared roster, the plants and plaintext "
            "controls are the standing references' frozen files, all "
            "stored raw with their markers and processed by the "
            "standing declared processing",
            "models_rule": "no score table is built or used: the "
            "instrument prices count structure only, so the standing "
            "add-one and leave-one-out tables play no part anywhere "
            "in this artifact",
            "corpus_facts": {},
        },
        "bridge_gate": {
            "status": "verified",
            "fields_compared": fields,
        },
        "files": {},
    }
    for code in FILES:
        cell = {}
        for language in LANGS:
            cell[language] = _search_free_bm_cell_facts(code, language)
        artifact["files"][code] = cell
    return artifact


def main_boundary_mark() -> None:
    artifact = substitution_homophonic_boundary_mark()
    SEARCH_FREE_BM_ARTIFACT_PATH.write_text(
        json.dumps(artifact, indent=2) + "\n"
    )
    print(SEARCH_FREE_BM_ARTIFACT_PATH)


# --------------------------------------------------------------------------
# The twelfth declared measurement: the corpus-breadth search-free
# instrument. Declared in the module docstring before any run beyond
# the probes it discloses.
# --------------------------------------------------------------------------

SEARCH_FREE_BREADTH_ARTIFACT_PATH = (
    Path(DATA_DIR).resolve().parent.parent.parent
    / "docs" / "research-notes"
    / "voynich-homophonic-corpus-breadth.json"
)

BREADTH_REFERENCE_FILES: dict[str, list[tuple[str, int, str]]] = {
    "english": [
        ("substref_english10_pg10.txt", 10,
         "The King James Version of the Bible"),
        ("substref_english11_pg829.txt", 829,
         "Gulliver's Travels (Swift)"),
        ("substref_english12_pg1041.txt", 1041,
         "Shakespeare's Sonnets"),
        ("substref_english13_pg1404.txt", 1404,
         "The Federalist Papers"),
        ("substref_english14_pg1228.txt", 1228,
         "On the Origin of Species (Darwin)"),
    ],
    "latin": [
        ("substref_latin11_pg227.txt", 227, "Aeneidos (Virgil)"),
        ("substref_latin12_pg18837.txt", 18837,
         "Commentarii de Bello Gallico, libri V-VIII (Caesar)"),
        ("substref_latin13_pg226.txt", 226, "Cicero's Orations"),
    ],
}

REJECTED_BREADTH_CANDIDATES: list[dict] = [
    {"ebook": 21765, "label": "The Metamorphoses of Ovid, Books I-VII",
     "cause": "an english translation carries the marker span (the "
     "header's declared Language English; 17,181 english common-word "
     "hits in every decile; mid-span in english: \"FABLE V. "
     "[IV.285-388]\")"},
    {"ebook": 14945, "label": "Cato Maior de Senectute with "
     "Introduction and Notes",
     "cause": "the editor's english school notes interleave through "
     "the span (3,916 common-word hits in every decile; mid-span in "
     "english: \"RECORDENTUR: this verb\")"},
    {"ebook": 16564, "label": "Amphitryo, Asinaria, Aulularia, "
     "Bacchides, Captivi (Plautus)",
     "cause": "a bilingual edition: the english render and notes "
     "interleave through the span (5,083 common-word hits in every "
     "decile; mid-span the translator's apparatus: \"footnotes are "
     "collected at the end of each play\")"},
    {"ebook": 20732, "label": "The Carmina of Caius Valerius Catullus",
     "cause": "a bilingual interleave: the english render interleaved "
     "with the latin through the span (4,330 common-word hits in "
     "every decile; the mid-span title page states the design: "
     "\"the carmina of caius valerius catullus now first completely "
     "englished into verse and prose\")"},
    {"ebook": 25861, "label": "Stories from Aulus Gellius",
     "cause": "an english reader's prose interleaved through the span "
     "(2,719 common-word hits; mid-span in english: \"5. The doe used "
     "to converse with Sertorius and advise him.\")"},
    {"ebook": 20771, "label": "Species Plantarum, Sections I-III "
     "(Linnaeus)",
     "cause": "the english head-and-trailing scaffolding totals 54 "
     "common-word hits against the standing transcriber-note scale's "
     "0 to 52 (16 head and 38 trailing, no mid-span hits), so the "
     "declared bar rejects it: the roster's scale letter is not "
     "widened by this roster"},
    {"ebook": 63139, "label": "Fratris Felicis Fabri Evagatorium in "
     "Terrae Sanctae, Arabiae et Egypti Peregrinationem. Volumen "
     "Tertium",
     "cause": "the english scaffolding totals 55 common-word hits "
     "against the standing transcriber-note scale's 0 to 52 (7 head "
     "and 48 in a trailing english block, no mid-span hits), the "
     "declared bar again; also the same printed travel account's "
     "third volume, both facts declared"},
    {"ebook": 19635, "label": "Biblia Sacra Vulgata - Psalmi XXII",
     "cause": "not accessible at the declared fetch source: the cache "
     "returned the 404 page again this run (the standing record's "
     "cause from the sixth measurement, reproduced)"},
]

BREADTH_EXTRA_NOT_SELECTED: list[dict] = [
    {"ebook": 3207, "label": "Leviathan (Hobbes)", "stream_total": 1162350},
    {"ebook": 148, "label": "The Autobiography of Benjamin Franklin",
     "stream_total": 365244},
]

BREADTH_ROSTER_FLOOR_STREAM = 45491


def _breadth_reference_members(language: str) -> list[tuple[str, int]]:
    """The corpus-breadth band's member texts: the standing widened
    list first, then the breadth members declared above."""
    return (
        [_extended_reference_members(language)[position]
         for position in _extended_band_positions(language)]
        + [(name, ebook) for name, ebook, _label in
           BREADTH_REFERENCE_FILES[language]]
    )


def _breadth_band_positions(language: str) -> tuple[int, ...]:
    """The corpus-breadth band's positions."""
    return tuple(range(len(_breadth_reference_members(language))))


def _breadth_cell_facts(code: str, language: str) -> dict:
    """One cell's corpus-breadth facts: the boundary-mark
    re-instrument's same cell replays (the real's kept-adjacent matrix
    reduced to its mark-excluded block, the standing widened band's
    members through their frozen selected draws, the plants, the
    floors, the plaintext control) with the band population extended
    by the declared breadth members at their listed positions: each
    breadth member's profile comes from draw 0 of the declared
    homo_cross_enc kind at that position, the stream's first encoding,
    declared in advance with no selection performed. Every profile is
    the mark-excluded glyph block exactly as the boundary-mark
    instrument declared it. No machinery anywhere in the instrument."""
    frozen = json.loads(RESTART_BUDGET_ARTIFACT_PATH.read_text())
    stored_band = frozen["files"][code][language]["band"]
    standing_count = len(_extended_reference_members(language))
    real = _homo_real_stream(code)
    real_mark = len(real["mapped_chars"]) - 1
    real_matrix = _count_matrix_37(real["event_ids"], real["kept_mask"])
    real_profile = _profile_facts(
        _glyph_block_matrix(real_matrix, real_mark)
    )
    members = _breadth_reference_members(language)
    member_facts = []
    for position in _breadth_band_positions(language):
        name, ebook = members[position]
        truncated = _truncated_reference(code, language, file=name)
        groups = _partition_groups(truncated, MAPPED_HOMO)
        rng_enc = np.random.default_rng(_seed(
            CELL_ID[code], KIND_ID["homo_cross_enc"],
            LANG_ID[language], position,
        ))
        if position < standing_count:
            selected = stored_band[position]["selected_draw_index"]
            encoded: np.ndarray | None = None
            for _draw in range(selected + 1):
                encoded = _encode(
                    truncated, groups, rng_enc, MAPPED_HOMO
                )
            draws_rule = "standing_frozen_selected"
            draws_value: int = selected
        else:
            encoded = _encode(
                truncated, groups, rng_enc, MAPPED_HOMO
            )
            draws_rule = "breadth_declared_draw_0"
            draws_value = 0
        full = _full_matrix_37(encoded)
        member_facts.append({
            "file": name,
            "ebook": ebook,
            "plant_length": len(truncated),
            "selected_draw_index": draws_value,
            "draw_rule": draws_rule,
            "full_width_total_pairs": int(round(full.sum())),
            "profile": _profile_facts(
                _glyph_block_matrix(full, MAPPED_HOMO)
            ),
        })
    standing_truncated = _truncated_reference(code, language)
    standing_groups = _partition_groups(standing_truncated, MAPPED_HOMO)
    plant_facts = []
    for index in range(N_PLANTS):
        rng_enc = np.random.default_rng(_seed(
            CELL_ID[code], KIND_ID["homo_plant_enc"],
            LANG_ID[language], index,
        ))
        encoded = _encode(
            standing_truncated, standing_groups, rng_enc, MAPPED_HOMO
        )
        full = _full_matrix_37(encoded)
        plant_facts.append({
            "index": index,
            "plant_length": len(standing_truncated),
            "full_width_total_pairs": int(round(full.sum())),
            "profile": _profile_facts(
                _glyph_block_matrix(full, MAPPED_HOMO)
            ),
        })
    floor_facts = []
    for index in range(N_FLOORS):
        rng_perm = np.random.default_rng(_seed(
            CELL_ID[code], KIND_ID["homo_floor_perm"],
            LANG_ID[language], index,
        ))
        values = real["kept_ids"].copy()
        rng_perm.shuffle(values)
        full = real["event_ids"].copy()
        full[real["kept_mask"]] = values
        floor_full = _count_matrix_37(full, real["kept_mask"])
        floor_facts.append({
            "index": index,
            "full_width_total_pairs": int(round(floor_full.sum())),
            "profile": _profile_facts(
                _glyph_block_matrix(floor_full, real_mark)
            ),
        })
    plaintext = _profile_facts(_stream_matrix_27(standing_truncated))
    tests = _search_free_envelope(real_profile, member_facts)
    outside = [key for key, test in tests.items() if not test["inside"]]
    verdict = (
        "shape-consistent-with-homophonic-encoding" if not outside
        else "shape-outside-analogues"
    )
    return {
        "stream_events": real["total_events"],
        "kept_pairs": int(real_matrix.sum()),
        "unmapped_events": (
            real["total_events"] - int(real["kept_mask"].sum())
        ),
        "boundary_carried_pairs": _boundary_carried_pairs(
            real_matrix, real_mark
        ),
        "real_profile": real_profile,
        "real_full_width_total_pairs": int(real_matrix.sum()),
        "standing_plant_length": len(standing_truncated),
        "plants_at_source_identity": all(
            plant["full_width_total_pairs"]
            == plant["plant_length"] - 1
            for plant in plant_facts
        ),
        "members_profiles": member_facts,
        "plants_profiles": plant_facts,
        "floors_profiles": floor_facts,
        "plaintext_profile": plaintext,
        "invariants": tests,
        "outside_invariants": outside,
        "verdict": verdict,
    }


def _breadth_member_row(
    code: str, language: str, position: int,
    standing_count: int,
) -> dict:
    """One corpus-breadth member's full-width encoding row: the
    standing positions through their frozen selected draws, the
    breadth positions through the declared draw 0 rule."""
    members = _breadth_reference_members(language)
    name, ebook = members[position]
    truncated = _truncated_reference(code, language, file=name)
    groups = _partition_groups(truncated, MAPPED_HOMO)
    rng_enc = np.random.default_rng(_seed(
        CELL_ID[code], KIND_ID["homo_cross_enc"],
        LANG_ID[language], position,
    ))
    if position < standing_count:
        stored = json.loads(
            RESTART_BUDGET_ARTIFACT_PATH.read_text()
        )["files"][code][language]["band"][position]
        selected = stored["selected_draw_index"]
        encoded: np.ndarray | None = None
        for _draw in range(selected + 1):
            encoded = _encode(truncated, groups, rng_enc, MAPPED_HOMO)
        draws_rule = "standing_frozen_selected"
        draws_value: int = selected
    else:
        encoded = _encode(truncated, groups, rng_enc, MAPPED_HOMO)
        draws_rule = "breadth_declared_draw_0"
        draws_value = 0
    full = _full_matrix_37(encoded)
    return {
        "file": name,
        "ebook": ebook,
        "plant_length": len(truncated),
        "selected_draw_index": draws_value,
        "draw_rule": draws_rule,
        "full_width_total_pairs": int(round(full.sum())),
        "profile": _profile_facts(
            _glyph_block_matrix(full, MAPPED_HOMO)
        ),
    }


def _compare_breadth_to_frozen() -> tuple[list[str], int]:
    """The declared bridge gate, two frozen sources first and the
    standing profiles verified beside them: the boundary-mark
    instrument's 288 anchor fields exactly as that instrument declared
    them (the restart-budget artifact's 171 anchors and the frozen
    search-free artifact's 117 full-width totals), then per cell the
    standing rows' mark-excluded profiles verified as dict-equal
    replays against the frozen boundary-mark artifact's stored rows
    (each standing member's file, ebook, plant_length, selected_draw
    index, full-width total and profile; each plant's profile; each
    floor's profile; each plaintext control's profile), 111 profile
    checks total (18 per english cell times 3 cells, 19 per latin cell
    times 3 cells). The breadth members carry no frozen counterpart:
    their encodings take the declared draw 0 rule and their facts are
    recorded as declared corpus facts with sha256 records in the
    artifact. Any divergence aborts with nothing written."""
    problems, fields = _compare_search_free_bm_to_frozen()
    frozen_bm = json.loads(SEARCH_FREE_BM_ARTIFACT_PATH.read_text())
    for code in FILES:
        for language in LANGS:
            stored_cell = frozen_bm["files"][code][language]
            members = _breadth_reference_members(language)
            standing_count = len(_extended_reference_members(language))
            for position, stored_row in enumerate(
                stored_cell["members_profiles"]
            ):
                if len(members) <= position:
                    problems.append(
                        f"member roster short at "
                        f"{code}/{language}/{position}"
                    )
                    continue
                fresh_row = _breadth_member_row(
                    code, language, position, standing_count
                )
                fields += 1
                differing = [
                    key for key in stored_row
                    if fresh_row.get(key) != stored_row[key]
                ]
                if differing:
                    problems.append(
                        f"member/{code}/{language}/{position}: the "
                        f"standing row's replay does not equal the "
                        f"stored boundary-mark row ({', '.join(differing)})"
                    )
            real = _homo_real_stream(code)
            real_mark = len(real["mapped_chars"]) - 1
            standing_truncated = _truncated_reference(code, language)
            standing_groups = _partition_groups(
                standing_truncated, MAPPED_HOMO
            )
            for index, stored_row in enumerate(
                stored_cell["plants_profiles"]
            ):
                rng_enc = np.random.default_rng(_seed(
                    CELL_ID[code], KIND_ID["homo_plant_enc"],
                    LANG_ID[language], index,
                ))
                encoded = _encode(
                    standing_truncated, standing_groups, rng_enc,
                    MAPPED_HOMO,
                )
                fresh_profile = _profile_facts(_glyph_block_matrix(
                    _full_matrix_37(encoded), MAPPED_HOMO
                ))
                fields += 1
                if fresh_profile != stored_row["profile"]:
                    problems.append(
                        f"plant/{code}/{language}/{index}: the block "
                        f"profile's replay does not equal the stored "
                        f"boundary-mark profile"
                    )
            for index, stored_row in enumerate(
                stored_cell["floors_profiles"]
            ):
                rng_perm = np.random.default_rng(_seed(
                    CELL_ID[code], KIND_ID["homo_floor_perm"],
                    LANG_ID[language], index,
                ))
                values = real["kept_ids"].copy()
                rng_perm.shuffle(values)
                full = real["event_ids"].copy()
                full[real["kept_mask"]] = values
                fresh_profile = _profile_facts(_glyph_block_matrix(
                    _count_matrix_37(full, real["kept_mask"]),
                    real_mark,
                ))
                fields += 1
                if fresh_profile != stored_row["profile"]:
                    problems.append(
                        f"floor/{code}/{language}/{index}: the block "
                        f"profile's replay does not equal the stored "
                        f"boundary-mark profile"
                    )
            fresh_plaintext = _profile_facts(
                _stream_matrix_27(standing_truncated)
            )
            fields += 1
            if fresh_plaintext != stored_cell["plaintext_profile"]:
                problems.append(
                    f"plaintext/{code}/{language}: the control's "
                    f"profile does not equal the stored boundary-mark "
                    f"profile"
                )
    return problems, fields


def substitution_homophonic_corpus_breadth() -> dict:
    """The declared corpus-breadth search-free instrument: the
    boundary-mark re-instrument's state space and summaries against a
    band population widened across the declared corpus breadth. The
    bridge gate runs first; any divergence aborts with nothing
    written."""
    problems, fields = _compare_breadth_to_frozen()
    if problems:
        raise AssertionError(
            "corpus-breadth bridge gate failed: " + "; ".join(problems)
        )
    accepted_facts = []
    for language in LANGS:
        for name, ebook, label in BREADTH_REFERENCE_FILES[language]:
            path = (Path(DATA_DIR).resolve().parent / name)
            text = path.read_text(encoding="utf-8", errors="replace")
            start = text.find("START OF THE PROJECT GUTENBERG")
            end = text.find("END OF THE PROJECT GUTENBERG")
            body = text[start + len("START OF THE PROJECT GUTENBERG"):end]
            stream = _reference_stream(language, file=name)
            letters = sum(1 for value in stream if value != 26)
            accepted_facts.append({
                "file": name,
                "ebook": ebook,
                "label": label,
                "language": language,
                "sha256": hashlib.sha256(
                    path.read_bytes()
                ).hexdigest(),
                "file_bytes": len(path.read_bytes()),
                "body_bytes": len(body),
                "stream_total": len(stream),
                "letters": letters,
                "boundary": len(stream) - letters,
                "types_present": len(set(stream)),
            })
    artifact = {
        "what": "The declared corpus-breadth search-free instrument: "
        "the boundary-mark re-instrument's same six relabeling-invariant "
        "summaries over the same mark-excluded state space (1296 "
        "ordered types, the boundary mark's row and column excluded on "
        "both sides exactly as declared there), recomputed against a "
        "band population widened across the declared corpus breadth "
        "(twelve english and eleven latin members per cell, the "
        "standing roster replayed byte-identically and extended by the "
        "declared breadth members frozen under the standing corpus "
        "rules), priced under the same declared strict-all verdict "
        "rule with no assignment search anywhere in the instrument. "
        "The declared truthful question: with the band population "
        "widened across the corpus breadth under the declared draw "
        "rules, does the real's mark-excluded profile sit inside the "
        "extended band's range on every declared invariant in every "
        "(file, language) cell, or is at least one invariant outside - "
        "the measured test of whether the interior's separation holds "
        "as the roster grows. No mapping is published; nothing here is "
        "a reading.",
        "declared": {
            "base_seed": BASE_SEED,
            "mapped": MAPPED_HOMO,
            "boundary_rule": "the word-boundary mark's row and column "
            "are excluded from every profile's state space on both "
            "sides exactly as the boundary-mark re-instrument declared: "
            "every profile is the mark-excluded block of its "
            "pair-count matrix, 1296 ordered types, the mark located in "
            "each matrix's own alphabet (symbol 36 in every simulated "
            "encoding and the real file's own last mapped position), "
            "the full width's total recorded beside every block "
            "profile, and no boundary-adjusted marginal appears "
            "anywhere; the standing alphabet-width disclosure carries "
            "unchanged (the IT real transcription ranks only 23 glyph "
            "types plus the mark, so 13 of its block's 36 glyph slots "
            "are empty by width alone on the real side while the "
            "simulated alphabets are saturated at 36 in every cell)",
            "corpus_breadth_rule": "the band population widens across "
            "the declared corpus breadth: five declared english slots "
            "(an early modern scriptural register, an eighteenth "
            "century satirical prose register, a verse register, a "
            "civic polemical register and a scientific non-fiction "
            "register) and three declared latin slots (classical epic "
            "verse, classical prose history and classical oratory), "
            "each filled by the declared roster's accepted candidates: "
            "ebook 10 the King James Version of the Bible, ebook 829 "
            "Gulliver's Travels (Swift), ebook 1041 Shakespeare's "
            "Sonnets, ebook 1404 The Federalist Papers, ebook 1228 On "
            "the Origin of Species (Darwin); ebook 227 Aeneidos "
            "(Virgil), ebook 18837 Commentarii de Bello Gallico, libri "
            "V-VIII (Caesar), ebook 226 Cicero's Orations; the "
            "standing roster replays first, the breadth members take "
            "the listed positions english 7 to 11 and latin 8 to 10, "
            "the declared homo_cross_enc kind's position axis extends, "
            "no new seed kind; each breadth member's processed stream "
            "must reach the standing roster's smallest member stream "
            "length (45,491 tokens, Vulgata Esther) and every accepted "
            "candidate clears that floor",
            "corpus_source_rule": "the corpus discipline stands: each "
            "candidate fetched from the standing members' plain text "
            "source at the declared cache form, each accepted file "
            "stored raw with its Gutenberg markers and processed by "
            "the standing declared processing with no new step, a "
            "sha256 recorded for every accepted file, candidates "
            "probed in their marker spans before acceptance (the "
            "english common-word probe over the body in deciles with "
            "their head-and-trailing structure read, the processed "
            "stream through the declared loader, and mid-span samples "
            "read); the standing fetch verification was rehearsed: the "
            "cache serves the standing english2 marker span "
            "byte-identical (447,911 bytes, span sha256 "
            "7f95a6c0484513216cffa7d9e1e0314896faa21cb5a713d65c125a86f"
            "1f43695) at the same byte counts, with a two-line title "
            "capitalization drift upstream in the header metadata "
            "(the modern prometheus to The modern Prometheus, bytes "
            "49, 60, 555 and 566), recorded as metadata drift the "
            "marker span does not carry; the rejected candidates and "
            "their causes are recorded verbatim in "
            "rejected_breadth_candidates; two further english "
            "candidates probed clean and not selected by the roster's "
            "declared five-slot design (ebook 3207 Leviathan, ebook "
            "148 The Autobiography of Benjamin Franklin); the "
            "acceptance bar is the standing scale in every respect: "
            "no english translation, gloss or apparatus interleaved "
            "through the body, and the english scaffolding totals "
            "inside the standing transcriber-note scale's 0 to 52 "
            "common-word hits",
            "invariants": {
                "sorted_symbol_marginals": "the 36 mark-excluded "
                "glyph marginals as a multiset, stored sorted "
                "descending as counts and shares, envelope-tested by "
                "sorted position over 36 positions",
                "sorted_pair_multiset": "the 1296 mark-excluded pair "
                "counts as a multiset, stored sorted descending as "
                "counts and shares, envelope-tested by sorted "
                "position",
                "empty_type_count": "the number of the block's "
                "mark-excluded pair types with zero counted "
                "occurrences, a scalar inside [min, max]",
                "self_pair_share": "the block's diagonal sum over the "
                "profile's glyph-pair total",
                "top_k_shares": "the share of the glyph-pair total "
                "carried by the k largest pair counts, at k 1, 10 "
                "and 50",
                "pair_entropy": "the natural entropy of the "
                "mark-excluded pair distribution in nats per counted "
                "glyph pair",
            },
            "state_note": "every profile here is the mark-excluded "
            "block of the same pair-count matrices the boundary-mark "
            "instrument priced: the real's kept-adjacent pairs and the "
            "encodings' full streams keep their structural "
            "difference, every share-valued invariant normalises by "
            "its own glyph-pair total, and the empty type count is a "
            "raw count tied to its own total and recorded in that "
            "context; the plaintext control's state is the 27 "
            "reference letters alone (729 types, no boundary mark) "
            "and takes no part in any envelope; the latin envelopes "
            "are size-mixed by the roster's own declared construction "
            "(the roster's member streams run 45,491 tokens upward), "
            "and the breadth members' declared draw-0 sources sit "
            "beside the standing members' frozen selected draws by "
            "declaration",
            "machinery_rule": "this instrument contains no assignment "
            "search anywhere: no candidate evaluation, no restarts, "
            "no sweep cap, no convergence flags; the standing budgets "
            "are not applicable and no machinery recording appears "
            "for that reason",
            "split_rule": "no split applies: a profile uses every "
            "counted pair of its stream after the declared exclusion; "
            "the climb and score halves of the band instruments have "
            "no counterpart here",
            "seed_kinds": "the standing encoding and floor kinds "
            "replay at their frozen positions exactly as every "
            "predecessor declared, and the homo_cross_enc kind's "
            "position axis extends to the breadth members' listed "
            "positions (english 7 to 11, latin 8 to 10); no new seed "
            "kind is consumed",
            "seed_sharing": "the standing members' encodings are "
            "byte-identical replays of their declared frozen draws "
            "with the selected draw read from the frozen restart "
            "artifact rather than re-derived; the breadth members' "
            "encodings take the stream's first draw at their listed "
            "positions, declared in advance with no selection "
            "performed; every block profile of every row is verified "
            "by the gate as the declared block of its own replayed "
            "encoding",
            "band_record_rule": "the simulated band per language cell "
            "is the standing widened roster's selected-draw encodings "
            "(7 english and 8 latin members) plus the declared "
            "breadth members' draw-0 encodings (5 english and 3 "
            "latin), so 12 english and 11 latin member profiles per "
            "cell: each standing member's row carries its frozen "
            "selected_draw_index and the breadth rows carry the "
            "declared draw-0 marker, membership unconditional exactly "
            "as declared before",
            "plants_rule": "the 30 plant encodings (5 per cell, the "
            "standing first references at the standing kinds) "
            "recorded as the instrument's own simulated calibration "
            "set, each reduced to its glyph block with the full "
            "width's total beside it, each cell recording its standing "
            "source's truncated length and the "
            "plants_at_source_identity boolean; no parity rule "
            "applies because there is no anchor geometry to exceed",
            "floors_rule": "the 30 destroyed-adjacency floors "
            "recorded with their glyph-block profiles and their "
            "full-width totals; their declared role is the "
            "shuffled-structure control recorded beside the verdict, "
            "not part of any envelope",
            "plaintext_rule": "each cell records the truncated "
            "standing reference's own plaintext stream profile "
            "computed by the same formulas on its own 27-type state "
            "(729 types), as the prose control beside the verdict; "
            "the state carries no boundary mark and takes no part in "
            "any envelope",
            "verdict_rule": "declared strict-all: a cell is "
            "shape-consistent-with-homophonic-encoding only when "
            "every declared invariant of the real's glyph-block "
            "profile sits inside the closed range of that cell's "
            "widened band's glyph-block profiles (the two vector "
            "summaries term by term inside the band's per-position "
            "envelope over 36 sorted positions, the scalar summaries "
            "inside [min, max] at the stored 6-decimal rounding); any "
            "outside invariant makes the cell "
            "shape-outside-analogues, and every outside entry is "
            "recorded with its band range so the miss is audited not "
            "summarized",
            "closure_rule": "no scalar margin is formed: this "
            "instrument's question is inside or outside per "
            "invariant, and the recorded distances are the outside "
            "entries' band ranges themselves",
            "exclusion_rule": "the family's declared exclusion format "
            "is not re-scoped by this artifact: it keys to the "
            "declared 36-slot class under the inherited add-one form "
            "exactly as the held-out screen declared it, so a "
            "search-free verdict is structure evidence and the band "
            "instruments' verdicts stand untouched by this "
            "artifact's numbers",
            "bridge_gate": "before any profile is priced, every fact "
            "this instrument re-derives fresh that a frozen "
            "predecessor already recorded must equal that stored "
            "value field for field: the boundary-mark instrument's "
            "288 anchor fields exactly as that instrument declared "
            "them (the restart-budget artifact's 171 anchors and the "
            "frozen search-free artifact's 117 full-width totals), "
            "then per cell the standing rows' mark-excluded profiles "
            "verified as replay-equal against the frozen "
            "boundary-mark artifact's stored rows: each standing "
            "member's file, ebook, plant_length, selected_draw_index, "
            "full-width total and block profile, each plant's block "
            "profile, each floor's block profile and each plaintext "
            "control's profile, 111 profile checks total (18 per "
            "english cell and 19 per latin cell times 3 files); the "
            "breadth members carry no frozen counterpart, their "
            "encodings take the declared draw-0 rule and their facts "
            "ride on the declared roster with sha256 records; any "
            "divergence aborts with nothing written",
            "models_rule": "no score table is built or used: the "
            "instrument prices count structure only, so the standing "
            "add-one and leave-one-out tables play no part anywhere "
            "in this artifact",
            "corpus_facts": {
                "fetch_verification": {
                    "standing_file": "substref_english2_pg84.txt",
                    "frozen_sha256": "7810cd483cffcf2cc8a1d8f0d5807931"
                    "e69d4f48cd14149b8c76f88af82fead3",
                    "fresh_sha256": "2b97b7f8aad508649481d8dd4f6b54f9b"
                    "965ddb3ba634e9151c815f537b49e42",
                    "file_bytes": 448885,
                    "marker_span_sha256": "7f95a6c0484513216cffa7d9e1e"
                    "0314896faa21cb5a713d65c125a86f1f43695",
                    "drift": "the cache's header metadata drifted "
                    "upstream in the title line's capitalization "
                    "(the modern prometheus to The modern Prometheus, "
                    "differing bytes at positions 49, 60, 555 and 566 "
                    "before the START marker); the marker span is "
                    "byte-identical, so every declared processing "
                    "output of the standing freeze is unchanged",
                },
                "accepted": accepted_facts,
                "rejected_breadth_candidates": REJECTED_BREADTH_CANDIDATES,
                "extras_not_selected": BREADTH_EXTRA_NOT_SELECTED,
                "roster_floor_stream": BREADTH_ROSTER_FLOOR_STREAM,
            },
        },
        "bridge_gate": {
            "status": "verified",
            "fields_compared": fields,
            "anchor_fields": 288,
            "profile_equality_checks": fields - 288,
        },
        "files": {},
    }
    for code in FILES:
        cell = {}
        for language in LANGS:
            cell[language] = _breadth_cell_facts(code, language)
        artifact["files"][code] = cell
    return artifact


def main_corpus_breadth() -> None:
    artifact = substitution_homophonic_corpus_breadth()
    SEARCH_FREE_BREADTH_ARTIFACT_PATH.write_text(
        json.dumps(artifact, indent=2) + "\n"
    )
    print(SEARCH_FREE_BREADTH_ARTIFACT_PATH)


# --------------------------------------------------------------------------
# The thirteenth declared measurement: the matched-truncation
# interior-shape instrument. Declared in the module docstring before
# any run beyond the probes it discloses.
# --------------------------------------------------------------------------

SEARCH_FREE_MATCHED_ARTIFACT_PATH = (
    Path(DATA_DIR).resolve().parent.parent.parent
    / "docs" / "research-notes"
    / "voynich-homophonic-matched-truncation.json"
)

MATCHED_REAL_RECORD_KEYS = (
    "stream_events",
    "kept_pairs",
    "unmapped_events",
    "boundary_carried_pairs",
    "real_profile",
    "real_full_width_total_pairs",
    "standing_plant_length",
    "plants_at_source_identity",
)


def _compare_matched_to_frozen() -> tuple[list[str], int]:
    """The declared bridge gate, three frozen sources first and the
    frozen roster's own rows verified beside them: the corpus-breadth
    instrument's 399 anchor fields exactly as that instrument declared
    them (the boundary-mark gate's 288 anchors and the 111 standing
    profile checks), then per cell the frozen corpus-breadth rows
    verified where fresh re-derivations replay them: each member row
    (file, ebook, plant_length, selected_draw_index, draw_rule,
    full-width total and block profile) replayed through its declared
    chain, each plant row (index, plant_length, standing full-width
    total and block profile), each floor row (index, full-width total
    and block profile), each plaintext control's standing profile, and
    each cell's real record's eight declared fields, 24 row checks per
    english cell and 23 per latin cell, 141 row checks total. The
    matched facts carry no frozen counterpart and ride on the declared
    roster. Any divergence aborts with nothing written."""
    problems, fields = _compare_breadth_to_frozen()
    frozen = json.loads(SEARCH_FREE_BREADTH_ARTIFACT_PATH.read_text())
    for code in FILES:
        for language in LANGS:
            stored_cell = frozen["files"][code][language]
            members = _breadth_reference_members(language)
            standing_count = len(_extended_reference_members(language))
            for position, stored_row in enumerate(
                stored_cell["members_profiles"]
            ):
                if len(members) <= position:
                    problems.append(
                        f"member roster short at "
                        f"{code}/{language}/{position}"
                    )
                    continue
                fresh_row = _breadth_member_row(
                    code, language, position, standing_count
                )
                fields += 1
                differing = [
                    key for key in sorted(
                        set(fresh_row) | set(stored_row)
                    )
                    if fresh_row.get(key) != stored_row.get(key)
                ]
                if differing:
                    problems.append(
                        f"member/{code}/{language}/{position}: the "
                        f"standing row's replay does not equal the "
                        f"stored corpus-breadth row ({', '.join(differing)})"
                    )
            real = _homo_real_stream(code)
            real_mark = len(real["mapped_chars"]) - 1
            real_matrix = _count_matrix_37(real["event_ids"], real["kept_mask"])
            standing_truncated = _truncated_reference(code, language)
            standing_groups = _partition_groups(
                standing_truncated, MAPPED_HOMO
            )
            fresh_plants: list[dict] = []
            for index, stored_row in enumerate(
                stored_cell["plants_profiles"]
            ):
                rng_enc = np.random.default_rng(_seed(
                    CELL_ID[code], KIND_ID["homo_plant_enc"],
                    LANG_ID[language], index,
                ))
                encoded = _encode(
                    standing_truncated, standing_groups, rng_enc,
                    MAPPED_HOMO,
                )
                full = _full_matrix_37(encoded)
                fresh_row = {
                    "index": index,
                    "plant_length": len(standing_truncated),
                    "full_width_total_pairs": int(round(full.sum())),
                    "profile": _profile_facts(_glyph_block_matrix(
                        full, MAPPED_HOMO
                    )),
                }
                fresh_plants.append(fresh_row)
                fields += 1
                differing = [
                    key for key in sorted(
                        set(fresh_row) | set(stored_row)
                    )
                    if fresh_row.get(key) != stored_row.get(key)
                ]
                if differing:
                    problems.append(
                        f"plant/{code}/{language}/{index}: the "
                        f"standing row's replay does not equal the "
                        f"stored corpus-breadth row ({', '.join(differing)})"
                    )
            for index, stored_row in enumerate(
                stored_cell["floors_profiles"]
            ):
                rng_perm = np.random.default_rng(_seed(
                    CELL_ID[code], KIND_ID["homo_floor_perm"],
                    LANG_ID[language], index,
                ))
                values = real["kept_ids"].copy()
                rng_perm.shuffle(values)
                full = real["event_ids"].copy()
                full[real["kept_mask"]] = values
                floor_full = _count_matrix_37(full, real["kept_mask"])
                fresh_row = {
                    "index": index,
                    "full_width_total_pairs": int(round(floor_full.sum())),
                    "profile": _profile_facts(_glyph_block_matrix(
                        floor_full, real_mark
                    )),
                }
                fields += 1
                differing = [
                    key for key in sorted(
                        set(fresh_row) | set(stored_row)
                    )
                    if fresh_row.get(key) != stored_row.get(key)
                ]
                if differing:
                    problems.append(
                        f"floor/{code}/{language}/{index}: the "
                        f"standing row's replay does not equal the "
                        f"stored corpus-breadth row ({', '.join(differing)})"
                    )
            fresh_plaintext = _profile_facts(
                _stream_matrix_27(standing_truncated)
            )
            fields += 1
            if fresh_plaintext != stored_cell["plaintext_profile"]:
                differing = [
                    key for key in sorted(
                        set(fresh_plaintext)
                        | set(stored_cell["plaintext_profile"])
                    )
                    if fresh_plaintext.get(key)
                    != stored_cell["plaintext_profile"].get(key)
                ]
                problems.append(
                    f"plaintext/{code}/{language}: the standing "
                    f"control's profile does not equal the stored "
                    f"corpus-breadth profile ({', '.join(differing)})"
                )
            fresh_real = {
                "stream_events": real["total_events"],
                "kept_pairs": int(real_matrix.sum()),
                "unmapped_events": (
                    real["total_events"] - int(real["kept_mask"].sum())
                ),
                "boundary_carried_pairs": _boundary_carried_pairs(
                    real_matrix, real_mark
                ),
                "real_profile": _profile_facts(
                    _glyph_block_matrix(real_matrix, real_mark)
                ),
                "real_full_width_total_pairs": int(real_matrix.sum()),
                "standing_plant_length": len(standing_truncated),
                "plants_at_source_identity": all(
                    row["full_width_total_pairs"]
                    == row["plant_length"] - 1
                    for row in fresh_plants
                ),
            }
            fields += 1
            differing = [
                key for key in MATCHED_REAL_RECORD_KEYS
                if fresh_real.get(key) != stored_cell.get(key)
            ]
            if differing:
                problems.append(
                    f"real/{code}/{language}: the read cell's fresh "
                    f"real record does not equal the stored "
                    f"corpus-breadth real record ({', '.join(differing)})"
                )
    return problems, fields


def _matched_cell_facts(
    code: str, language: str, basis: int | None = None
) -> dict:
    """One cell's matched-truncation facts: the corpus-breadth cell's
    roster replayed with every simulated stream cut to the declared
    basis, the cell's real counted pair total + 1 tokens: each member's
    and each plant's frozen draw chain re-run over the matched stream
    (the standing members' selected-draw counts replayed, the breadth
    members' declared draw 0), each row carrying its standing-basis
    anchors beside its matched facts; a stream at or below the basis
    stays whole; the floors replay unchanged, their full widths
    already the real's counted pair total by construction; the
    plaintext control records its standing profile and its matched cut
    beside it. The envelope runs the real's unchanged mark-excluded
    profile against the matched band's profiles under the declared
    strict-all rule. No machinery anywhere in the instrument. The
    basis defaults to the anchor (the real counted pair total + 1
    tokens) so the matched-basis ladder re-prices these same facts at
    its declared descending rungs."""
    real = _homo_real_stream(code)
    real_mark = len(real["mapped_chars"]) - 1
    real_matrix = _count_matrix_37(real["event_ids"], real["kept_mask"])
    real_profile = _profile_facts(
        _glyph_block_matrix(real_matrix, real_mark)
    )
    if basis is None:
        basis = int(real_matrix.sum()) + 1
    standing_truncated = _truncated_reference(code, language)
    standing_groups = _partition_groups(standing_truncated, MAPPED_HOMO)
    members = _breadth_reference_members(language)
    standing_count = len(_extended_reference_members(language))
    frozen = json.loads(RESTART_BUDGET_ARTIFACT_PATH.read_text())
    stored_band = frozen["files"][code][language]["band"]
    member_facts: list[dict] = []
    for position, (name, ebook) in enumerate(members):
        reference = _truncated_reference(code, language, file=name)
        seed = _seed(
            CELL_ID[code], KIND_ID["homo_cross_enc"],
            LANG_ID[language], position,
        )
        if position < standing_count:
            selected = stored_band[position]["selected_draw_index"]
            draws_rule = "standing_frozen_selected"
            draws_value: int = selected
        else:
            draws_rule = "breadth_declared_draw_0"
            draws_value: int = 0
        groups = _partition_groups(reference, MAPPED_HOMO)
        rng_enc = np.random.default_rng(seed)
        encoded: np.ndarray | None = None
        for _draw in range(draws_value + 1):
            encoded = _encode(reference, groups, rng_enc, MAPPED_HOMO)
        standing_full = _full_matrix_37(encoded)
        matched_reference = reference[:basis]
        matched_groups = _partition_groups(matched_reference, MAPPED_HOMO)
        rng_enc = np.random.default_rng(seed)
        matched_encoded: np.ndarray | None = None
        for _draw in range(draws_value + 1):
            matched_encoded = _encode(
                matched_reference, matched_groups, rng_enc, MAPPED_HOMO
            )
        matched_full = _full_matrix_37(matched_encoded)
        member_facts.append({
            "file": name,
            "ebook": ebook,
            "plant_length": len(reference),
            "selected_draw_index": draws_value,
            "draw_rule": draws_rule,
            "full_width_total_pairs": int(round(standing_full.sum())),
            "matched_length": len(matched_reference),
            "matched_total_pairs": int(round(matched_full.sum())),
            "matched_profile": _profile_facts(
                _glyph_block_matrix(matched_full, MAPPED_HOMO)
            ),
        })
    plant_facts: list[dict] = []
    for index in range(N_PLANTS):
        seed = _seed(
            CELL_ID[code], KIND_ID["homo_plant_enc"],
            LANG_ID[language], index,
        )
        rng_enc = np.random.default_rng(seed)
        encoded = _encode(
            standing_truncated, standing_groups, rng_enc, MAPPED_HOMO
        )
        standing_full = _full_matrix_37(encoded)
        matched_reference = standing_truncated[:basis]
        matched_groups = _partition_groups(matched_reference, MAPPED_HOMO)
        rng_enc = np.random.default_rng(seed)
        matched_encoded = _encode(
            matched_reference, matched_groups, rng_enc, MAPPED_HOMO
        )
        matched_full = _full_matrix_37(matched_encoded)
        plant_facts.append({
            "index": index,
            "plant_length": len(standing_truncated),
            "full_width_total_pairs": int(round(standing_full.sum())),
            "matched_length": len(matched_reference),
            "matched_total_pairs": int(round(matched_full.sum())),
            "matched_profile": _profile_facts(
                _glyph_block_matrix(matched_full, MAPPED_HOMO)
            ),
        })
    floor_facts: list[dict] = []
    for index in range(N_FLOORS):
        rng_perm = np.random.default_rng(_seed(
            CELL_ID[code], KIND_ID["homo_floor_perm"],
            LANG_ID[language], index,
        ))
        values = real["kept_ids"].copy()
        rng_perm.shuffle(values)
        full = real["event_ids"].copy()
        full[real["kept_mask"]] = values
        floor_full = _count_matrix_37(full, real["kept_mask"])
        floor_facts.append({
            "index": index,
            "full_width_total_pairs": int(round(floor_full.sum())),
            "profile": _profile_facts(
                _glyph_block_matrix(floor_full, real_mark)
            ),
        })
    plaintext = _profile_facts(_stream_matrix_27(standing_truncated))
    plaintext_matched = _profile_facts(
        _stream_matrix_27(standing_truncated[:basis])
    )
    band = [{"profile": row["matched_profile"]} for row in member_facts]
    tests = _search_free_envelope(real_profile, band)
    outside = [key for key, test in tests.items() if not test["inside"]]
    verdict = (
        "shape-consistent-with-homophonic-encoding" if not outside
        else "shape-outside-analogues"
    )
    return {
        "stream_events": real["total_events"],
        "kept_pairs": int(real_matrix.sum()),
        "unmapped_events": (
            real["total_events"] - int(real["kept_mask"].sum())
        ),
        "boundary_carried_pairs": _boundary_carried_pairs(
            real_matrix, real_mark
        ),
        "real_profile": real_profile,
        "real_full_width_total_pairs": int(real_matrix.sum()),
        "standing_plant_length": len(standing_truncated),
        "plants_at_source_identity": all(
            plant["full_width_total_pairs"]
            == plant["plant_length"] - 1
            for plant in plant_facts
        ),
        "match_basis_events": basis,
        "matched_members_cut": sum(
            1 for row in member_facts
            if row["matched_length"] < row["plant_length"]
        ),
        "matched_plants_cut": sum(
            1 for row in plant_facts
            if row["matched_length"] < row["plant_length"]
        ),
        "members_profiles": member_facts,
        "plants_profiles": plant_facts,
        "floors_profiles": floor_facts,
        "plaintext_profile": plaintext,
        "plaintext_matched_profile": plaintext_matched,
        "invariants": tests,
        "outside_invariants": outside,
        "verdict": verdict,
    }


def substitution_homophonic_matched_truncation() -> dict:
    """The declared matched-truncation interior-shape instrument: the
    corpus-breadth instrument's roster, state space and summaries
    re-priced with every simulated stream cut to the real's own
    counted pair mass. The bridge gate runs first; any divergence
    aborts with nothing written."""
    problems, fields = _compare_matched_to_frozen()
    if problems:
        raise AssertionError(
            "matched-truncation bridge gate failed: "
            + "; ".join(problems)
        )
    artifact = {
        "what": "The declared matched-truncation interior-shape "
        "instrument: the corpus-breadth instrument's same state space, "
        "the same twelve english and eleven latin member roster, the "
        "same plants, floors and controls, and the same six "
        "relabeling-invariant summaries over the same mark-excluded "
        "state space (1296 ordered types, the boundary mark's row and "
        "column excluded on both sides exactly as declared there), "
        "re-priced with every simulated stream cut to the real's own "
        "counted pair mass (each band member's encoding and every "
        "plant running its frozen chain over the matched stream, cut "
        "encodings' full widths equal to the real's counted pair "
        "total and the floors' full widths exactly, streams at or "
        "below the basis whole, the real and the floors unchanged), "
        "priced under the same declared strict-all verdict rule with "
        "no assignment search anywhere in the instrument. The "
        "declared truthful question: with the band's streams matched "
        "to the real's own pair mass under the declared cut, does the "
        "real's mark-excluded profile sit inside the matched band's "
        "range on every declared invariant in every (file, language) "
        "cell, or is at least one invariant outside - the measured "
        "test of whether the interior's separation is a length "
        "artifact of the real's own counted mass or holds as the "
        "masses match. No mapping is published; nothing here is a "
        "reading.",
        "declared": {
            "base_seed": BASE_SEED,
            "mapped": MAPPED_HOMO,
            "boundary_rule": "the word-boundary mark's row and column "
            "are excluded from every profile's state space on both "
            "sides exactly as the boundary-mark re-instrument declared: "
            "every profile is the mark-excluded block of its "
            "pair-count matrix, 1296 ordered types, the mark located in "
            "each matrix's own alphabet (symbol 36 in every simulated "
            "encoding and the real file's own last mapped position), "
            "the full width's total recorded beside the matched rows' "
            "block profiles, and no boundary-adjusted marginal appears "
            "anywhere; the standing alphabet-width disclosure carries "
            "unchanged (the IT real transcription ranks only 23 glyph "
            "types plus the mark, so 13 of its block's 36 glyph slots "
            "are empty by width alone on the real side while the "
            "simulated alphabets are saturated at 36 in every cell)",
            "matched_truncation_rule": "the matched truncation, "
            "declared before the run: the cell's real stream prices "
            "kept-adjacent pairs only (its unmapped events break "
            "adjacency), so its counted pair total is ZL 218,415, GC "
            "183,199 and IT 220,531 pairs; the basis is that total + 1 "
            "tokens (ZL 218,416, GC 183,200, IT 220,532), and every "
            "simulated encoding (each band member's encoding and "
            "every plant's encoding) re-runs its own frozen chain, the "
            "declared draws of its row's rule, over the matched "
            "stream, the standing truncated reference's first basis "
            "tokens, so a cut stream's full width equals the real's "
            "counted pair total exactly (ZL 218,415, GC 183,199, IT "
            "220,531), the same mass the floors already price by "
            "construction, while a stream at or below the basis stays "
            "whole; the cut takes the trailing tokens only, so the "
            "removed pair mass is bounded: ZL 247 of the standing "
            "218,662 full-width pairs (0.11296 percent), GC 3,508 of "
            "186,707 (1.87888 percent), IT 0; no new corpus files, no "
            "roster change, no new seed kind and no new selection "
            "anywhere",
            "roster_rule": "the corpus-breadth roster stands "
            "unchanged: the same eight accepted corpus files, the "
            "same rejected candidates with their verbatim causes, the "
            "same sha256 records, the roster floor and the fetch "
            "verification are the corpus-breadth artifact's declared "
            "facts taken by reference, no corpus file is re-fetched, "
            "re-probed or re-hashed here, and the roster's streams "
            "replay through the standing declared processing with no "
            "new step (the frozen rows' plant_length values "
            "replay-match under the gate), so no roster position "
            "changes",
            "invariants": {
                "sorted_symbol_marginals": "the 36 mark-excluded "
                "glyph marginals as a multiset, stored sorted "
                "descending as counts and shares, envelope-tested by "
                "sorted position over 36 positions",
                "sorted_pair_multiset": "the 1296 mark-excluded pair "
                "counts as a multiset, stored sorted descending as "
                "counts and shares, envelope-tested by sorted "
                "position",
                "empty_type_count": "the number of the block's "
                "mark-excluded pair types with zero counted "
                "occurrences, a scalar inside [min, max]",
                "self_pair_share": "the block's diagonal sum over the "
                "profile's glyph-pair total",
                "top_k_shares": "the share of the glyph-pair total "
                "carried by the k largest pair counts, at k 1, 10 "
                "and 50",
                "pair_entropy": "the natural entropy of the "
                "mark-excluded pair distribution in nats per counted "
                "glyph pair",
            },
            "state_note": "every profile here is the mark-excluded "
            "block of the same pair-count matrices the boundary-mark "
            "instrument priced: the real's kept-adjacent pairs and "
            "the encodings' full streams keep their structural "
            "difference, every share-valued invariant normalises by "
            "its own glyph-pair total, and the empty type count is a "
            "raw count tied to its own total and recorded in that "
            "context; the plaintext control's state is the 27 "
            "reference letters alone (729 types, no boundary mark) "
            "and takes no part in any envelope; the latin envelopes "
            "stay size-mixed by the roster's own declared "
            "construction (the below-basis members replay whole, so "
            "the matched member streams run 45,490 pairs upward), "
            "and the IT cells carry the declared degenerate case "
            "exactly: their basis equals the standing truncated "
            "length because the real transcription holds no unmapped "
            "events, so every IT matched fact equals its standing "
            "fact and the IT matched verdict is the corpus-breadth "
            "verdict replayed",
            "machinery_rule": "this instrument contains no assignment "
            "search anywhere: no candidate evaluation, no restarts, "
            "no sweep cap, no convergence flags; the standing budgets "
            "are not applicable and no machinery recording appears "
            "for that reason",
            "split_rule": "no split applies: a profile uses every "
            "counted pair of its stream after the declared exclusion; "
            "the climb and score halves of the band instruments have "
            "no counterpart here",
            "seed_kinds": "the standing encoding, plant and floor "
            "kinds replay at their frozen positions with their frozen "
            "selected draws exactly as every predecessor declared; "
            "each matched encoding runs its own frozen chain's "
            "declared draws over the matched stream from draw 0 "
            "upward; no new seed is consumed and no draw selection is "
            "performed",
            "seed_sharing": "the standing-basis facts (every member "
            "row's anchors, every plant's standing row, every floor "
            "row and the standing plaintext control) replay through "
            "the declared chains and verify against the frozen "
            "corpus-breadth artifact field for field under the gate; "
            "the matched facts run the same seeds over the matched "
            "streams from draw 0 upward; every block profile of every "
            "matched row is the declared block of its own replayed "
            "matched encoding",
            "matched_band_record_rule": "the simulated band per "
            "language cell stays the corpus-breadth roster's twelve "
            "english and eleven latin members, unconditional, priced "
            "at the matched basis: each member row carries its "
            "standing-basis anchors (file, ebook, plant_length, "
            "selected_draw_index, draw_rule, and the standing "
            "encoding's own full width, gate-anchored to the frozen "
            "corpus-breadth rows) and its matched facts (matched "
            "length, matched total and matched profile, the row's "
            "priced profile), the matched total an exact identity, "
            "matched length - 1, of every row; the standing members "
            "re-run their frozen selected-draw counts at the matched "
            "length and the breadth members run their declared draw 0 "
            "there, and no draw selection is performed anywhere",
            "plants_rule": "the 30 plant encodings (5 per cell, the "
            "standing first references at the standing kinds) "
            "recorded at the matched basis like the band: each row "
            "carries its standing full width (the standing encoding's "
            "own, gate-anchored to the frozen corpus-breadth rows), "
            "its matched length, its matched total (the same exact "
            "identity) and its matched glyph-block profile; the "
            "plants_at_source_identity boolean reports the standing "
            "widths at the standing lengths, and each matched row "
            "carries the same identity at its matched length; no "
            "parity rule applies because there is no anchor geometry "
            "to exceed",
            "floors_rule": "the 30 destroyed-adjacency floors "
            "recorded as identical replays: a floor's full width is "
            "the shuffled kept-adjacency structure's own pair count, "
            "the real's counted pair total exactly, so the floors "
            "already sit at the matched scale everywhere and nothing "
            "here re-cuts them; their glyph-block profiles replay "
            "under the gate; their declared role is the "
            "shuffled-structure control recorded beside the verdict, "
            "not part of any envelope",
            "plaintext_rule": "each cell records the standing "
            "truncated reference's own plaintext stream profile "
            "(replay-verified against the frozen records) and its "
            "matched control re-cut to the basis beside it "
            "(plaintext_matched_profile), both computed by the same "
            "formulas on the 27-type letter state (729 types, no "
            "boundary mark), as the prose control beside the verdict; "
            "neither control takes part in any envelope",
            "verdict_rule": "declared strict-all, unchanged: a cell "
            "is shape-consistent-with-homophonic-encoding only when "
            "every declared invariant of the real's glyph-block "
            "profile sits inside the closed range of that cell's "
            "matched band's glyph-block profiles (the two vector "
            "summaries term by term inside the band's per-position "
            "envelope over 36 sorted positions, the scalar summaries "
            "inside [min, max] at the stored 6-decimal rounding); any "
            "outside invariant makes the cell "
            "shape-outside-analogues, and every outside entry is "
            "recorded with its band range so the miss is audited not "
            "summarized",
            "closure_rule": "no scalar margin is formed: this "
            "instrument's question is inside or outside per "
            "invariant, and the recorded distances are the outside "
            "entries' band ranges themselves",
            "exclusion_rule": "the family's declared exclusion format "
            "is not re-scoped by this artifact: it keys to the "
            "declared 36-slot class under the inherited add-one form "
            "exactly as the held-out screen declared it, so a "
            "search-free verdict is structure evidence and the band "
            "instruments' verdicts stand untouched by this "
            "artifact's numbers",
            "bridge_gate": "before any profile is priced, every fact "
            "this instrument re-derives fresh that a frozen "
            "predecessor already recorded must equal that stored "
            "value field for field: the corpus-breadth instrument's "
            "399 anchor fields exactly as that instrument declared "
            "them (the boundary-mark gate's 288 anchors and the 111 "
            "standing profile checks), then per cell the frozen "
            "corpus-breadth rows' standing replays verified against "
            "fresh re-derivations: each member row (file, ebook, "
            "plant_length, selected_draw_index, draw_rule, full-width "
            "total and block profile) replayed through its declared "
            "chain, each plant row (index, plant_length, standing "
            "full-width total and block profile), each floor row "
            "(index, full-width total and block profile), each "
            "plaintext control's standing profile, and each cell's "
            "real record's eight declared fields, 24 row checks per "
            "english cell and 23 per latin cell, 141 row checks "
            "total; the matched facts carry no frozen counterpart and "
            "ride on the declared roster; any divergence aborts with "
            "nothing written",
            "models_rule": "no score table is built or used: the "
            "instrument prices count structure only, so the standing "
            "add-one and leave-one-out tables play no part anywhere "
            "in this artifact",
        },
        "bridge_gate": {
            "status": "verified",
            "fields_compared": fields,
            "anchor_fields": 399,
            "breadth_replay_checks": fields - 399,
        },
        "files": {},
    }
    for code in FILES:
        cell = {}
        for language in LANGS:
            cell[language] = _matched_cell_facts(code, language)
        artifact["files"][code] = cell
    return artifact


def main_matched_truncation() -> None:
    artifact = substitution_homophonic_matched_truncation()
    SEARCH_FREE_MATCHED_ARTIFACT_PATH.write_text(
        json.dumps(artifact, indent=2) + "\n"
    )
    print(SEARCH_FREE_MATCHED_ARTIFACT_PATH)


SEARCH_FREE_LADDER_ARTIFACT_PATH = (
    Path(DATA_DIR).resolve().parent.parent.parent
    / "docs" / "research-notes"
    / "voynich-homophonic-matched-basis-ladder.json"
)

LADDER_RUNGS = (1.0, 0.75, 0.5, 0.25)

LADDER_RUNG_FACT_KEYS = (
    "match_basis_events", "matched_members_cut",
    "matched_plants_cut", "members_profiles", "plants_profiles",
    "plaintext_matched_profile", "invariants",
    "outside_invariants", "verdict",
)


def _compare_ladder_to_frozen() -> tuple[list[str], int]:
    """The declared bridge gate for the ladder: the matched-truncation
    instrument's gate verified fresh first (the corpus-breadth
    instrument's 399 anchor fields and the 141 standing-row replay
    checks exactly as that instrument declared them), then the anchor
    rung's six cells verified equal to the frozen matched-truncation
    artifact's six cells field for field: each anchor member row's
    matched block, each anchor plant row's matched block, each anchor
    matched plaintext control, each anchor's basis with its cut
    counts, and each anchor's envelope result, 20 checks per english
    cell and 19 per latin cell, 117 checks total. The three descended
    rungs carry no frozen counterpart and ride on the declared rung
    rule. Any divergence aborts with nothing written."""
    problems, fields = _compare_matched_to_frozen()
    frozen = json.loads(SEARCH_FREE_MATCHED_ARTIFACT_PATH.read_text())
    for code in FILES:
        for language in LANGS:
            anchor = _matched_cell_facts(code, language)
            stored_cell = frozen["files"][code][language]
            for block, rows_key in (
                ("member", "members_profiles"),
                ("plant", "plants_profiles"),
            ):
                stored_rows = stored_cell[rows_key]
                fresh_rows = anchor[rows_key]
                if len(fresh_rows) != len(stored_rows):
                    problems.append(
                        f"ladder/{block}/{code}/{language}: row count "
                        f"{len(fresh_rows)} does not equal the frozen "
                        f"{len(stored_rows)}"
                    )
                    continue
                for position, (fresh_row, stored_row) in enumerate(
                    zip(fresh_rows, stored_rows)
                ):
                    fields += 1
                    differing = [
                        key for key in (
                            "matched_length", "matched_total_pairs",
                            "matched_profile",
                        )
                        if fresh_row.get(key) != stored_row.get(key)
                    ]
                    if differing:
                        problems.append(
                            f"ladder/{block}/{code}/{language}/"
                            f"{position}: the anchor replay's matched "
                            f"block does not equal the frozen "
                            f"matched-truncation block "
                            f"({', '.join(differing)})"
                        )
            fields += 1
            if (
                anchor["plaintext_matched_profile"]
                != stored_cell["plaintext_matched_profile"]
            ):
                problems.append(
                    f"ladder/plaintext/{code}/{language}: the anchor "
                    f"matched control does not equal the frozen "
                    f"matched-truncation matched control"
                )
            fields += 1
            differing = [
                key for key in (
                    "match_basis_events", "matched_members_cut",
                    "matched_plants_cut",
                )
                if anchor.get(key) != stored_cell.get(key)
            ]
            if differing:
                problems.append(
                    f"ladder/basis/{code}/{language}: the anchor's "
                    f"basis and cut counts do not equal the frozen "
                    f"matched-truncation record "
                    f"({', '.join(differing)})"
                )
            fields += 1
            differing = [
                key for key in (
                    "invariants", "outside_invariants", "verdict",
                )
                if anchor.get(key) != stored_cell.get(key)
            ]
            if differing:
                problems.append(
                    f"ladder/verdict/{code}/{language}: the anchor's "
                    f"envelope result does not equal the frozen "
                    f"matched-truncation record "
                    f"({', '.join(differing)})"
                )
    return problems, fields


def _ladder_rung_facts(code: str, language: str, rung: float) -> dict:
    """One rung's facts for one cell: the rung's descending basis is
    floor(rung * the anchor basis), the anchor basis the real counted
    pair total + 1 tokens, and the rung's facts are the matched cell
    facts at that basis restricted to the rung-varying record."""
    real = _homo_real_stream(code)
    anchor = (
        int(_count_matrix_37(
            real["event_ids"], real["kept_mask"]
        ).sum()) + 1
    )
    basis = anchor if rung == 1.0 else int(rung * anchor)
    facts = _matched_cell_facts(code, language, basis)
    return {key: facts[key] for key in LADDER_RUNG_FACT_KEYS}


def substitution_homophonic_ladder() -> dict:
    """The declared matched-basis ladder: the matched-truncation
    instrument's roster, state space and summaries re-priced with the
    truncation basis swept at declared rungs. The bridge gate runs
    first; any divergence aborts with nothing written."""
    problems, fields = _compare_ladder_to_frozen()
    if problems:
        raise AssertionError(
            "matched-basis ladder bridge gate failed: "
            + "; ".join(problems)
        )
    artifact = {
        "what": "The declared matched-basis ladder: the "
        "matched-truncation instrument's same state space, the same "
        "twelve english and eleven latin member roster, the same "
        "plants and floors, and the same six relabeling-invariant "
        "summaries over the same mark-excluded state space (1296 "
        "ordered types), re-priced with the truncation basis swept at "
        "declared rungs: the real's own mass anchor rung first (the "
        "matched-truncation artifact's own basis, band streams cut to "
        "the real's counted pair mass), then 75, 50 and 25 percent "
        "rungs of it, every band's closed ranges re-priced at each "
        "rung and every movement recorded against the anchor rung's "
        "bands both ways. The declared truthful question: does any "
        "rung's matched band admit the real's mark-excluded profile "
        "inside on every declared invariant in every (file, "
        "language) cell, or do every rung's verdicts stand. No "
        "mapping is published; nothing here is a reading.",
        "declared": {
            "base_seed": BASE_SEED,
            "mapped": MAPPED_HOMO,
            "boundary_rule": "the word-boundary mark's row and column "
            "are excluded from every profile's state space on both "
            "sides exactly as the boundary-mark re-instrument "
            "declared: every profile is the mark-excluded block of "
            "its pair-count matrix, 1296 ordered types, the mark "
            "located in each matrix's own alphabet, and the standing "
            "alphabet-width disclosure carries unchanged (the IT "
            "real transcription ranks only 23 glyph types plus the "
            "mark, so 13 of its block's 36 glyph slots are empty by "
            "width alone on the real side while the simulated "
            "alphabets are saturated at 36 in every cell)",
            "ladder_rung_rule": "the matched basis swept at declared "
            "rungs, recorded as design before any pricing: the anchor "
            "rung is the matched-truncation instrument's basis, the "
            "cell's real counted pair total + 1 tokens (ZL 218,416, "
            "GC 183,200, IT 220,532); the three declared rungs "
            "descend at floor(p x the anchor basis) tokens for p "
            "0.75, 0.50 and 0.25 (ZL 163,812, 109,208 and "
            "54,604; GC 137,400, 91,600 and 45,800; IT 165,399, "
            "110,266 and 55,133); at every rung each of the roster's "
            "encodings re-runs its own frozen chain over the "
            "standing truncated reference's first rung tokens, a "
            "stream above the rung cut accordingly and a stream at "
            "or below it stays whole, and every cut row prices its "
            "rung basis - 1 pairs full width (the exact identity, "
            "matched length - 1); the declared truth about the "
            "arithmetic is the matched-truncation instrument's "
            "restated: a cut can move a band's closed ranges both "
            "ways, both verdict directions are open at every rung, "
            "and the artifact records each rung's movement counts "
            "against the anchor rung's bands; the real is priced "
            "once, unchanged across rungs",
            "roster_rule": "the corpus-breadth roster stands "
            "unchanged: the same eight accepted corpus files, the "
            "same rejected candidates with their verbatim causes, "
            "the same sha256 records, the roster floor and the "
            "fetch verification are the corpus-breadth artifact's "
            "declared facts taken by reference, no corpus file is "
            "re-fetched, re-probed or re-hashed here, and the "
            "roster's streams replay through the standing declared "
            "processing with no new step",
            "invariants": {
                "sorted_symbol_marginals": "the 36 mark-excluded "
                "glyph marginals as a multiset, stored sorted "
                "descending as counts and shares, envelope-tested by "
                "sorted position over 36 positions",
                "sorted_pair_multiset": "the 1296 mark-excluded pair "
                "counts as a multiset, stored sorted descending as "
                "counts and shares, envelope-tested by sorted "
                "position",
                "empty_type_count": "the number of the block's "
                "mark-excluded pair types with zero counted "
                "occurrences, a scalar inside [min, max]",
                "self_pair_share": "the block's diagonal sum over "
                "the profile's glyph-pair total",
                "top_k_shares": "the share of the glyph-pair total "
                "carried by the k largest pair counts, at k 1, 10 "
                "and 50",
                "pair_entropy": "the natural entropy of the "
                "mark-excluded pair distribution in nats per "
                "counted glyph pair",
            },
            "state_note": "every profile here is the mark-excluded "
            "block of the same pair-count matrices the boundary-mark "
            "instrument priced, priced at its own stream's rung "
            "width: the real is priced once at its own kept-adjacent "
            "mass and is not re-cut anywhere (its profile is the "
            "matched-truncation artifact's real profile unchanged), "
            "so below the anchor rung the real's full-mass profile "
            "is compared against bands whose streams price the "
            "rung's descending mass and the ladder reads the bands' "
            "movements, not a mass match, at those rungs; every "
            "share-valued invariant normalises by its own "
            "glyph-pair total; the plaintext control's state is the "
            "27 reference letters alone (729 types, no boundary "
            "mark) and takes no part in any envelope; the latin "
            "envelopes stay size-mixed at every rung by the "
            "roster's own declared construction; the IT cells are "
            "degenerate only at the anchor rung (their basis there "
            "equals the standing truncated length because the real "
            "transcription holds no unmapped events) and at the "
            "lower rungs their streams cut like every other cell's, "
            "so the IT cells' anchor facts equal their matched-truncation "
            "facts exactly and their lower rungs carry fresh "
            "descending facts",
            "machinery_rule": "this instrument contains no assignment "
            "search anywhere: no candidate evaluation, no restarts, "
            "no sweep cap, no convergence flags; the standing "
            "budgets are not applicable and no machinery recording "
            "appears for that reason",
            "split_rule": "no split applies: a profile uses every "
            "counted pair of its stream after the declared "
            "exclusion; the climb and score halves of the band "
            "instruments have no counterpart here",
            "seed_kinds": "the standing encoding, plant and floor "
            "kinds replay at their frozen positions with their "
            "frozen selected draws exactly as every predecessor "
            "declared; each matched encoding runs its own frozen "
            "chain's declared draws over the rung's stream from "
            "draw 0 upward; no new seed is consumed and no draw "
            "selection is performed",
            "seed_sharing": "the standing-basis facts replay through "
            "the declared chains and verify against the frozen "
            "matched-truncation artifact field for field under the "
            "gate, whose anchor-run band the anchor rung re-derives "
            "fresh; every rung's matched facts run the same seeds "
            "over the rung's streams from draw 0 upward; every "
            "block profile of every rung row is the declared block "
            "of its own replayed rung encoding",
            "rung_record_rule": "per cell the artifact records the "
            "real record once (verified against the frozen "
            "matched-truncation real record) and four rungs in "
            "declared order (the anchor rung first, then 75, 50 and "
            "25 percent), each rung carrying its basis, its cut "
            "counts, its member and plant matched records, its "
            "matched plaintext control, its envelope tests, its "
            "outside list and its verdict; every member row carries "
            "its standing-basis anchors beside its matched facts at "
            "every rung, and the floors, the standing plant width "
            "and the standing plaintext control are recorded once "
            "at the cell because they are rung-independent facts "
            "the gate verifies",
            "plants_rule": "the plant encodings recorded at "
            "every rung like the band: each rung's rows carry the "
            "standing full width (the standing encoding's own, "
            "gate-anchored to the frozen corpus-breadth rows), "
            "their matched lengths min(plant length, rung), their "
            "matched totals (the same exact identity, matched "
            "length - 1) and their matched glyph-block profiles; "
            "the plants_at_source_identity boolean reports the "
            "standing widths at the standing lengths",
            "floors_rule": "the 30 destroyed-adjacency floors "
            "recorded once at the cell, unchanged across the "
            "rungs: a floor's full width is the shuffled "
            "kept-adjacency structure's own pair count, the real's "
            "counted pair total, so nothing here re-cuts them and "
            "their glyph-block profiles replay under the gate; "
            "their declared role is the shuffled-structure control "
            "recorded beside every rung's verdict, not part of any "
            "envelope",
            "plaintext_rule": "each cell records the standing "
            "truncated reference's own plaintext stream profile "
            "once and each rung's matched control re-cut to that "
            "rung beside it, both computed by the same formulas on "
            "the 27-type letter state, as the prose control beside "
            "the verdict; neither control takes part in any "
            "envelope",
            "verdict_rule": "declared strict-all, unchanged, "
            "priced per rung: a rung-cell is "
            "shape-consistent-with-homophonic-encoding only when "
            "every declared invariant of the real's glyph-block "
            "profile sits inside the closed range of that rung's "
            "matched band's glyph-block profiles (the two vector "
            "summaries term by term inside the band's per-position "
            "envelope over 36 sorted positions, the scalar "
            "summaries inside [min, max] at the stored 6-decimal "
            "rounding); any outside invariant makes the rung-cell "
            "shape-outside-analogues, every outside entry is "
            "recorded with its band range so the miss is audited "
            "not summarized, and the declared question is asked "
            "over all 24 rung-cell verdicts together",
            "closure_rule": "no scalar margin is formed: this "
            "instrument's question is inside or outside per "
            "invariant per rung, and the recorded distances are "
            "the outside entries' band ranges themselves",
            "exclusion_rule": "the family's declared exclusion "
            "format is not re-scoped by this artifact: it keys to "
            "the declared 36-slot class under the inherited "
            "add-one form exactly as the held-out screen declared "
            "it, so a search-free verdict is structure evidence "
            "and the band instruments' verdicts stand untouched by "
            "this artifact's numbers",
            "bridge_gate": "before any rung is priced, the gate "
            "verified fresh in two stages: the matched-truncation "
            "instrument's gate exactly as that instrument declared "
            "it (the corpus-breadth instrument's 399 anchor fields "
            "and the 141 standing-row replay checks, 540 fields), "
            "then the anchor rung's six cells verified equal to "
            "the frozen matched-truncation artifact's six cells "
            "field for field: each anchor member row's matched "
            "block, each anchor plant row's matched block, each "
            "anchor matched plaintext control, each anchor basis "
            "with its cut counts, and each anchor envelope "
            "result, 20 checks per english cell and 19 per latin "
            "cell, 117 checks total, 657 fields compared; the "
            "three descended rungs carry no frozen counterpart "
            "and ride on the declared rung rule; any divergence "
            "aborts with nothing written",
            "models_rule": "no score table is built or used: the "
            "instrument prices count structure only, so the "
            "standing add-one and leave-one-out tables play no "
            "part anywhere in this artifact",
        },
        "bridge_gate": {
            "status": "verified",
            "fields_compared": fields,
            "anchor_fields": 399,
            "breadth_replay_checks": fields - 399 - 117,
            "ladder_replay_checks": 117,
        },
        "files": {},
    }
    for code in FILES:
        cell = {}
        for language in LANGS:
            anchor = _matched_cell_facts(code, language)
            record = {
                key: anchor[key] for key in MATCHED_REAL_RECORD_KEYS
            }
            record["floors_profiles"] = anchor["floors_profiles"]
            record["plaintext_profile"] = anchor["plaintext_profile"]
            record["rungs"] = [
                {key: anchor[key] for key in LADDER_RUNG_FACT_KEYS}
            ]
            record["rungs"].extend(
                _ladder_rung_facts(code, language, rung)
                for rung in LADDER_RUNGS[1:]
            )
            cell[language] = record
        artifact["files"][code] = cell
    return artifact


def main_ladder() -> None:
    artifact = substitution_homophonic_ladder()
    SEARCH_FREE_LADDER_ARTIFACT_PATH.write_text(
        json.dumps(artifact, indent=2) + "\n"
    )
    print(SEARCH_FREE_LADDER_ARTIFACT_PATH)


# --------------------------------------------------------------------------
# The real-at-basis ladder: the fifteenth search-free measurement.
# --------------------------------------------------------------------------


REAL_LADDER_ARTIFACT_PATH = (
    Path(DATA_DIR).resolve().parent.parent.parent
    / "docs" / "research-notes"
    / "voynich-homophonic-real-at-basis-ladder.json"
)

REAL_LADDER_RUNG_KEYS = (
    "run", "match_basis_events", "real_rung_kept_pairs",
    "real_rung_boundary_carried_pairs", "real_rung_profile",
    "invariants", "outside_invariants", "verdict",
)


def _real_pair_sequence(code: str) -> tuple[np.ndarray, np.ndarray]:
    """The real's kept-adjacent pair sequence, ordered along the
    original stream: the exact ordered pairs _count_matrix_37 counts,
    returned as the ordered first elements and the ordered second
    elements, one pair per position."""
    real = _homo_real_stream(code)
    kept = np.where(real["kept_mask"])[0]
    values = real["event_ids"][kept]
    adjacent = kept[1:] == kept[:-1] + 1
    first = values[:-1][adjacent]
    second = values[1:][adjacent]
    return first, second


def _real_rung_facts(
    code: str, language: str, rung: float,
    frozen: dict | None = None,
) -> dict:
    """One rung's real-side facts for one cell: the real's ordered
    kept-adjacent pair sequence cut to the rung's basis minus 1 pairs
    and re-priced through the same mark-excluded block and the same
    six relabeling-invariant summaries, the rung's band the frozen
    matched-basis ladder's member profiles taken by reference, and
    the envelope record under the declared strict-all rule.

    The rung's basis is the matched-basis ladder's declared basis,
    the real counted pair total + 1 tokens at the anchor and floor(
    rung x the anchor basis) tokens at the descended rungs, and the
    real's cut prices its first basis - 1 kept-adjacent pairs, the
    exact full-width mass every one of the rung's cut rows prices.
    The mass-match identity is verified against the frozen rung's
    rows before any envelope is formed: every cut member row and
    every cut plant row prices the mass full width, and at the
    anchor rung the prefix is the whole pair sequence, its profile
    the real's unchanged profile exactly. Any divergence aborts."""
    if frozen is None:
        frozen = json.loads(SEARCH_FREE_LADDER_ARTIFACT_PATH.read_text())
    frozen_rung = frozen["files"][code][language]["rungs"][
        LADDER_RUNGS.index(rung)
    ]
    first, second = _real_pair_sequence(code)
    anchor = len(first) + 1
    basis = anchor if rung == 1.0 else int(rung * anchor)
    if basis != frozen_rung["match_basis_events"]:
        raise AssertionError(
            f"real-at-basis/{code}/{language}/rung {rung}: the "
            f"derived basis {basis} does not equal the frozen "
            f"matched-basis ladder basis "
            f"{frozen_rung['match_basis_events']}"
        )
    mass = basis - 1
    cut_rows = [
        row
        for rows in (
            frozen_rung["members_profiles"],
            frozen_rung["plants_profiles"],
        )
        for row in rows
        if row["matched_length"] < row["plant_length"]
    ]
    for row in cut_rows:
        if row["matched_total_pairs"] != mass:
            raise AssertionError(
                f"real-at-basis/{code}/{language}/rung {rung}: a cut "
                f"row prices {row['matched_total_pairs']} pairs, not "
                f"the mass {mass}"
            )
    prefix = np.zeros((37, 37))
    np.add.at(prefix, (first[:mass], second[:mass]), 1.0)
    real = _homo_real_stream(code)
    mark = len(real["mapped_chars"]) - 1
    profile = _profile_facts(_glyph_block_matrix(prefix, mark))
    carried = _boundary_carried_pairs(prefix, mark)
    if profile["total_pairs"] != mass - carried:
        raise AssertionError(
            f"real-at-basis/{code}/{language}/rung {rung}: the "
            f"re-priced block total {profile['total_pairs']} does "
            f"not equal the mass minus its boundary-carried pairs "
            f"{mass} - {carried}"
        )
    band = [
        {"profile": row["matched_profile"]}
        for row in frozen_rung["members_profiles"]
    ]
    tests = _search_free_envelope(profile, band)
    outside = [key for key, test in tests.items() if not test["inside"]]
    verdict = (
        "shape-consistent-with-homophonic-encoding" if not outside
        else "shape-outside-analogues"
    )
    return {
        "run": rung,
        "match_basis_events": basis,
        "real_rung_kept_pairs": mass,
        "real_rung_boundary_carried_pairs": carried,
        "real_rung_profile": profile,
        "invariants": tests,
        "outside_invariants": outside,
        "verdict": verdict,
    }


def _real_ladder_cell(code: str, language: str, frozen: dict) -> dict:
    """One cell's real-at-basis facts: the real record derived fresh
    (the real stream, its kept-adjacent matrix, its mark-excluded
    profile, the standing truncated reference's own length, and the
    standing plant encodings re-run through their frozen draw seeds
    for the plants-at-source identity) and the four declared rungs'
    real-side facts beside them."""
    real = _homo_real_stream(code)
    real_mark = len(real["mapped_chars"]) - 1
    real_matrix = _count_matrix_37(real["event_ids"], real["kept_mask"])
    real_profile = _profile_facts(
        _glyph_block_matrix(real_matrix, real_mark)
    )
    standing_truncated = _truncated_reference(code, language)
    standing_groups = _partition_groups(
        standing_truncated, MAPPED_HOMO
    )
    plant_identity = True
    for index in range(N_PLANTS):
        seed = _seed(
            CELL_ID[code], KIND_ID["homo_plant_enc"],
            LANG_ID[language], index,
        )
        rng_enc = np.random.default_rng(seed)
        encoded = _encode(
            standing_truncated, standing_groups, rng_enc, MAPPED_HOMO
        )
        standing_full = _full_matrix_37(encoded)
        if int(round(standing_full.sum())) != len(standing_truncated) - 1:
            plant_identity = False
    record = {
        "stream_events": real["total_events"],
        "kept_pairs": int(real_matrix.sum()),
        "unmapped_events": (
            real["total_events"] - int(real["kept_mask"].sum())
        ),
        "boundary_carried_pairs": _boundary_carried_pairs(
            real_matrix, real_mark
        ),
        "real_profile": real_profile,
        "real_full_width_total_pairs": int(real_matrix.sum()),
        "standing_plant_length": len(standing_truncated),
        "plants_at_source_identity": plant_identity,
    }
    cell = dict(record)
    cell["rungs"] = [
        _real_rung_facts(code, language, rung, frozen)
        for rung in LADDER_RUNGS
    ]
    return cell


def _compare_real_ladder_to_frozen() -> tuple[list[str], int]:
    """The declared bridge gate for the real-at-basis ladder, two
    stages: the matched-basis ladder's gate exactly as that
    instrument declared it (the matched-truncation instrument's 540
    anchor and replay fields plus the 117 anchor-rung replay checks,
    657 fields), then per cell the fresh real-side record verified
    against the frozen matched-basis ladder's cell: the record's
    eight declared fields, the four rung bases' identities, and the
    anchor rung's fresh envelope equal to the frozen anchor rung's
    envelope result, 6 checks per cell, 36 checks total, 693 fields
    compared. The three descended rungs' envelopes carry no frozen
    counterpart and ride on the declared rung rule, whose mass-match
    identity aborts on any divergence. Any divergence in any stage
    aborts with nothing written."""
    problems, fields = _compare_ladder_to_frozen()
    frozen = json.loads(SEARCH_FREE_LADDER_ARTIFACT_PATH.read_text())
    for code in FILES:
        for language in LANGS:
            frozen_cell = frozen["files"][code][language]
            fresh = _real_ladder_cell(code, language, frozen)
            fields += 1
            differing = [
                key for key in MATCHED_REAL_RECORD_KEYS
                if fresh[key] != frozen_cell[key]
            ]
            if differing:
                problems.append(
                    f"real-at-basis/record/{code}/{language}: the "
                    f"fresh real record does not equal the frozen "
                    f"matched-basis ladder record "
                    f"({', '.join(differing)})"
                )
            for index, rung in enumerate(LADDER_RUNGS):
                fields += 1
                if (
                    fresh["rungs"][index]["match_basis_events"]
                    != frozen_cell["rungs"][index]["match_basis_events"]
                ):
                    problems.append(
                        f"real-at-basis/basis/{code}/{language}/rung "
                        f"{rung}: the derived basis does not equal "
                        f"the frozen rung's basis"
                    )
            fresh_anchor = fresh["rungs"][0]
            frozen_anchor = frozen_cell["rungs"][0]
            fields += 1
            differing = [
                key for key in (
                    "invariants", "outside_invariants", "verdict",
                )
                if fresh_anchor[key] != frozen_anchor[key]
            ]
            if fresh_anchor["real_rung_profile"] != (
                frozen_cell["real_profile"]
            ):
                differing.append("real_rung_profile")
            if differing:
                problems.append(
                    f"real-at-basis/anchor/{code}/{language}: the "
                    f"anchor rung's fresh envelope does not equal "
                    f"the frozen matched-basis ladder's anchor "
                    f"envelope ({', '.join(differing)})"
                )
    return problems, fields


def substitution_homophonic_real_ladder() -> dict:
    """The declared real-at-basis ladder: the matched-basis ladder's
    same rungs, bands and strict-all question, with the real's own
    kept-adjacent pair sequence re-priced at each declared rung. The
    bridge gate runs first; any divergence aborts with nothing
    written."""
    problems, fields = _compare_real_ladder_to_frozen()
    if problems:
        raise AssertionError(
            "real-at-basis ladder bridge gate failed: "
            + "; ".join(problems)
        )
    frozen = json.loads(SEARCH_FREE_LADDER_ARTIFACT_PATH.read_text())
    artifact = {
        "what": "The declared real-at-basis ladder: the "
        "matched-basis ladder's same state space (1296 ordered "
        "types, the boundary mark's row and column excluded on both "
        "sides), the same four declared rungs, the same member bands "
        "re-priced per rung, and the same six relabeling-invariant "
        "summaries, with the real's own kept-adjacent pair sequence "
        "re-priced at each rung beside them: its first basis - 1 "
        "pairs, the exact full-width mass every one of the rung's "
        "cut rows prices, through the same mark-excluded block. The "
        "anchor rung's comparison is the matched-basis ladder's own; "
        "every descended rung's comparison is mass-matched on both "
        "sides for the first time in this family. The declared "
        "truthful question: does the real's own descending profile "
        "track the rung bands' descension or stay apart down the "
        "ladder in every (file, language) cell. No mapping is "
        "published; nothing here is a reading.",
        "declared": {
            "base_seed": BASE_SEED,
            "mapped": MAPPED_HOMO,
            "boundary_rule": "the word-boundary mark's row and "
            "column are excluded from every profile's state space "
            "on both sides exactly as the boundary-mark "
            "re-instrument declared: every profile is the "
            "mark-excluded block of its pair-count matrix, 1296 "
            "ordered types, the mark located in each matrix's own "
            "alphabet, and the standing alphabet-width disclosure "
            "carries unchanged (the IT real transcription ranks "
            "only 23 glyph types plus the mark, so 13 of its "
            "block's 36 glyph slots are empty by width alone on "
            "the real side while the simulated alphabets are "
            "saturated at 36 in every cell)",
            "real_ladder_rule": "the real's own kept-adjacent pair "
            "sequence re-priced at the matched-basis ladder's "
            "declared rungs, recorded as design before any "
            "pricing: the anchor rung first at the cell's real "
            "counted pair total + 1 tokens (ZL 218,416, GC 183,200, "
            "IT 220,532), then floor(p x the anchor basis) rungs "
            "at p 0.75, 0.50 and 0.25 (ZL 163,812, 109,208 and "
            "54,604; GC 137,400, 91,600 and 45,800; IT 165,399, "
            "110,266 and 55,133); at every rung the real prices "
            "its first basis - 1 kept-adjacent pairs through the "
            "same mark-excluded block and the same six summaries, "
            "and the real's cut can move its own profile both ways "
            "exactly as a band's cut moves a band's closed ranges "
            "both ways; the anchor rung's re-priced profile is the "
            "real's unchanged matched-basis ladder profile exactly "
            "and every descended rung's is fresh",
            "mass_rule": "the comparison at every rung is "
            "mass-matched on the paired side by the exact band "
            "arithmetic the matched-basis ladder priced, and "
            "mass-matched on the real side by construction: the "
            "real's rung mass is its rung basis - 1 pairs and "
            "every one of the rung's cut rows prices its "
            "match_basis_events - 1 pairs full width, the mass-match "
            "identity verified against the frozen rung's rows "
            "before any envelope is formed; a rung's whole rows "
            "keep their standing masses inside the envelope, the "
            "same disclosed mix the anchor rung carried, and the "
            "real's re-priced block total equals the mass minus "
            "its own boundary-carried pairs exactly",
            "band_reference_rule": "the rung bands are the frozen "
            "matched-basis ladder's rung facts taken by reference, "
            "their own measurements verified under that "
            "instrument's gate and tests: the anchor rung's "
            "envelope result is re-derived fresh here and verified "
            "equal to the frozen anchor rung's, and every "
            "descended rung's envelope runs the real's fresh "
            "re-priced profile against the frozen rung's member "
            "profiles exactly as that instrument stored them",
            "roster_rule": "the corpus-breadth roster stands "
            "unchanged: the same eight accepted corpus files, the "
            "same rejected candidates with their verbatim causes, "
            "the same sha256 records, the roster floor and the "
            "fetch verification are the corpus-breadth artifact's "
            "declared facts taken by reference, no corpus file is "
            "re-fetched, re-probed or re-hashed here, and no "
            "encoding is re-run on the band side anywhere: the "
            "bands are the frozen instrument's own",
            "invariants": {
                "sorted_symbol_marginals": "the 36 mark-excluded "
                "glyph marginals as a multiset, stored sorted "
                "descending as counts and shares, envelope-tested "
                "by sorted position over 36 positions",
                "sorted_pair_multiset": "the 1296 mark-excluded "
                "pair counts as a multiset, stored sorted "
                "descending as counts and shares, envelope-tested "
                "by sorted position",
                "empty_type_count": "the number of the block's "
                "mark-excluded pair types with zero counted "
                "occurrences, a scalar inside [min, max]",
                "self_pair_share": "the block's diagonal sum over "
                "the profile's glyph-pair total",
                "top_k_shares": "the share of the glyph-pair "
                "total carried by the k largest pair counts, at k "
                "1, 10 and 50",
                "pair_entropy": "the natural entropy of the "
                "mark-excluded pair distribution in nats per "
                "counted glyph pair",
            },
            "state_note": "every band profile here is the frozen "
            "matched-basis ladder's mark-excluded member profile "
            "at its rung width, taken by reference; the real's "
            "profiles are priced fresh at every rung from its own "
            "ordered kept-adjacent pair sequence, whose "
            "adjacency is the original stream's with the unmapped "
            "events breaking it (126 unmapped events inside ZL's "
            "218,663, 1,769 inside GC's 186,708, none inside IT's "
            "220,532) exactly as disclosed since the interior "
            "instrument; the anchor rung's real profile is the "
            "whole sequence and equals the frozen profile the "
            "gate verifies; the share-valued invariants "
            "normalise by their own glyph-pair totals, so the "
            "real's descending mass prices like the bands' "
            "descending masses at every rung",
            "machinery_rule": "this instrument contains no "
            "assignment search anywhere: no candidate evaluation, "
            "no restarts, no sweep cap, no convergence flags; the "
            "standing budgets are not applicable and no machinery "
            "recording appears for that reason",
            "split_rule": "no split applies: a profile uses every "
            "counted pair of its stream after the declared "
            "exclusion; the climb and score halves of the band "
            "instruments have no counterpart here",
            "seed_kinds": "no seed is consumed anywhere in this "
            "instrument: the real's own sequence needs no "
            "encoding, the bands are the frozen instrument's "
            "facts taken by reference, and the standing plant "
            "encodings replay their frozen declared draws on the "
            "real-record side only, the same standing encodings "
            "every predecessor priced",
            "record_rule": "per cell the artifact records the "
            "real record once (verified against the frozen "
            "matched-basis ladder record) and the four declared "
            "rungs in order (the anchor rung first, then 75, 50 "
            "and 25 percent), each rung carrying its run "
            "percentage, its basis, the real's rung mass, the "
            "rung's boundary-carried pairs, the real's re-priced "
            "profile, its envelope tests, its outside list and "
            "its verdict; the rung's member band itself is not "
            "re-stored here: it stays the frozen instrument's "
            "declared record",
            "verdict_rule": "declared strict-all, unchanged, "
            "priced per rung on the real's re-priced profile: a "
            "rung-cell is shape-consistent-with-homophonic-"
            "encoding only when every declared invariant of the "
            "real's re-priced glyph-block profile sits inside the "
            "closed range of that rung's matched band's "
            "glyph-block profiles (the two vector summaries term "
            "by term inside the band's per-position envelope "
            "over 36 sorted positions, the scalar summaries "
            "inside [min, max] at the stored 6-decimal "
            "rounding); any outside invariant makes the rung-cell "
            "shape-outside-analogues, every outside entry is "
            "recorded with its band range so the miss is audited "
            "not summarized, and the declared question is asked "
            "over all 24 rung-cell verdicts together",
            "closure_rule": "no scalar margin is formed: this "
            "instrument's question is inside or outside per "
            "invariant per rung, and the recorded distances are "
            "the outside entries' band ranges themselves",
            "exclusion_rule": "the family's declared exclusion "
            "format is not re-scoped by this artifact: it keys "
            "to the declared 36-slot class under the inherited "
            "add-one form exactly as the held-out screen "
            "declared it, so a search-free verdict is structure "
            "evidence and the band instruments' verdicts stand "
            "untouched by this artifact's numbers",
            "bridge_gate_rule": "before any rung is priced, the "
            "gate verified fresh in two stages: the "
            "matched-basis ladder's gate exactly as that "
            "instrument declared it (the matched-truncation "
            "instrument's 540 anchor and replay fields plus the "
            "117 anchor-rung replay checks, 657 fields), then "
            "per cell the fresh real record verified against the "
            "frozen matched-basis ladder's cell record (its "
            "eight declared fields), the four rung bases' "
            "identities, and the anchor rung's fresh envelope "
            "equal to the frozen anchor rung's envelope result, "
            "6 checks per cell, 36 checks total, 693 fields "
            "compared; the three descended rungs' envelopes "
            "carry no frozen counterpart and ride on the "
            "declared rung rule, whose mass-match identity "
            "aborts on any divergence; any divergence aborts "
            "with nothing written",
            "models_rule": "no score table is built or used: "
            "the instrument prices count structure only, so the "
            "standing add-one and leave-one-out tables play no "
            "part anywhere in this artifact",
        },
        "bridge_gate": {
            "status": "verified",
            "fields_compared": fields,
            "ladder_gate_fields": 657,
            "real_rung_replay_checks": fields - 657,
        },
        "files": {},
    }
    for code in FILES:
        cell = {}
        for language in LANGS:
            cell[language] = _real_ladder_cell(code, language, frozen)
        artifact["files"][code] = cell
    return artifact


def main_real_ladder() -> None:
    artifact = substitution_homophonic_real_ladder()
    REAL_LADDER_ARTIFACT_PATH.write_text(
        json.dumps(artifact, indent=2) + "\n"
    )
    print(REAL_LADDER_ARTIFACT_PATH)


# --------------------------------------------------------------------------
# The sixteenth declared measurement, the cut-geometry attribution
# instrument: the real's own kept-adjacent pair sequence cut at the
# declared rung masses under declared geometries (the standing prefix
# cut, a suffix cut, and declared seeded random submasses of the same
# masses), every geometry's re-priced profile priced against the same
# frozen rung bands under the same strict-all rule.
# --------------------------------------------------------------------------

N_CUT_SEEDS = 4

CUT_GEOM_ARTIFACT_PATH = (
    Path(DATA_DIR).resolve().parent.parent.parent
    / "docs" / "research-notes"
    / "voynich-homophonic-cut-geometry-attribution.json"
)

CUT_GEOM_RUNG_KEYS = (
    "real_rung_kept_pairs",
    "real_rung_boundary_carried_pairs",
    "real_rung_profile",
    "invariants",
    "verdict",
)


def _real_geometry_row(
    code: str, language: str, rung: float, geometry: str,
    seed_index: int | None, frozen_m15: dict, frozen_mb: dict,
) -> dict:
    """One cut-geometry row for one cell at one rung: the real's
    ordered kept-adjacent pair sequence cut to the rung's mass under
    the declared geometry (the standing prefix cut, a suffix cut, or
    a declared seeded random submass of the same mass), re-priced
    through the same mark-excluded block and the same six
    relabeling-invariant summaries, and envelope-tested against the
    rung's frozen band (the frozen matched-basis ladder's member
    profiles at the rung width, the same bands the real-at-basis
    ladder priced) under the declared strict-all rule.

    The declared geometry rule: the prefix cut prices the sequence's
    first mass positions (the real-at-basis ladder's own row,
    verified in the gate), the suffix cut prices its last mass
    positions, and a random row prices the declared seed's
    permutation of the sequence's positions at its first mass
    positions, so one seed's rung submasses are nested subsets. The
    declared seed kind is homo_cut_geom, positions 0 to 3, per file
    with the language slot fixed at 0 because the real's side is
    identical for both languages of a file. Every row prices the
    rung's mass exactly (the mass-match identity, enforced in code),
    and at the anchor rung every geometry's submass is the whole
    sequence, its profile the frozen real-at-basis ladder's
    whole-sequence profile exactly (the degenerate identity,
    enforced here). Any divergence aborts."""
    frozen_rung = frozen_m15["files"][code][language]["rungs"][
        LADDER_RUNGS.index(rung)
    ]
    frozen_mb_rung = frozen_mb["files"][code][language]["rungs"][
        LADDER_RUNGS.index(rung)
    ]
    first, second = _real_pair_sequence(code)
    total = len(first)
    anchor = total + 1
    basis = anchor if rung == 1.0 else int(rung * anchor)
    mass = basis - 1
    if mass != frozen_rung["real_rung_kept_pairs"]:
        raise AssertionError(
            f"cut-geometry/{code}/{language}/rung {rung}: the "
            f"derived mass {mass} does not equal the frozen "
            f"real-at-basis ladder rung mass "
            f"{frozen_rung['real_rung_kept_pairs']}"
        )
    if geometry == "prefix":
        take = np.arange(mass)
    elif geometry == "suffix":
        take = np.arange(total - mass, total)
    elif geometry == "random":
        seed = _seed(
            CELL_ID[code], KIND_ID["homo_cut_geom"], 0, seed_index
        )
        rng = np.random.default_rng(seed)
        take = rng.permutation(total)[:mass]
    else:
        raise AssertionError(f"cut-geometry: unknown geometry {geometry}")
    if len(take) != mass:
        raise AssertionError(
            f"cut-geometry/{code}/{language}/rung {rung}: the "
            f"{geometry} row prices {len(take)} pairs, not the rung's "
            f"mass {mass}"
        )
    sub_first = first[take]
    sub_second = second[take]
    matrix = np.zeros((37, 37))
    np.add.at(matrix, (sub_first, sub_second), 1.0)
    real = _homo_real_stream(code)
    mark = len(real["mapped_chars"]) - 1
    profile = _profile_facts(_glyph_block_matrix(matrix, mark))
    carried = _boundary_carried_pairs(matrix, mark)
    if profile["total_pairs"] != mass - carried:
        raise AssertionError(
            f"cut-geometry/{code}/{language}/rung {rung}: the "
            f"{geometry} row's re-priced block total "
            f"{profile['total_pairs']} does not equal the mass minus "
            f"its boundary-carried pairs {mass} - {carried}"
        )
    if rung == 1.0 and profile != frozen_rung["real_rung_profile"]:
        raise AssertionError(
            f"cut-geometry/{code}/{language}/rung {rung}: the "
            f"{geometry} row's anchor profile is not the degenerate "
            f"whole-sequence identity (the frozen real-at-basis "
            f"ladder's whole-sequence profile)"
        )
    band = [
        {"profile": row["matched_profile"]}
        for row in frozen_mb_rung["members_profiles"]
    ]
    tests = _search_free_envelope(profile, band)
    outside = [key for key, test in tests.items() if not test["inside"]]
    verdict = (
        "shape-consistent-with-homophonic-encoding" if not outside
        else "shape-outside-analogues"
    )
    row = {
        "geometry": geometry,
        "run": rung,
        "cut_mass_pairs": mass,
        "boundary_carried_pairs": carried,
        "profile": profile,
        "invariants": tests,
        "outside_invariants": outside,
        "verdict": verdict,
    }
    if seed_index is not None:
        row["seed_index"] = seed_index
    return row


def _compare_cut_geometry_to_frozen() -> tuple[list[str], int]:
    """The declared bridge gate for the cut-geometry attribution
    instrument, two stages: the real-at-basis ladder's gate exactly
    as that instrument declared it (the matched-basis ladder's 657
    fields plus the real-at-basis ladder's 36 per-cell checks, 693
    fields), then per cell the fresh real-at-basis rung records
    verified against the frozen real-at-basis ladder artifact's rungs
    field for field (each rung's mass, its boundary-carried pairs,
    its prefix profile, its envelope result and its verdict, 5 checks
    per rung, 20 per cell, 120 checks total), 813 fields all told.
    The suffix and random rows carry no frozen counterpart and ride
    on the declared geometry rule, whose mass-match and degenerate
    anchor identities abort on any divergence. Any divergence in any
    stage aborts with nothing written."""
    problems, fields = _compare_real_ladder_to_frozen()
    frozen_m15 = json.loads(REAL_LADDER_ARTIFACT_PATH.read_text())
    frozen_mb = json.loads(SEARCH_FREE_LADDER_ARTIFACT_PATH.read_text())
    for code in FILES:
        for language in LANGS:
            frozen_cell = frozen_m15["files"][code][language]
            fresh = _real_ladder_cell(code, language, frozen_mb)
            for index, rung in enumerate(LADDER_RUNGS):
                frozen_rung = frozen_cell["rungs"][index]
                fresh_rung = fresh["rungs"][index]
                for key in CUT_GEOM_RUNG_KEYS:
                    fields += 1
                    if fresh_rung[key] != frozen_rung[key]:
                        problems.append(
                            f"cut-geometry/rung/{code}/{language}/"
                            f"rung {rung}: the fresh {key} does not "
                            f"equal the frozen real-at-basis ladder "
                            f"rung's"
                        )
    return problems, fields


def substitution_homophonic_cut_geometry() -> dict:
    """The declared cut-geometry attribution instrument: the
    real-at-basis ladder's same rungs, bands and strict-all question,
    with the real's own kept-adjacent pair sequence cut at each
    declared rung's mass under the declared geometries (the standing
    prefix cut, a suffix cut, and the declared seeded random
    submasses of the same masses). The bridge gate runs first; any
    divergence aborts with nothing written."""
    problems, fields = _compare_cut_geometry_to_frozen()
    if problems:
        raise AssertionError(
            "cut-geometry bridge gate failed: " + "; ".join(problems)
        )
    frozen_m15 = json.loads(REAL_LADDER_ARTIFACT_PATH.read_text())
    frozen_mb = json.loads(SEARCH_FREE_LADDER_ARTIFACT_PATH.read_text())
    artifact = {
        "what": "The declared cut-geometry attribution instrument: "
        "the real-at-basis ladder's same state space (1296 ordered "
        "types, the boundary mark's row and column excluded on both "
        "sides), the same four declared rungs, the same frozen rung "
        "bands, and the same six relabeling-invariant summaries, "
        "with the real's own kept-adjacent pair sequence cut at each "
        "rung's mass under six declared geometries: the standing "
        "prefix cut the real-at-basis ladder priced, a suffix cut of "
        "the same mass, and four declared seeded random submasses of "
        "the same mass, every row re-priced through the same "
        "mark-excluded block and priced against its rung's frozen "
        "band under the declared strict-all rule. The declared "
        "truthful question: do same-mass cuts that differ only in "
        "geometry re-price the real the same way, so the real's "
        "deepening concentration is a function of mass alone, or do "
        "they disagree, so the real's own ordering carries it, in "
        "every (file, language) cell at every descended rung. No "
        "mapping is published; nothing here is a reading.",
        "declared": {
            "base_seed": BASE_SEED,
            "mapped": MAPPED_HOMO,
            "boundary_rule": "the word-boundary mark's row and "
            "column are excluded from every profile's state space "
            "on both sides exactly as the boundary-mark "
            "re-instrument declared: every profile is the "
            "mark-excluded block of its pair-count matrix, 1296 "
            "ordered types, the mark located in each matrix's own "
            "alphabet, and the standing alphabet-width disclosure "
            "carries unchanged (the IT real transcription ranks "
            "only 23 glyph types plus the mark, so 13 of its "
            "block's 36 glyph slots are empty by width alone on "
            "the real side while the simulated alphabets are "
            "saturated at 36 in every cell)",
            "cut_geometry_rule": "the real's own kept-adjacent pair "
            "sequence cut to each rung's mass under six declared "
            "geometries, recorded as design before any pricing: "
            "the prefix cut prices the sequence's first mass "
            "positions (the real-at-basis ladder's own row, "
            "verified against that artifact in the gate), the "
            "suffix cut prices the sequence's last mass positions, "
            "and each of the four random rows prices a declared "
            "seed's permutation of the sequence's positions at its "
            "first mass positions, so one seed's rung submasses "
            "are nested subsets; the real's cut under any geometry "
            "can move its own profile both ways, every direction "
            "is open per geometry and per rung, and every row is "
            "recorded with no selection performed",
            "mass_rule": "every geometry row prices its rung's "
            "mass exactly (the rung's basis - 1 pairs, the exact "
            "full-width mass every one of the frozen rung's cut "
            "rows prices), the mass-match identity enforced in "
            "code on every row before any envelope is formed; a "
            "random submass of the real's own pair multiset "
            "samples the multiset's relative frequencies with "
            "sampling noise alone, so its expected profile is the "
            "whole sequence's profile and not the prefix cut's, "
            "and this is the declared attribution arithmetic the "
            "row verdicts are read against",
            "band_reference_rule": "the rung bands are the frozen "
            "matched-basis ladder's rung member profiles taken by "
            "reference, the same bands the real-at-basis ladder "
            "priced: its own gate and tests verified them under "
            "that instrument, the real-at-basis ladder's rung "
            "records are re-derived fresh here and verified field "
            "for field against the frozen real-at-basis ladder "
            "artifact in the gate, and every geometry row's "
            "envelope runs against the frozen rung's member "
            "profiles exactly as that instrument stored them",
            "roster_rule": "the corpus-breadth roster stands "
            "unchanged: the same eight accepted corpus files, the "
            "same rejected candidates with their verbatim causes, "
            "the same sha256 records, the roster floor and the "
            "fetch verification are the corpus-breadth artifact's "
            "declared facts taken by reference, no corpus file is "
            "re-fetched, re-probed or re-hashed here, and no "
            "encoding is re-run on the band side anywhere: the "
            "bands are the frozen instrument's own",
            "invariants": {
                "sorted_symbol_marginals": "the 36 mark-excluded "
                "glyph marginals as a multiset, stored sorted "
                "descending as counts and shares, envelope-tested "
                "by sorted position over 36 positions",
                "sorted_pair_multiset": "the 1296 mark-excluded "
                "pair counts as a multiset, stored sorted "
                "descending as counts and shares, envelope-tested "
                "by sorted position",
                "empty_type_count": "the number of the block's "
                "mark-excluded pair types with zero counted "
                "occurrences, a scalar inside [min, max]",
                "self_pair_share": "the block's diagonal sum over "
                "the profile's glyph-pair total",
                "top_k_shares": "the share of the glyph-pair "
                "total carried by the k largest pair counts, at k "
                "1, 10 and 50",
                "pair_entropy": "the natural entropy of the "
                "mark-excluded pair distribution in nats per "
                "counted glyph pair",
            },
            "state_note": "every band profile here is the frozen "
            "matched-basis ladder's mark-excluded member profile "
            "at its rung width, taken by reference; the real's "
            "geometry rows are priced fresh at every rung from its "
            "own ordered kept-adjacent pair sequence, whose "
            "adjacency is the original stream's with the unmapped "
            "events breaking it (126 unmapped events inside ZL's "
            "218,663, 1,769 inside GC's 186,708, none inside IT's "
            "220,532) exactly as disclosed since the interior "
            "instrument; the real's side is identical for both "
            "languages of a file, so the geometry rows are per "
            "file and the cells price the same rows against their "
            "own bands; the anchor rung's mass is the whole "
            "sequence, every geometry's anchor submass is the "
            "whole sequence, and every geometry's anchor profile "
            "is the frozen whole-sequence profile exactly (the "
            "degenerate identity, enforced in the row builder and "
            "verified in the probes)",
            "machinery_rule": "this instrument contains no "
            "assignment search anywhere: no candidate evaluation, "
            "no restarts, no sweep cap, no convergence flags; the "
            "standing budgets are not applicable and no machinery "
            "recording appears for that reason",
            "split_rule": "no split applies: a profile uses every "
            "counted pair of its declared submass after the "
            "declared exclusion; the climb and score halves of "
            "the band instruments have no counterpart here",
            "seed_kinds": "the declared new seed kind homo_cut_geom "
            "(id 30), positions 0 to 3, per file with the language "
            "slot fixed at 0 because the real's side is identical "
            "for both languages of a file: each seed index derives "
            "one declared permutation of the real's pair-sequence "
            "positions and the rung's submass is that permutation's "
            "first mass positions, so one seed's rung submasses "
            "are nested subsets and no selection is performed over "
            "seeds; the bands and the prefix rows consume no seed "
            "(the prefix rows are the frozen real-at-basis "
            "ladder's own rows verified in the gate, and the "
            "band side is the frozen instruments' facts taken by "
            "reference)",
            "record_rule": "per cell the artifact records the "
            "real-at-basis ladder's cell record re-derived fresh "
            "(verified against the frozen real-at-basis ladder "
            "artifact in the gate) and the four declared rungs in "
            "order (the anchor rung first, then 75, 50 and 25 "
            "percent), each rung carrying the prefix row's full "
            "real-at-basis record (its run percentage, its basis, "
            "the real's rung mass, the rung's boundary-carried "
            "pairs, the re-priced profile, its envelope tests, "
            "its outside list and its verdict) and a geometries "
            "list of the five fresh rows (the suffix cut first, "
            "then the four random seeds in declared order), each "
            "row carrying its geometry, its seed index when "
            "random, its cut mass, its boundary-carried pairs, "
            "its re-priced profile, its envelope tests, its "
            "outside list and its verdict; the rung's member band "
            "itself is not re-stored here: it stays the frozen "
            "instrument's declared record",
            "verdict_rule": "declared strict-all, unchanged, "
            "priced per geometry row per rung: a geometry rung-cell "
            "is shape-consistent-with-homophonic-encoding only "
            "when every declared invariant of that row's "
            "re-priced glyph-block profile sits inside the closed "
            "range of its rung's matched band's glyph-block "
            "profiles (the two vector summaries term by term "
            "inside the band's per-position envelope over 36 "
            "sorted positions, the scalar summaries inside "
            "[min, max] at the stored 6-decimal rounding); any "
            "outside invariant makes the row shape-outside-"
            "analogues, every outside entry is recorded with its "
            "band range so the miss is audited not summarized, "
            "and the declared question is asked over all 144 "
            "geometry rung-cell verdicts together (24 rung-cells "
            "times the six geometries, the anchor rung's 24 the "
            "declared degenerate identity cases)",
            "closure_rule": "no scalar margin is formed: this "
            "instrument's question is inside or outside per "
            "invariant per geometry row per rung, and the "
            "recorded distances are the outside entries' band "
            "ranges themselves",
            "exclusion_rule": "the family's declared exclusion "
            "format is not re-scoped by this artifact: it keys "
            "to the declared 36-slot class under the inherited "
            "add-one form exactly as the held-out screen "
            "declared it, so a search-free verdict is structure "
            "evidence and the band instruments' verdicts stand "
            "untouched by this artifact's numbers",
            "bridge_gate_rule": "before any rung is priced, the "
            "gate verified fresh in two stages: the real-at-basis "
            "ladder's gate exactly as that instrument declared it "
            "(the matched-basis ladder's 657 fields plus the "
            "real-at-basis ladder's 36 per-cell checks, 693 "
            "fields), then per cell the fresh real-at-basis rung "
            "records verified against the frozen real-at-basis "
            "ladder artifact's rungs field for field (each "
            "rung's mass, its boundary-carried pairs, its prefix "
            "profile, its envelope result and its verdict, 5 "
            "checks per rung, 20 per cell, 120 checks total), "
            "813 fields all told; the suffix and random rows "
            "carry no frozen counterpart and ride on the "
            "declared geometry rule, whose mass-match and "
            "degenerate anchor identities abort on any "
            "divergence; any divergence aborts with nothing "
            "written",
            "models_rule": "no score table is built or used: "
            "the instrument prices count structure only, so the "
            "standing add-one and leave-one-out tables play no "
            "part anywhere in this artifact",
        },
        "bridge_gate": {
            "status": "verified",
            "fields_compared": fields,
            "ladder_gate_fields": 693,
            "geometry_replay_checks": fields - 693,
        },
        "files": {},
    }
    for code in FILES:
        cell = {}
        for language in LANGS:
            fresh = _real_ladder_cell(code, language, frozen_mb)
            for index, rung in enumerate(LADDER_RUNGS):
                rung_record = fresh["rungs"][index]
                rows = [
                    _real_geometry_row(
                        code, language, rung, "suffix", None,
                        frozen_m15, frozen_mb,
                    )
                ]
                for seed_index in range(N_CUT_SEEDS):
                    rows.append(
                        _real_geometry_row(
                            code, language, rung, "random",
                            seed_index, frozen_m15, frozen_mb,
                        )
                    )
                rung_record["geometries"] = rows
            cell[language] = fresh
        artifact["files"][code] = cell
    return artifact


def main_cut_geometry() -> None:
    artifact = substitution_homophonic_cut_geometry()
    CUT_GEOM_ARTIFACT_PATH.write_text(
        json.dumps(artifact, indent=2) + "\n"
    )
    print(CUT_GEOM_ARTIFACT_PATH)


# --------------------------------------------------------------------------
# The seventeenth declared measurement, the stream-position instrument:
# the real's own kept-adjacent pair sequence divided into four declared
# equal-count consecutive segments, each segment's profile priced fresh
# through the same mark-excluded block and the same six summaries, the
# four segment profiles recorded beside each other and beside the
# whole-sequence profile, no bands, no envelopes and no margin formed.
# --------------------------------------------------------------------------

STREAM_QUARTERS = (0.25, 0.5, 0.75, 1.0)

STREAM_POS_ARTIFACT_PATH = (
    Path(DATA_DIR).resolve().parent.parent.parent
    / "docs" / "research-notes"
    / "voynich-homophonic-stream-positions.json"
)

STREAM_SCALARS = (
    "empty_type_count", "self_pair_share", "top_1_share",
    "top_10_share", "top_50_share", "pair_entropy",
)


def _stream_bounds(total: int) -> list[int]:
    """The declared segment boundaries for one file's kept pair
    sequence of the given total: the standing basis arithmetic the
    rungs already use, applied at the four quarters - the first three
    boundaries sit at int(quarter x the anchor basis) positions with
    the anchor basis the kept pair total + 1, and the last boundary
    is the sequence's end. Every file's kept pair total is three over
    a multiple of four, so the first three segments come out the same
    size and the remainder lands on the last segment."""
    if total % 4 != 3:
        raise AssertionError(
            f"stream-position: the kept pair total {total} is not "
            f"three over a multiple of four"
        )
    anchor = total + 1
    bounds = [int(q * anchor) for q in STREAM_QUARTERS[:-1]]
    bounds.append(total)
    for earlier, later in zip(bounds, bounds[1:]):
        if later <= earlier:
            raise AssertionError(
                f"stream-position: the declared boundaries {bounds} "
                f"are not increasing for the total {total}"
            )
    return bounds


def _direction_vs_whole(
    profile: dict, whole_profile: dict,
) -> dict:
    """The declared direction device for one segment profile against
    the whole sequence's profile: for each of the six scalar
    summaries the two profiles share, whether the segment's value
    sits above, below or equal to the whole sequence's value at the
    stored 6-decimal rounding. Every entry is recorded; no margin is
    formed."""
    record = {}
    for key in STREAM_SCALARS:
        value = profile[key]
        base = whole_profile[key]
        record[key] = (
            "above" if value > base
            else "below" if value < base else "equal"
        )
    return record


def _stream_position_profiles(code: str) -> dict:
    """One file's declared stream-position records: the real's ordered
    kept-adjacent pair sequence divided into four declared equal-count
    consecutive segments by the declared boundaries, each segment's
    own pairs priced fresh through the same mark-excluded block and
    the same six relabeling-invariant summaries, the four segment
    profiles recorded beside each other and beside the whole
    sequence's profile priced fresh the same way. No band is loaded,
    no envelope is formed and no margin is produced anywhere in this
    builder; the direction device is the artifact's answer format.
    Every segment's block-total identity (its profile total equals
    its own kept pairs minus its own boundary-carried pairs) is
    enforced here and the whole profile's identity too; any
    divergence aborts."""
    first, second = _real_pair_sequence(code)
    total = int(len(first))
    real = _homo_real_stream(code)
    mark = len(real["mapped_chars"]) - 1
    bounds = _stream_bounds(total)

    whole_matrix = np.zeros((37, 37))
    np.add.at(whole_matrix, (first, second), 1.0)
    whole_profile = _profile_facts(
        _glyph_block_matrix(whole_matrix, mark)
    )
    whole_carried = _boundary_carried_pairs(whole_matrix, mark)
    if whole_profile["total_pairs"] != total - whole_carried:
        raise AssertionError(
            f"stream-position/{code}: the whole profile's block "
            f"total {whole_profile['total_pairs']} does not equal "
            f"the kept pairs {total} minus the whole's "
            f"boundary-carried pairs {whole_carried}"
        )

    segments = []
    previous = 0
    for index, bound in enumerate(bounds):
        take = np.arange(previous, bound)
        size = int(len(take))
        matrix = np.zeros((37, 37))
        np.add.at(matrix, (first[take], second[take]), 1.0)
        profile = _profile_facts(_glyph_block_matrix(matrix, mark))
        carried = _boundary_carried_pairs(matrix, mark)
        if profile["total_pairs"] != size - carried:
            raise AssertionError(
                f"stream-position/{code}/segment {index}: the "
                f"segment's block total {profile['total_pairs']} "
                f"does not equal its kept pairs {size} minus its "
                f"boundary-carried pairs {carried}"
            )
        segments.append({
            "segment": index,
            "first_position": previous,
            "end_position": bound,
            "pairs": size,
            "boundary_carried_pairs": carried,
            "profile": profile,
            "direction": _direction_vs_whole(profile, whole_profile),
        })
        previous = bound

    size_sum = sum(segment["pairs"] for segment in segments)
    if size_sum != total:
        raise AssertionError(
            f"stream-position/{code}: the four segments price "
            f"{size_sum} pairs, not the whole sequence's {total}"
        )
    total_sum = sum(
        segment["profile"]["total_pairs"] for segment in segments
    )
    if total_sum != whole_profile["total_pairs"]:
        raise AssertionError(
            f"stream-position/{code}: the four segments' block "
            f"totals sum to {total_sum}, not the whole profile's "
            f"{whole_profile['total_pairs']}"
        )
    carried_sum = sum(
        segment["boundary_carried_pairs"] for segment in segments
    )
    if carried_sum != whole_carried:
        raise AssertionError(
            f"stream-position/{code}: the four segments' "
            f"boundary-carried pairs sum to {carried_sum}, not the "
            f"whole's {whole_carried}"
        )
    return {
        "kept_pairs": total,
        "boundaries": bounds,
        "whole_profile": whole_profile,
        "whole_boundary_carried_pairs": whole_carried,
        "segments": segments,
    }


def _compare_stream_positions_to_frozen() -> tuple[list[str], int]:
    """The declared bridge gate for the stream-position instrument,
    per cell: the fresh whole-sequence profile verified field for
    field against the frozen real-at-basis ladder's anchor profile,
    the four boundaries recomputed from the declared rule and
    verified, the four segment sizes verified, each segment's
    block-total identity verified, the two partition identities
    verified (the four segments' block totals and their
    boundary-carried counts against the whole's), the four segments'
    kept pairs' sum verified against the whole's, and the whole's
    own block-total identity verified, 17 fields per cell, 102
    fields all told. Any divergence aborts with nothing written."""
    frozen_m15 = json.loads(REAL_LADDER_ARTIFACT_PATH.read_text())
    problems: list[str] = []
    fields = 0
    for code in FILES:
        for language in LANGS:
            fresh = _stream_position_profiles(code)
            frozen_profile = frozen_m15["files"][code][language][
                "rungs"
            ][0]["real_rung_profile"]
            total = fresh["kept_pairs"]
            first, second = _real_pair_sequence(code)
            if total != int(len(first)):
                raise AssertionError(
                    f"stream-position/{code}: the fresh kept pair "
                    f"total does not equal the sequence's length"
                )
            fields += 1
            if fresh["whole_profile"] != frozen_profile:
                problems.append(
                    f"stream-position/whole/{code}/{language}: the "
                    f"fresh whole profile does not equal the frozen "
                    f"real-at-basis ladder's anchor profile"
                )
            declared_bounds = _stream_bounds(total)
            for index in range(4):
                fields += 1
                if fresh["boundaries"][index] != declared_bounds[index]:
                    problems.append(
                        f"stream-position/{code}/{language}/segment "
                        f"{index}: the boundary does not equal the "
                        f"declared rule's"
                    )
            previous = 0
            for index in range(4):
                segment = fresh["segments"][index]
                fields += 1
                if segment["pairs"] != fresh["boundaries"][index] - previous:
                    problems.append(
                        f"stream-position/{code}/{language}/segment "
                        f"{index}: the segment's pairs do not equal "
                        f"its declared interval's width"
                    )
                previous = fresh["boundaries"][index]
            for index in range(4):
                segment = fresh["segments"][index]
                fields += 1
                if (
                    segment["profile"]["total_pairs"]
                    != segment["pairs"]
                    - segment["boundary_carried_pairs"]
                ):
                    problems.append(
                        f"stream-position/{code}/{language}/segment "
                        f"{index}: the segment's block total does "
                        f"not equal its kept pairs minus its "
                        f"boundary-carried pairs"
                    )
            fields += 1
            size_sum = sum(
                segment["pairs"] for segment in fresh["segments"]
            )
            if size_sum != total:
                problems.append(
                    f"stream-position/{code}/{language}: the four "
                    f"segments' pairs do not sum to the whole "
                    f"sequence's"
                )
            fields += 1
            total_sum = sum(
                segment["profile"]["total_pairs"]
                for segment in fresh["segments"]
            )
            if total_sum != fresh["whole_profile"]["total_pairs"]:
                problems.append(
                    f"stream-position/{code}/{language}: the four "
                    f"segments' block totals do not sum to the "
                    f"whole profile's"
                )
            fields += 1
            carried_sum = sum(
                segment["boundary_carried_pairs"]
                for segment in fresh["segments"]
            )
            if carried_sum != fresh["whole_boundary_carried_pairs"]:
                problems.append(
                    f"stream-position/{code}/{language}: the four "
                    f"segments' boundary-carried pairs do not sum "
                    f"to the whole's"
                )
            fields += 1
            if fresh["whole_profile"]["total_pairs"] != (
                total - fresh["whole_boundary_carried_pairs"]
            ):
                problems.append(
                    f"stream-position/{code}/{language}: the whole "
                    f"profile's block total does not equal the kept "
                    f"pairs minus the whole's boundary-carried pairs"
                )
    return problems, fields


def substitution_homophonic_stream_positions() -> dict:
    """The declared stream-position instrument: the real's own
    kept-adjacent pair sequence divided into four declared
    equal-count consecutive segments, each segment's profile priced
    fresh through the same mark-excluded block and the same six
    summaries, the four segment profiles recorded beside each other
    and beside the whole-sequence profile, no bands and no envelopes.
    The bridge gate runs first; any divergence aborts with nothing
    written."""
    problems, fields = _compare_stream_positions_to_frozen()
    if problems:
        raise AssertionError(
            "stream-position bridge gate failed: " + "; ".join(problems)
        )
    artifact = {
        "what": "The declared stream-position instrument: the "
        "state space 1296 ordered types with the boundary mark's row "
        "and column excluded on both sides and the same six "
        "relabeling-invariant summaries, with the real's own "
        "kept-adjacent pair sequence divided into four declared "
        "equal-count consecutive segments, each segment's profile "
        "priced fresh, the four segment profiles recorded beside "
        "each other and beside the whole-sequence profile, no bands "
        "and no envelopes. The declared truthful question: is the "
        "real's concentration a smooth function of stream position, "
        "or do particular spans of the stream carry it, answered by "
        "which segments' scalars sit above the whole-sequence values "
        "and which below, the span effect the cut-geometry "
        "instrument attributed to the stream's opening pairs. No "
        "mapping is published; nothing here is a reading.",
        "declared": {
            "base_seed": BASE_SEED,
            "mapped": MAPPED_HOMO,
            "boundary_rule": "the word-boundary mark's row and "
            "column are excluded from every profile's state space "
            "on both sides exactly as the boundary-mark "
            "re-instrument declared: every profile is the "
            "mark-excluded block of its pair-count matrix, 1296 "
            "ordered types, the mark located in each matrix's own "
            "alphabet, and the standing alphabet-width disclosure "
            "carries unchanged (the IT real transcription ranks "
            "only 23 glyph types plus the mark, so 13 of its "
            "block's 36 glyph slots are empty by width alone on "
            "the real side)",
            "partition_rule": "the real's own ordered kept-adjacent "
            "pair sequence divided into four declared equal-count "
            "consecutive segments, the boundaries placed by the "
            "standing basis arithmetic the rungs already use (the "
            "first three boundaries at int(quarter x the anchor "
            "basis) positions with the anchor basis the kept pair "
            "total + 1, at the quarters 0.25, 0.5 and 0.75, the "
            "last boundary the sequence's end); every file's kept "
            "pair total is three over a multiple of four, so each "
            "file's first three segments are the same size and the "
            "remainder lands on the last segment; each segment "
            "prices every kept-adjacent pair of its own consecutive "
            "interval, no pair dropped, no pair synthesized, and "
            "the four segments partition the whole sequence exactly",
            "summary_rule": "each profile is priced fresh through "
            "the same mark-excluded block and the same six "
            "relabeling-invariant summaries the standing "
            "instruments declare, each segment's own matrix "
            "carrying its own mark's row and column excluded; no "
            "profile is compared to any simulated profile anywhere "
            "in this artifact",
            "no_band_rule": "no rung band is loaded, no envelope is "
            "formed, no verdict and no scalar margin is produced "
            "anywhere in this artifact: the declared question is "
            "answered by direction, and the frozen rung bands stay "
            "the frozen instruments' declared records, untouched "
            "here",
            "direction_rule": "each segment records, for each of "
            "the six scalar summaries it shares with the whole "
            "profile (the empty type count, the self-pair share, "
            "the top-k shares at k 1, 10 and 50, and the pair "
            "entropy), whether its value sits above, below or equal "
            "to the whole sequence's value at the stored 6-decimal "
            "rounding, every entry recorded and no selection "
            "performed over anything",
            "roster_rule": "the corpus-breadth roster stands "
            "unchanged: the same eight accepted corpus files, the "
            "same rejected candidates with their verbatim causes, "
            "the same sha256 records, the roster floor and the "
            "fetch verification are the corpus-breadth artifact's "
            "declared facts taken by reference, no corpus file is "
            "re-fetched, re-probed or re-hashed here, and no "
            "encoding is re-run anywhere: this instrument prices "
            "the real's own side only",
            "state_note": "the real's kept-adjacency is real "
            "adjacency with 126 unmapped events inside ZL's "
            "218,663, 1,769 inside GC's 186,708, none inside IT's "
            "220,532, exactly as disclosed since the interior "
            "instrument; the real's side is identical for both "
            "languages of a file, so every cell prices the same "
            "segment records; the whole-sequence profile is priced "
            "fresh here and verified field for field against the "
            "frozen real-at-basis ladder's anchor profile in the "
            "gate",
            "machinery_rule": "this instrument contains no "
            "assignment search anywhere: no candidate evaluation, "
            "no restarts, no sweep cap, no convergence flags, and "
            "no seed of any kind: the segments are the declared "
            "consecutive quarters and every profile is priced fresh "
            "from the real's own pair sequence, so the standing "
            "budgets and the seed-kind registry play no part here",
            "split_rule": "no split applies: a profile uses every "
            "counted pair of its declared segment after the "
            "declared exclusion; the climb and score halves of the "
            "band instruments have no counterpart here",
            "record_rule": "per cell the artifact records the kept "
            "pair total, the four declared boundaries, the whole "
            "sequence's profile priced fresh with its "
            "boundary-carried pairs, and the four segment records "
            "in order, each carrying its segment index, its first "
            "and end positions, its kept-adjacent pairs, its own "
            "boundary-carried pairs, its fresh profile (the block "
            "total, both vector summaries as counts and shares, "
            "the empty type count, the self-pair share, the top-k "
            "shares and the pair entropy) and its direction record "
            "against the whole profile's six scalar summaries, "
            "every entry recorded",
            "closure_rule": "no scalar margin is formed: this "
            "instrument's question is direction per scalar summary "
            "per segment, and the record answers it entry by entry",
            "exclusion_rule": "the family's declared exclusion "
            "format is not re-scoped by this artifact: it keys to "
            "the declared 36-slot class under the inherited "
            "add-one form exactly as the held-out screen declared "
            "it, so a search-free verdict is structure evidence and "
            "the band instruments' verdicts stand untouched by "
            "this artifact's numbers",
            "gate_rule": "before any segment is recorded, the "
            "gate verified fresh per cell: the whole profile "
            "against the frozen real-at-basis ladder's anchor "
            "profile, the four boundaries from the declared rule, "
            "the four segment sizes, each segment's block-total "
            "identity, the two partition identities, the four "
            "segments' kept pairs' sum and the whole's own "
            "identity, 17 fields per cell, 102 fields all told; "
            "any divergence aborts with nothing written",
            "models_rule": "no score table is built or used: the "
            "instrument prices count structure only, so the "
            "standing add-one and leave-one-out tables play no "
            "part anywhere in this artifact",
        },
        "bridge_gate": {
            "status": "verified",
            "fields_compared": fields,
            "per_cell_fields": 17,
        },
        "files": {},
    }
    for code in FILES:
        artifact["files"][code] = {}
        for language in LANGS:
            artifact["files"][code][language] = (
                _stream_position_profiles(code)
            )
    return artifact


def main_stream_positions() -> None:
    artifact = substitution_homophonic_stream_positions()
    STREAM_POS_ARTIFACT_PATH.write_text(
        json.dumps(artifact, indent=2) + "\n"
    )
    print(STREAM_POS_ARTIFACT_PATH)

# --------------------------------------------------------------------------
# The eighteenth declared measurement, the boundary-walk instrument:
# the real's own kept-adjacent pair sequence walked by one declared
# boundary head at declared step positions between the stream's first and
# second declared boundaries, the two window-mass spans beside the head
# priced fresh at every position through the same mark-excluded block and
# the same six summaries, the direction tables recorded at every head,
# no bands, no envelopes and no margin formed.
# --------------------------------------------------------------------------

STREAM_WALK_STEP_DENOM = 100
STREAM_WALK_HEAD_STEPS = tuple(
    j / STREAM_WALK_STEP_DENOM for j in range(25, 51)
)
STREAM_WALK_FIRST_STEP = 25
STREAM_WALK_LAST_STEP = 50

STREAM_WALK_ARTIFACT_PATH = (
    Path(DATA_DIR).resolve().parent.parent.parent
    / "docs" / "research-notes"
    / "voynich-homophonic-boundary-walk.json"
)


def _walk_heads(total: int) -> list[int]:
    """The declared head positions for one file's kept pair sequence of
    the given total: int(step x the anchor basis) for the declared steps
    j / 100 with j running 25 to 50 inclusive, the anchor basis the kept
    pair total + 1. The first head sits exactly at the standing first
    boundary and the last head exactly at the standing second
    boundary."""
    anchor = total + 1
    heads = [int(step * anchor) for step in STREAM_WALK_HEAD_STEPS]
    standing = _stream_bounds(total)
    if heads[0] != standing[0] or heads[-1] != standing[1]:
        raise AssertionError(
            f"boundary-walk: the head endpoints {heads[0]} and "
            f"{heads[-1]} are not the standing first and second "
            f"boundaries for the total {total}"
        )
    for earlier, later in zip(heads, heads[1:]):
        if later <= earlier:
            raise AssertionError(
                "boundary-walk: the declared heads are not increasing"
            )
    return heads


def _walk_cell(
    code: str, frozen_m17_cell: dict,
) -> dict:
    """One cell's declared walk records: the declared head positions
    and, at every head, the two window-mass spans beside the head
    priced fresh through the same mark-excluded block and the same six
    relabeling-invariant summaries, each span carrying its own
    direction table against the whole-sequence profile, every entry
    recorded. Every span's block-total identity (its profile total
    equals its window mass minus its own boundary-carried pairs) is
    enforced here, and any divergence aborts. No band is loaded, no
    envelope is formed and no margin is produced anywhere in this
    builder."""
    first, second = _real_pair_sequence(code)
    real = _homo_real_stream(code)
    mark = len(real["mapped_chars"]) - 1
    total = int(len(first))
    whole_profile = frozen_m17_cell["whole_profile"]
    heads = _walk_heads(total)
    mass = _stream_bounds(total)[0]
    rows = []
    for index, head in enumerate(heads):
        row = {
            "step": STREAM_WALK_HEAD_STEPS[index],
            "head_position": head,
        }
        for side, start in (
            ("left", head - mass),
            ("right", head),
        ):
            take = np.arange(start, start + mass)
            if int(len(take)) != mass:
                raise AssertionError(
                    f"boundary-walk/{code}/head {index}/{side}: the "
                    f"span does not carry the declared window mass"
                )
            matrix = np.zeros((37, 37))
            np.add.at(matrix, (first[take], second[take]), 1.0)
            profile = _profile_facts(_glyph_block_matrix(matrix, mark))
            carried = _boundary_carried_pairs(matrix, mark)
            if profile["total_pairs"] != mass - carried:
                raise AssertionError(
                    f"boundary-walk/{code}/head {index}/{side}: the "
                    f"span's block total {profile['total_pairs']} "
                    f"does not equal the window mass {mass} minus "
                    f"its boundary-carried pairs {carried}"
                )
            row[side] = {
                "first_position": int(start),
                "end_position": int(start + mass),
                "pairs": int(mass),
                "boundary_carried_pairs": carried,
                "profile": profile,
                "direction": _direction_vs_whole(
                    profile, whole_profile,
                ),
            }
        rows.append(row)
    return {
        "kept_pairs": total,
        "window_pairs": mass,
        "whole_profile": whole_profile,
        "whole_boundary_carried_pairs": frozen_m17_cell[
            "whole_boundary_carried_pairs"
        ],
        "stream_position_boundaries": frozen_m17_cell["boundaries"],
        "heads": rows,
    }


def _compare_boundary_walk_to_frozen() -> tuple[list[str], int]:
    """The declared bridge gate for the boundary-walk instrument,
    per cell: the whole profile re-anchored to the frozen real-at-basis
    ladder's anchor profile, the fresh stream-position boundaries and
    sizes verified against the frozen stored ones, the 26 heads
    recomputed from the declared rule and verified one field each, the
    two window sizes verified at every head one field each, the first
    head's two span profiles verified against the frozen
    stream-position stored first and second segment profiles and the
    last head's two span profiles against its stored second and third,
    and the whole's own block-total identity verified. Any divergence
    aborts with nothing written."""
    frozen_m17 = json.loads(STREAM_POS_ARTIFACT_PATH.read_text())
    frozen_m15 = json.loads(REAL_LADDER_ARTIFACT_PATH.read_text())
    problems: list[str] = []
    fields = 0
    for code in FILES:
        for language in LANGS:
            frozen_cell = frozen_m17["files"][code][language]
            mass = frozen_cell["segments"][0]["pairs"]
            fresh = _walk_cell(code, frozen_cell)
            heads = _walk_heads(fresh["kept_pairs"])
            frozen_profile = frozen_m15["files"][code][language][
                "rungs"
            ][0]["real_rung_profile"]
            fields += 1
            if fresh["whole_profile"] != frozen_profile:
                problems.append(
                    f"boundary-walk/whole/{code}/{language}: the "
                    f"whole profile is not the frozen real-at-basis "
                    f"ladder's anchor profile"
                )
            fields += 1
            if fresh["stream_position_boundaries"] != (
                frozen_cell["boundaries"]
            ):
                problems.append(
                    f"boundary-walk/{code}/{language}: the fresh "
                    f"stream-position boundaries do not equal the "
                    f"frozen stored ones"
                )
            fields += 1
            if [
                segment["pairs"]
                for segment in frozen_cell["segments"]
            ] != [mass] * 3 + [frozen_cell["kept_pairs"] - 3 * mass]:
                problems.append(
                    f"boundary-walk/{code}/{language}: the frozen "
                    f"stream-position sizes do not fit the declared "
                    f"window and remainder arithmetic"
                )
            for index in range(len(heads)):
                row = fresh["heads"][index]
                fields += 1
                if row["head_position"] != heads[index]:
                    problems.append(
                        f"boundary-walk/{code}/{language}/head "
                        f"{index}: the head does not equal the "
                        f"declared rule's"
                    )
                fields += 1
                if row["left"]["pairs"] != mass:
                    problems.append(
                        f"boundary-walk/{code}/{language}/head "
                        f"{index}: the left span's window size "
                        f"differs from the declared one"
                    )
                fields += 1
                if row["right"]["pairs"] != mass:
                    problems.append(
                        f"boundary-walk/{code}/{language}/head "
                        f"{index}: the right span's window size "
                        f"differs from the declared one"
                    )
            confluence = (
                (0, fresh["heads"][0]["left"],
                 frozen_cell["segments"][0]["profile"]),
                (0, fresh["heads"][0]["right"],
                 frozen_cell["segments"][1]["profile"]),
                (len(heads) - 1, fresh["heads"][-1]["left"],
                 frozen_cell["segments"][1]["profile"]),
                (len(heads) - 1, fresh["heads"][-1]["right"],
                 frozen_cell["segments"][2]["profile"]),
            )
            for head_index, span, frozen_segment_profile in confluence:
                fields += 1
                if span["profile"] != frozen_segment_profile:
                    problems.append(
                        f"boundary-walk/{code}/{language}/head "
                        f"{head_index}: the span's fresh profile "
                        f"does not equal the frozen stream-position "
                        f"segment profile"
                    )
            fields += 1
            if fresh["whole_profile"]["total_pairs"] != (
                fresh["kept_pairs"]
                - fresh["whole_boundary_carried_pairs"]
            ):
                problems.append(
                    f"boundary-walk/{code}/{language}: the whole "
                    f"profile's block total does not equal the kept "
                    f"pairs minus the whole's boundary-carried pairs"
                )
    return problems, fields


def substitution_homophonic_boundary_walk() -> dict:
    """The declared boundary-walk instrument: the two declared
    window-mass spans beside every declared head priced fresh through
    the same mark-excluded block and the same six summaries, the
    direction tables recorded at every head, no bands and no
    envelopes. The bridge gate runs first; any divergence aborts with
    nothing written."""
    problems, fields = _compare_boundary_walk_to_frozen()
    if problems:
        raise AssertionError(
            "boundary-walk bridge gate failed: " + "; ".join(problems)
        )
    artifact = {
        "what": "The declared boundary-walk instrument: the state "
        "space 1296 ordered types with the boundary mark's row and "
        "column excluded on both sides and the same six "
        "relabeling-invariant summaries, with the real's own "
        "kept-adjacent pair sequence walked by one declared boundary "
        "head across declared step positions between the stream's "
        "first and second declared boundaries, the two window-mass "
        "spans beside the head priced fresh at every position, the "
        "direction tables recorded at every position, no bands and "
        "no envelopes. The declared truthful questions: where the "
        "second span's top_1 spike begins and ends along the stream, "
        "and whether the opening span's above-whole concentration "
        "turns off at a declared location or drifts smoothly across "
        "positions, the flip locations the stream-position "
        "instrument left to within a quarter of the stream. No "
        "mapping is published; nothing here is a reading.",
        "declared": {
            "base_seed": BASE_SEED,
            "mapped": MAPPED_HOMO,
            "boundary_rule": "the word-boundary mark's row and "
            "column are excluded from every profile's state space "
            "on both sides exactly as the boundary-mark "
            "re-instrument and the stream-position instrument "
            "declared: every profile is the mark-excluded block "
            "of its pair-count matrix, 1296 ordered types, and "
            "the standing alphabet-width disclosure carries "
            "unchanged (the IT real transcription ranks only 23 "
            "glyph types plus the mark, so 13 of its block's 36 "
            "glyph slots are empty by width alone on the real "
            "side)",
            "walk_rule": "the window mass fixed at the standing "
            "basis arithmetic's first boundary - the int(quarter x "
            "the anchor basis) positions with the anchor basis the "
            "kept pair total + 1, so the window mass is ZL 54,604, "
            "GC 45,800 and IT 55,133 kept-adjacent pairs - and the "
            "head walked at int(step x the anchor basis) positions "
            "for the declared steps j / 100 with j running 25 to 50 "
            "inclusive, 26 heads per file, the first head exactly "
            "the standing first boundary and the last head exactly "
            "the standing second boundary; at every head the two "
            "spans beside the head are the window-mass span ending "
            "at the head and the window-mass span starting at the "
            "head, each priced fresh, no pair dropped, no pair "
            "synthesized, and the first head's two spans are "
            "exactly the stream-position instrument's first and "
            "second segments while the last head's two spans are "
            "exactly its second and third",
            "summary_rule": "each profile is priced fresh through "
            "the same mark-excluded block and the same six "
            "relabeling-invariant summaries the standing "
            "instruments declare; no profile is compared to any "
            "simulated profile anywhere in this artifact",
            "no_band_rule": "no rung band is loaded, no envelope "
            "is formed, no verdict and no scalar margin is "
            "produced anywhere in this artifact: the declared "
            "question is answered by direction, and the frozen "
            "rung bands stay the frozen instruments' declared "
            "records, untouched here",
            "direction_rule": "each span records, for each of the "
            "six scalar summaries it shares with the whole "
            "profile (the empty type count, the self-pair share, "
            "the top-k shares at k 1, 10 and 50, and the pair "
            "entropy), whether its value sits above, below or "
            "equal to the whole sequence's value at the stored "
            "6-decimal rounding, every entry recorded and no "
            "selection performed over anything",
            "roster_rule": "the corpus-breadth roster stands "
            "unchanged: the same eight accepted corpus files, "
            "the same rejected candidates with their verbatim "
            "causes, the same sha256 records, the roster floor "
            "and the fetch verification are the corpus-breadth "
            "artifact's declared facts taken by reference, no "
            "corpus file is re-fetched, re-probed or re-hashed "
            "here, and no encoding is re-run anywhere: this "
            "instrument prices the real's own side only",
            "state_note": "the real's kept-adjacency is real "
            "adjacency with 126 unmapped events inside ZL's "
            "218,663, 1,769 inside GC's 186,708, none inside "
            "IT's 220,532, exactly as disclosed since the "
            "interior instrument; the real's side is identical "
            "for both languages of a file, so every cell prices "
            "the same walk records; the whole-sequence profile "
            "is anchored to the frozen real-at-basis ladder's "
            "anchor profile in the gate",
            "machinery_rule": "this instrument contains no "
            "assignment search anywhere: no candidate "
            "evaluation, no restarts, no sweep cap, no "
            "convergence flags, and no seed of any kind: the "
            "heads are the declared arithmetic and every profile "
            "is priced fresh from the real's own pair sequence, "
            "so the standing budgets and the seed-kind registry "
            "play no part here",
            "split_rule": "no split applies: a profile uses "
            "every counted pair of its declared window after "
            "the declared exclusion; the climb and score halves "
            "of the band instruments have no counterpart here",
            "record_rule": "per cell the artifact records the "
            "kept pair total, the window mass, the "
            "whole-sequence profile with its boundary-carried "
            "pairs, the frozen stream-position boundaries taken "
            "by reference, and the 26 head records in order, "
            "each carrying its declared step, its head position, "
            "and its two spans, each span carrying its first and "
            "end positions, its window mass, its own "
            "boundary-carried pairs, its fresh profile (the "
            "block total, both vector summaries as counts and "
            "shares, the empty type count, the self-pair share, "
            "the top-k shares and the pair entropy) and its "
            "direction record against the whole profile's six "
            "scalar summaries, every entry recorded",
            "closure_rule": "no scalar margin is formed: this "
            "instrument's question is the direction run at every "
            "declared head per span, and the record answers it "
            "entry by entry",
            "exclusion_rule": "the family's declared exclusion "
            "format is not re-scoped by this artifact: it keys "
            "to the declared 36-slot class under the inherited "
            "add-one form exactly as the held-out screen "
            "declared it, so a search-free verdict is structure "
            "evidence and the band instruments' verdicts stand "
            "untouched by this artifact's numbers",
            "gate_rule": "before any span at any declared head "
            "is recorded beyond the gate, the gate verified "
            "fresh per cell: the whole profile against the "
            "frozen real-at-basis ladder's anchor profile, the "
            "fresh stream-position boundaries and sizes against "
            "the frozen stored ones, the 26 heads against the "
            "declared rule, the two window sizes at every "
            "head, the first head's two spans against the "
            "frozen stream-position first and second segment "
            "profiles and the last head's against its second "
            "and third, and the whole's own identity, 86 fields "
            "per cell, 516 fields all told; any divergence "
            "aborts with nothing written",
            "confluence_rule": "the walk's endpoints are the "
            "stream-position instrument's frozen records taken "
            "by reference and verified field for field in the "
            "gate: the first head's left span is that "
            "instrument's first segment and its right span the "
            "second, the last head's left span the second "
            "segment and its right span the third, so the walk "
            "begins and ends inside the stream-position "
            "instrument's declared partition and its heads are "
            "declared arithmetic in between",
            "models_rule": "no score table is built or used: "
            "the instrument prices count structure only, so "
            "the standing add-one and leave-one-out tables "
            "play no part anywhere in this artifact",
        },
        "bridge_gate": {
            "status": "verified",
            "fields_compared": fields,
            "per_cell_fields": 86,
        },
        "files": {},
    }
    frozen_m17 = json.loads(STREAM_POS_ARTIFACT_PATH.read_text())
    for code in FILES:
        artifact["files"][code] = {}
        for language in LANGS:
            artifact["files"][code][language] = _walk_cell(
                code, frozen_m17["files"][code][language],
            )
    return artifact


def main_boundary_walk() -> None:
    artifact = substitution_homophonic_boundary_walk()
    STREAM_WALK_ARTIFACT_PATH.write_text(
        json.dumps(artifact, indent=2) + "\n"
    )
    print(STREAM_WALK_ARTIFACT_PATH)


# --------------------------------------------------------------------------
# The finer-resolution walk instrument: the real's own kept-adjacent pair
# sequence re-walked by one declared boundary head at the declared finer
# steps j / 1000 inside the three gaps the boundary-walk instrument
# located its flips in, the two window-mass spans beside the head priced
# fresh at every finer position through the same mark-excluded block and
# the same six summaries, the direction tables recorded at every finer
# head, no bands, no envelopes and no margin formed.
# --------------------------------------------------------------------------

FINE_WALK_STEP_DENOM = 1000

# (lower, upper) declared steps j / 1000 per file: the three gaps the
# boundary-walk instrument located, each spanning two consecutive
# boundary-walk hundredth steps.
FINE_WALK_GAP_STEPS = {
    "ZL": (470, 480),
    "GC": (430, 440),
    "IT": (480, 490),
}

FINE_WALK_ARTIFACT_PATH = (
    Path(DATA_DIR).resolve().parent.parent.parent
    / "docs" / "research-notes"
    / "voynich-homophonic-finer-walk.json"
)


def _fine_walk_steps(lower: int, upper: int) -> tuple[float, ...]:
    """The declared finer steps for one gap: j / 1000 with j running
    lower to upper inclusive."""
    return tuple(j / FINE_WALK_STEP_DENOM for j in range(lower, upper + 1))


def _fine_walk_rows(
    frozen_cell: dict, lower: int, upper: int,
) -> tuple[dict, dict]:
    """The frozen boundary-walk head rows at a gap's two hundredth
    steps: the endpoint records the finer walk's confluence anchors
    to. The hundredth step's arithmetic is the boundary-walk
    instrument's own, so the gap's endpoint steps sit inside that
    instrument's declared head steps."""
    lower_step = lower / FINE_WALK_STEP_DENOM
    upper_step = upper / FINE_WALK_STEP_DENOM
    lower_row = None
    upper_row = None
    for row in frozen_cell["heads"]:
        if row["step"] == lower_step:
            lower_row = row
        if row["step"] == upper_step:
            upper_row = row
    if lower_row is None or upper_row is None:
        raise AssertionError(
            "finer-walk: the frozen boundary-walk cell does not "
            "record the gap's hundredth steps among its declared "
            "head steps"
        )
    return lower_row, upper_row


def _tracked_flips(
    frozen_cell: dict, lower: int, upper: int,
) -> list[dict]:
    """The declared tracked flips for one gap: exactly the side and
    summary direction records the frozen boundary-walk cell records
    as changing across the gap's two hundredth steps, computed
    mechanically from the frozen stored directions, no hand
    selection performed over them."""
    lower_row, upper_row = _fine_walk_rows(frozen_cell, lower, upper)
    tracked = []
    for side in ("left", "right"):
        for key in STREAM_SCALARS:
            at_lower = lower_row[side]["direction"][key]
            at_upper = upper_row[side]["direction"][key]
            if at_lower != at_upper:
                tracked.append(
                    {
                        "side": side,
                        "summary": key,
                        "at_lower": at_lower,
                        "at_upper": at_upper,
                    }
                )
    return tracked


def _fine_walk_heads(total: int, lower: int, upper: int) -> list[int]:
    """The declared finer head positions for one file's kept pair
    sequence of the given total: int(step x the anchor basis) for
    the declared steps j / 1000 with j running lower to upper
    inclusive, the anchor basis the kept pair total + 1. The first
    and last heads sit exactly at the gap's two hundredth steps'
    positions."""
    anchor = total + 1
    steps = _fine_walk_steps(lower, upper)
    heads = [int(step * anchor) for step in steps]
    for earlier, later in zip(heads, heads[1:]):
        if later <= earlier:
            raise AssertionError(
                "finer-walk: the declared finer heads are not "
                "increasing"
            )
    return heads


def _fine_walk_cell(code: str, frozen_m18_cell: dict) -> dict:
    """One cell's declared fine-walk records: the declared finer head
    positions inside the file's located gap and, at every head, the
    two window-mass spans beside the head priced fresh through the
    same mark-excluded block and the same six relabeling-invariant
    summaries, each span carrying its own direction table against
    the whole-sequence profile, every entry recorded. Every span's
    block-total identity (its profile total equals its window mass
    minus its own boundary-carried pairs) is enforced here, and any
    divergence aborts. No band is loaded, no envelope is formed and
    no margin is produced anywhere in this builder."""
    lower, upper = FINE_WALK_GAP_STEPS[code]
    steps = _fine_walk_steps(lower, upper)
    first, second = _real_pair_sequence(code)
    real = _homo_real_stream(code)
    mark = len(real["mapped_chars"]) - 1
    total = int(len(first))
    whole_profile = frozen_m18_cell["whole_profile"]
    heads = _fine_walk_heads(total, lower, upper)
    mass = _stream_bounds(total)[0]
    rows = []
    for index, head in enumerate(heads):
        row = {
            "step": steps[index],
            "head_position": head,
        }
        for side, start in (
            ("left", head - mass),
            ("right", head),
        ):
            take = np.arange(start, start + mass)
            if int(len(take)) != mass:
                raise AssertionError(
                    f"finer-walk/{code}/head {index}/{side}: the "
                    f"span does not carry the declared window mass"
                )
            matrix = np.zeros((37, 37))
            np.add.at(matrix, (first[take], second[take]), 1.0)
            profile = _profile_facts(_glyph_block_matrix(matrix, mark))
            carried = _boundary_carried_pairs(matrix, mark)
            if profile["total_pairs"] != mass - carried:
                raise AssertionError(
                    f"finer-walk/{code}/head {index}/{side}: the "
                    f"span's block total {profile['total_pairs']} "
                    f"does not equal the window mass {mass} minus "
                    f"its boundary-carried pairs {carried}"
                )
            row[side] = {
                "first_position": int(start),
                "end_position": int(start + mass),
                "pairs": int(mass),
                "boundary_carried_pairs": carried,
                "profile": profile,
                "direction": _direction_vs_whole(
                    profile, whole_profile,
                ),
            }
        rows.append(row)
    return {
        "kept_pairs": total,
        "window_pairs": mass,
        "gap_steps": {"lower": lower, "upper": upper},
        "whole_profile": whole_profile,
        "whole_boundary_carried_pairs": frozen_m18_cell[
            "whole_boundary_carried_pairs"
        ],
        "tracked_flips": _tracked_flips(frozen_m18_cell, lower, upper),
        "heads": rows,
    }


def _compare_finer_walk_to_frozen() -> tuple[list[str], int]:
    """The declared bridge gate for the finer-resolution walk
    instrument, per cell: the whole profile re-anchored to the frozen
    real-at-basis ladder's anchor profile, the fresh window mass
    verified against the frozen boundary-walk record, the 11 finer
    heads recomputed from the declared rule and verified one field
    each, the two window sizes verified at every head one field each,
    the four endpoint span profiles verified field for field against
    the frozen boundary-walk instrument's stored profiles at the
    gap's two hundredth steps, the two endpoint head positions
    verified against the frozen stored head positions, and the
    whole's own block-total identity verified. Any divergence aborts
    with nothing written."""
    frozen_m18 = json.loads(STREAM_WALK_ARTIFACT_PATH.read_text())
    frozen_m15 = json.loads(REAL_LADDER_ARTIFACT_PATH.read_text())
    problems: list[str] = []
    fields = 0
    for code in FILES:
        for language in LANGS:
            frozen_cell = frozen_m18["files"][code][language]
            lower, upper = FINE_WALK_GAP_STEPS[code]
            fresh = _fine_walk_cell(code, frozen_cell)
            heads = _fine_walk_heads(fresh["kept_pairs"], lower, upper)
            mass = _stream_bounds(fresh["kept_pairs"])[0]
            frozen_profile = frozen_m15["files"][code][language][
                "rungs"
            ][0]["real_rung_profile"]
            fields += 1
            if fresh["whole_profile"] != frozen_profile:
                problems.append(
                    f"finer-walk/whole/{code}/{language}: the whole "
                    f"profile is not the frozen real-at-basis "
                    f"ladder's anchor profile"
                )
            fields += 1
            if fresh["window_pairs"] != frozen_cell["window_pairs"]:
                problems.append(
                    f"finer-walk/{code}/{language}: the fresh window "
                    f"mass does not equal the frozen boundary-walk "
                    f"instrument's"
                )
            for index in range(len(heads)):
                row = fresh["heads"][index]
                fields += 1
                if row["head_position"] != heads[index]:
                    problems.append(
                        f"finer-walk/{code}/{language}/head "
                        f"{index}: the head does not equal the "
                        f"declared rule's"
                    )
                fields += 1
                if row["left"]["pairs"] != mass:
                    problems.append(
                        f"finer-walk/{code}/{language}/head "
                        f"{index}: the left span's window size "
                        f"differs from the declared one"
                    )
                fields += 1
                if row["right"]["pairs"] != mass:
                    problems.append(
                        f"finer-walk/{code}/{language}/head "
                        f"{index}: the right span's window size "
                        f"differs from the declared one"
                    )
            lower_row, upper_row = _fine_walk_rows(
                frozen_cell, lower, upper,
            )
            confluence = (
                (0, fresh["heads"][0]["left"]["profile"],
                 lower_row["left"]["profile"]),
                (0, fresh["heads"][0]["right"]["profile"],
                 lower_row["right"]["profile"]),
                (len(heads) - 1, fresh["heads"][-1]["left"]["profile"],
                 upper_row["left"]["profile"]),
                (len(heads) - 1,
                 fresh["heads"][-1]["right"]["profile"],
                 upper_row["right"]["profile"]),
            )
            for head_index, span_profile, frozen_row_profile in (
                confluence
            ):
                fields += 1
                if span_profile != frozen_row_profile:
                    problems.append(
                        f"finer-walk/{code}/{language}/head "
                        f"{head_index}: the endpoint span's fresh "
                        f"profile does not equal the frozen "
                        f"boundary-walk instrument's stored profile"
                    )
            fields += 1
            if fresh["heads"][0]["head_position"] != (
                lower_row["head_position"]
            ):
                problems.append(
                    f"finer-walk/{code}/{language}: the gap's first "
                    f"head is not the frozen boundary-walk "
                    f"instrument's lower endpoint head"
                )
            fields += 1
            if fresh["heads"][-1]["head_position"] != (
                upper_row["head_position"]
            ):
                problems.append(
                    f"finer-walk/{code}/{language}: the gap's last "
                    f"head is not the frozen boundary-walk "
                    f"instrument's upper endpoint head"
                )
            fields += 1
            if fresh["whole_profile"]["total_pairs"] != (
                fresh["kept_pairs"]
                - fresh["whole_boundary_carried_pairs"]
            ):
                problems.append(
                    f"finer-walk/{code}/{language}: the whole "
                    f"profile's block total does not equal the kept "
                    f"pairs minus the whole's boundary-carried pairs"
                )
    return problems, fields


def substitution_homophonic_finer_walk() -> dict:
    """The declared finer-resolution walk instrument: the two declared
    window-mass spans beside every declared finer head priced fresh
    through the same mark-excluded block and the same six summaries,
    the direction tables recorded at every finer head, no bands and no
    envelopes. The bridge gate runs first; any divergence aborts with
    nothing written."""
    problems, fields = _compare_finer_walk_to_frozen()
    if problems:
        raise AssertionError(
            "finer-walk bridge gate failed: " + "; ".join(problems)
        )
    artifact = {
        "what": "The declared finer-resolution walk instrument: the "
        "state space 1296 ordered types with the boundary mark's row "
        "and column excluded on both sides and the same six "
        "relabeling-invariant summaries, with the real's own "
        "kept-adjacent pair sequence walked by one declared boundary "
        "head at the declared finer steps j / 1000 inside the three "
        "gaps the boundary-walk instrument located its flips in (ZL "
        "j 470 to 480, GC j 430 to 440, IT j 480 to 490), the two "
        "window-mass spans beside the head priced fresh at every "
        "finer position, the direction tables recorded at every "
        "finer position, no bands and no envelopes. The declared "
        "truthful questions: at which finer declared position each "
        "tracked direction flip turns - the tracked flips exactly "
        "the frozen boundary-walk direction records that change "
        "across each gap, computed mechanically - or whether any of "
        "them splits into more than one turn or drifts smoothly "
        "inside its gap. No mapping is published; nothing here is "
        "a reading.",
        "declared": {
            "base_seed": BASE_SEED,
            "mapped": MAPPED_HOMO,
            "boundary_rule": "the word-boundary mark's row and "
            "column are excluded from every profile's state space "
            "on both sides exactly as the boundary-mark "
            "re-instrument and the standing walk instruments "
            "declared: every profile is the mark-excluded block "
            "of its pair-count matrix, 1296 ordered types, and "
            "the standing alphabet-width disclosure carries "
            "unchanged (the IT real transcription ranks only 23 "
            "glyph types plus the mark, so 13 of its block's 36 "
            "glyph slots are empty by width alone on the real "
            "side)",
            "walk_rule": "the window mass fixed at the standing "
            "basis arithmetic's first boundary - the int(quarter x "
            "the anchor basis) positions with the anchor basis the "
            "kept pair total + 1, so the window mass is ZL 54,604, "
            "GC 45,800 and IT 55,133 kept-adjacent pairs - and the "
            "head walked at int(step x the anchor basis) positions "
            "for the declared steps j / 1000 with j running over "
            "the three declared gaps exactly as the boundary-walk "
            "instrument located them: ZL j 470 to 480 inclusive, "
            "GC j 430 to 440 inclusive, IT j 480 to 490 inclusive, "
            "11 heads per file, the first and last heads of each "
            "gap exactly the boundary-walk instrument's recorded "
            "heads at that gap's two hundredth steps; at every "
            "finer head the two spans beside the head are the "
            "window-mass span ending at the head and the "
            "window-mass span starting at the head, each priced "
            "fresh, no pair dropped, no pair synthesized",
            "tracked_rule": "the tracked flips are exactly the "
            "side and summary direction records the frozen "
            "boundary-walk artifact records as changing across "
            "each gap's two hundredth steps, computed "
            "mechanically from the frozen stored directions and "
            "listed in the artifact, no hand selection performed "
            "over them, and the fine walk's direction tables are "
            "recorded at every finer head so each tracked flip's "
            "finer location is read off the recorded entries",
            "summary_rule": "each profile is priced fresh through "
            "the same mark-excluded block and the same six "
            "relabeling-invariant summaries the standing "
            "instruments declare; no profile is compared to any "
            "simulated profile anywhere in this artifact",
            "no_band_rule": "no rung band is loaded, no envelope "
            "is formed, no verdict and no scalar margin is "
            "produced anywhere in this artifact: the declared "
            "question is answered by direction, and the frozen "
            "rung bands stay the frozen instruments' declared "
            "records, untouched here",
            "direction_rule": "each span records, for each of the "
            "six scalar summaries it shares with the whole "
            "profile (the empty type count, the self-pair share, "
            "the top-k shares at k 1, 10 and 50, and the pair "
            "entropy), whether its value sits above, below or "
            "equal to the whole sequence's value at the stored "
            "6-decimal rounding, every entry recorded and no "
            "selection performed over anything",
            "roster_rule": "the corpus-breadth roster stands "
            "unchanged: the same eight accepted corpus files, "
            "the same rejected candidates with their verbatim "
            "causes, the same sha256 records, the roster floor "
            "and the fetch verification are the corpus-breadth "
            "artifact's declared facts taken by reference, no "
            "corpus file is re-fetched, re-probed or re-hashed "
            "here, and no encoding is re-run anywhere: this "
            "instrument prices the real's own side only",
            "state_note": "the real's kept-adjacency is real "
            "adjacency with 126 unmapped events inside ZL's "
            "218,663, 1,769 inside GC's 186,708, none inside "
            "IT's 220,532, exactly as disclosed since the "
            "interior instrument; the real's side is identical "
            "for both languages of a file, so every cell prices "
            "the same fine-walk records; the whole-sequence "
            "profile is anchored to the frozen real-at-basis "
            "ladder's anchor profile in the gate",
            "machinery_rule": "this instrument contains no "
            "assignment search anywhere: no candidate "
            "evaluation, no restarts, no sweep cap, no "
            "convergence flags, and no seed of any kind: the "
            "finer heads are the declared arithmetic and every "
            "profile is priced fresh from the real's own pair "
            "sequence, so the standing budgets and the seed-kind "
            "registry play no part here",
            "split_rule": "no split applies: a profile uses "
            "every counted pair of its declared window after "
            "the declared exclusion; the climb and score halves "
            "of the band instruments have no counterpart here",
            "record_rule": "per cell the artifact records the "
            "kept pair total, the window mass, the declared "
            "gap's steps, the whole-sequence profile with its "
            "boundary-carried pairs, the mechanical tracked-flip "
            "list, and the 11 head records in order, each "
            "carrying its declared step, its head position, and "
            "its two spans, each span carrying its first and "
            "end positions, its window mass, its own "
            "boundary-carried pairs, its fresh profile (the "
            "block total, both vector summaries as counts and "
            "shares, the empty type count, the self-pair share, "
            "the top-k shares and the pair entropy) and its "
            "direction record against the whole profile's six "
            "scalar summaries, every entry recorded",
            "closure_rule": "no scalar margin is formed: this "
            "instrument's question is the direction run at every "
            "declared finer head per span, and the record "
            "answers it entry by entry",
            "exclusion_rule": "the family's declared exclusion "
            "format is not re-scoped by this artifact: it keys "
            "to the declared 36-slot class under the inherited "
            "add-one form exactly as the held-out screen "
            "declared it, so a search-free verdict is structure "
            "evidence and the band instruments' verdicts stand "
            "untouched by this artifact's numbers",
            "gate_rule": "before any span at any declared finer "
            "head is recorded beyond the gate, the gate verified "
            "fresh per cell: the whole profile against the "
            "frozen real-at-basis ladder's anchor profile, the "
            "fresh window mass against the frozen boundary-walk "
            "record, the 11 heads against the declared rule, "
            "the two window sizes at every head, the four "
            "endpoint span profiles against the frozen "
            "boundary-walk instrument's stored profiles at the "
            "gap's two hundredth steps, the two endpoint head "
            "positions against the frozen stored head "
            "positions, and the whole's own identity, 42 fields "
            "per cell, 252 fields all told; any divergence "
            "aborts with nothing written",
            "confluence_rule": "the fine walk's endpoints are "
            "the boundary-walk instrument's frozen head records "
            "taken by reference and verified field for field in "
            "the gate: each gap's first head is that "
            "instrument's recorded lower hundredth head and "
            "each gap's last head its recorded upper hundredth "
            "head, so the fine walk begins and ends inside the "
            "boundary-walk instrument's declared records and "
            "its heads are declared arithmetic in between",
            "models_rule": "no score table is built or used: "
            "the instrument prices count structure only, so "
            "the standing add-one and leave-one-out tables "
            "play no part anywhere in this artifact",
        },
        "bridge_gate": {
            "status": "verified",
            "fields_compared": fields,
            "per_cell_fields": 42,
        },
        "files": {},
    }
    frozen_m18 = json.loads(STREAM_WALK_ARTIFACT_PATH.read_text())
    for code in FILES:
        artifact["files"][code] = {}
        for language in LANGS:
            artifact["files"][code][language] = _fine_walk_cell(
                code, frozen_m18["files"][code][language],
            )
    return artifact


def main_finer_walk() -> None:
    artifact = substitution_homophonic_finer_walk()
    FINE_WALK_ARTIFACT_PATH.write_text(
        json.dumps(artifact, indent=2) + "\n"
    )
    print(FINE_WALK_ARTIFACT_PATH)


# --------------------------------------------------------------------------
# The switch-walk instrument: the real's own kept-adjacent pair sequence
# re-walked by one declared boundary head at the declared finer steps
# j / 10000 across the five switch bands the finer-resolution walk
# instrument located, the two window-mass spans beside the head priced
# fresh at every finer position through the same mark-excluded block and
# the same six summaries, the direction tables recorded at every finer
# head, no bands, no envelopes and no margin formed.
# --------------------------------------------------------------------------

SWITCH_WALK_STEP_DENOM = 10000

# (lower, upper) declared steps j / 10000 per file: the five switch bands
# the finer-resolution walk instrument located, each spanning two
# consecutive finer-walk thousandth steps, 11 heads per band.
SWITCH_WALK_SWITCH_STEPS = {
    "ZL": ((4700, 4710), (4790, 4800)),
    "GC": ((4370, 4380),),
    "IT": ((4820, 4830), (4890, 4900)),
}

SWITCH_WALK_ARTIFACT_PATH = (
    Path(DATA_DIR).resolve().parent.parent.parent
    / "docs" / "research-notes"
    / "voynich-homophonic-switch-walk.json"
)


def _switch_walk_steps(lower: int, upper: int) -> tuple[float, ...]:
    """The declared finer steps for one switch band: j / 10000 with j
    running lower to upper inclusive."""
    return tuple(j / SWITCH_WALK_STEP_DENOM for j in range(lower, upper + 1))


def _switch_walk_rows(
    frozen_cell: dict, lower: int, upper: int,
) -> tuple[dict, dict]:
    """The frozen finer-walk head rows at one switch band's two boundary
    thousandth steps: the endpoint records the switch walk's confluence
    anchors to, matched by head position with no float step equality
    asserted anywhere. The band's endpoint arithmetic is the finer-walk
    instrument's declared int(step x the anchor basis) form, so the
    band's two boundary positions sit among that instrument's stored
    head positions."""
    anchor = frozen_cell["kept_pairs"] + 1
    steps = _switch_walk_steps(lower, upper)
    lower_head = int(steps[0] * anchor)
    upper_head = int(steps[-1] * anchor)
    lower_row = None
    upper_row = None
    for row in frozen_cell["heads"]:
        if row["head_position"] == lower_head:
            lower_row = row
        if row["head_position"] == upper_head:
            upper_row = row
    if lower_row is None or upper_row is None:
        raise AssertionError(
            "switch-walk: the frozen finer-walk cell does not "
            "record the band's boundary positions among its stored "
            "head positions"
        )
    return lower_row, upper_row


def _switch_walk_flips(
    frozen_cell: dict, lower: int, upper: int,
) -> list[dict]:
    """The declared tracked flips for one switch band: exactly the side
    and summary direction records the frozen finer-walk cell records as
    changing across the band's two boundary heads, computed mechanically
    from the frozen stored directions, no hand selection performed over
    them."""
    lower_row, upper_row = _switch_walk_rows(frozen_cell, lower, upper)
    tracked = []
    for side in ("left", "right"):
        for key in STREAM_SCALARS:
            at_lower = lower_row[side]["direction"][key]
            at_upper = upper_row[side]["direction"][key]
            if at_lower != at_upper:
                tracked.append(
                    {
                        "side": side,
                        "summary": key,
                        "at_lower": at_lower,
                        "at_upper": at_upper,
                        "lower": lower,
                        "upper": upper,
                        "lower_position": lower_row["head_position"],
                        "upper_position": upper_row["head_position"],
                    }
                )
    return tracked


def _switch_walk_heads(total: int, lower: int, upper: int) -> list[int]:
    """The declared finer head positions for one file's kept pair
    sequence of the given total: int(step x the anchor basis) for the
    declared steps j / 10000 with j running lower to upper inclusive,
    the anchor basis the kept pair total + 1. The band lands inside the
    finer-walk instrument's located switch and must increase."""
    anchor = total + 1
    steps = _switch_walk_steps(lower, upper)
    heads = [int(step * anchor) for step in steps]
    for earlier, later in zip(heads, heads[1:]):
        if later <= earlier:
            raise AssertionError(
                "switch-walk: the declared finer heads are not "
                "increasing"
            )
    return heads


def _switch_walk_cell(code: str, frozen_m19_cell: dict) -> dict:
    """One cell's declared switch-walk records: the declared finer head
    positions inside the file's located switch bands (ZL two, GC one,
    IT two) and, at every head, the two window-mass spans beside the
    head priced fresh through the same mark-excluded block and the same
    six relabeling-invariant summaries, each span carrying its own
    direction table against the whole-sequence profile, every entry
    recorded. Every span's block-total identity (its profile total
    equals its window mass minus its own boundary-carried pairs) is
    enforced here, and any divergence aborts. No rung band is loaded,
    no envelope is formed and no margin is produced anywhere in this
    builder."""
    bands = SWITCH_WALK_SWITCH_STEPS[code]
    first, second = _real_pair_sequence(code)
    real = _homo_real_stream(code)
    mark = len(real["mapped_chars"]) - 1
    total = int(len(first))
    whole_profile = frozen_m19_cell["whole_profile"]
    mass = _stream_bounds(total)[0]
    anchor = total + 1
    switches = []
    tracked = []
    for lower, upper in bands:
        steps = _switch_walk_steps(lower, upper)
        heads = _switch_walk_heads(total, lower, upper)
        rows = []
        for index, head in enumerate(heads):
            row = {
                "step": steps[index],
                "head_j": lower + index,
                "head_position": head,
            }
            for side, start in (
                ("left", head - mass),
                ("right", head),
            ):
                take = np.arange(start, start + mass)
                if int(len(take)) != mass:
                    raise AssertionError(
                        f"switch-walk/{code}/band {lower}/{side}: the "
                        f"span does not carry the declared window mass"
                    )
                matrix = np.zeros((37, 37))
                np.add.at(matrix, (first[take], second[take]), 1.0)
                profile = _profile_facts(_glyph_block_matrix(matrix, mark))
                carried = _boundary_carried_pairs(matrix, mark)
                if profile["total_pairs"] != mass - carried:
                    raise AssertionError(
                        f"switch-walk/{code}/band {lower}/{side}: the "
                        f"span's block total {profile['total_pairs']} "
                        f"does not equal the window mass {mass} minus "
                        f"its boundary-carried pairs {carried}"
                    )
                row[side] = {
                    "first_position": int(start),
                    "end_position": int(start + mass),
                    "pairs": int(mass),
                    "boundary_carried_pairs": carried,
                    "profile": profile,
                    "direction": _direction_vs_whole(
                        profile, whole_profile,
                    ),
                }
            rows.append(row)
        switches.append({"lower": lower, "upper": upper, "heads": rows})
        tracked.extend(_switch_walk_flips(frozen_m19_cell, lower, upper))
    return {
        "kept_pairs": total,
        "window_pairs": mass,
        "whole_profile": whole_profile,
        "whole_boundary_carried_pairs": frozen_m19_cell[
            "whole_boundary_carried_pairs"
        ],
        "tracked_flips": tracked,
        "switches": switches,
    }


def _compare_switch_walk_to_frozen() -> tuple[list[str], int]:
    """The declared bridge gate for the switch-walk instrument, per
    cell: the whole profile re-anchored to the frozen real-at-basis
    ladder's anchor profile, the fresh window mass verified against the
    frozen finer-walk record, and the whole's own block-total identity
    verified; then per switch band the 11 heads recomputed from the
    declared rule and verified one field each, the two window sizes
    verified at every head one field each, the four endpoint span
    profiles verified field for field against the frozen finer-walk
    instrument's stored profiles at the band's two boundary steps, and
    the two endpoint head positions verified against the frozen stored
    head positions by position. Any divergence aborts with nothing
    written."""
    frozen_m19 = json.loads(FINE_WALK_ARTIFACT_PATH.read_text())
    frozen_m15 = json.loads(REAL_LADDER_ARTIFACT_PATH.read_text())
    problems: list[str] = []
    fields = 0
    for code in FILES:
        for language in LANGS:
            frozen_cell = frozen_m19["files"][code][language]
            fresh = _switch_walk_cell(code, frozen_cell)
            frozen_profile = frozen_m15["files"][code][language][
                "rungs"
            ][0]["real_rung_profile"]
            fields += 1
            if fresh["whole_profile"] != frozen_profile:
                problems.append(
                    f"switch-walk/whole/{code}/{language}: the whole "
                    f"profile is not the frozen real-at-basis "
                    f"ladder's anchor profile"
                )
            fields += 1
            if fresh["window_pairs"] != frozen_cell["window_pairs"]:
                problems.append(
                    f"switch-walk/{code}/{language}: the fresh window "
                    f"mass does not equal the frozen finer-walk "
                    f"instrument's"
                )
            fields += 1
            if fresh["whole_profile"]["total_pairs"] != (
                fresh["kept_pairs"]
                - fresh["whole_boundary_carried_pairs"]
            ):
                problems.append(
                    f"switch-walk/{code}/{language}: the whole "
                    f"profile's block total does not equal the kept "
                    f"pairs minus the whole's boundary-carried pairs"
                )
            for band_index, band in enumerate(fresh["switches"]):
                lower, upper = SWITCH_WALK_SWITCH_STEPS[code][band_index]
                rows = band["heads"]
                for index in range(len(rows)):
                    row = rows[index]
                    fields += 1
                    if row["head_position"] != _switch_walk_heads(
                        fresh["kept_pairs"], lower, upper,
                    )[index]:
                        problems.append(
                            f"switch-walk/{code}/{language}/band "
                            f"{band_index}/head {index}: the head "
                            f"does not equal the declared rule's"
                        )
                    fields += 1
                    if row["left"]["pairs"] != fresh["window_pairs"]:
                        problems.append(
                            f"switch-walk/{code}/{language}/band "
                            f"{band_index}/head {index}: the left "
                            f"span's window size differs from the "
                            f"declared one"
                        )
                    fields += 1
                    if row["right"]["pairs"] != fresh["window_pairs"]:
                        problems.append(
                            f"switch-walk/{code}/{language}/band "
                            f"{band_index}/head {index}: the right "
                            f"span's window size differs from the "
                            f"declared one"
                        )
                lower_row, upper_row = _switch_walk_rows(
                    frozen_cell, lower, upper,
                )
                confluence = (
                    (0, rows[0]["left"]["profile"],
                     lower_row["left"]["profile"]),
                    (0, rows[0]["right"]["profile"],
                     lower_row["right"]["profile"]),
                    (len(rows) - 1, rows[-1]["left"]["profile"],
                     upper_row["left"]["profile"]),
                    (len(rows) - 1, rows[-1]["right"]["profile"],
                     upper_row["right"]["profile"]),
                )
                for head_index, span_profile, frozen_row_profile in (
                    confluence
                ):
                    fields += 1
                    if span_profile != frozen_row_profile:
                        problems.append(
                            f"switch-walk/{code}/{language}/band "
                            f"{band_index}/head {head_index}: the "
                            f"endpoint span's fresh profile does not "
                            f"equal the frozen finer-walk instrument's "
                            f"stored profile"
                        )
                fields += 1
                if rows[0]["head_position"] != (
                    lower_row["head_position"]
                ):
                    problems.append(
                        f"switch-walk/{code}/{language}/band "
                        f"{band_index}: the band's first head is not "
                        f"the frozen finer-walk instrument's lower "
                        f"boundary head"
                    )
                fields += 1
                if rows[-1]["head_position"] != (
                    upper_row["head_position"]
                ):
                    problems.append(
                        f"switch-walk/{code}/{language}/band "
                        f"{band_index}: the band's last head is not "
                        f"the frozen finer-walk instrument's upper "
                        f"boundary head"
                    )
    return problems, fields


def substitution_homophonic_switch_walk() -> dict:
    """The declared switch-walk instrument: the two declared window-mass
    spans beside every declared finer head priced fresh through the
    same mark-excluded block and the same six summaries, the direction
    tables recorded at every finer head, no rung bands and no
    envelopes. The bridge gate runs first; any divergence aborts with
    nothing written."""
    problems, fields = _compare_switch_walk_to_frozen()
    if problems:
        raise AssertionError(
            "switch-walk bridge gate failed: " + "; ".join(problems)
        )
    artifact = {
        "what": "The declared switch-walk instrument: the state space "
        "1296 ordered types with the boundary mark's row and column "
        "excluded on both sides and the same six relabeling-invariant "
        "summaries, with the real's own kept-adjacent pair sequence "
        "walked by one declared boundary head at the declared finer "
        "steps j / 10000 across the five switch bands the "
        "finer-resolution walk instrument located (ZL j 4700 to 4710 "
        "and j 4790 to 4800, GC j 4370 to 4380, IT j 4820 to 4830 and "
        "j 4890 to 4900), the two window-mass spans beside the head "
        "priced fresh at every finer position, the direction tables "
        "recorded at every finer position, no rung bands and no "
        "envelopes. The declared truthful question: at which declared "
        "ten-thousandth position each tracked direction flip turns - "
        "the tracked flips exactly the frozen finer-walk direction "
        "records that change across each switch band's two boundary "
        "heads, computed mechanically - and whether each turns once or "
        "splits into more than one turn, whether the shared bands' "
        "paired flips stay together or separate, or whether any of "
        "them drifts smoothly inside its band. No mapping is "
        "published; nothing here is a reading.",
        "declared": {
            "base_seed": BASE_SEED,
            "mapped": MAPPED_HOMO,
            "boundary_rule": "the word-boundary mark's row and "
            "column are excluded from every profile's state space "
            "on both sides exactly as the boundary-mark "
            "re-instrument and the standing walk instruments "
            "declared: every profile is the mark-excluded block "
            "of its pair-count matrix, 1296 ordered types, and "
            "the standing alphabet-width disclosure carries "
            "unchanged (the IT real transcription ranks only 23 "
            "glyph types plus the mark, so 13 of its block's 36 "
            "glyph slots are empty by width alone on the real "
            "side)",
            "walk_rule": "the window mass fixed at the standing "
            "basis arithmetic's first boundary - the int(quarter x "
            "the anchor basis) positions with the anchor basis the "
            "kept pair total + 1, so the window mass is ZL 54,604, "
            "GC 45,800 and IT 55,133 kept-adjacent pairs - and the "
            "head walked at int(step x the anchor basis) positions "
            "for the declared steps j / 10000 with j running over "
            "the five declared switch bands exactly as the "
            "finer-resolution walk instrument located them: ZL j "
            "4700 to 4710 inclusive and j 4790 to 4800 inclusive, "
            "GC j 4370 to 4380 inclusive, IT j 4820 to 4830 "
            "inclusive and j 4890 to 4900 inclusive, 11 heads per "
            "band, the first and last heads of each band exactly "
            "the finer-resolution walk instrument's stored heads "
            "at the band's two boundary thousandth steps matched "
            "by head position; at every finer head the two spans "
            "beside the head are the window-mass span ending at "
            "the head and the window-mass span starting at the "
            "head, each priced fresh, no pair dropped, no pair "
            "synthesized",
            "tracked_rule": "the tracked flips are exactly the "
            "side and summary direction records the frozen "
            "finer-walk artifact records as changing across each "
            "switch band's two boundary heads, computed "
            "mechanically from the frozen stored directions and "
            "listed in the artifact band by band, no hand "
            "selection performed over them, and the switch walk's "
            "direction tables are recorded at every finer head so "
            "each tracked flip's finer location is read off the "
            "recorded entries",
            "summary_rule": "each profile is priced fresh through "
            "the same mark-excluded block and the same six "
            "relabeling-invariant summaries the standing "
            "instruments declare; no profile is compared to any "
            "simulated profile anywhere in this artifact",
            "no_band_rule": "no rung band is loaded, no envelope "
            "is formed, no verdict and no scalar margin is "
            "produced anywhere in this artifact: the declared "
            "question is answered by direction, and the frozen "
            "rung bands stay the frozen instruments' declared "
            "records, untouched here",
            "direction_rule": "each span records, for each of the "
            "six scalar summaries it shares with the whole "
            "profile (the empty type count, the self-pair share, "
            "the top-k shares at k 1, 10 and 50, and the pair "
            "entropy), whether its value sits above, below or "
            "equal to the whole sequence's value at the stored "
            "6-decimal rounding, every entry recorded and no "
            "selection performed over anything",
            "roster_rule": "the corpus-breadth roster stands "
            "unchanged: the same eight accepted corpus files, "
            "the same rejected candidates with their verbatim "
            "causes, the same sha256 records, the roster floor "
            "and the fetch verification are the corpus-breadth "
            "artifact's declared facts taken by reference, no "
            "corpus file is re-fetched, re-probed or re-hashed "
            "here, and no encoding is re-run anywhere: this "
            "instrument prices the real's own side only",
            "state_note": "the real's kept-adjacency is real "
            "adjacency with 126 unmapped events inside ZL's "
            "218,663, 1,769 inside GC's 186,708, none inside "
            "IT's 220,532, exactly as disclosed since the "
            "interior instrument; the real's side is identical "
            "for both languages of a file, so every cell prices "
            "the same switch-walk records; the whole-sequence "
            "profile is anchored to the frozen real-at-basis "
            "ladder's anchor profile in the gate",
            "machinery_rule": "this instrument contains no "
            "assignment search anywhere: no candidate "
            "evaluation, no restarts, no sweep cap, no "
            "convergence flags, and no seed of any kind: the "
            "switch bands' heads are the declared arithmetic and "
            "every profile is priced fresh from the real's own "
            "pair sequence, so the standing budgets and the "
            "seed-kind registry play no part here",
            "split_rule": "no split applies: a profile uses "
            "every counted pair of its declared window after "
            "the declared exclusion; the climb and score halves "
            "of the band instruments have no counterpart here",
            "record_rule": "per cell the artifact records the "
            "kept pair total, the window mass, the whole-"
            "sequence profile with its boundary-carried pairs, "
            "the mechanical tracked-flip list band by band, and "
            "each declared switch band in order, each carrying "
            "its lower and upper declared steps and its 11 head "
            "records, each head carrying its declared step, its "
            "declared head index j, and its head position, and "
            "its two spans, each span carrying its first and "
            "end positions, its window mass, its own "
            "boundary-carried pairs, its fresh profile (the "
            "block total, both vector summaries as counts and "
            "shares, the empty type count, the self-pair share, "
            "the top-k shares and the pair entropy) and its "
            "direction record against the whole profile's six "
            "scalar summaries, every entry recorded",
            "closure_rule": "no scalar margin is formed: this "
            "instrument's question is the direction run at every "
            "declared finer head per span, and the record "
            "answers it entry by entry",
            "exclusion_rule": "the family's declared exclusion "
            "format is not re-scoped by this artifact: it keys "
            "to the declared 36-slot class under the inherited "
            "add-one form exactly as the held-out screen "
            "declared it, so a search-free verdict is structure "
            "evidence and the band instruments' verdicts stand "
            "untouched by this artifact's numbers",
            "gate_rule": "before any span at any declared finer "
            "head is recorded beyond the gate, the gate verified "
            "fresh per cell: the whole profile against the "
            "frozen real-at-basis ladder's anchor profile, the "
            "fresh window mass against the frozen finer-walk "
            "record, the whole's own identity, and per switch "
            "band the 11 heads against the declared rule, the "
            "two window sizes at every head, the four endpoint "
            "span profiles against the frozen finer-walk "
            "instrument's stored profiles at the band's two "
            "boundary steps and the two endpoint head positions "
            "against the frozen stored head positions by "
            "position, 81 fields per ZL or IT cell (two switch "
            "bands), 42 fields per GC cell (one switch band), "
            "408 fields all told; any divergence aborts with "
            "nothing written",
            "confluence_rule": "the switch walk's endpoints are "
            "the finer-resolution walk instrument's frozen head "
            "records taken by reference and matched by head "
            "position, no float step equality asserted anywhere, "
            "and verified field for field in the gate: each "
            "band's first head is that instrument's stored head "
            "at the band's lower boundary thousandth step and "
            "each band's last head its stored head at the upper "
            "boundary thousandth step, so the switch walk begins "
            "and ends inside the finer-resolution walk "
            "instrument's declared records and its heads are "
            "declared arithmetic in between",
            "models_rule": "no score table is built or used: "
            "the instrument prices count structure only, so "
            "the standing add-one and leave-one-out tables "
            "play no part anywhere in this artifact",
        },
        "bridge_gate": {
            "status": "verified",
            "fields_compared": fields,
            "per_cell_fields": {"ZL": 81, "GC": 42, "IT": 81},
        },
        "files": {},
    }
    frozen_m19 = json.loads(FINE_WALK_ARTIFACT_PATH.read_text())
    for code in FILES:
        artifact["files"][code] = {}
        for language in LANGS:
            artifact["files"][code][language] = _switch_walk_cell(
                code, frozen_m19["files"][code][language],
            )
    return artifact


def main_switch_walk() -> None:
    artifact = substitution_homophonic_switch_walk()
    SWITCH_WALK_ARTIFACT_PATH.write_text(
        json.dumps(artifact, indent=2) + "\n"
    )
    print(SWITCH_WALK_ARTIFACT_PATH)
