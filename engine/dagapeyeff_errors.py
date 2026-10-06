"""Could enciphering errors hide English in the cells? Not a reading.

D'Agapeyeff's own worked exercise has about four faults in 92 letters (89
pairs for 92 letters, AREA written as ARYA), so the challenge might carry
about eight. Two questions, each answered with held-out English and a keyed
Polybius square:

1. Counts. A one-to-one key keeps letter counts, and the cells' counts are
   unlike any real English window. Each error moves one count, so the fewest
   errors that turn a window's counts into the cells' is half the distance
   between the sorted count vectors. That is the best case for the errors.
   Random errors are also applied: a digit slip moves a letter to one of the
   eight cells sharing its row or column of the square; a free error to any
   other cell.
2. Search. Planted English with k digit slips is solved as a keyed square
   (engine/dagapeyeff_additive.c at period 1). The question is how many
   errors it takes before English scores as low as the cells.

No letter string is stored.
"""

from __future__ import annotations

import os
import random
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

import numpy as np

from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_additive import _kernel, _tables, anneal
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_foursquare import PLAIN, _HELD, _held, _model

_SEED = 20261010
_LETTERS = 196
_ERRORS = (0, 4, 8, 12, 16, 24, 32, 48)
_STRIDE = 7
_DRAWS = 4
_PLANTED = 3
_RESTARTS = 2
_STEPS = 300_000
_PROSE_FLOOR = -2.5


def sorted_counts(symbols) -> np.ndarray:
    counts = sorted(Counter(symbols).values(), reverse=True)
    return np.asarray(counts + [0] * (25 - len(counts)))


def fewest_errors(symbols, target: np.ndarray) -> int:
    """The fewest single-cell changes that give these symbols the target's counts, under any relabeling."""
    return int(np.abs(sorted_counts(symbols) - target).sum()) // 2


def slip(cell: int, rng: random.Random) -> int:
    """A wrong row digit or a wrong column digit: another cell in the same row or column."""
    row, column = divmod(cell, 5)
    if rng.random() < 0.5:
        return rng.choice([r for r in range(5) if r != row]) * 5 + column
    return row * 5 + rng.choice([c for c in range(5) if c != column])


def corrupt(cells: list[int], k: int, rng: random.Random, kind: str) -> list[int]:
    out = list(cells)
    for place in rng.sample(range(len(out)), k):
        out[place] = slip(out[place], rng) if kind == "slip" else rng.choice([c for c in range(25) if c != out[place]])
    return out


def _encipher(text: str, rng: random.Random) -> list[int]:
    square = list(range(25))
    rng.shuffle(square)
    where = {PLAIN[square[cell]]: cell for cell in range(25)}
    return [where[ch] for ch in text]


def count_check() -> dict:
    rng = random.Random(_SEED)
    target = sorted_counts(_cells())
    windows = []
    for name in _HELD:
        prose = _held(name)
        windows += [prose[s:s + _LETTERS] for s in range(0, len(prose) - _LETTERS, _STRIDE)]
    best_case = [fewest_errors(w, target) for w in windows]
    rows = []
    for kind in ("slip", "free"):
        for k in _ERRORS:
            if k == 0:
                continue
            distances = []
            for w in windows:
                cells = _encipher(w, rng)
                for _ in range(_DRAWS):
                    distances.append(fewest_errors(corrupt(cells, k, rng, kind), target))
            rows.append({
                "kind": kind,
                "errors": k,
                "draws": len(distances),
                "fewest_remaining": min(distances),
                "median_remaining": float(np.median(distances)),
                "reaching_cells": sum(x == 0 for x in distances),
            })
    return {
        "windows": len(windows),
        "best_case_fewest": min(best_case),
        "best_case_median": float(np.median(best_case)),
        "best_case_at_most_8": sum(x <= 8 for x in best_case),
        "random": rows,
    }


def _per_letter(text: str) -> float:
    return _model().score([ord(ch) - 65 for ch in text]) / (len(text) - 3)


@frozen("dagapeyeff-errors")
def errors_report() -> dict:
    rng = random.Random(_SEED + 1)
    jobs = []
    for k in _ERRORS:
        for trial in range(_PLANTED):
            prose = _held(_HELD[trial % len(_HELD)])
            while True:
                start = rng.randrange(len(prose) - _LETTERS)
                text = prose[start:start + _LETTERS]
                if _per_letter(text) >= _PROSE_FLOOR:
                    break
            cells = corrupt(_encipher(text, rng), k, rng, "slip")
            jobs.append((k, text, cells, rng.randrange(1 << 40)))
    cell_job = ("cells", None, _cells(), rng.randrange(1 << 40))
    _kernel()
    _tables()
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 1) as pool:
        results = list(pool.map(lambda job: anneal(job[2], 1, "both", job[3], _RESTARTS, _STEPS), jobs + [cell_job]))
    cells_score = round(results[-1][0], 4)
    planted = []
    for (k, text, _, _), (score, letters) in zip(jobs, results[:-1]):
        planted.append({
            "errors": k,
            "true_per_letter": round(_per_letter(text), 4),
            "found_per_letter": round(score, 4),
            "letters_right": round(sum(chr(65 + x) == ch for x, ch in zip(letters, text)) / _LETTERS, 4),
        })
    by_errors = {}
    for k in _ERRORS:
        rows = [row for row in planted if row["errors"] == k]
        by_errors[str(k)] = {
            "found_low": min(row["found_per_letter"] for row in rows),
            "found_high": max(row["found_per_letter"] for row in rows),
            "letters_right_low": min(row["letters_right"] for row in rows),
        }
    return {
        "solved": False,
        "claimed_plaintext": None,
        "search": {"restarts": _RESTARTS, "steps": _STEPS, "planted_per_count": _PLANTED},
        "counts": count_check(),
        "planted": planted,
        "by_errors": by_errors,
        "cells_per_letter": cells_score,
        "fewest_errors_at_cells_level": next(
            (k for k in _ERRORS if by_errors[str(k)]["found_low"] <= cells_score), None),
    }
