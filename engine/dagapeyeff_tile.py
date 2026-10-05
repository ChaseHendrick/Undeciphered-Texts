"""Two blocks copy a 2 by 2 of the square. Not a reading.

A block is four neighboring grid cells. It counts when those four cells are
all different and are the four corners of a 2 by 2 on the square. The two
blocks may sit anywhere, and they may be two different squares. No letter
string is stored.
"""

from __future__ import annotations

import random

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_swarm import challenge_pairs

_WIDTH = 14
_ROWS = "67890"
_COLS = "12345"
_SEED = 20261004
_DRAWS = 20000


def _place(cell: str) -> tuple[int, int]:
    return _ROWS.index(cell[0]), _COLS.index(cell[1])


def _is_tile(cells: tuple[str, str, str, str]) -> bool:
    if len(set(cells)) != 4:
        return False
    points = [_place(cell) for cell in cells]
    rows = sorted({point[0] for point in points})
    cols = sorted({point[1] for point in points})
    return len(rows) == 2 and len(cols) == 2 and rows[1] - rows[0] == 1 and cols[1] - cols[0] == 1


def _tiles(seq: list[str]) -> list[dict[str, object]]:
    grid = [seq[row * _WIDTH:(row + 1) * _WIDTH] for row in range(_WIDTH)]
    found = []
    for row in range(_WIDTH - 1):
        for col in range(_WIDTH - 1):
            cells = (
                grid[row][col],
                grid[row][col + 1],
                grid[row + 1][col],
                grid[row + 1][col + 1],
            )
            if _is_tile(cells):
                found.append({"row": row, "col": col, "cells": list(cells)})
    return found


@frozen("tile")
def tile_report() -> dict:
    found = _tiles(list(challenge_pairs()))
    seen = random.Random(_SEED)
    as_many = 0
    base = list(challenge_pairs())
    for _ in range(_DRAWS):
        bag = base[:]
        seen.shuffle(bag)
        if len(_tiles(bag)) >= len(found):
            as_many += 1
    return {
        "solved": False,
        "claimed_plaintext": None,
        "tiles": len(found),
        "found": found,
        "draws": _DRAWS,
        "as_many": as_many,
        "allowed": as_many / _DRAWS < 0.05,
        "scope": "Two blocks that copy a square are not a reading. No letter string is stored.",
    }
