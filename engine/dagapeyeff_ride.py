"""An echoed triple rides on another spaced triple. Not a reading.

An echo is a line that holds a cell exactly three times, equally spaced
and not adjacent, with a parallel line repeating at least two of those
seats. The ride is when those two lines are also two seats of some
spaced triple, of any cell, in the other direction. No letter string
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


def _rides(seq: list[str]) -> list[dict[str, object]]:
    echoes: list[tuple[int, int, int, str]] = []
    triples: list[tuple[int, str, tuple[int, int, int]]] = []
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
                triple = (axis, cell, (start, middle, end))
                triples.append(triple)
                for other, parallel in enumerate(lines):
                    if other == index:
                        continue
                    if sum(parallel[seat] == cell for seat in seats) >= 2:
                        echoes.append((axis, index, other, cell))
                        break
    found = []
    for axis, index, other, cell in echoes:
        for taxis, tcell, tseats in triples:
            if taxis == axis:
                continue
            if index in tseats and other in tseats:
                found.append({
                    "echo_cell": cell,
                    "echo_axis": "row" if axis == 0 else "column",
                    "lines": sorted((index, other)),
                    "carrier_cell": tcell,
                    "carrier_axis": "column" if axis == 0 else "row",
                    "carrier_seats": list(tseats),
                })
                break
    return found


@frozen("ride")
def ride_report() -> dict:
    pairs = list(challenge_pairs())
    found = _rides(pairs)
    seen = random.Random(_SEED)
    as_many = 0
    for _ in range(_DRAWS):
        shuffled = pairs[:]
        seen.shuffle(shuffled)
        if len(_rides(shuffled)) >= len(found):
            as_many += 1
    return {
        "solved": False,
        "claimed_plaintext": None,
        "rides": found,
        "ride_count": len(found),
        "draws": _DRAWS,
        "as_many": as_many,
        "allowed": as_many / _DRAWS < 0.05,
        "scope": "An echo riding on a spaced triple is not a reading. No letter string is stored.",
    }
