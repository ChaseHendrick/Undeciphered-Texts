"""A side vote between Enigma and the M-209. The weights are not replaced.

Bob confuses those two families more than any other pair. Six M-209 pair
scores, fit on fresh training keys only, vote only when those two families
are already his top two. The vote has to hold the 480 and the older 204.
No letter string is stored.
"""

from __future__ import annotations

import hashlib
import random

import numpy as np

from engine.bob_caution import _SHIPPED, _WEIGHTS
from engine.dagapeyeff_cache import frozen
from engine.neural_features import feature_tables
from engine.neural_grade import (
    FAMILIES,
    HELD_EN_PATH,
    ROUTER_SEED,
    _english_unigram,
    encrypt_family,
    letters_az,
    load_training_prose,
)
from engine.neural_m209_features import m209_pair_features
from engine.neural_router_v2 import _encrypt, _features, load_router, network_logits

_TRAIN_SEED = 7
_PER_CLASS = 100
_STEPS = 600
_RIDGE = 0.2
_RATE = 0.2
_SURE = 0.7


def _fit(tables) -> tuple[np.ndarray, np.ndarray, np.ndarray, int]:
    training = letters_az(load_training_prose())
    drawn = random.Random(_TRAIN_SEED)
    rows = []
    labels = []
    for family, label in (("enigma", 0.0), ("m209", 1.0)):
        for _ in range(_PER_CLASS):
            length = drawn.choice((120, 180, 240))
            start = drawn.randrange(len(training) - length + 1)
            text = _encrypt(family, training[start:start + length], drawn)
            rows.append(m209_pair_features(text, tables))
            labels.append(label)
    samples = np.asarray(rows, dtype=float)
    target = np.asarray(labels, dtype=float)
    mean = samples.mean(axis=0)
    scale = samples.std(axis=0) + 1e-6
    design = np.concatenate([(samples - mean) / scale, np.ones((len(samples), 1))], axis=1)
    weights = np.zeros(design.shape[1])
    ridge = np.concatenate([np.full(design.shape[1] - 1, _RIDGE), [0.0]])
    for _ in range(_STEPS):
        probability = 1 / (1 + np.exp(-np.clip(design @ weights, -30, 30)))
        gradient = design.T @ (probability - target) / len(target) + ridge * weights
        weights -= _RATE * gradient
    correct = int(((1 / (1 + np.exp(-np.clip(design @ weights, -30, 30))) > 0.5) == target).sum())
    return weights, mean, scale, correct


def _texts(corpus: str, seed: int, names: list[str], count: int, rotate: bool) -> tuple[list[str], list[int]]:
    drawn = random.Random(seed)
    texts = []
    labels = []
    if rotate:
        windows = [corpus[index:index + 180] for index in range(0, len(corpus) - 179, 180)]
        for label, family in enumerate(names):
            for sample in range(count):
                window = windows[(sample * 5 + label * 2) % len(windows)]
                offset = (sample * 17) % 40
                texts.append(encrypt_family(family, window[offset:] + window[:offset], drawn))
                labels.append(label)
        return texts, labels
    for label, family in enumerate(names):
        for _ in range(count):
            length = drawn.choice((120, 180, 240))
            start = drawn.randrange(len(corpus) - length + 1)
            texts.append(_encrypt(family, corpus[start:start + length], drawn))
            labels.append(label)
    return texts, labels


def _score(texts, labels, names, saved, english, tables, weights, mean, scale, named) -> tuple[int, int, int]:
    rows = [_features(text, english, tables, version=saved["feature_version"]) for text in texts]
    logits = np.mean([network_logits(rows, model) for model in saved["models"]], axis=0)
    predicted = logits.argmax(axis=1)
    enigma = names.index("enigma")
    machine = names.index("m209")
    design = np.asarray([m209_pair_features(text, tables) for text in texts], dtype=float)
    design = np.concatenate([(design - mean) / scale, np.ones((len(design), 1))], axis=1)
    probability = 1 / (1 + np.exp(-np.clip(design @ weights, -30, 30)))
    chosen = predicted.copy()
    for index in range(len(texts)):
        order = np.argsort(-logits[index])
        if set(order[:2].tolist()) != {enigma, machine}:
            continue
        if probability[index] > _SURE:
            chosen[index] = machine
        elif probability[index] < 1 - _SURE:
            chosen[index] = enigma
    if named:
        before = sum(names[int(index)] == FAMILIES[label] for index, label in zip(predicted, labels))
        after = sum(names[int(index)] == FAMILIES[label] for index, label in zip(chosen, labels))
    else:
        labels = np.asarray(labels)
        before = int((predicted == labels).sum())
        after = int((chosen == labels).sum())
    return before, after, int((chosen != predicted).sum())


@frozen("bob-pair")
def bob_pair_report() -> dict:
    digest = hashlib.sha256(_WEIGHTS.read_bytes()).hexdigest()
    saved = load_router()
    english = _english_unigram(saved["training_letters"])
    tables = feature_tables(saved["training_letters"], english)
    weights, mean, scale, train_correct = _fit(tables)
    held = letters_az(load_training_prose(HELD_EN_PATH))
    held_texts, held_labels = _texts(held, ROUTER_SEED + 202, saved["families"], 24, False)
    held_before, held_after, held_flips = _score(
        held_texts, held_labels, saved["families"], saved, english, tables, weights, mean, scale, False
    )
    bench_texts, bench_labels = _texts(held, ROUTER_SEED + 1, list(FAMILIES), 12, True)
    bench_before, bench_after, bench_flips = _score(
        bench_texts, bench_labels, saved["families"], saved, english, tables, weights, mean, scale, True
    )
    promoted = held_after >= held_before and bench_after >= bench_before and (
        held_after > held_before or bench_after > bench_before
    )
    return {
        "solved": False,
        "claimed_plaintext": None,
        "weights_sha256": digest,
        "weights_replaced": False,
        "weights_match_shipped": digest == _SHIPPED,
        "train_correct": train_correct,
        "train_total": _PER_CLASS * 2,
        "held_before": held_before,
        "held_after": held_after,
        "held_total": len(held_labels),
        "held_flips": held_flips,
        "benchmark_before": bench_before,
        "benchmark_after": bench_after,
        "benchmark_total": len(bench_labels),
        "benchmark_flips": bench_flips,
        "promoted": promoted,
        "scope": "A side vote is not a reading. The weights were not replaced.",
    }
