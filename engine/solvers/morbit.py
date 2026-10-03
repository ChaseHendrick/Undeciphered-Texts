"""Supplied-key Morbit with strict Morse parsing and explicit framing.

ACA source: https://www.cryptogram.org/downloads/aca.info/ciphers/Morbit.pdf
Pairs of dot, dash, and divider symbols map to nine ranked key digits.
This recovers supplied-key examples, not an unknown script or unknown key.
"""

from __future__ import annotations

from engine.result import SolveResult
from engine.solvers.fractionated_morse import _MORSE, _MORSE_TO_CHAR

ACA_MORBIT_URL = "https://www.cryptogram.org/downloads/aca.info/ciphers/Morbit.pdf"
MAX_PLAINTEXT_CHARS = 10_000
MAX_CIPHERTEXT_CHARS = 100_000
_ASCII_LETTERS = frozenset("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
_DIGITS = "0123456789"
_PAIRS = tuple(left + right for left in ".-x" for right in ".-x")


def _text(value: str, name: str, maximum: int) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if not 1 <= len(value) <= maximum:
        raise ValueError(f"{name} must contain 1..{maximum} characters")


def _digit_stream(text: str, *, terminal_period: bool = False) -> str:
    """Only whitespace groups digits; an explicitly allowed final period frames."""
    if not isinstance(terminal_period, bool):
        raise TypeError("terminal_period must be a boolean")
    _text(text, "ciphertext", MAX_CIPHERTEXT_CHARS)
    body = text.strip()
    if terminal_period and body.endswith("."):
        body = body[:-1]
    if any(ch not in _DIGITS and not ch.isspace() for ch in body):
        raise ValueError("ciphertext must contain ASCII digits and whitespace; permit a final framing period explicitly")
    digits = "".join(ch for ch in body if ch in _DIGITS)
    if not digits:
        raise ValueError("ciphertext must contain at least one ASCII digit")
    return digits


def _encode_morse(text: str) -> str:
    _text(text, "plaintext", MAX_PLAINTEXT_CHARS)
    words = []
    for word in text.split():
        symbols = []
        for character in word:
            if character not in _ASCII_LETTERS and character not in _MORSE:
                raise ValueError(f"unsupported Morse plaintext character: {character!r}")
            code = _MORSE.get(character.upper())
            if code is None:
                raise ValueError(f"unsupported Morse plaintext character: {character!r}")
            symbols.append(code)
        words.append("x".join(symbols))
    if not words:
        raise ValueError("plaintext must contain encodable Morse characters")
    return "xx".join(words)


def _decode_morse(stream: str, *, allow_padding: bool = False) -> str:
    """No empty tokens or skipped invalid codes; Morbit allows one padding x."""
    if allow_padding and stream.endswith("x"):
        stream = stream[:-1]
    if not stream or stream.startswith("x") or stream.endswith("x") or "xxx" in stream:
        raise ValueError("Morse separators must be one x between characters and two between words, with no boundary gap")
    decoded = []
    for word in stream.split("xx"):
        letters = []
        for token in word.split("x"):
            character = _MORSE_TO_CHAR.get(token)
            if character is None:
                raise ValueError(f"invalid or missing Morse token: {token!r}")
            letters.append(character)
        decoded.append("".join(letters))
    return " ".join(decoded)


def morbit_key(key: str) -> str:
    """Rank nine ASCII keyword letters, or accept a permutation of digits 1..9."""
    _text(key, "Morbit key", 9)
    if len(key) != 9:
        raise ValueError("Morbit key must contain exactly nine ASCII letters or nine distinct digits 1..9")
    if set(key) == set("123456789"):
        return key
    if any(ch not in _ASCII_LETTERS for ch in key):
        raise ValueError("Morbit keyword must contain exactly nine ASCII letters")
    key = key.upper()
    ranks = [0] * 9
    for rank, index in enumerate(sorted(range(9), key=lambda index: (key[index], index)), 1):
        ranks[index] = rank
    return "".join(map(str, ranks))


def morbit_encrypt(text: str, key: str) -> str:
    """Encode Morse pairs; one final x pads an odd-length Morse stream."""
    ranks = morbit_key(key)
    stream = _encode_morse(text)
    if len(stream) % 2:
        stream += "x"
    table = dict(zip(_PAIRS, ranks))
    return "".join(table[stream[index:index + 2]] for index in range(0, len(stream), 2))


def morbit_decrypt(text: str, key: str, *, terminal_period: bool = False) -> str:
    """Decode with a supplied key, recovering uppercase Morse text and spaces."""
    table = dict(zip(morbit_key(key), _PAIRS))
    digits = _digit_stream(text, terminal_period=terminal_period)
    if "0" in digits:
        raise ValueError("Morbit ciphertext uses only digits 1..9")
    return _decode_morse("".join(table[digit] for digit in digits), allow_padding=True)


def solve_morbit(text: str, *, key: str, terminal_period: bool = False) -> SolveResult:
    ranks = morbit_key(key)
    plain = morbit_decrypt(text, ranks, terminal_period=terminal_period)
    return SolveResult("morbit", plain, ranks, float(len(plain.replace(" ", ""))), {
        "mode": "known_key", "pair_order": list(_PAIRS), "digit_order": ranks,
        "terminal_period_is_framing": terminal_period,
        "padding": "at most one trailing Morse divider",
        "source_url": ACA_MORBIT_URL,
        "scope": "Supplied-key Morbit only. Morse case and whitespace are normalized; no unknown-key or unknown-script decipherment.",
    })


__all__ = ["ACA_MORBIT_URL", "morbit_key", "morbit_encrypt", "morbit_decrypt", "solve_morbit"]
