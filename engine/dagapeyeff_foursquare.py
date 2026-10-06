"""Four-square on the cells: a count that needs no key, then a search. Not a reading.

In four-square the first letter of each cipher pair comes from one square and
the second from another. Which cell is hit depends only on the plaintext's
square rows and columns, so the number of different symbols on each side is
fixed before any cipher key is chosen. Held-out English sets the range.

The search anneals both cipher squares under the default English model, with a
compiled kernel (engine/dagapeyeff_foursquare.c). Planted held-out texts show
its power. Shuffled cells are the control. No letter string is stored.
"""

from __future__ import annotations

import ctypes
import random
import shutil
import subprocess
import tempfile
from functools import lru_cache
from pathlib import Path

from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_columnar import _regrouped_cells
from engine.language import DiscountedLanguageModel, _PUBLIC
from engine.neural_grade import letters_az

PLAIN = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
_DATA = Path(__file__).resolve().parent / "data"
_HELD = ("neural_train_austen.txt", "neural_heldout_doyle.txt", "neural_audit_wells.txt")
_SOURCE = Path(__file__).resolve().parent / "dagapeyeff_foursquare.c"
_LETTERS = 196
_SEED = 20261006
_KEYED_DRAWS = 20
_RESTARTS = 10
_STEPS = 1_000_000
_TEMPERATURE = 8.0
_SHUFFLES = 20
_RECOVERED = 0.95


def _held(name: str) -> str:
    return letters_az((_DATA / name).read_text(encoding="utf-8").upper()).replace("J", "I")


def sides(cells: list[int]) -> tuple[int, int]:
    """Different symbols at the first and at the second place of each pair."""
    return len(set(cells[0::2])), len(set(cells[1::2]))


def _phases(cells: list[int]) -> dict[str, list[int]]:
    return {"pairs-from-first": cells, "pairs-from-second": cells[1:-1]}


def encrypt(text: str, upper_right: list[int], lower_left: list[int],
            upper_left: str = PLAIN, lower_right: str = PLAIN) -> list[int]:
    """Cipher symbols 0 to 24 for an even run of 25-letter plaintext."""
    left = {ch: divmod(i, 5) for i, ch in enumerate(upper_left)}
    right = {ch: divmod(i, 5) for i, ch in enumerate(lower_right)}
    out = []
    for k in range(0, len(text) - 1, 2):
        r1, c1 = left[text[k]]
        r2, c2 = right[text[k + 1]]
        out += [upper_right[r1 * 5 + c2], lower_left[r2 * 5 + c1]]
    return out


def count_check() -> dict:
    """Side counts of held-out English under plain and keyed plain squares."""
    rng = random.Random(_SEED)
    standard = []
    keyed = []
    identity = list(range(25))
    for name in _HELD:
        prose = _held(name)
        for start in range(0, len(prose) - _LETTERS, 97):
            window = prose[start:start + _LETTERS]
            standard.append(sorted(sides(encrypt(window, identity, identity))))
            for _ in range(_KEYED_DRAWS):
                upper = list(PLAIN)
                lower = list(PLAIN)
                rng.shuffle(upper)
                rng.shuffle(lower)
                keyed.append(sorted(sides(encrypt(window, identity, identity, "".join(upper), "".join(lower)))))
    texts = {
        "cells": {phase: list(sides(cells)) for phase, cells in _phases(_cells()).items()},
        "regrouped": {phase: list(sides(cells)) for phase, cells in _phases(_regrouped_cells()).items()},
    }

    def reach(draws: list[list[int]], low: int, high: int) -> int:
        return sum(a <= low and b <= high for a, b in draws)

    cell_low, cell_high = sorted(texts["cells"]["pairs-from-first"])
    return {
        "texts": texts,
        "standard_windows": len(standard),
        "keyed_draws": len(keyed),
        "standard_fewest_larger_side": min(b for _, b in standard),
        "keyed_fewest_larger_side": min(b for _, b in keyed),
        "standard_reaching_cells": reach(standard, cell_low, cell_high),
        "keyed_reaching_cells": reach(keyed, cell_low, cell_high),
    }


