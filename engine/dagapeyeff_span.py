"""A palindrome fills the span of a spaced triple. Not a reading.

A line holds a cell exactly three times, equally spaced and not adjacent.
The seats from the first to the last are the span. The span is filled when
a parallel line reads the same forwards and backwards across those seats.
Rows and columns both count, and any cell may do it. No letter string
is stored.
"""

from __future__ import annotations

import random
from collections import defaultdict

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_swarm import challenge_pairs

_SEED = 20261004
_DRAWS = 20000
_WIDTH = 14


def _lines(seq: list[str], axis: int) -> list[list[str]]:
    if axis == 0:
        return [seq[row * _WIDTH:(row + 1) * _WIDTH] for row in range(_WIDTH)]
    return [[seq[row * _WIDTH + column] for row in range(_WIDTH)] for column in range(_WIDTH)]


def _spans(seq: list[str]) -> list[dict[str, object]]:
    found = []
    for axis in (0, 1):
        lines = _lines(seq, axis)
        for index, line in enumerate(lines):
            buckets: dict[str, list[int]] = defaultdict(list)
            for seat, cell in enumerate(line):
                buckets[cell].append(seat)
            for cell, seats in buckets.items():
                if len(seats) != 3:
                    continue
                start, middle, end = seats
                step = middle - start
                if step < 2 or end - middle != step:
                    continue
                for other, parallel in enumerate(lines):
                    if other == index:
                        continue
                    window = parallel[start:end + 1]
                    if window == window[::-1]:
                        found.append({
                            "cell": cell,
                            "axis": "row" if axis == 0 else "column",
                            "index": index,
                            "seats": seats,
                            "span": [start, end],
                            "echo": other,
                            "window": window,
                        })
                        break
    return found


@frozen("span")
def span_report() -> dict:
    pairs = list(challenge_pairs())
    found = _spans(pairs)
    seen = random.Random(_SEED)
    as_many = 0
    for _ in range(_DRAWS):
        shuffled = pairs[:]
        seen.shuffle(shuffled)
        if len(_spans(shuffled)) >= len(found):
            as_many += 1
    return {
        "solved": False,
        "claimed_plaintext": None,
        "spans": found,
        "span_count": len(found),
        "draws": _DRAWS,
        "as_many": as_many,
        "allowed": as_many / _DRAWS < 0.05,
        "scope": "A palindrome on a spaced span is not a reading. No letter string is stored.",
    }
