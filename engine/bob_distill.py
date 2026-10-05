"""A student of the three saved networks. The weight file is not replaced.

The student reads the three logit vectors. It does not read ciphertext
features and it does not see the development texts while it is fit. Hard
labels and a frozen mean teacher share the loss. The teacher term is the
temperature-squared KL from Hinton, Vinyals and Dean. A second mix puts the
three networks through a Sinkhorn matrix, the same doubly stochastic
projection DeepSeek uses to stop a residual mix from amplifying. Bob is two
layers, so the mix sits on the outputs, not inside the saved weights.

A ranking is allowed only when it is at least as high as the lifted ranking
on both development bars and higher on one of them. Otherwise it is refused.
No letter string is stored.
"""

from __future__ import annotations

import hashlib

import numpy as np

from engine.bob_caution import _SHIPPED, _WEIGHTS
from engine.bob_lift import _bundle, _choose, _correct, _top3
from engine.bob_pair import _texts
from engine.dagapeyeff_cache import frozen
from engine.neural_grade import FAMILIES, HELD_EN_PATH, ROUTER_SEED, letters_az, load_training_prose
from engine.neural_manifold import sinkhorn
from engine.neural_router_v2 import _features, network_logits

_TRAIN_SEED = 20261005
_PER_CLASS = 8
_TEMPERATURE = 2.0
_STRENGTH = 0.5
_RIDGE = 0.05
_STUDENT_STEPS = 300
_STUDENT_RATE = 0.15
_MIX_STEPS = 80
_SINKHORN_STEPS = 12


def _softmax(logits: np.ndarray) -> np.ndarray:
    shifted = logits - logits.max(axis=1, keepdims=True)
    exponentials = np.exp(np.clip(shifted, -40.0, 40.0))
    return exponentials / exponentials.sum(axis=1, keepdims=True)


def _teacher(mean_logits: np.ndarray, temperature: float) -> np.ndarray:
    if temperature <= 0:
        raise ValueError("temperature must be positive")
    return _softmax(np.asarray(mean_logits, dtype=np.float64) / temperature)


def student_loss(design: np.ndarray, weights: np.ndarray, labels: np.ndarray, teacher: np.ndarray, *,
                 strength: float = _STRENGTH, temperature: float = _TEMPERATURE, ridge: float = _RIDGE) -> float:
    """Hard-label cross entropy plus strength * T^2 * KL(teacher || student)."""
    if not 0 <= strength <= 1:
        raise ValueError("strength must lie between 0 and 1")
    probabilities = _softmax(design @ weights)
    soft = _softmax((design @ weights) / temperature)
    rows = np.arange(len(labels))
    hard = -np.log(np.clip(probabilities[rows, labels], 1e-12, 1.0)).mean()
    log_teacher = np.log(np.clip(teacher, 1e-12, 1.0))
    log_soft = np.log(np.clip(soft, 1e-12, 1.0))
    kl = float(np.sum(teacher * (log_teacher - log_soft)) / len(labels))
    penalty = ridge * float(np.sum(weights[:-1] ** 2))
    return float((1.0 - strength) * hard + strength * temperature ** 2 * kl + penalty)


def fit_student(each: np.ndarray, labels: np.ndarray, *, strength: float = _STRENGTH,
                temperature: float = _TEMPERATURE, steps: int = _STUDENT_STEPS,
                rate: float = _STUDENT_RATE, ridge: float = _RIDGE) -> np.ndarray:
    """Linear map on concatenated logits. `each` is (networks, rows, classes)."""
    networks, rows, classes = each.shape
    design = np.concatenate([each[index] for index in range(networks)] + [np.ones((rows, 1))], axis=1)
    teacher = _teacher(each.mean(axis=0), temperature)
    weights = np.zeros((design.shape[1], classes))
    targets = np.zeros((rows, classes))
    targets[np.arange(rows), labels] = 1.0
    for _ in range(steps):
        logits = design @ weights
        hard = _softmax(logits)
        soft = _softmax(logits / temperature)
        residual = (1.0 - strength) * (hard - targets) + strength * temperature * (soft - teacher)
        gradient = design.T @ residual / rows
        gradient[:-1] += ridge * weights[:-1]
        weights -= rate * gradient
    if not np.all(np.isfinite(weights)):
        raise ValueError("student weights are not finite")
    return weights


