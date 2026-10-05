"""Reorder the printed groups without moving an even group into an odd place.

That is not a delay of one coordinate, and it is not an order of the old
cells. The last group stays put, because it holds the filler. Shuffled
groups of the same parity get the same routes. No letter string is stored.
"""

from __future__ import annotations

import random

from engine.dagapeyeff_cache import frozen

from engine.alphabet import letters_only, to_ints
from engine.dagapeyeff_add import _PROSE
from engine.dagapeyeff_swarm import CHALLENGE
from engine.language import ENGLISH_ORDER, get_legacy_model

_SEED = 20261004
_NULL = 40
_ROW = "67890"
_COLUMN = "12345"


def _quad(plain_cells: list[int], logp: list[float], english: list[int]) -> float:
    counts = [0] * 25
    for cell in plain_cells:
        counts[cell] += 1
    order = sorted(range(25), key=lambda cell: (-counts[cell], cell))
    mapping = [0] * 25
    rank = 0
    for cell in order:
        if counts[cell] == 0:
            continue
        mapping[cell] = english[rank]
        rank += 1
    plain = [mapping[cell] for cell in plain_cells]
    left, mid, right = plain[0], plain[1], plain[2]
    total = 0.0
    for nxt in plain[3:]:
        total += logp[((left * 26 + mid) * 26 + right) * 26 + nxt]
        left, mid, right = mid, right, nxt
    return total / (len(plain) - 3)


def _split() -> tuple[list[str], list[str], str]:
    groups = CHALLENGE.split()
    if len(groups) != 79 or any(len(group) != 5 for group in groups):
        raise ValueError("the challenge is expected to be 79 groups of five")
    body = groups[:-1]
    even = body[0::2]
    odd = body[1::2]
    return even, odd, groups[-1]


def _rail(groups: list[str], period: int) -> list[str]:
    rows = [[] for _ in range(period)]
    for index, group in enumerate(groups):
        rows[index % period].append(group)
    return [group for row in rows for group in row]


def _join(even: list[str], odd: list[str], tail: str) -> str:
    if len(even) != len(odd):
        raise ValueError("even and odd groups are expected to match once the tail is held out")
    out = []
    for left, right in zip(even, odd):
        out.append(left)
        out.append(right)
    out.append(tail)
    return "".join(out)


def _cells(digits: str) -> list[int] | None:
    if not digits.endswith("000"):
        return None
    body = digits[:-3]
    if len(body) % 2:
        return None
    cells = []
    for index in range(0, len(body), 2):
        row_digit = body[index]
        column_digit = body[index + 1]
        if row_digit not in _ROW or column_digit not in _COLUMN:
            return None
        cells.append(_ROW.index(row_digit) * 5 + _COLUMN.index(column_digit))
    return cells


def _routes(even: list[str], odd: list[str]) -> list[tuple[str, list[str], list[str]]]:
    found = [
        ("identity", even, odd),
        ("reverse-even", list(reversed(even)), odd),
        ("reverse-odd", even, list(reversed(odd))),
        ("reverse-both", list(reversed(even)), list(reversed(odd))),
    ]
    for shift in range(1, len(even)):
        found.append((f"rotate-even-{shift}", even[shift:] + even[:shift], odd))
        found.append((f"rotate-odd-{shift}", even, odd[shift:] + odd[:shift]))
        found.append(
            (
                f"rotate-both-{shift}",
                even[shift:] + even[:shift],
                odd[shift:] + odd[:shift],
            )
        )
    for period in range(2, 16):
        found.append((f"rail-even-{period}", _rail(even, period), odd))
        found.append((f"rail-odd-{period}", even, _rail(odd, period)))
        found.append((f"rail-both-{period}", _rail(even, period), _rail(odd, period)))
    return found


def _best(
    even: list[str],
    odd: list[str],
    tail: str,
    logp: list[float],
    english: list[int],
) -> tuple[float, str, int]:
    best = float("-inf")
    best_name = ""
    kept = 0
    for name, left, right in _routes(even, odd):
        cells = _cells(_join(left, right, tail))
        if cells is None:
            continue
        kept += 1
        score = _quad(cells, logp, english)
        if score > best:
            best = score
            best_name = name
    return best, best_name, kept


@frozen("groups")
def group_report() -> dict:
    logp = get_legacy_model().logp
    english = [ord(char) - 65 for char in ENGLISH_ORDER]
    even, odd, tail = _split()
    menu = len(_routes(even, odd))
    best, name, kept = _best(even, odd, tail, logp, english)
    prose = to_ints(letters_only(_PROSE))
    prose_quad = get_legacy_model().score(prose) / (len(prose) - 3)
    drawn = random.Random(_SEED)
    as_high = 0
    for _ in range(_NULL):
        shuffled_even = even[:]
        shuffled_odd = odd[:]
        drawn.shuffle(shuffled_even)
        drawn.shuffle(shuffled_odd)
        score, _route, _kept = _best(shuffled_even, shuffled_odd, tail, logp, english)
        if score >= best:
            as_high += 1
    return {
        "solved": False,
        "claimed_plaintext": None,
        "even_groups": len(even),
        "odd_groups": len(odd),
        "routes": menu,
        "routes_on_square": kept,
        "best_route": name,
        "best_quadgram": round(best, 4),
        "prose_quadgram": round(prose_quad, 4),
        "reaches_prose": best >= prose_quad,
        "null_texts": _NULL,
        "shuffles_as_high": as_high,
        "scope": "A regrouping of the printed groups is not a reading. No letter string is stored.",
    }
