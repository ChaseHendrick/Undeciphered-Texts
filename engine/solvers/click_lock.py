"""Synthetic click-train lock solver.

The signal is a waveform built in code, not a microphone recording.
One planted three number combination is written as three groups of
clicks. A click is the short sample burst (0.0, 1.0, 0.25, 0.0).
Inside a number, clicks are separated by a short run of zeros. Between
numbers, the run of zeros is longer. The number of clicks in a group
is one more than the dial number, so zero is a single click. Dial
numbers are integers from 0 through 39.

solve_click_lock reads only that sample list. It finds peaks, splits
them on the long gaps, and subtracts one from each group count.

The signals are synthetic and this does not open a real safe. It is
not instructions for a specific physical lock and not a claim about
Nr. 86.
"""

from __future__ import annotations

from engine.result import SolveResult

METHOD_NAME = "synthetic_click_lock"
PLANTED_COMBINATION = (22, 15, 8)
PLANTED_COMBINATION_STRING = "22-15-8"
DIAL_MAX = 39

# One synthetic click. The 1.0 sample is the only peak.
CLICK = (0.0, 1.0, 0.25, 0.0)
WITHIN_SILENCE = 8
BETWEEN_SILENCE = 32
PEAK_LEVEL = 0.9
# Intra-click peak spacing is 12 samples. Inter-number spacing is 36.
SPLIT_GAP = 20

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
    """Format three dial numbers as 22-15-8."""
    first, second, third = _require_combination(combination)
    return f"{first}-{second}-{third}"


def synthesize_clicks(combination: tuple[int, int, int]) -> list[float]:
    """Build a synthetic click waveform for one three number combination.

    The combination is used only to place clicks. Callers that recover
    a combination must pass the returned samples to solve_click_lock
    and must not pass the combination again.
    """
    first, second, third = _require_combination(combination)
    samples: list[float] = []
    for index, number in enumerate((first, second, third)):
        if index:
            samples.extend([0.0] * BETWEEN_SILENCE)
        for click_index in range(number + 1):
            if click_index:
                samples.extend([0.0] * WITHIN_SILENCE)
            samples.extend(CLICK)
    return samples


def planted_click_signal() -> list[float]:
    """Synthetic click train for the one planted combination."""
    return synthesize_clicks(PLANTED_COMBINATION)


def _peak_indexes(signal: list[float]) -> list[int]:
    peaks: list[int] = []
    last = len(signal) - 1
    for index in range(1, last):
        sample = signal[index]
        if sample < PEAK_LEVEL:
            continue
        if sample >= signal[index - 1] and sample > signal[index + 1]:
            peaks.append(index)
    return peaks


def _groups(peaks: list[int]) -> list[int]:
    if not peaks:
        raise ValueError("click signal has no peaks")
    counts = [1]
    for previous, current in zip(peaks, peaks[1:]):
        if current - previous > SPLIT_GAP:
            counts.append(1)
        else:
            counts[-1] += 1
    return counts


def recover_click_combination(signal: list[float]) -> tuple[int, int, int]:
    """Recover three dial numbers from a synthetic click waveform.

    The combination is not an argument. Only the samples are read.
    """
    if not isinstance(signal, list) or not signal:
        raise ValueError("click signal must be a non-empty list of samples")
    if any(isinstance(sample, bool) or not isinstance(sample, (int, float)) for sample in signal):
        raise ValueError("click signal samples must be numbers")
    counts = _groups(_peak_indexes([float(sample) for sample in signal]))
    if len(counts) != 3:
        raise ValueError("click signal must contain exactly three click groups")
    numbers: list[int] = []
    for count in counts:
        number = count - 1
        if number < 0 or number > DIAL_MAX:
            raise ValueError("recovered dial number is outside 0 through 39")
        numbers.append(number)
    return (numbers[0], numbers[1], numbers[2])


def solve_click_lock(signal: list[float]):
    """Solve one synthetic click train. This does not open a real safe."""
    combination = recover_click_combination(signal)
    text = combination_string(combination)
    return SolveResult(
        method=METHOD_NAME,
        plaintext=text,
        key=text,
        score=1.0,
        details={
            "signal_kind": "synthetic_clicks",
            "combination": text,
            "scope": _SCOPE,
        },
    )
