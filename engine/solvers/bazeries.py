"""Bazeries known-key solver: digit transposition plus two Polybius squares.

Étienne Bazeries' product cipher takes one number less than a million.
Its digits (a 0 counts as 10) cut the letter stream into groups that are
reversed. The number spelled in English, with "and" omitted, keys a 5×5
ciphertext square filled by rows. A plaintext square is the alphabet
without a separate J, filled down the columns. I and J share a cell.
Each transposed letter is replaced by the ciphertext-square letter in
the same cell.

The worked example checked here is the American Cryptogram Association
cipher-type sheet (page 35), fetched 2026-10-02:

  https://www.cryptogram.org/downloads/aca.info/ciphers/Bazeries.pdf

This module is a **known classical-cipher** solver. It recovers plaintext
only when the number is supplied. It is **not** an unknown-script reading
and **not** a claim about army message Nr. 86.
"""

from __future__ import annotations

from engine.alphabet import letters_only, reinject
from engine.result import SolveResult

# ACA cipher types, Bazeries (fetched 2026-10-02).
# https://www.cryptogram.org/downloads/aca.info/ciphers/Bazeries.pdf
ACA_URL = "https://www.cryptogram.org/downloads/aca.info/ciphers/Bazeries.pdf"
ACA_KEY = "3752"
ACA_PLAIN = "SIMPLESUBSTITUTIONPLUSTRANSPOSITION"
ACA_CIPHER = "ACYYUXYMRQKXKCKGCRQIYITNKYXKCYGQGCI"

_SCOPE = (
    "Known classical Bazeries cipher solver only; "
    "not an unknown-script reading and not a claim about army message Nr. 86."
)

# I/J share one cell. The plaintext square is this alphabet written in columns.
_PLAIN_ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

_ONES = (
    "",
    "ONE",
    "TWO",
    "THREE",
    "FOUR",
    "FIVE",
    "SIX",
    "SEVEN",
    "EIGHT",
    "NINE",
    "TEN",
    "ELEVEN",
    "TWELVE",
    "THIRTEEN",
    "FOURTEEN",
    "FIFTEEN",
    "SIXTEEN",
    "SEVENTEEN",
    "EIGHTEEN",
    "NINETEEN",
)
_TENS = (
    "",
    "",
    "TWENTY",
    "THIRTY",
    "FORTY",
    "FIFTY",
    "SIXTY",
    "SEVENTY",
    "EIGHTY",
    "NINETY",
)


def bazeries_key(key: str | int) -> str:
    """Decimal key, 0 through 999999. Spaces are ignored. Leading zeros drop."""
    raw = str(key).strip().replace(" ", "").replace(",", "")
    if not raw.isdigit():
        raise ValueError("Bazeries key must be a number less than one million")
    number = int(raw)
    if number > 999_999:
        raise ValueError("Bazeries key must be less than one million")
    return str(number)


def spell_bazeries_number(key: str | int) -> str:
    """English cardinal of the key, concatenated, without the word AND.

    3752 is THREE THOUSAND SEVEN HUNDRED FIFTY TWO, which is the keyword
    behind the ciphertext square printed on the ACA sheet.
    """
    number = int(bazeries_key(key))
    if number == 0:
        return "ZERO"
    thousands, rest = divmod(number, 1000)
    parts: list[str] = []
    if thousands:
        parts.append(_under_one_thousand(thousands) + "THOUSAND")
    if rest:
        parts.append(_under_one_thousand(rest))
    return "".join(parts)


def _under_one_hundred(number: int) -> str:
    if number < 20:
        return _ONES[number]
    tens, ones = divmod(number, 10)
    return _TENS[tens] + _ONES[ones]


def _under_one_thousand(number: int) -> str:
    hundreds, rest = divmod(number, 100)
    words = (_ONES[hundreds] + "HUNDRED") if hundreds else ""
    if rest:
        words += _under_one_hundred(rest)
    return words


def _fold(text: str) -> str:
    """A–Z stream with J folded into I. Empty input is an error."""
    folded = letters_only(text).replace("J", "I")
    if not folded:
        raise ValueError("text has no letters")
    return folded


