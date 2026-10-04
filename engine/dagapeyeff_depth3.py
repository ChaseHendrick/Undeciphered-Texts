"""Every three-move change of the cell counts. Not a reading.

Two moves were already exhausted. This exhausts the third. The changed
cells are not kept. A count that reaches English is still not a reading.
"""

from __future__ import annotations

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_convert import _rate_balls, chi_ball
from engine.dagapeyeff_edits import _ENGLISH_LINE, _counts, _fast, _symbols


def _best_state(start: list[int]) -> tuple[float, list[int], int]:
    layer = [tuple(start)]
    best_score = _fast(start)
    best_state = start[:]
    for _depth in range(3):
        seen = set()
        best_score = None
        best_state = None
        nxt = []
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
                    if best_score is None or score < best_score:
                        best_score = score
                        best_state = changed
        layer = nxt
    return best_score, best_state, len(layer)


@frozen("depth3")
def depth3_report() -> dict:
    score, state, states = _best_state(_counts())
    symbols = _symbols()
    expanded = [symbols[index] for index, count in enumerate(state) for _ in range(count)]
    ball = chi_ball(expanded, _rate_balls())
    hi = float(ball.hi())
    lo = float(ball.lo())
    return {
        "solved": False,
        "claimed_plaintext": None,
        "moves": 3,
        "states": states,
        "best_chi": round(score, 4),
        "ball_lo": round(lo, 6),
        "ball_hi": round(hi, 6),
        "english_line": _ENGLISH_LINE,
        "clears": hi < _ENGLISH_LINE,
        "scope": "Three count-moves are not a reading. The changed cells are not stored.",
    }
