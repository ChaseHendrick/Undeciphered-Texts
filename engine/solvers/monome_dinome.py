"""Supplied-key ACA Monome-Dinome with a 24-entry variable-length digit box.

Primary source:
https://www.cryptogram.org/downloads/aca.info/ciphers/MonomeDinome.pdf
I/J share an entry, as does one supplied pair, default Y/Z. These merges
are lossy: decryption reports their representatives, not original choices.
"""

from __future__ import annotations

from engine.result import SolveResult
from engine.solvers.morbit import MAX_PLAINTEXT_CHARS, _digit_stream, _text

ACA_MONOME_DINOME_URL = "https://www.cryptogram.org/downloads/aca.info/ciphers/MonomeDinome.pdf"
_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _merges(merge: tuple[str, str]) -> dict[str, str]:
    if not isinstance(merge, tuple):
        raise TypeError("merge must be a tuple of two distinct uppercase letters")
    if len(merge) != 2 or any(not isinstance(ch, str) or len(ch) != 1 or ch not in _ALPHABET or ch in "IJ" for ch in merge) or merge[0] == merge[1]:
        raise ValueError("additional merge must contain two distinct uppercase letters excluding I/J")
    return {"J": "I", merge[1]: merge[0]}


def keyed_alphabet(key: str, *, merge: tuple[str, str] = ("Y", "Z")) -> str:
    """Keyword first, deduplicated after declared merges, then unused letters."""
    replacements = _merges(merge)
    _text(key, "Monome-Dinome keyword", 1000)
    if any(ch not in _ALPHABET + _ALPHABET.lower() for ch in key):
        raise ValueError("Monome-Dinome keyword must contain ASCII letters only")
    sequence = (replacements.get(ch, ch) for ch in key.upper() + _ALPHABET)
    return "".join(dict.fromkeys(sequence))


def _table(key: str, digit_order: str, merge: tuple[str, str]) -> tuple[str, dict[str, str]]:
    if not isinstance(digit_order, str):
        raise TypeError("digit_order must be a string")
    if len(digit_order) != 10 or set(digit_order) != set("0123456789"):
        raise ValueError("digit_order must be a permutation of ASCII digits 0..9")
    alphabet = keyed_alphabet(key, merge=merge)
    rows, columns = digit_order[:2], digit_order[2:]
    table = {letter: ("" if index < 8 else rows[index // 8 - 1]) + columns[index % 8]
             for index, letter in enumerate(alphabet)}
    return alphabet, table


def monome_dinome_encrypt(text: str, key: str, *, digit_order: str = "0123456789", merge: tuple[str, str] = ("Y", "Z")) -> str:
    """Encrypt normalized letters; plaintext whitespace is omitted explicitly."""
    _, table = _table(key, digit_order, merge)
    replacements = _merges(merge)
    _text(text, "plaintext", MAX_PLAINTEXT_CHARS)
    if any(ch not in _ALPHABET + _ALPHABET.lower() and not ch.isspace() for ch in text):
        raise ValueError("Monome-Dinome plaintext permits ASCII letters and whitespace only")
    letters = [replacements.get(ch.upper(), ch.upper()) for ch in text if not ch.isspace()]
    if not letters:
        raise ValueError("plaintext must contain letters")
    return "".join(table[letter] for letter in letters)


def monome_dinome_decrypt(text: str, key: str, *, digit_order: str = "0123456789", merge: tuple[str, str] = ("Y", "Z"), terminal_period: bool = False) -> str:
    """Parse disjoint single-digit codes and row-prefix/column-digit codes."""
    _, table = _table(key, digit_order, merge)
    inverse = {code: letter for letter, code in table.items()}
    digits = _digit_stream(text, terminal_period=terminal_period)
    rows = digit_order[:2]
    output = []
    index = 0
    while index < len(digits):
        width = 2 if digits[index] in rows else 1
        code = digits[index:index + width]
        if len(code) != width or code not in inverse:
            raise ValueError(f"truncated or invalid Monome-Dinome code at digit {index}: {code!r}")
        output.append(inverse[code])
        index += width
    return "".join(output)


def solve_monome_dinome(text: str, *, key: str, digit_order: str = "0123456789", merge: tuple[str, str] = ("Y", "Z"), terminal_period: bool = False) -> SolveResult:
    alphabet, table = _table(key, digit_order, merge)
    plain = monome_dinome_decrypt(text, key, digit_order=digit_order, merge=merge, terminal_period=terminal_period)
    return SolveResult("monome-dinome", plain, alphabet, float(len(plain)), {
        "mode": "known_key", "digit_order": digit_order, "keyed_alphabet": alphabet,
        "letter_codes": table, "letter_merges": _merges(merge), "lossy": True,
        "plaintext_word_spaces": "not encoded", "terminal_period_is_framing": terminal_period,
        "source_url": ACA_MONOME_DINOME_URL,
        "scope": "Supplied-key Monome-Dinome only. Letter merges and omitted spaces prevent recovery of original orthography; no unknown-key or unknown-script decipherment.",
    })


__all__ = ["ACA_MONOME_DINOME_URL", "keyed_alphabet", "monome_dinome_encrypt", "monome_dinome_decrypt", "solve_monome_dinome"]
