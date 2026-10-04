"""What the best count repairs have in common. Not a reading.

Four count-moves can match English counts. The 70 vectors that tie for the
best score are compared as count changes, not as letters. A separate pass
asks whether four neighbor edits, chosen to raise the order score, beat a
shuffle. No letter string is stored.
"""

from __future__ import annotations

import random

from engine.alphabet import letters_only, to_ints
from engine.dagapeyeff_add import _PROSE
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_edits import _counts, _fast, _symbols
from engine.dagapeyeff_swarm import challenge_pairs
from engine.language import ENGLISH_ORDER, get_model

_SEED = 20261004


def _targets() -> list[tuple[int, ...]]:
    start = _counts()
    layer = [tuple(start)]
    best3 = None
    for _depth in range(3):
        seen = set()
        nxt = []
        best3 = None
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
                    if best3 is None or score < best3:
                        best3 = score
        layer = nxt
    band = [state for state in layer if _fast(list(state)) <= best3 + 1e-9]
    best4 = None
    found: list[tuple[int, ...]] = []
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
                score = _fast(changed)
                if best4 is None or score < best4 - 1e-12:
                    best4 = score
                    found = [tuple(changed)]
                elif abs(score - best4) <= 1e-12:
                    found.append(tuple(changed))
    return list(set(found))


def _cells() -> list[int]:
    symbols = _symbols()
    index = {symbol: place for place, symbol in enumerate(symbols)}
    return [index[pair] for pair in challenge_pairs()]


def _quad(seq: list[int], logp: list[float], english: list[int]) -> float:
    counts = [0] * 25
    for cell in seq:
        counts[cell] += 1
    order = sorted(range(25), key=lambda cell: (-counts[cell], cell))
    mapping = [0] * 25
    rank = 0
    for cell in order:
        if counts[cell] == 0:
            continue
        mapping[cell] = english[rank]
        rank += 1
    plain = [mapping[cell] for cell in seq]
    left, mid, right = plain[0], plain[1], plain[2]
    total = 0.0
    for nxt in plain[3:]:
        total += logp[((left * 26 + mid) * 26 + right) * 26 + nxt]
        left, mid, right = mid, right, nxt
    return total / (len(plain) - 3)


def _neighbors(cell: int) -> list[int]:
    row, column = divmod(cell, 5)
    found = []
    for d_row, d_column in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        next_row, next_column = row + d_row, column + d_column
        if 0 <= next_row < 5 and 0 <= next_column < 5:
            found.append(next_row * 5 + next_column)
    return found


def _greedy(seq: list[int], steps: int, adjacent: bool, logp: list[float], english: list[int]) -> float:
    current = seq[:]
    for _step in range(steps):
        best = None
        for index, old in enumerate(current):
            choices = _neighbors(old) if adjacent else range(25)
            for symbol in choices:
                if symbol == old:
                    continue
                current[index] = symbol
                score = _quad(current, logp, english)
                if best is None or score > best[0]:
                    best = (score, index, symbol)
                current[index] = old
        _score, index, symbol = best
        current[index] = symbol
    return _quad(current, logp, english)


def _one(seq: list[int], logp: list[float], english: list[int]) -> float:
    best = _quad(seq, logp, english)
    current = seq[:]
    for index, old in enumerate(current):
        for symbol in _neighbors(old):
            current[index] = symbol
            score = _quad(current, logp, english)
            if score > best:
                best = score
            current[index] = old
    return best


@frozen("repair")
def repair_report() -> dict:
    start = _counts()
    targets = _targets()
    union: set[int] = set()
    shared: set[int] = set(range(25))
    losses: set[int] = set()
    gains: set[int] = set()
    touched = []
    for target in targets:
        changed = [index for index, count in enumerate(start) if target[index] != count]
        touched.append(len(changed))
        union.update(changed)
        shared &= set(changed)
        for index, count in enumerate(start):
            if target[index] < count:
                losses.add(index)
            elif target[index] > count:
                gains.add(index)
    shared_index = next(iter(shared))
    roles = []
    for target in targets:
        delta = target[shared_index] - start[shared_index]
        roles.append("loss" if delta < 0 else "gain")
    shared_role = roles[0] if len(set(roles)) == 1 else "mixed"
    symbols = _symbols()
    logp = get_model().logp
    english = [ord(char) - 65 for char in ENGLISH_ORDER]
    cells = _cells()
    prose = to_ints(letters_only(_PROSE))
    prose_score = get_model().score(prose) / (len(prose) - 3)
    neighbor = _greedy(cells, 4, True, logp, english)
    free = _greedy(cells, 4, False, logp, english)
    one = _one(cells, logp, english)
    drawn = random.Random(_SEED)
    neighbor_high = 0
    free_high = 0
    one_high = 0
    for draw in range(80):
        shuffled = cells[:]
        drawn.shuffle(shuffled)
        if _greedy(shuffled, 4, True, logp, english) >= neighbor:
            neighbor_high += 1
        if draw < 40 and _greedy(shuffled, 4, False, logp, english) >= free:
            free_high += 1
        if _one(shuffled, logp, english) >= one:
            one_high += 1
    return {
        "solved": False,
        "claimed_plaintext": None,
        "targets": len(targets),
        "touched_each": touched[0],
        "touched_same": len(set(touched)) == 1,
        "union": len(union),
        "intersection": len(shared),
        "shared_symbol": symbols[shared_index],
        "shared_role": shared_role,
        "loss_symbols": len(losses),
        "gain_symbols": len(gains),
        "transfer": 4,
        "neighbor_quadgram": round(neighbor, 4),
        "neighbor_draws": 80,
        "neighbor_shuffles_as_high": neighbor_high,
        "free_quadgram": round(free, 4),
        "free_draws": 40,
        "free_shuffles_as_high": free_high,
        "one_quadgram": round(one, 4),
        "one_draws": 80,
        "one_shuffles_as_high": one_high,
        "prose_quadgram": round(prose_score, 4),
        "reaches_prose": max(neighbor, free, one) >= prose_score,
        "scope": "A shared count change is not a reading. No letter string is stored.",
    }
