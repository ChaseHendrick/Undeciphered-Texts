"""Latin under double columnar transposition with a letter key: power only. Not a reading.

engine.dagapeyeff_double closed double transposition only to width 6, with a
score no letter key can change whose power was shown on English and German.
This pass anneals both column orders and the letter key together under the
Latin quadgram model of engine.dagapeyeff_latin
(engine/dagapeyeff_latindouble.c), and measures its power on planted
held-out Latin at growing sizes. A planted text counts as recovered when at
least 90 percent of its cells get their true letter and the found score is at
least the true text's less 0.1 a letter, so a right key under wrong orders is
not counted. The cells are not searched: power is shown only at small sizes,
which the key-invariant search of engine.dagapeyeff_double already covers.
No letter string is stored.
"""

from __future__ import annotations

import ctypes
import os
import random
import shutil
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from pathlib import Path

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_columnar14c import frequency_key
from engine.dagapeyeff_foursquare import PLAIN
from engine.dagapeyeff_latin import _model, texts
from engine.dagapeyeff_latin14 import _tables

N = 196
_SOURCE = Path(__file__).resolve().parent / "dagapeyeff_latindouble.c"
_SEED = 20261109
SIZES = ((4, 5), (5, 7), (6, 8), (7, 9), (9, 11))
_PER_SIZE = 3
_RESTARTS = 4
_STEPS = 8_000_000
_TEMPERATURE = 12.0
_KEY_SHARE = 0.5
_RECOVERED = 0.9
_SCORE_SLACK = 0.1
_I = ctypes.c_int


@lru_cache(maxsize=1)
def _kernel():
    compiler = shutil.which("cc") or shutil.which("gcc") or shutil.which("clang")
    if compiler is None:
        raise RuntimeError("a C compiler is needed to rerun the double transposition search")
    built = Path(tempfile.mkdtemp(prefix="latindouble-")) / "kernel.so"
    subprocess.run([compiler, "-O3", "-shared", "-fPIC", "-o", str(built), str(_SOURCE), "-lm"], check=True)
    lib = ctypes.CDLL(str(built))
    lib.dt_anneal.restype = ctypes.c_double
    lib.dt_anneal.argtypes = [ctypes.POINTER(_I), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(_I),
                              ctypes.POINTER(_I), _I, _I, ctypes.c_ulonglong, _I, _I, ctypes.c_double,
                              ctypes.c_double] + [ctypes.POINTER(_I)] * 4
    return lib


def read_map(width: int, slot: list[int]) -> list[int]:
    """Written position of each read-out symbol; slot[c] is the place column c is read in."""
    rows, rem = -(-N // width), N % width
    inverse = [0] * width
    for column in range(width):
        inverse[slot[column]] = column
    out = []
    for place in range(width):
        column = inverse[place]
        out += [r * width + column for r in range(rows if rem == 0 or column < rem else rows - 1)]
    return out


def encrypt(symbols: list[int], s1: list[int], w1: int, s2: list[int], w2: int) -> tuple[list[int], list[int]]:
    m1, m2 = read_map(w1, s1), read_map(w2, s2)
    origin = [m1[m2[i]] for i in range(N)]
    return [symbols[o] for o in origin], origin


def anneal(cells: list[int], w1: int, w2: int, seed: int) -> tuple[float, list[int]]:
    logp, letters = _tables()
    key = (_I * 25)()
    total = _kernel().dt_anneal((_I * N)(*cells), logp, letters, (_I * 25)(*frequency_key(cells)), w1, w2, seed,
                                _RESTARTS, _STEPS, _TEMPERATURE, _KEY_SHARE, (_I * 32)(), (_I * 32)(), key,
                                (_I * N)())
    return total / (N - 3), list(key)


@frozen("dagapeyeff-latindouble")
def latindouble_report() -> dict:
    rng = random.Random(_SEED)
    jobs = []
    for w1, w2 in SIZES:
        for _ in range(_PER_SIZE):
            prose = texts()["held"]
            start = rng.randrange(len(prose) - N)
            text = prose[start:start + N]
            s1, s2, sub = list(range(w1)), list(range(w2)), list(range(25))
            rng.shuffle(s1), rng.shuffle(s2), rng.shuffle(sub)
            cells, origin = encrypt([sub[PLAIN.index(ch)] for ch in text], s1, w1, s2, w2)
            jobs.append({"w1": w1, "w2": w2, "text": text, "cells": cells, "origin": origin,
                         "seed": rng.randrange(1 << 40)})
    _kernel(), _tables()
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 1) as pool:
        found = list(pool.map(lambda job: anneal(job["cells"], job["w1"], job["w2"], job["seed"]), jobs))
    rows = []
    for job, (score, key) in zip(jobs, found):
        right = sum(PLAIN[key[c]] == job["text"][o] for c, o in zip(job["cells"], job["origin"])) / N
        rows.append({"widths": [job["w1"], job["w2"]],
                     "true_per_letter": round(_model().score([ord(ch) - 65 for ch in job["text"]]) / (N - 3), 4),
                     "found_per_letter": round(score, 4), "cells_right": round(right, 4)})
        rows[-1]["recovered"] = right >= _RECOVERED and score >= rows[-1]["true_per_letter"] - _SCORE_SLACK
    by_size = {}
    for row in rows:
        cell = by_size.setdefault(f"{row['widths'][0]}x{row['widths'][1]}", {"recovered": 0, "of": 0})
        cell["recovered"] += row["recovered"]
        cell["of"] += 1
    return {"solved": False, "claimed_plaintext": None, "cells_searched": False,
            "language": "Latin (UD_Latin-ITTB model, held-out tail planted)",
            "search": {"restarts": _RESTARTS, "steps": _STEPS, "temperature": _TEMPERATURE, "key_share": _KEY_SHARE},
            "rows": rows, "by_size": by_size}
