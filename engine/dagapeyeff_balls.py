"""Ball enclosures for the yardstick. Not a reading.

Each score is a center and a radius. The true value sits inside. The series
for the logarithm is stopped only once the radius is too small to touch the
gap. No letter string is stored.
"""

from __future__ import annotations

from fractions import Fraction

from engine.dagapeyeff_order import _prose
from engine.dagapeyeff_swarm import challenge_pairs

_TERMS = 30
_WIDTH = 14
_LOG2: tuple[Fraction, Fraction] | None = None


class Ball:
    def __init__(self, mid: Fraction, rad: Fraction) -> None:
        if rad < 0:
            raise ValueError("a radius cannot be negative")
        self.mid = mid
        self.rad = rad

    def lo(self) -> Fraction:
        return self.mid - self.rad

    def hi(self) -> Fraction:
        return self.mid + self.rad

    def __add__(self, other: "Ball") -> "Ball":
        return Ball(self.mid + other.mid, self.rad + other.rad)

    def __sub__(self, other: "Ball") -> "Ball":
        return Ball(self.mid - other.mid, self.rad + other.rad)

    def scale(self, factor: Fraction) -> "Ball":
        return Ball(self.mid * factor, self.rad * abs(factor))

    def contains(self, value: Fraction) -> bool:
        return self.lo() <= value <= self.hi()


def _log2_ball() -> tuple[Fraction, Fraction]:
    global _LOG2
    if _LOG2 is not None:
        return _LOG2
    # log(2) = 2 (y + y^3/3 + ...) with y = 1/3. The tail is positive.
    y = Fraction(1, 3)
    y2 = y * y
    power = y
    total = Fraction(0)
    for index in range(_TERMS):
        total += power / (2 * index + 1)
        power *= y2
    tail = power / ((2 * _TERMS + 1) * (1 - y2))
    _LOG2 = (2 * total, 2 * (total + tail))
    return _LOG2


def log_ball(number: int) -> Ball:
    """Natural log of a positive integer, as a center and a radius."""
    if number <= 0:
        raise ValueError("log is only enclosed for a positive integer")
    if number == 1:
        return Ball(Fraction(0), Fraction(0))
    shift = number.bit_length() - 1
    # number / 2^shift is in [1, 2). y = (number - 2^shift) / (number + 2^shift).
    half = 1 << shift
    y = Fraction(number - half, number + half)
    y2 = y * y
    power = y
    total = Fraction(0)
    for index in range(_TERMS):
        total += power / (2 * index + 1)
        power *= y2
    tail = power / ((2 * _TERMS + 1) * (1 - y2)) if y2 != 1 else power
    low = 2 * total
    high = 2 * (total + tail)
    log_low, log_high = _log2_ball()
    low += shift * log_low
    high += shift * log_high
    return Ball((low + high) / 2, (high - low) / 2)


def information_ball(symbols: list[str]) -> Ball:
    """Successive information, enclosed. Relabeling does not change the value."""
    count = len(symbols) - 1
    if count <= 0:
        return Ball(Fraction(0), Fraction(0))
    joint: dict[tuple[str, str], int] = {}
    left: dict[str, int] = {}
    right: dict[str, int] = {}
    for index in range(count):
        first = symbols[index]
        second = symbols[index + 1]
        joint[(first, second)] = joint.get((first, second), 0) + 1
        left[first] = left.get(first, 0) + 1
        right[second] = right.get(second, 0) + 1
    logs = {1: log_ball(1), count: log_ball(count)}
    for bucket in (joint.values(), left.values(), right.values()):
        for seen in bucket:
            if seen not in logs:
                logs[seen] = log_ball(seen)
    score = Ball(Fraction(0), Fraction(0))
    for (first, second), seen in joint.items():
        piece = logs[seen] + logs[count] - logs[left[first]] - logs[right[second]]
        score += piece.scale(Fraction(seen, count))
    return score


def _outgoing_balls(symbols: list[str]) -> list[Ball]:
    count = len(symbols) - 1
    joint: dict[tuple[str, str], int] = {}
    left: dict[str, int] = {}
    right: dict[str, int] = {}
    for index in range(count):
        first = symbols[index]
        second = symbols[index + 1]
        joint[(first, second)] = joint.get((first, second), 0) + 1
        left[first] = left.get(first, 0) + 1
        right[second] = right.get(second, 0) + 1
    needed = {1, count}
    needed.update(joint.values())
    needed.update(left.values())
    needed.update(right.values())
    logs = {seen: log_ball(seen) for seen in needed}
    shares = [Ball(Fraction(0), Fraction(0)) for _ in range(_WIDTH)]
    unit = Fraction(1, count)
    for index in range(count):
        first = symbols[index]
        second = symbols[index + 1]
        seen = joint[(first, second)]
        piece = logs[seen] + logs[count] - logs[left[first]] - logs[right[second]]
        shares[index % _WIDTH] += piece.scale(unit)
    return shares


def _float(ball: Ball) -> dict:
    return {
        "lo": float(ball.lo()),
        "hi": float(ball.hi()),
        "rad": float(ball.rad),
    }


def ball_report() -> dict:
    pairs = list(challenge_pairs())
    cipher = information_ball(pairs)
    english = information_ball(list(_prose("english.txt", len(pairs))))
    german = information_ball(list(_prose("german_excerpt.txt", len(pairs))))
    ordered = information_ball(sorted(pairs))
    outgoing = _outgoing_balls(pairs)
    ranked = sorted(range(_WIDTH), key=lambda column: outgoing[column].mid, reverse=True)
    return {
        "solved": False,
        "claimed_plaintext": None,
        "terms": _TERMS,
        "cipher": _float(cipher),
        "english": _float(english),
        "german": _float(german),
        "sorted": _float(ordered),
        "cipher_below_english": cipher.hi() < english.lo(),
        "cipher_below_german": cipher.hi() < german.lo(),
        "sorted_above_english": ordered.lo() > english.hi(),
        "highest_column": ranked[0],
        "second_column": ranked[1],
        "highest_above_second": outgoing[ranked[0]].lo() > outgoing[ranked[1]].hi(),
        "second_above_rest": outgoing[ranked[1]].lo() > max(
            outgoing[column].hi() for column in ranked[2:]
        ),
        "outgoing_rad_max": max(float(ball.rad) for ball in outgoing),
        "scope": (
            "A ball is a center and a radius. A comparison is kept only when the balls do not meet. "
            "That is not a reading. No letter string is stored."
        ),
    }
