"""Tridigital known-key solver.

The American Cryptogram Association cipher sheet (fetched 2026-10-02)
describes Tridigital:

  https://www.cryptogram.org/downloads/aca.info/ciphers/Tridigital.pdf

A 10-letter keyword is numbered in alphabetical order. The first letter
in that order is 1, then 2, and so on through 9, and the last letter is
0 (the digit used for 10). That 10-digit row sits above a block that is
10 columns wide. A second keyword builds a mixed alphabet: write the
keyword, skip repeated letters, then the unused letters of A-Z. Those
26 letters fill the block in rows of 9, leaving the last column blank.
The digit above the blank column is the word separator. Every other
plaintext letter is replaced by the digit above its column.

On that sheet the digit keyword is NOVELCRAFT (digits 6703528149) and
the alphabet keyword is DRAGONFLY. The plaintext sentence is "the ides
of march". The ciphertext is 03095 60795 89107 73.

Each digit other than the separator stands for two or three letters, so
the key alone does not pick one letter. This solver keeps every letter
in the column, splits the ciphertext on the separator, and chooses the
lexicon word of that length with the best frequency rank. The lexicon
is the 40,000 most frequent English words in engine/data/tridigital_lexicon.txt
(membership from the public-domain dwyl words_alpha list, order from
Peter Norvig's count_1w.txt, both fetched 2026-10-02). For the sheet's
sentence that choice is THE IDES OF MARCH.

A second published walk-through (CryptoCrack, fetched 2026-10-02) uses
digit keyword TRAMPOLINE and alphabet keyword OSCARWILDE. This module
reproduces that ciphertext as well.

  https://sites.google.com/site/cryptocrackprogram/user-guide/cipher-types/other/tridigital

This module is a **known classical-cipher** solver (a known-cipher
solver). It recovers a reading only when both keywords are supplied.
It is **not** an unknown-script reading and **not** a claim about
army message Nr. 86.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from engine.alphabet import ALPHABET
from engine.result import SolveResult

# ACA Tridigital sheet (fetched 2026-10-02).
ACA_TRIDIGITAL_URL = (
    "https://www.cryptogram.org/downloads/aca.info/ciphers/Tridigital.pdf"
)
ACA_TRIDIGITAL_DIGIT_KEYWORD = "NOVELCRAFT"
ACA_TRIDIGITAL_ALPHABET_KEYWORD = "DRAGONFLY"
ACA_TRIDIGITAL_KEY = "NOVELCRAFT|DRAGONFLY"
ACA_TRIDIGITAL_DIGIT_KEY = "6703528149"
ACA_TRIDIGITAL_PLAIN = "THE IDES OF MARCH"
ACA_TRIDIGITAL_CIPHER = "03095607958910773"
ACA_TRIDIGITAL_CIPHER_GROUPED = "03095 60795 89107 73."

# CryptoCrack user guide (fetched 2026-10-02). Not the certificate example.
CRYPTOCRACK_TRIDIGITAL_URL = (
    "https://sites.google.com/site/cryptocrackprogram/user-guide/"
    "cipher-types/other/tridigital"
)
CRYPTOCRACK_TRIDIGITAL_KEY = "TRAMPOLINE|OSCARWILDE"
CRYPTOCRACK_TRIDIGITAL_PLAIN = (
    "SOME CAUSE HAPPINESS WHEREVER THEY GO OTHERS WHENEVER THEY GO"
)
CRYPTOCRACK_TRIDIGITAL_CIPHER = (
    "9030215590285004609927808080821804250201808927806080821804250"
)

_SCOPE = (
    "Known classical Tridigital cipher solver only; "
    "not an unknown-script reading and not a claim about army message Nr. 86."
)

_LEXICON_PATH = (
    Path(__file__).resolve().parents[1] / "data" / "tridigital_lexicon.txt"
)
_DIGIT_RANKS = "1234567890"


class _Node:
    __slots__ = ("nxt", "rank")

    def __init__(self) -> None:
        self.nxt: dict[str, _Node] = {}
        self.rank: int | None = None


def _letters(text: str) -> str:
    return "".join(ch.upper() for ch in text if "A" <= ch.upper() <= "Z")


def parse_tridigital_key(key: str) -> tuple[str, str]:
    """Split ``digit-keyword|alphabet-keyword`` into two A-Z keywords."""
    if "|" not in key:
        raise ValueError(
            "Tridigital key must be digit-keyword|alphabet-keyword"
        )
    digit_part, alphabet_part = key.split("|", 1)
    digit_keyword = _letters(digit_part)
    alphabet_keyword = _letters(alphabet_part)
    if len(digit_keyword) != 10 or len(set(digit_keyword)) != 10:
        raise ValueError(
            "Tridigital digit keyword must be 10 distinct letters"
        )
    if not alphabet_keyword:
        raise ValueError("Tridigital alphabet keyword must contain a letter")
    return digit_keyword, alphabet_keyword


def digit_key_from_keyword(keyword: str) -> str:
    """Number a 10-letter keyword 1..9 then 0, in alphabetical order.

    An earlier copy would get the smaller number, but the keyword must
    already be 10 distinct letters so each digit is used once.
    """
    cleaned = _letters(keyword)
    if len(cleaned) != 10 or len(set(cleaned)) != 10:
        raise ValueError("digit keyword must be 10 distinct letters")
    order = sorted(range(10), key=lambda i: (cleaned[i], i))
    digits = [""] * 10
    for rank, index in enumerate(order):
        digits[index] = _DIGIT_RANKS[rank]
    return "".join(digits)


def mixed_alphabet(keyword: str) -> str:
    """Keyword alphabet: keyword letters first, then the unused A-Z letters."""
    seen: list[str] = []
    for ch in _letters(keyword):
        if ch not in seen:
            seen.append(ch)
    for ch in ALPHABET:
        if ch not in seen:
            seen.append(ch)
    if len(seen) != 26:
        raise ValueError("mixed alphabet must contain 26 letters")
    return "".join(seen)


def column_letters(digit_keyword: str, alphabet_keyword: str) -> tuple[str, dict[str, str], str]:
    """Return the digit row, a map of digit to column letters, and the separator.

    The mixed alphabet is written in rows of 9. The tenth column is blank
    and its digit is the word separator. The last letter cell is empty
    because 26 letters do not fill 27 cells.
    """
    digits = digit_key_from_keyword(digit_keyword)
    letters = mixed_alphabet(alphabet_keyword)
    columns: dict[str, str] = {digit: "" for digit in digits}
    for index, ch in enumerate(letters):
        row, col = divmod(index, 9)
        if row > 2:
            break
        columns[digits[col]] += ch
    separator = digits[9]
    del columns[separator]
    return digits, columns, separator


@lru_cache(maxsize=1)
def _lexicon_trie() -> _Node:
    root = _Node()
    rank = 0
    for line in _LEXICON_PATH.read_text(encoding="utf-8").splitlines():
        word = line.strip().upper()
        if not word or any(ch < "A" or ch > "Z" for ch in word):
            continue
        node = root
        for ch in word:
            nxt = node.nxt.get(ch)
            if nxt is None:
                nxt = _Node()
                node.nxt[ch] = nxt
            node = nxt
        if node.rank is None:
            node.rank = rank
            rank += 1
    if rank == 0:
        raise ValueError("Tridigital lexicon is empty")
    return root


def _best_word(chunk: str, columns: dict[str, str]) -> tuple[int, str]:
    """Best-ranked lexicon word whose letters sit in these digit columns."""
    root = _lexicon_trie()
    best_rank: int | None = None
    best_word = ""

    def walk(pos: int, node: _Node, acc: list[str]) -> None:
        nonlocal best_rank, best_word
        if pos == len(chunk):
            if node.rank is None:
                return
            if best_rank is None or node.rank < best_rank:
                best_rank = node.rank
                best_word = "".join(acc)
            return
        for ch in columns[chunk[pos]]:
            nxt = node.nxt.get(ch)
            if nxt is None:
                continue
            acc.append(ch)
            walk(pos + 1, nxt, acc)
            acc.pop()

    walk(0, root, [])
    if best_rank is None:
        raise ValueError(
            "no lexicon word matches a Tridigital ciphertext word"
        )
    return best_rank, best_word


def tridigital_encrypt(text: str, key: str) -> str:
    """Encrypt with a known Tridigital key.

    Whitespace between words becomes the separator digit. Other
    non-letters are dropped. A run of whitespace is one separator.
    """
    digit_keyword, alphabet_keyword = parse_tridigital_key(key)
    _digits, columns, separator = column_letters(digit_keyword, alphabet_keyword)
    letter_to_digit: dict[str, str] = {}
    for digit, letters in columns.items():
        for ch in letters:
            letter_to_digit[ch] = digit
    out: list[str] = []
    pending_space = False
    started = False
    for ch in text:
        if ch.isspace():
            if started:
                pending_space = True
            continue
        if not ("A" <= ch.upper() <= "Z"):
            continue
        if pending_space:
            out.append(separator)
            pending_space = False
        out.append(letter_to_digit[ch.upper()])
        started = True
    if not out:
        raise ValueError("text has no letters")
    return "".join(out)


def tridigital_decrypt(text: str, key: str) -> str:
    """Decrypt with a known Tridigital key.

    Split on the separator digit. For each word, take the lexicon entry
    with the best frequency rank whose letters lie in the keyed columns.
    """
    digit_keyword, alphabet_keyword = parse_tridigital_key(key)
    _digits, columns, separator = column_letters(digit_keyword, alphabet_keyword)
    allowed = set(columns) | {separator}
    stream = [ch for ch in text if ch in "0123456789"]
    if not stream:
        raise ValueError("ciphertext has no digits")
    if any(ch not in allowed for ch in stream):
        raise ValueError("ciphertext digit is not in the Tridigital key")
    chunks = [chunk for chunk in "".join(stream).split(separator) if chunk]
    if not chunks:
        raise ValueError("ciphertext has no words")
    words = [_best_word(chunk, columns)[1] for chunk in chunks]
    return " ".join(words)


def solve_tridigital(text: str, *, key: str) -> SolveResult:
    """Recover a Tridigital reading when both keywords are known.

    Known-cipher decrypt only. Not an unknown-script reading and not a
    claim about army message Nr. 86.
    """
    digit_keyword, alphabet_keyword = parse_tridigital_key(key)
    digits, _columns, separator = column_letters(digit_keyword, alphabet_keyword)
    plaintext = tridigital_decrypt(text, key)
    letter_count = sum(ch.isalpha() for ch in plaintext)
    return SolveResult(
        method="tridigital",
        plaintext=plaintext,
        key=f"{digit_keyword}|{alphabet_keyword}",
        score=float(letter_count),
        details={
            "key": f"{digit_keyword}|{alphabet_keyword}",
            "digit_keyword": digit_keyword,
            "alphabet_keyword": alphabet_keyword,
            "digit_key": digits,
            "separator": separator,
            "letters": letter_count,
            "mode": "known_tridigital",
            "variant": "column_digit_word_separator",
            "scope": _SCOPE,
            "source_url": ACA_TRIDIGITAL_URL,
        },
    )


__all__ = [
    "ACA_TRIDIGITAL_ALPHABET_KEYWORD",
    "ACA_TRIDIGITAL_CIPHER",
    "ACA_TRIDIGITAL_CIPHER_GROUPED",
    "ACA_TRIDIGITAL_DIGIT_KEY",
    "ACA_TRIDIGITAL_DIGIT_KEYWORD",
    "ACA_TRIDIGITAL_KEY",
    "ACA_TRIDIGITAL_PLAIN",
    "ACA_TRIDIGITAL_URL",
    "CRYPTOCRACK_TRIDIGITAL_CIPHER",
    "CRYPTOCRACK_TRIDIGITAL_KEY",
    "CRYPTOCRACK_TRIDIGITAL_PLAIN",
    "CRYPTOCRACK_TRIDIGITAL_URL",
    "column_letters",
    "digit_key_from_keyword",
    "mixed_alphabet",
    "parse_tridigital_key",
    "solve_tridigital",
    "tridigital_decrypt",
    "tridigital_encrypt",
]
