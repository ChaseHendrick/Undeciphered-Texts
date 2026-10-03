"""Simplex five-button combination enumerator.

Published count for the Simplex 9600 style lock: five buttons, each
used at most once, pressed either alone or together with others, in
an ordered series of presses. Patrick Ekman (fetched 2026-10-02)
tables 18 patterns whose sizes sum to 1081, and he names the factory
default "2+4, 3" (buttons 2 and 4 together, then button 3).

A first glance that only counts sequences of all five buttons, with
no simultaneous presses, is 5 factorial, which is 120. The published
set is the larger figure, 1081, because shorter codes and simultaneous
presses are allowed. This module enumerates that set. It does not
search a 64,000-dial space.

Source:

    https://ekman.cx/articles/simplex_locks/

The check is that the factory default string is in the set and that
the set has 1081 entries, matching the table total on that page.
This is published math checked on one known combination. It is not instructions
for a specific physical lock and not a claim about Nr. 86.
"""

from __future__ import annotations

from itertools import permutations

from engine.result import SolveResult

METHOD_NAME = "simplex_9600"
SOURCE_URL = "https://ekman.cx/articles/simplex_locks/"
BUTTONS = (1, 2, 3, 4, 5)
PUBLISHED_CANDIDATE_COUNT = 1081
# Page: using every button once, in sequence only, is 120.
SEQUENCE_ONLY_ALL_FIVE = 120

# Factory default, written as on the page.
KNOWN_COMBINATION_STRING = "2+4, 3"

_SCOPE = (
    "Published math for the five-button Simplex combination set, "
    "checked on one known combination (factory default 2+4, 3, "
    "1081 candidates). Not instructions for a specific physical lock "
    "and not a claim about Nr. 86."
)


def _groupings(sequence: tuple[int, ...]) -> list[tuple[tuple[int, ...], ...]]:
    """Ordered splits of sequence into non-empty contiguous groups.

    A simultaneous group is the same press in any button order, so a
    group is kept only when its buttons are strictly increasing. That
    is the page's rule that 1+2 is the same press as 2+1.
    """
    found: list[tuple[tuple[int, ...], ...]] = []

    def walk(start: int, acc: list[tuple[int, ...]]) -> None:
        if start == len(sequence):
            found.append(tuple(acc))
            return
        for end in range(start + 1, len(sequence) + 1):
            group = sequence[start:end]
            if len(group) > 1 and tuple(group) != tuple(sorted(group)):
                continue
            walk(end, acc + [tuple(group)])

    walk(0, [])
    return found


def combination_string(groups: tuple[tuple[int, ...], ...]) -> str:
    """Format presses as on the page: 2+4, 3."""
    parts = ["+".join(str(button) for button in group) for group in groups]
    return ", ".join(parts)


def reduce_simplex() -> list[str]:
    """Return the published 1081 combination strings, in sorted order.

    Sorted order is only so the list is stable. The page does not
    prescribe an order. Each string uses each of buttons 1 through 5
    at most once.
    """
    seen: set[str] = set()
    for length in range(1, len(BUTTONS) + 1):
        for sequence in permutations(BUTTONS, length):
            for groups in _groupings(sequence):
                seen.add(combination_string(groups))
    combos = sorted(seen)
    if len(combos) != PUBLISHED_CANDIDATE_COUNT:
        raise RuntimeError(
            f"expected {PUBLISHED_CANDIDATE_COUNT} candidates, got {len(combos)}"
        )
    return combos


def includes_combination(combo: str) -> bool:
    """True when combo is one of the published 1081 strings."""
    return combo in reduce_simplex()


def solve_simplex() -> SolveResult:
    """List the published combination set. Plaintext is not a script reading."""
    combos = reduce_simplex()
    return SolveResult(
        method=METHOD_NAME,
        plaintext="\n".join(combos),
        key="factory",
        score=float(len(combos)),
        details={
            "source_url": SOURCE_URL,
            "candidate_count": len(combos),
            "sequence_only_all_five": SEQUENCE_ONLY_ALL_FIVE,
            "known_combination": KNOWN_COMBINATION_STRING,
            "scope": _SCOPE,
        },
    )
