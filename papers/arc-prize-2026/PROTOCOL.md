# Bounded ambiguity in ARC program search: protocol v1

Recorded on 13 October 2026 before any real-task predictions or scores from this
implementation. This is a prospective repository protocol, not an externally
registered study. Source hashes and a Git commit seal are recorded separately
before the locked runs.

## Question and scope

At the same finite program-search budget, does choosing the two largest groups
of demonstration-consistent predictions improve exact test-output accuracy over
the first two distinct predictions? The first two programs provide a second,
weaker baseline that can waste an attempt on a duplicate. The primary comparison
is group voting versus distinct outputs, not voting versus duplicate programs.

This is a small symbolic baseline and an audit of ambiguity. It does not claim
a new general reasoning architecture, calibrated confidence, or novelty of
program synthesis, voting, or version-space reasoning. Positive and negative
results will be reported together. A submitted notebook and a completed score
are separate from local benchmark results.

## Data and partition

Use only the official `arcprize/ARC-AGI-2` repository at commit
`f3283f727488ad98fe575ea6a5ac981e4a188e49`, under its Apache-2.0 license.
There are 1,000 public training tasks and 120 public evaluation tasks.
Sort training IDs by SHA-256 of UTF-8 `arc-prize-2026-v1:` followed by the ID.
The first 800 are development; the remaining 200 are locked validation.
All 120 official public evaluation tasks are a separate locked evaluation.
The public evaluation is not the private competition set.

The implementation team did not inspect locked task grids during development.
One earlier web lookup incidentally exposed public training task ID `4cd1b7b2`.
Its deterministic partition will be disclosed and not changed to improve results.
An AI coding assistant may have prior training exposure to public ARC material;
this study cannot certify absence of such exposure. The deployed solver contains
no language model, task-ID lookup, fitted benchmark weights, or stored answers.

Preparation removes every test answer from the solver input and writes answers
to a separate scoring file. The prediction command has no solution-file argument.
Scoring starts only after a complete predictions artifact has been sealed.
Dataset bytes, each original task, IDs, code, configuration, and result files
receive SHA-256 hashes. Do not print or visually inspect locked grids.

## Fixed method

Use `engine/arc` grammar `arc-dsl-v1`, depth at most two, a deterministic prefix
of at most **4,096 candidate programs per task**, and no wall-time selection.
The exact primitive inventory and order are defined by the hashed source.
All primitives and parameter fitting use demonstration pairs only. Undefined or
oversized intermediate grids reject that program on the affected input.
At a supplied test input, defined predictions are grouped by exact grid equality.

All policies share the same candidate stream, stopping point, and consistent
programs. Policies are: `first_programs`, `first_distinct`, and `group_vote`.
Voting counts syntactically distinct consistent programs, not semantic families
or probabilities. Ties use shortest representative program, then canonical
lexical program order. There are exactly two attempts per test input. An absent
attempt copies that input, and every such fallback is explicitly counted.

The deployed policy is **group_vote**, fixed before scoring, even if a baseline
wins locally. No weights, selection threshold, palette, or grammar will be tuned
using these locked results. Any later revision needs a new documented protocol
and these data must then be labelled development rather than untouched tests.

Search-prefix agreement is incomplete. Uniqueness is conditional on exhausting
the entire declared finite grammar, nonempty consistency, and all consistent
programs being defined and agreeing at the query. A pair of agreeing-on-training
programs that disagree at the query certifies ambiguity only within that grammar.

## Runs and readouts

Run synthetic tests first. Run development, locked validation, then locked public
evaluation, once each under the same frozen configuration. The development run
is descriptive and does not authorize tuning v1. If a software defect prevents
a valid run, preserve the failed artifact, document the defect and repair, and
restart under a new seal. Performance alone is not a defect.

Primary metric: the share of test inputs for which either of the two attempts
exactly equals the answer, matching the Kaggle scoring definition. Also report
the stricter share of tasks for which every test input is solved. No cell-level
partial credit. Report primary and baseline metrics, fallback counts, consistent
candidate coverage, ambiguity states, distinct-output groups, candidate checks,
primitive applications, wall seconds, and peak process RSS with platform units.

For each locked partition, report paired differences between voting and both
baselines. Use 10,000 bootstrap resamples of whole tasks, seed 20261013; compute
the test-output-weighted ratio anew in each resample. Report percentile 95%
intervals, total tasks and test inputs. These are descriptive uncertainty
intervals for a small public benchmark, not population guarantees. The voting
versus diversity comparison is primary; other comparisons are secondary.

Also report accuracy conditional on ambiguity state, including incomplete
agreement and unknown, without interpreting syntax counts as calibrated
probabilities. Report all partitions and all failed cases. No selective reruns,
secret-label access, or test-answer-based promotion.

## Competition execution and publication

Prepare a self-contained Kaggle CPU notebook with Internet disabled and output
`/kaggle/working/submission.json`. Read only the competition challenge file in
the notebook, never solution files. No installation, network calls, pretrained
model, or external runtime dataset is required. Verify two attempts, all task
IDs, original test order, grids of size 1..30 and integer colors 0..9.

Kaggle rules acceptance, completed notebook run, accepted scored submission,
public code link, and paper-track writeup remain separately recorded milestones.
Do not report a local dry run as a competition submission. No prize is predicted.
Check current official rules before each external step. The owner controls
personal eligibility and acceptance of competition terms.

Sources: [official data](https://github.com/arcprize/ARC-AGI-2),
[code competition](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2),
[paper requirement](https://arcprize.org/competitions/2026/paper).
