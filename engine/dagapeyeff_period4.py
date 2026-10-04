"""Every period-4 shift on the 5 by 5 square. Not a reading.

Period 2 and period 3 were already exhausted. Period 4 is 390,625 keys.
The friendliest key is kept as a chi-square and a quadgram, not as letters.
Shuffled copies get the same free choice of key.
"""

from __future__ import annotations

import random
from functools import lru_cache

from engine.alphabet import letters_only, to_ints
from engine.dagapeyeff_add import _PROSE, _cells, _chi, _mean_quadgram, _phases
from engine.language import get_model

_SEED = 20261004
_NULL = 40
_KEYS = 25 ** 4


def _best(seq: list[int]) -> tuple[float, tuple[int, ...], list[int]]:
    first_set, second_set, third_set, fourth_set = _phases(seq, 4)
    best = float("inf")
    best_key: tuple[int, ...] = ()
    best_counts: list[int] = []
    for i, first in enumerate(first_set):
        for j, second in enumerate(second_set):
            partial = [first[bin_] + second[bin_] for bin_ in range(25)]
            for k, third in enumerate(third_set):
                partial_three = [partial[bin_] + third[bin_] for bin_ in range(25)]
                for n, fourth in enumerate(fourth_set):
                    counts = [partial_three[bin_] + fourth[bin_] for bin_ in range(25)]
                    score = _chi(counts)
                    if score < best:
                        best = score
                        best_key = (i, j, k, n)
                        best_counts = counts
    return best, best_key, best_counts


@lru_cache(maxsize=1)
def period4_report() -> dict:
    cells = _cells()
    chi, key, counts = _best(cells)
    quad = _mean_quadgram(cells, key, counts)
    drawn = random.Random(_SEED)
    chi_as_low = 0
    quad_as_high = 0
    for _ in range(_NULL):
        shuffled = cells[:]
        drawn.shuffle(shuffled)
        null_chi, null_key, null_counts = _best(shuffled)
        if null_chi <= chi + 1e-9:
            chi_as_low += 1
        if _mean_quadgram(shuffled, null_key, null_counts) >= quad - 1e-12:
            quad_as_high += 1
    prose = to_ints(letters_only(_PROSE))
    prose_quad = get_model().score(prose) / (len(prose) - 3)
    return {
        "solved": False,
        "claimed_plaintext": None,
        "keys": _KEYS,
        "null_texts": _NULL,
        "trials": _KEYS * (1 + _NULL),
        "chi": round(chi, 2),
        "quadgram": round(quad, 4),
        "prose_quadgram": round(prose_quad, 4),
        "chi_as_low": chi_as_low,
        "quad_as_high": quad_as_high,
        "reaches_prose": quad >= prose_quad,
        "scope": (
            "A period-4 shift can paint English-looking counts. "
            "The quadgram has to reach prose, and shuffled cells get the same search. "
            "No letter string is stored."
        ),
    }
