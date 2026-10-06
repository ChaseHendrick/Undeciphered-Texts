# Undeciphered-text research notes

Primary sources checked on **3 October 2026** for the first eight notes. Later notes keep their own dates. These notes distinguish a source's publication date from the date we inspected it. They are an evidence register and experiment plan, not a list of new decipherments. Availability failures and older status statements remain visible.

The case table is generated. `tools/refresh_docs.py` rewrites it from the `index-*` block in each note. A push to main runs that script and commits the indexes when they moved.

<!-- case-index:start -->
| Case | Problem represented here | Data entry point | Next measurable task |
| --- | --- | --- | --- |
| [Kryptos K4](kryptos-k4-2026-10-03.md) | Public cryptanalytic method not established by the checked sources; private archival knowledge documented | Sculpture transcription and disclosed clue coordinates | Separate fitted clues from reserved evidence |
| [Voynich manuscript](voynich-2026-10-03.md) | Unidentified script; encipherment uncertain | Yale MS 408 images and versioned transliterations | Measure sensitivity to transcription and segmentation |
| [Linear A](linear-a-2026-10-03.md) | Undeciphered language with conventional partial sign readings | SigLA sign occurrences and inscription metadata | Compare repeated sequences across held-out sites |
| [Indus signs](indus-2026-10-03.md) | Unresolved sign system and language | Authored studies and named concordances | Test sign prediction without duplicate-artifact leakage |
| [Rongorongo](rongorongo-2026-10-03.md) | Undeciphered script with material and reading uncertainties | Museum object records and authored tablet study | Separate originals, casts and line orientations |
| [Phaistos disc](phaistos-disc-2026-10-03.md) | Undeciphered inscription on one object | Heraklion Museum object description | Reconcile sign inventories before language fitting |
| [Zodiac Z13 and Z32](zodiac-short-ciphers-2026-10-03.md) | Short cryptograms with many compatible readings | FBI documents and the Z340 solvers' account | Measure ambiguity; reproduce Z340 separately as a control |
| [Dorabella](dorabella-2026-10-03.md) | Short historical cipher with ambiguous glyph orientations | Authored experimental paper and its facsimile | Compare transcription variants with matched synthetic controls |
| [D'Agapeyeff challenge](dagapeyeff-2026-10-05.md) | 1939 digit challenge with no public reading; measured structure is not a plaintext | Wikipedia digit block used by the engine, plus the solved exercise as the control | Fit quadgram models for French, German, Latin and a Russian transliteration, and rerun the keyed-square, nulls and four-square searches with planted texts in each language |
<!-- case-index:end -->

The case notes carry the citations supporting this table. The [machine-readable source register](source-register-2026-10-03.json) records access limitations and the claim each source supports. This dated collection does not certify current universal agreement or the absence of every proposed solution.

## What the engine can presently test

The classical text tools operate on declared Latin A-Z models. Bob ranks the cipher families it was trained to distinguish; its output is neither a reading of an unknown script nor proof of a key. Converting a glyph transcription to uppercase Latin letters does not turn it into an English ciphertext. Keep original images, stable sign identifiers, uncertainty markers, line and object boundaries outside that normalization.

Follow [AI-AGENTS](../AI-AGENTS.md), [QUALITY](../QUALITY.md), [WORKFLOW](../WORKFLOW.md) and [verification certificates](../verification-certificates.md). A source-backed known-key control validates an implementation within its stated domain. It does not independently validate a historical hypothesis.

## Experiment standards

The larger experiments proposed in these notes remain plans. Separately,
the [K4 composition run](../k4-focus/model-experiments-2026-10-03.md) and
[Dorabella attempt](../easy-unsolved-attempt-2026-10-03.md) contain executed
inputs, controls, output and limits. Neither recovered a verified historical
reading. These narrower runs do not complete the proposed experiments.

Before fitting a model, freeze source URLs and retrieval date, lawful corpus access, object and transcription versions, raw SHA-256, normalization rules, duplicate groups, train/validation/test split, model family, search caps and random seeds. Save disagreements instead of resolving them in favor of an attractive answer. Split entire related objects or folios when line-level splits could leak shared material.

Use a simple baseline and a matched known-answer control. Include null models that preserve relevant nuisance structure, such as text length or repeated-sign frequencies. Record every tried inventory and model, including negative results. Reserve independent evidence before search; do not use it to choose an alphabet, ranking corpus or preferred candidate. If it is later used for selection, rename it development evidence and obtain another independent test.

For ciphers, require a reproducible forward transform covering the complete supplied ciphertext, with every null, error and exception disclosed. For scripts, require consistent sign interpretation on unseen material plus independent linguistic or archaeological grounding. A frequency pattern, a plausible phrase, persona agreement, an illustration match or a high English score does not meet either standard by itself.

An exhausted budget is incomplete work. Exhaustive rejection within a finite model is a negative result for that model. A compatible partial reading is underdetermined. None automatically changes a case to solved.

## Work priorities and update triggers

First make the material and transcription auditable. Then reproduce a published method on a solved control, measure ambiguity or predictive structure, and only then propose a broader interpretation. These priorities are based on testability, not a ranking of which historical target is closest to a solution.

Recheck a note when its custodian updates access, a new inscription or independent transcription becomes available, a published bilingual anchor appears, or a complete public transformation is released. Record the new evidence and date rather than silently rewriting an older claim. Public search visibility should come from these accurate names, source links and useful experiments; no Google ranking outcome is promised.
