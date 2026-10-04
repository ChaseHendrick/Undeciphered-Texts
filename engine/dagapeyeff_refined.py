"""The most surprising neighboring pair, not the average. Not a reading.

The large gap search found no period. This asks whether any one pair of
neighbors is still surprising once the symbol counts are fixed. Shuffled
copies keep those counts. No letter string is stored.
"""

from __future__ import annotations

import math
import random
from collections import Counter

from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_cache import frozen

_SEED = 20261004
_DRAWS = 2000


def _peak(cells: list[int]) -> tuple[float, int]:
    length = len(cells)
    singles = Counter(cells)
    pairs = Counter(zip(cells, cells[1:]))
    steps = length - 1
    best = float("-inf")
    best_count = 0
    for (left, right), count in pairs.items():
        expected = steps * (singles[left] / length) * (singles[right] / length)
        if expected <= 0:
            continue
        score = (count - expected) / math.sqrt(expected)
        if score > best:
            best = score
            best_count = count
    return best, best_count


@frozen("refined-swarm")
def refined_report() -> dict:
    cells = _cells()
    peak, count = _peak(cells)
    drawn = random.Random(_SEED)
    as_high = 0
    for _ in range(_DRAWS):
        shuffled = cells[:]
        drawn.shuffle(shuffled)
        score, _pair_count = _peak(shuffled)
        if score >= peak:
            as_high += 1
    return {
        "solved": False,
        "claimed_plaintext": None,
        "cells": len(cells),
        "peak_z": round(peak, 4),
        "peak_count": count,
        "draws": _DRAWS,
        "shuffles_as_high": as_high,
        "scope": "One surprising pair is not a reading. No letter string is stored.",
    }
