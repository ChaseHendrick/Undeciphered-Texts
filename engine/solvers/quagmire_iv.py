"""Quagmire IV known-key solver.

The American Cryptogram Association sheet numbers the Quagmires the same
way as keyword plans. Quagmire 4 is the K4 plan: a keyed plaintext
alphabet and a different keyed ciphertext alphabet. Each keyword is
written once, dropping repeated letters, and the unused letters follow
in alphabetical order. An indicator keyword sets the period. It is
written vertically under one chosen letter of the plaintext alphabet.
Each indicator letter rotates the ciphertext alphabet so that letter
sits in that column. Plaintext is enciphered one letter at a time,
cycling through the indicator.

  https://www.cryptogram.org/downloads/aca.info/ciphers/QuagmireIV.pdf

On that sheet the plaintext keyword is SENSORY, the ciphertext keyword
is PERC(EP)TION (the parenthesized letters are the repeats that are
dropped), and the indicator EXTRA stands under plaintext S (period 5).
The printed plaintext is "This one employs three keywords". The printed
ciphertext is VBMRF CYISP MPBRR HEICX RREIG DX.

This module encrypts and decrypts only when the keywords are supplied.
It is a known classical-cipher helper for that published example. It does
not read an unknown script and it does not claim Kryptos K4, Zodiac,
Beale, McCormick, Voynich, or army message Nr. 86.
"""

from __future__ import annotations

from engine.alphabet import ALPHABET, letters_only
from engine.result import SolveResult

# ACA Quagmire IV sheet (fetched 2026-10-03).
# PDF SHA-256: 51bce54487ffe6aada67d9b6c84c87c1ae904c3c3a889b26be3464c9cd9214cf
ACA_URL = "https://www.cryptogram.org/downloads/aca.info/ciphers/QuagmireIV.pdf"
ACA_PLAINTEXT_KEYWORD = "SENSORY"
ACA_CIPHERTEXT_KEYWORD = "PERCEPTION"
ACA_INDICATOR = "EXTRA"
ACA_INDICATOR_UNDER = "S"
ACA_PLAINTEXT_ALPHABET = "SENORYABCDFGHIJKLMPQTUVWXZ"
ACA_CIPHERTEXT_ALPHABET = "PERCTIONABDFGHJKLMQSUVWXYZ"
ACA_MESSAGE = "This one employs three keywords"
ACA_PLAIN = "THISONEEMPLOYSTHREEKEYWORDS"
ACA_CIPHER = "VBMRFCYISPMPBRRHEICXRREIGDX"
ACA_PRINTED_CIPHER = "VBMRF CYISP MPBRR HEICX RREIG DX"
ACA_KEY = "pt=SENSORY ct=PERCEPTION indicator=EXTRA under=S"

_SCOPE = (
    "Known classical Quagmire IV cipher solver only; "
    "not an unknown-script reading and not a claim about Kryptos K4, "
    "Zodiac, Beale, McCormick, Voynich, or army message Nr. 86."
)


def quagmire_iv_alphabet(keyword: str) -> str:
    """K4 mixed alphabet: keyword letters in order, then the unused A-Z letters.

    Repeated keyword letters are dropped. Non-letters are ignored, so a
    sheet form such as PERC(EP)TION is the same keyword as PERCEPTION.
    """
    cleaned = letters_only(keyword)
    if not cleaned:
        raise ValueError("Quagmire IV keyword must contain at least one letter")
    seen: list[str] = []
    for ch in cleaned:
        if ch not in seen:
            seen.append(ch)
    for ch in ALPHABET:
        if ch not in seen:
            seen.append(ch)
    return "".join(seen)


def quagmire_iv_indicator(indicator: str) -> str:
    """Indicator letters in order. Repeats are kept; they set the period."""
    cleaned = letters_only(indicator)
    if not cleaned:
        raise ValueError("Quagmire IV indicator must contain at least one letter")
    return cleaned


def quagmire_iv_under(letter: str) -> str:
    """The one plaintext-alphabet letter the indicator is written under."""
    cleaned = letters_only(letter)
    if len(cleaned) != 1:
        raise ValueError("Quagmire IV indicator column must be one letter")
    return cleaned


def quagmire_iv_row(ciphertext_alphabet: str, indicator_letter: str, under_index: int) -> str:
    """Rotate the ciphertext alphabet so indicator_letter sits at under_index."""
    if len(ciphertext_alphabet) != 26 or len(set(ciphertext_alphabet)) != 26:
        raise ValueError("ciphertext alphabet must be a permutation of A-Z")
    if not 0 <= under_index < 26:
        raise ValueError("indicator column index must be in 0..25")
    letter = quagmire_iv_under(indicator_letter)
    start = ciphertext_alphabet.index(letter)
    shift = (start - under_index) % 26
    return ciphertext_alphabet[shift:] + ciphertext_alphabet[:shift]


def _setup(
    plaintext_keyword: str,
    ciphertext_keyword: str,
    indicator: str,
    indicator_under: str,
) -> tuple[str, str, str, int, list[str]]:
    plaintext_alphabet = quagmire_iv_alphabet(plaintext_keyword)
    ciphertext_alphabet = quagmire_iv_alphabet(ciphertext_keyword)
    indicator_letters = quagmire_iv_indicator(indicator)
    under = quagmire_iv_under(indicator_under)
    under_index = plaintext_alphabet.index(under)
    rows = [
        quagmire_iv_row(ciphertext_alphabet, letter, under_index)
        for letter in indicator_letters
    ]
    return plaintext_alphabet, ciphertext_alphabet, indicator_letters, under_index, rows


