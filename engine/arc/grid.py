# SPDX-License-Identifier: MIT-0
"""Small immutable ARC grids. No test answer is needed by these operations."""
from __future__ import annotations

from collections import Counter

Grid = tuple[tuple[int, ...], ...]
MAX_SIDE = 30


def as_grid(value) -> Grid:
    if not isinstance(value, (list, tuple)) or not 1 <= len(value) <= MAX_SIDE:
        raise ValueError('a grid needs 1..30 rows')
    if not isinstance(value[0], (list, tuple)) or not 1 <= len(value[0]) <= MAX_SIDE:
        raise ValueError('a grid needs 1..30 columns')
    width = len(value[0])
    rows = []
    for row in value:
        if not isinstance(row, (list, tuple)) or len(row) != width:
            raise ValueError('grid rows must have equal lengths')
        if any(type(cell) is not int or not 0 <= cell <= 9 for cell in row):
            raise ValueError('grid colors must be integers in 0..9, excluding bool')
        rows.append(tuple(row))
    return tuple(rows)


def to_lists(grid: Grid | None):
    return None if grid is None else [list(row) for row in grid]


def shape(grid: Grid) -> tuple[int, int]:
    return len(grid), len(grid[0])


def mode_color(grid: Grid) -> int:
    counts = Counter(cell for row in grid for cell in row)
    return min(counts, key=lambda color: (-counts[color], color))


def crop_cells(grid: Grid, cells, *, mask=False, background=0) -> Grid | None:
    cells = tuple(cells)
    if not cells:
        return None
    top, bottom = min(r for r, _ in cells), max(r for r, _ in cells)
    left, right = min(c for _, c in cells), max(c for _, c in cells)
    if not mask:
        return tuple(row[left:right + 1] for row in grid[top:bottom + 1])
    selected = set(cells)
    return tuple(tuple(grid[r][c] if (r, c) in selected else background
                       for c in range(left, right + 1)) for r in range(top, bottom + 1))


def components(grid: Grid, background=0, monochrome=True):
    """Four-connected non-background components, with deterministic row order."""
    h, w = shape(grid)
    unseen = {(r, c) for r in range(h) for c in range(w) if grid[r][c] != background}
    found = []
    while unseen:
        seed = min(unseen)
        unseen.remove(seed)
        todo, cells = [seed], [seed]
        color = grid[seed[0]][seed[1]]
        while todo:
            r, c = todo.pop()
            for nxt in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                if nxt in unseen and (not monochrome or grid[nxt[0]][nxt[1]] == color):
                    unseen.remove(nxt)
                    todo.append(nxt)
                    cells.append(nxt)
        found.append(tuple(sorted(cells)))
    return tuple(found)
