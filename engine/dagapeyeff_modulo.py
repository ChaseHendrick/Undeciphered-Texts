"""Whether a square digit tracks the grid. Not a reading.

Twenty alignments are scored together. Each uses one digit of the cell,
the row or the column of the 14 by 14 grid, and one of five phases.
A hit is a digit index equal to that position plus the phase, modulo 5.
The score is the best of the twenty, so the phase is not chosen after
looking. The same four digit-and-axis pairs are also scored as whole
tables. A high diagonal with an ordinary table is not a finding.
The solved exercise is the same twenty alignments on its own letters.
No letter string is stored.
"""

from __future__ import annotations

import random

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_swarm import CONTROL, _pairs, challenge_pairs

_SEED = 20261004
_DRAWS = 100000
_EARLY = 20000
_CHI_DRAWS = 20000
_WIDTH = 14
_ROW = "67890"
_COLUMN = "12345"
_FAMILIES = (
    ("column", "x"),
    ("row", "y"),
    ("column", "y"),
    ("row", "x"),
)


def _indexes(cell: str, alphabet: str) -> tuple[int, int]:
    if alphabet == "digits":
        return _ROW.index(cell[0]), _COLUMN.index(cell[1])
    return ord(cell[0]) - 65, ord(cell[1]) - 65


def _best(seq: list[str], alphabet: str) -> tuple[int, str, str, int]:
    buckets = [0] * 20
    for index, cell in enumerate(seq):
        row, column = divmod(index, _WIDTH)
        row_digit, column_digit = _indexes(cell, alphabet)
        digits = (column_digit, row_digit, column_digit, row_digit)
        positions = (column, row, row, column)
        for family, (digit, position) in enumerate(zip(digits, positions)):
            buckets[family * 5 + (digit - position) % 5] += 1
    best = max(buckets)
    winner = buckets.index(best)
    family = winner // 5
    phase = winner % 5
    digit_name, axis = _FAMILIES[family]
    return best, digit_name, axis, phase


def _chi(seq: list[str], alphabet: str) -> float:
    best = 0.0
    for digit_name, axis in _FAMILIES:
        table = [0] * 25
        for index, cell in enumerate(seq):
            row, column = divmod(index, _WIDTH)
            row_digit, column_digit = _indexes(cell, alphabet)
            digit = column_digit if digit_name == "column" else row_digit
            position = column if axis == "x" else row
            table[digit * 5 + position % 5] += 1
        rows = [sum(table[row * 5:(row + 1) * 5]) for row in range(5)]
        columns = [sum(table[row * 5 + column] for row in range(5)) for column in range(5)]
        total = sum(rows)
        score = 0.0
        for row in range(5):
            for column in range(5):
                expected = rows[row] * columns[column] / total
                if expected:
                    gap = table[row * 5 + column] - expected
                    score += gap * gap / expected
        if score > best:
            best = score
    return best


def _as_high(seq: list[str], alphabet: str, observed: int, draws: int, seen: random.Random) -> int:
    count = 0
    for _ in range(draws):
        shuffled = seq[:]
        seen.shuffle(shuffled)
        if _best(shuffled, alphabet)[0] >= observed:
            count += 1
    return count


@frozen("modulo")
def modulo_report() -> dict:
    pairs = list(challenge_pairs())
    hits, digit, axis, phase = _best(pairs, "digits")
    seen = random.Random(_SEED)
    early = _as_high(pairs, "digits", hits, _EARLY, seen)
    later = _as_high(pairs, "digits", hits, _DRAWS - _EARLY, seen)
    as_high = early + later
    observed_chi = _chi(pairs, "digits")
    chi_seen = random.Random(_SEED)
    chi_as_high = 0
    for _ in range(_CHI_DRAWS):
        shuffled = pairs[:]
        chi_seen.shuffle(shuffled)
        if _chi(shuffled, "digits") >= observed_chi - 1e-9:
            chi_as_high += 1
    control = list(_pairs(CONTROL, "ABCDE"))
    control_hits = _best(control, "letters")[0]
    control_as_high = _as_high(control, "letters", control_hits, _CHI_DRAWS, random.Random(_SEED))
    rate = as_high / _DRAWS
    chi_rate = chi_as_high / _CHI_DRAWS
    return {
        "solved": False,
        "claimed_plaintext": None,
        "families": 4,
        "phases": 5,
        "alignments": 20,
        "hits": hits,
        "digit": digit,
        "axis": axis,
        "phase": phase,
        "draws": _DRAWS,
        "as_high": as_high,
        "early_draws": _EARLY,
        "early_as_high": early,
        "chi": round(observed_chi, 4),
        "chi_draws": _CHI_DRAWS,
        "chi_as_high": chi_as_high,
        "control_pairs": len(control),
        "control_hits": control_hits,
        "control_draws": _CHI_DRAWS,
        "control_as_high": control_as_high,
        "allowed": rate < 0.05 and chi_rate < 0.05,
        "scope": "A digit that tracks the grid is not a reading. No letter string is stored.",
    }
