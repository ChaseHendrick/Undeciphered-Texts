"""Grandpre known-key solver.

The American Cryptogram Association cipher sheet (fetched 2026-10-02)
describes Grandpre:

  https://www.cryptogram.org/downloads/aca.info/ciphers/Grandpre.pdf

An n-by-n square (n from 6 to 10; 8 is the usual size) is filled with
n words of n letters. The first letter of each word, read down, is
itself a word. Rows and columns are numbered 1 through n. On a 10-by-10
square the labels are 1 through 9 and then 0, and 0 means the tenth
row or column. A plaintext letter is replaced by one row-column pair
for a cell that holds that letter. A letter that appears more than
once may use any of those pairs, so encryption is homophonic.
Decryption reads each pair back to the single cell it names.

On that sheet the square is:

  1 2 3 4 5 6 7 8
  L A D Y B U G S
  A Z I M U T H S
  C A L F S K I N
  Q U A C K I S H
  U N J O V I A L
  E V U L S I O N
  R O W D Y I S M
  S E X T U P L Y

The first column is LACQUERS. The plaintext sentence is "The first
column is the keyword." One published encipherment is:

  84 27 82 34 56 71 77 26 44 54 64 63 78
  52 66 65 84 27 82 36 61 88 73 54 71 13

Spaces are not encrypted, so the recovered letters are
THEFIRSTCOLUMNISTHEKEYWORD. Those pairs are one valid encipherment.
`grandpre_encrypt` does not try to copy that choice. It uses the first
cell in row-major order for each letter, which still decrypts to the
same letters.

This module is a **known classical-cipher** solver (a known-cipher
solver). It recovers a reading only when the square is supplied.
It is **not** an unknown-script reading and **not** a claim about
army message Nr. 86. It does not read Kryptos K4, the Voynich
manuscript, Linear A, the Indus script, or rongorongo.
"""

from __future__ import annotations

from engine.result import SolveResult

# ACA Grandpre sheet (fetched 2026-10-02).
ACA_GRANDPRE_URL = "https://www.cryptogram.org/downloads/aca.info/ciphers/Grandpre.pdf"
ACA_GRANDPRE_KEY = (
    "LADYBUGS|AZIMUTHS|CALFSKIN|QUACKISH|UNJOVIAL|EVULSION|ROWDYISM|SEXTUPLY"
)
ACA_GRANDPRE_KEYWORD = "LACQUERS"
ACA_GRANDPRE_PLAIN = "THEFIRSTCOLUMNISTHEKEYWORD"
ACA_GRANDPRE_PHRASE = "THE FIRST COLUMN IS THE KEYWORD"
ACA_GRANDPRE_CIPHER = "8427823456717726445464637852666584278236618873547113"
ACA_GRANDPRE_CIPHER_GROUPED = (
    "84 27 82 34 56 71 77 26 44 54 64 63 78 "
    "52 66 65 84 27 82 36 61 88 73 54 71 13"
)

_SCOPE = (
    "Known classical Grandpre cipher solver only; "
    "not an unknown-script reading and not a claim about army message Nr. 86."
)


def _labels(size: int) -> str:
    if size == 10:
        return "1234567890"
    return "".join(str(i) for i in range(1, size + 1))


def parse_grandpre_key(key: str) -> tuple[str, ...]:
    """Split a `|` key into n words of n uppercase letters, n from 6 to 10."""
    parts = key.split("|")
    if not 6 <= len(parts) <= 10:
        raise ValueError("Grandpre key must be 6 to 10 words separated by |")
    words: list[str] = []
    size = len(parts)
    for part in parts:
        stripped = part.strip()
        if not stripped or any(not ("A" <= ch.upper() <= "Z") for ch in stripped):
            raise ValueError("each Grandpre word must be letters only")
        word = stripped.upper()
        if len(word) != size:
            raise ValueError("each Grandpre word must have one letter per column")
        words.append(word)
    return tuple(words)


def _index(labels: str, digit: str) -> int:
    if digit not in labels:
        raise ValueError("ciphertext digit is not a Grandpre row or column label")
    return labels.index(digit)


def grandpre_encrypt(text: str, key: str) -> str:
    """Encrypt with a known Grandpre square.

    Each letter uses the first cell in row-major order that holds it.
    Spaces and other non-letters are dropped. A letter missing from the
    square is an error. The published sheet may pick a later cell for
    the same letter; decryption of either pair returns that letter.
    """
    words = parse_grandpre_key(key)
    size = len(words)
    labels = _labels(size)
    first: dict[str, str] = {}
    for row, word in enumerate(words):
        for col, ch in enumerate(word):
            first.setdefault(ch, labels[row] + labels[col])
    out: list[str] = []
    for ch in text:
        if not ("A" <= ch.upper() <= "Z"):
            continue
        letter = ch.upper()
        if letter not in first:
            raise ValueError("plaintext letter is not in the Grandpre square")
        out.append(first[letter])
    if not out:
        raise ValueError("text has no letters")
    return "".join(out)


def grandpre_decrypt(text: str, key: str) -> str:
    """Decrypt with a known Grandpre square.

    Digits are read in pairs, row then column. Non-digits are ignored.
    """
    words = parse_grandpre_key(key)
    labels = _labels(len(words))
    digits = [ch for ch in text if ch.isdigit()]
    if not digits:
        raise ValueError("ciphertext has no digits")
    if len(digits) % 2 != 0:
        raise ValueError("Grandpre ciphertext must contain an even number of digits")
    out: list[str] = []
    for i in range(0, len(digits), 2):
        row = _index(labels, digits[i])
        col = _index(labels, digits[i + 1])
        out.append(words[row][col])
    return "".join(out)


def solve_grandpre(text: str, *, key: str) -> SolveResult:
    """Recover a Grandpre reading when the square is known.

    Known-cipher decrypt only. Not an unknown-script reading and not a
    claim about army message Nr. 86, Kryptos K4, Voynich, Linear A,
    Indus, or rongorongo.
    """
    words = parse_grandpre_key(key)
    plaintext = grandpre_decrypt(text, key)
    keyword = "".join(word[0] for word in words)
    letter_count = sum(ch.isalpha() for ch in plaintext)
    return SolveResult(
        method="grandpre",
        plaintext=plaintext,
        key="|".join(words),
        score=float(letter_count),
        details={
            "key": "|".join(words),
            "keyword": keyword,
            "size": len(words),
            "letters": letter_count,
            "mode": "known_grandpre",
            "variant": "coordinate_square",
            "scope": _SCOPE,
            "source_url": ACA_GRANDPRE_URL,
        },
    )


__all__ = [
    "ACA_GRANDPRE_CIPHER",
    "ACA_GRANDPRE_CIPHER_GROUPED",
    "ACA_GRANDPRE_KEY",
    "ACA_GRANDPRE_KEYWORD",
    "ACA_GRANDPRE_PHRASE",
    "ACA_GRANDPRE_PLAIN",
    "ACA_GRANDPRE_URL",
    "grandpre_decrypt",
    "grandpre_encrypt",
    "parse_grandpre_key",
    "solve_grandpre",
]
