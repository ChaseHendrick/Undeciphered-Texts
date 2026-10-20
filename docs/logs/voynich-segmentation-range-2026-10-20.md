Voynich MS: the word-segmentation range - 20 October 2026

Fourth execution step for the Voynich case, and family 2's measurement: do
the declared statistics survive a change of word segmentation? The
segmentation ambiguity itself turned out to be smaller and stranger than
expected: in this corpus pair, only ZL (and GC) carry uncertain spaces at
all. IT2a has zero: its 5,215 in-file commas all belong to the IVTFF locus
locator field (`<f1r.1,@P0>`, one per locus), none to word text. Every IT
word break is definite, which makes IT the built-in zero-join control for
everything below.

## What was computed, on what, and with what declared choices

The module is `engine/voynich_segmentation.py`; the report lives at
`docs/research-notes/voynich-segmentation-range.json`; the tests are
`tests/test_voynich_segmentation.py`. The locus set is the same 5,013
worded loci shared by ZL and IT outside the same ten reserved folios
(frozen list in the ledger). Two declared segmentations of one and the
same locus text:

- `join`, the frozen long-word convention, is delegated verbatim to the
  frozen parser, and a lock test asserts equality with the parser's words
  on every locus of all three files (16 thousand loci), so the policy
  machinery cannot drift from the validated parser;
- `split`, the identical normalisation chain with every uncertain space
  (comma) cut as a definite separator.

Three files are measured: ZL and IT (their word strings compare) and GC
(the v101 alphabet file, included for its within-file range only; GC word
strings are never compared with the other two by house rule). GC lacks one
of the shared keys and that absence is recorded in the report.

## The measurement, file by file

| File | Joins | Tokens join | Tokens split | Types join | Types split | Mean join | Mean split |
|------|-------|-------------|--------------|------------|-------------|-----------|------------|
| ZL   | 2,603 | 34,354      | 36,957       | 8,988      | 7,959       | 5.365     | 4.987      |
| GC   | 2,321 | 36,232      | 38,553       | 10,140     | 9,438       | 4.153     | 3.903      |
| IT   | 0     | 36,441      | 36,441       | 7,901      | 7,901       | 5.052     | 5.052      |

Token delta equals the join count exactly in every file: each uncertain
space in these files is interior, so one join is exactly one new token
(2,603 of 34,354 ZL tokens, 7.6 percent; 2,321 of 36,232 GC tokens, 6.4
percent; IT zero). The vocabulary result is the sharp one: cutting at
uncertain spaces produces MORE tokens but FEWER types (ZL 8,988 to 7,959,
GC 10,140 to 9,438), because the long-word convention manufactured rare
joined hapaxes that splitting recycles into frequent short forms. A large
share of measured "lexical richness" in these transcriptions is
segmentation, not vocabulary.

Sign frequencies are exactly invariant under both policies in every file
(delta 0, not "small"): the glyph multiset of a locus does not depend on
where tokens are cut, and the machinery demonstrates the identity it
should.

Higher n-grams lose only what crossed an uncertain space: ZL quadgram
totals 84,075 to 78,476 (types 4,704 to 4,140), bigrams 149,956 to 147,353
(types 496 to 480); GC shrinks the same way proportionally.

The word-frequency statistic moves without collapsing: Spearman between a
file's join-words and its own split-words is 0.942 for ZL (over 7,507
shared types), 0.947 for GC, and exactly 1.0 for IT, where the two
policies are identical by construction.

## Cross-transcription agreement under both policies

ZL vs IT Spearman over shared types (orders 1 to 4, then word tokens):

| Policy | char1 | ngram2 | ngram3 | ngram4 | word1 |
|--------|-------|--------|--------|--------|-------|
| join   | 0.999 | 0.965  | 0.937  | 0.915  | 0.901 |
| split  | 0.999 | 0.970  | 0.948  | 0.933  | 0.915 |

The join row reproduces family 1's frozen numbers exactly (same machinery,
same loci: a real cross-module check). Under the split policy every order
is at or above the join value. Why cutting at unsure spaces should raise
agreement is not yet tested; the plain observation is that the corpus's
own long-word default is the lower-agreement segmentation and the
difference is small (at most 0.019 on quadgrams, 0.013 on words). What
matters for the family question: the family 1 conclusion, agreement of
0.90 or better at every order, does not depend on which segmentation the
files use. No mechanism is claimed.

## Controls

- Lock: the join policy equals the frozen parser on every locus of all
  three files, and on synthetic loci.
- Zero-join control: IT's join and split reports are byte-identical.
- Bookkeeping identity: token delta equals the join count exactly in all
  three files and in the planted synthetic, whose 10 loci (per-folio
  composition 4, 3, 2, 1 outside one reserved folio) carry interior commas
  only; the synthetic also asserts exact sign invariance, a changed type
  inventory, a falling mean length, and agreement of 1.0 for the identical
  file pair under both policies.
- Sign invariance as a positive control: delta 0 exactly, everywhere,
  rather than a tolerance.

## Statement of the result, and its limits

The declared statistics survive the segmentation range, but not in the
flat where-they-all-same sense: sign frequencies are provably invariant;
token, type, length and word-frequency statistics move by exactly the
number of uncertain spaces, which is 6 to 8 percent of tokens in the two
files that have ambiguity and zero in the third; and the
cross-transcription agreement stands under both policies. The honest word
for family 2 is therefore: the token-level story is segmentation-bound to
the measured extent, the sign-level story is not, and no statistical
conclusion drawn in family 1 flips.

Limits: the range covers the two policies the corpus text can express (a
"join" slid halfway, weighting joins probabilistically, is not declared
here); IT contributes no range because IT2a publishes no uncertain spaces,
which is a property of the transcript, not of the manuscript; the
length-preserving permutation nulls and the reserved folios remain family
3's tools and stay untouched. Nothing in this log is a reading of the
manuscript, and no conclusion about language, cipher or meaning follows.

Family 2 closes with this measurement. Family 3, the held-out prediction
of the ten reserved folios against length-preserving nulls, is now the
first job.