def apply_student(each: np.ndarray, weights: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    networks, rows, _classes = each.shape
    design = np.concatenate([each[index] for index in range(networks)] + [np.ones((rows, 1))], axis=1)
    scores = design @ weights
    return scores.argmax(axis=1), scores


def fit_sinkhorn_mix(each: np.ndarray, labels: np.ndarray, *, steps: int = _MIX_STEPS) -> np.ndarray:
    """Doubly stochastic mix of the networks. Identity is the start, via zeros."""
    raw = np.zeros((each.shape[0], each.shape[0]))
    rows = np.arange(len(labels))

    def nll(candidate: np.ndarray) -> float:
        mix = sinkhorn(candidate, steps=_SINKHORN_STEPS)
        mixed = np.einsum("ij,jnc->inc", mix, each).mean(axis=0)
        probabilities = _softmax(mixed)
        return float(-np.log(np.clip(probabilities[rows, labels], 1e-12, 1.0)).mean())

    eps = 1e-3
    for _ in range(steps):
        base = nll(raw)
        gradient = np.empty_like(raw)
        for left in range(raw.shape[0]):
            for right in range(raw.shape[1]):
                raw[left, right] += eps
                gradient[left, right] = (nll(raw) - base) / eps
                raw[left, right] -= eps
        raw -= 0.35 * gradient
    mix = sinkhorn(raw, steps=_SINKHORN_STEPS)
    if not np.all(np.isfinite(mix)):
        raise ValueError("sinkhorn mix is not finite")
    return mix


def apply_mix(each: np.ndarray, mix: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    mixed = np.einsum("ij,jnc->inc", mix, each).mean(axis=0)
    return mixed.argmax(axis=1), mixed


def _each(texts, saved, english, tables) -> np.ndarray:
    rows = [_features(text, english, tables, version=saved["feature_version"]) for text in texts]
    return np.stack([network_logits(rows, model) for model in saved["models"]], axis=0)


def _score_row(pred, scores, labels, names, named) -> dict:
    return {
        "correct": _correct(pred, labels, names, named),
        "top3": _top3(pred, np.argsort(-scores, axis=1), labels, names, named),
    }


@frozen("bob-distill")
def bob_distill_report() -> dict:
    digest = hashlib.sha256(_WEIGHTS.read_bytes()).hexdigest()
    saved, english, tables, pair_weights, pair_mean, pair_scale, _train_pair = _bundle()
    names = saved["families"]
    training = letters_az(load_training_prose())
    train_texts, train_labels = _texts(training, _TRAIN_SEED, names, _PER_CLASS, False)
    train_each = _each(train_texts, saved, english, tables)
    student = fit_student(train_each, np.asarray(train_labels))
    mix = fit_sinkhorn_mix(train_each, np.asarray(train_labels))
    train_pred, _train_scores = apply_student(train_each, student)
    train_student = int((train_pred == np.asarray(train_labels)).sum())
    train_loss = student_loss(
        np.concatenate([train_each[index] for index in range(train_each.shape[0])] + [np.ones((len(train_labels), 1))], axis=1),
        student,
        np.asarray(train_labels),
        _teacher(train_each.mean(axis=0), _TEMPERATURE),
    )
    held_corpus = letters_az(load_training_prose(HELD_EN_PATH))
    packs = {}
    for key, corpus_seed, count, rotate, named in (
        ("held", ROUTER_SEED + 202, 24, False, False),
        ("benchmark", ROUTER_SEED + 1, 12, True, True),
    ):
        label_names = names if not named else list(FAMILIES)
        texts, labels = _texts(held_corpus, corpus_seed, label_names, count, rotate)
        each = _each(texts, saved, english, tables)
        _base, lifted, _order = _choose(texts, each, tables, pair_weights, pair_mean, pair_scale, names)
        mean_logits = each.mean(axis=0)
        student_pred, student_scores = apply_student(each, student)
        mix_pred, mix_scores = apply_mix(each, mix)
        packs[key] = {
            "labels": labels,
            "named": named,
            "mean": _score_row(mean_logits.argmax(axis=1), mean_logits, labels, names, named),
            "lift": _score_row(lifted, mean_logits, labels, names, named),
            "student": _score_row(student_pred, student_scores, labels, names, named),
            "sinkhorn": _score_row(mix_pred, mix_scores, labels, names, named),
            "total": len(labels),
        }
    from engine.bob_lift import bob_lift_report

    lift_report = bob_lift_report()
    if packs["held"]["lift"]["correct"] != lift_report["held_after"]:
        raise RuntimeError("held lift does not match the frozen lifted ranking")
    if packs["benchmark"]["lift"]["correct"] != lift_report["benchmark_after"]:
        raise RuntimeError("benchmark lift does not match the frozen lifted ranking")
    student_promoted = (
        packs["held"]["student"]["correct"] >= packs["held"]["lift"]["correct"]
        and packs["benchmark"]["student"]["correct"] >= packs["benchmark"]["lift"]["correct"]
        and (
            packs["held"]["student"]["correct"] > packs["held"]["lift"]["correct"]
            or packs["benchmark"]["student"]["correct"] > packs["benchmark"]["lift"]["correct"]
        )
    )
    sinkhorn_promoted = (
        packs["held"]["sinkhorn"]["correct"] >= packs["held"]["lift"]["correct"]
        and packs["benchmark"]["sinkhorn"]["correct"] >= packs["benchmark"]["lift"]["correct"]
        and (
            packs["held"]["sinkhorn"]["correct"] > packs["held"]["lift"]["correct"]
            or packs["benchmark"]["sinkhorn"]["correct"] > packs["benchmark"]["lift"]["correct"]
        )
    )
    return {
        "solved": False,
        "claimed_plaintext": None,
        "weights_sha256": digest,
        "weights_replaced": False,
        "weights_match_shipped": digest == _SHIPPED,
        "train_per_class": _PER_CLASS,
        "train_total": len(train_labels),
        "train_student_correct": train_student,
        "train_loss": round(train_loss, 6),
        "temperature": _TEMPERATURE,
        "strength": _STRENGTH,
        "held_mean": packs["held"]["mean"]["correct"],
        "held_lift": packs["held"]["lift"]["correct"],
        "held_student": packs["held"]["student"]["correct"],
        "held_student_top3": packs["held"]["student"]["top3"],
        "held_sinkhorn": packs["held"]["sinkhorn"]["correct"],
        "held_total": packs["held"]["total"],
        "benchmark_mean": packs["benchmark"]["mean"]["correct"],
        "benchmark_lift": packs["benchmark"]["lift"]["correct"],
        "benchmark_student": packs["benchmark"]["student"]["correct"],
        "benchmark_student_top3": packs["benchmark"]["student"]["top3"],
        "benchmark_sinkhorn": packs["benchmark"]["sinkhorn"]["correct"],
        "benchmark_total": packs["benchmark"]["total"],
        "student_promoted": student_promoted,
        "sinkhorn_promoted": sinkhorn_promoted,
        "promoted": bool(student_promoted or sinkhorn_promoted),
        "scope": (
            "A student of the saved networks is not a reading and is not a new weight file. "
            "It is refused unless it beats the lifted ranking on a development bar without losing the other."
        ),
    }
