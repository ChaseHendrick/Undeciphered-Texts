"""The two runs of three sit in the same printed columns.

A run is three or more copies of one cell inside one row of the 14 by 14
grid. The score is the most runs that share a starting column. A shuffle of
the cells is the null. The solved exercise is not a 14 by 14 grid, so it is
not this control. No letter string is stored.
"""

from __future__ import annotations

import random
from collections import Counter

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_swarm import challenge_pairs

_SEED = 20261004
_DRAWS = 20000
_WIDTH = 14
_RUN = 3


def _shared_starts(seq: list[str]) -> int:
    starts = []
    index = 0
    length = len(seq)
    while index < length:
        end = index
        while end + 1 < length and seq[end + 1] == seq[index] and (end + 1) % _WIDTH != 0:
            end += 1
        if end // _WIDTH == index // _WIDTH and end - index + 1 >= _RUN:
            starts.append(index % _WIDTH)
        index = end + 1
    if not starts:
        return 0
    return max(Counter(starts).values())


def _runs(seq: list[str]) -> list[dict]:
    found = []
    index = 0
    length = len(seq)
    while index < length:
        end = index
        while end + 1 < length and seq[end + 1] == seq[index] and (end + 1) % _WIDTH != 0:
            end += 1
        if end // _WIDTH == index // _WIDTH and end - index + 1 >= _RUN:
            found.append({
                "cell": seq[index],
                "row": index // _WIDTH,
                "column": index % _WIDTH,
                "length": end - index + 1,
            })
        index = end + 1
    return found


@frozen("triples")
def triples_report() -> dict:
    pairs = list(challenge_pairs())
    runs = _runs(pairs)
    shared = _shared_starts(pairs)
    drawn = random.Random(_SEED)
    hits = 0
    for _ in range(_DRAWS):
        shuffled = pairs[:]
        drawn.shuffle(shuffled)
        if _shared_starts(shuffled) >= shared:
            hits += 1
    return {
        "solved": False,
        "claimed_plaintext": None,
        "runs": len(runs),
        "cells": [run["cell"] for run in runs],
        "rows": [run["row"] for run in runs],
        "columns": [run["column"] for run in runs],
        "lengths": [run["length"] for run in runs],
        "shared_starts": shared,
        "draws": _DRAWS,
        "as_aligned": hits,
        "scope": (
            "Two runs in one column band are not a reading. "
            "No letter string is stored."
        ),
    }
