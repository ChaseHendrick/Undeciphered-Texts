"""Slidefair known-key solver (ACA digraph rectangle on a keyed tableau).

The American Cryptogram Association cipher sheet (fetched 2026-10-03)
describes Slidefair:

  https://www.cryptogram.org/downloads/aca.info/ciphers/Slidefair.pdf

Encipherment is by pairs. The keyword sets the period: one key letter
per pair, then the keyword repeats. The first plaintext letter is taken
in the top alphabet (A through Z). The second is taken in the row of
the current key letter. Those two cells are opposite corners of a
rectangle. The other two corners are the ciphertext pair, and the top
alphabet letter is written first. If both letters already stand in one
column, the ciphertext pair is the column immediately to the right
(wrapping from Z back to A).

The sheet prints three table shapes. The worked example uses the
Vigenere table. Variant and Beaufort are the other two shapes, checked
on the same sheet with key letter B.

  Key: DIGRAPH
  Sentence: The Slidefair can be used with Vigenere, Variant or Beaufort.
  Letter stream: THESLIDEFAIRCANBEUSEDWITHVIGENEREVARIANTORBEAUFORT
  Ciphertext: EW KM CR NU AF CX TJ YQ MM YY FU TI GW ZP KH JM PK BS AI EC KV CF MI IL CI

Spaces, the comma, and the final period are not enciphered. The sheet
spells Vigenere with an accent; the accent is not a letter.

This module is a **known classical-cipher** solver (a known-cipher
solver). It recovers a reading only when the keyword and table are
supplied. It is **not** an unknown-script reading and **not** a claim
about army message Nr. 86.
"""

from __future__ import annotations

from engine.result import SolveResult

ACA_SLIDEFAIR_URL = (
    "https://www.cryptogram.org/downloads/aca.info/ciphers/Slidefair.pdf"
)
ACA_SLIDEFAIR_KEYWORD = "DIGRAPH"
ACA_SLIDEFAIR_TABLE = "vigenere"
ACA_SLIDEFAIR_SENTENCE = (
    "The Slidefair can be used with Vigenere, Variant or Beaufort."
)
ACA_SLIDEFAIR_PLAIN = "THESLIDEFAIRCANBEUSEDWITHVIGENEREVARIANTORBEAUFORT"
ACA_SLIDEFAIR_CIPHER = (
    "EW KM CR NU AF CX TJ YQ MM YY FU TI GW ZP "
    "KH JM PK BS AI EC KV CF MI IL CI"
)

# CryptoCrack Vigenere Slidefair quote (fetched 2026-10-03). The odd
# letter count is completed with X, and the apostrophe is not a letter.
CRYPTOCRACK_SLIDEFAIR_URL = (
    "https://sites.google.com/site/cryptocrackprogram/user-guide/cipher-types/substitution/slidefair"
)
CRYPTOCRACK_SLIDEFAIR_KEYWORD = "SLIDEFAIR"
CRYPTOCRACK_SLIDEFAIR_SENTENCE = (
    "If you do a job too well, you'll get stuck with it."
)
CRYPTOCRACK_SLIDEFAIR_PLAIN = "IFYOUDOAJOBTOOWELLYOULLGETSTUCKWITHITX"
CRYPTOCRACK_SLIDEFAIR_CIPHER = (
    "NA DJ VC XR KN OG PP XF UC WQ AF YT QH PW XZ WK LQ RY FL"
)

TABLES = ("vigenere", "variant", "beaufort")

_SCOPE = (
    "Known classical Slidefair cipher solver only; "
    "not an unknown-script reading and not a claim about army message Nr. 86."
)


def _letters(text: str) -> str:
    return "".join(ch.upper() for ch in text if ch.isalpha())


def slidefair_keyword(keyword: str) -> str:
    """Keyword letters in order. Repeats stay; they still advance the period."""
    letters = _letters(keyword)
    if not letters:
        raise ValueError("Slidefair keyword must contain at least one letter")
    return letters


def _normalize_table(table: str) -> str:
    name = table.strip().lower()
    if name not in TABLES:
        raise ValueError(
            "Slidefair table must be vigenere, variant, or beaufort"
        )
    return name


def _cell(table: str, shift: int, col: int) -> str:
    """Letter in one tableau row. The top alphabet is an unshifted A-Z row."""
    if table == "vigenere":
        value = (col + shift) % 26
    elif table == "variant":
        value = (col - shift) % 26
    else:
        value = (shift - col) % 26
    return chr(value + ord("A"))


