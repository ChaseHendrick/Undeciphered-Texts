"""Latin across three more families: a repeating shift, a homophonic key and four-square. Not a reading.

Latin is the closest language to the cells' letter counts, and it is closed
under a keyed square (engine.dagapeyeff_latin) and a 14-column key
(engine.dagapeyeff_latin14). This pass finishes the cheaper families under the
same Latin quadgram model (UD_Latin-ITTB, first 90 percent):

1. The repeating-shift count of engine.dagapeyeff_additive, with held-out
   Latin windows in place of English, under random squares and shift keys.
2. A many-to-one key capped at the most places one letter takes in a
   196-letter window of held-out Latin (engine/dagapeyeff_homophone.c).
3. Four-square with standard plain squares (engine/dagapeyeff_foursquare.c).

Planted held-out Latin shows each search's power; shuffled cells are the
control. Texts are fetched, not stored. No letter string is stored.
"""

from __future__ import annotations

import ctypes
import os
import random
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_additive import MODES, PERIODS, _random_key, _shape
from engine.dagapeyeff_additive import encrypt as shift_encrypt
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_columnar import _regrouped_cells
from engine.dagapeyeff_foursquare import PLAIN
from engine.dagapeyeff_foursquare import _kernel as fs_kernel
from engine.dagapeyeff_foursquare import encrypt as fs_encrypt
from engine.dagapeyeff_homophone import _kernel as hom_kernel
from engine.dagapeyeff_homophone import homophonic
from engine.dagapeyeff_latin import _model, _tables, texts

_SEED = 20261017
_LETTERS = 196
_COUNT_DRAWS = 3
_PLANTED = 3
_SHUFFLES = 8
_RECOVERED = 0.9


def _windows(step: int) -> list[str]:
    out = []
    for source in ("held", "classical"):
        text = texts()[source]
        out += [text[s:s + _LETTERS] for s in range(0, len(text) - _LETTERS, step)]
    return out


def shift_counts(rng: random.Random) -> dict:
    cells = _shape(_cells())
    windows = _windows(2003)
    rows = []
    for mode in MODES:
        for period in PERIODS:
            draws = []
            for window in windows:
                for _ in range(_COUNT_DRAWS):
                    draws.append(_shape(shift_encrypt(window, rng.sample(range(25), 25),
                                                      _random_key(period, mode, rng))))
            rows.append({"mode": mode, "period": period, "draws": len(draws),
                         "fewest_distinct": min(d["distinct"] for d in draws),
                         "reaching_cells": sum(d["distinct"] <= cells["distinct"]
                                               and d["top_three_rows"] >= cells["top_three_rows"] for d in draws)})
    return {"windows": len(windows), "rows": rows}


def latin_cap() -> int:
    return max(Counter(w).most_common(1)[0][1] for w in _windows(49))


def _hom(cells: list[int], cap: int, seed: int) -> tuple[float, list[int]]:
    lib = hom_kernel()
    logp, letters = _tables()
    n = len(cells)
    ints = ctypes.c_int * n
    out = ints()
    total = lib.homophone_anneal(ints(*cells), n, logp, letters, cap, ctypes.c_ulonglong(seed), 2, 600_000,
                                 ctypes.c_double(8.0), (ctypes.c_int * 25)(), out)
    return total / (n - 3), list(out)


def _fs(cells: list[int], seed: int) -> tuple[float, list[int]]:
    lib = fs_kernel()
    logp, _ = _tables()
    pairs = len(cells) // 2
    ints = ctypes.c_int * (2 * pairs)
    out = ints()
    total = lib.fs_anneal(ints(*cells[:2 * pairs]), pairs, logp, (ctypes.c_int * 25)(*[ord(c) - 65 for c in PLAIN]),
                          ctypes.c_ulonglong(seed), 10, 1_000_000, ctypes.c_double(8.0),
                          (ctypes.c_int * 25)(), (ctypes.c_int * 25)(), out)
    return total / (2 * pairs - 3), list(out)


def _per_letter(text: str) -> float:
    return _model().score([ord(ch) - 65 for ch in text]) / (len(text) - 3)


def _planted_texts(rng: random.Random) -> list[str]:
    out = []
    for k in range(_PLANTED):
        source = texts()["held" if k % 2 == 0 else "classical"]
        start = rng.randrange(len(source) - _LETTERS)
        out.append(source[start:start + _LETTERS])
    return out


