Voynich MS: the declared substitution screen - 20 October 2026

Sixth execution step for the Voynich case, and family 4's first
measurement: the first test of this program that aims at a
decipherment-shaped hypothesis, run under the house rule that its power
is measured on synthetic controls before any real-text number is
interpreted.

## The hypothesis class declared before the run

Voynichese, in a given file, is the result of a one-to-one (monoalphabetic)
substitution cipher of running text in a known natural language, with the
text's word divisions carried through the cipher, where every plaintext
letter's cipher symbol lies among that file's most frequent glyph
characters (up to 26) plus the word-boundary mark. Everything else is
outside this declaration: homophonic or polyalphabetic substitution,
word-level ciphers, transpositions inside words, inserted nulls, and
abbreviated script are not measured by this unit and are recorded in the
ledger as the declared next directions.

Material: the shared worded loci outside the reserved folios, exactly as
in families 1 to 3. The ten reserved folios are excluded wholesale (the
conservative choice; such a screen has no holdout role for them anyway).
Each file keeps its own transcription's glyph characters, with such
defects as each transcription has, for example ZL's frequent zero-knowledge
runs carried by the declared question-run glyph and two high-code
ligature glyphs, and GC's Currier digit-marked glyph characters.

## Reference languages and their declared processing

Two declared references, frozen as files in `engine/data`, each the
public-domain prose of its language, fetched from Project Gutenberg and
recorded by sha256 in the artifact: English, Pride and Prejudice
(ebook 1342), 692,537 processed symbols, 18.6 percent space; Latin,
Augustinus, Confessiones (ebook 33849), 858,522 processed symbols, 15.8
percent space. Processing body of the source only: expand the ligature
letters into letter pairs, case-fold, non-letters become spaces, space
runs collapse; then an add-one bigram log-likelihood table over the 26
letters and space. One prose source per language is a declared scope
limit; a second reference per language is exactly the declared next
instrument, for the reason this log gives at the end.

## The machinery declared before the run

Per file: the declared glyph form of every word, one word-boundary mark
between every two adjacent words whether inside a locus or across a locus
edge; the mapped set, the file's most frequent glyph characters up to 26
plus the boundary mark, ties by character order; a file whose inventory
over the material is smaller maps its whole inventory (IT maps 23, and
kept everything, kept share 1.0; ZL kept 99.9 percent, GC 97.9 percent,
the rest declared outside the mapped set with no bigram counted across
such a gap). Per (file, language): the bigram count matrix over the
declared stream, and the search, a greedy swap hill-climb over all
assignments of the mapped positions to the 27 plaintext symbols from one
frequency-rank initialisation and 16 seeded random restarts, sweeps
capped at 200. The reported number is the best mean log-likelihood per
counted pair, natural-log nats. The recovered mappings are deliberately
not recorded anywhere in this unit's output: an optimal relabelling of
the manuscript's stream would look like a reading, and this family
produces exclusions, not readings.

## The power instruments

Plants: 5 per (file, language), the reference's own processed stream
encoded through a seeded permutation of the mapped positions and cut to
the file's stream length, machinery identical. Floors: 5 per (file,
language), the file's kept-position mapped values permuted over the kept
slots, so the multiset, the kept share, the symbol counts, and the gap
structure are exact while adjacency is destroyed. Seeds, one rng per
cell, declared in the module header, so every stored number recomputes
in isolation and the tests do exactly that.

## The table

Real best (nats per pair), the plant band, the floor band, the margins,
and the verdict the declared rule emits (rule: real at or above the
smallest plant is consistent-with-substitution; real at or below the
largest floor is not-consistent; between them, indeterminate):

| File | Language | Real | Plants (5x) | Floors (max) | To floor | To plants | Verdict |
|------|----------|------|-------------|--------------|----------|-----------|---------|
| ZL | english | -5.2832 | -5.1422 | -6.6068 | +1.3236 | -0.1410 | indeterminate |
| ZL | latin   | -5.3162 | -5.0742 | -6.4983 | +1.1821 | -0.2420 | indeterminate |
| GC | english | -5.3536 | -5.1430 | -6.5788 | +1.2252 | -0.2106 | indeterminate |
| GC | latin   | -5.3883 | -5.0743 | -6.5584 | +1.1701 | -0.3140 | indeterminate |
| IT | english | -5.2541 | -5.1422 | -6.5855 | +1.3314 | -0.1119 | indeterminate |
| IT | latin   | -5.2933 | -5.0740 | -6.4740 | +1.1807 | -0.2193 | indeterminate |

All four plants per band converged to exactly one value (twenty of
twenty at plant parity across the five plant seeds per language), which
is the machinery's own adequacy witness: restarts reach the same optimum,
and the declared 48-restart probe in the tests does not beat the stored
best by more than a ten-thousandth of a nat on the rechecked cells.

## The honest reading

- The machinery knows what a substitution looks like: on twenty of
  twenty plants it recovered parity exactly, and it is invariant to the
  glyph labels it receives (tests, on synthetic languages too).
- No relabelling of the real text, over the full search space the class
  allows, reaches what the substitution of the reference prose itself
  achieves: the real text sits 0.11 to 0.31 nats per pairwise gap below
  plant parity, cumulative on the order of tens of thousands of nats,
  consistently across the three transcriptions and both languages.
- What that does NOT yet exclude: the plant band is self-parity, text
  and model of one prose. A genuine member of the class scored a second
  prose belonging to the same language against the same model would sit
  somewhat below self-parity, plausibly in the very 0.1 to 0.3 range
  measured here. Therefore the declared verdicts are, exactly as the
  rule demands, indeterminate. A cross-text calibration band is the
  declared next unit of this family.
- What is measured beyond the rule: the real text stands 1.17 to 1.33
  nats per pair above its own destroyed-adjacency floors in all six
  cells. Its glyph-level bigram structure aligns with any language
  table much better than its own structureless shadow does, in all
  three files - consistent with family 3's conclusion that the measured
  structure lives inside the words, and a statement that this machinery
  is not blind on real material.

Cross-check worth recording: ZL's stream word count, 34,354, is exactly
family 2's token count on the same locus set, so this unit's parser
delegation is verified against its predecessor's frozen bookkeeping.

## Statement of the result, and its limits

It is measured, so stated: to bigram resolution, under the declared
inventory-bound search and these two reference proeses, the manuscript's
text sits between its substitution-parity band and its
destroyed-adjacency band in every one of six (file, language) cells,
about 0.11 to 0.31 nats per pair below parity and about 1.2 to 1.3 nats
per pair above destruction - too far below self-parity to be explained
by a substitution of exactly these two proeses, too close to them and
too far above destruction for this machinery alone to exclude the
language class as scoped. The verdict rule emitted indeterminate on all
six cells, honestly.

Limits: bigram resolution only; one reference prose per language,
self-calibrated; cross-text penalty unmeasured (the declared next);
inventory-bound mapped set; one-to-one substitution only; every
non-simple cipher class unmeasured. Nothing here is a reading, no
mapping is published, and no claim about language, cipher or meaning is
made beyond the scoped instrument's verdicts.

Family 4 stays open: measured once, with its power instruments green,
its verdict withheld because the calibration band (cross-text plants of
a second reference prose per language) is exactly what this unit's own
numbers prove the instrument still needs before it can say what the
band membership would mean. That unit is next, and if its band clears
the real text the class exclusion is there to read in its own declared
format.
