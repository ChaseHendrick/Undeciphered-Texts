"""The aligned runs are not the only copies in their rows.

A run is three or more copies of one cell inside one row. An outside copy
is another copy of that same cell in the same row, not inside the run.
The alignment of two runs was already scored. This asks whether those
rows still hold two outside copies once a shuffle already has the
alignment. A vertical run is a different question. No letter string is
stored.
"""

from __future__ import annotations

import random
from collections import Counter, defaultdict

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_swarm import challenge_pairs

_SEED = 20261004
_DRAWS = 40000
_WIDTH = 14
_RUN = 3


def _runs(seq: list[str]) -> list[dict]:
    found = []
    for row in range(_WIDTH):
        line = seq[row * _WIDTH:(row + 1) * _WIDTH]
        column = 0
        while column < _WIDTH:
            end = column
            while end + 1 < _WIDTH and line[end + 1] == line[column]:
                end += 1
            length = end - column + 1
            if length >= _RUN:
                cell = line[column]
                outside_columns = [
                    index for index, item in enumerate(line)
                    if item == cell and not column <= index <= end
                ]
                found.append({
                    "cell": cell,
                    "row": row,
                    "column": column,
                    "length": length,
                    "outside": len(outside_columns),
                    "outside_columns": outside_columns,
                })
            column = end + 1
    return found


def _score(seq: list[str]) -> tuple[int, int, list[dict]]:
    runs = _runs(seq)
    if not runs:
        return 0, 0, runs
    by_column: dict[int, int] = defaultdict(int)
    for run in runs:
        by_column[run["column"]] += 1
    shared = max(by_column.values())
    columns = {column for column, count in by_column.items() if count == shared}
    chosen = [run for run in runs if run["column"] in columns]
    outside = min(run["outside"] for run in chosen)
    return shared, outside, runs


@frozen("outside")
def outside_report() -> dict:
    pairs = list(challenge_pairs())
    shared, outside, runs = _score(pairs)
    drawn = random.Random(_SEED)
    aligned = 0
    spare = 0
    for _ in range(_DRAWS):
        shuffled = pairs[:]
        drawn.shuffle(shuffled)
        shuffle_shared, shuffle_outside, _ignored = _score(shuffled)
        if shuffle_shared >= shared:
            aligned += 1
            if shuffle_outside >= outside:
                spare += 1
    places = []
    for run in runs:
        for column in run["outside_columns"]:
            places.append({"row": run["row"], "column": column, "cell": run["cell"]})
    return {
        "solved": False,
        "claimed_plaintext": None,
        "cells": [run["cell"] for run in runs],
        "rows": [run["row"] for run in runs],
        "columns": [run["column"] for run in runs],
        "lengths": [run["length"] for run in runs],
        "outside": outside,
        "places": places,
        "shared": shared,
        "draws": _DRAWS,
        "aligned": aligned,
        "spare": spare,
        "scope": (
            "Copies outside an aligned run are not a reading. "
            "No letter string is stored."
        ),
    }
