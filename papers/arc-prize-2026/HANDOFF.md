# ARC Prize handoff, 13 October 2026

## Goal and current state

Build Chase Hendrick's paper and a working linked ARC Prize 2026 competition submission. Save the work in ChaseHendrick/Undeciphered-Texts, branch codex/arc-prize-2026. No PR. Match the evidence and presentation standard of the owner's Zenodo papers, follow current contest rules, and do not use em dashes. This is unfinished research infrastructure, not a completed paper or qualifying submission. No real ARC benchmark has run and no Kaggle notebook has been uploaded or submitted.

Local checkout: /Users/chasehendrick/Desktop/arc-prize-2026
Baseline: 312c4dd3a7e5afb592ebd091d8983c450cee747d
Python: /Users/chasehendrick/scrolls-work/venv/bin/python (3.14). Code supports Python 3.10+ and standard library only.

The user stopped work for a handoff at 1% remaining usage. No jobs remain running. Do not spend compute merely to exhaust credit. No Modal launches. User authorized the actual ARC working submission and GitHub save; do not ask again merely to perform those tasks.

## Completed

- engine/arc/{grid,dsl,solver,__init__}.py: deterministic depth-two grid DSL, 4096 candidate prefix, all demonstration-consistent candidates, ambiguity witnesses and conditional exhaustive-grammar uniqueness. Exact methods and limitations are in notes/METHODS.md.
- Policies first_programs, first_distinct, group_vote share the identical candidate stream. The primary baseline is first_distinct. Voting is syntax count, not probability. Unknown remains unknown. A separate tagged input-copy fallback fills missing competition attempts.
- papers/arc-prize-2026/kaggle/{adapter.py,build_notebook.py,README.md}: self-contained CPU notebook, offline execution, stripped test outputs, strict submission validation, source/input/output hashes.
- PROTOCOL.md records a prospective fixed experiment. code/prepare_data.py separates challenges and scoring answers and makes hash manifests. It has not yet been executed or independently tested.
- 35 targeted tests passed in 0.254 seconds: python -m unittest tests.test_arc_solver tests.test_arc_kaggle -q. These are synthetic tests only. Full repository suite still required.
- Current generated bundle is ignored work/arc-kaggle/. Notebook ID intended: chasehendrick/arc-bounded-ambiguity-2026. Notebook SHA ae54df5ce77aa81c77954372b9c36e8d432e83e9a6a3c97e7b14bfd51a9710dc. Local fresh-process synthetic rotation smoke at actual4096 budget passed with socket operations blocked, zero fallbacks. Receipt: work/arc-kaggle-smoke/smoke-receipt.json. Rebuild and repeat smoke after any embedded source changes.
- Official data cloned into ignored work/ARC-AGI-2 at f3283f727488ad98fe575ea6a5ac981e4a188e49. No real tasks have been scored or inspected by the implementation team. One earlier web lookup incidentally exposed training task ID4cd1b7b2; disclose its deterministic split, do not move it.
- Real Chrome is signed in as chasehendrick. The owner said they joined. Root verified membership: ARC-AGI-2 now shows Submit Prediction, Team and Submissions tabs. Do not ask them to join ARC-AGI-2 again. Paper-track membership has not been verified. The in-app browser was signed out and should not be confused with Chrome.
- Kaggle CLI absent and no configured CLI credentials. Use the signed-in Chrome UI or obtain a scoped supported auth flow. Do not extract browser cookies/tokens. CLI OAuth defaults to broad resources.admin:* permissions; do not silently authorize it.

## Resume in this order

