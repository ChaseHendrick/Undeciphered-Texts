"""Digrafid (ACA) known-key solver: two 27-symbol alphabets and a period.

Digrafid, published by ACA member KNUTE, writes one mixed alphabet in a 3x9
grid and a second in a 9x3 grid (filled down the columns). Each plaintext
digraph becomes a 3-digit coordinate. Digraphs are grouped by the period,
those digits are read across in threes, and each new triple is turned back
into a ciphertext digraph. The American Cryptogram Association cipher sheet
prints a full worked example:

  https://www.cryptogram.org/downloads/aca.info/ciphers/Digrafid.pdf

This module recovers plaintext only when both alphabets and the period are
supplied. It is a known classical-cipher decrypt helper for published
fixtures. It does not read ancient scripts, unknown languages, or claim
any historical break of an unsolved ciphertext.
"""

from __future__ import annotations

from engine.result import SolveResult

# 26 letters plus the ACA null symbol. J stays a separate letter.
DIGRAFID_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGRAFID_EXTRA = "#"
DIGRAFID_ALPHABET = DIGRAFID_LETTERS + DIGRAFID_EXTRA

# ACA cipher sheet (page 43), tableau and fractionation-3 example.
# URL: https://www.cryptogram.org/downloads/aca.info/ciphers/Digrafid.pdf
# Horizontal keyword KEYWORD, then unused letters, then #.
# Vertical keyword VERTICAL, written down the columns of the 9x3 grid.
ACA_HORIZONTAL = "KEYWORDABCFGHIJLMNPQSTUVXZ#"
ACA_VERTICAL = "VERTICALBDFGHJKMNOPQSUWXYZ#"
ACA_PERIOD = 3
# Source prints "This is the forest pri". Spaces are not part of the
# letter stream that is enciphered, and they are not in this plaintext.
ACA_PLAIN = "THISISTHEFORESTPRI"
ACA_CIPHER = "HJMXWSWJADWGFCSPYI"
# Same sheet, fractionation 4 (4 digraphs per group).
ACA_PERIOD_4 = 4
ACA_CIPHER_PERIOD_4 = "HJTKVHYUFFWDSQYPRI"
ACA_URL = "https://www.cryptogram.org/downloads/aca.info/ciphers/Digrafid.pdf"


def digrafid_symbols(text: str) -> str:
    """A-Z and # stream: other characters dropped, letters uppercased."""
    out: list[str] = []
    for ch in text:
        if ch == DIGRAFID_EXTRA:
            out.append(ch)
            continue
        if ch.isalpha():
            out.append(ch.upper())
    return "".join(out)


def alphabet_from_keyword(keyword: str) -> str:
    """27-symbol Digrafid alphabet: keyword, then unused A-Z, then #.

    Repeated letters are skipped. A # already present in the keyword keeps
    its place and is not appended again. This is the construction printed
    by the ACA sheet (KEYWORD / VERTICAL) and by CryptoCrack.
    """
    seen: list[str] = []
    for ch in keyword:
        if ch == DIGRAFID_EXTRA:
            symbol = ch
        elif ch.isalpha():
            symbol = ch.upper()
        else:
            continue
        if symbol not in seen:
            seen.append(symbol)
    for ch in DIGRAFID_LETTERS:
        if ch not in seen:
            seen.append(ch)
    if DIGRAFID_EXTRA not in seen:
        seen.append(DIGRAFID_EXTRA)
    alphabet = "".join(seen)
    return normalize_alphabet(alphabet)


def normalize_alphabet(alphabet: str) -> str:
    """Return a 27-symbol alphabet (A-Z and exactly one #) or raise ValueError."""
    cells = digrafid_symbols(alphabet)
    if len(cells) != 27 or len(set(cells)) != 27:
        raise ValueError("digrafid alphabet must be 27 distinct symbols (A-Z and #)")
    missing = [ch for ch in DIGRAFID_ALPHABET if ch not in cells]
    if missing:
        raise ValueError("digrafid alphabet missing symbols: " + "".join(missing))
    return cells


def _layouts(horizontal: str, vertical: str) -> tuple[str, str, dict[str, tuple[int, int]], dict[str, tuple[int, int]]]:
    horiz = normalize_alphabet(horizontal)
    vert = normalize_alphabet(vertical)
    # Horizontal 3x9 is row-major. Vertical 9x3 is filled down the columns.
    hpos = {ch: divmod(i, 9) for i, ch in enumerate(horiz)}
    vpos: dict[str, tuple[int, int]] = {}
    for i, ch in enumerate(vert):
        col, row = divmod(i, 9)
        vpos[ch] = (row, col)
    return horiz, vert, hpos, vpos


