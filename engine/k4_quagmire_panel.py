"""Quagmire I-IV panel on K4 using only the published Kryptos keywords.

Indicators are those keywords or a single A-Z letter. The indicator column
is every A-Z letter. This is the setting space the earlier keyword panel
did not enter. A crib hit is unverified. solved stays false.
"""

from __future__ import annotations

from engine.solvers.k4_attempt import K4_CIPHERTEXT, cribs_in_place
from engine.solvers.quagmire_i import quagmire_i_decrypt
from engine.solvers.quagmire_ii import quagmire_ii_decrypt
from engine.solvers.quagmire_iii import quagmire_iii_decrypt
from engine.solvers.quagmire_iv import quagmire_iv_decrypt

KEYWORDS = ("KRYPTOS", "PALIMPSEST", "ABSCISSA")
LETTERS = tuple(chr(65 + index) for index in range(26))
INDICATORS = KEYWORDS + LETTERS
_CAP = 20


def _tally() -> dict:
    return {"tried": 0, "rejected": 0, "crib_hits": 0}


def _check(decrypt, tally, unverified, **kwargs) -> None:
    try:
        plain = decrypt(K4_CIPHERTEXT, **kwargs)
    except (ValueError, IndexError):
        tally["rejected"] += 1
        return
    tally["tried"] += 1
    if len(plain) == 97 and cribs_in_place(plain):
        tally["crib_hits"] += 1
        if len(unverified) < _CAP:
            unverified.append({"status": "unverified", "plaintext": plain, "settings": kwargs})


def search_k4_quagmire_panel() -> dict:
    """Sweep the declared Quagmire settings. No plaintext is claimed."""
    if len(K4_CIPHERTEXT) != 97:
        raise ValueError("K4 ciphertext must be 97 letters")
    tallies = {name: _tally() for name in ("I", "II", "III", "IV")}
    unverified: list[dict] = []
    for keyword in KEYWORDS:
        for indicator in INDICATORS:
            for under in LETTERS:
                _check(
                    quagmire_i_decrypt, tallies["I"], unverified,
                    plaintext_keyword=keyword, indicator=indicator, indicator_under=under,
                )
                _check(
                    quagmire_ii_decrypt, tallies["II"], unverified,
                    ciphertext_keyword=keyword, indicator=indicator, indicator_under=under,
                )
                _check(
                    quagmire_iii_decrypt, tallies["III"], unverified,
                    keyword=keyword, indicator=indicator, indicator_under=under,
                )
    for left in KEYWORDS:
        for right in KEYWORDS:
            if left == right:
                continue
            for indicator in INDICATORS:
                for under in LETTERS:
                    _check(
                        quagmire_iv_decrypt, tallies["IV"], unverified,
                        plaintext_keyword=left, ciphertext_keyword=right,
                        indicator=indicator, indicator_under=under,
                    )
    expected = {
        "I": len(KEYWORDS) * len(INDICATORS) * len(LETTERS),
        "II": len(KEYWORDS) * len(INDICATORS) * len(LETTERS),
        "III": len(KEYWORDS) * len(INDICATORS) * len(LETTERS),
        "IV": (len(KEYWORDS) * (len(KEYWORDS) - 1)) * len(INDICATORS) * len(LETTERS),
    }
    return {
        "claimed_plaintext": None,
        "solved": False,
        "keywords": KEYWORDS,
        "indicators": len(INDICATORS),
        "tallies": tallies,
        "expected": expected,
        "crib_hits": sum(row["crib_hits"] for row in tallies.values()),
        "unverified": unverified,
    }
