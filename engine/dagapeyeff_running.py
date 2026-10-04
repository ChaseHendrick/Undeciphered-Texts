"""Slide printed prose along the cells as a running key. Not a reading.

A running key is a text subtracted from the cells, one letter per cell.
Five texts already in the repo are tried, in both directions. The friendliest
score is compared with shuffled cells against the same text. No letter
string is stored.
"""

from __future__ import annotations

import random
from functools import lru_cache
from pathlib import Path

from engine.dagapeyeff_add import _PROSE, _cells
from engine.alphabet import letters_only, to_ints
from engine.language import ENGLISH_ORDER, get_model

_DATA = Path(__file__).resolve().parent / "data"
_TEXTS = (
    "english.txt",
    "alice_excerpt.txt",
    "neural_train_austen.txt",
    "german_excerpt.txt",
    "neural_audit_wells.txt",
)
_SEED = 20261004
_NULL = 8


def _shifts(text: str) -> list[int]:
    out = []
    for char in text.upper():
        if not ("A" <= char <= "Z"):
            continue
        if char == "J":
            char = "I"
        value = ord(char) - 65
        if value > 8:
            value -= 1
        out.append(value)
    return out


def _quad(plain_cells: list[int], logp: list[float], english: list[int]) -> float:
    counts = [0] * 25
    for cell in plain_cells:
        counts[cell] += 1
    order = sorted(range(25), key=lambda cell: (-counts[cell], cell))
    mapping = [0] * 25
    rank = 0
    for cell in order:
        if counts[cell] == 0:
            continue
        mapping[cell] = english[rank]
        rank += 1
    plain = [mapping[cell] for cell in plain_cells]
    left, mid, right = plain[0], plain[1], plain[2]
    total = 0.0
    for nxt in plain[3:]:
        total += logp[((left * 26 + mid) * 26 + right) * 26 + nxt]
        left, mid, right = mid, right, nxt
    return total / (len(plain) - 3)


def _best(seq: list[int], shifts: list[int], logp: list[float], english: list[int], key_minus_cell: bool) -> float:
    count = len(seq)
    best = float("-inf")
    last = len(shifts) - count
    for offset in range(last + 1):
        window = shifts[offset : offset + count]
        if key_minus_cell:
            plain = [(window[index] - seq[index]) % 25 for index in range(count)]
        else:
            plain = [(seq[index] - window[index]) % 25 for index in range(count)]
        score = _quad(plain, logp, english)
        if score > best:
            best = score
    return best


@lru_cache(maxsize=1)
def running_report() -> dict:
    logp = get_model().logp
    english = [ord(char) - 65 for char in ENGLISH_ORDER]
    cells = _cells()
    best = float("-inf")
    best_text = ""
    best_direction = ""
    alignments = 0
    for name in _TEXTS:
        shifts = _shifts((_DATA / name).read_text(encoding="utf-8"))
        alignments += max(0, len(shifts) - len(cells) + 1) * 2
        for key_minus_cell, direction in ((False, "cell-minus-key"), (True, "key-minus-cell")):
            score = _best(cells, shifts, logp, english, key_minus_cell)
            if score > best:
                best = score
                best_text = name
                best_direction = direction
    winner = _shifts((_DATA / "neural_audit_wells.txt").read_text(encoding="utf-8"))
    drawn = random.Random(_SEED)
    as_high = 0
    for _ in range(_NULL):
        shuffled = cells[:]
        drawn.shuffle(shuffled)
        if _best(shuffled, winner, logp, english, True) >= best:
            as_high += 1
    prose = to_ints(letters_only(_PROSE))
    prose_quad = get_model().score(prose) / (len(prose) - 3)
    return {
        "solved": False,
        "claimed_plaintext": None,
        "texts": len(_TEXTS),
        "alignments": alignments,
        "best_text": best_text,
        "best_direction": best_direction,
        "best_quadgram": round(best, 4),
        "prose_quadgram": round(prose_quad, 4),
        "reaches_prose": best >= prose_quad,
        "null_texts": _NULL,
        "shuffles_as_high": as_high,
        "scope": (
            "A running key from these texts is a score, not a reading. "
            "No letter string is stored."
        ),
    }
