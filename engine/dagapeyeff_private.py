"""Symbols that never leave one column of the 1939 grid. Not a reading.

A symbol is private to a column when every copy of it sits in that column.
The score is the number of cells those private symbols account for.
The luckiest column is allowed to win. No letter string is stored.
"""

from __future__ import annotations

import random
from collections import defaultdict

from engine.dagapeyeff_swarm import challenge_pairs

_SEED = 20261004
_DRAWS = 20000
_WIDTH = 14


def private_columns(seq: list[str], width: int = _WIDTH) -> list[tuple[str, int, int]]:
    columns: dict[str, set[int]] = defaultdict(set)
    counts: dict[str, int] = defaultdict(int)
    for index, symbol in enumerate(seq):
        columns[symbol].add(index % width)
        counts[symbol] += 1
    found = []
    for symbol, used in columns.items():
        if len(used) == 1:
            column = next(iter(used))
            found.append((symbol, column, counts[symbol]))
    found.sort(key=lambda item: (-item[2], item[0]))
    return found


def private_mass(seq: list[str], width: int = _WIDTH) -> int:
    mass = [0] * width
    for _symbol, column, count in private_columns(seq, width):
        mass[column] += count
    return max(mass)


def private_report() -> dict:
    pairs = list(challenge_pairs())
    found = private_columns(pairs)
    mass = [0] * _WIDTH
    for _symbol, column, count in found:
        mass[column] += count
    positions = {}
    for index, symbol in enumerate(pairs):
        if any(symbol == item[0] for item in found):
            positions.setdefault(symbol, []).append(index)
    drawn = random.Random(_SEED)
    observed = max(mass)
    as_high = 0
    for _ in range(_DRAWS):
        shuffled = pairs[:]
        drawn.shuffle(shuffled)
        if private_mass(shuffled) >= observed:
            as_high += 1
    moduli = []
    for symbol, _column, _count in found:
        for index in positions[symbol]:
            moduli.append((index % _WIDTH, index % 7))
    return {
        "solved": False,
        "claimed_plaintext": None,
        "trials": _DRAWS,
        "private": tuple(found),
        "mass_by_column": tuple(mass),
        "private_mass": observed,
        "as_high": as_high,
        "draws": _DRAWS,
        "all_in_column_13": all(column == 13 for _symbol, column, _count in found),
        "all_mod_14_is_13": all(item[0] == 13 for item in moduli),
        "all_mod_7_is_6": all(item[1] == 6 for item in moduli),
        "scope": (
            "A symbol that never leaves one column is a measured fact. "
            "It is not a word, and a period of 7 is only the coarser view of the same column. "
            "No letter string is stored."
        ),
    }