@lru_cache(maxsize=1)
def _kernel():
    compiler = shutil.which("cc") or shutil.which("gcc") or shutil.which("clang")
    if compiler is None:
        raise RuntimeError("a C compiler is needed to rerun the four-square search")
    built = Path(tempfile.mkdtemp(prefix="foursquare-")) / "kernel.so"
    subprocess.run([compiler, "-O3", "-shared", "-fPIC", "-o", str(built), str(_SOURCE), "-lm"], check=True)
    lib = ctypes.CDLL(str(built))
    lib.fs_anneal.restype = ctypes.c_double
    return lib


@lru_cache(maxsize=1)
def _model() -> DiscountedLanguageModel:
    """The default model's prose with J folded into I, to match the 25 letters."""
    return DiscountedLanguageModel(_PUBLIC.read_text(encoding="utf-8").upper().replace("J", "I"))


def anneal(cells: list[int], seed: int) -> tuple[float, list[int]]:
    """Best quadgram score per letter and the letters behind it, as integers."""
    lib = _kernel()
    pairs = len(cells) // 2
    ints = ctypes.c_int * (2 * pairs)
    cipher = ints(*cells[:2 * pairs])
    logp = (ctypes.c_double * 26 ** 4)(*_model().logp)
    plain = (ctypes.c_int * 25)(*[ord(ch) - 65 for ch in PLAIN])
    upper = (ctypes.c_int * 25)()
    lower = (ctypes.c_int * 25)()
    out = ints()
    total = lib.fs_anneal(cipher, pairs, logp, plain, ctypes.c_ulonglong(seed), _RESTARTS, _STEPS,
                          ctypes.c_double(_TEMPERATURE), upper, lower, out)
    return total / (2 * pairs - 3), list(out)


def _per_letter(letters: str) -> float:
    return _model().score([ord(ch) - 65 for ch in letters]) / (len(letters) - 3)


def _control(cells: list[int], rng: random.Random) -> dict:
    best, _ = anneal(cells, rng.randrange(1 << 40))
    scores = []
    for _ in range(_SHUFFLES):
        mixed = list(cells)
        rng.shuffle(mixed)
        scores.append(round(anneal(mixed, rng.randrange(1 << 40))[0], 4))
    return {
        "per_letter": round(best, 4),
        "shuffles": sorted(scores, reverse=True),
        "shuffles_as_high": sum(score >= round(best, 4) for score in scores),
    }


@frozen("dagapeyeff-foursquare")
def foursquare_report() -> dict:
    rng = random.Random(_SEED)
    planted = []
    for name in _HELD:
        prose = _held(name)
        for _ in range(2):
            start = rng.randrange(len(prose) - _LETTERS)
            text = prose[start:start + _LETTERS]
            upper = list(range(25))
            lower = list(range(25))
            rng.shuffle(upper)
            rng.shuffle(lower)
            found, letters = anneal(encrypt(text, upper, lower), rng.randrange(1 << 40))
            share = sum(chr(65 + x) == ch for x, ch in zip(letters, text)) / _LETTERS
            planted.append({
                "source": name,
                "true_per_letter": round(_per_letter(text), 4),
                "found_per_letter": round(found, 4),
                "letters_right": round(share, 4),
            })
    searched = {}
    for label, cells in (("cells", _cells()), ("regrouped", _regrouped_cells())):
        for phase, run in _phases(cells).items():
            searched[f"{label} {phase}"] = _control(run, rng)
    recovered = sum(row["letters_right"] >= _RECOVERED for row in planted)
    return {
        "solved": False,
        "claimed_plaintext": None,
        "search": {"restarts": _RESTARTS, "steps": _STEPS, "temperature": _TEMPERATURE},
        "counts": count_check(),
        "planted": planted,
        "planted_recovered": recovered,
        "planted_lowest_true": min(row["true_per_letter"] for row in planted),
        "searched": searched,
    }
