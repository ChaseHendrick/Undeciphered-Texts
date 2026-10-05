"""A lifted ranking. The weight file is not replaced.

Two of the three saved networks have to name the same family before that
label replaces the mean. The Enigma versus M-209 vote then speaks only
when those two families are already the mean's top two, the pair score is
past 0.8, and the mean's own gap is at least 0.7. The looser vote, with
no gap, raises the 480 and drops the older 204, so those two cutoffs stay.
Both bars have to hold. No letter string is stored.
"""

from __future__ import annotations

import hashlib
from functools import lru_cache

import numpy as np

from engine.bob_caution import _SHIPPED, _WEIGHTS
from engine.bob_pair import _SURE as _LOOSE_SURE
from engine.bob_pair import _fit, _texts
from engine.dagapeyeff_cache import frozen
from engine.neural_features import feature_tables
from engine.neural_grade import (
    FAMILIES,
    HELD_EN_PATH,
    ROUTER_SEED,
    _english_unigram,
    letters_az,
    load_training_prose,
)
from engine.neural_m209_features import m209_pair_features
from engine.neural_router_v2 import _features, load_router, network_logits, route_probabilities

_SURE = 0.8
_MARGIN = 0.7


@lru_cache(maxsize=1)
def _bundle():
    saved = load_router()
    english = _english_unigram(saved["training_letters"])
    tables = feature_tables(saved["training_letters"], english)
    weights, mean, scale, train_correct = _fit(tables)
    return saved, english, tables, weights, mean, scale, train_correct


def _choose(texts, each, tables, weights, mean_scale, scale, names):
    mean = each.mean(axis=0)
    order = np.argsort(-mean, axis=1)
    base = order[:, 0].copy()
    chosen = base.copy()
    votes = each.argmax(axis=2)
    for index in range(len(texts)):
        values, counts = np.unique(votes[:, index], return_counts=True)
        if int(counts.max()) >= 2:
            chosen[index] = int(values[int(counts.argmax())])
    enigma = names.index("enigma")
    machine = names.index("m209")
    design = np.asarray([m209_pair_features(text, tables) for text in texts], dtype=float)
    design = np.concatenate([(design - mean_scale) / scale, np.ones((len(design), 1))], axis=1)
    probability = 1 / (1 + np.exp(-np.clip(design @ weights, -30, 30)))
    for index in range(len(texts)):
        if set(order[index, :2].tolist()) != {enigma, machine}:
            continue
        margin = float(mean[index, order[index, 0]] - mean[index, order[index, 1]])
        if margin < _MARGIN:
            continue
        vote = None
        if probability[index] > _SURE:
            vote = machine
        elif probability[index] < 1 - _SURE:
            vote = enigma
        if vote is not None:
            chosen[index] = vote
    return base, chosen, order


def _correct(pred, labels, names, named) -> int:
    if named:
        return sum(names[int(index)] == FAMILIES[int(label)] for index, label in zip(pred, labels))
    return int((np.asarray(pred) == np.asarray(labels)).sum())


def _flips(base, chosen, labels, names, named) -> tuple[int, int, int]:
    corrections = mistakes = same_error = 0
    for index in range(len(labels)):
        if int(chosen[index]) == int(base[index]):
            continue
        if named:
            truth = FAMILIES[int(labels[index])]
            before = names[int(base[index])] == truth
            after = names[int(chosen[index])] == truth
        else:
            before = int(base[index]) == int(labels[index])
            after = int(chosen[index]) == int(labels[index])
        if after and not before:
            corrections += 1
        elif before and not after:
            mistakes += 1
        else:
            same_error += 1
    return corrections, mistakes, same_error


def _top3(chosen, order, labels, names, named) -> int:
    hits = 0
    for index, label in enumerate(labels):
        ranking = [int(chosen[index])]
        for slot in order[index]:
            if int(slot) not in ranking:
                ranking.append(int(slot))
            if len(ranking) == 3:
                break
        if named:
            hits += FAMILIES[int(label)] in [names[slot] for slot in ranking]
        else:
            hits += int(label) in ranking
    return hits


