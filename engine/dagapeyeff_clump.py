"""Pair 72 in the last rows looked rare. The window was chosen after looking.

Six of the nine 72 pairs sit in the last four rows. That is 35 of 2000
shuffles if the window is fixed in advance. The same height, scored at every
starting row, is 268 of 2000. The second number is the one that counts.
No letter string is stored.
"""

from __future__ import annotations

import random
from collections import Counter

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_swarm import challenge_pairs

_SEED = 20261004
_DRAWS = 2000
_WIDTH = 4


def _rows(cells: list[str]) -> list[int]:
    rows = [0] * 14
    for index, cell in enumerate(cells):
        if cell == "72":
            rows[index // 14] += 1
    return rows


def _window(rows: list[int], start: int, width: int) -> int:
    return sum(rows[start : start + width])


def _best(rows: list[int], width: int) -> int:
    return max(_window(rows, start, width) for start in range(14 - width + 1))


@frozen("clump")
def clump_report() -> dict:
    cells = list(challenge_pairs())
    rows = _rows(cells)
    fixed = _window(rows, 10, _WIDTH)
    best = _best(rows, _WIDTH)
    drawn = random.Random(_SEED)
    fixed_high = 0
    every_high = 0
    for _ in range(_DRAWS):
        shuffled = cells[:]
        drawn.shuffle(shuffled)
        other = _rows(shuffled)
        if _window(other, 10, _WIDTH) >= fixed:
            fixed_high += 1
        if _best(other, _WIDTH) >= best:
            every_high += 1
    return {
        "solved": False,
        "claimed_plaintext": None,
        "symbol": "72",
        "count": sum(rows),
        "width": _WIDTH,
        "fixed_start": 10,
        "fixed_count": fixed,
        "fixed_chosen_after_looking": True,
        "fixed_shuffles_as_high": fixed_high,
        "every_window_count": best,
        "every_window_shuffles_as_high": every_high,
        "draws": _DRAWS,
        "scope": "A window chosen after looking is not a reading. No letter string is stored.",
    }
