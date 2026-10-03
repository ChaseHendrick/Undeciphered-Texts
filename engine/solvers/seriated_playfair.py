"""Seriated Playfair known-key solver.

The American Cryptogram Association cipher sheet (fetched 2026-10-03)
describes seriated Playfair:

  https://www.cryptogram.org/downloads/aca.info/ciphers/SeriatedPlayfair.pdf

Plaintext is written in horizontal 2-line groups whose width is the
period. Each column is one vertical pair. Those pairs are enciphered
with the ordinary Playfair rules (same row moves right, same column
moves down, otherwise the other corners of the rectangle, first letter's
row first). When the next plaintext letter would repeat the letter
above it, a null is inserted in that cell and the plaintext letter
waits for the next column. The sheet's null is X. Ciphertext is read
off horizontally, top row then bottom row of each period group.

The sheet's worked example uses period 6 and this square, which is the
keyword square for LOGARITHM (J omitted, I and J share a cell):

  L O G A R
  I T H M B
  C D E F K
  N P Q S U
  V W X Y Z

  Sentence: Come quickly we need help immediately. tom.
  Prepared: COMEQUICKLYWENEEDHXELPIMMEDIATELYTOM
  Ciphertext: NLBCS PCDFG XZQQC DCMGC GQTBH CFTRH FGWHG B

The X in the prepared stream is the null under the first E of the
second group (the E of "help" would otherwise sit under the E of
"needh"). Spaces, the period, and the five-letter grouping are not
letters.

PDF SHA-256 (fetched 2026-10-03, America/New_York):
8cce8115f416d4a6b8d133190cd26e0ca4aea3332ae432f0a366b66db08da94d

This module is a **known classical-cipher** solver (a known-cipher
solver). It recovers a reading only when the keyword and period are
supplied. It is **not** an unknown-script reading and **not** a claim
about Kryptos K4, Zodiac, Beale, McCormick, Voynich, or army message
Nr. 86.
"""

from __future__ import annotations

from engine.ciphers import two_square_letters
from engine.language import get_model
from engine.result import SolveResult
from engine.solvers.playfair import playfair_decrypt, playfair_encrypt, playfair_square

ACA_URL = "https://www.cryptogram.org/downloads/aca.info/ciphers/SeriatedPlayfair.pdf"
# sha256sum of the PDF fetched 2026-10-03.
ACA_PDF_SHA256 = "8cce8115f416d4a6b8d133190cd26e0ca4aea3332ae432f0a366b66db08da94d"
ACA_KEYWORD = "LOGARITHM"
ACA_PERIOD = 6
ACA_SENTENCE = "Come quickly we need help immediately. tom."
ACA_PLAIN = "COMEQUICKLYWENEEDHXELPIMMEDIATELYTOM"
ACA_CIPHER = "NLBCSPCDFGXZQQCDCMGCGQTBHCFTRHFGWHGB"
ACA_PRINTED_CIPHER = "NLBCS PCDFG XZQQC DCMGC GQTBH CFTRH FGWHG B"
ACA_SQUARE = "LOGARITHMBCDEFKNPQSUVWXYZ"

_SCOPE = (
    "Known classical seriated Playfair cipher solver only; "
    "not an unknown-script reading and not a claim about Kryptos K4, "
    "Zodiac, Beale, McCormick, Voynich, or army message Nr. 86."
)


def _keyword(keyword: str) -> str:
    cleaned = two_square_letters(keyword)
    if not cleaned:
        raise ValueError("Seriated Playfair keyword must contain at least one letter")
    return cleaned


def _period(period: int) -> int:
    if isinstance(period, bool) or not isinstance(period, int) or period < 1:
        raise ValueError("Seriated Playfair period must be a positive integer")
    return period


def _null_for(top: str, null: str) -> str:
    """Null letter that does not repeat the letter above it."""
    if len(null) != 1 or not null.isalpha() or null.upper() == "J":
        raise ValueError("null must be a single non-J letter")
    chosen = null.upper()
    if chosen == top:
        chosen = "Q" if top != "Q" else "Z"
    return chosen


