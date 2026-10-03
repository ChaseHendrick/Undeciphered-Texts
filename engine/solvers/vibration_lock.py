"""Synthetic vibration-trace lock solver.

The signal is a numeric trace built in code, not a sensor recording
from a lock or a safe. One planted three number combination is written
as three windows laid end to end. Each window has 128 samples. Dial
number n is the damped sine of frequency n + 1:

    exp(-3 * t / 128) * sin(2 * pi * (n + 1) * t / 128)

Dial numbers are integers from 0 through 39, so the frequencies are
1 through 40. Those bins are distinct on a 128 sample window.

solve_vibration_lock reads only that trace. It splits the trace into
three windows and picks the dial number whose template has the largest
dot product with the window.

The signals are synthetic and this does not open a real safe. It is
not instructions for a specific physical lock and not a claim about
Nr. 86.
"""

from __future__ import annotations

import math

from engine.result import SolveResult

METHOD_NAME = "synthetic_vibration_lock"
PLANTED_COMBINATION = (11, 4, 36)
PLANTED_COMBINATION_STRING = "11-4-36"
DIAL_MAX = 39
WINDOW = 128

_SCOPE = (
    "The signals are synthetic and this does not open a real safe. "
    "Not instructions for a specific physical lock and not a claim "
    "about Nr. 86."
)


def _require_combination(combination: tuple[int, int, int]) -> tuple[int, int, int]:
    if not isinstance(combination, tuple) or len(combination) != 3:
        raise ValueError("combination must be a tuple of three integers")
    checked: list[int] = []
    for number in combination:
        if isinstance(number, bool) or not isinstance(number, int):
            raise ValueError("each dial number must be an integer from 0 through 39")
        if number < 0 or number > DIAL_MAX:
            raise ValueError("each dial number must be an integer from 0 through 39")
        checked.append(number)
    return (checked[0], checked[1], checked[2])


def combination_string(combination: tuple[int, int, int]) -> str:
    """Format three dial numbers as 11-4-36."""
    first, second, third = _require_combination(combination)
    return f"{first}-{second}-{third}"


def _window(number: int) -> list[float]:
    if isinstance(number, bool) or not isinstance(number, int):
        raise ValueError("each dial number must be an integer from 0 through 39")
    if number < 0 or number > DIAL_MAX:
        raise ValueError("each dial number must be an integer from 0 through 39")
    frequency = number + 1
    samples: list[float] = []
    for t in range(WINDOW):
        decay = math.exp(-3.0 * t / WINDOW)
        wave = math.sin(2.0 * math.pi * frequency * t / WINDOW)
        samples.append(decay * wave)
    return samples


def synthesize_vibration(combination: tuple[int, int, int]) -> list[float]:
    """Build a synthetic vibration trace for one three number combination.

    The combination is used only to choose the three window frequencies.
    Callers that recover a combination must pass the returned samples
    to solve_vibration_lock and must not pass the combination again.
    """
    first, second, third = _require_combination(combination)
    trace: list[float] = []
    for number in (first, second, third):
        trace.extend(_window(number))
    return trace


def planted_vibration_signal() -> list[float]:
    """Synthetic vibration trace for the one planted combination."""
    return synthesize_vibration(PLANTED_COMBINATION)


def _best_number(window: list[float]) -> int:
    best_number = 0
    best_score = -1.0
    for number in range(DIAL_MAX + 1):
        template = _window(number)
        score = sum(sample * basis for sample, basis in zip(window, template))
        if score > best_score:
            best_score = score
            best_number = number
    return best_number


def recover_vibration_combination(signal: list[float]) -> tuple[int, int, int]:
    """Recover three dial numbers from a synthetic vibration trace.

    The combination is not an argument. Only the samples are read.
    """
    if not isinstance(signal, list) or not signal:
        raise ValueError("vibration signal must be a non-empty list of samples")
    if any(isinstance(sample, bool) or not isinstance(sample, (int, float)) for sample in signal):
        raise ValueError("vibration signal samples must be numbers")
    expected = WINDOW * 3
    if len(signal) != expected:
        raise ValueError(
            f"vibration signal must contain {expected} samples, three windows of {WINDOW}"
        )
    samples = [float(sample) for sample in signal]
    numbers = tuple(
        _best_number(samples[offset : offset + WINDOW])
        for offset in (0, WINDOW, WINDOW * 2)
    )
    return (numbers[0], numbers[1], numbers[2])


def solve_vibration_lock(signal: list[float]):
    """Solve one synthetic vibration trace. This does not open a real safe."""
    combination = recover_vibration_combination(signal)
    text = combination_string(combination)
    return SolveResult(
        method=METHOD_NAME,
        plaintext=text,
        key=text,
        score=1.0,
        details={
            "signal_kind": "synthetic_vibration",
            "combination": text,
            "scope": _SCOPE,
        },
    )