def _group_sizes(key: str) -> list[int]:
    """Digits of the key. A 0 digit is a group of length 10, not an empty group."""
    return [10 if digit == "0" else int(digit) for digit in bazeries_key(key)]


def reverse_groups(letters: str, key: str | int) -> str:
    """Reverse successive groups whose lengths are the key digits, repeated."""
    sizes = _group_sizes(key)
    out: list[str] = []
    index = 0
    size_index = 0
    while index < len(letters):
        size = sizes[size_index % len(sizes)]
        size_index += 1
        group = letters[index : index + size]
        out.append(group[::-1])
        index += len(group)
    return "".join(out)


def plaintext_square() -> list[str]:
    """Five rows of the column-filled plaintext square (I/J combined)."""
    return ["".join(row) for row in _plain_grid()]


def ciphertext_square(key: str | int) -> list[str]:
    """Five rows of the keyed ciphertext square, filled left to right."""
    grid = _cipher_grid(key)
    return ["".join(row) for row in grid]


def _plain_grid() -> list[list[str]]:
    grid = [[""] * 5 for _ in range(5)]
    for index, letter in enumerate(_PLAIN_ALPHABET):
        column, row = divmod(index, 5)
        grid[row][column] = letter
    return grid


def _cipher_grid(key: str | int) -> list[list[str]]:
    keyword = spell_bazeries_number(key)
    seen: list[str] = []
    for letter in keyword:
        if letter not in seen:
            seen.append(letter)
    for letter in _PLAIN_ALPHABET:
        if letter not in seen:
            seen.append(letter)
    if len(seen) != 25:
        raise ValueError("Bazeries ciphertext square did not fill 25 cells")
    return [seen[row * 5 : (row + 1) * 5] for row in range(5)]


def _substitution_maps(key: str | int) -> tuple[dict[str, str], dict[str, str]]:
    plain = _plain_grid()
    cipher = _cipher_grid(key)
    encrypt: dict[str, str] = {}
    decrypt: dict[str, str] = {}
    for row in range(5):
        for column in range(5):
            encrypt[plain[row][column]] = cipher[row][column]
            decrypt[cipher[row][column]] = plain[row][column]
    return encrypt, decrypt


def bazeries_encrypt(text: str, key: str | int) -> str:
    """Encrypt with a known Bazeries number. Non-letters are dropped. J becomes I."""
    number = bazeries_key(key)
    transposed = reverse_groups(_fold(text), number)
    encrypt_map, _decrypt_map = _substitution_maps(number)
    return "".join(encrypt_map[letter] for letter in transposed)


def bazeries_decrypt(text: str, key: str | int) -> str:
    """Decrypt with a known Bazeries number. Undo the square, then the groups."""
    number = bazeries_key(key)
    _encrypt_map, decrypt_map = _substitution_maps(number)
    substituted = "".join(decrypt_map[letter] for letter in _fold(text))
    return reverse_groups(substituted, number)


def solve_bazeries(text: str, *, key: str | int) -> SolveResult:
    """Recover Bazeries plaintext when the number is known.

    Known-cipher decrypt only. Not an unknown-script reading and not a
    claim about army message Nr. 86.
    """
    number = bazeries_key(key)
    plain_letters = bazeries_decrypt(text, number)
    rendered = reinject(text, plain_letters) if any(not ch.isalpha() for ch in text) else plain_letters
    return SolveResult(
        method="bazeries",
        plaintext=rendered,
        key=number,
        score=float(len(plain_letters)),
        details={
            "key": number,
            "spelling": spell_bazeries_number(number),
            "letters": len(_fold(text)),
            "mode": "known_number",
            "scope": _SCOPE,
            "source_url": ACA_URL,
        },
    )


__all__ = [
    "ACA_CIPHER",
    "ACA_KEY",
    "ACA_PLAIN",
    "ACA_URL",
    "bazeries_decrypt",
    "bazeries_encrypt",
    "bazeries_key",
    "ciphertext_square",
    "plaintext_square",
    "reverse_groups",
    "solve_bazeries",
    "spell_bazeries_number",
]
