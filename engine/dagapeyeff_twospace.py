"""Two cells in one line are each equally spaced. Not a reading.

A line is a row or a column. A cell counts when it appears in that line
exactly three times, the gaps are equal, and the three seats are not
adjacent. The score is how many lines hold two or more such cells. A
scramble may use any cells. No letter string is stored.
"""

from __future__ import annotations

import random

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_swarm import challenge_pairs

_SEED = 20261004
_DRAWS = 20000
_WIDTH = 14


def _line(seq: list[str], axis: int, fixed: int) -> list[str]:
    if axis == 0:
        return seq[fixed * _WIDTH:(fixed + 1) * _WIDTH]
    return [seq[row * _WIDTH + fixed] for row in range(_WIDTH)]


def _spaced(seats: list[int]) -> bool:
    if len(seats) != 3:
        return False
    step = seats[1] - seats[0]
    return step >= 2 and seats[2] - seats[1] == step


def _hosts(seq: list[str]) -> int:
    count = 0
    for axis in (0, 1):
        for fixed in range(_WIDTH):
            buckets: dict[str, list[int]] = {}
            for index, cell in enumerate(_line(seq, axis, fixed)):
                buckets.setdefault(cell, []).append(index)
            spaced = sum(_spaced(seats) for seats in buckets.values())
            if spaced >= 2:
                count += 1
    return count


def _where(seq: list[str]) -> list[dict[str, object]]:
    found = []
    for axis in (0, 1):
        for fixed in range(_WIDTH):
            buckets: dict[str, list[int]] = {}
            for index, cell in enumerate(_line(seq, axis, fixed)):
                buckets.setdefault(cell, []).append(index)
            cells = [
                {"cell": cell, "seats": seats, "step": seats[1] - seats[0]}
                for cell, seats in sorted(buckets.items())
                if _spaced(seats)
            ]
            if len(cells) >= 2:
                found.append({"axis": "row" if axis == 0 else "column", "index": fixed, "cells": cells})
    return found


@frozen("twospace")
def twospace_report() -> dict:
    pairs = list(challenge_pairs())
    found = _where(pairs)
    observed = len(found)
    seen = random.Random(_SEED)
    as_many = 0
    for _ in range(_DRAWS):
        shuffled = pairs[:]
        seen.shuffle(shuffled)
        if _hosts(shuffled) >= observed:
            as_many += 1
    return {
        "solved": False,
        "claimed_plaintext": None,
        "lines": found,
        "line_count": observed,
        "draws": _DRAWS,
        "as_many": as_many,
        "allowed": as_many / _DRAWS < 0.05,
        "scope": "Two spaced triples in one line are not a reading. No letter string is stored.",
    }
