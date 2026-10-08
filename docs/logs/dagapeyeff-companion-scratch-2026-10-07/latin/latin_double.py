"""Latin under double columnar transposition with a letter key. Not a reading.

The Undeciphered-Texts engine closed Latin under a single columnar key at
widths 2 to 15, but double transposition was only screened with a
key-invariant score whose power was shown on English and German, and only to
width 6. This pass anneals both column orders and the letter key together
under the Latin quadgram model of engine.dagapeyeff_latin (Thomas Aquinas,
first 90 percent), with planted held-out Latin for power and shuffled cells
as the control. No letter string is stored.

Needs a clone of github.com/ChaseHendrick/Undeciphered-Texts; set
UNDECIPHERED_TEXTS to its path (default: ../chasehendrick/undeciphered-texts).
"""

from __future__ import annotations

import ctypes
import os
import random
import shutil
import subprocess
import sys
import tempfile
from functools import lru_cache
from pathlib import Path

_ROOT = Path(os.environ.get("UNDECIPHERED_TEXTS",
                            Path(__file__).resolve().parents[2] / "chasehendrick" / "undeciphered-texts"))
sys.path.insert(0, str(_ROOT))

from engine.dagapeyeff_add import _cells  # noqa: E402
from engine.dagapeyeff_columnar import _regrouped_cells  # noqa: E402
from engine.dagapeyeff_foursquare import PLAIN  # noqa: E402
from engine.dagapeyeff_latin import _model, texts  # noqa: E402
from engine.dagapeyeff_latin14 import _tables, frequency_key  # noqa: E402

N = 196
_SOURCE = Path(__file__).resolve().parent / "latin_double.c"


@lru_cache(maxsize=1)
def kernel():
    compiler = shutil.which("cc") or shutil.which("gcc")
    out = Path(tempfile.gettempdir()) / f"latin_double_{os.getpid()}.so"
    subprocess.run([compiler, "-O3", "-march=native", "-shared", "-fPIC", "-o", str(out), str(_SOURCE), "-lm"],
                   check=True)
    lib = ctypes.CDLL(str(out))
    lib.dt_anneal.restype = ctypes.c_double
    lib.dt_anneal.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_double),
                              ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.c_int,
                              ctypes.c_int, ctypes.c_ulonglong, ctypes.c_int, ctypes.c_int, ctypes.c_double,
                              ctypes.c_double] + [ctypes.POINTER(ctypes.c_int)] * 4
    return lib


def read_map(width: int, slot: list[int]) -> list[int]:
    rows, rem = -(-N // width), N % width
    inv = [0] * width
    for column in range(width):
        inv[slot[column]] = column
    src = []
    for j in range(width):
        column = inv[j]
        length = rows if rem == 0 or column < rem else rows - 1
        src += [r * width + column for r in range(length)]
    return src


def encrypt(symbols: list[int], s1: list[int], w1: int, s2: list[int], w2: int) -> tuple[list[int], list[int]]:
    m1, m2 = read_map(w1, s1), read_map(w2, s2)
    origin = [m1[m2[i]] for i in range(N)]
    return [symbols[o] for o in origin], origin


def anneal(cells: list[int], w1: int, w2: int, seed: int, restarts: int, steps: int,
           temperature: float = 12.0, key_share: float = 0.5) -> tuple[float, list[int]]:
    logp, letters = _tables()
    ints = ctypes.c_int
    key = (ints * 25)()
    total = kernel().dt_anneal((ints * N)(*cells), logp, letters, (ints * 25)(*frequency_key(cells)), w1, w2,
                               seed, restarts, steps, temperature, key_share, (ints * 32)(), (ints * 32)(), key,
                               (ints * N)())
    return total / (N - 3), list(key)


def plant(rng: random.Random, w1: int, w2: int, source: str, errors: int) -> dict:
    prose = texts()[source]
    start = rng.randrange(len(prose) - N)
    text = prose[start:start + N]
    s1, s2, sub = list(range(w1)), list(range(w2)), list(range(25))
    rng.shuffle(s1), rng.shuffle(s2), rng.shuffle(sub)
    cells, origin = encrypt([sub[PLAIN.index(ch)] for ch in text], s1, w1, s2, w2)
    for _ in range(errors):
        cells[rng.randrange(N)] = rng.randrange(25)
    return {"text": text, "cells": cells, "origin": origin, "seed": rng.randrange(1 << 40)}


def cells_right(job: dict, key: list[int]) -> float:
    return sum(PLAIN[key[c]] == job["text"][o] for c, o in zip(job["cells"], job["origin"])) / N


def per_letter(text: str) -> float:
    return _model().score([ord(ch) - 65 for ch in text]) / (N - 3)


def printed() -> dict[str, list[int]]:
    return {"cells": _cells(), "regrouped": _regrouped_cells()}


def _bind_phases(lib) -> None:
    p_int, p_dbl = ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_double)
    lib.dt_orders.restype = ctypes.c_double
    lib.dt_orders.argtypes = [p_int, ctypes.c_int, ctypes.c_int, ctypes.c_ulonglong, ctypes.c_int, ctypes.c_int,
                              ctypes.c_double, ctypes.c_double, p_int, p_int]
    lib.dt_key.restype = ctypes.c_double
    lib.dt_key.argtypes = [p_int, p_dbl, p_int, p_int, ctypes.c_int, ctypes.c_int, p_int, p_int,
                           ctypes.c_ulonglong, ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_double,
                           p_int, p_int, p_int]


def orders(cells: list[int], w1: int, w2: int, seed: int, restarts: int, steps: int, temperature: float = 2.0,
           tri: float = 1.0) -> tuple[float, list[int], list[int]]:
    """Phase one: both read orders under a score no letter key can change."""
    lib = kernel()
    _bind_phases(lib)
    ints = ctypes.c_int
    o1, o2 = (ints * 32)(), (ints * 32)()
    best = lib.dt_orders((ints * N)(*cells), w1, w2, seed, restarts, steps, temperature, tri, o1, o2)
    return best, list(o1)[:w1], list(o2)[:w2]


def solve_key(cells: list[int], w1: int, w2: int, o1: list[int], o2: list[int], seed: int, restarts: int,
              steps: int, temperature: float = 8.0, polish: float = 0.2) -> tuple[float, list[int]]:
    """Phase two: the letter key under the Latin model from the phase-one orders, with a joint polish."""
    lib = kernel()
    _bind_phases(lib)
    logp, letters = _tables()
    ints = ctypes.c_int
    key = (ints * 25)()
    total = lib.dt_key((ints * N)(*cells), logp, letters, (ints * 25)(*frequency_key(cells)), w1, w2,
                       (ints * 32)(*o1), (ints * 32)(*o2), seed, restarts, steps, temperature, polish,
                       (ints * 32)(), (ints * 32)(), key)
    return total / (N - 3), list(key)


def two_phase(cells: list[int], w1: int, w2: int, seed: int, order_restarts: int = 8, order_steps: int = 2_000_000,
              key_restarts: int = 4, key_steps: int = 2_000_000) -> tuple[float, list[int], float]:
    found, o1, o2 = orders(cells, w1, w2, seed, order_restarts, order_steps)
    score, key = solve_key(cells, w1, w2, o1, o2, seed + 1, key_restarts, key_steps)
    return score, key, found
