"""One repeated cell, versus several rare cells in one column. Not a reading.

The rare cells already share a column. This asks whether any single cell
does the same thing on its own, and whether the rows of those rare cells
are bunched once the column is given. No letter string is stored.
"""

from __future__ import annotations

import random
from collections import Counter
from itertools import combinations

from engine.dagapeyeff_swarm import challenge_pairs

_SEED = 20261004
_DRAWS = 20000
_WIDTHS = range(2, 29)
_WIDTH_DRAWS = 5000


def _symbol_pile(seq: list[str], width: int = 14) -> int:
    bags: dict[str, dict[int, int]] = {}
    best = 1
    for index, symbol in enumerate(seq):
        columns = bags.get(symbol)
        if columns is None:
            columns = bags[symbol] = {}
        column = index % width
        columns[column] = columns.get(column, 0) + 1
        if columns[column] > best:
            best = columns[column]
    return best


def _owner(seq: list[str], width: int = 14) -> tuple[int, str]:
    bags: dict[str, dict[int, int]] = {}
    best = 1
    name = seq[0]
    for index, symbol in enumerate(seq):
        columns = bags.get(symbol)
        if columns is None:
            columns = bags[symbol] = {}
        column = index % width
        columns[column] = columns.get(column, 0) + 1
        if columns[column] > best:
            best = columns[column]
            name = symbol
    return best, name


def _rare_pile(seq: list[str]) -> int:
    totals = Counter(seq)
    columns = [0] * 14
    for index, symbol in enumerate(seq):
        if totals[symbol] <= 2:
            columns[index % 14] += 1
    return max(columns)


def _max_adjacent(seq: list[str]) -> int:
    best = 0
    for column in range(14):
        run = 0
        previous = ""
        for row in range(14):
            symbol = seq[row * 14 + column]
            if symbol == previous:
                run += 1
                if run > best:
                    best = run
            else:
                previous = symbol
                run = 1
    return best


def _longest_run(rows: tuple[int, ...]) -> int:
    ordered = sorted(rows)
    best = current = 1
    for left, right in zip(ordered, ordered[1:]):
        if right == left + 1:
            current += 1
            best = max(best, current)
        else:
            current = 1
    return best


def symbol_report() -> dict:
    pairs = list(challenge_pairs())
    pile, owner = _owner(pairs)
    rare = _rare_pile(pairs)
    adjacent = _max_adjacent(pairs)
    totals = Counter(pairs)
    rare_rows = tuple(index // 14 for index, symbol in enumerate(pairs) if totals[symbol] <= 2)
    observed_run = _longest_run(rare_rows)
    as_bunched = sum(
        1 for choice in combinations(range(14), len(rare_rows)) if _longest_run(choice) >= observed_run
    )
    drawn = random.Random(_SEED)
    symbol_as_high = 0
    rare_as_high = 0
    adjacent_as_high = 0
    for _ in range(_DRAWS):
        shuffled = pairs[:]
        drawn.shuffle(shuffled)
        if _symbol_pile(shuffled) >= pile:
            symbol_as_high += 1
        if _rare_pile(shuffled) >= rare:
            rare_as_high += 1
        if _max_adjacent(shuffled) >= adjacent:
            adjacent_as_high += 1
    real_widths = {width: _symbol_pile(pairs, width) for width in _WIDTHS}
    width_tails = {width: 0 for width in _WIDTHS}
    drawn = random.Random(_SEED + 1)
    for _ in range(_WIDTH_DRAWS):
        shuffled = pairs[:]
        drawn.shuffle(shuffled)
        for width in _WIDTHS:
            if _symbol_pile(shuffled, width) >= real_widths[width]:
                width_tails[width] += 1
    closest = min(width_tails, key=width_tails.get)
    return {
        "solved": False,
        "claimed_plaintext": None,
        "trials": _DRAWS * 3 + _WIDTH_DRAWS * len(tuple(_WIDTHS)),
        "owner": owner,
        "owner_pile": pile,
        "owner_as_high": symbol_as_high,
        "rare_pile": rare,
        "rare_as_high": rare_as_high,
        "longest_vertical_run": adjacent,
        "vertical_as_long": adjacent_as_high,
        "draws": _DRAWS,
        "rare_rows": rare_rows,
        "row_run": observed_run,
        "row_subsets": 2002,
        "rows_as_bunched": as_bunched,
        "closest_width": closest,
        "closest_width_tail": width_tails[closest],
        "width_draws": _WIDTH_DRAWS,
        "scope": (
            "The luckiest symbol and the luckiest width are allowed to win. "
            "A meeting of several rare cells is not the same as one cell repeating. "
            "No letter string is stored."
        ),
    }
