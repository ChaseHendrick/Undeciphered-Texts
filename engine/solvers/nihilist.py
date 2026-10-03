"""Nihilist known-key solver: keyed Polybius square plus an additive keyword.

A 5x5 Polybius square is filled from a square keyword (J folded into I).
Each plaintext letter becomes a two-digit coordinate, rows and columns
numbered 1 to 5. The additive keyword is converted the same way and
repeated. Ciphertext numbers are the ordinary decimal sums of those pairs.
Decryption subtracts the same repeating key numbers and reads the square.

The worked example used here is the one on Wikipedia (fetched 2026-10-02):

  https://en.wikipedia.org/wiki/Nihilist_cipher

  square keyword ZEBRAS, additive keyword RUSSIAN,
  "DYNAMITE WINTER PALACE" -> 37 106 62 36 67 47 86 26 104 53 62 77 27 55 57 66 55 36 54 27

This module is a **known classical-cipher** solver. It recovers plaintext
only when both keywords are supplied. It is **not** an unknown-script
reading and **not** a claim about army message Nr. 86.
"""

from __future__ import annotations

from engine.result import SolveResult

# 25-letter alphabet: J folded into I (the Wikipedia square has I and no J).
NIHILIST_ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

# Wikipedia worked example (fetched 2026-10-02).
# https://en.wikipedia.org/wiki/Nihilist_cipher
WIKIPEDIA_URL = "https://en.wikipedia.org/wiki/Nihilist_cipher"
WIKIPEDIA_SQUARE_KEYWORD = "ZEBRAS"
WIKIPEDIA_ADDITIVE_KEYWORD = "RUSSIAN"
WIKIPEDIA_KEY = "ZEBRAS RUSSIAN"
# The page writes "DYNAMITE WINTER PALACE". Spaces are not encrypted.
WIKIPEDIA_PLAIN = "DYNAMITEWINTERPALACE"
WIKIPEDIA_CIPHER = "37 106 62 36 67 47 86 26 104 53 62 77 27 55 57 66 55 36 54 27"

_SCOPE = (
    "Known classical Nihilist cipher solver only; "
    "not an unknown-script reading and not a claim about army message Nr. 86."
)


def nihilist_letters(text: str) -> str:
    """A-Z stream for the Nihilist square: non-letters dropped, J folded to I."""
    out: list[str] = []
    for ch in text:
        if not ch.isalpha():
            continue
        up = ch.upper()
        out.append("I" if up == "J" else up)
    return "".join(out)


def square_from_keyword(keyword: str) -> str:
    """Build a 5x5 keysquare: keyword letters first, then unused A-Z without J."""
    cleaned = nihilist_letters(keyword)
    if not cleaned:
        raise ValueError("Nihilist square keyword has no letters")
    seen: set[str] = set()
    cells: list[str] = []
    for ch in cleaned:
        if ch not in seen:
            seen.add(ch)
            cells.append(ch)
    for ch in NIHILIST_ALPHABET:
        if ch not in seen:
            cells.append(ch)
    if len(cells) != 25:
        raise ValueError("Nihilist keysquare must contain 25 letters")
    return "".join(cells)


def _coordinates(square: str) -> dict[str, int]:
    """Map each letter to a 1-based row-column number (11 through 55)."""
    coords: dict[str, int] = {}
    for index, ch in enumerate(square):
        row, col = divmod(index, 5)
        coords[ch] = (row + 1) * 10 + (col + 1)
    return coords


def _letter_at(square: str, number: int) -> str:
    if number < 11 or number > 55:
        raise ValueError(f"Nihilist coordinate {number} is outside 11-55")
    row, col = divmod(number, 10)
    if row < 1 or row > 5 or col < 1 or col > 5:
        raise ValueError(f"Nihilist coordinate {number} is not a 1-5 row and column")
    return square[(row - 1) * 5 + (col - 1)]


