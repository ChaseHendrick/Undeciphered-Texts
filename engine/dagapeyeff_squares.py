"""One tied cell prefers one color of the board. Not a reading.

The cells are the ones whose count is 17. Black and white are the two
colors of the grid, (row + column) even and odd. A straight run alternates
those colors, so a run cannot pile onto one of them. The score is the
larger split among the four cells, and a scramble is allowed the same
choice. No letter string is stored.
"""

from __future__ import annotations

import random
from collections import Counter

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_swarm import challenge_pairs

_SEED = 20261004
_DRAWS = 20000
_WIDTH = 14


def _split(seq: list[str], cell: str) -> tuple[int, int, int]:
    even = 0
    odd = 0
    for index, symbol in enumerate(seq):
        if symbol != cell:
            continue
        row, column = divmod(index, _WIDTH)
        if (row + column) % 2:
            odd += 1
        else:
            even += 1
    return abs(even - odd), even, odd


def _worst(seq: list[str], cells: tuple[str, ...]) -> int:
    return max(_split(seq, cell)[0] for cell in cells)


@frozen("squares")
def squares_report() -> dict:
    pairs = list(challenge_pairs())
    counts = Counter(pairs)
    cells = tuple(sorted(cell for cell, count in counts.items() if count == 17))
    observed = _worst(pairs, cells)
    detail = {}
    where = ""
    for cell in cells:
        gap, even, odd = _split(pairs, cell)
        detail[cell] = {"even": even, "odd": odd, "gap": gap}
        if gap == observed and where == "":
            where = cell
    seen = random.Random(_SEED)
    as_split = 0
    for _ in range(_DRAWS):
        shuffled = pairs[:]
        seen.shuffle(shuffled)
        if _worst(shuffled, cells) >= observed:
            as_split += 1
    return {
        "solved": False,
        "claimed_plaintext": None,
        "cells": list(cells),
        "cell": where,
        "even": detail[where]["even"],
        "odd": detail[where]["odd"],
        "gap": observed,
        "detail": detail,
        "draws": _DRAWS,
        "as_split": as_split,
        "allowed": as_split / _DRAWS < 0.05,
        "scope": "A color split of a tied cell is not a reading. No letter string is stored.",
    }
