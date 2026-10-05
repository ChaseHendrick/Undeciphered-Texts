"""Repeated pairs of cells, in the challenge and in the solved exercise. Not a reading.

A digraph is two cells in a row. One count is how many different digraphs
occur more than once. The other is the single most common digraph. Shuffles
of the same cells get both counts. No letter string is stored.
"""

from __future__ import annotations

import random
from collections import Counter

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_swarm import CONTROL, challenge_pairs

_SEED = 20261004
_DRAWS = 10000


def _control_pairs() -> list[str]:
    letters = "".join(char for char in CONTROL if char.isalpha())
    even = len(letters) - (len(letters) % 2)
    return [letters[index:index + 2] for index in range(0, even, 2)]


def _counts(seq: list[str]) -> tuple[int, int]:
    grams = Counter(zip(seq, seq[1:]))
    peak = max(grams.values())
    repeated = sum(value > 1 for value in grams.values())
    return peak, repeated


def _null(seq: list[str], peak: int, repeated: int) -> tuple[int, int, int]:
    drawn = random.Random(_SEED)
    peak_as_high = 0
    repeated_as_high = 0
    either = 0
    for _ in range(_DRAWS):
        shuffled = seq[:]
        drawn.shuffle(shuffled)
        trial_peak, trial_repeated = _counts(shuffled)
        peak_hit = trial_peak >= peak
        repeated_hit = trial_repeated >= repeated
        peak_as_high += peak_hit
        repeated_as_high += repeated_hit
        either += peak_hit or repeated_hit
    return peak_as_high, repeated_as_high, either


@frozen("digraph")
def digraph_report() -> dict:
    pairs = list(challenge_pairs())
    control = _control_pairs()
    peak, repeated = _counts(pairs)
    control_peak, control_repeated = _counts(control)
    peak_as_high, repeated_as_high, either = _null(pairs, peak, repeated)
    control_peak_as_high, control_repeated_as_high, control_either = _null(
        control, control_peak, control_repeated
    )
    return {
        "solved": False,
        "claimed_plaintext": None,
        "cells": len(pairs),
        "peak": peak,
        "repeated_digraphs": repeated,
        "draws": _DRAWS,
        "peak_as_high": peak_as_high,
        "repeated_as_high": repeated_as_high,
        "either_as_high": either,
        "control_cells": len(control),
        "control_peak": control_peak,
        "control_repeated_digraphs": control_repeated,
        "control_peak_as_high": control_peak_as_high,
        "control_repeated_as_high": control_repeated_as_high,
        "control_either_as_high": control_either,
        "scope": (
            "A digraph count that a second count can explain is not a reading. "
            "The solved exercise is the check. No letter string is stored."
        ),
    }
