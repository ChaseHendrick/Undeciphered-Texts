Voynich MS: held-out prediction of the reserved folios - 20 October 2026

Fifth execution step for the Voynich case, and family 3's measurement: does
the text predict unseen folios better than shuffled text? The ten whole
folios reserved statistics-blind on 20 October (f87r, f96v, f95r2, f68v1,
f32v, f106r, f67r1, f36r, f82v, f24r) were measured today, and the
reservation's testing role is now discharged.

## What was computed, on what, and with what declared choices

The module is `engine/voynich_heldout.py`; the report lives at
`docs/research-notes/voynich-heldout-prediction.json`; the tests are
`tests/test_voynich_heldout.py`. Two statistics per file, declared in the
module header before the run: a glyph statistic (trigram likelihood of the
reserved folios' words under an add-one model trained on the shared worded
loci outside the reservation, one alphabet per file from the union of
training and reserved glyphs) and a token statistic (add-one word-type
bigram likelihood of adjacent pairs inside reserved loci under a model
trained the same way, pairs scored inside loci only).

One null per statistic, declared in the module header: the word-glyph null
permutes glyphs inside each training word (word lengths and the glyph
multiset exactly preserved, order destroyed), and the token null permutes
whole training tokens over all token slots (locus token counts and the
training word multiset exactly preserved, adjacency destroyed). Both nulls
therefore move only the thing their statistic scores. Budget: 1,000
seeded permutations per (file, statistic) cell, within the plan's cap of
at most 2,000 per test, each replicate its own numpy general random
generator seeded by the declared base seed, the cell, and the replicate
index, so every stored value reproduces in isolation. The verdict rule was
declared before the run: p = (one plus nulls at or below the real value)
over (permutations plus one); p at or below 0.01 is `detected`.

## The measurement

Reserved material per file: 201 shared worded loci, 1,410 tokens (ZL),
1,478 (GC), 1,477 (IT). All six cells:

| File | Statistic | Real NLL | Null range | Real below null min | p | Verdict |
|------|-----------|----------|------------|---------------------|---|---------|
| ZL   | glyph     | 7,454.0  | 12,153.7 to 12,390.0 | 38.7 percent | 0.0010 | detected |
| ZL   | token     | 10,810.5 | 10,882.7 to 10,934.2 | 0.7 percent  | 0.0010 | detected |
| GC   | glyph     | 7,325.6  | 10,438.4 to 10,616.5 | 29.8 percent | 0.0010 | detected |
| GC   | token     | 11,609.6 | 11,672.6 to 11,718.6 | 0.5 percent  | 0.0010 | detected |
| IT   | glyph     | 6,839.8  | 11,295.0 to 11,528.7 | 39.4 percent | 0.0010 | detected |
| IT   | token     | 11,195.8 | 11,280.5 to 11,331.1 | 0.8 percent  | 0.0010 | detected |

Every cell is detected at p = 0.0010, the smallest p the declared budget
can emit: the real statistic sits below every one of the 1,000 null values
in all six cells, across three files by four different authors or
lineages.

## The honest reading

The family question is answered yes. What is measured beyond the rule
itself matters more:

- Within-word glyph-order structure transfers to unseen folios at an
  enormous margin: 30 to 39 percent below the null floor. Under this
  declared statistic that means the seen folios share glyph-sequence
  scaffolding with the unseen folios far beyond what per-word content
  shuffling explains. Recurring word forms (the corpus's well known
  repeated vocabulary) are the natural carrier of this signal, together
  with any language-like glyph sequencing.
- Word-adjacency structure transfers too, but little: 0.5 to 0.8 percent
  below the null floor. The token nulls are narrowly spread, so the real
  value still lies outside all 1,000 draws, but the effect size is tiny
  compared with the within-word result. Under this machinery, most of the
  transferable structure lives inside words, and much less connects words.

Both patterns already had qualitative witnesses in the literature; what is
new here is that they are now measured under pre-declared statistics,
pre-declared nulls and pre-declared verdict rules, on reserved material
that no earlier family touched, with the machinery's power demonstrated in
both directions (below). Line-position structure is reached only through
the adjacency statistic as declared; a dedicated positional feature was
not added, and if family 4 or a later family needs one it must be declared
then.

## Controls

- Power, positive direction: a synthetic corpus whose words follow a
  template glyph rule is detected (zero nulls at or below real, at
  n equals 25 replicates); a synthetic corpus with a deterministic word
  adjacency rule using three word types is likewise detected. The
  adjacency instrument needed the third type: on a perfectly balanced
  two-type corpus a token shuffle reproduces the adjacency rates in
  expectation, so it is not a valid positive control, and the instrument
  was fixed before use.
- Power, negative direction: i.i.d. glyph-bag and i.i.d. token-bag
  synthetic corpora are NOT detected (at least one of the replicate nulls
  at or below the real value, p at least 0.05), confirming the machinery
  does not manufacture detection from noise.
- Reproducibility: with per-replicate declared seeds, the stored null
  heads of the artifact recompute exactly, and the committed artifact's
  real statistics recompute exactly.
- Triangulation: the same verdict falls out of three documents with
  different alphabets and different edition lineages, so no single
  transcription quirk carries the result.

## Statement of the result, and its limits

It is measured, so stated: the Voynich text predicts unseen folios better
than every declared shuffle, for within-word glyph order strongly and for
word adjacency weakly but beyond all replication noise, independently in
three files. This is a necessary condition for language-like structure,
not a sufficient condition, and it is compatible with plaintext, with
cipher, and with construction: no conclusion about language, cipher,
cipher-effort or meaning follows from this family. The machinery is
add-one smoothed trigram and word-bigram likelihoods, one declared lens;
other models remain unmeasured and any future family must declare its
own.

Limits: six cells were tested under the same declared per-cell rule
without a multiple-comparisons correction; with every cell pinned at the
floor p value this was immaterial to the verdict, and it is recorded
anyway. The reserved folios have now served their declared testing role
and are extinguished for reuse: family 4 must declare its own held-out
discipline if it needs prediction material. Nothing here is a reading.

Family 3 closes with power. Family 4, the first family to engage a
decipherment-shaped hypothesis, is now the first job.