1. Read docs/AI-AGENTS.md, docs/QUALITY.md, docs/TESTING.md, docs/NOVELTY.md and docs/PUBLISHING-PAPERS.md. Inspect git status and this branch before editing. No reset, merge or PR.
2. Review the solver and packaging independently, using synthetic controls only. Review/test prepare_data.py. Source is frozen for planned v1; any necessary bug fix before real evaluation must be documented and sealed. Do not claim a completed independent review.
3. Freeze protocol, config and source hashes before real predictions. Run prepare_data.py --source work/ARC-AGI-2 --output work/arc-data. IDs sorted by SHA256('arc-prize-2026-v1:'+ID): first800 development, last200 locked validation;120 official public evaluation tasks separate. Do not inspect locked answers/grids.
4. Implement a research evaluator that generates all three policies from each single solve_task receipt, writes/seals predictions before reading the separate solution file, and then scores exact two-attempt outputs. Same4096 budget, primary policy group_vote even if baseline wins. No tuning from locked results. Record output-weighted accuracy plus all-test-input task accuracy, fallbacks, coverage, ambiguity, candidate/primitive counts, seconds and RSS. Paired whole-task bootstrap10000 draws seed20261013, percentile95% intervals for both policy differences. Run development, validation and public evaluation once each. Public evaluation is not competition-private score. Preserve failures. Current protocol has the complete specification.
5. Run full repo unittest discovery and python -m engine demo, report optional skips separately and inspect generated DEMO.md diff. Do not claim old or targeted tests establish a full pass.
6. Write actual manuscript with clear question, stated finite grammar, complete conditional proofs, generated data-bound numbers/tables, matched-budget ablation, failure analysis, related work, limitations, AI-use disclosure and reproducibility. Use notes/QUALITY.md U1..U7 based on existing dagapeyeff paper. Existing paper source and docs/PUBLISHING-PAPERS.md give author/ORCID and quality convention. Do not copy its scientific results into ARC. No manuscript/PDF exists yet, no DOI or peer review.
7. Build notebook: python papers/arc-prize-2026/kaggle/build_notebook.py --kernel-id chasehendrick/arc-bounded-ambiguity-2026 --output-dir work/arc-kaggle --max-candidates 4096 --policy group_vote. Verify actual attached competition mount/file in Kaggle: assumed /kaggle/input/arc-prize-2026-arc-agi-2/arc-agi_test_challenges.json has NOT been verified in a live notebook. CPU, Internet OFF, all IDs/two attempts/original order, submission.json.
8. Upload/run the exact frozen notebook and submit its successful version to the competition. Record notebookURL/version, submission reference, completed status, score/error and hashes. A saved URL or local smoke is NOT a working linked submission. Inspect daily allowance before submitting. No paid GPU required.
9. Link the actual working submission in the paper and complete paper-track submission. Public sharing must exclude hidden competition data and all unrelated private research. User authorized GitHub storage and the entry, not an invented claim. No prize prediction; earlier answer was plan on $0 pending evidence.

## Rules checked 13 October, recheck before submission

- https://arcprize.org/competitions/2026/paper requires working linked ARC-AGI-2 or3 Kaggle submission; high score not required for eligibility. Novelty/performance still unestablished.
- https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2/rules and overview: CPU/GPU notebooks <=12h, Internet disabled, public external data allowed. Exactly2 predictions per test input. One submission/day, up to2 finals, team<=5.
- Entry/team deadline26Oct2026 23:59UTC; final code2Nov2026 23:59UTC. Organizer says paper8Nov; Kaggle paper track9Nov23:59UTC. Work to earlier8Nov and disclose discrepancy.
- Organizer asks authored code/methods CC0 or MIT-0. Kaggle winner clause says CC BY4.0. Preserve this discrepancy and resolve required grants for the new components. New core files declare MIT-0. Existing repository and third-party licenses remain unchanged. ARC data Apache2.0. Existing papers default all-rights-reserved manuscripts, so do not blindly reuse that for a competition requiring open release.
- Read full current sources and cite claims. Program synthesis, voting and version spaces are established; this baseline has no demonstrated novelty. Public data may have been in AI assistant training; disclose that uncertainty despite no task lookup/model in deployed solver.

## What remains absent

Real ARC scores, measured end-to-end runtime, evaluator, full-suite run, finished independent review, manuscript/PDF, evidence-generated tables, complete new-component license grant, Kaggle upload/run/submission receipt, public notebook URL, linked paper submission, Zenodo release. Do not imply any exists.

## Update 13 October 2026 (sandbox continuation)

Real public scores measured under frozen protocol v1, max_candidates=4096, group_vote primary:

- Development (800 tasks, 856 outputs): first_programs 0.0245, first_distinct 0.0257, group_vote 0.0257
- Validation (200 tasks, 220 outputs): all policies 0.0273
- Public evaluation (120 tasks, 167 outputs): all policies 0.0000

Evaluator added at papers/arc-prize-2026/code/evaluate.py. Manuscript at papers/arc-prize-2026/paper/arc-bounded-ambiguity.md. Notebook built locally (not uploaded). Branch pushed (commit 727efe4). Kaggle upload/submission and paper-track linking remain pending signed-in Chrome session. No prize claimed. Protocol preserved. No PR, no Modal.
