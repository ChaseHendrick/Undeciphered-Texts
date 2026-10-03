"""Known-key M-209 (Hagelin C-38) solver.

The Converter M-209-A is the U.S. Army version of Boris Hagelin's C-38.
Six pin wheels and 27 lug bars produce a keystream. Each letter is then
enciphered with the Beaufort step published for this machine:

    C = (25 + K - P) mod 26
    P = (25 + K - C) mod 26

with A=0. The same function encrypts and decrypts.

The worked example is the one Jean-François Bouchaudy prints for every
M-209 page in this set (fetched 2026-10-02). The internal key is the
"LP" list from TM 11-380 (1944). The external key is PEOPLE. Spaces in
"Attack at dawn" are replaced by Z, which is how the machine enciphers
a space:

  http://www.jfbouch.fr/crypto/m209/WORK/index.html

The formula, the building offsets, and the first keystream values are on
the mathematical page of the same set:

  http://www.jfbouch.fr/crypto/m209/WORK/mathematical.html

This module decrypts only when the pin patterns, lug settings, and
external key are supplied. It is a **known-key historical machine**
solver. It is **not** a break of an unsolved intercept, **not** an
unknown-script reading, and **not** a claim about army message Nr. 86.
"""

from __future__ import annotations

from collections.abc import Sequence

from engine.alphabet import letters_only, reinject
from engine.result import SolveResult

# Worked example (fetched 2026-10-02).
# http://www.jfbouch.fr/crypto/m209/WORK/index.html
BOUCHAUDY_URL = "http://www.jfbouch.fr/crypto/m209/WORK/index.html"
BOUCHAUDY_MATH_URL = "http://www.jfbouch.fr/crypto/m209/WORK/mathematical.html"
BOUCHAUDY_EXTERNAL_KEY = "PEOPLE"
BOUCHAUDY_INDICATOR = "LP"
# "Attack at dawn" with each space replaced by Z, as the page enciphers it.
BOUCHAUDY_PLAINTEXT = "ATTACKZATZDAWN"
BOUCHAUDY_CIPHERTEXT = "WUHDUAJRJQTLRG"
# Grouped the way the page prints them.
BOUCHAUDY_PLAINTEXT_GROUPS = "ATTAC KZATZ DAWN"
BOUCHAUDY_CIPHERTEXT_GROUPS = "WUHDU AJRJQ TLRG"

# Wheel letter order from the same site's computer view. Wheel 2 has no W,
# wheel 3 no WYZ, and so on. Pin position i is the i-th letter of that wheel.
WHEEL_ALPHABETS: tuple[str, ...] = (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "ABCDEFGHIJKLMNOPQRSTUVXYZ",
    "ABCDEFGHIJKLMNOPQRSTUVX",
    "ABCDEFGHIJKLMNOPQRSTU",
    "ABCDEFGHIJKLMNOPQRS",
    "ABCDEFGHIJKLMNOPQ",
)
WHEEL_SIZES: tuple[int, ...] = tuple(len(alphabet) for alphabet in WHEEL_ALPHABETS)

# Gap between the letter in the window and the pin that is effective for
# that setting. Fixed by the M-209's construction (not a daily key).
# http://www.jfbouch.fr/crypto/m209/WORK/mathematical.html
BUILDING_OFFSETS: tuple[int, ...] = (15, 14, 13, 12, 11, 10)

# TM 11-380 indicator LP, as printed on the index page. "_" is inactive.
BOUCHAUDY_PINS: tuple[str, ...] = (
    "AB_D___HI_K_MN____ST_VW___",
    "A__DE_G__JKL__O__RS_U_X__",
    "AB____GH_J_LMN___RSTU_X",
    "__C_EF_HI___MN_P__STU",
    "_B_DEF_HI___MN_P__S",
    "AB_D___H__K__NO_Q",
)
# Drum-bar lugs, wheel numbers 1-6. 0 is the ineffective position.
# Ten bars are set 2-0 (bars 10-19) and six bars are set 0-5 (bars 22-27).
BOUCHAUDY_LUGS: tuple[str, ...] = (
    "3-6",
    "0-6",
    "1-6",
    "1-5",
    "4-5",
    "0-4",
    "0-4",
    "0-4",
    "0-4",
    "2-0",
    "2-0",
    "2-0",
    "2-0",
    "2-0",
    "2-0",
    "2-0",
    "2-0",
    "2-0",
    "2-0",
    "2-5",
    "2-5",
    "0-5",
    "0-5",
    "0-5",
    "0-5",
    "0-5",
    "0-5",
)

