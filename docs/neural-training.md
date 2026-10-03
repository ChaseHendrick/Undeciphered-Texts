# Training objectives and correctness signals

`engine.neural_training` provides a bounded NumPy objective for supervised classification, paired-view consistency, a curriculum based on training errors, and an optional correctness-gated speed signal. This is a repository-specific composition. It does not run a training loop, alter model files, choose evaluation samples, or promote a model by itself.

The objectives draw on established ideas: label smoothing appears in [Szegedy and colleagues' Inception paper](https://arxiv.org/abs/1512.00567), and prediction consistency across augmentation conditions is developed in [Laine and Aila's Temporal Ensembling paper](https://arxiv.org/abs/1610.02242). This implementation uses an explicit pairwise probability-distance term, rather than claiming to reproduce either complete training system.

## Objective and exact gradient

```python
from engine.neural_training import classification_objective

loss, gradient_logits, metrics = classification_objective(
    logits,
    labels,
    smoothing=.03,
    paired_rows=((0, 2), (1, 3)),
    consistency_weight=.1,
    sample_weights=weights,
)
```

For C classes, the target distribution is `(1 - smoothing) * one_hot(label) + smoothing / C`. The supervised loss is the weighted mean cross-entropy, divided by the supplied weight sum. Its logit gradient is `(softmax(logits) - target) * normalized_weight`. Log probabilities are computed directly with shifted log-sum-exp so very unlikely classes do not acquire a clipped objective with a mismatched gradient.

Each unique unordered pair contributes half the squared distance between its softmax probability vectors. The consistency loss is the mean across pairs and enters the total objective multiplied by `consistency_weight`. Both views receive gradients. Shared rows accumulate contributions, and the softmax Jacobian-vector product gives the exact derivative without allocating a separate Jacobian per row. Pair order and repeated copies of a pair do not create extra weight. Views must have distinct row indices and the same training label. A zero coefficient disables its gradient; the raw consistency metric is still available.

Labels are integer class indices. The input matrix must be numeric, finite, nonempty, and bounded to 20,000 rows, 128 classes, and 1,000,000 cells. There must be at least two classes. Pair input is a finite sequence of at most 10,000 pairs. These separate bounds permit two views of 256 examples across 23 training classes. Smoothing is in `[0, 1)`, consistency weight in `[0, 1000]`, and sample weights in `[0, 1000000]` with at least one positive entry. A zero supervised weight does not suppress consistency gradients from a supplied pair. Float64 dynamic ranges that cannot be represented fail explicitly. Metrics report the two loss terms separately, unique pair count, unweighted accuracy, weighted accuracy, and weighting parameters.

The classifier's label is a known cipher family from controlled training data. Formatting changes or deliberately noisy paired views are augmentation choices for those labeled training examples. They are not repairs of unknown ciphertext and must not become evidence that a proposed plaintext is correct. A formatting-only view that yields identical features can have exactly zero consistency loss; record the actual augmentation and its limitations. Family ranking at inference does not return a verified plaintext.

## Curriculum from training feedback

```python
from engine.neural_training import curriculum_weights

weights = curriculum_weights(
    training_labels,
    training_predictions,
    epoch=epoch,
    total_epochs=epochs,
    easy_mask=known_easy_training_examples,
)
```

Predictions can be class-index vectors or finite row-wise score matrices. Epoch zero gives unit weights. By the final epoch, incorrect training examples have raw weight 3, ordinary correct examples 1, and explicitly easy correct examples .75. Normalization gives unit mean with weights bounded to `[.25, 4]`. An incorrect example is emphasized even if the caller marked it easy. Total epochs are 1 through 1,000; the current epoch is 0 through the total. Masks are Boolean vectors matching the training rows.

This function has no heldout metrics or plaintext reference input. Supply only training predictions and training annotations. Validation, calibration, benchmark controls, and heldout plaintext must stay outside curriculum selection. Validation can select checkpoints separately; final promotion must continue to compare the same fixed benchmark cases and report unscored or missing families honestly. Passing gradient tests establishes objective correctness, not improved benchmark accuracy. Execute and report the actual training and independent evaluation before claiming a gain.

## Warm starts and the learning rate

`engine.neural_router_v2.train_router(warm_start=True, learning_rate=.0003, hidden=96, ensemble_size=3)`
starts a bounded local pass from a compatible saved residual ensemble. The
maximum cosine-schedule rate defaults to `.01`, accepts finite positive values
through `.1`, and decreases toward one tenth of that maximum. The CLI exposes
the same settings as `train-router --warm-start --learning-rate 0.0003`.
Specify the incumbent's hidden width and ensemble size explicitly.

Warm start preserves the exact output family list and order, hidden width,
ensemble size and training-only language-table provenance. A compatible old
feature vector must be the exact prefix of the new vector. Over that old
feature prefix, the first layer converts normalization with `Wnew = scaleNew / scaleOld * Wold` and
`bnew = bold + (meanNew - meanOld) / scaleOld @ Wold`; added inputs receive
zero weights. Subsequent layers remain unchanged. The conversion preserves
initial logits mathematically, subject to floating-point precision, and rejects
nonfinite or unrepresentable conversions. Optimizer moments restart.

The incumbent participates as validation checkpoint 0. Selection maximizes
correct Austen validation labels, then minimizes negative log likelihood, and
retains the earliest exact tie. Doyle development comparisons and Wells audit
data do not enter the gradients, curriculum or checkpoint selection. Final
promotion still requires no added errors against the actual incumbent on both
reused Doyle comparisons, plus a serialized artifact within 4 MiB. Warm starts
and smaller rates do not guarantee that gate will pass. See
[actual trial outcomes and artifact-specific audit scope](neural-upgrades.md).

Focused tests check an independent matrix calculation of preserved logits,
zero added rows, checkpoint 0 ties and degradation, early incompatibility
errors, and an analytical one-step AdamW control for two supplied rates.
Their gradients are mocked in the step control, so those tests do not constitute
an accuracy experiment.

## Optional frozen teacher

A compatible warm start can add a temperature-scaled KL term against the frozen
incumbent ensemble. The teacher sees generated Austen training rows only; the
known synthetic labels retain their full supervised weight. The default
strength is zero and preserves the prior training path. Positive strength
requires a compatible warm start and does not relax the promotion gates.

```sh
python3 -m engine train-router --warm-start --hidden 96 --ensemble-size 3 --learning-rate .0003 --distillation-strength .1 --distillation-temperature 2 --dry-run
```

The [dated implementation and trial record](bob-distillation-2026-10-03.md)
documents the exact objective, gradient controls, provenance, and actual outcome.
An optional training method is not an accuracy improvement until its measured
candidate passes the fixed incumbent comparisons.

## Simulated performance signal

```python
from engine.neural_training import correctness_speed_reward

reward = correctness_speed_reward(
    independently_correct,
    elapsed_seconds,
    reference_seconds=1.,
    speed_weight=.1,
)
```

Every incorrect result receives `-1`, regardless of speed. An independently correct result receives `1 + speed_weight * reference_seconds / (reference_seconds + elapsed_seconds)`, bounded above by 2. A fast correct result therefore scores above a slow correct result, while a fast wrong result gains no speed bonus. Elapsed time is 0 through 3,600 seconds, the positive reference time is at most 3,600 seconds, and speed weight is 0 through 1. The reference is a declared comparison setting, not a universal performance standard across hardware.

If shown as simulated happiness, this scalar means measured correctness and speed feedback. It represents no subjective emotion or consciousness. Correctness must come from an independent expected answer or verified heldout evidence; a solver's own success label, crib fit, or confidence is insufficient. The reward does not replace benchmark promotion checks, authenticate unknown text, or justify trading correctness for speed.

```sh
.venv/bin/python -m unittest tests.test_neural_training -v
```

Tests compare analytical gradients with central finite differences for weighted supervised and consistency terms, including shared pair rows. They also check shifted-logit invariance, zero consistency for identical views, invalid inputs, curriculum normalization and bounds, and controls where a faster wrong answer remains penalized. This module imports NumPy; standard-library cipher primitives retain their own dependency scope.
