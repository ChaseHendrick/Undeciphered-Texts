# Dorabella: transcription uncertainty and matched experimental controls
<!--
index-id: dorabella
index-title: Dorabella
index-problem: Short historical cipher with ambiguous glyph orientations
index-data: Authored experimental paper and its facsimile
index-next: Two annotators mark orientations independently from permitted images, before seeing any candidate text; freeze at most four inventories
-->

Source check: **2026-10-03**. Category: historical cipher; no systematic reading is established by this note.

<!-- generated-status:start -->
## How close is this to solved?

**Unsolved. Plaintext recovered: 0 percent. 0 of 5 hypothesis families listed (0 percent) are closed with shown power; 3 are open. Reviewed through 2026-10-03.**

**In plain words.** In 1897 the composer Edward Elgar sent Dora Penny a short note of 87 small semicircle symbols. She never read it, and nobody has since. We ran standard letter-substitution searches on a published transcription. They produced several different, conflicting outputs, and tests on known messages of the same length showed the method is not yet strong enough at this length to settle anything.

Progress here means testing a cipher model with matched-length controls. At 87 symbols even the best-understood model failed to bring back a matched-length control, so a failure on Dorabella closes nothing yet.

| Status | Families | Share |
| --- | --- | --- |
| Open | 3 | 60 percent |
| Tested without shown power | 2 | 40 percent |
| Closed with shown power | 0 | 0 percent |

### Open (3)

| Family | Evidence |
| --- | --- |
| Alternative transcriptions of the ambiguous symbols | An older participant transcription differs at positions 33 and 77 after relabeling; neither was searched. |
| Languages other than English, and spacing rules | The 2021 study's language ranking is conditional model evidence; it was not reproduced here. |
| Music or another non-text encoding | Proposed by others; not tested here. |

### Tested without shown power (2)

| Family | Evidence |
| --- | --- |
| English under a one-to-one symbol key | Three annealing runs give three conflicting outputs; the matched-length control recovered 80 of 87 letters, not all. [log](../easy-unsolved-attempt-2026-10-03.md) |
| English under a many-to-one (homophonic) key | The best output merges ten symbol distinctions without a coherent message; the matched-length control recovered 34 of 87. [log](../easy-unsolved-attempt-2026-10-03.md) |

Generated from [`dorabella-status.json`](dorabella-status.json) by `tools/refresh_docs.py`.
<!-- generated-status:end -->

Hauer, Choi, Sundar, Hindle, Smallwood and Kondrak's 2021 primary experimental paper tests substitution, language, music and unusual-pattern hypotheses. Its transcription has 87 characters and acknowledges ambiguous orientations. Failed substitution trials weigh against the particular tested English monoalphabetic model; they do not prove that all encipherments or languages are impossible. [Experimental analysis](https://softwareprocess.es/pubs/hauer2021HistoCrypt-dorabella.pdf).

The paper's language-ranking results are conditional model evidence, not a decoded text. A musical or English-looking interpretation likewise needs a stable transform and independent support. No current universally accepted answer was established from the primary source inspected; later claimed readings were not exhaustively reviewed.

## Corpus and access

The authored PDF was accessible and includes a facsimile and its experimental transcription. This pass did not inspect the original autograph or authenticate a new glyph inventory. Preserve symbol arc count, orientation, line position and every disputed assignment. Any Roman code is a transcription convention, not an authentic Elgar key.

Before using the paper's transcription, freeze its version and identify ambiguous positions. Keep a visually justified alternative inventory as a separate input; do not rotate a difficult sign because it improves the candidate's English score. The manuscript's lack of spaces must not be silently replaced with boundaries learned from a preferred answer.

## Proposed next experiment, not executed here

1. Have two annotators independently inspect permitted images and record orientations before viewing candidate text. Limit the initial trial to at most four predeclared inventories; report agreements and unresolved positions.
2. Generate 100 fresh 87-character known-answer controls across declared languages and monoalphabetic keys. Retain removed-space and preserved-space variants as distinct control conditions. Record source-corpus hashes and keep test excerpts separate from ranking data.
3. Apply the same bounded solver configuration to every control and target variant: at most 50,000 total node or key checks, 20 retained witnesses and fixed seeds. Report full recovery rate on controls, score distributions on shuffled-sign nulls, and every target alternative rather than a selected phrase.

These are proposed budgets, not measured performance. A target score above a null does not establish correctness; score selection also spends evidence and must be recorded.

## Executed bounded follow-up

The [3 October open-target attempt](../easy-unsolved-attempt-2026-10-03.md) acquired the author's literal 87-label transcription from the [archived HistoCrypt code/data deposit](https://doi.org/10.5281/zenodo.4819086), then ran a frequency baseline, bijective annealing and relaxed homophonic annealing. No verified reading was recovered. Longer controls succeeded, but matched-length controls recovered only 80/87 and 34/87 positions; conflicting target outputs and absent independent historical plaintext prevent a solution claim. The [JSON record](../easy-unsolved-attempt-2026-10-03.json) preserves hashes, seeds, actual work counts and conditional replay limits. This smaller executed comparison does not complete the larger proposed experiment above.

## Evidence standard

A proposed reading should account for all positions with one disclosed method, key and spacing rule, and re-create the glyph sequence without undisclosed exceptions. Independent Elgar cryptographic material, if authenticated and not used to fit the target, could provide stronger external evidence. A personal-sounding sentence or a composer's musical vocabulary is not a reference plaintext.

The first useful product is a repeatable uncertainty/control comparison. Keep absence of a result, failure of a finite hypothesis and search-budget exhaustion as different outcomes. No persona's preferred words enter the mathematics or evidence ranking.

## Next steps

<!-- generated-next:start -->
Open families, in the order they are planned:

1. **Alternative transcriptions of the ambiguous symbols.** Two annotators mark orientations independently from permitted images, before seeing any candidate text; freeze at most four inventories.
2. **Languages other than English, and spacing rules.** Build 100 fresh 87-character controls across declared languages, with and without spaces, and report full-recovery rates before searching the target.
3. **Music or another non-text encoding.** State a fixed symbol-to-note rule in advance and test whether it reproduces all 87 symbols; a pleasing tune is not evidence.

Generated from [`dorabella-status.json`](dorabella-status.json) by `tools/refresh_docs.py`.
<!-- generated-next:end -->
