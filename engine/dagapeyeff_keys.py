"""Column orders of the regrouped cells, against a matched shuffle. Not a reading.

The counts of regrouping 01432 already sit near English. A column order
would matter only if its best score beat the best shuffle of those same
cells, drawn the same number of times. No letter string is stored.
"""

from __future__ import annotations

import random
from engine.dagapeyeff_cache import frozen

from engine.dagapeyeff_order import _down_read, _grid, _mi, _prose, _row_read
from engine.dagapeyeff_regroup import regrouped_pairs

_DRAWS = 20000
_SEED = 20261004
_REPEATS = 20


@frozen("keys")
def key_report() -> dict:
    pairs = regrouped_pairs()
    grid = _grid(pairs)
    identity = list(range(14))
    drawn = random.Random(_SEED)
    best_row = _mi(_row_read(grid, identity))
    best_down = _mi(_down_read(grid, identity))
    for _ in range(_DRAWS):
        order = identity[:]
        drawn.shuffle(order)
        best_row = max(best_row, _mi(_row_read(grid, order)))
        best_down = max(best_down, _mi(_down_read(grid, order)))
    sample = pairs[:]
    drawn = random.Random(_SEED + 1)
    shuffle_max = 0.0
    for _ in range(_DRAWS):
        drawn.shuffle(sample)
        shuffle_max = max(shuffle_max, _mi(sample))
    repeats_as_high = 0
    best = max(best_row, best_down)
    for repeat in range(_REPEATS):
        sample = pairs[:]
        drawn = random.Random(_SEED + 100 + repeat)
        repeat_max = 0.0
        for _ in range(_DRAWS):
            drawn.shuffle(sample)
            repeat_max = max(repeat_max, _mi(sample))
        if repeat_max >= best:
            repeats_as_high += 1
    english = _mi(list(_prose("english.txt", len(pairs))))
    return {
        "solved": False,
        "claimed_plaintext": None,
        "reorder": "01432",
        "draws": _DRAWS,
        "repeats": _REPEATS,
        "best_row_mi": round(best_row, 4),
        "best_down_mi": round(best_down, 4),
        "shuffle_max_mi": round(shuffle_max, 4),
        "english_mi": round(english, 4),
        "one_sample_higher": best > shuffle_max,
        "repeats_as_high": repeats_as_high,
        "key_reaches_english": best >= english,
        "scope": (
            "One shuffle sample can sit under a searched maximum by chance. "
            "Repeated samples of the same size correct that. No letter string is stored."
        ),
    }
