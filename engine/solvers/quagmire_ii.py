"""Quagmire II known-key solver for the ACA published worked example.

The American Cryptogram Association defines Quagmire II as its K2 plan:
the plaintext alphabet is straight A-Z and the ciphertext alphabet is
keyed. The indicator sets the period. Each ciphertext row rotates so
the current indicator letter sits below the chosen plaintext letter.

Source: https://www.cryptogram.org/downloads/aca.info/ciphers/QuagmireII.pdf

The sheet gives ciphertext keyword SPRINGFEV(ER), indicator FLOWER under
plaintext A, and both the plaintext and ciphertext of a 66-letter example.
The parenthesized E and R mark repeated keyword letters.

This is a known classical-cipher helper with supplied keys. It does not
recover unknown keys, read an unknown script, or claim a solution for
Kryptos K4, Zodiac, Beale, McCormick, Voynich, or army message Nr. 86.
The alphabet transformation uses the existing Quagmire IV implementation
with its plaintext alphabet fixed to straight A-Z.
"""

from __future__ import annotations

from engine.alphabet import ALPHABET
from engine.result import SolveResult
from engine.solvers.quagmire_iv import (
    quagmire_iv_alphabet,
    quagmire_iv_decrypt,
    quagmire_iv_encrypt,
)


ACA_URL = "https://www.cryptogram.org/downloads/aca.info/ciphers/QuagmireII.pdf"
# Fetched and visually checked 2026-10-03.
ACA_PDF_SHA256 = "9a732261fe24ef967df09f8eda892e10c7f340383f542958cf33189f53e51fbc"
ACA_CIPHERTEXT_KEYWORD = "SPRINGFEVER"
ACA_INDICATOR = "FLOWER"
ACA_INDICATOR_UNDER = "A"
ACA_PLAINTEXT_ALPHABET = ALPHABET
ACA_CIPHERTEXT_ALPHABET = "SPRINGFEVABCDHJKLMOQTUWXYZ"
ACA_MESSAGE = "In the Quag Two a straight plain alphabet is run against a keyed cipher alphabet."
ACA_PLAIN = "INTHEQUAGTWOASTRAIGHTPLAINALPHABETISRUNAGAINSTAKEYEDCIPHERALPHABET"
ACA_PRINTED_CIPHER = (
    "JICIC OSLYK ILFVC HEBDX CCORJ IOEWA FMWKK TXBGW HRJIB KEDBJ WZABU "
    "XWHEH UXOXC U."
)
ACA_CIPHER = "JICICOSLYKILFVCHEBDXCCORJIOEWAFMWKKTXBGWHRJIBKEDBJWZABUXWHEHUXOXCU"
ACA_KEY = "ct=SPRINGFEVER indicator=FLOWER under=A"

_SCOPE = (
    "Known classical Quagmire II cipher with supplied keys; "
    "not an unknown-script reading or a claim about Kryptos K4, "
    "Zodiac, Beale, McCormick, Voynich, or army message Nr. 86."
)


def _letters(value: str, name: str) -> str:
    """Normalize A-Z letters, ignore punctuation, and reject other alphabets."""
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    for letter in value:
        if letter.isalpha() and not ("A" <= letter <= "Z" or "a" <= letter <= "z"):
            raise ValueError(f"{name} must use only A-Z letters")
    cleaned = "".join(letter.upper() for letter in value if letter.isalpha())
    if not cleaned:
        raise ValueError(f"{name} must contain at least one A-Z letter")
    return cleaned


def quagmire_ii_alphabet(keyword: str) -> str:
    """Ciphertext alphabet: unique keyword letters, then unused A-Z letters."""
    return quagmire_iv_alphabet(_letters(keyword, "Quagmire II ciphertext keyword"))


def _settings(
    ciphertext_keyword: str, indicator: str, indicator_under: str
) -> tuple[str, str, str]:
    keyword = _letters(ciphertext_keyword, "Quagmire II ciphertext keyword")
    indicator_letters = _letters(indicator, "Quagmire II indicator")
    under = _letters(indicator_under, "Quagmire II indicator column")
    if len(under) != 1:
        raise ValueError("Quagmire II indicator column must be one A-Z letter")
    return keyword, indicator_letters, under


def quagmire_ii_encrypt(
    text: str,
    *,
    ciphertext_keyword: str,
    indicator: str,
    indicator_under: str,
) -> str:
    """Encrypt an A-Z stream with known Quagmire II keys.

    Non-letter separators are dropped. Indicator repeats are kept, and no
    padding is added to the final short period group.
    """
    keyword, indicator_letters, under = _settings(ciphertext_keyword, indicator, indicator_under)
    letters = _letters(text, "text")
    return quagmire_iv_encrypt(
        letters,
        plaintext_keyword=ALPHABET,
        ciphertext_keyword=keyword,
        indicator=indicator_letters,
        indicator_under=under,
    )


def quagmire_ii_decrypt(
    text: str,
    *,
    ciphertext_keyword: str,
    indicator: str,
    indicator_under: str,
) -> str:
    """Decrypt an A-Z stream with known Quagmire II keys, without padding."""
    keyword, indicator_letters, under = _settings(ciphertext_keyword, indicator, indicator_under)
    letters = _letters(text, "text")
    return quagmire_iv_decrypt(
        letters,
        plaintext_keyword=ALPHABET,
        ciphertext_keyword=keyword,
        indicator=indicator_letters,
        indicator_under=under,
    )


def quagmire_ii_key(ciphertext_keyword: str, indicator: str, indicator_under: str) -> str:
    """Stable label retaining keyword and indicator repeats."""
    keyword, indicator_letters, under = _settings(ciphertext_keyword, indicator, indicator_under)
    return f"ct={keyword} indicator={indicator_letters} under={under}"


def solve_quagmire_ii(
    text: str,
    *,
    ciphertext_keyword: str,
    indicator: str,
    indicator_under: str,
) -> SolveResult:
    """Return known-key Quagmire II plaintext and metadata.

    This wrapper does not search for a keyword or identify a cipher type.
    Its score is the number of recovered letters, matching Quagmire IV.
    """
    keyword, indicator_letters, under = _settings(ciphertext_keyword, indicator, indicator_under)
    plaintext = quagmire_ii_decrypt(
        text,
        ciphertext_keyword=keyword,
        indicator=indicator_letters,
        indicator_under=under,
    )
    key = quagmire_ii_key(keyword, indicator_letters, under)
    return SolveResult(
        method="quagmire-ii",
        plaintext=plaintext,
        key=key,
        score=float(len(plaintext)),
        details={
            "key": key,
            "ciphertext_keyword": keyword,
            "indicator": indicator_letters,
            "indicator_under": under,
            "period": len(indicator_letters),
            "plaintext_alphabet": ALPHABET,
            "ciphertext_alphabet": quagmire_ii_alphabet(keyword),
            "letters": len(plaintext),
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
    "ACA_PDF_SHA256",
    "ACA_PLAIN",
    "ACA_PLAINTEXT_ALPHABET",
    "ACA_PRINTED_CIPHER",
    "ACA_URL",
    "quagmire_ii_alphabet",
    "quagmire_ii_decrypt",
    "quagmire_ii_encrypt",
    "quagmire_ii_key",
    "solve_quagmire_ii",
]
