"""Latin under a one-to-one key, the closest language by letter counts. Not a reading.

engine.dagapeyeff_screen found Latin the closest of 39 languages to the cells'
letter counts: a window of the Index Thomisticus treebank needs only 4 errors,
and 294 windows need 8 or fewer, about the rate of the book's own exercise.
That is a count, not a reading. This pass searches.

A quadgram model is fit on the first 90 percent of the Index Thomisticus
(UD_Latin-ITTB). Planted Latin from the held-out tail and from classical
Latin (UD_Latin-Perseus), under random keyed squares, with 0 and 8 digit
slips, shows the search's power. The cells and the regrouping are solved as a
keyed square (engine/dagapeyeff_additive.c at period 1) under that model, as
are the book's dummy rule (every 3rd, 4th or 5th cell dropped, every phase),
and every variant is run on 8 shuffles of all the cells, best against best.

The texts are fetched into the ignored work/ folder; only scores are stored.
No letter string is stored.
"""

from __future__ import annotations

import ctypes
import os
import random
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache

import numpy as np

from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_additive import _kernel
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_columnar import _regrouped_cells
from engine.dagapeyeff_errors import corrupt, fewest_errors, sorted_counts
from engine.dagapeyeff_foursquare import PLAIN
from engine.dagapeyeff_screen import text_of
from engine.language import DiscountedLanguageModel

_SEED = 20261012
_LETTERS = 196
_TRAIN_SHARE = 0.9
_PLANTED = 3
_SHUFFLES = 8
_RESTARTS = 2
_STEPS = 400_000
_TEMPERATURE = 8.0
_RECOVERED = 0.9
NULL_PERIODS = (3, 4, 5)
_ERRORS = (4, 8, 16)
_DRAWS = 2


@lru_cache(maxsize=1)
def texts() -> dict[str, str]:
    thomas = text_of("Latin-ITTB")
    cut = int(len(thomas) * _TRAIN_SHARE)
    return {"train": thomas[:cut], "held": thomas[cut:], "classical": text_of("Latin-Perseus")}


@lru_cache(maxsize=1)
def _model() -> DiscountedLanguageModel:
    return DiscountedLanguageModel(texts()["train"])


@lru_cache(maxsize=1)
def _tables():
    return (ctypes.c_double * 26 ** 4)(*_model().logp), (ctypes.c_int * 25)(*[ord(ch) - 65 for ch in PLAIN])


def anneal(cells: list[int], seed: int) -> tuple[float, list[int]]:
    lib = _kernel()
    logp, letters = _tables()
    n = len(cells)
    ints = ctypes.c_int * n
    out = ints()
    total = lib.additive_anneal(ints(*cells), n, 1, 0, logp, letters, ctypes.c_ulonglong(seed), _RESTARTS, _STEPS,
                                ctypes.c_double(_TEMPERATURE), ctypes.c_double(0.0), (ctypes.c_int * 25)(),
                                ints(), ints(), out)
    return total / (n - 3), list(out)


def _per_letter(text: str) -> float:
    return _model().score([ord(ch) - 65 for ch in text]) / (len(text) - 3)


def variants(cells: list[int]) -> dict[str, list[int]]:
    out = {"square": list(cells)}
    for period in NULL_PERIODS:
        for phase in range(period):
            out[f"nulls {period}:{phase}"] = [c for i, c in enumerate(cells) if i % period != phase]
    return out


def slip_check(rng: random.Random) -> list[dict]:
    target = sorted_counts(_cells())
    rows = []
    for source in ("held", "classical"):
        text = texts()[source]
        windows = [text[s:s + _LETTERS] for s in range(0, len(text) - _LETTERS, 389)]
        for k in _ERRORS:
            remaining = []
            for window in windows:
                square = list(range(25))
                rng.shuffle(square)
                where = {PLAIN[square[cell]]: cell for cell in range(25)}
                cells = [where[ch] for ch in window]
                for _ in range(_DRAWS):
                    remaining.append(fewest_errors(corrupt(cells, k, rng, "slip"), target))
            rows.append({"source": source, "errors": k, "draws": len(remaining),
                         "fewest_remaining": min(remaining), "median_remaining": float(np.median(remaining)),
                         "reaching_cells": sum(x == 0 for x in remaining)})
    return rows


