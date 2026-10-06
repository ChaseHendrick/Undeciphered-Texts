"""Italian under a one-to-one key, with and without enciphering errors. Not a reading.

An early pass let each language choose a merged pair of letters and liked
Italian best (engine.dagapeyeff_swarm); letter rates alone put Italian draws
on the cells' flatness 6 times in 2,000 (engine.dagapeyeff_languages). Neither
used real Italian text or allowed errors. This pass does both.

The text is Manzoni's I promessi sposi in its 1827 edition (the Ventisettana),
as aligned by Sprugnoli and Sartor (https://github.com/RacheleSprugnoli/
Sentence_Alignment_Manzoni, commit e0eedb6). The repository states no licence
for its digital text, so it is not copied into this repository: it is fetched
into the ignored work/ folder when the search is rerun. Accents are removed,
J is folded into I, and only letters are kept.

1. Counts. The fewest errors that turn each 196-letter window's counts into
   the cells', as in engine.dagapeyeff_errors, and the same with random slips.
2. Search. A quadgram model is fit on chapters 1 to 30. Planted Italian from
   chapters 31 to 37 under a random keyed square, with 0 and 8 digit slips, is
   solved by the keyed-square search (engine/dagapeyeff_additive.c at period 1)
   under that model; so are the cells and their shuffles.

No letter string is stored.
"""

from __future__ import annotations

import ctypes
import os
import random
import re
import subprocess
import unicodedata
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from pathlib import Path

import numpy as np

from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_additive import _kernel
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_errors import corrupt, fewest_errors, sorted_counts
from engine.dagapeyeff_foursquare import PLAIN
from engine.language import DiscountedLanguageModel

SOURCE = "https://github.com/RacheleSprugnoli/Sentence_Alignment_Manzoni"
COMMIT = "e0eedb6eb3cfe30ecc0387df8d9a8e8c165bd3d5"
_WORK = Path(__file__).resolve().parents[1] / "work" / "external" / "manzoni"
_SEED = 20261011
_LETTERS = 196
_STRIDE = 4
_TRAIN_CHAPTERS = 30
_ERRORS = (4, 8, 16)
_DRAWS = 2
_PLANTED = 4
_SHUFFLES = 8
_RESTARTS = 2
_STEPS = 300_000
_TEMPERATURE = 8.0
_RECOVERED = 0.9


def _fetch() -> Path:
    folder = _WORK / "repo"
    if not (folder / ".git").exists():
        folder.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "clone", "--quiet", SOURCE, str(folder)], check=True)
    subprocess.run(["git", "-C", str(folder), "checkout", "--quiet", COMMIT], check=True)
    return folder / "Ventisettana-Bentley1834"


def fold(text: str) -> str:
    """Upper-case letters A to Z without accents, J folded into I."""
    plain = unicodedata.normalize("NFD", text.upper())
    return "".join(ch for ch in plain if "A" <= ch <= "Z").replace("J", "I")


@lru_cache(maxsize=1)
def chapters() -> list[str]:
    folder = _fetch()
    paths = sorted(folder.glob("cap.*_src.xml"), key=lambda p: int(re.search(r"cap\.(\d+)_src", p.name).group(1)))
    return [fold(re.sub(r"<[^>]+>", " ", path.read_text(encoding="utf-8"))) for path in paths]


@lru_cache(maxsize=1)
def _italian_model() -> DiscountedLanguageModel:
    return DiscountedLanguageModel("".join(chapters()[:_TRAIN_CHAPTERS]))


def _anneal(cells: list[int], seed: int) -> tuple[float, list[int]]:
    lib = _kernel()
    logp = (ctypes.c_double * 26 ** 4)(*_italian_model().logp)
    letters = (ctypes.c_int * 25)(*[ord(ch) - 65 for ch in PLAIN])
    n = len(cells)
    ints = ctypes.c_int * n
    square = (ctypes.c_int * 25)()
    out = ints()
    total = lib.additive_anneal(ints(*cells), n, 1, 0, logp, letters, ctypes.c_ulonglong(seed), _RESTARTS, _STEPS,
                                ctypes.c_double(_TEMPERATURE), ctypes.c_double(0.0), square, ints(), ints(), out)
    return total / (n - 3), list(out)


def _per_letter(text: str) -> float:
    return _italian_model().score([ord(ch) - 65 for ch in text]) / (len(text) - 3)