def _family(name: str, plant, solve, rng: random.Random, parallel: bool) -> dict:
    jobs = []
    for text in _planted_texts(rng):
        jobs.append(("planted", text, plant(text), rng.randrange(1 << 40)))
    for label, cells in (("cells", _cells()), ("regrouped", _regrouped_cells())):
        jobs.append((label, None, cells, rng.randrange(1 << 40)))
        for _ in range(_SHUFFLES):
            jobs.append((label + " shuffle", None, rng.sample(cells, len(cells)), rng.randrange(1 << 40)))
    if parallel:
        with ThreadPoolExecutor(max_workers=os.cpu_count() or 1) as pool:
            results = list(pool.map(lambda job: solve(job[2], job[3]), jobs))
    else:
        # The four-square kernel keeps its random state in a global, so it runs one call at a time.
        results = [solve(job[2], job[3]) for job in jobs]
    planted, searched = [], {}
    for (label, text, _, _), (score, letters) in zip(jobs, results):
        if label == "planted":
            planted.append({"true_per_letter": round(_per_letter(text), 4), "found_per_letter": round(score, 4),
                            "letters_right": round(sum(chr(65 + x) == c for x, c in zip(letters, text))
                                                   / len(letters), 4)})
            continue
        row = searched.setdefault(label.replace(" shuffle", ""), {"per_letter": None, "shuffles": []})
        if label.endswith("shuffle"):
            row["shuffles"].append(round(score, 4))
        else:
            row["per_letter"] = round(score, 4)
    for row in searched.values():
        row["shuffles"].sort(reverse=True)
        row["shuffles_as_high"] = sum(x >= row["per_letter"] for x in row["shuffles"])
    return {"planted": planted, "planted_recovered": sum(r["letters_right"] >= _RECOVERED for r in planted),
            "searched": searched}


@frozen("dagapeyeff-latinmore")
def latinmore_report() -> dict:
    rng = random.Random(_SEED)
    cap = latin_cap()

    def plant_hom(text):
        return homophonic(text, rng)

    def plant_fs(text):
        return fs_encrypt(text, rng.sample(range(25), 25), rng.sample(range(25), 25))

    _model()
    hom_kernel()
    fs_kernel()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "shift_counts": shift_counts(rng),
        "homophone_cap": cap,
        "homophone": _family("homophone", plant_hom, lambda c, s: _hom(c, cap, s), rng, True),
        "foursquare": _family("foursquare", plant_fs, _fs, rng, False),
    }


_SHIFT_SHUFFLES = 3


def _shift(cells: list[int], period: int, mode: str, seed: int) -> tuple[float, list[int]]:
    from engine.dagapeyeff_additive import _kernel as add_kernel

    lib = add_kernel()
    logp, letters = _tables()
    n = len(cells)
    ints = ctypes.c_int * n
    out = ints()
    total = lib.additive_anneal(ints(*cells), n, period, MODES[mode], logp, letters, ctypes.c_ulonglong(seed),
                                4, 4_000_000, ctypes.c_double(8.0), ctypes.c_double(0.3), (ctypes.c_int * 25)(),
                                ints(), ints(), out)
    return total / (n - 3), list(out)


@frozen("dagapeyeff-latinshift")
def latinshift_report() -> dict:
    """A repeating coordinate shift on a keyed square under the Latin model, which the count did not exclude."""
    rng = random.Random(_SEED + 1)
    jobs = []
    for mode in MODES:
        for period in PERIODS:
            source = texts()["held" if len(jobs) % 2 == 0 else "classical"]
            start = rng.randrange(len(source) - _LETTERS)
            text = source[start:start + _LETTERS]
            cipher = shift_encrypt(text, rng.sample(range(25), 25), _random_key(period, mode, rng))
            jobs.append(("planted", mode, period, text, cipher, rng.randrange(1 << 40)))
            for label, cells in (("cells", _cells()), ("regrouped", _regrouped_cells())):
                jobs.append((label, mode, period, None, cells, rng.randrange(1 << 40)))
                for _ in range(_SHIFT_SHUFFLES):
                    jobs.append((label + " shuffle", mode, period, None, rng.sample(cells, len(cells)),
                                 rng.randrange(1 << 40)))
    _model()
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 1) as pool:
        results = list(pool.map(lambda job: _shift(job[4], job[2], job[1], job[5]), jobs))
    planted, searched = [], {}
    for (label, mode, period, text, _, _), (score, letters) in zip(jobs, results):
        if label == "planted":
            planted.append({"mode": mode, "period": period, "true_per_letter": round(_per_letter(text), 4),
                            "found_per_letter": round(score, 4),
                            "letters_right": round(sum(chr(65 + x) == c for x, c in zip(letters, text)) / _LETTERS, 4)})
            continue
        row = searched.setdefault(f"{label.replace(' shuffle', '')} {mode} {period}", {"per_letter": None, "shuffles": []})
        if label.endswith("shuffle"):
            row["shuffles"].append(round(score, 4))
        else:
            row["per_letter"] = round(score, 4)
    for row in searched.values():
        row["shuffles"].sort(reverse=True)
        row["shuffles_as_high"] = sum(x >= row["per_letter"] for x in row["shuffles"])
    best = max(searched, key=lambda k: searched[k]["per_letter"])
    return {
        "solved": False,
        "claimed_plaintext": None,
        "planted": planted,
        "planted_recovered": sum(r["letters_right"] >= _RECOVERED for r in planted),
        "searched": searched,
        "searched_best": {"case": best, **searched[best]},
        "cases_cells_above_all_shuffles": sum(r["shuffles_as_high"] == 0 for r in searched.values()),
    }
