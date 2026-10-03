"""Four-square (Delastelle) known-key digraph solver.

Uses four 5×5 squares. The upper-left and lower-right squares are the
standard alphabet with Q omitted (I and J stay distinct). The upper-right
and lower-left squares are keyword squares. Encipherment follows the
rectangle rule in the Wikipedia worked example for keywords ``example`` and
``keyword`` and plaintext ``he lp me ob iw an ke no bi``:

https://en.wikipedia.org/wiki/Four-square_cipher

This module decrypts when both keywords are supplied. It is a **known-cipher**
solver for that classical system. It does **not** read an unknown script, and
it does not claim a solution of army message Nr. 86 or any unsolved wartime
message.
"""

from __future__ import annotations

from engine.alphabet import letters_only
from engine.language import get_model
from engine.result import SolveResult

# Wikipedia "Using four-square" / "Algorithm" (fetched 2026-10-02, America/New_York).
WIKIPEDIA_SOURCE_URL = "https://en.wikipedia.org/wiki/Four-square_cipher"
WIKIPEDIA_UPPER_RIGHT_KEYWORD = "example"
WIKIPEDIA_LOWER_LEFT_KEYWORD = "keyword"
# Digraphs as printed: he lp me ob iw an ke no bi.
WIKIPEDIA_PLAINTEXT = "HELPMEOBIWANKENOBI"
WIKIPEDIA_CIPHERTEXT = "FYGMKYHOBXMFKKKIMD"
WIKIPEDIA_MESSAGE = "he lp me ob iw an ke no bi"

# Plaintext squares: a-z with Q omitted, row-major, as printed on Wikipedia.
PLAIN_ALPHABET = "ABCDEFGHIJKLMNOPRSTUVWXYZ"


def four_square_letters(text: str) -> str:
    """A-Z stream with Q removed. Four-square here follows Wikipedia and omits Q."""
    return "".join(ch for ch in letters_only(text) if ch != "Q")


def square_from_keyword(keyword: str) -> str:
    """Keyword-first 5×5 square over the 25-letter alphabet that omits Q."""
    seen: list[str] = []
    for ch in four_square_letters(keyword) + PLAIN_ALPHABET:
        if ch not in seen:
            seen.append(ch)
    if len(seen) != 25:
        raise ValueError("four-square keyword square must contain 25 distinct letters without Q")
    return "".join(seen)


def _positions(square: str) -> dict[str, tuple[int, int]]:
    cells = four_square_letters(square)
    if len(cells) != 25 or len(set(cells)) != 25 or "Q" in cells:
        raise ValueError("four-square square must be 25 distinct letters without Q")
    return {ch: divmod(i, 5) for i, ch in enumerate(cells)}


def _require_even(stream: str, label: str) -> str:
    if len(stream) == 0 or len(stream) % 2 == 1:
        raise ValueError(f"four-square {label} needs a positive even number of letters")
    return stream


def four_square_encrypt(
    text: str,
    upper_right_keyword: str,
    lower_left_keyword: str,
) -> str:
    """Encrypt with two keyword squares (odd length is padded with X).

    First plaintext letter is taken from the upper-left standard square.
    Second plaintext letter is taken from the lower-right standard square.
    Ciphertext is the other two corners: upper-right letter, then lower-left.
    """
    plain_pos = _positions(PLAIN_ALPHABET)
    upper = square_from_keyword(upper_right_keyword)
    lower = square_from_keyword(lower_left_keyword)
    stream = four_square_letters(text)
    if len(stream) == 0:
        raise ValueError("four-square plaintext needs at least one letter")
    if len(stream) % 2 == 1:
        stream += "X"
    out: list[str] = []
    for i in range(0, len(stream), 2):
        r1, c1 = plain_pos[stream[i]]
        r2, c2 = plain_pos[stream[i + 1]]
        out.append(upper[r1 * 5 + c2])
        out.append(lower[r2 * 5 + c1])
    return "".join(out)


def four_square_decrypt(
    ciphertext: str,
    upper_right_keyword: str,
    lower_left_keyword: str,
) -> str:
    """Decrypt a four-square ciphertext when both keywords are known.

    Returns the digraph letter stream. Does not invent word breaks.
    """
    plain = PLAIN_ALPHABET
    upper = square_from_keyword(upper_right_keyword)
    lower = square_from_keyword(lower_left_keyword)
    upper_pos = _positions(upper)
    lower_pos = _positions(lower)
    stream = _require_even(four_square_letters(ciphertext), "ciphertext")
    out: list[str] = []
    for i in range(0, len(stream), 2):
        r1, c1 = upper_pos[stream[i]]
        r2, c2 = lower_pos[stream[i + 1]]
        out.append(plain[r1 * 5 + c2])
        out.append(plain[r2 * 5 + c1])
    return "".join(out)


def solve_four_square(
    text: str,
    upper_right_keyword: str,
    lower_left_keyword: str,
) -> SolveResult:
    """Recover plaintext from a four-square ciphertext when both keywords are known.

    This is a known-cipher, known-key decrypt. It does not search for an
    unknown key, does not read an unknown script, and does not claim a
    reading of army message Nr. 86.
    """
    plaintext = four_square_decrypt(text, upper_right_keyword, lower_left_keyword)
    upper = square_from_keyword(upper_right_keyword)
    lower = square_from_keyword(lower_left_keyword)
    az = [ord(ch) - 65 for ch in plaintext]
    return SolveResult(
        method="four_square",
        plaintext=plaintext,
        key=f"{four_square_letters(upper_right_keyword)}/{four_square_letters(lower_left_keyword)}",
        score=get_model().score(az) if az else 0.0,
        details={
            "upper_right_keyword": upper_right_keyword,
            "lower_left_keyword": lower_left_keyword,
            "upper_right_square": upper,
            "lower_left_square": lower,
            "plaintext_square": PLAIN_ALPHABET,
            "omitted_letter": "Q",
            "letters": len(az),
            "source_example": WIKIPEDIA_SOURCE_URL,
            "scope": (
                "known-key four-square digraph decrypt; classical cipher only; "
                "does not read an unknown script; not a claim about army message Nr. 86"
            ),
        },
    )


__all__ = [
    "PLAIN_ALPHABET",
    "WIKIPEDIA_CIPHERTEXT",
    "WIKIPEDIA_LOWER_LEFT_KEYWORD",
    "WIKIPEDIA_MESSAGE",
    "WIKIPEDIA_PLAINTEXT",
    "WIKIPEDIA_SOURCE_URL",
    "WIKIPEDIA_UPPER_RIGHT_KEYWORD",
    "four_square_decrypt",
    "four_square_encrypt",
    "four_square_letters",
    "solve_four_square",
    "square_from_keyword",
]
