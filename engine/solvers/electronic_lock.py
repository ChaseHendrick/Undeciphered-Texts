"""Headless simulated modern electronic lock.

This module is an in-process model of a short electronic code. The
code is four digits, each an integer from 0 through 9. One code is
planted when the simulator is built. The simulator answers a try with
a boolean only: true when the try is exactly the planted code, false
otherwise. It does not report which digit missed, how close a try
was, or the code itself.

recover_code asks that boolean about codes in numeric order and
returns the first code the simulator accepts. The search space is
10 to the fourth, which is 10,000 tries at most. Nothing in the
search reads the planted code except through that boolean.

This opens only the simulated lock inside the test, not a real safe.
It is not a procedure for a physical keypad, a mounted safe, a
padlock, or any other container. It is not a claim about army
message Nr. 86.
"""

from __future__ import annotations

from collections.abc import Callable

from engine.result import SolveResult

METHOD_NAME = "electronic_lock"
DIGIT_MIN = 0
DIGIT_MAX = 9
CODE_LENGTH = 4
SPACE_SIZE = 10 ** CODE_LENGTH

# One code planted for the published certificate and unit test.
PLANTED_CODE = (4, 8, 1, 6)
PLANTED_CODE_STRING = "4816"

_SCOPE = (
    "This opens only the simulated lock inside the test, not a real "
    "safe. Not a procedure for a physical keypad, a mounted safe, a "
    "padlock, or any other container, and not a claim about Nr. 86."
)

CodeOracle = Callable[[tuple[int, int, int, int]], bool]


def validate_code(code: tuple[int, ...]) -> tuple[int, int, int, int]:
    """Require four integers, each from 0 through 9."""
    if not isinstance(code, tuple) or len(code) != CODE_LENGTH:
        raise ValueError("a try must be a tuple of four digits")
    digits: list[int] = []
    for digit in code:
        if isinstance(digit, bool) or not isinstance(digit, int):
            raise ValueError("each digit must be an integer from 0 through 9")
        if digit < DIGIT_MIN or digit > DIGIT_MAX:
            raise ValueError("each digit must be an integer from 0 through 9")
        digits.append(digit)
    return (digits[0], digits[1], digits[2], digits[3])


def code_string(code: tuple[int, ...]) -> str:
    """Format four digits with no separator, for example 4816."""
    digits = validate_code(code)
    return "".join(str(digit) for digit in digits)


def simulated_electronic_lock(code: tuple[int, ...]) -> CodeOracle:
    """Build an electronic lock whose only output is whether a try matches.

    The planted code is closed over. Callers receive a function of one
    four-digit tuple. That function returns true or false and nothing else.
    """
    planted = validate_code(code)

    def try_code(attempt: tuple[int, int, int, int]) -> bool:
        return validate_code(attempt) == planted

    return try_code


def recover_code(try_code: CodeOracle) -> tuple[int, int, int, int]:
    """Search the simulated electronic lock and return the planted code.

    Order is numeric, from 0000 through 9999. The search stops at the
    first accepted try. It does not inspect the planted value except
    by calling try_code.
    """
    for index in range(SPACE_SIZE):
        guess = (
            (index // 1000) % 10,
            (index // 100) % 10,
            (index // 10) % 10,
            index % 10,
        )
        if try_code(guess):
            return guess
    raise RuntimeError("simulated electronic lock rejected every code")


def solve_electronic_lock(try_code: CodeOracle) -> SolveResult:
    """Recover the planted code of an in-process electronic lock.

    This opens only the simulated lock inside the test, not a real safe.
    """
    found = recover_code(try_code)
    text = code_string(found)
    return SolveResult(
        method=METHOD_NAME,
        plaintext=text,
        key=text,
        score=1.0,
        details={
            "code": text,
            "model": "modern_electronic_code",
            "code_length": CODE_LENGTH,
            "digit_min": DIGIT_MIN,
            "digit_max": DIGIT_MAX,
            "space_size": SPACE_SIZE,
            "oracle": "boolean_match_only",
            "scope": _SCOPE,
        },
    )


__all__ = [
    "CODE_LENGTH",
    "DIGIT_MAX",
    "DIGIT_MIN",
    "METHOD_NAME",
    "PLANTED_CODE",
    "PLANTED_CODE_STRING",
    "SPACE_SIZE",
    "code_string",
    "recover_code",
    "simulated_electronic_lock",
    "solve_electronic_lock",
    "validate_code",
]
