"""The family router, and the rows and columns of the printed grid. Not a reading.

The router ranks known cipher families. A high score is not a plaintext.
The grid test asks whether one printed row or column repeats more than a
shuffled grid. No letter string is stored.
"""

from __future__ import annotations

import random
from collections import Counter

from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_cache import frozen
from engine.neural_router_v2 import route_probabilities

_SEED = 20261004
_ROUTER_DRAWS = 40
_GRID_DRAWS = 200
_WIDTH = 14


def _letters(cells: list[int]) -> str:
    return "".join(chr(65 + cell) for cell in cells)


def _ic(seq: list[int]) -> float:
    count = len(seq)
    if count < 2:
        return 0.0
    tally = Counter(seq)
    return sum(value * (value - 1) for value in tally.values()) / (count * (count - 1))


def _axes(cells: list[int]) -> tuple[float, float]:
    rows = [_ic(cells[index * _WIDTH : (index + 1) * _WIDTH]) for index in range(_WIDTH)]
    columns = [_ic(cells[index::_WIDTH]) for index in range(_WIDTH)]
    return max(rows), max(columns)


@frozen("router-swarm")
def router_swarm_report() -> dict:
    cells = _cells()
    if len(cells) != _WIDTH * _WIDTH:
        raise ValueError("the grid test expects a 14 by 14 block of cells")
    ranked = route_probabilities(_letters(cells))
    top = ranked["candidates"][0]
    second = ranked["candidates"][1]
    drawn = random.Random(_SEED)
    as_confident = 0
    same_family = 0
    for _ in range(_ROUTER_DRAWS):
        shuffled = cells[:]
        drawn.shuffle(shuffled)
        result = route_probabilities(_letters(shuffled))
        if result["candidates"][0]["family"] == top["family"]:
            same_family += 1
        if result["candidates"][0]["probability"] >= top["probability"]:
            as_confident += 1
    row_peak, column_peak = _axes(cells)
    column_index = max(range(_WIDTH), key=lambda index: _ic(cells[index::_WIDTH]))
    top_count = Counter(cells[column_index::_WIDTH]).most_common(1)[0][1]
    grid = random.Random(_SEED)
    row_as_high = 0
    column_as_high = 0
    for _ in range(_GRID_DRAWS):
        shuffled = cells[:]
        grid.shuffle(shuffled)
        row, column = _axes(shuffled)
        if row >= row_peak:
            row_as_high += 1
        if column >= column_peak:
            column_as_high += 1
    return {
        "solved": False,
        "claimed_plaintext": None,
        "families": len(ranked["candidates"]),
        "top_family": top["family"],
        "top_probability": round(top["probability"], 4),
        "second_family": second["family"],
        "uncertain": ranked["uncertain"],
        "router_draws": _ROUTER_DRAWS,
        "shuffles_same_family": same_family,
        "shuffles_as_confident": as_confident,
        "row_ic": round(row_peak, 4),
        "column_ic": round(column_peak, 4),
        "column_index": column_index,
        "column_top_count": top_count,
        "grid_draws": _GRID_DRAWS,
        "row_shuffles_as_high": row_as_high,
        "column_shuffles_as_high": column_as_high,
        "scope": "A family probability is not a reading. No letter string is stored.",
    }