def _digraph_from_triple(
    triple: tuple[int, int, int],
    horizontal: str,
    vertical: str,
) -> str:
    first_digit, middle, third_digit = triple
    if not (1 <= first_digit <= 9 and 1 <= middle <= 9 and 1 <= third_digit <= 9):
        raise ValueError("digrafid coordinates must be digits 1-9")
    mid = middle - 1
    hrow = mid // 3
    vcol = mid % 3
    hcol = first_digit - 1
    vrow = third_digit - 1
    first = horizontal[hrow * 9 + hcol]
    second = vertical[vcol * 9 + vrow]
    return first + second


def _triple_from_digraph(
    pair: str,
    hpos: dict[str, tuple[int, int]],
    vpos: dict[str, tuple[int, int]],
) -> tuple[int, int, int]:
    a, b = pair
    if a not in hpos or b not in vpos:
        raise ValueError("digrafid symbol missing from an alphabet: " + pair)
    hrow, hcol = hpos[a]
    vrow, vcol = vpos[b]
    middle = hrow * 3 + vcol + 1
    return (hcol + 1, middle, vrow + 1)


def _require_period(period: int) -> int:
    if not isinstance(period, int) or isinstance(period, bool) or period < 1:
        raise ValueError("period must be an integer of at least 1 (digraphs per group)")
    return period


def _pairs(stream: str) -> list[str]:
    if len(stream) % 2 != 0:
        raise ValueError(
            "digrafid text must have an even number of symbols "
            "(the ACA sheet adds a null such as X when the plaintext is odd)"
        )
    return [stream[i : i + 2] for i in range(0, len(stream), 2)]


def digrafid_encrypt(text: str, horizontal: str, vertical: str, period: int) -> str:
    """Encrypt with two known alphabets and a period (digraphs per group)."""
    period = _require_period(period)
    horiz, vert, hpos, vpos = _layouts(horizontal, vertical)
    stream = digrafid_symbols(text)
    if not stream:
        raise ValueError("plaintext has no Digrafid symbols")
    pairs = _pairs(stream)
    out: list[str] = []
    for start in range(0, len(pairs), period):
        block = pairs[start : start + period]
        rows: list[list[int]] = [[], [], []]
        for pair in block:
            d1, d2, d3 = _triple_from_digraph(pair, hpos, vpos)
            rows[0].append(d1)
            rows[1].append(d2)
            rows[2].append(d3)
        flat = rows[0] + rows[1] + rows[2]
        for i in range(0, len(flat), 3):
            out.append(_digraph_from_triple((flat[i], flat[i + 1], flat[i + 2]), horiz, vert))
    return "".join(out)


def digrafid_decrypt(text: str, horizontal: str, vertical: str, period: int) -> str:
    """Decrypt with two known alphabets and a period (digraphs per group)."""
    period = _require_period(period)
    horiz, vert, hpos, vpos = _layouts(horizontal, vertical)
    stream = digrafid_symbols(text)
    if not stream:
        raise ValueError("ciphertext has no Digrafid symbols")
    pairs = _pairs(stream)
    out: list[str] = []
    for start in range(0, len(pairs), period):
        block = pairs[start : start + period]
        triples = [_triple_from_digraph(pair, hpos, vpos) for pair in block]
        flat = [digit for triple in triples for digit in triple]
        n = len(block)
        rows = (flat[:n], flat[n : 2 * n], flat[2 * n :])
        for i in range(n):
            out.append(_digraph_from_triple((rows[0][i], rows[1][i], rows[2][i]), horiz, vert))
    return "".join(out)


def solve_digrafid(
    text: str,
    *,
    horizontal: str,
    vertical: str,
    period: int,
) -> SolveResult:
    """Recover Digrafid plaintext when both alphabets and the period are known.

    This is a known-cipher decrypt, not a blind cryptanalysis search and not
    an ancient-script reading. Period is the number of digraphs per group,
    which the ACA sheet also calls the fractionation.
    """
    period = _require_period(period)
    horiz, vert, _, _ = _layouts(horizontal, vertical)
    stream = digrafid_symbols(text)
    plain = digrafid_decrypt(stream, horiz, vert, period)
    return SolveResult(
        method="digrafid",
        plaintext=plain,
        key=f"{horiz}/{vert}/{period}",
        score=float(len(plain)),
        details={
            "horizontal": horiz,
            "vertical": vert,
            "period": period,
            "letters": len(stream),
            "mode": "known_alphabets_and_period",
            "scope": (
                "Known classical Digrafid decrypt only; "
                "not an ancient-script or unknown-language reading."
            ),
            "source_url": ACA_URL,
        },
    )


__all__ = [
    "ACA_CIPHER",
    "ACA_CIPHER_PERIOD_4",
    "ACA_HORIZONTAL",
    "ACA_PERIOD",
    "ACA_PERIOD_4",
    "ACA_PLAIN",
    "ACA_URL",
    "ACA_VERTICAL",
    "DIGRAFID_ALPHABET",
    "alphabet_from_keyword",
    "digrafid_decrypt",
    "digrafid_encrypt",
    "digrafid_symbols",
    "normalize_alphabet",
    "solve_digrafid",
]
