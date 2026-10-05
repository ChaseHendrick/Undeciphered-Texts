"""63 sits between two copies of the most common cell.

A gap counts in a row or in a column. The middle cell has to be one that
also forms a run of three in some row, and it cannot be the common cell
itself. A shuffle of the cells is the null. No letter string is stored.
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


def _gaps(seq: list[str]) -> tuple[int, str, str, list[tuple[int, int, str]]]:
    mode = Counter(seq).most_common(1)[0][0]
    triples: set[str] = set()
    index = 0
    length = len(seq)
    while index < length:
        end = index
        while end + 1 < length and seq[end + 1] == seq[index] and (end + 1) % _WIDTH != 0:
            end += 1
        if end // _WIDTH == index // _WIDTH and end - index + 1 >= _RUN and seq[index] != mode:
            triples.add(seq[index])
        index = end + 1
    found = []
    for row in range(_WIDTH):
        for column in range(1, _WIDTH - 1):
            middle = seq[row * _WIDTH + column]
            if (
                seq[row * _WIDTH + column - 1] == mode
                and seq[row * _WIDTH + column + 1] == mode
                and middle in triples
            ):
                found.append((row, column, "row"))
    for column in range(_WIDTH):
        for row in range(1, _WIDTH - 1):
            middle = seq[row * _WIDTH + column]
            if (
                seq[(row - 1) * _WIDTH + column] == mode
                and seq[(row + 1) * _WIDTH + column] == mode
                and middle in triples
            ):
                found.append((row, column, "column"))
    middle = seq[found[0][0] * _WIDTH + found[0][1]] if found else ""
    return len(found), mode, middle, found


@frozen("sandwich")
def sandwich_report() -> dict:
    pairs = list(challenge_pairs())
    count, mode, middle, found = _gaps(pairs)
    drawn = random.Random(_SEED)
    hits = 0
    for _ in range(_DRAWS):
        shuffled = pairs[:]
        drawn.shuffle(shuffled)
        if _gaps(shuffled)[0] >= count:
            hits += 1
    return {
        "solved": False,
        "claimed_plaintext": None,
        "mode": mode,
        "middle": middle,
        "gaps": count,
        "places": [{"row": row, "column": column, "axis": axis} for row, column, axis in found],
        "draws": _DRAWS,
        "as_many": hits,
        "scope": "A cell between two copies of another is not a reading. No letter string is stored.",
    }
