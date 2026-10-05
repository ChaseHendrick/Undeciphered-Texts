"""Two copies outside the aligned runs, with the rare cells held still.

Cells that appear at most three times keep their seats. The other cells are
shuffled. Among the shuffles that already have two runs in one starting
column, the score is the smallest number of further copies of that cell in
the same row. One further copy is the wider score. Two is the observed
score. The contact with a rare cell is counted on the same draws so the
two events are not mistaken for each other. No letter string is stored.
"""

from __future__ import annotations

import random
from collections import Counter

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_contact import _band, _rare
from engine.dagapeyeff_outside import _score
from engine.dagapeyeff_swarm import challenge_pairs

_SEED = 20261004
_DRAWS = 20000
_RUN = 3


@frozen("extras")
def extras_report() -> dict:
    pairs = list(challenge_pairs())
    rare = _rare(pairs)
    shared, outside, _runs = _score(pairs)
    shared_touch, touched, _ignored = _band(pairs, rare)
    low = sorted(rare)
    pinned = {index for index, cell in enumerate(pairs) if cell in rare}
    free = [index for index in range(len(pairs)) if index not in pinned]
    seen = random.Random(_SEED)
    aligned = 0
    at_least_one = 0
    at_least_two = 0
    also_touching = 0
    different_cells = 0
    exact_length = 0
    close_rows = 0
    for _ in range(_DRAWS):
        shuffled = pairs[:]
        bag = [shuffled[index] for index in free]
        seen.shuffle(bag)
        for index, cell in zip(free, bag):
            shuffled[index] = cell
        shuffle_shared, shuffle_outside, runs = _score(shuffled)
        if shuffle_shared < shared:
            continue
        aligned += 1
        if shuffle_outside >= 1:
            at_least_one += 1
        columns = {
            run["column"] for run in runs
            if sum(item["column"] == run["column"] for item in runs) == shuffle_shared
        }
        chosen = [run for run in runs if run["column"] in columns]
        if len({run["cell"] for run in chosen}) >= 2:
            different_cells += 1
        if chosen and all(run["length"] == _RUN for run in chosen):
            exact_length += 1
        rows = sorted({run["row"] for run in chosen})
        if len(rows) >= 2 and min(b - a for a, b in zip(rows, rows[1:])) <= 4:
            close_rows += 1
        if shuffle_outside >= outside:
            at_least_two += 1
            touch_shared, touch_count, _band_runs = _band(shuffled, rare)
            if touch_shared >= shared_touch and touch_count >= touched:
                also_touching += 1
    one_rate = at_least_one / aligned if aligned else 1.0
    two_rate = at_least_two / aligned if aligned else 1.0
    return {
        "solved": False,
        "claimed_plaintext": None,
        "pinned": len(pinned),
        "low": low,
        "outside": outside,
        "draws": _DRAWS,
        "aligned": aligned,
        "at_least_one": at_least_one,
        "at_least_two": at_least_two,
        "also_touching": also_touching,
        "different_cells": different_cells,
        "exact_length": exact_length,
        "close_rows": close_rows,
        "allowed": aligned > 0 and two_rate < 0.05 and one_rate >= 0.05 and also_touching == 0,
        "scope": "Two copies outside an aligned run are not a reading. No letter string is stored.",
    }
