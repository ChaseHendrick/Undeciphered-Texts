"""A smaller student of the three saved networks. The weight file is not replaced.

The linear student from the previous drill had sixty free numbers and lost
both bars. This one keeps two small fits, both on the same training draw.
A 20-number bias is added to the mean logits. Half the loss is the label
and half is the frozen mean at temperature 2, the same Hinton mix as before.
A second bias imitates the lifted ranking on that training draw only.
A third fit is three mixture weights on the three networks.

A ranking is allowed only when it is at least as high as the lifted ranking
on both development bars and higher on one of them. Otherwise it is refused.
No letter string is stored.
"""

from __future__ import annotations

import hashlib

import numpy as np

from engine.bob_caution import _SHIPPED, _WEIGHTS
from engine.bob_distill import _each, _score_row
from engine.bob_lift import _bundle, _choose
from engine.bob_pair import _texts
from engine.dagapeyeff_cache import frozen
from engine.neural_grade import FAMILIES, HELD_EN_PATH, ROUTER_SEED, letters_az, load_training_prose

_TRAIN_SEED = 20261005
_PER_CLASS = 8
_TEMPERATURE = 2.0
_STRENGTH = 0.5
_RIDGE = 0.02
_STEPS = 400
_RATE = 0.08


def _softmax(logits: np.ndarray) -> np.ndarray:
    shifted = logits - logits.max(axis=1, keepdims=True)
    exponentials = np.exp(np.clip(shifted, -40.0, 40.0))
    return exponentials / exponentials.sum(axis=1, keepdims=True)


def fit_bias(
    logits: np.ndarray,
    labels: np.ndarray,
    *,
    steps: int = _STEPS,
    rate: float = _RATE,
    ridge: float = _RIDGE,
    strength: float = _STRENGTH,
    temperature: float = _TEMPERATURE,
) -> np.ndarray:
    """Add one bias per family. Fit on the given rows only."""
    logits = np.asarray(logits, dtype=np.float64)
    labels = np.asarray(labels, dtype=np.int64)
    if logits.ndim != 2 or len(labels) != len(logits):
        raise ValueError("bias fit needs one label per row")
    if steps < 1 or rate <= 0 or ridge < 0 or temperature <= 0 or not 0.0 <= strength <= 1.0:
        raise ValueError("bias fit settings are out of range")
    bias = np.zeros(logits.shape[1], dtype=np.float64)
    rows = np.arange(len(labels))
    teacher = _softmax(logits / temperature) if strength > 0.0 else None
    for _ in range(steps):
        scores = logits + bias
        hard = _softmax(scores)
        onehot = np.zeros_like(hard)
        onehot[rows, labels] = 1.0
        gradient = (1.0 - strength) * (hard - onehot).mean(axis=0)
        if teacher is not None:
            soft = _softmax(scores / temperature)
            gradient = gradient + strength * temperature * (soft - teacher).mean(axis=0)
        gradient = gradient + ridge * bias
        if not np.all(np.isfinite(gradient)):
            raise ValueError("bias gradient is not finite")
        bias -= rate * gradient
    if not np.all(np.isfinite(bias)):
        raise ValueError("bias is not finite")
    return bias


def fit_mix(each: np.ndarray, labels: np.ndarray, *, steps: int = _STEPS, rate: float = 0.25, ridge: float = 0.01) -> np.ndarray:
    """Three weights that mix the networks. They sum to one."""
    each = np.asarray(each, dtype=np.float64)
    labels = np.asarray(labels, dtype=np.int64)
    if each.ndim != 3 or each.shape[1] != len(labels):
        raise ValueError("mix fit needs one label per text")
    if steps < 1 or rate <= 0 or ridge < 0:
        raise ValueError("mix fit settings are out of range")
    raw = np.zeros(each.shape[0], dtype=np.float64)
    rows = np.arange(each.shape[1])
    for _ in range(steps):
        weights = _softmax(raw[None, :])[0]
        mixed = np.einsum("k,knc->nc", weights, each)
        probabilities = _softmax(mixed)
        onehot = np.zeros_like(probabilities)
        onehot[rows, labels] = 1.0
        d_mixed = (probabilities - onehot) / len(labels)
        d_weights = np.einsum("nc,knc->k", d_mixed, each)
        d_raw = d_weights * weights - weights * float(np.dot(weights, d_weights))
        d_raw = d_raw + ridge * raw
        if not np.all(np.isfinite(d_raw)):
            raise ValueError("mix gradient is not finite")
        raw -= rate * d_raw
    weights = _softmax(raw[None, :])[0]
    if not np.all(np.isfinite(weights)) or abs(float(weights.sum()) - 1.0) > 1e-6:
        raise ValueError("mix weights are not a probability")
    return weights


def _beats(lift_held: int, lift_bench: int, cand_held: int, cand_bench: int) -> bool:
    return cand_held >= lift_held and cand_bench >= lift_bench and (cand_held > lift_held or cand_bench > lift_bench)


