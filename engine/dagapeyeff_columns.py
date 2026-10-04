"""Other reading orders, scored by dictionary shape. Not a reading.

The printed order matches fewer dictionary shapes than a shuffle. This pass
asks whether a different width, or a different order of the 14 columns,
matches more. The words are not kept. Shuffled cells get the same search.
"""

from __future__ import annotations

import random
from engine.dagapeyeff_cache import frozen

from engine.dagapeyeff_order import _grid
from engine.dagapeyeff_patterns import _hits, _shapes
from engine.dagapeyeff_swarm import challenge_pairs

_SEED = 20261004
_COLUMN_DRAWS = 25_000
_NULL_GRIDS = 8


def _rows(pairs: list[str], width: int) -> list[list[str]]:
    return [pairs[start : start + width] for start in range(0, len(pairs), width)]


def _down(pairs: list[str], width: int) -> list[str]:
    rows = _rows(pairs, width)
    out = []
    for column in range(width):
        for row in rows:
            if column < len(row):
                out.append(row[column])
    return out


def _best_route(pairs: list[str], shapes: set) -> tuple[int, int, str]:
    best = (_hits(pairs, shapes), 14, "across")
    for width in range(2, 29):
        down = _hits(_down(pairs, width), shapes)
        if down > best[0]:
            best = (down, width, "down")
    return best


def _column_read(pairs: list[str], order: list[int]) -> list[str]:
    grid = _grid(pairs)
    return [grid[row][column] for row in range(14) for column in order]


def _best_columns(pairs: list[str], shapes: set, draws: int, drawn: random.Random) -> int:
    identity = list(range(14))
    best = _hits(_column_read(pairs, identity), shapes)
    for _ in range(draws):
        order = identity[:]
        drawn.shuffle(order)
        score = _hits(_column_read(pairs, order), shapes)
        if score > best:
            best = score
    return best


@frozen("columns")
def column_report() -> dict:
    shapes = _shapes()
    pairs = list(challenge_pairs())
    route_hits, route_width, route_read = _best_route(pairs, shapes)
    drawn = random.Random(_SEED)
    column_best = _best_columns(pairs, shapes, _COLUMN_DRAWS, drawn)
    as_high = 0
    for index in range(_NULL_GRIDS):
        shuffled = pairs[:]
        drawn.shuffle(shuffled)
        null_best = _best_columns(shuffled, shapes, _COLUMN_DRAWS, random.Random(_SEED + 1 + index))
        if null_best >= column_best:
            as_high += 1
    return {
        "solved": False,
        "claimed_plaintext": None,
        "route_hits": route_hits,
        "route_width": route_width,
        "route_read": route_read,
        "column_draws": _COLUMN_DRAWS,
        "column_best": column_best,
        "null_grids": _NULL_GRIDS,
        "nulls_as_high": as_high,
        "trials": _COLUMN_DRAWS * (1 + _NULL_GRIDS),
        "scope": (
            "A higher window count from a searched order is not a word. "
            "No letter string is stored."
        ),
    }
