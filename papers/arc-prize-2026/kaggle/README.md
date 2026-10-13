# ARC-AGI-2 competition package

This directory builds a self-contained, offline CPU notebook from the current
`engine/arc/` sources. It does not accept rules, upload, execute on Kaggle, submit
an entry or publish a notebook. Local output validation is not a leaderboard
result. Record an actual Kaggle submission reference and completed status before
describing the paper as linked to a working competition submission.

## Local preparation

Use Python 3.10 or newer. The notebook and adapter use only the standard library.
From the repository root:

```bash
python -m unittest discover -s tests -p 'test_arc_kaggle.py' -v
python papers/arc-prize-2026/kaggle/build_notebook.py \
  --kernel-id chasehendrick/arc-bounded-ambiguity-2026 \
  --output-dir work/arc-kaggle \
  --max-candidates 4096 --policy group_vote
```

The username `chasehendrick` was verified in the signed-in browser on 13 October
2026. The intended private notebook is `arc-bounded-ambiguity-2026`; a generated
metadata ID does not mean that notebook has been uploaded. The builder writes
`arc-prize-2026.ipynb`, `kernel-metadata.json` and `source-manifest.json`. Metadata
is private, CPU-only, internet-disabled and bound to
`arc-prize-2026-arc-agi-2`. Rebuild after any solver or adapter change. Keep
generated bundles, competition inputs and inference outputs under ignored
`work/`; review any future public artifact separately.

The builder copies Python sources only from `engine/arc/` and this adapter. It
creates a minimal `engine` namespace, so unrelated cipher imports or optional
dependencies are not carried into the notebook. Each embedded source and the
builder have SHA-256 seals. The notebook verifies its embedded source, then
writes that manifest alongside its output. `submission-audit.json` binds the
manifest, sanitized challenge inputs and predictions by canonical JSON hashes.
The source manifest seals content; it does not prove the source is correct.

The notebook reads
`/kaggle/input/arc-prize-2026-arc-agi-2/arc-agi_test_challenges.json` and writes
`/kaggle/working/submission.json`. `ARC_INPUT_PATH` and `ARC_WORK_DIR` overrides
exist for constructed local smoke tests, not for choosing hidden evaluation
labels. No data, pretrained model, API call, download or package installation is
embedded. The notebook has no stored cell outputs.

For an already staged local challenge file:

```bash
python papers/arc-prize-2026/kaggle/adapter.py \
  --input work/arc-data/local_challenges.json \
  --output work/arc-kaggle/local-submission.json \
  --audit work/arc-kaggle/local-audit.json \
  --max-candidates 4096 --policy group_vote
```

This command imports the checkout's engine. The generated notebook instead uses
the embedded source snapshot. Challenge files must map task IDs to ARC tasks.
The caller controls development, validation and evaluation access; this adapter
does not define an experimental split.

## Output and uncertainty contract

The solver sees training input/output pairs and test inputs only. Any supplied
test output or extra task metadata is removed before inference. Each requested
test input receives exactly `attempt_1` and `attempt_2`, in original test order.
Every grid must be rectangular, 1 to 30 cells on either axis, with integer colors
0 through 9. Booleans, extra attempts, missing task IDs and duplicate JSON keys
are rejected.

For a deliberately unavailable (`null`) solver prediction, the adapter copies
that test input as a legal fallback. Each fallback is separately tagged in the
audit. It is not classified as a recovered answer, forced prediction or
additional consistent program. Invalid non-null predictions fail the run;
exceptions are not hidden by fallback generation. Research comparisons must
report solver coverage separately from official-format fallback scores. The
first-program, first-distinct and group-vote policies share this same fallback
rule. A failed rerun removes older output files to prevent stale submissions.

The bounded grammar is not a universal ARC solver. Consistency with the supplied
examples is not proof of the intended rule. Any uniqueness or ambiguity status
is conditional on the stated finite grammar and whether its search completed.

## Verified competition constraints and unresolved text

Checked on 13 October 2026 against primary organizer pages and the live Kaggle
competition UI. Recheck before submitting, since organizers may revise rules.

