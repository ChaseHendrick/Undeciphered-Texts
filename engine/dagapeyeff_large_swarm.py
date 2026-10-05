"""A large deletion search, and a large repeat-gap search. Not a reading.

Every pair of cells is dropped, 19,110 ways, and the best score is compared
with shuffled cells that get the same search. Repeat gaps are tested at
periods 2 through 28 against 5,000 shuffles. No letter string is stored.
"""

from __future__ import annotations

import math
import random

from engine.alphabet import letters_only, to_ints
from engine.dagapeyeff_add import _PROSE, _cells
from engine.dagapeyeff_cache import frozen
from engine.language import ENGLISH_ORDER, get_legacy_model

_SEED = 20261004
_DELETION_DRAWS = 40
_GAP_DRAWS = 5000
_PERIODS = range(2, 29)


def _quad(seq: list[int], logp: list[float], english: list[int]) -> float:
    counts = [0] * 25
    for cell in seq:
        counts[cell] += 1
    order = sorted(range(25), key=lambda cell: (-counts[cell], cell))
    mapping = [0] * 25
    rank = 0
    for cell in order:
        if counts[cell] == 0:
            continue
        mapping[cell] = english[rank]
        rank += 1
    plain = [mapping[cell] for cell in seq]
    left, mid, right = plain[0], plain[1], plain[2]
    total = 0.0
    for nxt in plain[3:]:
        total += logp[((left * 26 + mid) * 26 + right) * 26 + nxt]
        left, mid, right = mid, right, nxt
    return total / (len(plain) - 3)


def _best_pair(cells: list[int], logp: list[float], english: list[int]) -> float:
    best = float("-inf")
    count = len(cells)
    for left_at in range(count - 1):
        head = cells[:left_at]
        tail = cells[left_at + 1 :]
        for right_at in range(left_at + 1, count):
            offset = right_at - left_at - 1
            seq = head + tail[:offset] + tail[offset + 1 :]
            score = _quad(seq, logp, english)
            if score > best:
                best = score
    return best


def _gaps(cells: list[int]) -> list[int]:
    last: dict[int, int] = {}
    gaps = []
    for index, cell in enumerate(cells):
        if cell in last:
            gaps.append(index - last[cell])
        last[cell] = index
    return gaps


def _peak_z(gaps: list[int]) -> float:
    count = len(gaps)
    peak = float("-inf")
    for period in _PERIODS:
        hits = sum(gap % period == 0 for gap in gaps)
        expected = count / period
        variance = count * (1 / period) * (1 - 1 / period)
        score = (hits - expected) / math.sqrt(variance)
        if score > peak:
            peak = score
    return peak


@frozen("large-swarm")
def large_swarm_report() -> dict:
    logp = get_legacy_model().logp
    english = [ord(char) - 65 for char in ENGLISH_ORDER]
    cells = _cells()
    pairs = len(cells) * (len(cells) - 1) // 2
    deletion = _best_pair(cells, logp, english)
    prose = to_ints(letters_only(_PROSE))
    prose_score = get_legacy_model().score(prose) / (len(prose) - 3)
    drawn = random.Random(_SEED)
    deletion_as_high = 0
    for _ in range(_DELETION_DRAWS):
        shuffled = cells[:]
        drawn.shuffle(shuffled)
        if _best_pair(shuffled, logp, english) >= deletion:
            deletion_as_high += 1
    gaps = _gaps(cells)
    peak = _peak_z(gaps)
    gap_draw = random.Random(_SEED)
    gap_as_high = 0
    for _ in range(_GAP_DRAWS):
        shuffled = cells[:]
        gap_draw.shuffle(shuffled)
        if _peak_z(_gaps(shuffled)) >= peak:
            gap_as_high += 1
    return {
        "solved": False,
        "claimed_plaintext": None,
        "cells": len(cells),
        "pairs": pairs,
        "deletion_quadgram": round(deletion, 4),
        "prose_quadgram": round(prose_score, 4),
        "reaches_prose": deletion >= prose_score,
        "deletion_draws": _DELETION_DRAWS,
        "deletion_shuffles_as_high": deletion_as_high,
        "gap_periods": "2-28",
        "gap_count": len(gaps),
        "gap_peak_z": round(peak, 4),
        "gap_draws": _GAP_DRAWS,
        "gap_shuffles_as_high": gap_as_high,
        "scope": "A large search is not a reading. No letter string is stored.",
    }
