"""Headless simulated pin-tumbler, wafer, and keypad locks.

Each model plants one secret when it is built. A picker may call only
the yes or no methods below. Those methods return a bool and nothing
else. They do not return the secret, which position missed, or how
close a guess was.

The pin-tumbler model has four pins, one planted binding order, and
one planted cut depth per pin. Depths are integers from 0 through 5.
pin_is_next(index) is true only for the next unset pin in that order.
depth_sets(depth) is true only when depth equals that pin's cut. A
true depth answer records the pin as set. A false answer leaves the
model where it was.

The wafer model is a separate three-position stack. It has its own
planted order and its own lift depths, integers from 0 through 3.
wafer_is_next and lift_sets are the only questions, and they behave
the same way for that stack.

The keypad model plants four digits. code_matches(attempt) is true
only when the whole attempt equals the planted code. A false answer
does not say which digit differs.

recover_pin_tumbler_key, recover_wafer_key, and recover_keypad_code
call only those methods.

This opens only the simulated lock inside the test, not a real lock.
It is not a procedure for a physical pin-tumbler, wafer lock, keypad,
padlock, safe, or any other container. It is not a claim about army
message Nr. 86.
"""

from __future__ import annotations

METHOD_NAME = "lockpicks"

PIN_COUNT = 4
PIN_DEPTH_MIN = 0
PIN_DEPTH_MAX = 5
PLANTED_PIN_BINDING = (2, 0, 3, 1)
PLANTED_PIN_CUTS = (3, 1, 5, 0)
PLANTED_PIN_KEY = "3-1-5-0"

WAFER_COUNT = 3
WAFER_DEPTH_MIN = 0
WAFER_DEPTH_MAX = 3
PLANTED_WAFER_ORDER = (0, 2, 1)
PLANTED_WAFER_LIFTS = (1, 3, 2)
PLANTED_WAFER_KEY = "1-3-2"

KEYPAD_LENGTH = 4
KEYPAD_DIGIT_MIN = 0
KEYPAD_DIGIT_MAX = 9
PLANTED_KEYPAD_DIGITS = (7, 3, 9, 5)
PLANTED_KEYPAD_KEY = "7395"
KEYPAD_SPACE = 10 ** KEYPAD_LENGTH

_SCOPE = (
    "This opens only the simulated lock inside the test, not a real "
    "lock. Not a procedure for a physical pin-tumbler, wafer lock, "
    "keypad, padlock, safe, or any other container, and not a claim "
    "about Nr. 86."
)


