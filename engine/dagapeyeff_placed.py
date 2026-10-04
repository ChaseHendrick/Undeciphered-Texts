"""Place the count-matched edits on the printed cells. Not a reading.

Four count-moves can match English letter counts. The positions were not
kept. This puts every such best edit back onto the cells and scores the
order. A shuffled cell order gets the same edits. No letter string is stored.
"""

from __future__ import annotations

import random
from itertools import combinations, permutations, product

from engine.alphabet import letters_only, to_ints
from engine.dagapeyeff_add import _PROSE
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_edits import _counts, _fast, _symbols
from engine.dagapeyeff_swarm import challenge_pairs
from engine.language import ENGLISH_ORDER, get_model

_SEED = 20261004
_DRAWS = 20


def _best_targets() -> list[tuple[int, ...]]:
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


def _mapping(target: tuple[int, ...], english: list[int]) -> list[int]:
    order = sorted(range(25), key=lambda cell: (-target[cell], cell))
    mapping = [0] * 25
    rank = 0
    for cell in order:
        if target[cell] == 0:
            continue
        mapping[cell] = english[rank]
        rank += 1
    return mapping


def _patterns(target: tuple[int, ...], start: tuple[int, ...]) -> tuple[list[list[tuple[int, ...]]], tuple[int, ...]]:
    groups = []
    slots: list[int] = []
    for symbol, count in enumerate(target):
        delta = count - start[symbol]
        if delta < 0:
            groups.append(symbol)
        elif delta > 0:
            slots.extend([symbol] * delta)
    return groups, tuple(slots)


def _best_order(
    cells: list[int],
    targets: list[tuple[int, ...]],
    start: tuple[int, ...],
    logp: list[float],
    english: list[int],
) -> tuple[float, int]:
    best = float("-inf")
    scored = 0
    length = len(cells)
    span = length - 3
    positions = [[] for _ in range(25)]
    for index, cell in enumerate(cells):
        positions[cell].append(index)
    for target in targets:
        mapping = _mapping(target, english)
        plain = [mapping[cell] for cell in cells]
        windows = []
        left, mid, right = plain[0], plain[1], plain[2]
        for nxt in plain[3:]:
            windows.append(logp[((left * 26 + mid) * 26 + right) * 26 + nxt])
            left, mid, right = mid, right, nxt
        base = sum(windows)
        losers, slots = _patterns(target, start)
        groups = []
        for symbol in losers:
            lose = start[symbol] - target[symbol]
            groups.append(list(combinations(positions[symbol], lose)))
        assigns = list(set(permutations(slots)))
        for choice in product(*groups):
            picks = [index for group in choice for index in group]
            affected = []
            seen = set()
            for index in picks:
                for start_at in range(max(0, index - 3), min(index, span - 1) + 1):
                    if start_at not in seen:
                        seen.add(start_at)
                        affected.append(start_at)
            for assign in assigns:
                old = [plain[index] for index in picks]
                for index, symbol in zip(picks, assign):
                    plain[index] = mapping[symbol]
                score = base
                for start_at in affected:
                    a, b, c, d = plain[start_at : start_at + 4]
                    score += logp[((a * 26 + b) * 26 + c) * 26 + d] - windows[start_at]
                if score > best:
                    best = score
                for index, letter in zip(picks, old):
                    plain[index] = letter
                scored += 1
    return best / span, scored


@frozen("placed")
def placed_report() -> dict:
    logp = get_model().logp
    english = [ord(char) - 65 for char in ENGLISH_ORDER]
    start = tuple(_counts())
    targets = _best_targets()
    cells = _cells()
    best, scored = _best_order(cells, targets, start, logp, english)
    prose = to_ints(letters_only(_PROSE))
    prose_score = get_model().score(prose) / (len(prose) - 3)
    drawn = random.Random(_SEED)
    as_high = 0
    for _ in range(_DRAWS):
        shuffled = cells[:]
        drawn.shuffle(shuffled)
        shuffle_best, _count = _best_order(shuffled, targets, start, logp, english)
        if shuffle_best >= best:
            as_high += 1
    return {
        "solved": False,
        "claimed_plaintext": None,
        "targets": len(targets),
        "placements": scored,
        "best_quadgram": round(best, 4),
        "prose_quadgram": round(prose_score, 4),
        "reaches_prose": best >= prose_score,
        "draws": _DRAWS,
        "shuffles_as_high": as_high,
        "scope": "Placing a count-matched edit is not a reading. No letter string is stored.",
    }
