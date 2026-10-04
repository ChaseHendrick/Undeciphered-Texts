"""Bounded K4 running-key check against plaintext constants already in the repo.

A running key is not repeated and is not wrapped. Short repeating keys are a
different search and are not repeated here. This module does not claim a K4
plaintext. `solved` stays false and `claimed_plaintext` stays None.
"""

from __future__ import annotations

from engine.alphabet import letters_only
from engine.solvers.columnar import KRYPTOS_K3_PLAINTEXT
from engine.solvers.k4_attempt import (
    K4_CIPHERTEXT,
    cribs_in_place,
    english_pass,
)
from engine.solvers.running_key import running_key_decrypt

# K4 length minus one. Offset count is max(0, key_letters - (97 - 1)).
_WINDOW = 97
_OFFSET_BASE = _WINDOW - 1
_UNVERIFIED_CAP = 20

_K1_MODULE = "tests.test_keyed_vigenere"


def _published_k1_plaintext() -> str:
    """The K1 string defined in the keyed Vigenere tests. Not retyped here."""
    from tests.test_keyed_vigenere import PUBLISHED_K1_PLAINTEXT

    if not isinstance(PUBLISHED_K1_PLAINTEXT, str):
        raise TypeError("PUBLISHED_K1_PLAINTEXT must be a string")
    return PUBLISHED_K1_PLAINTEXT


def _key_sources() -> tuple[tuple[str, str, str], ...]:
    """Name, source label, and the constant text. K2 is not typed in."""
    return (
        (
            "KRYPTOS_K3_PLAINTEXT",
            "engine.solvers.columnar.KRYPTOS_K3_PLAINTEXT",
            KRYPTOS_K3_PLAINTEXT,
        ),
        (
            "PUBLISHED_K1_PLAINTEXT",
            f"{_K1_MODULE}.PUBLISHED_K1_PLAINTEXT",
            _published_k1_plaintext(),
        ),
    )


def search_k4_running_key() -> dict:
    """Try each in-repo key at every start that still has 97 unused letters.

    A text shorter than 97 letters is skipped and the reason is recorded.
    A crib match is stored as unverified, at most 20 strings, and is not a solve.
    """
    if len(K4_CIPHERTEXT) != _WINDOW:
        raise ValueError("K4 ciphertext must be 97 letters")

    tallies: list[dict] = []
    skipped: list[dict] = []
    unverified: list[dict] = []
    tried_total = 0
    crib_total = 0
    english_total = 0

    for name, source, raw in _key_sources():
        key = letters_only(raw)
        offsets = max(0, len(key) - _OFFSET_BASE)
        if len(key) < _WINDOW:
            skipped.append(
                {
                    "key": name,
                    "source": source,
                    "letters": len(key),
                    "offsets": 0,
                    "reason": (
                        f"{len(key)} letters is shorter than {_WINDOW}. "
                        "A running key is not repeated, so this text was not used."
                    ),
                }
            )
            continue

        tried = 0
        crib_ok = 0
        english_ok = 0
        for offset in range(offsets):
            segment = key[offset : offset + _WINDOW]
            if len(segment) != _WINDOW:
                raise RuntimeError("running-key window slipped")
            plain = running_key_decrypt(K4_CIPHERTEXT, segment)
            tried += 1
            if not cribs_in_place(plain):
                continue
            crib_ok += 1
            # english_pass reloads its model on every call. Only crib matches
            # are scored, which is the same order as the earlier K4 attempt.
            passed = english_pass(plain)
            if passed:
                english_ok += 1
            if len(unverified) < _UNVERIFIED_CAP:
                unverified.append(
                    {
                        "status": "unverified",
                        "key": name,
                        "source": source,
                        "offset": offset,
                        "plaintext": plain,
                        "english_pass": passed,
                    }
                )
        tried_total += tried
        crib_total += crib_ok
        english_total += english_ok
        tallies.append(
            {
                "key": name,
                "source": source,
                "letters": len(key),
                "offsets": offsets,
                "tried": tried,
                "crib_consistent": crib_ok,
                "english_pass": english_ok,
                "bound": (
                    "start offsets that leave 97 unused key letters; "
                    "no wrapping; running_key_decrypt"
                ),
            }
        )

    return {
        "claimed_plaintext": None,
        "solved": False,
        "tallies": tallies,
        "skipped": skipped,
        "unverified": unverified,
        "unverified_cap": _UNVERIFIED_CAP,
        "totals": {
            "tried": tried_total,
            "crib_consistent": crib_total,
            "english_pass": english_total,
        },
    }


__all__ = ["search_k4_running_key"]
