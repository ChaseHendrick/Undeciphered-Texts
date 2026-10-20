Voynich MS: the transcription-robustness measurement - 20 October 2026

Third execution step for the Voynich case, and family 1's measurement: do
the declared statistics survive a change of transcription? The answer, with
controls, is yes, and the difference that does appear is segmentation, which
is exactly the next family's question.

## What was computed, on what, and with what declared choices

The module is `engine/voynich_transcript_stats.py`; the report lives at
`docs/research-notes/voynich-transcript-stats.json`; the frozen tests are
`tests/test_voynich_transcript_stats.py`. The locus set is the worded loci
shared by ZL 3b and IT 2a, outside the reserved folios: 5,013 loci in the
identical folio and locus numbering of both files.

Reservation discipline, before any statistics existed: ten whole folios
were selected deterministically by sorting folio names under a sha256 hash
keyed with seed 20261020, taking the first ten. The selection function reads
only folio names and locus presence, never the text, so the reservation
cannot have been tuned to the statistics. The reserved folios are frozen in
this log, in the tests, and in the ledger's family 3 record:

f87r, f96v, f95r2, f68v1, f32v, f106r, f67r1, f36r, f82v, f24r

The declared statistics, all in the glyphs of the file's own EVA spelling,
with one `@nnn;` as one glyph and a maximal run of question marks as one:
sign frequencies (order 1), sign n-grams of orders 2, 3 and 4 inside words,
word token frequencies and type counts, and token lengths. Uncertain
readings resolve to their first option, commas join, and braces are
removed, the same frozen conventions as the parser. Statistics are at the
EVA-character level; the mapping from EVA characters to manuscript signs is
not asserted here.

## The measurement

Spearman rank correlation, over the types both files share, between the two
transcriptions on the same 5,013 loci:

| Statistic | Shared types | Spearman |
|-----------|--------------|----------|
| Glyph frequency | 23 | 0.999 |
| Bigrams | 292 | 0.965 |
| Trigrams | 1,337 | 0.937 |
| Quadgrams | 3,299 | 0.915 |
| Word tokens | 6,335 | 0.901 |

The files' aggregate counts on the same loci: glyph totals 184,310 (ZL)
against 184,092 (IT), a 218 glyph difference on about 184 thousand, 0.12
percent; word types 8,988 against 7,901; token totals 34,354 against
36,441, a 2,087 token difference, 6.1 percent; mean token length 5.37
against 5.05 glyphs. Same glyph content, different segmentation, one
thousand more ZL word types with fewer tokens.

## Controls

Two controls, both frozen as test assertions:

Within-file resampling baseline: each file's used loci are split alternately
into halves, and each statistic is compared half against half. This is what
the same metric does with two guaranteed samples of the same text, statistic
by statistic: ZL gives 0.912, 0.953, 0.893, 0.836, 0.732 (orders 1 to 4,
then words); IT gives 0.999, 0.970, 0.906, 0.851, 0.741. The
cross-transcription values sit at or above these ceilings at every order
beyond 2, and for word tokens the real agreement, 0.901, is far above the
baseline's 0.73 to 0.74, the largest gap in the table: word frequencies
agree across two different transcriptions better than this metric can
reproduce two random halves of one transcription.

Planted different answer: IT is relabelled by cycling its ten most frequent
EVA characters one rank over (a signed transposition of the kind a
translator's alphabet slip could produce), and the same comparison is run.
Glyph frequency falls to 0.954, bigrams to 0.404, trigrams to 0.100,
quadgrams to -0.067 and word tokens to 0.257. Margins over the real values:
0.04 (glyphs), 0.56 (bigrams), 0.84 (trigrams), 0.98 (quadgrams), 0.64
(words). The glyph-level margin is small by construction, since a rank
cycle inside the ten head characters leaves most ranks standing; the
detection criterion across all five statistics is what the tests pin.

A further synthetic control replays the whole pipeline on planted miniature
files: identical files must agree at 1.0 on every statistic, and a relabel
of the head characters must fall.

## Statement of the result, and its limits

On the declared statistics, the ZL and IT transcriptions measure the same
text stable enough that every statistic's cross-transcription agreement
reaches or exceeds the metric's own resampling ceiling. The thing that does
not survive unchanged is segmentation: for the same glyph content the two
files cut 6 percent more tokens in IT, and ZL produces one thousand more
word types with fewer tokens. That difference is family 2's question, not
family 1's, and there it will be measured by varying the declared
segmentation, not assumed.

Limits stated honestly: statistics are at the EVA-character level; Eva- and
EvaT rare-character conventions were reconciled only as far as the parser's
shared conventions go, so a share of the residual disagreement above the
baseline may be alphabet noise; the intersection-type selection is
restricted to types in both files; readings resolve to their first option.
Length-preserving permutation nulls remain deferred to family 3, as
planned, and ten reserved whole folios have stayed out of every statistic
here. Nothing in this log is a reading of the manuscript, and no
conclusion about language, cipher or meaning follows from it.

The transcription family closes with this measurement. The segmentation
family becomes the current first job.