@frozen("bob-slim")
def bob_slim_report() -> dict:
    digest = hashlib.sha256(_WEIGHTS.read_bytes()).hexdigest()
    saved, english, tables, pair_weights, pair_mean, pair_scale, _train_pair = _bundle()
    names = saved["families"]
    training = letters_az(load_training_prose())
    train_texts, train_labels = _texts(training, _TRAIN_SEED, names, _PER_CLASS, False)
    train_each = _each(train_texts, saved, english, tables)
    mean_logits = train_each.mean(axis=0)
    label_array = np.asarray(train_labels)
    bias = fit_bias(mean_logits, label_array)
    _base, lifted, _order = _choose(train_texts, train_each, tables, pair_weights, pair_mean, pair_scale, names)
    lift_bias = fit_bias(mean_logits, np.asarray(lifted), strength=0.0)
    mix = fit_mix(train_each, label_array)
    train_bias = int(((mean_logits + bias).argmax(axis=1) == label_array).sum())
    train_lift = int(((mean_logits + lift_bias).argmax(axis=1) == label_array).sum())
    train_mix = int((np.einsum("k,knc->nc", mix, train_each).argmax(axis=1) == label_array).sum())
    held_corpus = letters_az(load_training_prose(HELD_EN_PATH))
    packs = {}
    for key, corpus_seed, count, rotate, named in (
        ("held", ROUTER_SEED + 202, 24, False, False),
        ("benchmark", ROUTER_SEED + 1, 12, True, True),
    ):
        label_names = names if not named else list(FAMILIES)
        texts, labels = _texts(held_corpus, corpus_seed, label_names, count, rotate)
        each = _each(texts, saved, english, tables)
        _mean_choice, lifted_choice, _order = _choose(
            texts, each, tables, pair_weights, pair_mean, pair_scale, names
        )
        logits = each.mean(axis=0)
        bias_scores = logits + bias
        lift_scores = logits + lift_bias
        mix_scores = np.einsum("k,knc->nc", mix, each)
        packs[key] = {
            "mean": _score_row(logits.argmax(axis=1), logits, labels, names, named),
            "lift": _score_row(lifted_choice, logits, labels, names, named),
            "bias": _score_row(bias_scores.argmax(axis=1), bias_scores, labels, names, named),
            "lift_bias": _score_row(lift_scores.argmax(axis=1), lift_scores, labels, names, named),
            "mix": _score_row(mix_scores.argmax(axis=1), mix_scores, labels, names, named),
            "total": len(labels),
        }
    from engine.bob_lift import bob_lift_report

    lift_report = bob_lift_report()
    if packs["held"]["lift"]["correct"] != lift_report["held_after"]:
        raise RuntimeError("held lift does not match the frozen lifted ranking")
    if packs["benchmark"]["lift"]["correct"] != lift_report["benchmark_after"]:
        raise RuntimeError("benchmark lift does not match the frozen lifted ranking")
    held_lift = packs["held"]["lift"]["correct"]
    bench_lift = packs["benchmark"]["lift"]["correct"]
    bias_promoted = _beats(held_lift, bench_lift, packs["held"]["bias"]["correct"], packs["benchmark"]["bias"]["correct"])
    lift_bias_promoted = _beats(
        held_lift, bench_lift, packs["held"]["lift_bias"]["correct"], packs["benchmark"]["lift_bias"]["correct"]
    )
    mix_promoted = _beats(held_lift, bench_lift, packs["held"]["mix"]["correct"], packs["benchmark"]["mix"]["correct"])
    return {
        "solved": False,
        "claimed_plaintext": None,
        "weights_sha256": digest,
        "weights_replaced": False,
        "weights_match_shipped": digest == _SHIPPED,
        "train_per_class": _PER_CLASS,
        "train_total": len(train_labels),
        "train_bias_correct": train_bias,
        "train_lift_bias_correct": train_lift,
        "train_mix_correct": train_mix,
        "bias_l2": round(float(np.linalg.norm(bias)), 6),
        "mix_weights": [round(float(weight), 4) for weight in mix],
        "held_mean": packs["held"]["mean"]["correct"],
        "held_lift": held_lift,
        "held_bias": packs["held"]["bias"]["correct"],
        "held_bias_top3": packs["held"]["bias"]["top3"],
        "held_lift_bias": packs["held"]["lift_bias"]["correct"],
        "held_mix": packs["held"]["mix"]["correct"],
        "held_mix_top3": packs["held"]["mix"]["top3"],
        "held_total": packs["held"]["total"],
        "benchmark_mean": packs["benchmark"]["mean"]["correct"],
        "benchmark_lift": bench_lift,
        "benchmark_bias": packs["benchmark"]["bias"]["correct"],
        "benchmark_bias_top3": packs["benchmark"]["bias"]["top3"],
        "benchmark_lift_bias": packs["benchmark"]["lift_bias"]["correct"],
        "benchmark_mix": packs["benchmark"]["mix"]["correct"],
        "benchmark_mix_top3": packs["benchmark"]["mix"]["top3"],
        "benchmark_total": packs["benchmark"]["total"],
        "bias_promoted": bias_promoted,
        "lift_bias_promoted": lift_bias_promoted,
        "mix_promoted": mix_promoted,
        "promoted": bool(bias_promoted or lift_bias_promoted or mix_promoted),
        "scope": (
            "A smaller student is not a reading and is not a new weight file. "
            "It is refused unless it beats the lifted ranking on a development bar without losing the other."
        ),
    }
