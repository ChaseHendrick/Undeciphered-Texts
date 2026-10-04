"""Dummy-letter schedules from the 1939 book. Not a reading.

The book says a dummy may be every third, fourth, or fifth letter. This
swarm tries every period from 2 to 31 and every phase, on the cells and,
separately, on the digits. The score is the best letter-count fit after
the deletion. A low score is not plaintext, and the letters are not kept.
"""

from __future__ import annotations

import random

from engine.dagapeyeff_swarm import ENGLISH_25, best_chi_square, challenge_pairs
from engine.dagapeyeff_swarm import CONTROL, _pairs

_PERIODS = range(2, 32)
_SEED = 20261004
_DRAWS = 80
_ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
_ROW = set("67890")
_COLUMN = set("12345")


def schedules() -> tuple[tuple[int, int], ...]:
    """One (period, phase) for every dummy position the book-style rule allows."""
    return tuple((period, phase) for period in _PERIODS for phase in range(period))


def drop_cells(pairs: tuple[str, ...], period: int, phase: int) -> tuple[str, ...]:
    return tuple(pair for index, pair in enumerate(pairs) if index % period != phase)


def _challenge_rows() -> list[tuple[int, int, int, float]]:
    pairs = challenge_pairs()
    rows = []
    for period, phase in schedules():
        kept = drop_cells(pairs, period, phase)
        rows.append((period, phase, len(kept), best_chi_square(kept)))
    return rows


def worker_report(worker: int) -> dict:
    """One schedule. Hundreds of these cover the menu. No letter string."""
    menu = schedules()
    if worker < 0 or worker >= len(menu):
        raise IndexError(worker)
    period, phase = menu[worker]
    kept = drop_cells(challenge_pairs(), period, phase)
    return {
        "worker": worker,
        "period": period,
        "phase": phase,
        "kept": len(kept),
        "chi": round(best_chi_square(kept), 2),
        "claimed_plaintext": None,
    }


def _digits() -> str:
    from engine.dagapeyeff_swarm import CHALLENGE, _digits as only_digits

    digits = only_digits(CHALLENGE)
    if not digits.endswith("000"):
        raise ValueError("expected the printed filler")
    return digits[:-3]


def _legal_digit_deletion(period: int, phase: int) -> int | None:
    """Drop every phase digit, then pair. None when the square breaks."""
    digits = _digits()
    kept = "".join(char for index, char in enumerate(digits) if index % period != phase)
    if len(kept) < 2 or len(kept) % 2:
        return None
    pairs = tuple(kept[index:index + 2] for index in range(0, len(kept), 2))
    for pair in pairs:
        if pair[0] not in _ROW or pair[1] not in _COLUMN:
            return None
    return len(pairs)


def search_nulls() -> dict:
    """Score the whole menu, then ask how often English cherry-picks look as good."""
    rows = _challenge_rows()
    best = min(rows, key=lambda row: row[3])
    book = {}
    for period in (3, 4, 5):
        period_rows = [row for row in rows if row[0] == period]
        chosen = min(period_rows, key=lambda row: row[3])
        book[str(period)] = {
            "phase": chosen[1],
            "kept": chosen[2],
            "chi": round(chosen[3], 2),
        }
    drawn = random.Random(_SEED)
    menu = schedules()
    cherry = []
    for _ in range(_DRAWS):
        sample = tuple(drawn.choices(_ALPHABET, weights=ENGLISH_25, k=196))
        lowest = min(best_chi_square(drop_cells(sample, period, phase)) for period, phase in menu)
        cherry.append(lowest)
    ordered = sorted(cherry)
    legal_digits = 0
    digit_trials = 0
    for period, phase in menu:
        digit_trials += 1
        if _legal_digit_deletion(period, phase) is not None:
            legal_digits += 1
    control = _pairs(CONTROL, "ABCDE")
    control_best = min(
        best_chi_square(drop_cells(control, period, phase)) for period, phase in menu
    )
    return {
        "claimed_plaintext": None,
        "solved": False,
        "schedules": len(menu),
        "best_period": best[0],
        "best_phase": best[1],
        "best_kept": best[2],
        "best_chi": round(best[3], 2),
        "book": book,
        "english_cherry_draws": _DRAWS,
        "english_cherry_median": round(ordered[_DRAWS // 2], 2),
        "english_as_high": sum(1 for score in cherry if score >= best[3]),
        "digit_trials": digit_trials,
        "digit_deletions_still_a_square": legal_digits,
        "control_best_chi": round(control_best, 2),
        "scope": (
            "Every period from 2 to 31, every phase. Digit deletions that leave "
            "the 5 by 5 square are counted. The English figure is the best of the "
            "same menu, so a lone low score is not a reading."
        ),
    }