def count_check() -> dict:
    rng = random.Random(_SEED)
    target = sorted_counts(_cells())
    text = "".join(chapters())
    ints = np.asarray([PLAIN.index(ch) for ch in text])
    starts = np.arange(0, len(ints) - _LETTERS + 1, _STRIDE)
    counts = np.zeros((len(starts), 25), dtype=np.int64)
    for letter in range(25):
        running = np.concatenate([[0], np.cumsum(ints == letter)])
        counts[:, letter] = running[starts + _LETTERS] - running[starts]
    ordered = -np.sort(-counts, axis=1)
    fewest = np.abs(ordered - target).sum(axis=1) // 2
    distinct = (counts > 0).sum(axis=1)
    largest = counts.max(axis=1)
    sample = [text[s:s + _LETTERS] for s in range(0, len(text) - _LETTERS, 97 * _STRIDE)]
    rows = []
    for k in _ERRORS:
        remaining = []
        for window in sample:
            square = list(range(25))
            rng.shuffle(square)
            where = {PLAIN[square[cell]]: cell for cell in range(25)}
            cells = [where[ch] for ch in window]
            for _ in range(_DRAWS):
                remaining.append(fewest_errors(corrupt(cells, k, rng, "slip"), target))
        rows.append({"errors": k, "draws": len(remaining), "fewest_remaining": min(remaining),
                     "reaching_cells": sum(x == 0 for x in remaining)})
    return {
        "letters": len(text),
        "windows": int(len(starts)),
        "fewest_errors": int(fewest.min()),
        "median_errors": float(np.median(fewest)),
        "windows_within_8": int((fewest <= 8).sum()),
        "windows_within_12": int((fewest <= 12).sum()),
        "distinct_at_most_18": int((distinct <= 18).sum()),
        "largest_at_most_20": int((largest <= 20).sum()),
        "both": int(((distinct <= 18) & (largest <= 20)).sum()),
        "random_slips": rows,
    }


@frozen("dagapeyeff-italian")
def italian_report() -> dict:
    rng = random.Random(_SEED + 1)
    held = "".join(chapters()[_TRAIN_CHAPTERS:])
    jobs = []
    for errors in (0, 8):
        for _ in range(_PLANTED):
            start = rng.randrange(len(held) - _LETTERS)
            text = held[start:start + _LETTERS]
            square = list(range(25))
            rng.shuffle(square)
            where = {PLAIN[square[cell]]: cell for cell in range(25)}
            cells = corrupt([where[ch] for ch in text], errors, rng, "slip")
            jobs.append(("planted", errors, text, cells, rng.randrange(1 << 40)))
    cells = _cells()
    jobs.append(("cells", 0, None, cells, rng.randrange(1 << 40)))
    for _ in range(_SHUFFLES):
        mixed = list(cells)
        rng.shuffle(mixed)
        jobs.append(("shuffle", 0, None, mixed, rng.randrange(1 << 40)))
    _italian_model()
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 1) as pool:
        results = list(pool.map(lambda job: _anneal(job[3], job[4]), jobs))
    planted = []
    shuffles = []
    cell_score = None
    for (kind, errors, text, _, _), (score, letters) in zip(jobs, results):
        if kind == "planted":
            planted.append({
                "errors": errors,
                "true_per_letter": round(_per_letter(text), 4),
                "found_per_letter": round(score, 4),
                "letters_right": round(sum(chr(65 + x) == ch for x, ch in zip(letters, text)) / _LETTERS, 4),
            })
        elif kind == "cells":
            cell_score = round(score, 4)
        else:
            shuffles.append(round(score, 4))
    clean = [row for row in planted if row["errors"] == 0]
    slipped = [row for row in planted if row["errors"] == 8]
    return {
        "solved": False,
        "claimed_plaintext": None,
        "source": {"url": SOURCE, "commit": COMMIT, "edition": "Ventisettana, 1827", "train_chapters": _TRAIN_CHAPTERS},
        "search": {"restarts": _RESTARTS, "steps": _STEPS, "temperature": _TEMPERATURE},
        "counts": count_check(),
        "planted": planted,
        "planted_recovered": sum(row["letters_right"] >= _RECOVERED for row in clean),
        "planted_with_errors_recovered": sum(row["letters_right"] >= _RECOVERED for row in slipped),
        "planted_lowest_true": min(row["true_per_letter"] for row in clean),
        "planted_with_errors_lowest_found": min(row["found_per_letter"] for row in slipped),
        "cells_per_letter": cell_score,
        "shuffles": sorted(shuffles, reverse=True),
        "shuffles_as_high": sum(score >= cell_score for score in shuffles),
    }
