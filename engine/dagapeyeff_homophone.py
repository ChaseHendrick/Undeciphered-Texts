"""A many-to-one key from cell symbols to letters, on the cells. Not a reading.

A homophonic key lets several symbols stand for one letter, which flattens
counts as the cells' 13 common symbols are flattened. This search lets each of
the 25 symbols stand for any letter (engine/dagapeyeff_homophone.c) under the
default model with J folded into I.

The model scores a run of one repeated letter above English, so a free key
collapses onto one letter. A key that gives any letter more places than the
most common letter has in any 196-letter window of held-out English is
refused. Planted held-out English under a homophonic key shows the search's
power; shuffled cells are the control. No letter string is stored.
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
from engine.dagapeyeff_additive import _tables
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_columnar import _regrouped_cells
from engine.dagapeyeff_foursquare import _HELD, _held, _model

_SOURCE = Path(__file__).resolve().parent / "dagapeyeff_homophone.c"
_LETTERS = 196
_SEED = 20261009
_RESTARTS = 2
_STEPS = 600_000
_TEMPERATURE = 8.0
_PLANTED = 6
_SHUFFLES = 8
_RECOVERED = 0.9
_PROSE_FLOOR = -2.5


def letter_cap() -> int:
    """The most places one letter takes in any 196-letter window of held-out English."""
    return max(
        Counter(prose[start:start + _LETTERS]).most_common(1)[0][1]
        for prose in map(_held, _HELD)
        for start in range(0, len(prose) - _LETTERS, 49)
    )


@lru_cache(maxsize=1)
def _kernel():
    compiler = shutil.which("cc") or shutil.which("gcc") or shutil.which("clang")
    if compiler is None:
        raise RuntimeError("a C compiler is needed to rerun the homophone search")
    built = Path(tempfile.mkdtemp(prefix="homophone-")) / "kernel.so"
    subprocess.run([compiler, "-O3", "-shared", "-fPIC", "-o", str(built), str(_SOURCE), "-lm"], check=True)
    lib = ctypes.CDLL(str(built))
    lib.homophone_anneal.restype = ctypes.c_double
    return lib


def anneal(cells: list[int], cap: int, seed: int) -> tuple[float, list[int]]:
    lib = _kernel()
    logp, letters = _tables()
    n = len(cells)
    ints = ctypes.c_int * n
    key = (ctypes.c_int * 25)()
    out = ints()
    total = lib.homophone_anneal(ints(*cells), n, logp, letters, cap, ctypes.c_ulonglong(seed), _RESTARTS, _STEPS,
                                 ctypes.c_double(_TEMPERATURE), key, out)
    return total / (n - 3), list(out)


def homophonic(text: str, rng: random.Random) -> list[int]:
    """25 symbols: one for each letter in the text, the spare ones to the commonest letters."""
    order = [ch for ch, _ in Counter(text).most_common()]
    symbols = list(range(25))
    rng.shuffle(symbols)
    owners = {ch: [symbols[k]] for k, ch in enumerate(order[:25])}
    for extra, k in enumerate(range(len(owners), 25)):
        owners[order[extra % len(order)]].append(symbols[k])
    return [rng.choice(owners[ch]) for ch in text]


def _per_letter(text: str) -> float:
    return _model().score([ord(ch) - 65 for ch in text]) / (len(text) - 3)


@frozen("dagapeyeff-homophone")
def homophone_report() -> dict:
    rng = random.Random(_SEED)
    cap = letter_cap()
    jobs = []
    for k in range(_PLANTED):
        prose = _held(_HELD[k % len(_HELD)])
        while True:
            start = rng.randrange(len(prose) - _LETTERS)
            text = prose[start:start + _LETTERS]
            if _per_letter(text) >= _PROSE_FLOOR:
                break
        jobs.append(("planted", homophonic(text, rng), text, rng.randrange(1 << 40)))
    for label, cells in (("cells", _cells()), ("regrouped", _regrouped_cells())):
        jobs.append((label, cells, None, rng.randrange(1 << 40)))
        for _ in range(_SHUFFLES):
            mixed = list(cells)
            rng.shuffle(mixed)
            jobs.append((label + " shuffle", mixed, None, rng.randrange(1 << 40)))
    _kernel()
    _tables()
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 1) as pool:
        results = list(pool.map(lambda job: anneal(job[1], cap, job[3]), jobs))
    planted = []
    searched = {}
    for (label, cipher, text, _), (score, letters) in zip(jobs, results):
        if label == "planted":
            planted.append({
                "symbols": len(set(cipher)),
                "true_per_letter": round(_per_letter(text), 4),
                "found_per_letter": round(score, 4),
                "letters_right": round(sum(chr(65 + x) == ch for x, ch in zip(letters, text)) / _LETTERS, 4),
            })
            continue
        row = searched.setdefault(label.replace(" shuffle", ""), {"per_letter": None, "shuffles": []})
        if label.endswith("shuffle"):
            row["shuffles"].append(round(score, 4))
        else:
            row["per_letter"] = round(score, 4)
            row["letters_used"] = len(set(letters))
    for row in searched.values():
        row["shuffles"].sort(reverse=True)
        row["shuffles_as_high"] = sum(score >= row["per_letter"] for score in row["shuffles"])
    return {
        "solved": False,
        "claimed_plaintext": None,
        "search": {"restarts": _RESTARTS, "steps": _STEPS, "temperature": _TEMPERATURE, "letter_cap": cap},
        "planted": planted,
        "planted_recovered": sum(row["letters_right"] >= _RECOVERED for row in planted),
        "planted_lowest_true": min(row["true_per_letter"] for row in planted),
        "searched": searched,
    }
