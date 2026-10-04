"""Rails, diagonals, and regular deletions. Not a reading.

Deleting every other cell raises successive-symbol dependence, but the text
also gets shorter, and shorter text scores higher. The comparison is
same-length prose, and the same deletion applied to shuffled cells.
No letter string is stored.
"""

from __future__ import annotations

import random

from engine.dagapeyeff_order import _mi, _prose
from engine.dagapeyeff_swarm import challenge_pairs

_SEED = 20261004
_DRAWS = 10000
_RAILS = range(2, 21)
_PERIODS = range(2, 16)


def _rail(pairs: list[str], period: int) -> list[str]:
    rows = [[] for _ in range(period)]
    for index, symbol in enumerate(pairs):
        rows[index % period].append(symbol)
    return [symbol for row in rows for symbol in row]


def _diagonal(pairs: list[str], row_step: int, column_step: int) -> list[str]:
    grid = [pairs[row * 14:(row + 1) * 14] for row in range(14)]
    seen = [[False] * 14 for _ in range(14)]
    out = []
    for row in range(14):
        for column in range(14):
            if seen[row][column]:
                continue
            rr, cc = row, column
            while 0 <= rr < 14 and 0 <= cc < 14 and not seen[rr][cc]:
                seen[rr][cc] = True
                out.append(grid[rr][cc])
                rr += row_step
                cc += column_step
    return out


def _kept(pairs: list[str], period: int, phase: int) -> list[str]:
    return [symbol for index, symbol in enumerate(pairs) if index % period != phase]


def route_report() -> dict:
    pairs = list(challenge_pairs())
    rails = {period: _mi(_rail(pairs, period)) for period in _RAILS}
    best_rail = max(rails, key=rails.get)
    diagonals = {
        f"{row_step},{column_step}": _mi(_diagonal(pairs, row_step, column_step))
        for row_step, column_step in ((1, 1), (1, -1), (2, 1))
    }
    runs = []
    counts: dict[str, int] = {}
    for symbol in pairs:
        counts[symbol] = counts.get(symbol, 0) + 1
    for symbol, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
        runs.extend([symbol] * count)
    english = _prose("english.txt", 400)
    german = _prose("german_excerpt.txt", 400)
    deletions = []
    for period in _PERIODS:
        scores = [_mi(_kept(pairs, period, phase)) for phase in range(period)]
        phase = max(range(period), key=lambda index: scores[index])
        kept = _kept(pairs, period, phase)
        deletions.append({
            "period": period,
            "phase": phase,
            "kept": len(kept),
            "mi": round(scores[phase], 4),
            "english": round(_mi(english[:len(kept)]), 4),
            "german": round(_mi(german[:len(kept)]), 4),
        })
    phase_scores = [_mi(_kept(pairs, 2, phase)) for phase in (0, 1)]
    drawn = random.Random(_SEED)
    as_high = [0, 0]
    best_as_high = 0
    observed_best = max(phase_scores)
    for _ in range(_DRAWS):
        shuffled = pairs[:]
        drawn.shuffle(shuffled)
        trial = [_mi(_kept(shuffled, 2, phase)) for phase in (0, 1)]
        for phase in (0, 1):
            if trial[phase] >= phase_scores[phase] - 1e-15:
                as_high[phase] += 1
        if max(trial) >= observed_best - 1e-15:
            best_as_high += 1
    return {
        "solved": False,
        "claimed_plaintext": None,
        "trials": _DRAWS * 2,
        "best_rail_period": best_rail,
        "best_rail_mi": round(rails[best_rail], 4),
        "rail_14_mi": round(rails[14], 4),
        "best_diagonal": max(diagonals, key=diagonals.get),
        "best_diagonal_mi": round(max(diagonals.values()), 4),
        "run_mi": round(_mi(runs), 4),
        "period2_phase0_mi": round(phase_scores[0], 4),
        "period2_phase1_mi": round(phase_scores[1], 4),
        "period2_kept": 98,
        "english_98_mi": round(_mi(english[:98]), 4),
        "german_98_mi": round(_mi(german[:98]), 4),
        "phase0_as_high": as_high[0],
        "best_phase_as_high": best_as_high,
        "draws": _DRAWS,
        "closest_deletion": min(deletions, key=lambda row: row["english"] - row["mi"]),
        "scope": (
            "A higher score after a deletion is not a reading unless same-length prose "
            "and a shuffled deletion fail to match it. No letter string is stored."
        ),
    }
