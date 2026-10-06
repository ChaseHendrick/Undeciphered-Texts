"""A homophonic key under any transposition, judged by counts alone. Not a reading.

A transposition keeps every letter count, and a homophonic key splits each
letter's count among the symbols that stand for it. So a text can become the
cells under some homophonic key and some transposition only if the cells' 18
symbol counts can be grouped, one group a letter, into exactly the text's
letter counts. A text with more than 18 different letters cannot be grouped
at all.

For each window of 196 letters of held-out English and of Latin this probe
records the number of different letters, decides exactly (by backtracking)
whether the counts can be grouped with no error, and finds by local search
the fewest single-cell errors it can reach, which is an upper bound on the
true fewest. No letter string is stored.
"""

from __future__ import annotations

import random
from collections import Counter

from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_cache import frozen

_SEED = 20261023
_LETTERS = 196
_STRIDE = 59


def exact_grouping(symbols: list[int], letters: list[int]) -> bool:
    """True when the symbol counts split into groups whose sums are exactly the letter counts."""
    symbols = sorted(symbols, reverse=True)
    need = sorted(letters, reverse=True)
    if sum(symbols) != sum(need) or len(need) > len(symbols):
        return False

    def place(i: int) -> bool:
        if i == len(symbols):
            return True
        if sum(1 for n in need if n) > len(symbols) - i:
            return False
        tried = set()
        for j, n in enumerate(need):
            if n >= symbols[i] and n not in tried:
                tried.add(n)
                need[j] -= symbols[i]
                if place(i + 1):
                    return True
                need[j] += symbols[i]
        return False

    return place(0)


def fewest_errors(symbols: list[int], letters: list[int], rng: random.Random, restarts: int = 6) -> int | None:
    """Local search over groupings; returns an upper bound on the fewest single-cell errors."""
    sym = sorted(symbols, reverse=True)
    want = sorted(letters, reverse=True)
    m = len(want)
    if m > len(sym):
        return None
    best = None
    for _ in range(restarts):
        assign = list(range(m)) + [rng.randrange(m) for _ in range(len(sym) - m)]
        rng.shuffle(assign)
        sums, size = [0] * m, [0] * m
        for s, a in zip(sym, assign):
            sums[a] += s
            size[a] += 1
        cost = sum(abs(a - b) for a, b in zip(sums, want))
        improved = True
        while improved:
            improved = False
            for i, s in enumerate(sym):
                a = assign[i]
                if size[a] == 1:
                    continue
                for b in range(m):
                    if b == a:
                        continue
                    new = (cost - abs(sums[a] - want[a]) - abs(sums[b] - want[b])
                           + abs(sums[a] - s - want[a]) + abs(sums[b] + s - want[b]))
                    if new < cost:
                        sums[a] -= s; sums[b] += s; size[a] -= 1; size[b] += 1
                        assign[i] = a = b; cost = new; improved = True
            for i in range(len(sym)):
                for j in range(i + 1, len(sym)):
                    a, b = assign[i], assign[j]
                    if a == b:
                        continue
                    d = sym[j] - sym[i]
                    new = (cost - abs(sums[a] - want[a]) - abs(sums[b] - want[b])
                           + abs(sums[a] + d - want[a]) + abs(sums[b] - d - want[b]))
                    if new < cost:
                        sums[a] += d; sums[b] -= d; assign[i], assign[j] = b, a; cost = new; improved = True
        best = cost if best is None else min(best, cost)
    return best // 2


def _summary(texts: list[str], symbols: list[int], rng: random.Random) -> dict:
    distinct, errors, exact = [], [], 0
    for text in texts:
        for start in range(0, len(text) - _LETTERS, _STRIDE):
            letters = list(Counter(text[start:start + _LETTERS]).values())
            distinct.append(len(letters))
            if len(letters) <= len(symbols):
                exact += exact_grouping(symbols, letters)
                errors.append(fewest_errors(symbols, letters, rng))
    errors.sort()
    return {"windows": len(distinct), "fewest_letters": min(distinct),
            "windows_within_18_letters": len(errors), "exact_groupings": exact,
            "fewest_errors_found": errors[0] if errors else None,
            "median_errors_found": errors[len(errors) // 2] if errors else None,
            "within_4_errors": sum(e <= 4 for e in errors)}


@frozen("dagapeyeff-homgroup")
def homgroup_report() -> dict:
    from engine.dagapeyeff_foursquare import _HELD, _held
    from engine.dagapeyeff_latin import texts

    rng = random.Random(_SEED)
    symbols = list(Counter(_cells()).values())
    latin = texts()
    return {"solved": False, "claimed_plaintext": None, "symbols": len(symbols),
            "english": _summary([_held(name) for name in _HELD], symbols, rng),
            "latin": _summary([latin["held"], latin["classical"]], symbols, rng)}
