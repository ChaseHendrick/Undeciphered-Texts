"""Splitting an overloaded 1939 cell into two labels. Not a reading.

The substitution solver now refuses an order that a shuffle can match.
This pass asks a different question: if one crowded cell is really two
letters sharing a label, does giving those occurrences two labels create
prose-like dependence? The same split search on shuffled cells is the
control. No letter string is stored.
"""

from __future__ import annotations

import random
from collections import Counter

from engine.dagapeyeff_order import _prose
from engine.dagapeyeff_swarm import challenge_pairs
from engine.stats import successive_information

_SEED = 20261004
_SPLITS = 5000
_NULL = 20
_NULL_SPLITS = 1000
_CELLS = ("91", "75", "81")


def _apply(pairs: list[str], target: str, bits: int) -> list[str]:
    out = []
    seen = 0
    for symbol in pairs:
        if symbol != target:
            out.append(symbol)
            continue
        out.append(target + ("a" if (bits >> seen) & 1 else "b"))
        seen += 1
    return out


def _best_split(pairs: list[str], target: str, splits: int, drawn: random.Random) -> float:
    count = sum(symbol == target for symbol in pairs)
    if count < 2:
        return successive_information(pairs)
    span = (1 << count) - 1
    best = 0.0
    for _ in range(splits):
        bits = drawn.randrange(1, span)
        best = max(best, successive_information(_apply(pairs, target, bits)))
    return best


def split_report() -> dict:
    pairs = list(challenge_pairs())
    counts = Counter(pairs)
    drawn = random.Random(_SEED)
    best = {}
    for cell in _CELLS:
        best[cell] = _best_split(pairs, cell, _SPLITS, drawn)
    winner = max(best, key=best.get)
    observed = best[winner]
    null_as_high = 0
    for _ in range(_NULL):
        shuffled = pairs[:]
        drawn.shuffle(shuffled)
        trial = max(_best_split(shuffled, cell, _NULL_SPLITS, drawn) for cell in _CELLS)
        if trial >= observed - 1e-15:
            null_as_high += 1
    english = successive_information(_prose("english.txt", len(pairs)))
    return {
        "solved": False,
        "claimed_plaintext": None,
        "trials": _SPLITS * len(_CELLS) + _NULL * _NULL_SPLITS * len(_CELLS),
        "cells": {cell: {"count": counts[cell], "best_mi": round(best[cell], 4)} for cell in _CELLS},
        "best_cell": winner,
        "best_mi": round(observed, 4),
        "null_texts": _NULL,
        "null_as_high": null_as_high,
        "english_mi": round(english, 4),
        "scope": (
            "Splitting one crowded cell is not a reading unless the dependence "
            "beats both a shuffled split and same-length prose. No letter string is stored."
        ),
    }