| Topic | Current published requirement or discrepancy | Source |
| --- | --- | --- |
| Execution | Notebook submission, no internet, CPU notebook at most 12 hours or GPU notebook at most 12 hours. Public external data and pretrained models are permitted. This package uses CPU and no external model. | [Kaggle code requirements](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2/overview/code-requirements) |
| Output | A file named `submission.json`, all challenge IDs, two guesses per test input using `attempt_1` and `attempt_2`. | [Kaggle evaluation](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2/overview/evaluation) |
| Submission limits | At most one submission per day and up to two selected final submissions. Teams have at most five members. | [Kaggle rules](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2/rules) |
| Code dates | Entry and team merger: 26 October 2026 at 23:59 UTC. Final code submission: 2 November 2026 at 23:59 UTC. | [Kaggle timeline](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2/overview/upgraded-accelerators) |
| Paper requirement | A working, linked Kaggle submission in ARC-AGI-2 or ARC-AGI-3 is required. A high code score is not required for paper eligibility. | [Official paper rules](https://arcprize.org/competitions/2026/paper) |
| Paper deadline conflict | Organizer overview says 8 November; Kaggle paper track says 9 November 2026 at 23:59 UTC. Use the earlier 8 November target until clarified. | [Organizer overview](https://arcprize.org/competitions/2026), [Kaggle paper track](https://www.kaggle.com/competitions/arc-prize-2026-paper-track/overview/abstract) |
| Authored-code license conflict | Organizer overview specifies CC0 or MIT-0 for submitter-authored competition code/methods; Kaggle ARC-AGI-2 Rules identifies the winner-license provision as CC BY 4.0. These are different licenses. Keep the discrepancy visible and resolve the release obligations before submission or prize acceptance. | [Organizer overview](https://arcprize.org/competitions/2026), [Kaggle rules](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2/rules) |
| Third-party materials | Organizer requirements distinguish authored code from third-party components, which must permit appropriate public sharing. Preserve source licenses and attribution rather than relabeling the whole repository or ARC data. | [Organizer overview](https://arcprize.org/competitions/2026) |

The Kaggle Rules page calls its $275,000 rubric award the Innovation Prize,
while the overview calls it the Grand Prize. This packaging does not infer
eligibility or promise an award from either label. The local rule check did not
accept binding terms. The preexisting repository license is not changed by this
builder; any new competition-component license must be explicitly scoped by
the repository owner.

## Kaggle completion and receipt checklist

The owner must be signed in to the correct account and have reviewed and
accepted the competition's rules. Account sign-in and legal rule acceptance are
separate from a locally validated package. Never put credentials in this repo,
notebook, output receipts or chat.

After the package has been reviewed and the owner authorizes execution:

1. Confirm the username, competition membership and current daily submission
   allowance. Confirm the final source manifest and chosen policy/budget.
2. Save the private notebook with its competition data attachment and CPU,
   internet-off settings. Run it and inspect its completed version and outputs.
3. Submit that exact successful notebook version and `submission.json` to the
   ARC-AGI-2 competition. Record the returned submission reference.
4. Check submission completion, score or error. Preserve the notebook URL,
   exact version, submission reference, timestamp, source manifest and output
   hashes. A saved notebook URL alone does not establish a working submission.
5. Add those verified links and facts to the paper. When release is authorized,
   satisfy applicable public sharing and licensing obligations, then prepare
   the public paper and Zenodo release. Do not expose competition-private data
   or hidden inference outputs in a public repository.

The current [official Kaggle CLI](https://github.com/Kaggle/kaggle-cli) supports
notebook-version submissions. The following commands are documentation only;
the builder does not invoke them:

```bash
# Upload AND run by default. --no-run saves without launching a run.
kaggle kernels push -p work/arc-kaggle
kaggle kernels status USERNAME/NOTEBOOK_SLUG/VERSION
kaggle kernels output USERNAME/NOTEBOOK_SLUG/VERSION -p work/arc-kaggle/output
kaggle competitions submit arc-prize-2026-arc-agi-2 \
  -k USERNAME/NOTEBOOK_SLUG -v VERSION -f submission.json \
  -m "Frozen source manifest and paper experiment"
kaggle competitions submission SUBMISSION_REF
```

See [kernel metadata](https://github.com/Kaggle/kaggle-cli/blob/main/docs/kernels_metadata.md),
[kernel commands](https://github.com/Kaggle/kaggle-cli/blob/main/docs/kernels.md),
and [competition commands](https://github.com/Kaggle/kaggle-cli/blob/main/docs/competitions.md).
Current CLI OAuth requests `resources.admin:*` by default; review its permission
grant rather than silently initiating account authorization. See the official
[authentication guide](https://github.com/Kaggle/kaggle-cli/blob/main/skills/references/auth.md).

The local tests use constructed grids only. They test exact output shape,
label exclusion, fallback attribution, rejected corruption, deterministic
bundling and fresh-process notebook execution with network operations blocked.
They do not establish Kaggle acceptance, runtime on the complete competition
test set, model quality, novelty or paper eligibility.