@frozen("dagapeyeff-latin")
def latin_report() -> dict:
    rng = random.Random(_SEED)
    jobs = []
    for source in ("held", "classical"):
        prose = texts()[source]
        for errors in (0, 8):
            for _ in range(_PLANTED):
                start = rng.randrange(len(prose) - _LETTERS)
                text = prose[start:start + _LETTERS]
                square = list(range(25))
                rng.shuffle(square)
                where = {PLAIN[square[cell]]: cell for cell in range(25)}
                cipher = corrupt([where[ch] for ch in text], errors, rng, "slip")
                jobs.append(("planted", f"{source} {errors}", text, cipher, rng.randrange(1 << 40)))
    for label, cells in (("cells", _cells()), ("regrouped", _regrouped_cells())):
        sources = [cells]
        for _ in range(_SHUFFLES):
            mixed = list(cells)
            rng.shuffle(mixed)
            sources.append(mixed)
        for index, source in enumerate(sources):
            for name, run in variants(source).items():
                jobs.append((label, index, name, run, rng.randrange(1 << 40)))
    _kernel()
    _tables()
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 1) as pool:
        results = list(pool.map(lambda job: anneal(job[3], job[4]), jobs))

    planted = []
    scores: dict[str, dict[str, list]] = {"cells": {}, "regrouped": {}}
    for job, (score, letters) in zip(jobs, results):
        if job[0] == "planted":
            _, case, text, _, _ = job
            planted.append({
                "case": case,
                "true_per_letter": round(_per_letter(text), 4),
                "found_per_letter": round(score, 4),
                "letters_right": round(sum(chr(65 + x) == ch for x, ch in zip(letters, text)) / _LETTERS, 4),
            })
            continue
        label, index, name, _, _ = job
        scores[label].setdefault(name, [None] * (_SHUFFLES + 1))[index] = round(score, 4)

    searched = {}
    for label, table in scores.items():
        best = max(values[0] for values in table.values())
        shuffle_bests = sorted((max(values[i] for values in table.values()) for i in range(1, _SHUFFLES + 1)),
                               reverse=True)
        square = table["square"]
        searched[label] = {
            "square": square[0],
            "square_shuffles_as_high": sum(x >= square[0] for x in square[1:]),
            "best": best,
            "best_variant": max(table, key=lambda name: table[name][0]),
            "shuffle_bests": shuffle_bests,
            "shuffle_bests_as_high": sum(x >= best for x in shuffle_bests),
        }
    clean = [row for row in planted if row["case"].endswith(" 0")]
    slipped = [row for row in planted if row["case"].endswith(" 8")]
    return {
        "solved": False,
        "claimed_plaintext": None,
        "source": {"model": "UD_Latin-ITTB, first 90 percent", "planted": "UD_Latin-ITTB tail and UD_Latin-Perseus"},
        "search": {"restarts": _RESTARTS, "steps": _STEPS, "temperature": _TEMPERATURE,
                   "variants": len(variants(_cells())), "shuffles": _SHUFFLES},
        "letters": {name: len(text) for name, text in texts().items()},
        "planted": planted,
        "planted_recovered": sum(row["letters_right"] >= _RECOVERED for row in clean),
        "planted_with_errors_recovered": sum(row["letters_right"] >= _RECOVERED for row in slipped),
        "planted_lowest_true": min(row["true_per_letter"] for row in clean),
        "planted_with_errors_lowest_found": min(row["found_per_letter"] for row in slipped),
        "searched": searched,
        "random_slips": slip_check(rng),
    }
