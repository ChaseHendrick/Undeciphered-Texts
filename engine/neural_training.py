"""Validated, bounded classification objectives and performance signals.

This is a repository-specific composition of supervised label smoothing,
paired-view probability consistency, a training-only curriculum, and a
correctness-gated speed signal. It does not train itself, choose heldout
examples, repair ciphertext, or model subjective feelings.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
import numpy as np

MAX_ROWS = 20_000
MAX_CLASSES = 128
MAX_CELLS = 1_000_000
MAX_PAIRS = 10_000


def _number(value, name: str, minimum: float, maximum: float, *, inclusive_minimum: bool = True) -> float:
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, float, np.integer, np.floating)):
        raise TypeError(f"{name} must be a number")
    try:
        value = float(value)
    except (OverflowError, ValueError) as exc:
        raise ValueError(f"{name} must be finite") from exc
    if not math.isfinite(value) or value > maximum or (value < minimum if inclusive_minimum else value <= minimum):
        bracket = "[" if inclusive_minimum else "("
        raise ValueError(f"{name} must be finite and in {bracket}{minimum}, {maximum}]")
    return value


def _integer(value, name: str, minimum: int, maximum: int) -> int:
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)):
        raise TypeError(f"{name} must be an integer")
    if not minimum <= value <= maximum:
        raise ValueError(f"{name} must be in {minimum}..{maximum}")
    return int(value)


def _matrix(value, name: str) -> np.ndarray:
    raw = np.asarray(value)
    if raw.dtype.kind not in "fiu" or raw.ndim != 2:
        raise TypeError(f"{name} must be a numeric matrix")
    if not 1 <= raw.shape[0] <= MAX_ROWS or not 2 <= raw.shape[1] <= MAX_CLASSES or raw.size > MAX_CELLS:
        raise ValueError(f"{name} exceeds row/class/cell bounds or is empty")
    try:
        array = raw.astype(np.float64)
    except (OverflowError, ValueError) as exc:
        raise ValueError(f"{name} must have representable float64 values") from exc
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must be finite")
    return array


def _labels(value, count: int, classes: int) -> np.ndarray:
    raw = np.asarray(value)
    if raw.dtype.kind not in "iu" or raw.shape != (count,):
        raise TypeError("labels must be a one-dimensional integer array matching the rows")
    if np.any(raw < 0) or np.any(raw >= classes):
        raise ValueError("labels must be valid class indices")
    return raw.astype(np.int64)


def _weights(value, count: int) -> np.ndarray:
    if value is None:
        return np.ones(count, dtype=np.float64)
    raw = np.asarray(value)
    if raw.dtype.kind not in "fiu" or raw.shape != (count,):
        raise TypeError("sample_weights must be a numeric vector matching the rows")
    weights = raw.astype(np.float64)
    if not np.all(np.isfinite(weights)) or np.any(weights < 0) or np.any(weights > 1_000_000) or not np.any(weights > 0):
        raise ValueError("weights must be finite in 0..1000000 with at least one positive value")
    return weights


def _pairs(value, labels: np.ndarray) -> tuple[tuple[int, int], ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, (Sequence, np.ndarray)):
        raise TypeError("paired_rows must be a finite sequence of index pairs")
    if len(value) > MAX_PAIRS:
        raise ValueError(f"paired_rows must contain at most {MAX_PAIRS} pairs")
    pairs = []
    seen = set()
    for row in value:
        if isinstance(row, (str, bytes)) or not isinstance(row, (Sequence, np.ndarray)) or len(row) != 2:
            raise ValueError("each paired_rows entry must contain two indices")
        left = _integer(row[0], "pair index", 0, len(labels) - 1)
        right = _integer(row[1], "pair index", 0, len(labels) - 1)
        if left == right or labels[left] != labels[right]:
            raise ValueError("paired views must be distinct rows with the same training label")
        key = tuple(sorted((left, right)))
        if key not in seen:
            seen.add(key)
            pairs.append(key)
    return tuple(pairs)


def classification_objective(
    logits, labels, *, smoothing: float = .03, paired_rows=(),
    consistency_weight: float = 0., sample_weights=None,
) -> tuple[float, np.ndarray, dict]:
    """Weighted smoothed CE plus mean half-squared paired softmax distance.

    Sample weights normalize the supervised term by their sum. Consistency
    treats each unique unordered pair equally and supports shared rows.
    Returned gradients are with respect to logits, before any optimizer.
    """
    smoothing = _number(smoothing, "smoothing", 0., 1.)
    if smoothing == 1.:
        raise ValueError("smoothing must be less than one")
    consistency_weight = _number(consistency_weight, "consistency_weight", 0., 1000.)
    logits = _matrix(logits, "logits")
    rows, classes = logits.shape
    labels = _labels(labels, rows, classes)
    weights = _weights(sample_weights, rows)
    pairs = _pairs(paired_rows, labels)
    try:
        with np.errstate(over="raise", invalid="raise", divide="raise", under="ignore"):
            shifted = logits - logits.max(axis=1, keepdims=True)
            exponentials = np.exp(shifted)
            totals = exponentials.sum(axis=1, keepdims=True)
            probabilities = exponentials / totals
            log_probabilities = shifted - np.log(totals)
    except FloatingPointError as exc:
        raise ValueError("logit dynamic range exceeds representable float64 arithmetic") from exc
    targets = np.full_like(probabilities, smoothing / classes)
    targets[np.arange(rows), labels] += 1. - smoothing
    normalized_weights = weights / weights.sum()
    supervised = -float(np.sum(normalized_weights[:, None] * targets * log_probabilities))
    gradient = (probabilities - targets) * normalized_weights[:, None]
    consistency = 0.
    if pairs:
        left, right = np.asarray(pairs, dtype=np.int64).T
        difference = probabilities[left] - probabilities[right]
        consistency = .5 * float(np.sum(difference * difference) / len(pairs))
        probability_gradient = np.zeros_like(probabilities)
        np.add.at(probability_gradient, left, difference / len(pairs))
        np.add.at(probability_gradient, right, -difference / len(pairs))
        # Softmax Jacobian-vector product, without allocating per-row Jacobians.
        consistency_gradient = probabilities * (
            probability_gradient - np.sum(probability_gradient * probabilities, axis=1, keepdims=True)
        )
        gradient += consistency_weight * consistency_gradient
    loss = supervised + consistency_weight * consistency
    if not math.isfinite(loss) or not np.all(np.isfinite(gradient)):
        raise ValueError("objective exceeds representable float64 arithmetic")
    correct = probabilities.argmax(axis=1) == labels
    metrics = {"loss": loss, "supervised_loss": supervised, "consistency_loss": consistency,
               "weighted_consistency_loss": consistency_weight * consistency, "samples": rows,
               "classes": classes, "smoothing": smoothing, "consistency_weight": consistency_weight,
               "paired_rows": len(pairs), "weight_sum": float(weights.sum()),
               "correct_count": int(correct.sum()), "accuracy": float(correct.mean()),
               "weighted_accuracy": float(np.sum(normalized_weights * correct))}
    return loss, gradient, metrics


def curriculum_weights(labels, predictions, epoch: int, total_epochs: int, easy_mask=None) -> np.ndarray:
    """Use training predictions only, emphasizing errors later in training.

    Epoch zero yields unit weights. At the final epoch errors have raw
    weight 3, ordinary correct examples 1, and explicitly easy correct
    examples .75. Division by the mean gives mean-one weights in [.25, 4].
    """
    total_epochs = _integer(total_epochs, "total_epochs", 1, 1000)
    epoch = _integer(epoch, "epoch", 0, total_epochs)
    raw_labels = np.asarray(labels)
    if raw_labels.ndim != 1 or not 1 <= len(raw_labels) <= MAX_ROWS:
        raise ValueError("curriculum labels must be a nonempty bounded vector")
    labels = _labels(raw_labels, len(raw_labels), MAX_CLASSES)
    raw_predictions = np.asarray(predictions)
    if raw_predictions.ndim == 2:
        scores = _matrix(predictions, "predictions")
        if len(scores) != len(labels) or np.any(labels >= scores.shape[1]):
            raise ValueError("prediction scores must match labels and class indices")
        predicted = scores.argmax(axis=1)
    else:
        predicted = _labels(predictions, len(labels), MAX_CLASSES)
    if easy_mask is None:
        easy = np.zeros(len(labels), dtype=bool)
    else:
        easy = np.asarray(easy_mask)
        if easy.dtype.kind != "b" or easy.shape != labels.shape:
            raise TypeError("easy_mask must be a matching Boolean vector")
    wrong = predicted != labels
    progress = epoch / total_epochs
    raw = 1. + progress * (2. * wrong - .25 * (easy & ~wrong))
    return raw / raw.mean()


def correctness_speed_reward(
    correct: bool, elapsed_seconds: float, *, reference_seconds: float = 1., speed_weight: float = .1,
) -> float:
    """A bounded simulated performance reward, not an emotional state.

    Correctness must come from an independent expected answer. Every wrong
    result gets -1 regardless of speed. Correct results get 1 plus a bounded
    speed bonus; this scalar never substitutes for benchmark promotion.
    """
    if not isinstance(correct, (bool, np.bool_)):
        raise TypeError("correct must be a Boolean verified outcome")
    elapsed = _number(elapsed_seconds, "elapsed_seconds", 0., 3600.)
    reference = _number(reference_seconds, "reference_seconds", 0., 3600., inclusive_minimum=False)
    weight = _number(speed_weight, "speed_weight", 0., 1.)
    return 1. + weight * reference / (reference + elapsed) if correct else -1.
