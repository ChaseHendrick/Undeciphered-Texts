"""A keyed Polybius square with a repeating coordinate shift, on the cells. Not a reading.

The classical next step after a plain Polybius square is to add a short key
to the coordinates, row and column each modulo 5. engine.dagapeyeff_add tried
periods 2 and 3 on the book's own letter order under the old model. Here the
square is unknown and is annealed together with the shifts, at periods 2, 3,
4, 5, 7 and 14, shifting both coordinates or the column only, in a compiled
kernel (engine/dagapeyeff_additive.c) under the default model with J folded
into I.

A count comes first and needs no search. A repeating shift spreads each
letter over several cells, so it raises the number of different symbols. The
cells use 18. Planted held-out English under random squares and shift keys
sets the range.

Planted held-out texts show the search's power. Shuffled cells are the
control. No letter string is stored.
"""

from __future__ import annotations

import ctypes
import os
import random
import shutil
import subprocess
import tempfile
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from pathlib import Path

from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_columnar import _regrouped_cells
from engine.dagapeyeff_foursquare import PLAIN, _HELD, _held, _model

_SOURCE = Path(__file__).resolve().parent / "dagapeyeff_additive.c"
_LETTERS = 196
_SEED = 20261006
PERIODS = (2, 3, 4, 5, 7, 14)
MODES = {"both": 0, "column": 1, "row": 2}
_SEARCHED_MODES = ("both", "column")
_COUNT_DRAWS = 5
_RESTARTS = 4
_STEPS = 4_000_000
_TEMPERATURE = 8.0
_KEY_SHARE = 0.3
_SHUFFLES = 3
_RECOVERED = 0.9


def encrypt(text: str, square: list[int], key: list[tuple[int, int]]) -> list[int]:
    """Cells 0 to 24. square[cell] is the letter index in PLAIN at that cell."""
    where = {PLAIN[square[cell]]: cell for cell in range(25)}
    out = []
    for i, ch in enumerate(text):
        row, column = divmod(where[ch], 5)
        dr, dc = key[i % len(key)]
        out.append(((row + dr) % 5) * 5 + (column + dc) % 5)
    return out


def _random_key(period: int, mode: str, rng: random.Random) -> list[tuple[int, int]]:
    return [
        (0 if mode == "column" else rng.randrange(5), 0 if mode == "row" else rng.randrange(5))
        for _ in range(period)
    ]


