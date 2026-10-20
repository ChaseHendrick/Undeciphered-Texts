Voynich MS: IVTFF parser and first agreement table - 19 October 2026

Second execution step for the Voynich case, same working day as the corpus
freeze. The build has two committed pieces, `engine/voynich_ivtff.py` (the
parser) and `engine/voynich_compare.py` (the locus alignment), with 17 tests
in `tests/test_voynich_ivtff.py` and `tests/test_voynich_compare.py`. The
machine-readable result is `docs/research-notes/voynich-transcript-agreement.json`.
Nothing here is a reading, and nothing follows about language, cipher, or
meaning.

## What the parser had to agree with

The file grammar was built from the corpus source's own documentation: the
IVTFF Format Definition 2.0.2, issue 08/07/2025, R. Zandbergen
(https://www.voynich.nu/software/ivtt/IVTFF_format.pdf), whose PDF text I
extracted and used while designing the parse, plus the transliteration page's
summary tables (transcr.html, site update dated 31/05/2025). The PDF was
fetched to the ignored `work/` directory (sha256
7ac9c4a82064763cac8767cca6f661cc4e1b4503ab9342acc03032ddb6939d49) and is
cited, not vendored. The site's own command line tool ivtt, version 2.4
(https://www.voynich.nu/software/ivtt/ivtt.c), was compiled locally on 19
October 2026 purely to pin down the exact semantics of the site's published
word counts; the parser does not depend on it and ships no binary.

The parser's counting convention reproduces the site's ivtt extraction with
uncertain spaces not counted: definite separators are `.`, `<->` and `<~>`;
commas join; uncertain readings `[a:b]` resolve to their first option;
ligature braces are removed; one `@nnn;` is one glyph; a maximal run of
question marks is one glyph. Uncertain joins are recorded per locus, so the
split on commas is recoverable later.

## External validation of the parse

Against the site's published statistics table (transcr.html, Table 9), the
parser reproduces, for the three frozen files, all three published counts
exactly:

| File | Loci (published) | Paragraphs (published) | Long words (published) |
|------|-----------------|------------------------|------------------------|
| ZL 3b | 5,385 (5,385) | 740 (740) | 36,278 (36,278) |
| GC 2a | 5,367 (5,367) | 775 (775) | 38,242 (38,242) |
| IT 2a | 5,215 (5,215) | 772 (772) | 37,919 (37,919) |

Other structural checks built into the tests: page counts 227 / 226 / 225
(the rosette fold-out fRos is covered by ZL and GC and absent from IT); the
one invalid-labelled locus, f89v2.26 (a word showing through from the other
side of the leaf, removed by ZL in May 2025), is carried by GC and IT and by
no other; the freeze logs' version strings all match. The parse produces no
warnings on any of the three files.

During development the official ivtt tool was also run on all three files
under several option sets; its `-x8` mode (words with uncertain spaces not
counted) is the one matching the published counts, and the parser's
normalisation is that convention. For the record, where the two differ: ivtt
`-x8` returned 36,278 / 38,241 / 37,918 for ZL / GC / IT, one word below the
published GC and IT figures, because ivtt drops the invalid-marked locus line
that those published counts still include; the parser counts every locus line
in the file and therefore lands exactly on the published numbers. The
exploratory counting used before the parser landed is superseded by the
tests.

## The agreement table, first pass

Shared loci are matched by (folio, locus number). Word tuples are compared
only within the same alphabet family, which over the frozen files means ZL
against IT only; for pairs with GC the comparison reports structure and word
counts without comparing glyph strings.

| Pair | Shared loci | A alone | B alone | Shared with equal word count | Identical word tuples | Words matched in place |
|------|------------|---------|---------|------------------------------|----------------------|------------------------|
| ZL vs IT (Eva vs EvaT) | 5,214 | 171 | 1 | 3,511 (67.3%) | 2,240 (43.0%) | 30,625 of 38,030 (80.5%) |
| ZL vs GC (Eva vs v101) | 5,366 | 19 | 1 | 3,713 (69.2%) | not comparable | not compared |
| GC vs IT (v101 vs EvaT) | 5,214 | 153 | 1 | 3,867 (74.2%) | not comparable | not compared |

The ZL-alone loci are mostly the rosette fold-out fRos (160 loci against IT,
12 against GC), which IT does not cover; scattered singles elsewhere (f2r,
f116v, f102r2). The B-alone locus in every pair is the invalid f89v2.26.

For the ZL-IT pair the shared loci fall into agreement bands: 2,240
identical, 1,935 with at least two thirds of words matched in place, 713 with
one third to two thirds, and 326 under one third. The locations of least
agreement cluster in the astronomical and cosmological circular and radial
text: f72v3 (0.347), f72v2 (0.436), f67v2 (0.452), f72r3 (0.533), f67v1
(0.541), f73r (0.583) among folios with at least 30 shared words. An example
of a least-agreed locus, f100r item 6: oraro in ZL against osaro in IT.

## Recorded caveats, stated as uncertainties and not resolved here

- Word comparison reflects the frozen normalisation choices (first-option
  readings, commas joined, braces removed). Disagreements are not yet
  classified at glyph level; the next step belongs to family 1's
  transcription-statistics question.
- EvaT and Eva- differ in the versions of EVA Takahashi and Zandbergen
  publish; the parser counts their rare glyphs as single tokens without
  reconciling any systematic differences between those alphabets, so a small
  part of the ZL-IT disagreement may be alphabet-conversion noise rather
  than transcription disagreement in the study sense.
- Cross-alphabet pairs (word counts only) can disagree by one word under
  either alphabet's own split-and-refactor conventions; the note stands in
  the JSON for each such pair.

## Next steps on the ledger

Family 1 asks whether statistics survive a change of transcription, and the
descriptive agreement table above is its prerequisite, not yet its
measurement. The remaining work in order: (1) pick the statistics set (sign
and word frequencies, orders 1 to 4 n-grams, token lengths) and compute them
on the shared loci for the ZL-IT pair, plus held-out folio prediction against
the length-preserving permutation nulls of family 3; (2) recompute under
declared segmentation choices for family 2. Family status stays open until
those measurements exist.
