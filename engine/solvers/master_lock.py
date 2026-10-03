"""Master Lock 1500-style combination reducer.

Published math for the common 40-position Master combination dial
(the 1500 family and the same wheel layout). The dial has positions
0 through 39, so three unrestricted numbers would be 40 cubed, which
is 64,000 candidates. The published reduction does not search that
space. Given the third number, the first number is one of the 10
positions with the same remainder modulo 4, and the second number is
one of the 10 positions whose remainder is 2 more modulo 4. That is
10 times 10 times 1, which is 100 candidates.

Source, fetched 2026-10-02. Jon Westfall, "Recovering Master Lock
Combinations: Guide & Combination List" (assembled 2007, portions
from Liam Bowen):

    https://jonwestfall.com/wp-content/uploads/2007/08/mlock1.pdf

Westfall's worked case uses third number 19 (19 mod 4 is 3). The
first numbers are 3, 7, 11, 15, 19, 23, 27, 31, 35, and 39. The
second numbers are those values plus 2, wrapping past 39, namely
5, 9, 13, 17, 21, 25, 29, 33, 37, and 1. He marks 7-9-19 as the
actual combination of that lock, and he states the list is one
hundred combinations rather than 64,000.

This module only enumerates that residue-class set from a third
number already in hand. It is the published math reduction for that
lock family, checked on one known combination. It is not instructions
for a specific physical lock and not a claim about Nr. 86.
"""

from __future__ import annotations

from engine.result import SolveResult

METHOD_NAME = "master_lock_1500"
SOURCE_URL = "https://jonwestfall.com/wp-content/uploads/2007/08/mlock1.pdf"
DIAL_POSITIONS = 40
FULL_BRUTE_FORCE = DIAL_POSITIONS ** 3  # 64000
PUBLISHED_CANDIDATE_COUNT = 100

# Westfall's published known combination, written as in the guide.
KNOWN_COMBINATION = (7, 9, 19)
KNOWN_COMBINATION_STRING = "7-9-19"
KNOWN_THIRD = 19

_SCOPE = (
    "Published math reduction for the Master Lock 1500-style dial "
    "family, checked on one known combination. Not instructions for "
    "a specific physical lock and not a claim about Nr. 86."
)


def _require_third(third: int) -> int:
    if isinstance(third, bool) or not isinstance(third, int):
        raise ValueError("third number must be an integer from 0 through 39")
    if third < 0 or third >= DIAL_POSITIONS:
        raise ValueError("third number must be an integer from 0 through 39")
    return third


def first_numbers(third: int) -> list[int]:
    """Ten dial positions congruent to the third number modulo 4."""
    third = _require_third(third)
    residue = third % 4
    return list(range(residue, DIAL_POSITIONS, 4))


def second_numbers(third: int) -> list[int]:
    """Ten dial positions two steps off the third number modulo 4.

    Westfall: add 2 to each possible first number and wrap at 40.
    Because -2 and +2 are the same remainder modulo 4, this is the
    single residue class (third + 2) mod 4.
    """
    third = _require_third(third)
    residue = (third + 2) % 4
    return list(range(residue, DIAL_POSITIONS, 4))


def reduce_master_lock(third: int) -> list[tuple[int, int, int]]:
    """Return the published 100-candidate set for this third number.

    Order is first number ascending, then second number ascending.
    The third number is fixed. This is not a scan of all 64,000
    dial triples.
    """
    third = _require_third(third)
    combos = [
        (first, second, third)
        for first in first_numbers(third)
        for second in second_numbers(third)
    ]
    if len(combos) != PUBLISHED_CANDIDATE_COUNT:
        raise RuntimeError(
            f"expected {PUBLISHED_CANDIDATE_COUNT} candidates, got {len(combos)}"
        )
    return combos


def combination_string(combo: tuple[int, int, int]) -> str:
    """Format a triple the way the Westfall guide writes it: 7-9-19."""
    first, second, third = combo
    return f"{first}-{second}-{third}"


def includes_combination(
    combo: tuple[int, int, int], third: int | None = None
) -> bool:
    """True when combo is in the reduced set for its third number."""
    first, second, known_third = combo
    if third is None:
        third = known_third
    if known_third != third:
        return False
    return combo in reduce_master_lock(third)


def solve_master_lock(third: int) -> SolveResult:
    """List the reduced candidate set. Plaintext is not a script reading."""
    combos = reduce_master_lock(third)
    lines = [combination_string(combo) for combo in combos]
    return SolveResult(
        method=METHOD_NAME,
        plaintext="\n".join(lines),
        key=str(third),
        score=float(len(combos)),
        details={
            "source_url": SOURCE_URL,
            "third_number": third,
            "candidate_count": len(combos),
            "full_brute_force": FULL_BRUTE_FORCE,
            "known_combination": KNOWN_COMBINATION_STRING,
            "scope": _SCOPE,
        },
    )
