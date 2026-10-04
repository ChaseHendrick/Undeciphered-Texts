"""What other people measured on the 1939 challenge, checked again. Not a reading.

Column 14 of the 14 by 14 grid is the column Nick Pelling marked in 2014.
The test asks only whether the rare cells sit there, and whether deleting
that column makes the remaining counts closer to English. No letter string
is stored.
"""

from __future__ import annotations

import random
from collections import Counter
from math import comb

from engine.dagapeyeff_swarm import ENGLISH_25, best_chi_square, challenge_pairs

_SEED = 20261004
_DRAWS = 200
_LEGAL_ROWS = "67890"
_LEGAL_COLUMNS = "12345"


def _hypergeometric_at_least(population: int, marked: int, draw: int, observed: int) -> float:
    denom = comb(population, draw)
    total = 0
    for count in range(observed, min(marked, draw) + 1):
        total += comb(marked, count) * comb(population - marked, draw - count)
    return total / denom


def column_report() -> dict:
    pairs = challenge_pairs()
    counts = Counter(pairs)
    legal = [row + column for row in _LEGAL_ROWS for column in _LEGAL_COLUMNS]
    missing = tuple(pair for pair in legal if pair not in counts)
    total = len(pairs)
    ic = sum(count * (count - 1) for count in counts.values()) / (total * (total - 1))

    def cells(limit: int) -> int:
        return sum(count for count in counts.values() if count <= limit)

    def in_last_column(limit: int) -> int:
        return sum(1 for index, pair in enumerate(pairs) if counts[pair] <= limit and index % 14 == 13)

    singletons = cells(1)
    up_to_two = cells(2)
    drop_chi = []
    for column in range(14):
        kept = tuple(pair for index, pair in enumerate(pairs) if index % 14 != column)
        drop_chi.append(round(best_chi_square(kept), 2))
    drawn = random.Random(_SEED)
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    english = []
    for _ in range(_DRAWS):
        letters = tuple(drawn.choices(alphabet, weights=ENGLISH_25, k=182))
        english.append(best_chi_square(letters))
    friendliest = min(drop_chi)
    return {
        "solved": False,
        "claimed_plaintext": None,
        "pairs": total,
        "distinct": len(counts),
        "missing": missing,
        "ic": round(ic, 6),
        "singletons": singletons,
        "singletons_in_column_14": in_last_column(1),
        "p_singletons": _hypergeometric_at_least(196, singletons, 14, in_last_column(1)),
        "cells_at_most_two": up_to_two,
        "at_most_two_in_column_14": in_last_column(2),
        "p_at_most_two": _hypergeometric_at_least(196, up_to_two, 14, in_last_column(2)),
        "pelling_cells": counts["04"] + counts["92"],
        "pelling_in_column_14": sum(1 for index, pair in enumerate(pairs) if pair in {"04", "92"} and index % 14 == 13),
        "drop_chi": tuple(drop_chi),
        "worst_drop_column": drop_chi.index(max(drop_chi)),
        "worst_drop_chi": max(drop_chi),
        "best_drop_chi": friendliest,
        "english_draws": _DRAWS,
        "english_as_flat": sum(score >= friendliest for score in english),
        "scope": (
            "Column 14 was named in 2014, so the column is not chosen by this search. "
            "The frequency score cannot be moved by a later transposition. "
            "No letter string is stored."
        ),
    }
