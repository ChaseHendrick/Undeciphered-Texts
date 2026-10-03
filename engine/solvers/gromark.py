"""Gromark known-key solver: mixed alphabet plus a numeric running key.

Gromark (GROnsfeld with Mixed Alphabet and Running Key) is the ACA
cipher described on the American Cryptogram Association cipher sheet.
A keyword builds a K2M cipher alphabet: write the keyword (duplicate
letters dropped) and then the unused letters of A-Z into rows whose
width is the keyword, and read the columns off in alphabetical order
of the keyword letters. A 5-digit primer is extended by adding
successive pairs of digits and keeping only the units digit (the 1st
plus the 2nd give the 6th, the 2nd plus the 3rd give the 7th, and so
on). Each plaintext letter is shifted that many places to the right in
A-Z, and the letter in the cipher alphabet at that position is taken.

The worked example used here is the one on that sheet (fetched
2026-10-02):

  https://www.cryptogram.org/downloads/aca.info/ciphers/Gromark.pdf

Keyword: ENIGMA
Primer: 23452
Plaintext: THEREAREUPTOTENSUBSTITUTESPERLETTER
  (the sheet prints these letters in lowercase)
Ciphertext: NFYCKBTIJCNWZYCACJNAYNLQPWWSTWPJQFL

This module is a **known classical-cipher** solver. It recovers plaintext
only when the keyword and primer are supplied. It is **not** an
unknown-script reading and **not** a claim about army message Nr. 86.
"""

from __future__ import annotations

from engine.alphabet import ALPHABET, letters_only, reinject
from engine.result import SolveResult

# American Cryptogram Association Gromark sheet (fetched 2026-10-02).
# https://www.cryptogram.org/downloads/aca.info/ciphers/Gromark.pdf
ACA_GROMARK_URL = (
    "https://www.cryptogram.org/downloads/aca.info/ciphers/Gromark.pdf"
)
ACA_GROMARK_KEYWORD = "ENIGMA"
ACA_GROMARK_PRIMER = "23452"
ACA_GROMARK_KEY = "ENIGMA 23452"
ACA_GROMARK_PLAIN = "THEREAREUPTOTENSUBSTITUTESPERLETTER"
ACA_GROMARK_CIPHER = "NFYCKBTIJCNWZYCACJNAYNLQPWWSTWPJQFL"
ACA_GROMARK_ALPHABET = "AJRXEBKSYGFPVIDOUMHQWNCLTZ"
ACA_GROMARK_RUNNING_KEY = "23452579772664982037023072537978066"

_SCOPE = (
    "Known classical Gromark cipher solver only; "
    "not an unknown-script reading and not a claim about army message Nr. 86."
)


def gromark_keyword(keyword: str) -> str:
    """A-Z keyword with duplicate letters removed, first occurrence kept."""
    unique: list[str] = []
    for ch in letters_only(keyword):
        if ch not in unique:
            unique.append(ch)
    if not unique:
        raise ValueError("Gromark keyword must contain at least one letter")
    return "".join(unique)


def gromark_primer(primer: str) -> str:
    """A 5-digit primer. Spaces are ignored. Letters are rejected."""
    if any(ch.isalpha() for ch in primer):
        raise ValueError("Gromark primer must be 5 digits, not letters")
    digits = "".join(ch for ch in primer if ch.isdigit())
    if len(digits) != 5:
        raise ValueError("Gromark primer must be exactly 5 digits")
    return digits


def split_gromark_key(key: str) -> tuple[str, str]:
    """Split 'KEYWORD 23452' into a keyword and a 5-digit primer.

    The last whitespace-separated token is the primer. Earlier tokens
    are the keyword.
    """
    parts = key.split()
    if len(parts) < 2:
        raise ValueError(
            "Gromark key must be a keyword and a 5-digit primer, "
            "for example ENIGMA 23452"
        )
    keyword = gromark_keyword("".join(parts[:-1]))
    primer = gromark_primer(parts[-1])
    return keyword, primer