def prepare_seriated_playfair(text: str, period: int, null: str = "X") -> str:
    """Write plaintext into 2-line period groups, inserting a vertical null.

    Non-letters are dropped and J is folded to I. A final incomplete group
    is filled with the null (or Q when the null would repeat the letter
    above it). The returned stream is what decrypt gives back, including
    those nulls.
    """
    width = _period(period)
    stream = list(two_square_letters(text))
    if not stream:
        raise ValueError("text has no letters")
    # Validate the null before the first pad.
    _null_for("A", null)
    out: list[str] = []
    while stream:
        top: list[str] = []
        for _ in range(width):
            if stream:
                top.append(stream.pop(0))
            else:
                top.append(_null_for("?", null))
        bottom: list[str] = []
        for col in range(width):
            if stream and stream[0] == top[col]:
                bottom.append(_null_for(top[col], null))
            elif stream:
                bottom.append(stream.pop(0))
            else:
                bottom.append(_null_for(top[col], null))
        out.extend(top)
        out.extend(bottom)
    return "".join(out)


def _blocks(letters: str, period: int) -> list[tuple[str, str]]:
    width = period
    block = 2 * width
    if len(letters) % block != 0:
        raise ValueError("Seriated Playfair length must fill 2-line period groups")
    groups: list[tuple[str, str]] = []
    for start in range(0, len(letters), block):
        chunk = letters[start : start + block]
        groups.append((chunk[:width], chunk[width:]))
    return groups


def _map_blocks(groups: list[tuple[str, str]], keyword: str, decrypt: bool) -> str:
    pair_fn = playfair_decrypt if decrypt else playfair_encrypt
    parts: list[str] = []
    for top, bottom in groups:
        new_top: list[str] = []
        new_bottom: list[str] = []
        for col in range(len(top)):
            mapped = pair_fn(top[col] + bottom[col], keyword)
            if len(mapped) != 2:
                raise ValueError("Playfair pair did not stay a digraph")
            new_top.append(mapped[0])
            new_bottom.append(mapped[1])
        parts.append("".join(new_top) + "".join(new_bottom))
    return "".join(parts)


def seriated_playfair_encrypt(text: str, keyword: str, period: int, null: str = "X") -> str:
    """Encrypt with a known keyword square and period.

    The keyword builds the 5x5 Playfair square (J omitted). The period is
    the width of each 2-line group and is not the keyword length.
    """
    cleaned = _keyword(keyword)
    width = _period(period)
    prepared = prepare_seriated_playfair(text, width, null=null)
    return _map_blocks(_blocks(prepared, width), cleaned, decrypt=False)


def seriated_playfair_decrypt(text: str, keyword: str, period: int) -> str:
    """Decrypt with a known keyword square and period.

    Ciphertext must already fill complete 2-line groups. Nulls that were
    inserted before encryption stay in the letter stream. No pad is added.
    """
    cleaned = _keyword(keyword)
    width = _period(period)
    letters = two_square_letters(text)
    if not letters:
        raise ValueError("text has no letters")
    if len(letters) % (2 * width) != 0:
        raise ValueError("Seriated Playfair ciphertext must fill 2-line period groups")
    return _map_blocks(_blocks(letters, width), cleaned, decrypt=True)


def solve_seriated_playfair(text: str, *, keyword: str, period: int) -> SolveResult:
    """Recover seriated Playfair plaintext when the keyword and period are known.

    Known-cipher decrypt only. Not an unknown-script reading and not a
    claim about Kryptos K4, Zodiac, Beale, McCormick, Voynich, or army
    message Nr. 86.
    """
    cleaned = _keyword(keyword)
    width = _period(period)
    plain_letters = seriated_playfair_decrypt(text, cleaned, width)
    square = playfair_square(cleaned)
    az = [ord(ch) - 65 for ch in plain_letters]
    return SolveResult(
        method="seriated_playfair",
        plaintext=plain_letters,
        key=cleaned,
        score=get_model().score(az) if az else 0.0,
        details={
            "keyword": cleaned,
            "period": width,
            "square": square,
            "letters": len(two_square_letters(text)),
            "mode": "known_keyword",
            "scope": _SCOPE,
            "source_url": ACA_URL,
        },
    )


__all__ = [
    "ACA_CIPHER",
    "ACA_KEYWORD",
    "ACA_PDF_SHA256",
    "ACA_PERIOD",
    "ACA_PLAIN",
    "ACA_PRINTED_CIPHER",
    "ACA_SENTENCE",
    "ACA_SQUARE",
    "ACA_URL",
    "prepare_seriated_playfair",
    "seriated_playfair_decrypt",
    "seriated_playfair_encrypt",
    "solve_seriated_playfair",
]
