"""The aligned runs sit next to rare cells. Not a reading.

A run is three or more copies of one cell inside one row. Rare cells are
the ones that appear at most three times. A run sits next to a rare cell
when the cell before it or the cell after it, in the same row, is rare.
The alignment of two runs was already scored. This asks whether that
contact still happens once a shuffle already has the alignment. No letter
string is stored.
"""

from __future__ import annotations

import random
from collections import Counter, defaultdict

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_swarm import challenge_pairs

_SEED = 20261004
_DRAWS = 40000
_WIDTH = 14
_RUN = 3


def _rare(seq: list[str]) -> set[str]:
    return {cell for cell, count in Counter(seq).items() if count <= _RUN}


def _band(seq: list[str], rare: set[str]) -> tuple[int, int, list[dict]]:
    runs = []
    index = 0
    length = len(seq)
    while index < length:
        end = index
        while end + 1 < length and seq[end + 1] == seq[index] and (end + 1) % _WIDTH != 0:
            end += 1
        if end // _WIDTH == index // _WIDTH and end - index + 1 >= _RUN:
            row = index // _WIDTH
            start = index % _WIDTH
            stop = end % _WIDTH
            previous = seq[row * _WIDTH + start - 1] if start else None
            following = seq[row * _WIDTH + stop + 1] if stop < _WIDTH - 1 else None
            runs.append({
                "cell": seq[index],
                "row": row,
                "column": start,
                "previous": previous,
                "following": following,
                "touches": previous in rare or following in rare,
            })
        index = end + 1
    if not runs:
        return 0, 0, runs
    by_column: dict[int, int] = defaultdict(int)
    touched: dict[int, int] = defaultdict(int)
    for run in runs:
        by_column[run["column"]] += 1
        if run["touches"]:
            touched[run["column"]] += 1
    column = max(by_column, key=lambda item: (by_column[item], touched[item]))
    return by_column[column], touched[column], runs


@frozen("contact")
def contact_report() -> dict:
    pairs = list(challenge_pairs())
    rare = _rare(pairs)
    shared, touched, runs = _band(pairs, rare)
    drawn = random.Random(_SEED)
    aligned = 0
    contact = 0
    for _ in range(_DRAWS):
        shuffled = pairs[:]
        drawn.shuffle(shuffled)
        shuffle_shared, shuffle_touched, _ignored = _band(shuffled, rare)
        if shuffle_shared >= shared:
            aligned += 1
            if shuffle_touched >= touched:
                contact += 1
    return {
        "solved": False,
        "claimed_plaintext": None,
        "rare": sorted(rare),
        "cells": [run["cell"] for run in runs],
        "following": [run["following"] for run in runs],
        "shared": shared,
        "touched": touched,
        "draws": _DRAWS,
        "aligned": aligned,
        "contact": contact,
        "scope": (
            "Contact with a rare cell is not a reading. "
            "No letter string is stored."
        ),
    }