def gromark_cipher_alphabet(keyword: str) -> str:
    """K2M cipher alphabet: rows filled left to right, columns read A-Z.

    The sheet's ENIGMA block reads off as AJRXEBKSYGFPVIDOUMHQWNCLTZ.
    """
    head = gromark_keyword(keyword)
    width = len(head)
    keyed = head + "".join(ch for ch in ALPHABET if ch not in head)
    columns: list[list[str]] = [[] for _ in range(width)]
    for index, ch in enumerate(keyed):
        columns[index % width].append(ch)
    order = sorted(range(width), key=lambda i: head[i])
    return "".join(ch for col in order for ch in columns[col])


def gromark_running_key(primer: str, length: int) -> str:
    """Extend a 5-digit primer until it covers `length` letters.

    Each new digit is the units digit of the sum of the digits five and
    four places back (1st+2nd makes the 6th).
    """
    if length < 1:
        raise ValueError("running key length must be at least 1")
    digits = [int(ch) for ch in gromark_primer(primer)]
    while len(digits) < length:
        digits.append((digits[-5] + digits[-4]) % 10)
    return "".join(str(d) for d in digits[:length])


def gromark_encrypt(text: str, key: str) -> str:
    """Encrypt with a known Gromark keyword and primer. Non-letters are dropped.

    Find the plaintext letter in A-Z, count right by the running-key digit,
    and take the cipher-alphabet letter in that column.
    """
    keyword, primer = split_gromark_key(key)
    plain = letters_only(text)
    if not plain:
        raise ValueError("text has no letters")
    alphabet = gromark_cipher_alphabet(keyword)
    shifts = gromark_running_key(primer, len(plain))
    out = [
        alphabet[(ord(ch) - 65 + int(digit)) % 26]
        for ch, digit in zip(plain, shifts)
    ]
    return "".join(out)


def gromark_decrypt(text: str, key: str) -> str:
    """Decrypt with a known Gromark keyword and primer.

    Find the ciphertext letter in the cipher alphabet, count left by the
    running-key digit, and read that column of A-Z.
    """
    keyword, primer = split_gromark_key(key)
    cipher = letters_only(text)
    if not cipher:
        raise ValueError("text has no letters")
    alphabet = gromark_cipher_alphabet(keyword)
    shifts = gromark_running_key(primer, len(cipher))
    out: list[str] = []
    for ch, digit in zip(cipher, shifts):
        if ch not in alphabet:
            raise ValueError(f"letter {ch} is outside the cipher alphabet")
        index = (alphabet.index(ch) - int(digit)) % 26
        out.append(chr(65 + index))
    return "".join(out)


def solve_gromark(text: str, *, key: str) -> SolveResult:
    """Recover Gromark plaintext when the keyword and primer are known.

    Known-cipher decrypt only. Not an unknown-script reading and not a
    claim about army message Nr. 86.
    """
    keyword, primer = split_gromark_key(key)
    plain_letters = gromark_decrypt(text, f"{keyword} {primer}")
    rendered = (
        reinject(text, plain_letters)
        if any(not ch.isalpha() for ch in text)
        else plain_letters
    )
    combined = f"{keyword} {primer}"
    return SolveResult(
        method="gromark",
        plaintext=rendered,
        key=combined,
        score=float(len(plain_letters)),
        details={
            "key": combined,
            "keyword": keyword,
            "primer": primer,
            "cipher_alphabet": gromark_cipher_alphabet(keyword),
            "letters": len(letters_only(text)),
            "mode": "known_gromark",
            "variant": "k2m_mixed_alphabet_numeric_running_key",
            "scope": _SCOPE,
            "source_url": ACA_GROMARK_URL,
        },
    )


__all__ = [
    "ACA_GROMARK_ALPHABET",
    "ACA_GROMARK_CIPHER",
    "ACA_GROMARK_KEY",
    "ACA_GROMARK_KEYWORD",
    "ACA_GROMARK_PLAIN",
    "ACA_GROMARK_PRIMER",
    "ACA_GROMARK_RUNNING_KEY",
    "ACA_GROMARK_URL",
    "gromark_cipher_alphabet",
    "gromark_decrypt",
    "gromark_encrypt",
    "gromark_keyword",
    "gromark_primer",
    "gromark_running_key",
    "solve_gromark",
    "split_gromark_key",
]
