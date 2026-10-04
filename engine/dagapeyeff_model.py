"""Language-model score of the frequency labeling. Not a reading.

The most common cell is given the most common English letter, and so on.
Ties break on the cell text. The resulting string is scored with the
solver's quadgram model and its neural trigram, then compared with shuffles
of the same letters. English is the yardstick. No letter string is stored.
"""

from __future__ import annotations

import random
from functools import lru_cache

from engine.dagapeyeff_life import _assign
from engine.dagapeyeff_order import _prose
from engine.dagapeyeff_regroup import regrouped_pairs
from engine.dagapeyeff_swarm import challenge_pairs
from engine.language import get_model
from engine.neural import get_neural_model

_DRAWS = 200_000
_SEED = 20261004


def _per_step(total: float, length: int, skip: int) -> float:
    return total / (length - skip)


def _tail(seq: list[int], observed_quad: float, observed_neural: float, seed: int) -> dict:
    model = get_model()
    neural = get_neural_model()
    drawn = random.Random(seed)
    sample = seq[:]
    quad_as_high = 0
    neural_as_high = 0
    best_quad = float("-inf")
    best_neural = float("-inf")
    length = len(seq)
    for _ in range(_DRAWS):
        drawn.shuffle(sample)
        quad = _per_step(model.score(sample), length, 3)
        brain = _per_step(neural.score(sample), length, 2)
        if quad >= observed_quad:
            quad_as_high += 1
        if brain >= observed_neural:
            neural_as_high += 1
        if quad > best_quad:
            best_quad = quad
        if brain > best_neural:
            best_neural = brain
    return {
        "draws": _DRAWS,
        "quad_as_high": quad_as_high,
        "neural_as_high": neural_as_high,
        "best_shuffle_quad": round(best_quad, 4),
        "best_shuffle_neural": round(best_neural, 4),
    }


@lru_cache(maxsize=1)
def model_report() -> dict:
    model = get_model()
    neural = get_neural_model()
    regrouped = [ord(letter) - 65 for letter in _assign(tuple(regrouped_pairs()))]
    printed = [ord(letter) - 65 for letter in _assign(challenge_pairs())]
    english = [ord(letter) - 65 for letter in _prose("english.txt", len(printed))]
    length = len(printed)
    regrouped_quad = _per_step(model.score(regrouped), length, 3)
    printed_quad = _per_step(model.score(printed), length, 3)
    english_quad = _per_step(model.score(english), length, 3)
    regrouped_neural = _per_step(neural.score(regrouped), length, 2)
    printed_neural = _per_step(neural.score(printed), length, 2)
    english_neural = _per_step(neural.score(english), length, 2)
    regrouped_tail = _tail(regrouped, regrouped_quad, regrouped_neural, _SEED)
    printed_tail = _tail(printed, printed_quad, printed_neural, _SEED + 1)
    return {
        "solved": False,
        "claimed_plaintext": None,
        "length": length,
        "english_quad": round(english_quad, 4),
        "english_neural": round(english_neural, 4),
        "printed_quad": round(printed_quad, 4),
        "printed_neural": round(printed_neural, 4),
        "regrouped_quad": round(regrouped_quad, 4),
        "regrouped_neural": round(regrouped_neural, 4),
        "printed_tail": printed_tail,
        "regrouped_tail": regrouped_tail,
        "regrouped_beats_printed_quad": regrouped_quad > printed_quad,
        "either_reaches_english": max(printed_quad, regrouped_quad) >= english_quad,
        "scope": (
            "A frequency labeling is not a key. A shuffle that scores higher is not a reading. "
            "No letter string is stored."
        ),
    }
