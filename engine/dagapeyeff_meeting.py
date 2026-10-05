"""A vertical run of the most common cell meets a horizontal run.

Both runs are three or more cells inside one column or one row. The most
common cell is fixed by the counts. A meeting is a king's move: some cell
of the vertical run is a side or a corner away from some cell of the
horizontal run, and the horizontal run is a different cell. A shuffle of
the cells is the null. No letter string is stored.
"""

from __future__ import annotations

import random
from collections import Counter

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_swarm import challenge_pairs

_SEED = 20261004
_DRAWS = 20000
_WIDTH = 14
_RUN = 3


def _meetings(seq: list[str]) -> tuple[int, str, list[dict]]:
    mode = Counter(seq).most_common(1)[0][0]
    vertical = []
    for column in range(_WIDTH):
        start = 0
        while start < _WIDTH:
            end = start
            while end + 1 < _WIDTH and seq[(end + 1) * _WIDTH + column] == seq[start * _WIDTH + column]:
                end += 1
            if end - start + 1 >= _RUN and seq[start * _WIDTH + column] == mode:
                vertical.append((start, end, column))
            start = end + 1
    horizontal = []
    for row in range(_WIDTH):
        start = 0
        while start < _WIDTH:
            end = start
            while end + 1 < _WIDTH and seq[row * _WIDTH + end + 1] == seq[row * _WIDTH + start]:
                end += 1
            if end - start + 1 >= _RUN and seq[row * _WIDTH + start] != mode:
                horizontal.append((row, start, end, seq[row * _WIDTH + start]))
            start = end + 1
    found = []
    for top, bottom, column in vertical:
        for row, left, right, cell in horizontal:
            touch = False
            for across in range(left, right + 1):
                for down in range(top, bottom + 1):
                    if max(abs(row - down), abs(across - column)) == 1:
                        touch = True
                        break
                if touch:
                    break
            if touch:
                found.append({
                    "mode": mode,
                    "vertical_column": column,
                    "vertical_top": top,
                    "vertical_bottom": bottom,
                    "cell": cell,
                    "row": row,
                    "left": left,
                    "right": right,
                })
    return len(found), mode, found


@frozen("meeting")
def meeting_report() -> dict:
    pairs = list(challenge_pairs())
    count, mode, found = _meetings(pairs)
    drawn = random.Random(_SEED)
    hits = 0
    for _ in range(_DRAWS):
        shuffled = pairs[:]
        drawn.shuffle(shuffled)
        if _meetings(shuffled)[0] >= count:
            hits += 1
    first = found[0]
    return {
        "solved": False,
        "claimed_plaintext": None,
        "mode": mode,
        "meetings": count,
        "vertical_column": first["vertical_column"],
        "vertical_top": first["vertical_top"],
        "vertical_bottom": first["vertical_bottom"],
        "cell": first["cell"],
        "row": first["row"],
        "left": first["left"],
        "right": first["right"],
        "draws": _DRAWS,
        "as_many": hits,
        "scope": "A meeting of two runs is not a reading. No letter string is stored.",
    }