def _score(texts, labels, named):
    saved, english, tables, weights, mean, scale, _train = _bundle()
    rows = [_features(text, english, tables, version=saved["feature_version"]) for text in texts]
    each = np.stack([network_logits(rows, model) for model in saved["models"]], axis=0)
    base, chosen, order = _choose(texts, each, tables, weights, mean, scale, saved["families"])
    corrections, mistakes, same_error = _flips(base, chosen, labels, saved["families"], named)
    return {
        "before": _correct(base, labels, saved["families"], named),
        "after": _correct(chosen, labels, saved["families"], named),
        "flips": int((chosen != base).sum()),
        "corrections": corrections,
        "mistakes": mistakes,
        "same_error": same_error,
        "top3": _top3(chosen, order, labels, saved["families"], named),
    }


def lifted_family(text: str) -> str:
    """The family the lifted ranking would name. Not a plaintext.

    Lower case is folded first. The feature table only reads A-Z, so a
    lower-case string used to look empty and the call failed. The mean
    router already folds case. This path now does the same.
    """
    if not isinstance(text, str):
        raise TypeError("ciphertext must be text")
    folded = text.upper()
    saved, english, tables, weights, mean, scale, _train = _bundle()
    rows = [_features(folded, english, tables, version=saved["feature_version"])]
    each = np.stack([network_logits(rows, model) for model in saved["models"]], axis=0)
    _base, chosen, _order = _choose([folded], each, tables, weights, mean, scale, saved["families"])
    return saved["families"][int(chosen[0])]


def route_lifted(text: str) -> dict:
    """The shipped probabilities, with the lifted family placed first.

    Probability values stay the mean network's. The weight file is not read
    as a new model. No plaintext is returned.
    """
    report = route_probabilities(text)
    family = lifted_family(text)
    candidates = list(report["candidates"])
    picked = [row for row in candidates if row["family"] == family]
    rest = [row for row in candidates if row["family"] != family]
    changed = bool(picked) and picked[0] is not candidates[0]
    return {
        **report,
        "candidates": picked + rest if picked else candidates,
        "ordered_by": "lifted-vote" if changed else "probability",
        "lift_applied": changed,
        "scope": (
            "Ranks trained known cipher families only. A family probability does not validate a plaintext. "
            "When the lift applies, the first family is that vote and its probability is still the mean network's."
        ),
    }


@frozen("bob-lift")
def bob_lift_report() -> dict:
    digest = hashlib.sha256(_WEIGHTS.read_bytes()).hexdigest()
    saved, _english, _tables, _weights, _mean, _scale, train_correct = _bundle()
    held = letters_az(load_training_prose(HELD_EN_PATH))
    held_texts, held_labels = _texts(held, ROUTER_SEED + 202, saved["families"], 24, False)
    held_score = _score(held_texts, held_labels, False)
    bench_texts, bench_labels = _texts(held, ROUTER_SEED + 1, list(FAMILIES), 12, True)
    bench_score = _score(bench_texts, bench_labels, True)
    promoted = (
        held_score["after"] >= held_score["before"]
        and bench_score["after"] >= bench_score["before"]
        and (held_score["after"] > held_score["before"] or bench_score["after"] > bench_score["before"])
    )
    return {
        "solved": False,
        "claimed_plaintext": None,
        "weights_sha256": digest,
        "weights_replaced": False,
        "weights_match_shipped": digest == _SHIPPED,
        "loose_sure": _LOOSE_SURE,
        "sure": _SURE,
        "margin": _MARGIN,
        "train_correct": train_correct,
        "train_total": 200,
        "held_before": held_score["before"],
        "held_after": held_score["after"],
        "held_total": len(held_labels),
        "held_flips": held_score["flips"],
        "held_corrections": held_score["corrections"],
        "held_mistakes": held_score["mistakes"],
        "held_top3": held_score["top3"],
        "benchmark_before": bench_score["before"],
        "benchmark_after": bench_score["after"],
        "benchmark_total": len(bench_labels),
        "benchmark_flips": bench_score["flips"],
        "benchmark_corrections": bench_score["corrections"],
        "benchmark_mistakes": bench_score["mistakes"],
        "benchmark_top3": bench_score["top3"],
        "promoted": promoted,
        "scope": "A lifted ranking is not a reading. The weight file was not replaced.",
    }
