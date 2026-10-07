"""Latin under a 14 by 14 turning grille with a letter key: power only. Not a reading.

engine.dagapeyeff_grillec recovers planted grilles with the letter key given
but none with grille and key both unknown, settling at 13 to 20 of 49 holes.
This pass asks two questions under the Latin quadgram model of
engine.dagapeyeff_latin, on planted held-out Latin.

1. How right must the key be? The grille is annealed with the key held fixed
   at the true key, and at keys with about 15 and 30 percent of cells spoiled.
2. Does re-solving the key at every grille move help? Each grille move is
   scored by a greedy key climb under the quadgram model
   (engine/dagapeyeff_latingrille.c), then grille and key are polished
   together. A version that climbs the key on a letter-pair model is also run.

The cells are not searched: a search without power closes nothing. No letter
string is stored.
"""

from __future__ import annotations

import ctypes
import math
import os
import random
import shutil
import subprocess
import tempfile
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from pathlib import Path

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_columnar14c import frequency_key
from engine.dagapeyeff_foursquare import PLAIN
from engine.dagapeyeff_grille import ORBITS, agreement
from engine.dagapeyeff_grillec import encrypt
from engine.dagapeyeff_latin import _model, texts
from engine.dagapeyeff_latin14 import _tables

N = 196
_SOURCE = Path(__file__).resolve().parent / "dagapeyeff_latingrille.c"
_SEED = 20261107
_PLANTED = 4
SPOILED = (0.0, 0.15, 0.3)
_FIXED = (4, 2_000_000, 8.0)
_NESTED = (2, 60_000, 6.0)
_POLISH = (2_000_000, 6.0)
_I, _D = ctypes.c_int, ctypes.c_double


@lru_cache(maxsize=1)
def _kernel():
    compiler = shutil.which("cc") or shutil.which("gcc") or shutil.which("clang")
    if compiler is None:
        raise RuntimeError("a C compiler is needed to rerun the grille search")
    built = Path(tempfile.mkdtemp(prefix="latingrille-")) / "kernel.so"
    subprocess.run([compiler, "-O3", "-shared", "-fPIC", "-o", str(built), str(_SOURCE), "-lm"], check=True)
    lib = ctypes.CDLL(str(built))
    p_i, p_d = ctypes.POINTER(_I), ctypes.POINTER(_D)
    lib.grille_nested.restype = _D
    lib.grille_nested.argtypes = [p_i, p_d, p_i, ctypes.c_ulonglong, _I, _I, _D, p_i, p_i]
    lib.grille_nestq.restype = _D
    lib.grille_nestq.argtypes = [p_i, p_d, p_i, p_i, ctypes.c_ulonglong, _I, _I, _D, _I, p_i, p_i]
    lib.grille_polish.restype = _D
    lib.grille_polish.argtypes = [p_i, p_d, p_i, p_i, p_i, ctypes.c_ulonglong, _I, _D, _D, p_i, p_i]
    return lib


@lru_cache(maxsize=1)
def pair_table():
    """Latin letter-pair log probabilities, log P(b | a), on PLAIN indices."""
    text = texts()["train"]
    pairs = Counter(zip(text, text[1:]))
    singles = Counter(text[:-1])
    return (_D * 625)(*[math.log((pairs[(a, b)] + 0.5) / (singles[a] + 12.5)) for a in PLAIN for b in PLAIN])


def plant(rng: random.Random) -> dict:
    prose = texts()["held"]
    start = rng.randrange(len(prose) - N)
    text = prose[start:start + N]
    choice = [rng.randrange(4) for _ in range(ORBITS)]
    sub = list(range(25))
    rng.shuffle(sub)
    cells, origin = encrypt([sub[PLAIN.index(ch)] for ch in text], choice)
    return {"text": text, "choice": choice, "cells": cells, "origin": origin, "seed": rng.randrange(1 << 40)}


def true_key(job: dict) -> list[int]:
    key = [0] * 25
    for c, o in zip(job["cells"], job["origin"]):
        key[c] = PLAIN.index(job["text"][o])
    return key


def spoil(key: list[int], cells: list[int], share: float, rng: random.Random) -> list[int]:
    """Rotate the letters of random symbols until about `share` of the cells are wrong."""
    counts = Counter(cells)
    symbols = list(counts)
    rng.shuffle(symbols)
    chosen, covered = [], 0
    for symbol in symbols:
        if covered >= share * N:
            break
        chosen.append(symbol)
        covered += counts[symbol]
    key = key[:]
    if len(chosen) > 1:
        letters = [key[s] for s in chosen]
        for symbol, letter in zip(chosen, letters[1:] + letters[:1]):
            key[symbol] = letter
    return key


