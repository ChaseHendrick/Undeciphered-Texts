# Bob: optional frozen-teacher distillation, 3 October 2026

This adds an opt-in preservation objective to the existing warm-start training
path. It transfers the incumbent ensemble's probability relationships on
generated training examples while retaining their correct synthetic family
labels. It is a family-ranking experiment, not plaintext recovery or a
historical decipherment. No K4 labels or clues enter this training path.

The source method is [Hinton, Vinyals and Dean, *Distilling the Knowledge in a
Neural Network*](https://arxiv.org/abs/1503.02531), section 2. The paper describes
soft probability targets, a shared softmax temperature, and a temperature
squared multiplier when combining soft and correct-label objectives. Bob uses
those established ideas as a preservation penalty in the same residual
ensemble architecture. It does not claim a new distillation algorithm or a
smaller deployed model.

## API and mathematical objective

```python
from engine.neural_router_v2 import train_router

metrics = train_router(
    warm_start=True,
    distillation_strength=0.1,
    distillation_temperature=2.0,
    learning_rate=0.0003,
    train_per_class=256,
    epochs=250,
    hidden=96,
    ensemble_size=3,
    write=False,
)
```

`distillation_strength` defaults to zero and must be finite in `[0, 1]`.
`distillation_temperature` defaults to 2 and must be finite in `[0.5, 10]`.
Booleans and nonnumeric settings are rejected. Positive strength requires an
incumbent warm start. The CLI exposes `--distillation-strength` and
`--distillation-temperature` alongside `--warm-start` and `--learning-rate`.

For each generated training row, freeze the mean of the incumbent ensemble's
raw logits, then compute teacher distribution `q = softmax(teacher_logits / T)`.
For student logits `z`, let `p = softmax(z / T)`. The added loss is

```text
L_teacher = strength * T^2 / N * sum_rows KL(q || p)
dL_teacher/dz = strength * T / N * (p - q)
```

The implementation includes the teacher row sum in the derivative after
roundoff normalization. Teacher probabilities remain fixed during
backpropagation. The full objective retains the weighted, label-smoothed
correct-label cross entropy and the existing paired-dropout consistency term,
then adds `L_teacher`. The supervised coefficient remains 1. Distillation
temperature is distinct from the later calibration temperature used for
inference.

Log probabilities use max-centered log-sum-exp. Zero teacher probabilities
contribute zero without evaluating their logarithm. Malformed distributions,
nonfinite numbers and unrepresentable arithmetic are rejected. The objective
allows up to 20,000 rows and 128 classes, covering two dropout views of the
fitter's bounded 10,000-row training matrix. Both views receive the same frozen
targets.

Strength zero bypasses teacher evaluation and preserves the current numerical
training path, gradients, random draws, parameters and default result fields.
Inference and feature extraction are unchanged. Formats 2 through 8 retain
their existing replay behavior.

## Data and compatibility boundaries

The high-level trainer obtains teacher targets only from incumbent models on
generated examples from the training portion of the Austen corpus. Teacher
evaluation receives neither checkpoint-validation, calibration nor Doyle
comparison rows. Known synthetic family labels still supervise training. The
low-level fitter's teacher ensemble must preserve the incumbent input width,
hidden width and output-class count; the high-level warm-start path also
requires exact family order, ensemble size, training prose and prefix-compatible
feature semantics. V6/V7 artifacts remain readable, but cannot discard their
extra features to warm-start V8.

The incumbent's byte hash is captured while loading the frozen teacher. A
changed file during loading fails before sampling; a changed incumbent before
a promoted write refuses replacement. Metadata records the captured teacher
identity rather than rereading its identity after training.

The existing disjoint Austen slices select checkpoints and calibration. Both
already reused Doyle comparisons remain development gates. The incumbent
itself has been selected with those comparisons, so its soft targets inherit
that prior selection history. Distillation is not a new independent audit.
No frozen final corpus is fitted, no Wells evaluation is repeated, and no new
historical target is treated as a labeled training example. Teachers can be
wrong; an added preservation term is not a guarantee of improvement.

## Predeclared single trial

The one trial was fixed before observing its evaluation:

| Setting | Value |
| --- | --- |
| Teacher | Shipped V5 incumbent, frozen mean-logit ensemble |
| Teacher SHA-256 | `d8c985dfdaf2d1dd0e17cfdb8412d0f947221b3f9e30318169d9183145c5c825` |
| Candidate source/features | Format 8 / `cipher_statistics_v8`, 148 features |
| Distillation strength | 0.1 |
| Distillation temperature | 2 |
| Peak learning rate | 0.0003, existing cosine schedule |
| Training samples | 256 per family, 20 families |
| Epochs / ensemble / hidden width | 250 / 3 / 96 |
| Base seed | 20261002; existing per-network offsets of 997 |
| Checkpoint rule | Correct validation labels, then NLL; checkpoint zero and earliest exact ties retained |
| Promotion rule | No additional errors on either fixed 480-case or 204-case comparison; artifact at most 4 MiB |
| Production writes | Disabled during the trial |

Strength 0.1 adds a modest preservation term while keeping the synthetic-label
objective at full weight. Temperature 2 softens the incumbent distribution.
These values are a declared conservative experiment, not values selected from
the trial's comparison scores. No further tuning is part of this run.

The trial was **rejected**. It improved the 480-case comparison by three correct
labels, but lost two correct labels on the 204-case comparison. The existing
zero-regression gate retained the shipped V5 artifact. No second distillation
trial or tuning followed this result.

| Comparison | Incumbent V5 | Distillation candidate |
| --- | --- | --- |
| Reused 480-case top one | 428/480 | 431/480 |
| Reused 480-case top three | 477/480 | 476/480 |
| Reused legacy top one | 193/204 | 191/204 |

The serialized candidate is 1,612,234 bytes. Its exact bytes and full metrics
were retained in the local task work directory as
`bob-distillation-candidate.json` and `bob-distillation-trial.json`. Neither was
installed as the shipped model. The concise reproduction record is:

```json
{
  "status": "rejected",
  "seed": 20261002,
  "distillation_strength": 0.1,
  "distillation_temperature": 2.0,
  "learning_rate": 0.0003,
  "train_per_class": 256,
  "epochs": 250,
  "hidden": 96,
  "ensemble_size": 3,
  "source_file_sha256": "1212b53c1b9b01adc72507163ae41fc48d59738b967c8d103dec39763bd76f35",
  "teacher_sha256": "d8c985dfdaf2d1dd0e17cfdb8412d0f947221b3f9e30318169d9183145c5c825",
  "candidate_sha256": "fb1e3c309746fba32d2996c51245a6c71a1501fbfa2efe420dd87b9e1f50a820",
  "artifact_bytes": 1612234,
  "checkpoint_epochs": [75, 90, 15],
  "calibration_temperature": 1.0,
  "correct": 431,
  "total": 480,
  "top3_correct": 476,
  "benchmark_correct": 191,
  "benchmark_total": 204,
  "train_sha256": "e5678102f300af1ba71cb63da50c9b037fbed9282c18a2c2369cee0cf5112bcc",
  "validation_sha256": "fa3e19ce8046fc2d6e7a64c1432d55834313d7e74e1f2a9393a6c0d44a41c02e",
  "calibration_sha256": "aa0dc75b524b6ab09fb267780db5e9ed92cd017e3aeb2aed40d0c5f8ee2f7add",
  "comparison_corpus_sha256": "cbee687d0c9465488180c158b20542777681e2b1900ca4015caa9d25aaba162a",
  "elapsed_seconds": 83.298,
  "promoted": false,
  "shipped_model_unchanged": true
}
```

The source-file hash identifies `engine/neural_router_v2.py` during this trial.
Elapsed time includes concurrent local verification load and is not a
comparative speed benchmark. The script verified that the shipped V5 bytes
and unrelated duplicate weight file remained unchanged.

## Verification

The initial six new tests failed on the missing objective and unsupported API
before implementation. A separate regression reproduced source drift reaching
sampling before the provenance fix. All eight new tests now pass. The combined
41-test focused check also covers existing warm-start normalization preservation,
artifact promotion, classification gradients and format 2 through 8 feature
compatibility.

Controls independently evaluate the KL loss, finite-difference every logit and
every parameter of a small residual network, verify additive synthetic-label
gradients despite a wrong teacher, reject invalid domains and architectures,
check frozen targets against an independent ensemble calculation, distinguish
training rows from validation sentinels, and prove the exact zero-strength
path. These tests verify the implementation; only the recorded trial gates
determine whether its candidate can replace the incumbent.
