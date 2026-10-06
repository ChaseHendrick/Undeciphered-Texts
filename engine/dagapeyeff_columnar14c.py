"""Width-14 columnar transposition with a letter key, compiled, on the cells. Not a reading.

The cells are 196 symbols, exactly 14 rows of 14. The plainest large-key
hypothesis is a Polybius substitution and a complete 14-column transposition.
The Python joint search in engine.dagapeyeff_columnar recovered 0 of 3 planted
texts at this width. This pass anneals the column order and the letter key
together in a compiled kernel (engine/dagapeyeff_columnar14c.c) under the
default model with J folded into I, with far more steps.

Both directions are searched. Undone: the plaintext was written in rows of 14
and the columns copied out in key order. Done: the cells are what that copying
gives when run backwards. In the done direction the plaintext is 14 runs of 14
letters whose order only shows at 13 joins, so a planted text counts as
recovered when the key gives the right letter for at least 90 percent of the
cells, whatever the column order. Planted texts with wrong cells show what
enciphering errors cost. Shuffled cells are the control. No letter string is
stored.
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

WIDTH = 14
_LETTERS = WIDTH * WIDTH
_SOURCE = Path(__file__).resolve().parent / "dagapeyeff_columnar14c.c"
_ENGLISH = "ETAOINSRHLDCUMFPGWYBVKXQZ"
_SEED = 20261016
_RESTARTS = 8
_STEPS = 16_000_000
_TEMPERATURE = 12.0
_KEY_SHARE = 0.6
_SHUFFLES = 20
_RECOVERED = 0.9
_PLANTED = ((0, 2), (8, 1))
DIRECTIONS = ("undone", "done")


def encrypt(symbols: list[int], order: list[int], direction: str) -> tuple[list[int], list[int]]:
    """Cipher symbols, and the plaintext position behind each cipher position."""
    source = [0] * _LETTERS
    for column in range(WIDTH):
        for row in range(WIDTH):
            if direction == "done":
                source[row * WIDTH + column] = order[column] * WIDTH + row
            else:
                source[order[column] * WIDTH + row] = row * WIDTH + column
    return [symbols[i] for i in source], source


def frequency_key(cells: list[int]) -> list[int]:
    """Most common symbol to E, the next to T, and so on."""
    counts = Counter(cells)
    ranked = sorted(range(25), key=lambda symbol: (-counts[symbol], symbol))
    key = [0] * 25
    for rank, symbol in enumerate(ranked):
        key[symbol] = PLAIN.index(_ENGLISH[rank])
    return key


@lru_cache(maxsize=1)
def _kernel():
    compiler = shutil.which("cc") or shutil.which("gcc") or shutil.which("clang")
    if compiler is None:
        raise RuntimeError("a C compiler is needed to rerun the width-14 search")
    built = Path(tempfile.mkdtemp(prefix="columnar14-")) / "kernel.so"
    subprocess.run([compiler, "-O3", "-shared", "-fPIC", "-o", str(built), str(_SOURCE), "-lm"], check=True)
    lib = ctypes.CDLL(str(built))
    lib.c14_anneal.restype = ctypes.c_double
    return lib


@lru_cache(maxsize=1)
def _tables():
    logp = (ctypes.c_double * 26 ** 4)(*_model().logp)
    letters = (ctypes.c_int * 25)(*[ord(ch) - 65 for ch in PLAIN])
    return logp, letters


def anneal(cells: list[int], direction: str, seed: int, restarts: int = _RESTARTS,
           steps: int = _STEPS) -> tuple[float, list[int], list[int]]:
    """Best quadgram score per letter, the key and the column order behind it."""
    lib = _kernel()
    logp, letters = _tables()
    cipher = (ctypes.c_int * _LETTERS)(*cells)
    start = (ctypes.c_int * 25)(*frequency_key(cells))
    order = (ctypes.c_int * WIDTH)()
    key = (ctypes.c_int * 25)()
    plain = (ctypes.c_int * _LETTERS)()
    total = lib.c14_anneal(cipher, logp, letters, start, int(direction == "done"), ctypes.c_ulonglong(seed),
                           restarts, steps, ctypes.c_double(_TEMPERATURE), ctypes.c_double(_KEY_SHARE),
                           order, key, plain)
    return total / (_LETTERS - 3), list(key), list(order)


def _per_letter(text: str) -> float:
    return _model().score([ord(ch) - 65 for ch in text]) / (len(text) - 3)


def _jobs(rng: random.Random) -> tuple[list[dict], list[dict]]:
    planted = []
    for direction in DIRECTIONS:
        for errors, per_source in _PLANTED:
            for name in _HELD:
                prose = _held(name)
                for _ in range(per_source):
                    start = rng.randrange(len(prose) - _LETTERS)
                    text = prose[start:start + _LETTERS]
                    order = list(range(WIDTH))
                    substitution = list(range(25))
                    rng.shuffle(order)
                    rng.shuffle(substitution)
                    cells, source = encrypt([substitution[PLAIN.index(ch)] for ch in text], order, direction)
                    for _ in range(errors):
                        cells[rng.randrange(_LETTERS)] = rng.randrange(25)
                    planted.append({"source": name, "direction": direction, "errors": errors, "text": text,
                                    "cells": cells, "from": source, "seed": rng.randrange(1 << 40)})
    searched = []
    for label, cells in (("cells", _cells()), ("regrouped", _regrouped_cells())):
        for direction in DIRECTIONS:
            searched.append({"label": f"{label} {direction}", "direction": direction, "cells": cells,
                             "seed": rng.randrange(1 << 40)})
            for index in range(_SHUFFLES):
                mixed = list(cells)
                rng.shuffle(mixed)
                searched.append({"label": f"{label} {direction}", "direction": direction, "cells": mixed,
                                 "shuffle": index, "seed": rng.randrange(1 << 40)})
    return planted, searched


@frozen("dagapeyeff-columnar14c")
def columnar14c_report() -> dict:
    planted_jobs, searched_jobs = _jobs(random.Random(_SEED))
    jobs = planted_jobs + searched_jobs
    _kernel()
    _tables()
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 1) as pool:
        found = list(pool.map(lambda job: anneal(job["cells"], job["direction"], job["seed"]), jobs))
    planted = []
    for job, (score, key, _) in zip(planted_jobs, found):
        text, cells, source = job["text"], job["cells"], job["from"]
        right = sum(PLAIN[key[cells[i]]] == text[source[i]] for i in range(_LETTERS)) / _LETTERS
        planted.append({
            "source": job["source"],
            "direction": job["direction"],
            "errors": job["errors"],
            "true_per_letter": round(_per_letter(text), 4),
            "found_per_letter": round(score, 4),
            "cells_right": round(right, 4),
        })
    searched = {}
    for job, (score, _, _) in zip(searched_jobs, found[len(planted_jobs):]):
        row = searched.setdefault(job["label"], {"per_letter": None, "shuffles": []})
        if "shuffle" in job:
            row["shuffles"].append(round(score, 4))
        else:
            row["per_letter"] = round(score, 4)
    for row in searched.values():
        row["shuffles"].sort(reverse=True)
        row["shuffles_as_high"] = sum(score >= row["per_letter"] for score in row["shuffles"])
    recovered = {}
    for row in planted:
        tally = recovered.setdefault(f"{row['direction']} errors {row['errors']}", [0, 0])
        tally[0] += row["cells_right"] >= _RECOVERED
        tally[1] += 1
    return {
        "solved": False,
        "claimed_plaintext": None,
        "search": {"restarts": _RESTARTS, "steps": _STEPS, "temperature": _TEMPERATURE, "key_share": _KEY_SHARE},
        "planted": planted,
        "planted_recovered": recovered,
        "planted_lowest_true": min(row["true_per_letter"] for row in planted),
        "searched": searched,
    }
