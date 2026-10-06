"""Four-square with all squares keyed, and two-square: power only. Not a reading.

The four-square side count excludes only standard plain squares
(engine.dagapeyeff_fskeyed), and engine.dagapeyeff_foursquare searched only
those. This probe anneals all four squares (engine/dagapeyeff_keyedsquares.c,
with the move set of Colossus's two-square solver) on planted held-out English:
two-square behind an unknown Polybius labelling, and four-square with all four
squares keyed. The cells are searched only if planted texts come back.

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

from engine.dagapeyeff_additive import _tables
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_foursquare import PLAIN, _HELD, _held, _model

_SOURCE = Path(__file__).resolve().parent / "dagapeyeff_keyedsquares.c"
_SEED = 20261015
_LETTERS = 196
_PLANTED = 3
_RESTARTS = 1
_STEPS = 40_000_000
_TEMPERATURE = 8.0
_RECOVERED = 0.9
_PROSE_FLOOR = -2.3


@lru_cache(maxsize=1)
def _kernel():
    compiler = shutil.which("cc") or shutil.which("gcc") or shutil.which("clang")
    if compiler is None:
        raise RuntimeError("a C compiler is needed to rerun the keyed-squares search")
    built = Path(tempfile.mkdtemp(prefix="keyedsquares-")) / "kernel.so"
    subprocess.run([compiler, "-O3", "-shared", "-fPIC", "-o", str(built), str(_SOURCE), "-lm"], check=True)
    lib = ctypes.CDLL(str(built))
    lib.keyed_anneal.restype = ctypes.c_double
    return lib


def encrypt(text: str, p1: list[int], p2: list[int], u: list[int], l: list[int]) -> list[int]:
    """p1, p2: cell to letter index; u, l: cell to cipher symbol."""
    where1 = {p1[c]: c for c in range(25)}
    where2 = {p2[c]: c for c in range(25)}
    out = []
    for k in range(0, len(text) - 1, 2):
        r1, c1 = divmod(where1[PLAIN.index(text[k])], 5)
        r2, c2 = divmod(where2[PLAIN.index(text[k + 1])], 5)
        out += [u[r1 * 5 + c2], l[r2 * 5 + c1]]
    return out


def two_square(text: str, rng: random.Random) -> list[int]:
    """Horizontal two-square with keyed squares, behind an unknown Polybius labelling of letters."""
    s1, s2, label = (rng.sample(range(25), 25) for _ in range(3))
    return encrypt(text, s1, s2, [label[s2[c]] for c in range(25)], [label[s1[c]] for c in range(25)])


def four_square(text: str, rng: random.Random) -> list[int]:
    return encrypt(text, *(rng.sample(range(25), 25) for _ in range(4)))


def anneal(cells: list[int], seed: int) -> tuple[float, list[int]]:
    lib = _kernel()
    logp, letters = _tables()
    n = len(cells)
    ints = ctypes.c_int * n
    out = ints()
    total = lib.keyed_anneal(ints(*cells), n, logp, letters, ctypes.c_ulonglong(seed), _RESTARTS, _STEPS,
                             ctypes.c_double(_TEMPERATURE), (ctypes.c_int * 100)(), out)
    return total / (n - 3), list(out)


def _per_letter(text: str) -> float:
    return _model().score([ord(ch) - 65 for ch in text]) / (len(text) - 3)


@frozen("dagapeyeff-keyedsquares")
def keyedsquares_report() -> dict:
    rng = random.Random(_SEED)
    jobs = []
    for kind, make in (("two-square", two_square), ("four-square keyed", four_square)):
        for k in range(_PLANTED):
            prose = _held(_HELD[k % len(_HELD)])
            while True:
                start = rng.randrange(len(prose) - _LETTERS)
                text = prose[start:start + _LETTERS]
                if _per_letter(text) >= _PROSE_FLOOR:
                    break
            jobs.append((kind, text, make(text, rng), rng.randrange(1 << 40)))
    _kernel()
    _tables()
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 1) as pool:
        results = list(pool.map(lambda job: anneal(job[2], job[3]), jobs))
    planted = [{
        "kind": kind,
        "true_per_letter": round(_per_letter(text), 4),
        "found_per_letter": round(score, 4),
        "letters_right": round(sum(chr(65 + x) == ch for x, ch in zip(letters, text)) / _LETTERS, 4),
    } for (kind, text, _, _), (score, letters) in zip(jobs, results)]
    return {
        "solved": False,
        "claimed_plaintext": None,
        "cells_searched": False,
        "search": {"restarts": _RESTARTS, "steps": _STEPS, "temperature": _TEMPERATURE},
        "planted": planted,
        "planted_recovered": sum(row["letters_right"] >= _RECOVERED for row in planted),
        "highest_wrong_found": max((row["found_per_letter"] for row in planted if row["letters_right"] < _RECOVERED),
                                   default=None),
    }
