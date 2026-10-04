"""How many count changes the chi-square ball needs. Not a reading.

One move takes a count off one cell and puts it on another. Two moves are
exhaustive. The forged cells are not kept. Clearing the English line would
still not be a reading.
"""

from __future__ import annotations

from engine.dagapeyeff_cache import frozen

from engine.dagapeyeff_convert import _rate_balls, chi_ball
from engine.dagapeyeff_swarm import ENGLISH_25, best_chi_square, challenge_pairs

_ENGLISH_LINE = 24.165
_RATES = tuple(sorted(ENGLISH_25, reverse=True))


def _fast(counts: list[int]) -> float:
    score = 0.0
    for count, rate in zip(sorted(counts, reverse=True), _RATES):
        expected = 196 * rate
        gap = count - expected
        score += gap * gap / expected
    return score


def _symbols() -> list[str]:
    return [row + column for row in "67890" for column in "12345"]


def _counts() -> list[int]:
    symbols = _symbols()
    index = {symbol: place for place, symbol in enumerate(symbols)}
    counts = [0] * 25
    for pair in challenge_pairs():
        counts[index[pair]] += 1
    return counts


def _best_after(start: list[int], moves: int) -> tuple[float, list[int]]:
    layer = [tuple(start)]
    best_score = _fast(start)
    best_state = start[:]
    for _ in range(moves):
        seen = set()
        best_score = None
        best_state = None
        nxt_layer = []
        for state in layer:
            for source in range(25):
                if state[source] == 0:
                    continue
                for dest in range(25):
                    if source == dest:
                        continue
                    nxt = list(state)
                    nxt[source] -= 1
                    nxt[dest] += 1
                    key = tuple(nxt)
                    if key in seen:
                        continue
                    seen.add(key)
                    nxt_layer.append(key)
                    score = _fast(nxt)
                    if best_score is None or score < best_score:
                        best_score = score
                        best_state = nxt
        layer = nxt_layer
    return best_score, best_state


def _as_symbols(counts: list[int]) -> list[str]:
    return [str(index) for index, count in enumerate(counts) for _ in range(count)]


def _greedy_ball(step: int) -> float:
    cells = _symbols()
    current = list(challenge_pairs())
    rates = _rate_balls()
    for _ in range(step):
        best = None
        for index, old in enumerate(current):
            for cell in cells:
                if cell == old:
                    continue
                current[index] = cell
                score = best_chi_square(tuple(current))
                if best is None or score < best[0]:
                    best = (score, index, cell)
            current[index] = old
        _score, index, cell = best
        current[index] = cell
    return float(chi_ball(current, rates).hi())


@frozen("edits")
def edit_report() -> dict:
    start = _counts()
    score_1, _state_1 = _best_after(start, 1)
    score_2, state_2 = _best_after(start, 2)
    rates = _rate_balls()
    ball_2 = chi_ball(_as_symbols(state_2), rates)
    hi_2 = float(ball_2.hi())
    hi_3 = _greedy_ball(3)
    hi_4 = _greedy_ball(4)
    required = 3 if hi_2 > _ENGLISH_LINE else 2
    return {
        "solved": False,
        "claimed_plaintext": None,
        "english_line": _ENGLISH_LINE,
        "depth1_chi": round(score_1, 2),
        "depth2_chi": round(score_2, 2),
        "depth2_ball_hi": round(hi_2, 6),
        "depth2_clears": hi_2 < _ENGLISH_LINE,
        "greedy3_ball_hi": round(hi_3, 6),
        "greedy4_ball_hi": round(hi_4, 6),
        "greedy4_clears": hi_4 < _ENGLISH_LINE,
        "moves_required": required,
        "scope": (
            "Two count-moves are exhaustive and still sit above English. "
            "A fourth greedy edit can clear the frequency line and is not kept. "
            "No letter string is stored."
        ),
    }
