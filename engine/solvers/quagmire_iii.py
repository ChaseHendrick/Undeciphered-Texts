"""Quagmire III known-key helper for the ACA published example.

The same keyed alphabet is used for plaintext and ciphertext. A repeating
indicator rotates each ciphertext row under a chosen plaintext letter.
The mapping uses the existing Quagmire IV core with both alphabets keyed
by the same keyword. This module does not search for an unknown key.

Source, inspected 2026-10-03:
https://www.cryptogram.org/downloads/aca.info/ciphers/QuagmireIII.pdf

This is known classical-cipher recovery. It does not read an unknown
script or claim a solve of Kryptos K4, Zodiac, Beale, McCormick, Voynich,
or army message Nr. 86.
"""

from __future__ import annotations

from engine.alphabet import ALPHABET, letters_only
from engine.result import SolveResult
from engine.solvers.quagmire_iv import (
    quagmire_iv_alphabet,
    quagmire_iv_decrypt,
    quagmire_iv_encrypt,
    quagmire_iv_row,
)


ACA_URL = "https://www.cryptogram.org/downloads/aca.info/ciphers/QuagmireIII.pdf"
# SHA-256 of the PDF downloaded and visually inspected on 2026-10-03.
ACA_PDF_SHA256 = "d8ef8e5f4fd9f9727dcf91a43e2ff279d92622daaf8ce44dd7b17493b154260e"
ACA_KEYWORD = "AUTOMOBILE"
ACA_INDICATOR = "HIGHWAY"
ACA_INDICATOR_UNDER = "A"
ACA_ALPHABET = "AUTOMBILECDFGHJKNPQRSVWXYZ"
ACA_MESSAGE = "The same keyed alphabet is used for plain and cipher alphabets."
ACA_PLAIN = "THESAMEKEYEDALPHABETISUSEDFORPLAINANDCIPHERALPHABETS"
ACA_PRINTED_CIPHER = "KRSLW MITJD VIABM RGQMT MLLIV IFUIX RHTNY ONVRH HIIIR MCAOV EI"
ACA_CIPHER = "KRSLWMITJDVIABMRGQMTMLLIVIFUIXRHTNYONVRHHIIIRMCAOVEI"
ACA_KEY = "keyword=AUTOMOBILE indicator=HIGHWAY under=A"

_ASCII_LETTERS = frozenset(ALPHABET + ALPHABET.lower())
_SCOPE = (
    "Known classical Quagmire III cipher helper with a supplied key; "
    "not an unknown-script reading and not a claim about Kryptos K4, "
    "Zodiac, Beale, McCormick, Voynich, or army message Nr. 86."
)


def _letters(value: str, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"Quagmire III {name} must be a string")
    if any(ch.isalpha() and ch not in _ASCII_LETTERS for ch in value):
        raise ValueError(f"Quagmire III {name} must use only A-Z letters")
    cleaned = letters_only(value)
    if not cleaned:
        raise ValueError(f"Quagmire III {name} must contain at least one letter")
    return cleaned


def quagmire_iii_alphabet(keyword: str) -> str:
    """Build the shared keyed alphabet, dropping keyword repeats."""
    return quagmire_iv_alphabet(_letters(keyword, "keyword"))


def quagmire_iii_indicator(indicator: str) -> str:
    """Normalize the indicator, keeping repeats because they set the period."""
    return _letters(indicator, "indicator")


def quagmire_iii_under(letter: str) -> str:
    """Normalize the one plaintext letter used for the indicator column."""
    cleaned = _letters(letter, "indicator column")
    if len(cleaned) != 1:
        raise ValueError("Quagmire III indicator column must be one letter")
    return cleaned


def quagmire_iii_row(ciphertext_alphabet: str, indicator_letter: str, under_index: int) -> str:
    """Rotate the keyed alphabet so the indicator occupies under_index."""
    if not isinstance(ciphertext_alphabet, str):
        raise TypeError("ciphertext alphabet must be a string")
    if len(ciphertext_alphabet) != 26 or set(ciphertext_alphabet) != set(ALPHABET):
        raise ValueError("ciphertext alphabet must be a permutation of A-Z")
    if not isinstance(under_index, int) or isinstance(under_index, bool):
        raise TypeError("indicator column index must be an integer")
    return quagmire_iv_row(
        ciphertext_alphabet, quagmire_iii_under(indicator_letter), under_index
    )