def _column(table: str, shift: int, letter: str) -> int:
    for col in range(26):
        if _cell(table, shift, col) == letter:
            return col
    raise ValueError(f"letter {letter} is not in the Slidefair alphabet")


def _pair(first: str, second: str, key_letter: str, table: str, *, decrypt: bool) -> str:
    shift = ord(key_letter) - ord("A")
    col_top = _column("vigenere", 0, first)
    col_row = _column(table, shift, second)
    if col_top == col_row:
        step = -1 if decrypt else 1
        out_top = _cell("vigenere", 0, (col_top + step) % 26)
        out_row = _cell(table, shift, (col_row + step) % 26)
    else:
        out_top = _cell("vigenere", 0, col_row)
        out_row = _cell(table, shift, col_top)
    return out_top + out_row


def slidefair_encrypt(
    text: str,
    key: str,
    *,
    table: str = "vigenere",
    pad: str = "X",
) -> str:
    """Encrypt with a known Slidefair keyword. Non-letters are dropped.

    An odd letter count is completed with `pad` so the last pair is full.
    The result is space-separated digraphs, top letter first.
    """
    keyword = slidefair_keyword(key)
    kind = _normalize_table(table)
    pad_letter = _letters(pad)
    if len(pad_letter) != 1:
        raise ValueError("Slidefair pad must be one letter")
    letters = _letters(text)
    if not letters:
        raise ValueError("text has no letters")
    if len(letters) % 2 == 1:
        letters += pad_letter
    pairs: list[str] = []
    for index in range(0, len(letters), 2):
        key_letter = keyword[(index // 2) % len(keyword)]
        pairs.append(
            _pair(letters[index], letters[index + 1], key_letter, kind, decrypt=False)
        )
    return " ".join(pairs)


def slidefair_decrypt(
    text: str,
    key: str,
    *,
    table: str = "vigenere",
) -> str:
    """Decrypt with a known Slidefair keyword. Returns the uppercase letter stream.

    Spaces between digraphs are ignored. A final pad letter is not stripped.
    """
    keyword = slidefair_keyword(key)
    kind = _normalize_table(table)
    letters = _letters(text)
    if not letters:
        raise ValueError("text has no letters")
    if len(letters) % 2 != 0:
        raise ValueError("Slidefair ciphertext must contain an even number of letters")
    out: list[str] = []
    for index in range(0, len(letters), 2):
        key_letter = keyword[(index // 2) % len(keyword)]
        out.append(
            _pair(letters[index], letters[index + 1], key_letter, kind, decrypt=True)
        )
    return "".join(out)


def solve_slidefair(
    text: str,
    *,
    key: str,
    table: str = "vigenere",
) -> SolveResult:
    """Recover Slidefair plaintext when the keyword and table are known.

    Known-cipher decrypt only. Not an unknown-script reading and not a
    claim about army message Nr. 86.
    """
    keyword = slidefair_keyword(key)
    kind = _normalize_table(table)
    plain = slidefair_decrypt(text, keyword, table=kind)
    return SolveResult(
        method="slidefair",
        plaintext=plain,
        key=keyword,
        score=float(len(plain)),
        details={
            "key": keyword,
            "keyword": keyword,
            "table": kind,
            "period": len(keyword),
            "letters": len(plain),
            "mode": "known_slidefair",
            "variant": f"aca_{kind}_rectangle",
            "scope": _SCOPE,
            "source_url": ACA_SLIDEFAIR_URL,
        },
    )


__all__ = [
    "ACA_SLIDEFAIR_CIPHER",
    "ACA_SLIDEFAIR_KEYWORD",
    "ACA_SLIDEFAIR_PLAIN",
    "ACA_SLIDEFAIR_SENTENCE",
    "ACA_SLIDEFAIR_TABLE",
    "ACA_SLIDEFAIR_URL",
    "CRYPTOCRACK_SLIDEFAIR_CIPHER",
    "CRYPTOCRACK_SLIDEFAIR_KEYWORD",
    "CRYPTOCRACK_SLIDEFAIR_PLAIN",
    "CRYPTOCRACK_SLIDEFAIR_SENTENCE",
    "CRYPTOCRACK_SLIDEFAIR_URL",
    "TABLES",
    "slidefair_decrypt",
    "slidefair_encrypt",
    "slidefair_keyword",
    "solve_slidefair",
]