def _shape(cells: list[int]) -> dict:
    rows = Counter(cell // 5 for cell in cells)
    return {"distinct": len(set(cells)), "top_three_rows": sum(n for _, n in rows.most_common(3))}


def count_check() -> dict:
    """Different symbols and the share of the three busiest rows, for English under random keys."""
    rng = random.Random(_SEED)
    cells = _shape(_cells())
    rows = []
    for mode in MODES:
        for period in PERIODS:
            draws = []
            for name in _HELD:
                prose = _held(name)
                for start in range(0, len(prose) - _LETTERS, 197):
                    window = prose[start:start + _LETTERS]
                    for _ in range(_COUNT_DRAWS):
                        square = list(range(25))
                        rng.shuffle(square)
                        draws.append(_shape(encrypt(window, square, _random_key(period, mode, rng))))
            rows.append({
                "mode": mode,
                "period": period,
                "draws": len(draws),
                "fewest_distinct": min(d["distinct"] for d in draws),
                "most_in_top_three_rows": max(d["top_three_rows"] for d in draws),
                "reaching_cells": sum(
                    d["distinct"] <= cells["distinct"] and d["top_three_rows"] >= cells["top_three_rows"]
                    for d in draws
                ),
            })
    return {"cells": cells, "rows": rows}


@lru_cache(maxsize=1)
def _kernel():
    compiler = shutil.which("cc") or shutil.which("gcc") or shutil.which("clang")
    if compiler is None:
        raise RuntimeError("a C compiler is needed to rerun the additive search")
    built = Path(tempfile.mkdtemp(prefix="additive-")) / "kernel.so"
    subprocess.run([compiler, "-O3", "-shared", "-fPIC", "-o", str(built), str(_SOURCE), "-lm"], check=True)
    lib = ctypes.CDLL(str(built))
    lib.additive_anneal.restype = ctypes.c_double
    return lib


@lru_cache(maxsize=1)
def _tables():
    logp = (ctypes.c_double * 26 ** 4)(*_model().logp)
    letters = (ctypes.c_int * 25)(*[ord(ch) - 65 for ch in PLAIN])
    return logp, letters


def anneal(cells: list[int], period: int, mode: str, seed: int,
           restarts: int = _RESTARTS, steps: int = _STEPS) -> tuple[float, list[int]]:
    """Best quadgram score per letter, and the letters behind it as integers."""
    lib = _kernel()
    logp, letters = _tables()
    n = len(cells)
    ints = ctypes.c_int * n
    square = (ctypes.c_int * 25)()
    dr = ints()
    dc = ints()
    out = ints()
    total = lib.additive_anneal(ints(*cells), n, period, MODES[mode], logp, letters, ctypes.c_ulonglong(seed),
                                restarts, steps, ctypes.c_double(_TEMPERATURE), ctypes.c_double(_KEY_SHARE),
                                square, dr, dc, out)
    return total / (n - 3), list(out)


def _per_letter(text: str) -> float:
    return _model().score([ord(ch) - 65 for ch in text]) / (len(text) - 3)


@frozen("dagapeyeff-additive")
def additive_report() -> dict:
    rng = random.Random(_SEED)
    jobs = []
    for mode in _SEARCHED_MODES:
        for period in PERIODS:
            prose = _held(_HELD[len(jobs) % len(_HELD)])
            start = rng.randrange(len(prose) - _LETTERS)
            text = prose[start:start + _LETTERS]
            square = list(range(25))
            rng.shuffle(square)
            cipher = encrypt(text, square, _random_key(period, mode, rng))
            jobs.append(("planted", mode, period, cipher, text, rng.randrange(1 << 40)))
            for label, cells in (("cells", _cells()), ("regrouped", _regrouped_cells())):
                jobs.append((label, mode, period, cells, None, rng.randrange(1 << 40)))
                for _ in range(_SHUFFLES):
                    mixed = list(cells)
                    rng.shuffle(mixed)
                    jobs.append((label + " shuffle", mode, period, mixed, None, rng.randrange(1 << 40)))

    def run(job):
        _, mode, period, cells, _, seed = job
        return anneal(cells, period, mode, seed)

    _kernel()
    _tables()
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 1) as pool:
        results = list(pool.map(run, jobs))

    planted = []
    searched = {}
    for (label, mode, period, _, text, _), (score, letters) in zip(jobs, results):
        if label == "planted":
            planted.append({
                "mode": mode,
                "period": period,
                "true_per_letter": round(_per_letter(text), 4),
                "found_per_letter": round(score, 4),
                "letters_right": round(sum(chr(65 + x) == ch for x, ch in zip(letters, text)) / _LETTERS, 4),
            })
            continue
        base = label.replace(" shuffle", "")
        row = searched.setdefault(f"{base} {mode} {period}", {"per_letter": None, "shuffles": []})
        if label.endswith("shuffle"):
            row["shuffles"].append(round(score, 4))
        else:
            row["per_letter"] = round(score, 4)
    for row in searched.values():
        row["shuffles"].sort(reverse=True)
        row["shuffles_as_high"] = sum(score >= row["per_letter"] for score in row["shuffles"])
    return {
        "solved": False,
        "claimed_plaintext": None,
        "search": {"restarts": _RESTARTS, "steps": _STEPS, "temperature": _TEMPERATURE, "key_share": _KEY_SHARE},
        "counts": count_check(),
        "planted": planted,
        "planted_recovered": sum(row["letters_right"] >= _RECOVERED for row in planted),
        "planted_lowest_true": min(row["true_per_letter"] for row in planted),
        "searched": searched,
        "searched_best": max(row["per_letter"] for row in searched.values()),
    }
