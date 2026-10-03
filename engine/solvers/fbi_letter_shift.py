"""FBI one-letter shift known-key solver.

The FBI printed this teaching example in "Help Solve an Open Murder
Case, Part 2" (fetched 2026-10-03 from the Internet Archive capture of
the 2011-04-05 FBI page):

  https://web.archive.org/web/20110405112022/http://www.fbi.gov/news/stories/2011/march/cryptanalysis_032911

Original page:

  http://www.fbi.gov/news/stories/2011/march/cryptanalysis_032911

The article states four steps: determine the language, determine the
system, reconstruct the key, and reconstruct the plaintext. The printed
cipher is:

  Nffu nf bu uif qbsl bu oppo

The printed key is that every character shifted one letter to the right
in the alphabet. The printed solution is:

  Meet me at the park at noon

The period after the cipher in the article closes that sentence. It is
not a ciphertext character. Spaces stay in place. Letter case follows
the ciphertext.

This module is a **known classical-cipher** solver (a known-cipher
solver). It applies that published shift. It is **not** an
unknown-script reading and **not** a claim about army message Nr. 86.
It does not read Kryptos K4, the Voynich manuscript, Linear A, the
Indus script, or rongorongo. It does not read the unsolved notes
discussed in the same FBI article.
"""

from __future__ import annotations

from engine.alphabet import from_ints, letters_only, reinject, to_ints
from engine.result import SolveResult

FBI_LETTER_SHIFT_URL = (
    "https://web.archive.org/web/20110405112022/"
    "http://www.fbi.gov/news/stories/2011/march/cryptanalysis_032911"
)
FBI_LETTER_SHIFT_CIPHER = "Nffu nf bu uif qbsl bu oppo"
FBI_LETTER_SHIFT_PLAIN = "Meet me at the park at noon"
FBI_LETTER_SHIFT_RIGHT = 1

_SCOPE = (
    "Known classical-cipher check of the FBI published one-letter "
    "shift. Not an unknown-script reading. Not a claim about army "
    "message Nr. 86, Kryptos K4, Voynich, Linear A, Indus, or "
    "rongorongo, and not a reading of the unsolved notes in the same "
    "FBI article."
)


def _shift_letters(text: str, delta: int) -> str:
    letters = letters_only(text)
    if not letters:
        raise ValueError("text has no letters")
    seq = [(n + delta) % 26 for n in to_ints(letters)]
    return reinject(text, from_ints(seq))


def fbi_letter_shift_encrypt(text: str, shift_right: int = FBI_LETTER_SHIFT_RIGHT) -> str:
    """Shift each letter right by shift_right. Non-letters stay put."""
    return _shift_letters(text, shift_right)


def fbi_letter_shift_decrypt(text: str, shift_right: int = FBI_LETTER_SHIFT_RIGHT) -> str:
    """Undo a right shift of shift_right. Non-letters stay put."""
    return _shift_letters(text, -shift_right)


def solve_fbi_letter_shift(
    text: str, *, shift_right: int = FBI_LETTER_SHIFT_RIGHT
) -> SolveResult:
    """Recover plaintext for the published FBI one-letter right shift.

    Known-cipher decrypt only. Not an unknown-script reading and not a
    claim about army message Nr. 86, Kryptos K4, Voynich, Linear A,
    Indus, or rongorongo.
    """
    if shift_right % 26 == 0 and letters_only(text) == "":
        raise ValueError("text has no letters")
    plaintext = fbi_letter_shift_decrypt(text, shift_right)
    letter_count = sum(ch.isalpha() for ch in plaintext)
    return SolveResult(
        method="fbi-letter-shift",
        plaintext=plaintext,
        key=str(shift_right),
        score=float(letter_count),
        details={
            "shift_right": shift_right % 26,
            "letters": letter_count,
            "mode": "known_fbi_letter_shift",
            "variant": "caesar_shift_right",
            "scope": _SCOPE,
            "source_url": FBI_LETTER_SHIFT_URL,
        },
    )


__all__ = [
    "FBI_LETTER_SHIFT_CIPHER",
    "FBI_LETTER_SHIFT_PLAIN",
    "FBI_LETTER_SHIFT_RIGHT",
    "FBI_LETTER_SHIFT_URL",
    "fbi_letter_shift_decrypt",
    "fbi_letter_shift_encrypt",
    "solve_fbi_letter_shift",
]