def parse_nihilist_key(key: str) -> tuple[str, str]:
    """Split 'SQUARE ADDITIVE' into the two keywords.

    A slash or a vertical bar is also accepted between the keywords.
    """
    text = str(key).strip().replace("/", " ").replace("|", " ")
    parts = text.split()
    if len(parts) != 2:
        raise ValueError(
            "Nihilist key must be the square keyword and the additive keyword"
        )
    square_keyword, additive_keyword = parts
    if not nihilist_letters(square_keyword) or not nihilist_letters(additive_keyword):
        raise ValueError("Nihilist key keywords must contain letters")
    return square_keyword, additive_keyword


def _key_numbers(square: str, additive_keyword: str) -> list[int]:
    coords = _coordinates(square)
    letters = nihilist_letters(additive_keyword)
    if not letters:
        raise ValueError("Nihilist additive keyword has no letters")
    return [coords[ch] for ch in letters]


def _cipher_numbers(text: str) -> list[int]:
    """Read whitespace- or comma-separated ciphertext numbers."""
    chunk = []
    numbers: list[int] = []
    for ch in text:
        if ch.isdigit():
            chunk.append(ch)
            continue
        if chunk:
            numbers.append(int("".join(chunk)))
            chunk = []
        elif ch not in " \t\r\n,;":
            raise ValueError("Nihilist ciphertext must be separated numbers")
    if chunk:
        numbers.append(int("".join(chunk)))
    if not numbers:
        raise ValueError("Nihilist ciphertext has no numbers")
    return numbers


def nihilist_encrypt(text: str, key: str) -> str:
    """Encrypt with a known square keyword and additive keyword.

    Non-letters are dropped. J is folded into I. Numbers are space-separated
    because some sums have three digits and cannot be concatenated safely.
    """
    square_keyword, additive_keyword = parse_nihilist_key(key)
    square = square_from_keyword(square_keyword)
    coords = _coordinates(square)
    plain = nihilist_letters(text)
    if not plain:
        raise ValueError("text has no letters")
    key_nums = _key_numbers(square, additive_keyword)
    width = len(key_nums)
    sums = [coords[ch] + key_nums[index % width] for index, ch in enumerate(plain)]
    return " ".join(str(number) for number in sums)


def nihilist_decrypt(text: str, key: str) -> str:
    """Decrypt with a known square keyword and additive keyword."""
    square_keyword, additive_keyword = parse_nihilist_key(key)
    square = square_from_keyword(square_keyword)
    numbers = _cipher_numbers(text)
    key_nums = _key_numbers(square, additive_keyword)
    width = len(key_nums)
    plain: list[str] = []
    for index, number in enumerate(numbers):
        coord = number - key_nums[index % width]
        plain.append(_letter_at(square, coord))
    return "".join(plain)


def solve_nihilist(text: str, *, key: str) -> SolveResult:
    """Recover Nihilist plaintext when both keywords are known.

    Known-cipher decrypt only. Not an unknown-script reading and not a
    claim about army message Nr. 86.
    """
    square_keyword, additive_keyword = parse_nihilist_key(key)
    plain_letters = nihilist_decrypt(text, key)
    canonical = f"{nihilist_letters(square_keyword)} {nihilist_letters(additive_keyword)}"
    # Keep the caller's keyword spelling when it is already one token each.
    shown = f"{square_keyword.strip()} {additive_keyword.strip()}"
    return SolveResult(
        method="nihilist",
        plaintext=plain_letters,
        key=shown,
        score=float(len(plain_letters)),
        details={
            "key": shown,
            "square_keyword": square_keyword.strip(),
            "additive_keyword": additive_keyword.strip(),
            "canonical_key": canonical,
            "numbers": len(_cipher_numbers(text)),
            "mode": "known_keywords",
            "scope": _SCOPE,
            "source_url": WIKIPEDIA_URL,
        },
    )


__all__ = [
    "WIKIPEDIA_ADDITIVE_KEYWORD",
    "WIKIPEDIA_CIPHER",
    "WIKIPEDIA_KEY",
    "WIKIPEDIA_PLAIN",
    "WIKIPEDIA_SQUARE_KEYWORD",
    "WIKIPEDIA_URL",
    "nihilist_decrypt",
    "nihilist_encrypt",
    "parse_nihilist_key",
    "solve_nihilist",
    "square_from_keyword",
]
