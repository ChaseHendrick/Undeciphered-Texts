"""Periodic independent alphabets, excluded by per-phase letter counts. Not a reading.

A periodic substitution with independent alphabets enciphers the letters at
places i, i+p, i+2p and so on with one one-to-one key, and each of the p
phases with its own. Proposition 2 of the D'Agapeyeff manuscript then applies
phase by phase: the fewest errors that turn a text into the cells, under any
such keys, is the sum over phases of half the distance between the sorted
counts of the text's phase and the cells'. This probe computes it for held-out
English windows at periods 2 to 14, and the same for shuffled cells as a
calibration of how much of the distance comes from the cells' overall counts.
No transposition is assumed before the substitution.

No letter string is stored.
"""

from __future__ import annotations

import random

import numpy as np

from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_errors import fewest_errors, sorted_counts
from engine.dagapeyeff_foursquare import _HELD, _held

_SEED = 20261020
_LETTERS = 196
_STRIDE = 23
_SHUFFLES = 5
PERIODS = (2, 3, 4, 5, 6, 7, 14)


def phase_errors(text, targets: list, period: int) -> int:
    return sum(fewest_errors(text[f::period], targets[f]) for f in range(period))


@frozen("dagapeyeff-phases")
def phases_report() -> dict:
    rng = random.Random(_SEED)
    cells = _cells()
    windows = [prose[s:s + _LETTERS] for prose in map(_held, _HELD)
               for s in range(0, len(prose) - _LETTERS, _STRIDE)]
    shuffles = [rng.sample(cells, len(cells)) for _ in range(_SHUFFLES)]
    rows = []
    for period in PERIODS:
        targets = [sorted_counts(cells[f::period]) for f in range(period)]
        errors = [phase_errors(w, targets, period) for w in windows]
        shuffled = []
        for mixed in shuffles:
            mixed_targets = [sorted_counts(mixed[f::period]) for f in range(period)]
            shuffled.append(min(phase_errors(w, mixed_targets, period) for w in windows))
        rows.append({"period": period, "fewest": min(errors), "median": float(np.median(errors)),
                     "within_8": sum(x <= 8 for x in errors), "shuffled_cells_fewest": shuffled})
    return {"solved": False, "claimed_plaintext": None, "windows": len(windows), "rows": rows}