_SCOPE = (
    "Known-key historical M-209 (Hagelin C-38) decrypt only; "
    "not a break of an unsolved intercept, not an unknown-script reading, "
    "and not a claim about army message Nr. 86."
)
_SLIDE = 25
_N_BARS = 27
_N_WHEELS = 6


def pins_from_pattern(pattern: str, alphabet: str) -> list[int]:
    """Read one wheel's pin pattern. A letter is active; '_' is inactive."""
    if len(pattern) != len(alphabet):
        raise ValueError(
            f"pin pattern length {len(pattern)} does not match wheel size {len(alphabet)}"
        )
    pins: list[int] = []
    for index, mark in enumerate(pattern):
        if mark == "_":
            pins.append(0)
        elif mark == alphabet[index]:
            pins.append(1)
        else:
            raise ValueError(
                f"pin {mark!r} at position {index} is not '_' or {alphabet[index]!r}"
            )
    return pins


def lugs_from_specs(specs: Sequence[str]) -> list[tuple[int, int]]:
    """Read 27 lug pairs. Each number is a wheel 1-6, or 0 if ineffective."""
    if len(specs) != _N_BARS:
        raise ValueError(f"M-209 has {_N_BARS} lug bars, got {len(specs)}")
    bars: list[tuple[int, int]] = []
    for spec in specs:
        left_text, right_text = spec.split("-")
        left, right = int(left_text), int(right_text)
        if not 0 <= left <= _N_WHEELS or not 0 <= right <= _N_WHEELS:
            raise ValueError(f"lug {spec!r} is outside wheels 0-6")
        if left and left == right:
            raise ValueError(f"lug {spec!r} sets both lugs on the same wheel")
        bars.append((left, right))
    return bars


def _wheel_indexes(external_key: str) -> list[int]:
    """Index of each external-key letter on that wheel's own alphabet."""
    cleaned = letters_only(external_key)
    if len(cleaned) != _N_WHEELS:
        raise ValueError("M-209 external key must be 6 letters, one per wheel")
    indexes: list[int] = []
    for wheel, letter in enumerate(cleaned):
        try:
            indexes.append(WHEEL_ALPHABETS[wheel].index(letter))
        except ValueError as exc:
            raise ValueError(
                f"letter {letter!r} is not on wheel {wheel + 1} ({WHEEL_ALPHABETS[wheel]})"
            ) from exc
    return indexes


def active_pins_at(
    step: int,
    external_indexes: Sequence[int],
    pins: Sequence[Sequence[int]],
) -> list[int]:
    """Six effective pins at letter ``step`` (0-based), after the building offset.

    The wheels advance after the letter is printed, so letter i uses
    position (external index + building offset + i) on each wheel.
    """
    if len(pins) != _N_WHEELS or len(external_indexes) != _N_WHEELS:
        raise ValueError("M-209 needs pin settings and an index for all 6 wheels")
    active: list[int] = []
    for wheel in range(_N_WHEELS):
        size = len(pins[wheel])
        if size != WHEEL_SIZES[wheel]:
            raise ValueError(
                f"wheel {wheel + 1} has {size} pins, expected {WHEEL_SIZES[wheel]}"
            )
        position = (step + external_indexes[wheel] + BUILDING_OFFSETS[wheel]) % size
        active.append(pins[wheel][position])
    return active


def displacement(active: Sequence[int], bars: Sequence[tuple[int, int]]) -> int:
    """How many drum bars shift. A bar with two live lugs still counts once."""
    kicked = 0
    for left, right in bars:
        if (left and active[left - 1]) or (right and active[right - 1]):
            kicked += 1
    return kicked


