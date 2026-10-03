"""Supplied-map Pollux with strict Morse tokens and bounded homophone choices.

ACA source: https://www.cryptogram.org/downloads/aca.info/ciphers/Pollux.pdf
Every decimal digit represents a dot, dash, or divider. The caller supplies
that complete map. This helper performs no unknown-map search.
"""

from __future__ import annotations

from collections.abc import Mapping

from engine.result import SolveResult
from engine.solvers.morbit import _decode_morse, _digit_stream, _encode_morse

ACA_POLLUX_URL = "https://www.cryptogram.org/downloads/aca.info/ciphers/Pollux.pdf"
_DIGITS = "0123456789"
_SYMBOLS = frozenset(".-x")


def pollux_key(key: str | Mapping[str, str]) -> str:
    """Canonical symbols for digits 0..9; all three symbol types must occur."""
    if isinstance(key, str):
        if len(key) != 10:
            raise ValueError("Pollux key must contain ten symbols in digit order 0..9")
        symbols = key
    elif isinstance(key, Mapping):
        if len(key) != 10 or set(key) != set(_DIGITS):
            raise ValueError("Pollux mapping must contain every ASCII digit 0..9 exactly once")
        if any(not isinstance(key[digit], str) or len(key[digit]) != 1 for digit in _DIGITS):
            raise ValueError("each Pollux digit must map to exactly one Morse symbol")
        symbols = "".join(key[digit] for digit in _DIGITS)
    else:
        raise TypeError("Pollux key must be a ten-symbol string or a complete digit mapping")
    if set(symbols) != _SYMBOLS:
        raise ValueError("Pollux digit symbols must use dot '.', dash '-', and divider 'x', with every type present")
    return symbols


def pollux_encrypt(text: str, key: str | Mapping[str, str], *, choices: str | None = None) -> str:
    """Cycle through homophones deterministically, or validate explicit digits.

    Explicit choices contain one valid digit per encoded Morse symbol. They
    reproduce a particular homophonic ciphertext without a random callback.
    """
    symbols = pollux_key(key)
    stream = _encode_morse(text)
    if choices is not None:
        digits = _digit_stream(choices)
        if len(digits) != len(stream) or any(symbols[int(digit)] != symbol for digit, symbol in zip(digits, stream)):
            raise ValueError("Pollux choices must supply one correctly mapped digit for every Morse symbol")
        return digits
    homophones = {symbol: [str(index) for index, value in enumerate(symbols) if value == symbol] for symbol in ".-x"}
    counts = dict.fromkeys(".-x", 0)
    digits = []
    for symbol in stream:
        options = homophones[symbol]
        digits.append(options[counts[symbol] % len(options)])
        counts[symbol] += 1
    return "".join(digits)


def pollux_decrypt(text: str, key: str | Mapping[str, str], *, terminal_period: bool = False) -> str:
    """Recover uppercase text with strict Morse gaps; no trailing divider pads."""
    symbols = pollux_key(key)
    digits = _digit_stream(text, terminal_period=terminal_period)
    return _decode_morse("".join(symbols[int(digit)] for digit in digits))


def solve_pollux(text: str, *, key: str | Mapping[str, str], terminal_period: bool = False) -> SolveResult:
    symbols = pollux_key(key)
    plain = pollux_decrypt(text, symbols, terminal_period=terminal_period)
    return SolveResult("pollux", plain, symbols, float(len(plain.replace(" ", ""))), {
        "mode": "known_key", "digit_symbols": {digit: symbols[int(digit)] for digit in _DIGITS},
        "terminal_period_is_framing": terminal_period, "padding": "none",
        "source_url": ACA_POLLUX_URL,
        "scope": "Supplied-map Pollux only. Homophones do not recover an unknown map; Morse case and whitespace are normalized. No unknown-script decipherment.",
    })


__all__ = ["ACA_POLLUX_URL", "pollux_key", "pollux_encrypt", "pollux_decrypt", "solve_pollux"]
