"""The 13 common symbols look uniform. Not a reading.

Outside the five rare symbols, every cell is one of 13 symbols, with counts
20, 17, 17, 17, 17, 16, 15, 14, 12, 12, 11, 11 and 9. Those counts are close
to what 188 draws from 13 equally likely symbols give. A one-to-one
substitution of a real text keeps its letters' skew: in English the most
common letter is about three times as common as the thirteenth.

The test takes the 13 most common symbols of a text, and asks how far their
counts are from equal, as a chi-square on 12 degrees of freedom. The cells
are compared with every fourth 196-letter window of the public training
file, and with 20,000 draws of 188 symbols from 13 equally likely ones. A
transposition cannot change counts. No letter string is stored.
"""

from __future__ import annotations

import random
from collections import Counter
from pathlib import Path

import numpy as np

from engine.alphabet import letters_only
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_swarm import challenge_pairs

_PUBLIC = Path(__file__).resolve().parent / "data" / "neural_train_public.txt"
_WIDTH = 196
_STRIDE = 4
_COMMON = 13
_DRAWS = 20000
_SEED = 20261018


def top_flatness(counts: list[int] | np.ndarray) -> float:
    """Chi-square of the 13 largest counts against their own mean."""
    top = np.sort(np.asarray(counts, dtype=np.float64))[::-1][:_COMMON]
    mean = top.mean()
    return float(((top - mean) ** 2 / mean).sum())


@frozen("dagapeyeff-body")
def body_report() -> dict:
    cells = challenge_pairs()
    cell_counts = sorted(Counter(cells).values(), reverse=True)
    cell_flat = top_flatness(cell_counts)
    text = letters_only(_PUBLIC.read_text(encoding="utf-8")).replace("J", "I")
    ints = np.frombuffer(text.encode("ascii"), dtype=np.uint8).astype(np.int64) - 65
    starts = np.arange(0, len(ints) - _WIDTH + 1, _STRIDE)
    counts = np.zeros((len(starts), 26), dtype=np.int64)
    for letter in range(26):
        running = np.concatenate([[0], np.cumsum(ints == letter)])
        counts[:, letter] = running[starts + _WIDTH] - running[starts]
    top = -np.sort(-counts, axis=1)[:, :_COMMON].astype(np.float64)
    mean = top.mean(axis=1, keepdims=True)
    window_flat = ((top - mean) ** 2 / mean).sum(axis=1)
    drawn = random.Random(_SEED)
    uniform = []
    for _ in range(_DRAWS):
        sample = Counter(drawn.randrange(_COMMON) for _ in range(sum(cell_counts[:_COMMON])))
        uniform.append(top_flatness(list(sample.values())))
    uniform = np.asarray(uniform)
    return {
        "solved": False,
        "claimed_plaintext": None,
        "common_counts": cell_counts[:_COMMON],
        "cells_top13_chi": round(cell_flat, 2),
        "windows": int(len(starts)),
        "windows_as_flat": int((window_flat <= cell_flat).sum()),
        "window_top13_chi_min": round(float(window_flat.min()), 2),
        "window_top13_chi_median": round(float(np.median(window_flat)), 2),
        "uniform_draws": _DRAWS,
        "uniform_as_flat_or_flatter": int((uniform <= cell_flat).sum()),
        "uniform_median": round(float(np.median(uniform)), 2),
        "scope": (
            "The common body of the cells is as flat as typical draws of 13 equally likely symbols. About "
            "1 real prose window in 2,500 is that flat. A transposition cannot change counts. Not a reading. "
            "No letter string is stored."
        ),
    }