def _require_int(value: object, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{label} must be an integer")
    return value


def _validate_order(order: tuple[int, ...], count: int) -> tuple[int, ...]:
    if not isinstance(order, tuple) or len(order) != count:
        raise ValueError("order must be a tuple covering every position once")
    seen: list[int] = []
    for item in order:
        number = _require_int(item, "order entry")
        if number < 0 or number >= count or number in seen:
            raise ValueError("order must be a tuple covering every position once")
        seen.append(number)
    return tuple(seen)


def _validate_depths(
    depths: tuple[int, ...], count: int, depth_min: int, depth_max: int
) -> tuple[int, ...]:
    if not isinstance(depths, tuple) or len(depths) != count:
        raise ValueError("depths must be one integer per position")
    cleaned: list[int] = []
    for item in depths:
        number = _require_int(item, "depth")
        if number < depth_min or number > depth_max:
            raise ValueError("depth is outside this model")
        cleaned.append(number)
    return tuple(cleaned)


def cuts_string(depths: tuple[int, ...]) -> str:
    """Join depths with hyphens, for example 3-1-5-0."""
    if not isinstance(depths, tuple) or not depths:
        raise ValueError("depths must be a non-empty tuple")
    numbers = [_require_int(item, "depth") for item in depths]
    return "-".join(str(number) for number in numbers)


def code_string(digits: tuple[int, ...]) -> str:
    """Join keypad digits with no separator, for example 7395."""
    if not isinstance(digits, tuple) or len(digits) != KEYPAD_LENGTH:
        raise ValueError("a keypad code must be four digits")
    numbers: list[int] = []
    for item in digits:
        number = _require_int(item, "digit")
        if number < KEYPAD_DIGIT_MIN or number > KEYPAD_DIGIT_MAX:
            raise ValueError("a keypad digit must be from 0 through 9")
        numbers.append(number)
    return "".join(str(number) for number in numbers)


def _as_bool(value: object) -> bool:
    if not isinstance(value, bool):
        raise TypeError("model feedback must be a bool")
    return value


class _OrderedStack:
    """In-process stack. Feedback is only whether a guess is exact."""

    def __init__(
        self,
        depths: tuple[int, ...],
        order: tuple[int, ...],
        depth_min: int,
        depth_max: int,
    ) -> None:
        self._depths = _validate_depths(depths, len(depths), depth_min, depth_max)
        self._order = _validate_order(order, len(self._depths))
        self._depth_min = depth_min
        self._depth_max = depth_max
        self._cursor = 0

    def _waiting(self) -> int | None:
        if self._cursor >= len(self._order):
            return None
        return self._order[self._cursor]

    def is_next(self, index: int) -> bool:
        waiting = self._waiting()
        if waiting is None:
            return False
        number = _require_int(index, "index")
        if number < 0 or number >= len(self._depths):
            raise ValueError("index is outside this model")
        return number == waiting

    def sets_at(self, depth: int) -> bool:
        waiting = self._waiting()
        if waiting is None:
            raise RuntimeError("no position is waiting")
        number = _require_int(depth, "depth")
        if number < self._depth_min or number > self._depth_max:
            raise ValueError("depth is outside this model")
        if number != self._depths[waiting]:
            return False
        self._cursor += 1
        return True


class PinTumblerModel:
    """Four simulated pins. Answers are yes or no only."""

    def __init__(
        self,
        cuts: tuple[int, ...] = PLANTED_PIN_CUTS,
        binding_order: tuple[int, ...] = PLANTED_PIN_BINDING,
    ) -> None:
        self._stack = _OrderedStack(
            cuts, binding_order, PIN_DEPTH_MIN, PIN_DEPTH_MAX
        )

    def pin_is_next(self, index: int) -> bool:
        return self._stack.is_next(index)

    def depth_sets(self, depth: int) -> bool:
        return self._stack.sets_at(depth)


class WaferModel:
    """Three simulated wafers. Answers are yes or no only."""

    def __init__(
        self,
        lifts: tuple[int, ...] = PLANTED_WAFER_LIFTS,
        order: tuple[int, ...] = PLANTED_WAFER_ORDER,
    ) -> None:
        self._stack = _OrderedStack(
            lifts, order, WAFER_DEPTH_MIN, WAFER_DEPTH_MAX
        )

    def wafer_is_next(self, index: int) -> bool:
        return self._stack.is_next(index)

    def lift_sets(self, depth: int) -> bool:
        return self._stack.sets_at(depth)


class KeypadModel:
    """Four-digit simulated keypad. The only answer is match or not."""

    def __init__(self, digits: tuple[int, ...] = PLANTED_KEYPAD_DIGITS) -> None:
        self._digits = tuple(int(ch) for ch in code_string(digits))

    def code_matches(self, attempt: tuple[int, ...]) -> bool:
        return tuple(int(ch) for ch in code_string(attempt)) == self._digits


def _search_stack(is_next, sets_depth, count: int, depth_max: int) -> tuple[int, ...]:
    """Ask is_next and sets_depth only. Both must return bool."""
    found: list[int | None] = [None] * count
    unset = set(range(count))
    while unset:
        current: int | None = None
        for index in range(count):
            if index not in unset:
                continue
            if _as_bool(is_next(index)):
                current = index
                break
        if current is None:
            raise RuntimeError("model did not mark a next position")
        matched: int | None = None
        for depth in range(0, depth_max + 1):
            if _as_bool(sets_depth(depth)):
                matched = depth
                break
        if matched is None:
            raise RuntimeError("model rejected every depth")
        found[current] = matched
        unset.remove(current)
    return tuple(int(item) for item in found)


def recover_pin_tumbler_key(model: object) -> str:
    """Recover planted pin cuts using pin_is_next and depth_sets only."""
    is_next = model.pin_is_next
    sets_depth = model.depth_sets
    return cuts_string(_search_stack(is_next, sets_depth, PIN_COUNT, PIN_DEPTH_MAX))


def recover_wafer_key(model: object) -> str:
    """Recover planted wafer lifts using wafer_is_next and lift_sets only."""
    is_next = model.wafer_is_next
    sets_depth = model.lift_sets
    return cuts_string(
        _search_stack(is_next, sets_depth, WAFER_COUNT, WAFER_DEPTH_MAX)
    )


def recover_keypad_code(model: object) -> str:
    """Try codes in order. code_matches is the only feedback."""
    matches = model.code_matches
    for number in range(KEYPAD_SPACE):
        text = f"{number:0{KEYPAD_LENGTH}d}"
        attempt = tuple(int(ch) for ch in text)
        if _as_bool(matches(attempt)):
            return text
    raise RuntimeError("simulated keypad rejected every code")


__all__ = [
    "KEYPAD_LENGTH",
    "KEYPAD_SPACE",
    "METHOD_NAME",
    "PIN_COUNT",
    "PIN_DEPTH_MAX",
    "PLANTED_KEYPAD_DIGITS",
    "PLANTED_KEYPAD_KEY",
    "PLANTED_PIN_BINDING",
    "PLANTED_PIN_CUTS",
    "PLANTED_PIN_KEY",
    "PLANTED_WAFER_KEY",
    "PLANTED_WAFER_LIFTS",
    "PLANTED_WAFER_ORDER",
    "WAFER_COUNT",
    "WAFER_DEPTH_MAX",
    "KeypadModel",
    "PinTumblerModel",
    "WaferModel",
    "code_string",
    "cuts_string",
    "recover_keypad_code",
    "recover_pin_tumbler_key",
    "recover_wafer_key",
]
