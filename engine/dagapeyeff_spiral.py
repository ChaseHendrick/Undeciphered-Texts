"""Spiral, snake and zigzag routes on the 14 by 14 square. Not a reading.

Earlier passes tried column keys, rails, straight diagonals and regular
deletions. These are the remaining classical routes on a square: a spiral
from each corner in each turning direction, a snake along rows or columns
from each side, and a zigzag along the diagonals from each corner. Each
route is read two ways: as the path the plaintext was written along before
the rows were copied out, and as the path the rows were copied out along.

The score is successive-symbol information, which no letter key can change.
The control gives shuffled cells the same set of routes and keeps the best.
No letter string is stored.
"""

from __future__ import annotations

import random

from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_order import _mi, _prose

SIDE = 14
_SEED = 20261012
_DRAWS = 2000


def _corner_frames():
    """The 8 symmetries of the square, as maps from a canonical (row, column)."""
    last = SIDE - 1
    return [
        lambda r, c: (r, c),
        lambda r, c: (r, last - c),
        lambda r, c: (last - r, c),
        lambda r, c: (last - r, last - c),
        lambda r, c: (c, r),
        lambda r, c: (c, last - r),
        lambda r, c: (last - c, r),
        lambda r, c: (last - c, last - r),
    ]


def _spiral() -> list[tuple[int, int]]:
    top, bottom, left, right = 0, SIDE - 1, 0, SIDE - 1
    path = []
    while top <= bottom and left <= right:
        path.extend((top, c) for c in range(left, right + 1))
        path.extend((r, right) for r in range(top + 1, bottom + 1))
        if top < bottom:
            path.extend((bottom, c) for c in range(right - 1, left - 1, -1))
        if left < right:
            path.extend((r, left) for r in range(bottom - 1, top, -1))
        top, bottom, left, right = top + 1, bottom - 1, left + 1, right - 1
    return path


def _snake() -> list[tuple[int, int]]:
    path = []
    for r in range(SIDE):
        columns = range(SIDE) if r % 2 == 0 else range(SIDE - 1, -1, -1)
        path.extend((r, c) for c in columns)
    return path


def _zigzag() -> list[tuple[int, int]]:
    path = []
    for total in range(2 * SIDE - 1):
        diagonal = [(r, total - r) for r in range(SIDE) if 0 <= total - r < SIDE]
        path.extend(diagonal if total % 2 else diagonal[::-1])
    return path


def routes() -> dict[str, list[int]]:
    """Every distinct route as a list of square positions, row-major numbering."""
    found: dict[str, list[int]] = {}
    seen = set()
    for name, base in (("spiral", _spiral()), ("snake", _snake()), ("zigzag", _zigzag())):
        for index, frame in enumerate(_corner_frames()):
            path = [frame(r, c) for r, c in base]
            positions = [r * SIDE + c for r, c in path]
            key = tuple(positions)
            if key in seen or tuple(reversed(positions)) in seen:
                continue
            seen.add(key)
            found[f"{name}-{index}"] = positions
    return found


def _readings(cells: list[int], path: list[int]) -> tuple[list[int], list[int]]:
    written = [cells[position] for position in path]
    copied = [0] * len(cells)
    for index, position in enumerate(path):
        copied[position] = cells[index]
    return written, copied


def best_route(cells: list[int], table: dict[str, list[int]]) -> tuple[float, str]:
    best = (-1.0, "")
    for name, path in table.items():
        written, copied = _readings(cells, path)
        for label, sequence in (("written", written), ("copied", copied)):
            score = _mi(sequence)
            if score > best[0]:
                best = (score, f"{name}-{label}")
    return best


@frozen("dagapeyeff-spiral")
def spiral_report() -> dict:
    table = routes()
    cells = _cells()
    score, name = best_route(cells, table)
    drawn = random.Random(_SEED)
    as_high = 0
    for _ in range(_DRAWS):
        shuffled = cells[:]
        drawn.shuffle(shuffled)
        if best_route(shuffled, table)[0] >= score:
            as_high += 1
    english = _prose("english.txt", len(cells))
    return {
        "solved": False,
        "claimed_plaintext": None,
        "routes": len(table),
        "readings": 2 * len(table),
        "printed_mi": round(_mi(cells), 4),
        "best_mi": round(score, 4),
        "best_route": name,
        "draws": _DRAWS,
        "shuffles_as_high": as_high,
        "english_mi": round(_mi(english), 4),
        "scope": (
            "The best spiral, snake or zigzag reading is matched by shuffled cells given the same "
            "routes, and it stays under same-length English. No letter key can raise this score. "
            "Not a reading. No letter string is stored."
        ),
    }
