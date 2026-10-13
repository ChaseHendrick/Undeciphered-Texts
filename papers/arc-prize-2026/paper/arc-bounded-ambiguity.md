# Bounded Ambiguity in ARC Program Search

Chase Hendrick  
Independent Researcher  
ORCID 0009-0002-9754-6087  

## Abstract

At a fixed candidate budget of 4096 programs of depth at most two in a declared grid DSL, does selecting the two largest groups of demonstration-consistent predictions improve exact test-output accuracy over the first two distinct predictions? On the official ARC-AGI-2 public data the answer is no under this grammar. Output-weighted accuracy for the primary policy `group_vote` is 0.0257 on the development partition (800 tasks), 0.0273 on locked validation (200 tasks), and 0.0000 on the public evaluation set (120 tasks). The same figures hold for the `first_distinct` baseline. All results are numerical. No general reasoning architecture or prize is claimed.

## Introduction

ARC-AGI-2 requires exact recovery of held-out output grids from a few demonstration pairs. The present work is a prospective audit of ambiguity inside a finite, fully enumerated prefix of a small symbolic grammar. It follows the fixed protocol recorded in `PROTOCOL.md` before any real-task predictions. Program synthesis, voting, and version-space reasoning are established techniques; this baseline demonstrates none of them to be novel.

## Methods

The grammar `arc-dsl-v1` is defined by the ordered primitives in `engine/arc/dsl.py` (174 fixed operations plus zero to eight demonstration-fitted color maps). Programs contain one or two steps. Search examines a deterministic prefix of at most 4096 candidates per task. All three policies (`first_programs`, `first_distinct`, `group_vote`) share the identical candidate stream. Voting counts syntactically distinct consistent programs. The deployed policy is `group_vote`. Test answers are never consulted by the solver. Full details appear in `notes/METHODS.md`.

Data partitions follow the protocol: training IDs sorted by SHA-256 of `arc-prize-2026-v1:` + ID; first 800 development, last 200 validation; 120 official public evaluation tasks held separate. One incidental exposure of public training task `4cd1b7b2` is disclosed and left in its deterministic partition.

## Results

| Partition | Tasks | Test inputs | first_programs | first_distinct | group_vote |
|-----------|-------|-------------|----------------|----------------|------------|
| Development | 800 | 856 | 0.0245 | 0.0257 | 0.0257 |
| Validation | 200 | 220 | 0.0273 | 0.0273 | 0.0273 |
| Public evaluation | 120 | 167 | 0.0000 | 0.0000 | 0.0000 |

Figures are output-weighted exact-match rates under the Kaggle two-attempt rule. Task-level rates (every test input solved) are of the same order. Wall time on a single core was under two minutes per partition. Peak RSS remained under 60 MB. No policy separation reaches statistical significance under the planned 10 000-task bootstrap (intervals omitted; differences are zero or within sampling noise).

## Discussion

The grammar recovers a handful of trivial transformations on training data and none on the public evaluation set. Conditional uniqueness claims hold only inside the declared finite class and only when the search is complete. Incomplete search remains unknown. The result is a negative finding for this particular bounded search, not evidence against program synthesis in general.

## Limitations

The candidate budget and depth are deliberately small. Algebraically equivalent programs remain distinct and can bias syntax counts. No language model, external knowledge, or test-time training is used. Public ARC material may have appeared in the training corpora of the AI assistants used to write the code; the deployed solver contains no such model.

## Reproducibility

Source, protocol, data-preparation script, and evaluator are in the repository under `papers/arc-prize-2026/`. Predictions are sealed before scoring. Hashes of challenges, solutions, and prediction files are recorded in the run logs. New components are released under MIT-0; existing repository licenses are unchanged. ARC-AGI-2 data remains under Apache-2.0.

## Use of AI

This work was prepared with AI assistance. The author takes full responsibility for its content.

## Competition note

Version 2 of the private notebook Bounded Ambiguity in ARC Program Search completed on 13 October 2026: https://www.kaggle.com/code/chasehendrick/bounded-ambiguity-in-arc-program-search. Kaggle assigned that slug from the title. The requested slug `arc-bounded-ambiguity-2026` was not created. Version 1 failed because the challenge file is mounted at `/kaggle/input/competitions/arc-prize-2026-arc-agi-2/arc-agi_test_challenges.json`. Version 2 used that path, CPU, and internet disabled. The run wrote `submission.json` for 240 tasks and 259 test inputs. 511 of 518 attempts used the audited input-copy fallback. `submission.json` SHA-256 is `10f7aa8890613a2040fc0318e8d34e27523cf6a71fe6ca0ec9682aadf13109ee`. Submission reference 57137736 was accepted and is pending. No leaderboard score is available yet. The notebook is private.
