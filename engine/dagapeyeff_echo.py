"""A spaced triple is echoed in a parallel line. Not a reading.

A line holds a cell exactly three times, the gaps are equal, and the
three seats are not adjacent. The triple is echoed when a parallel line
holds that cell in at least two of those seats. Rows and columns both
count, and any cell may do it. No letter string is stored.
"""

from __future__ import annotations

import random

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_swarm import challenge_pairs

_SEED = 20261004
_DRAWS = 20000
_WIDTH = 14


def _lines(seq: list[str], axis: int) -> list[list[str]]:
    if axis == 0:
        return [seq[row * _WIDTH:(row + 1) * _WIDTH] for row in range(_WIDTH)]
    return [[seq[row * _WIDTH + column] for row in range(_WIDTH)] for column in range(_WIDTH)]


def _echoes(seq: list[str]) -> list[dict[str, object]]:
    found = []
    for axis in (0, 1):
        lines = _lines(seq, axis)
        for index, line in enumerate(lines):
            buckets: dict[str, list[int]] = {}
            for seat, cell in enumerate(line):
                buckets.setdefault(cell, []).append(seat)
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
                    echoed = [seat for seat in seats if parallel[seat] == cell]
                    if len(echoed) >= 2:
                        found.append({
                            "cell": cell,
                            "axis": "row" if axis == 0 else "column",
                            "index": index,
                            "seats": seats,
                            "step": step,
                            "echo": other,
                            "echoed": echoed,
                        })
                        break
    return found


@frozen("echo")
def echo_report() -> dict:
    pairs = list(challenge_pairs())
    found = _echoes(pairs)
    seen = random.Random(_SEED)
    as_many = 0
    for _ in range(_DRAWS):
        shuffled = pairs[:]
        seen.shuffle(shuffled)
        if len(_echoes(shuffled)) >= len(found):
            as_many += 1
    return {
        "solved": False,
        "claimed_plaintext": None,
        "echoes": found,
        "echo_count": len(found),
        "draws": _DRAWS,
        "as_many": as_many,
        "allowed": as_many / _DRAWS < 0.05,
        "scope": "An echoed spaced triple is not a reading. No letter string is stored.",
    }
