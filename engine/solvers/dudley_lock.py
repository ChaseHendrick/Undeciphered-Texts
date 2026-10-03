"""Dudley 60-position dial combination reducer.

Published math for the common Dudley dial with 60 marks. Three
unrestricted numbers would be 60 cubed, which is 216,000 candidates.
James Howell's worked example (fetched 2026-10-02) says the discs use
only 10 positions, spaced 6 apart. For the lock in that example the
positions are 2, 8, 14, 20, 26, 32, 38, 44, 50, and 56. He then keeps
only the pairs whose second number is lower than the first:

    9 + 8 + 7 + 6 + 5 + 4 + 3 + 2 + 1 = 45

and he prints that list, beginning 8-2 and ending 56-50. The page
calls 45 the size of the list. It does not mark one pair as the
combination that opened the lock. The check here is that the printed
pair 8-2 is in the generated list and that the list has 45 entries.

Source:

    https://jameshowell.wordpress.com/2010/09/04/hack-a-dudley-lock-in-10-minutes/

This module only enumerates that published pair list from the worked
first position. It is the published math for that example, checked
against one pair the page prints. It is not instructions for a
specific physical lock and not a claim about Nr. 86.
"""

from __future__ import annotations

from engine.result import SolveResult

METHOD_NAME = "dudley_60"
SOURCE_URL = (
    "https://jameshowell.wordpress.com/2010/09/04/"
    "hack-a-dudley-lock-in-10-minutes/"
)
DIAL_POSITIONS = 60
POSITION_STEP = 6
POSITION_COUNT = 10
FULL_BRUTE_FORCE = DIAL_POSITIONS ** 3  # 216000
PUBLISHED_CANDIDATE_COUNT = 45

# Howell's worked first position, and the first pair he prints.
WORKED_FIRST_POSITION = 2
KNOWN_COMBINATION = (8, 2)
KNOWN_COMBINATION_STRING = "8-2"
PUBLISHED_POSITIONS = (2, 8, 14, 20, 26, 32, 38, 44, 50, 56)

_SCOPE = (
    "Published math for the Dudley 60-position dial, checked on one "
    "pair from a worked example (8-2, 45 candidates). Not instructions "
    "for a specific physical lock and not a claim about Nr. 86."
)


def _require_position(first_position: int) -> int:
    if isinstance(first_position, bool) or not isinstance(first_position, int):
        raise ValueError("first position must be an integer from 0 through 59")
    if first_position < 0 or first_position >= DIAL_POSITIONS:
        raise ValueError("first position must be an integer from 0 through 59")
    return first_position


def dial_positions(first_position: int) -> list[int]:
    """Ten dial marks, starting at first_position and stepping by 6.

    Howell: keep adding 6. The worked example starts at 2 and yields
    2, 8, 14, 20, 26, 32, 38, 44, 50, and 56. Values wrap modulo 60.
    """
    first_position = _require_position(first_position)
    positions = [
        (first_position + POSITION_STEP * index) % DIAL_POSITIONS
        for index in range(POSITION_COUNT)
    ]
    if len(set(positions)) != POSITION_COUNT:
        raise RuntimeError("expected 10 distinct dial positions")
    return positions


def reduce_dudley(first_position: int) -> list[tuple[int, int]]:
    """Return the published 45 pairs for this first position.

    Order matches the worked list: second number ascending, then first
    number ascending among values strictly greater than that second.
    The page's 45 entries are these two-number pairs, not three-number
    opening codes.
    """
    positions = dial_positions(first_position)
    combos = [
        (first, second)
        for second in sorted(positions)
        for first in sorted(positions)
        if first > second
    ]
    if len(combos) != PUBLISHED_CANDIDATE_COUNT:
        raise RuntimeError(
            f"expected {PUBLISHED_CANDIDATE_COUNT} candidates, got {len(combos)}"
        )
    return combos


def combination_string(combo: tuple[int, int]) -> str:
    """Format a pair the way the worked list writes it: 8-2."""
    first, second = combo
    return f"{first}-{second}"


def includes_combination(
    combo: tuple[int, int], first_position: int | None = None
) -> bool:
    """True when combo is in the reduced pair list."""
    if first_position is None:
        first_position = WORKED_FIRST_POSITION
    return combo in reduce_dudley(first_position)


def solve_dudley(first_position: int) -> SolveResult:
    """List the reduced pair set. Plaintext is not a script reading."""
    combos = reduce_dudley(first_position)
    lines = [combination_string(combo) for combo in combos]
    return SolveResult(
        method=METHOD_NAME,
        plaintext="\n".join(lines),
        key=str(first_position),
        score=float(len(combos)),
        details={
            "source_url": SOURCE_URL,
            "first_position": first_position,
            "candidate_count": len(combos),
            "full_brute_force": FULL_BRUTE_FORCE,
            "known_combination": KNOWN_COMBINATION_STRING,
            "scope": _SCOPE,
        },
    )