def _cells_right(job: dict, key: list[int]) -> float:
    return sum(PLAIN[key[c]] == job["text"][o] for c, o in zip(job["cells"], job["origin"])) / N


def fixed_search(job: dict, key: list[int], seed: int) -> tuple[float, list[int]]:
    """The grille alone, the key held fixed."""
    lib = _kernel()
    logp, letters = _tables()
    restarts, steps, temperature = _FIXED
    best = (-1e300, [])
    for r in range(restarts):
        start = [random.Random(seed + r).randrange(4) for _ in range(ORBITS)]
        choice, out_key = (_I * ORBITS)(), (_I * 25)()
        score = lib.grille_polish((_I * N)(*job["cells"]), logp, letters, (_I * ORBITS)(*start), (_I * 25)(*key),
                                  seed + r, steps, temperature, 0.0, choice, out_key)
        if score > best[0]:
            best = (score, list(choice))
    return best[0] / (N - 3), best[1]


def nested_search(cells: list[int], seed: int, model: str) -> dict:
    """Key re-solved at every grille move (quadgram or letter-pair), then a joint polish."""
    lib = _kernel()
    logp, letters = _tables()
    restarts, steps, temperature = _NESTED
    choice, key = (_I * ORBITS)(), (_I * 25)()
    start = (_I * 25)(*frequency_key(cells))
    if model == "quad":
        lib.grille_nestq((_I * N)(*cells), logp, letters, start, seed, restarts, steps, temperature, 2, choice, key)
    else:
        lib.grille_nested((_I * N)(*cells), pair_table(), start, seed, restarts, steps * 10, 3.0, choice, key)
    first = list(choice)
    out_choice, out_key = (_I * ORBITS)(), (_I * 25)()
    total = lib.grille_polish((_I * N)(*cells), logp, letters, choice, key, seed + 1, _POLISH[0], _POLISH[1], 0.5,
                              out_choice, out_key)
    return {"nested_choice": first, "per_letter": total / (N - 3), "choice": list(out_choice), "key": list(out_key)}


@frozen("dagapeyeff-latingrille")
def latingrille_report() -> dict:
    rng = random.Random(_SEED)
    _kernel(), _tables(), pair_table()
    planted = [plant(rng) for _ in range(_PLANTED)]
    fixed_jobs = [(job, share, spoil(true_key(job), job["cells"], share, rng), rng.randrange(1 << 40))
                  for job in planted for share in SPOILED]

    def run_fixed(item):
        job, share, key, seed = item
        score, choice = fixed_search(job, key, seed)
        return {"spoiled": share, "key_cells_right": round(_cells_right(job, key), 4),
                "found_per_letter": round(score, 4), "holes_right": agreement(choice, job["choice"])}

    def run_nested(item):
        job, model = item
        found = nested_search(job["cells"], job["seed"], model)
        return {"model": model,
                "true_per_letter": round(_model().score([ord(ch) - 65 for ch in job["text"]]) / (N - 3), 4),
                "found_per_letter": round(found["per_letter"], 4),
                "holes_after_nested": agreement(found["nested_choice"], job["choice"]),
                "holes_right": agreement(found["choice"], job["choice"])}

    with ThreadPoolExecutor(max_workers=os.cpu_count() or 1) as pool:
        fixed = list(pool.map(run_fixed, fixed_jobs))
        nested = list(pool.map(run_nested, [(job, model) for model in ("quad", "pair") for job in planted]))
    by_share = {}
    for row in fixed:
        cell = by_share.setdefault(str(row["spoiled"]), {"recovered": 0, "of": 0, "key_cells_right": []})
        cell["recovered"] += row["holes_right"] == ORBITS
        cell["of"] += 1
        cell["key_cells_right"].append(row["key_cells_right"])
    return {
        "solved": False, "claimed_plaintext": None, "cells_searched": False,
        "language": "Latin (UD_Latin-ITTB model, held-out tail planted)",
        "search": {"fixed": _FIXED, "nested": _NESTED, "polish": _POLISH},
        "fixed_key": fixed, "fixed_by_spoiled": by_share, "nested": nested,
        "nested_recovered": sum(row["holes_right"] == ORBITS for row in nested),
        "nested_holes_high": max(row["holes_right"] for row in nested),
    }
