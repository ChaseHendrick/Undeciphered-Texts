"""Quagmire I encrypt/decrypt with a known plaintext keyword and indicator.

The ACA sheet uses a keyword-mixed plaintext alphabet and a straight A-Z
ciphertext alphabet. Each indicator letter rotates the ciphertext alphabet
to sit under the chosen plaintext letter. This is the Quagmire IV table
construction with a straight ciphertext alphabet, so the transformation is
shared with that existing implementation.

Source: https://www.cryptogram.org/downloads/aca.info/ciphers/QuagmireI.pdf
Known classical-cipher check only. No unknown-script or Kryptos K4 claim.
"""

from __future__ import annotations

from engine.alphabet import ALPHABET
from engine.result import SolveResult
from engine.solvers.quagmire_iv import quagmire_iv_encrypt, solve_quagmire_iv

ACA_URL = "https://www.cryptogram.org/downloads/aca.info/ciphers/QuagmireI.pdf"
ACA_MESSAGE = (
    "The Quag One is a periodic cipher with a keyed plain alphabet "
    "run against a straight cipher alphabet."
)
ACA_PLAIN = (
    "THEQUAGONEISAPERIODICCIPHERWITHAKEYEDPLAINALPHABETRUNAGAINST"
    "ASTRAIGHTCIPHERALPHABET"
)
ACA_PRINTED_CIPHER = (
    "QPMGQ RBUJU YIFDM PYAIF QYYJJ JHJYC JLUUT PIDVW YMFSG AESDW HIZRB "
    "LIRVC FCZPE LBPZY YJJJH WLJJL PUP."
)
ACA_CIPHER = ACA_PRINTED_CIPHER.replace(" ", "").rstrip(".")
ACA_PLAINTEXT_KEYWORD = "SPRINGFEVER"
ACA_PLAINTEXT_ALPHABET = "SPRINGFEVABCDHJKLMOQTUWXYZ"
ACA_INDICATOR = "FLOWER"
ACA_INDICATOR_UNDER = "A"
ACA_KEY = "pt=SPRINGFEVER indicator=FLOWER under=A"


def _letters(text: str, field: str) -> str:
    """Normalize A-Z, drop non-letters, and reject letters outside that alphabet."""
    if any(ch.isalpha() and ch not in ALPHABET + ALPHABET.lower() for ch in text):
        raise ValueError(f"Quagmire I {field} accepts only A-Z letters")
    cleaned = "".join(ch.upper() for ch in text if ch in ALPHABET + ALPHABET.lower())
    if not cleaned:
        raise ValueError(f"Quagmire I {field} must contain at least one letter")
    return cleaned


def _parameters(plaintext_keyword: str, indicator: str, indicator_under: str) -> dict[str, str]:
    keyword = _letters(plaintext_keyword, "plaintext keyword")
    indicator_letters = _letters(indicator, "indicator")
    under = _letters(indicator_under, "indicator column")
    if len(under) != 1:
        raise ValueError("Quagmire I indicator column must be one letter")
    return dict(plaintext_keyword=keyword, ciphertext_keyword=ALPHABET,
                indicator=indicator_letters, indicator_under=under)


def quagmire_i_encrypt(
    text: str, *, plaintext_keyword: str, indicator: str, indicator_under: str,
) -> str:
    """Encrypt a letter stream with known keys. Spaces and punctuation are dropped."""
    keys = _parameters(plaintext_keyword, indicator, indicator_under)
    return quagmire_iv_encrypt(_letters(text, "text"), **keys)


def quagmire_i_decrypt(
    text: str, *, plaintext_keyword: str, indicator: str, indicator_under: str,
) -> str:
    """Decrypt with known keys. A final incomplete period needs no padding."""
    return solve_quagmire_i(
        text, plaintext_keyword=plaintext_keyword,
        indicator=indicator, indicator_under=indicator_under,
    ).plaintext


def solve_quagmire_i(
    text: str, *, plaintext_keyword: str, indicator: str, indicator_under: str,
) -> SolveResult:
    """Return a known-key result; this function does not search for unknown keys."""
    keys = _parameters(plaintext_keyword, indicator, indicator_under)
    result = solve_quagmire_iv(_letters(text, "text"), **keys)
    key = (f"pt={keys['plaintext_keyword']} indicator={keys['indicator']} "
           f"under={keys['indicator_under']}")
    details = dict(result.details)
    details.pop("ciphertext_keyword")
    details.update(
        key=key, source_url=ACA_URL,
        scope=("Known classical Quagmire I cipher with supplied keys. "
               "Not an unknown-script reading or a solution of Kryptos K4, "
               "Zodiac, Beale, McCormick, Voynich, or army message Nr. 86."),
    )
    return SolveResult(method="quagmire-i", plaintext=result.plaintext, key=key,
                       score=result.score, details=details)


__all__ = [
    "ACA_URL", "ACA_MESSAGE", "ACA_PLAIN", "ACA_PRINTED_CIPHER", "ACA_CIPHER",
    "ACA_PLAINTEXT_KEYWORD", "ACA_PLAINTEXT_ALPHABET", "ACA_INDICATOR",
    "ACA_INDICATOR_UNDER", "ACA_KEY", "quagmire_i_encrypt", "quagmire_i_decrypt",
    "solve_quagmire_i",
]
