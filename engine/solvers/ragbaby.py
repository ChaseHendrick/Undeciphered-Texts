"""Ragbaby known-key solver (ACA 24-letter alphabet).

The American Cryptogram Association cipher sheet (fetched 2026-10-02)
describes Ragbaby:

  https://www.cryptogram.org/downloads/aca.info/ciphers/Ragbaby.pdf

Historically the cipher uses a 24-letter keyed alphabet with I/J and
W/X paired. A keyword is written first, dropping repeated letters, and
the unused letters of that 24-letter alphabet follow in alphabetical
order. J in the keyword or the text is read as I, and X is read as W.

Word divisions are kept. A hyphenated word is one word, and so is a
word with an apostrophe. An asterisk before a proper noun is not a
letter and does not start a new word. Number the letters of each word
starting at 1 for the first word, 2 for the second word, and so on.
The count goes to 24 and then repeats (25 is 1). Each plaintext letter
is replaced by the letter that many places to the right in the keyed
alphabet. Decryption counts the same distance to the left.

On that sheet the keyed alphabet begins GROSBEAK and then the unused
letters, so the keyword is GROSBEAK:

  GROSBEAKCDFHILMNPQTUVWYZ

The plaintext sentence is "Word divisions are kept." The ciphertext,
word divisions kept, is YBBL HNGQDUFGL DEF HFYR.

This module is a **known classical-cipher** solver (a known-cipher
solver). It recovers a reading only when the keyword is supplied.
It is **not** an unknown-script reading and **not** a claim about
army message Nr. 86.
"""

from __future__ import annotations

from engine.result import SolveResult

# ACA Ragbaby sheet (fetched 2026-10-02).
ACA_RAGBABY_URL = "https://www.cryptogram.org/downloads/aca.info/ciphers/Ragbaby.pdf"
ACA_RAGBABY_KEYWORD = "GROSBEAK"
ACA_RAGBABY_ALPHABET = "GROSBEAKCDFHILMNPQTUVWYZ"
ACA_RAGBABY_PLAIN = "WORD DIVISIONS ARE KEPT."
ACA_RAGBABY_CIPHER = "YBBL HNGQDUFGL DEF HFYR."

# 24-letter alphabet: A-Z without J and without X.
_ALPHABET24 = "ABCDEFGHIKLMNOPQRSTUVWYZ"
_WORD_MARKS = "-'*"

_SCOPE = (
    "Known classical Ragbaby cipher solver only; "
    "not an unknown-script reading and not a claim about army message Nr. 86."
)


def _pair(ch: str) -> str | None:
    """Map one character onto the 24-letter alphabet, or None if it is not a letter.

    J is read as I and X is read as W, matching the sheet's pairing.
    """
    if not ch.isalpha():
        return None
    up = ch.upper()
    if up == "J":
        return "I"
    if up == "X":
        return "W"
    if up in _ALPHABET24:
        return up
    return None


def ragbaby_keyword(keyword: str) -> str:
    """Keyword letters in order, duplicates dropped, J/X paired to I/W."""
    seen: list[str] = []
    for ch in keyword:
        mapped = _pair(ch)
        if mapped and mapped not in seen:
            seen.append(mapped)
    if not seen:
        raise ValueError("Ragbaby keyword must contain at least one letter")
    return "".join(seen)


def keyed_alphabet(keyword: str) -> str:
    """24-letter keyed alphabet: keyword, then the unused letters in order."""
    head = ragbaby_keyword(keyword)
    return head + "".join(ch for ch in _ALPHABET24 if ch not in head)


def _transform(text: str, key: str, *, decrypt: bool) -> str:
    alphabet = keyed_alphabet(key)
    if not any(_pair(ch) is not None for ch in text):
        raise ValueError("text has no letters")
    out: list[str] = []
    word_index = 0
    in_word = False
    pos_in_word = 0
    for ch in text:
        mapped = _pair(ch)
        if mapped is None:
            if ch not in _WORD_MARKS:
                in_word = False
            out.append(ch)
            continue
        if not in_word:
            in_word = True
            word_index += 1
            pos_in_word = 0
        start = ((word_index - 1) % 24) + 1
        shift = ((start - 1 + pos_in_word) % 24) + 1
        pos_in_word += 1
        index = alphabet.index(mapped)
        step = -shift if decrypt else shift
        out.append(alphabet[(index + step) % 24])
    return "".join(out)


def ragbaby_encrypt(text: str, key: str) -> str:
    """Encrypt with a known Ragbaby keyword. Word spaces and punctuation stay.

    Each letter moves right in the keyed alphabet by its word number.
    J is enciphered as I, and X is enciphered as W.
    """
    return _transform(text, key, decrypt=False)


def ragbaby_decrypt(text: str, key: str) -> str:
    """Decrypt with a known Ragbaby keyword. Word spaces and punctuation stay.

    Each letter moves left in the keyed alphabet by its word number.
    """
    return _transform(text, key, decrypt=True)


def solve_ragbaby(text: str, *, key: str) -> SolveResult:
    """Recover Ragbaby plaintext when the keyword is known.

    Known-cipher decrypt only. Not an unknown-script reading and not a
    claim about army message Nr. 86.
    """
    keyword = ragbaby_keyword(key)
    plain = ragbaby_decrypt(text, keyword)
    letters = sum(_pair(ch) is not None for ch in text)
    return SolveResult(
        method="ragbaby",
        plaintext=plain,
        key=keyword,
        score=float(letters),
        details={
            "key": keyword,
            "keyword": keyword,
            "keyed_alphabet": keyed_alphabet(keyword),
            "letters": letters,
            "alphabet_size": 24,
            "mode": "known_ragbaby",
            "variant": "aca_24_ij_wx_paired",
            "scope": _SCOPE,
            "source_url": ACA_RAGBABY_URL,
        },
    )


__all__ = [
    "ACA_RAGBABY_ALPHABET",
    "ACA_RAGBABY_CIPHER",
    "ACA_RAGBABY_KEYWORD",
    "ACA_RAGBABY_PLAIN",
    "ACA_RAGBABY_URL",
    "keyed_alphabet",
    "ragbaby_decrypt",
    "ragbaby_encrypt",
    "ragbaby_keyword",
    "solve_ragbaby",
]
