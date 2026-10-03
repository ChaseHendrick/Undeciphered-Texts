"""Normalize Roman inscription spelling.

Latin is a known language. This module only rewrites letters and word
dividers. It does not decipher an unknown script, and it does not decide
what an undeciphered text means.

Epigraphic form: capitals, consonantal and vocalic U both written V, J
written I, interpuncts turned into spaces.

Classical form: J becomes I, and V becomes U when it is the vocalic letter
in the usual inscription convention:

- QV is QU
- V before a consonant, or at the end of a word, is U
- V before a vowel stays V when it is word-initial or follows a vowel
  (VENI, DIVISA)

A vowel written V after another consonant and before a vowel is left as V
(SERVARE stays SERVARE; PUER would be left as PVER). That case is ambiguous
without a dictionary. The limit is recorded in docs/latin-roman-reader.md.
"""

from __future__ import annotations

import unicodedata

# Word dividers used in diplomatic transcriptions of Latin inscriptions.
# ASCII "." is not one of them. It is dropped, so M.AGRIPPA stays one token.
INTERPUNCTS = frozenset(
    {
        "\u00b7",  # middle dot
        "\u0387",  # greek ano teleia
        "\u16eb",  # runic single punctuation
        "\u2022",  # bullet
        "\u2027",  # hyphenation point
        "\u2219",  # bullet operator
        "\u22c5",  # dot operator
        "\u2e31",  # word separator middle dot
    }
)

_VOWELS = frozenset("AEIOU")


def strip_marks(text: str) -> str:
    """Drop macrons and other combining marks. Letters stay uppercase later."""
    decomposed = unicodedata.normalize("NFD", text)
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")


def _letters_and_spaces(text: str, *, u_to_v: bool) -> str:
    cleaned = strip_marks(text)
    out: list[str] = []
    for ch in cleaned:
        if ch in INTERPUNCTS or ch.isspace():
            out.append(" ")
            continue
        if not ch.isalpha():
            continue
        upper = ch.upper()
        if upper == "J":
            upper = "I"
        elif u_to_v and upper == "U":
            upper = "V"
        if "A" <= upper <= "Z":
            out.append(upper)
    return " ".join("".join(out).split())


def to_epigraphic(text: str) -> str:
    """Capitals with V for U, I for J, and interpuncts as spaces."""
    return _letters_and_spaces(text, u_to_v=True)


def _classical_token(token: str) -> str:
    chars = list(token)
    for i, ch in enumerate(chars):
        if ch != "V":
            continue
        prev = chars[i - 1] if i else ""
        nxt = chars[i + 1] if i + 1 < len(chars) else ""
        if prev == "Q" or nxt not in _VOWELS:
            chars[i] = "U"
    return "".join(chars)


def to_classical(text: str) -> str:
    """Epigraphic capitals rewritten toward classical U/V, J already folded to I."""
    epigraphic_letters = _letters_and_spaces(text, u_to_v=False)
    # _letters_and_spaces already folded J to I and did not map U to V,
    # so a typed U is still U. Map remaining vocalic V.
    tokens = [_classical_token(token) for token in epigraphic_letters.split()]
    return " ".join(tokens)
