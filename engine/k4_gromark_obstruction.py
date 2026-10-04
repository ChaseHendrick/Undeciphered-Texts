"""K4 Gromark obstruction, then the compositions that might escape it.

Plain Gromark shifts by a digit 0 through 9. One cipher alphabet gives each
ciphertext letter one index. If the same letter appears under two crib
letters whose allowed indexes do not overlap, no keyword and no primer can
place those cribs in situ.

Myszkowski with the three published Kryptos keywords is the transposition
tried on either side of Gromark. A position-wise substitution makes those
two orders the same crib pairs, so they are one check. Periodic Gromark
adds a keyword rotation and is decrypted instead of ruled out by the digit bound.

This is not a K4 decipherment. solved stays false. claimed_plaintext stays None.
"""

from __future__ import annotations

from engine.alphabet import letters_only
from engine.solvers.k4_attempt import K4_CIPHERTEXT, cribs_in_place
from engine.solvers.myszkowski import (
    _columns_by_number,
    _heights,
    myszkowski_decrypt,
    myszkowski_numbers,
)
from engine.solvers.periodic_gromark import periodic_gromark_decrypt

CRIB_SPANS = ((21, "EASTNORTHEAST"), (63, "BERLINCLOCK"))
KEYWORDS = ("KRYPTOS", "PALIMPSEST", "ABSCISSA")


def crib_pairs(ciphertext: str, spans=CRIB_SPANS) -> tuple[tuple[int, str, str], ...]:
    """(position, ciphertext letter, plaintext letter) for each crib letter."""
    letters = letters_only(ciphertext)
    pairs = []
    for start, word in spans:
        for offset, plain in enumerate(word):
            position = start + offset
            pairs.append((position, letters[position], plain))
    return tuple(pairs)


def empty_domain_letters(pairs: tuple[tuple[int, str, str], ...]) -> tuple[str, ...]:
    """Cipher letters that cannot sit at one alphabet index for every crib use.

    Allowed indexes are ``(plaintext index + digit) mod 26`` for a digit 0..9.
    """
    by_letter: dict[str, set[int]] = {}
    for _position, cipher_letter, plain_letter in pairs:
        allowed = {(ord(plain_letter) - 65 + digit) % 26 for digit in range(10)}
        if cipher_letter not in by_letter:
            by_letter[cipher_letter] = allowed
        else:
            by_letter[cipher_letter] &= allowed
    return tuple(sorted(letter for letter, allowed in by_letter.items() if not allowed))


def _plain_to_cipher(keyword: str, length: int) -> list[int]:
    """Plaintext index to Myszkowski ciphertext index, matching decrypt."""
    numbers = myszkowski_numbers(keyword)
    width = len(numbers)
    heights = _heights(length, width)
    rows = max(heights)
    grid = [[None] * width for _ in range(rows)]
    cursor = 0
    for columns in _columns_by_number(numbers):
        for row in range(rows):
            for column in columns:
                if row < heights[column]:
                    grid[row][column] = cursor
                    cursor += 1
    order = []
    for row in range(rows):
        for column in range(width):
            if row < heights[column]:
                order.append(grid[row][column])
    return order


def _composition_pairs(ciphertext: str, keyword: str) -> tuple[tuple[int, str, str], ...]:
    """Cipher letter and crib letter after one Myszkowski around in-place Gromark.

    Decrypting the transposition, then reading the crib in place, uses the
    same pairs as Gromark on the original ciphertext followed by that
    transposition. ``order[p]`` is the ciphertext index that lands at
    plaintext index ``p``.
    """
    order = _plain_to_cipher(keyword, len(letters_only(ciphertext)))
    moved = []
    for position, _cipher_letter, plain_letter in crib_pairs(ciphertext):
        source = order[position]
        moved.append((source, ciphertext[source], plain_letter))
    return tuple(moved)


def search_k4_gromark_obstruction() -> dict:
    """Rule out in-place Gromark, then test the published-keyword escapes."""
    if len(K4_CIPHERTEXT) != 97:
        raise ValueError("K4 ciphertext must be 97 letters")
    in_place = empty_domain_letters(crib_pairs(K4_CIPHERTEXT))
    compositions = []
    myszkowski_hits = []
    for keyword in KEYWORDS:
        transposed = myszkowski_decrypt(K4_CIPHERTEXT, keyword)
        plain_hit = cribs_in_place(transposed)
        if plain_hit:
            myszkowski_hits.append({"keyword": keyword, "status": "unverified", "plaintext": transposed})
        composed = empty_domain_letters(_composition_pairs(K4_CIPHERTEXT, keyword))
        direct = empty_domain_letters(crib_pairs(transposed))
        if composed != direct:
            raise RuntimeError("Myszkowski orders disagreed; the pair identity failed")
        compositions.append(
            {
                "keyword": keyword,
                "myszkowski_crib_hit": plain_hit,
                "gromark_myszkowski_blocked": bool(composed),
                "blocked_letters": composed,
                "orders_agree": True,
            }
        )
    periodic = []
    for keyword in KEYWORDS:
        plain = periodic_gromark_decrypt(K4_CIPHERTEXT, keyword=keyword, framed=False)
        hit = cribs_in_place(plain)
        periodic.append(
            {
                "keyword": keyword,
                "crib_hit": hit,
                "status": "unverified" if hit else "rejected",
                "plaintext": plain if hit else None,
            }
        )
    return {
        "claimed_plaintext": None,
        "solved": False,
        "model": "ACA Gromark digit 0..9, one cipher alphabet, cribs at published plaintext indexes",
        "in_place_blocked_letters": in_place,
        "in_place_blocked": bool(in_place),
        "keywords": KEYWORDS,
        "compositions": compositions,
        "myszkowski_crib_hits": len(myszkowski_hits),
        "periodic_gromark": periodic,
        "periodic_crib_hits": sum(1 for row in periodic if row["crib_hit"]),
        "unverified": myszkowski_hits + [row for row in periodic if row["crib_hit"]],
    }