def quagmire_iv_encrypt(
    text: str,
    *,
    plaintext_keyword: str,
    ciphertext_keyword: str,
    indicator: str,
    indicator_under: str,
) -> str:
    """Encrypt with known Quagmire IV keywords.

    Non-letters are dropped. Each plaintext letter uses the next indicator
    letter, and the indicator repeats after its last letter.
    """
    plaintext_alphabet, _ciphertext_alphabet, indicator_letters, _under_index, rows = _setup(
        plaintext_keyword, ciphertext_keyword, indicator, indicator_under
    )
    letters = letters_only(text)
    if not letters:
        raise ValueError("text has no letters")
    index = {ch: i for i, ch in enumerate(plaintext_alphabet)}
    period = len(indicator_letters)
    return "".join(rows[n % period][index[ch]] for n, ch in enumerate(letters))


def quagmire_iv_decrypt(
    text: str,
    *,
    plaintext_keyword: str,
    ciphertext_keyword: str,
    indicator: str,
    indicator_under: str,
) -> str:
    """Decrypt with known Quagmire IV keywords.

    Non-letters are dropped. No pad is added. A final short period group
    is left short, matching the two-letter group on the ACA sheet.
    """
    plaintext_alphabet, _ciphertext_alphabet, indicator_letters, _under_index, rows = _setup(
        plaintext_keyword, ciphertext_keyword, indicator, indicator_under
    )
    letters = letters_only(text)
    if not letters:
        raise ValueError("text has no letters")
    period = len(indicator_letters)
    out: list[str] = []
    for n, ch in enumerate(letters):
        plain_index = rows[n % period].index(ch)
        out.append(plaintext_alphabet[plain_index])
    return "".join(out)


def quagmire_iv_key(
    plaintext_keyword: str,
    ciphertext_keyword: str,
    indicator: str,
    indicator_under: str,
) -> str:
    """Stable key label for the three keywords and the indicator column.

    Keyword repeats are kept in the label. The mixed alphabets still drop
    them. PERC(EP)TION and PERCEPTION therefore share one label.
    """
    quagmire_iv_alphabet(plaintext_keyword)
    quagmire_iv_alphabet(ciphertext_keyword)
    plain_kw = letters_only(plaintext_keyword)
    cipher_kw = letters_only(ciphertext_keyword)
    indicator_letters = quagmire_iv_indicator(indicator)
    under = quagmire_iv_under(indicator_under)
    return (
        f"pt={plain_kw} ct={cipher_kw} indicator={indicator_letters} under={under}"
    )


def solve_quagmire_iv(
    text: str,
    *,
    plaintext_keyword: str,
    ciphertext_keyword: str,
    indicator: str,
    indicator_under: str,
) -> SolveResult:
    """Recover Quagmire IV plaintext when the keywords are known.

    Known-cipher decrypt only. Not an unknown-script reading and not a
    claim about Kryptos K4, Zodiac, Beale, McCormick, Voynich, or army
    message Nr. 86.
    """
    plaintext_alphabet, ciphertext_alphabet, indicator_letters, under_index, _rows = _setup(
        plaintext_keyword, ciphertext_keyword, indicator, indicator_under
    )
    plain_letters = quagmire_iv_decrypt(
        text,
        plaintext_keyword=plaintext_keyword,
        ciphertext_keyword=ciphertext_keyword,
        indicator=indicator,
        indicator_under=indicator_under,
    )
    key = quagmire_iv_key(
        plaintext_keyword, ciphertext_keyword, indicator, indicator_under
    )
    return SolveResult(
        method="quagmire-iv",
        plaintext=plain_letters,
        key=key,
        score=float(len(plain_letters)),
        details={
            "key": key,
            "plaintext_keyword": letters_only(plaintext_keyword),
            "ciphertext_keyword": letters_only(ciphertext_keyword),
            "indicator": indicator_letters,
            "indicator_under": plaintext_alphabet[under_index],
            "period": len(indicator_letters),
            "plaintext_alphabet": plaintext_alphabet,
            "ciphertext_alphabet": ciphertext_alphabet,
            "letters": len(letters_only(text)),
            "mode": "known_key",
            "scope": _SCOPE,
            "source_url": ACA_URL,
        },
    )


__all__ = [
    "ACA_CIPHER",
    "ACA_CIPHERTEXT_ALPHABET",
    "ACA_CIPHERTEXT_KEYWORD",
    "ACA_INDICATOR",
    "ACA_INDICATOR_UNDER",
    "ACA_KEY",
    "ACA_MESSAGE",
    "ACA_PLAIN",
    "ACA_PLAINTEXT_ALPHABET",
    "ACA_PLAINTEXT_KEYWORD",
    "ACA_PRINTED_CIPHER",
    "ACA_URL",
    "quagmire_iv_alphabet",
    "quagmire_iv_decrypt",
    "quagmire_iv_encrypt",
    "quagmire_iv_indicator",
    "quagmire_iv_key",
    "quagmire_iv_row",
    "quagmire_iv_under",
    "solve_quagmire_iv",
]
