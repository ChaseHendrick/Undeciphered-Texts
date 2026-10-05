"""Four cells share a count, and they do not pile into one line. Not a reading.

The cells are the ones whose count is 17. A scramble keeps every cell and
moves their places. The score is the fuller of the two directions, rows or
columns, so a scramble is allowed its more even direction. Two other sets
are scored the same way: the most common cell, and the next four cells by
count. No letter string is stored.
"""

from __future__ import annotations

import random
from collections import Counter

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_swarm import challenge_pairs

_SEED = 20261004
_DRAWS = 100000
_WIDTH = 14


def _most(seq: list[str], tied: frozenset[str], axis: str) -> int:
    best = 0
    if axis == "row":
        for row in range(_WIDTH):
            count = sum(seq[row * _WIDTH + column] in tied for column in range(_WIDTH))
            if count > best:
                best = count
    else:
        for column in range(_WIDTH):
            count = sum(seq[row * _WIDTH + column] in tied for row in range(_WIDTH))
            if count > best:
                best = count
    return best


def _even(seq: list[str], tied: frozenset[str]) -> int:
    return min(_most(seq, tied, "row"), _most(seq, tied, "column"))


@frozen("quartet")
def quartet_report() -> dict:
    pairs = list(challenge_pairs())
    counts = Counter(pairs)
    tied = frozenset(cell for cell, count in counts.items() if count == 17)
    ranked = [cell for cell, _count in counts.most_common() if cell not in tied]
    mode = frozenset(ranked[:1])
    nxt = frozenset(ranked[:4])
    observed = _even(pairs, tied)
    mode_observed = _even(pairs, mode)
    next_observed = _even(pairs, nxt)
    seen = random.Random(_SEED)
    as_even = 0
    mode_as_even = 0
    next_as_even = 0
    for _ in range(_DRAWS):
        shuffled = pairs[:]
        seen.shuffle(shuffled)
        if _even(shuffled, tied) <= observed:
            as_even += 1
        if _even(shuffled, mode) <= mode_observed:
            mode_as_even += 1
        if _even(shuffled, nxt) <= next_observed:
            next_as_even += 1
    return {
        "solved": False,
        "claimed_plaintext": None,
        "cells": sorted(tied),
        "count": 17,
        "copies": sum(counts[cell] for cell in tied),
        "row_most": _most(pairs, tied, "row"),
        "column_most": _most(pairs, tied, "column"),
        "cap": observed,
        "draws": _DRAWS,
        "as_even": as_even,
        "mode_cell": sorted(mode),
        "mode_cap": mode_observed,
        "mode_as_even": mode_as_even,
        "next_cells": sorted(nxt),
        "next_cap": next_observed,
        "next_as_even": next_as_even,
        "allowed": as_even / _DRAWS < 0.05 and mode_as_even / _DRAWS >= 0.05 and next_as_even / _DRAWS >= 0.05,
        "scope": "Four cells that share a count are not a reading. No letter string is stored.",
    }
