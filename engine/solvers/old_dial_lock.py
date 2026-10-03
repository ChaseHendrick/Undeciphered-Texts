"""Headless simulated old dial lock.

This module is an in-process model of an old three-number dial. Each
number is an integer from 0 through 99. One combination is planted
when the simulator is built. The simulator answers a try with a
boolean only: true when the try is exactly the planted combination,
false otherwise. It does not report which wheel missed, how close a
try was, or the combination itself.

recover_combination asks that boolean about triples in dial order and
returns the first triple the simulator accepts. The search space is
100 times 100 times 100, which is 1,000,000 tries at most. Nothing in
the search reads the planted combination except through that boolean.

This opens only the simulated lock inside the test, not a real safe.
It is not a procedure for a physical dial, a mounted safe, a padlock,
or any other container. It is not a claim about army message Nr. 86.
"""

from __future__ import annotations

from collections.abc import Callable

from engine.result import SolveResult

METHOD_NAME = "old_dial_lock"
DIAL_MIN = 0
DIAL_MAX = 99
WHEEL_COUNT = 3
SPACE_SIZE = 100 ** WHEEL_COUNT

# One combination planted for the published certificate and unit test.
PLANTED_COMBINATION = (3, 11, 7)
PLANTED_COMBINATION_STRING = "3-11-7"

_SCOPE = (
    "This opens only the simulated lock inside the test, not a real "
    "safe. Not a procedure for a physical dial, a mounted safe, a "
    "padlock, or any other container, and not a claim about Nr. 86."
)

DialOracle = Callable[[tuple[int, int, int]], bool]


def validate_triple(combo: tuple[int, int, int]) -> tuple[int, int, int]:
    """Require three integers, each from 0 through 99."""
    if not isinstance(combo, tuple) or len(combo) != WHEEL_COUNT:
        raise ValueError("a try must be a tuple of three integers")
    numbers: list[int] = []
    for number in combo:
        if isinstance(number, bool) or not isinstance(number, int):
            raise ValueError("each dial number must be an integer from 0 through 99")
        if number < DIAL_MIN or number > DIAL_MAX:
            raise ValueError("each dial number must be an integer from 0 through 99")
        numbers.append(number)
    return (numbers[0], numbers[1], numbers[2])


def combination_string(combo: tuple[int, int, int]) -> str:
    """Format a triple as first-second-third, for example 3-11-7."""
    first, second, third = validate_triple(combo)
    return f"{first}-{second}-{third}"


def simulated_old_dial(combination: tuple[int, int, int]) -> DialOracle:
    """Build an old dial whose only output is whether a try matches.

    The planted combination is closed over. Callers receive a function
    of one triple. That function returns true or false and nothing else.
    """
    planted = validate_triple(combination)

    def try_combination(attempt: tuple[int, int, int]) -> bool:
        return validate_triple(attempt) == planted

    return try_combination


def recover_combination(try_combination: DialOracle) -> tuple[int, int, int]:
    """Search the simulated old dial and return the planted combination.

    Order is the first wheel, then the second, then the third, each
    from 0 through 99. The search stops at the first accepted try.
    It does not inspect the planted value except by calling
    try_combination.
    """
    for first in range(DIAL_MIN, DIAL_MAX + 1):
        for second in range(DIAL_MIN, DIAL_MAX + 1):
            for third in range(DIAL_MIN, DIAL_MAX + 1):
                guess = (first, second, third)
                if try_combination(guess):
                    return guess
    raise RuntimeError("simulated old dial rejected every triple")


def solve_old_dial_lock(try_combination: DialOracle) -> SolveResult:
    """Recover the planted combination of an in-process old dial.

    This opens only the simulated lock inside the test, not a real safe.
    """
    found = recover_combination(try_combination)
    text = combination_string(found)
    return SolveResult(
        method=METHOD_NAME,
        plaintext=text,
        key=text,
        score=1.0,
        details={
            "combination": text,
            "model": "old_three_number_dial",
            "wheels": WHEEL_COUNT,
            "dial_min": DIAL_MIN,
            "dial_max": DIAL_MAX,
            "space_size": SPACE_SIZE,
            "oracle": "boolean_match_only",
            "scope": _SCOPE,
        },
    )


__all__ = [
    "DIAL_MAX",
    "DIAL_MIN",
    "METHOD_NAME",
    "PLANTED_COMBINATION",
    "PLANTED_COMBINATION_STRING",
    "SPACE_SIZE",
    "WHEEL_COUNT",
    "combination_string",
    "recover_combination",
    "simulated_old_dial",
    "solve_old_dial_lock",
    "validate_triple",
]
