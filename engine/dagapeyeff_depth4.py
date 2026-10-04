"""One more count-move, from the best three-move states only. Not a reading.

Three moves cannot reach English. The states that tie for that best score
are each given every legal fourth move. The positions of the edits are not
stored. A count under the English line is still not a reading.
"""

from __future__ import annotations

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_convert import _rate_balls, chi_ball
from engine.dagapeyeff_edits import _ENGLISH_LINE, _counts, _fast, _symbols


def _layer(start: list[int], moves: int) -> tuple[list[tuple[int, ...]], float]:
    layer = [tuple(start)]
    best = _fast(start)
    for _depth in range(moves):
        seen = set()
        nxt = []
        best = None
        for state in layer:
            for source in range(25):
                if state[source] == 0:
                    continue
                for dest in range(25):
                    if source == dest:
                        continue
                    changed = list(state)
                    changed[source] -= 1
                    changed[dest] += 1
                    key = tuple(changed)
                    if key in seen:
                        continue
                    seen.add(key)
                    nxt.append(key)
                    score = _fast(changed)
                    if best is None or score < best:
                        best = score
        layer = nxt
    return layer, best


def _ball(state: list[int]) -> tuple[float, float]:
    symbols = _symbols()
    expanded = [symbols[index] for index, count in enumerate(state) for _ in range(count)]
    ball = chi_ball(expanded, _rate_balls())
    return float(ball.lo()), float(ball.hi())


@frozen("depth4")
def depth4_report() -> dict:
    layer, best3 = _layer(_counts(), 3)
    band = [state for state in layer if _fast(list(state)) <= best3 + 1e-9]
    seen = set()
    best4 = None
    best_state = None
    under_line = 0
    for state in band:
        for source in range(25):
            if state[source] == 0:
                continue
            for dest in range(25):
                if source == dest:
                    continue
                changed = list(state)
                changed[source] -= 1
                changed[dest] += 1
                key = tuple(changed)
                if key in seen:
                    continue
                seen.add(key)
                score = _fast(changed)
                if score < _ENGLISH_LINE:
                    under_line += 1
                if best4 is None or score < best4:
                    best4 = score
                    best_state = changed
    lo, hi = _ball(best_state)
    return {
        "solved": False,
        "claimed_plaintext": None,
        "tied_after_three": len(band),
        "fourth_states": len(seen),
        "best_chi": round(best4, 4),
        "point_under_line": under_line,
        "ball_lo": round(lo, 6),
        "ball_hi": round(hi, 6),
        "english_line": _ENGLISH_LINE,
        "ball_clears": hi < _ENGLISH_LINE,
        "scope": "A fourth count-move is not a reading. The edited cells are not stored.",
    }
