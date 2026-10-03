"""Playfair (Wheatstone–Playfair) known-key digraph solver.

Uses one 5×5 square that omits J (I and J share a cell). Encipherment follows
the four rules in the Wikipedia worked example for keyword ``playfair example``
and plaintext ``hide the gold in the tree stump``:

https://en.wikipedia.org/wiki/Playfair_cipher

This module decrypts when the keyword is supplied. It is a **known-cipher**
solver for that classical system. It does **not** read an unknown script, and
it does not claim a cryptanalysis of an unsolved historical Playfair message.
"""

from __future__ import annotations

from engine.alphabet import letters_only
from engine.ciphers import square_from_keyword, two_square_letters
from engine.language import get_model
from engine.result import SolveResult

# Wikipedia "Example" section (fetched 2026-10-02, America/New_York).
WIKIPEDIA_SOURCE_URL = "https://en.wikipedia.org/wiki/Playfair_cipher"
WIKIPEDIA_KEYWORD = "playfair example"
# Digraph form after the null X is inserted between the repeated E's in TREE.
WIKIPEDIA_PREPARED_PLAINTEXT = "HIDETHEGOLDINTHETREXESTUMP"
WIKIPEDIA_CIPHERTEXT = "BMODZBXDNABEKUDMUIXMMOUVIF"
# Spaced message as printed in the article ("hide the gold in the tree stump").
WIKIPEDIA_MESSAGE = "hide the gold in the tree stump"


def playfair_square(keyword: str) -> str:
    """Build the 25-letter Playfair square (no J) from a keyword phrase."""
    return square_from_keyword(keyword)


def prepare_playfair_plaintext(text: str, pad: str = "X") -> str:
    """Fold J→I, insert ``pad`` between identical pair letters, pad odd length.

    Matches the Wikipedia preparation of ``hide the gold in the tree stump``
    into pairs ``HI DE TH EG OL DI NT HE TR EX ES TU MP``.
    """
    if len(pad) != 1 or not pad.isalpha() or pad.upper() == "J":
        raise ValueError("pad must be a single non-J letter")
    pad = pad.upper()
    stream = two_square_letters(text)
    out: list[str] = []
    i = 0
    while i < len(stream):
        a = stream[i]
        if i + 1 >= len(stream):
            out.append(a)
            out.append(pad)
            break
        b = stream[i + 1]
        if a == b:
            out.append(a)
            out.append(pad)
            i += 1
            continue
        out.append(a)
        out.append(b)
        i += 2
    return "".join(out)


def _positions(square: str) -> dict[str, tuple[int, int]]:
    cells = two_square_letters(square)
    if len(cells) != 25 or len(set(cells)) != 25 or "J" in cells:
        raise ValueError("Playfair square must be 25 distinct letters without J")
    return {ch: divmod(i, 5) for i, ch in enumerate(cells)}


def _encrypt_pair(a: str, b: str, square: str, pos: dict[str, tuple[int, int]]) -> str:
    r1, c1 = pos[a]
    r2, c2 = pos[b]
    if r1 == r2:
        return square[r1 * 5 + (c1 + 1) % 5] + square[r2 * 5 + (c2 + 1) % 5]
    if c1 == c2:
        return square[((r1 + 1) % 5) * 5 + c1] + square[((r2 + 1) % 5) * 5 + c2]
    return square[r1 * 5 + c2] + square[r2 * 5 + c1]


def _decrypt_pair(a: str, b: str, square: str, pos: dict[str, tuple[int, int]]) -> str:
    r1, c1 = pos[a]
    r2, c2 = pos[b]
    if r1 == r2:
        return square[r1 * 5 + (c1 - 1) % 5] + square[r2 * 5 + (c2 - 1) % 5]
    if c1 == c2:
        return square[((r1 - 1) % 5) * 5 + c1] + square[((r2 - 1) % 5) * 5 + c2]
    return square[r1 * 5 + c2] + square[r2 * 5 + c1]


def playfair_encrypt(text: str, keyword: str) -> str:
    """Encrypt with a Playfair keyword square (prepares the plaintext first)."""
    square = playfair_square(keyword)
    pos = _positions(square)
    prepared = prepare_playfair_plaintext(text)
    out: list[str] = []
    for i in range(0, len(prepared), 2):
        out.append(_encrypt_pair(prepared[i], prepared[i + 1], square, pos))
    return "".join(out)


def playfair_decrypt(ciphertext: str, keyword: str) -> str:
    """Decrypt a Playfair ciphertext with a known keyword square.

    Returns the digraph letter stream (including any null X/Q pads that were
    present in the prepared plaintext). Does not invent word breaks.
    """
    square = playfair_square(keyword)
    pos = _positions(square)
    stream = two_square_letters(ciphertext)
    if len(stream) % 2 == 1:
        raise ValueError("Playfair ciphertext length must be even")
    out: list[str] = []
    for i in range(0, len(stream), 2):
        out.append(_decrypt_pair(stream[i], stream[i + 1], square, pos))
    return "".join(out)


def solve_playfair(text: str, keyword: str) -> SolveResult:
    """Recover plaintext from a Playfair ciphertext when the keyword is known.

    This is a known-cipher, known-key decrypt. It does not search for an
    unknown key and does not read an unknown script.
    """
    plaintext = playfair_decrypt(text, keyword)
    square = playfair_square(keyword)
    letters = letters_only(plaintext)
    az = [ord(ch) - 65 for ch in letters]
    return SolveResult(
        method="playfair",
        plaintext=plaintext,
        key=letters_only(keyword),
        score=get_model().score(az) if az else 0.0,
        details={
            "keyword": keyword,
            "square": square,
            "letters": len(az),
            "source_example": WIKIPEDIA_SOURCE_URL,
            "scope": (
                "known-key Playfair digraph decrypt; classical cipher only; "
                "does not read an unknown script"
            ),
        },
    )


__all__ = [
    "WIKIPEDIA_CIPHERTEXT",
    "WIKIPEDIA_KEYWORD",
    "WIKIPEDIA_MESSAGE",
    "WIKIPEDIA_PREPARED_PLAINTEXT",
    "WIKIPEDIA_SOURCE_URL",
    "playfair_decrypt",
    "playfair_encrypt",
    "playfair_square",
    "prepare_playfair_plaintext",
    "solve_playfair",
]