def m209_keystream(
    length: int,
    external_key: str,
    pin_patterns: Sequence[str],
    lug_specs: Sequence[str],
) -> list[int]:
    """Keystream K for ``length`` letters. The slide of 25 is not included."""
    if length < 1:
        raise ValueError("keystream length must be positive")
    if len(pin_patterns) != _N_WHEELS:
        raise ValueError("M-209 needs 6 pin patterns")
    pins = [
        pins_from_pattern(pattern, WHEEL_ALPHABETS[wheel])
        for wheel, pattern in enumerate(pin_patterns)
    ]
    bars = lugs_from_specs(lug_specs)
    external_indexes = _wheel_indexes(external_key)
    return [
        displacement(active_pins_at(step, external_indexes, pins), bars)
        for step in range(length)
    ]


def m209_transform(
    text: str,
    external_key: str,
    pin_patterns: Sequence[str],
    lug_specs: Sequence[str],
) -> str:
    """Encrypt or decrypt. Non-letters are dropped. The map is an involution."""
    stream = letters_only(text)
    if not stream:
        raise ValueError("text has no letters")
    keystream = m209_keystream(len(stream), external_key, pin_patterns, lug_specs)
    out: list[str] = []
    for plain, kick in zip(stream, keystream):
        value = (_SLIDE + kick - (ord(plain) - 65)) % 26
        out.append(chr(65 + value))
    return "".join(out)


def m209_encrypt(
    text: str,
    external_key: str,
    pin_patterns: Sequence[str],
    lug_specs: Sequence[str],
) -> str:
    """Encrypt with known pins, lugs, and external key."""
    return m209_transform(text, external_key, pin_patterns, lug_specs)


def m209_decrypt(
    text: str,
    external_key: str,
    pin_patterns: Sequence[str],
    lug_specs: Sequence[str],
) -> str:
    """Decrypt with known pins, lugs, and external key. Same map as encrypt."""
    return m209_transform(text, external_key, pin_patterns, lug_specs)


def solve_m209(
    text: str,
    *,
    external_key: str,
    pins: Sequence[str],
    lugs: Sequence[str],
) -> SolveResult:
    """Recover M-209 plaintext when the pin, lug, and external settings are known.

    Known-key historical machine only. Not a break of an unsolved intercept
    and not an unknown-script reading.
    """
    plain_letters = m209_decrypt(text, external_key, pins, lugs)
    rendered = (
        reinject(text, plain_letters)
        if any(not ch.isalpha() for ch in text)
        else plain_letters
    )
    keyword = letters_only(external_key)
    published = (
        keyword == BOUCHAUDY_EXTERNAL_KEY
        and list(pins) == list(BOUCHAUDY_PINS)
        and list(lugs) == list(BOUCHAUDY_LUGS)
    )
    return SolveResult(
        method="m209",
        plaintext=rendered,
        key=keyword,
        score=float(len(plain_letters)),
        details={
            "external_key": keyword,
            "indicator": BOUCHAUDY_INDICATOR if published else "",
            "pins": list(pins),
            "lugs": list(lugs),
            "letters": len(letters_only(text)),
            "mode": "known_key",
            "machine": "M-209 (Hagelin C-38)",
            "scope": _SCOPE,
            "source_url": BOUCHAUDY_URL,
        },
    )


__all__ = [
    "BOUCHAUDY_CIPHERTEXT",
    "BOUCHAUDY_CIPHERTEXT_GROUPS",
    "BOUCHAUDY_EXTERNAL_KEY",
    "BOUCHAUDY_INDICATOR",
    "BOUCHAUDY_LUGS",
    "BOUCHAUDY_MATH_URL",
    "BOUCHAUDY_PINS",
    "BOUCHAUDY_PLAINTEXT",
    "BOUCHAUDY_PLAINTEXT_GROUPS",
    "BOUCHAUDY_URL",
    "BUILDING_OFFSETS",
    "WHEEL_ALPHABETS",
    "active_pins_at",
    "displacement",
    "lugs_from_specs",
    "m209_decrypt",
    "m209_encrypt",
    "m209_keystream",
    "m209_transform",
    "pins_from_pattern",
    "solve_m209",
]