def _setup(keyword: str, indicator: str, indicator_under: str) -> tuple[str, str, str, str]:
    cleaned_keyword = _letters(keyword, "keyword")
    indicator_letters = quagmire_iii_indicator(indicator)
    under = quagmire_iii_under(indicator_under)
    alphabet = quagmire_iii_alphabet(cleaned_keyword)
    return cleaned_keyword, indicator_letters, under, alphabet


def quagmire_iii_encrypt(
    text: str,
    *,
    keyword: str,
    indicator: str,
    indicator_under: str,
) -> str:
    """Encrypt A-Z letters with supplied keys; nonletters are dropped.

    Indicator position advances only for letters. A final short period
    remains short, with no padding.
    """
    cleaned_keyword, indicator_letters, under, _alphabet = _setup(
        keyword, indicator, indicator_under
    )
    return quagmire_iv_encrypt(
        _letters(text, "text"),
        plaintext_keyword=cleaned_keyword,
        ciphertext_keyword=cleaned_keyword,
        indicator=indicator_letters,
        indicator_under=under,
    )


def quagmire_iii_decrypt(
    text: str,
    *,
    keyword: str,
    indicator: str,
    indicator_under: str,
) -> str:
    """Decrypt A-Z letters with supplied keys; nonletters are dropped."""
    cleaned_keyword, indicator_letters, under, _alphabet = _setup(
        keyword, indicator, indicator_under
    )
    return quagmire_iv_decrypt(
        _letters(text, "text"),
        plaintext_keyword=cleaned_keyword,
        ciphertext_keyword=cleaned_keyword,
        indicator=indicator_letters,
        indicator_under=under,
    )


def quagmire_iii_key(keyword: str, indicator: str, indicator_under: str) -> str:
    """Return a stable key label with keyword repeats retained."""
    cleaned_keyword, indicator_letters, under, _alphabet = _setup(
        keyword, indicator, indicator_under
    )
    return f"keyword={cleaned_keyword} indicator={indicator_letters} under={under}"


def solve_quagmire_iii(
    text: str,
    *,
    keyword: str,
    indicator: str,
    indicator_under: str,
) -> SolveResult:
    """Recover classical Quagmire III plaintext with a supplied key."""
    cleaned_keyword, indicator_letters, under, alphabet = _setup(
        keyword, indicator, indicator_under
    )
    plain = quagmire_iii_decrypt(
        text, keyword=cleaned_keyword, indicator=indicator_letters, indicator_under=under
    )
    key = quagmire_iii_key(cleaned_keyword, indicator_letters, under)
    return SolveResult(
        method="quagmire-iii",
        plaintext=plain,
        key=key,
        score=float(len(plain)),
        details={
            "key": key,
            "keyword": cleaned_keyword,
            "indicator": indicator_letters,
            "indicator_under": under,
            "period": len(indicator_letters),
            "plaintext_alphabet": alphabet,
            "ciphertext_alphabet": alphabet,
            "letters": len(plain),
            "mode": "known_key",
            "scope": _SCOPE,
            "source_url": ACA_URL,
        },
    )


__all__ = [
    "ACA_ALPHABET",
    "ACA_CIPHER",
    "ACA_INDICATOR",
    "ACA_INDICATOR_UNDER",
    "ACA_KEY",
    "ACA_KEYWORD",
    "ACA_MESSAGE",
    "ACA_PDF_SHA256",
    "ACA_PLAIN",
    "ACA_PRINTED_CIPHER",
    "ACA_URL",
    "quagmire_iii_alphabet",
    "quagmire_iii_decrypt",
    "quagmire_iii_encrypt",
    "quagmire_iii_indicator",
    "quagmire_iii_key",
    "quagmire_iii_row",
    "quagmire_iii_under",
    "solve_quagmire_iii",
]
