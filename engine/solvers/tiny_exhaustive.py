"""Exhaustive search of two tiny classical keyspaces.

Caesar is 26 shifts. Rail fence, as searched here, is a few rail counts:
2 through 6 inclusive (5 keys). Every candidate is decrypted with the
existing known-key function, then ranked by the English quadgram model.
The winner is the unique best score inside that finite list.

Transposition does not change letter counts, so a unigram score cannot
separate rail-fence keys. The quadgram model can, on the certificate text.

This is exhaustive search of a tiny space. It is not an unsolved-text break.
It does not search Enigma, the M-209, army message Nr. 86, or Kryptos K4.
"""

from __future__ import annotations

from engine.alphabet import letters_only, to_ints
from engine.ciphers import caesar_decrypt
from engine.language import get_model
from engine.result import SolveResult
from engine.solvers.rail_fence import rail_fence_decrypt

CAESAR_KEYSPACE_SIZE = 26
RAIL_FENCE_MIN_RAILS = 2
RAIL_FENCE_MAX_RAILS = 6
RAIL_FENCE_KEYSPACE_SIZE = RAIL_FENCE_MAX_RAILS - RAIL_FENCE_MIN_RAILS + 1

_SCOPE = (
    "Exhaustive search of a tiny classical keyspace only. "
    "Not an unsolved-text break. "
    "Does not search Enigma, the M-209, army message Nr. 86, or Kryptos K4."
)


def _english_score(text: str) -> float:
    letters = letters_only(text)
    if len(letters) < 4:
        raise ValueError("text is too short to rank English letter order")
    return get_model().score(to_ints(letters))


def _unique_best(rows: list[tuple[str, str, float]]) -> tuple[str, str, float]:
    if not rows:
        raise ValueError("keyspace is empty")
    ranked = sorted(rows, key=lambda row: row[2], reverse=True)
    if len(ranked) > 1 and ranked[0][2] == ranked[1][2]:
        raise ValueError("exhaustive search did not find a unique best key")
    return ranked[0]


def brute_caesar(text: str) -> SolveResult:
    """Try all 26 Caesar shifts. The shift is not an argument.

    Uses caesar_decrypt. Keyspace size is 26. Not an unsolved-text break.
    """
    if not letters_only(text):
        raise ValueError("ciphertext has no letters")
    rows: list[tuple[str, str, float]] = []
    for shift in range(CAESAR_KEYSPACE_SIZE):
        plain = caesar_decrypt(text, shift)
        rows.append((str(shift), plain, _english_score(plain)))
    key, plain, score = _unique_best(rows)
    return SolveResult(
        method="caesar_exhaustive",
        plaintext=plain,
        key=key,
        score=score,
        details={
            "shift": int(key),
            "keyspace_size": CAESAR_KEYSPACE_SIZE,
            "trials": len(rows),
            "search": "exhaustive",
            "scope": _SCOPE,
        },
    )


def brute_rail_fence(text: str) -> SolveResult:
    """Try rail counts 2 through 6. The rail count is not an argument.

    Uses rail_fence_decrypt. Keyspace size is 5. Not an unsolved-text break.
    """
    if not letters_only(text):
        raise ValueError("ciphertext has no letters")
    rows: list[tuple[str, str, float]] = []
    for rails in range(RAIL_FENCE_MIN_RAILS, RAIL_FENCE_MAX_RAILS + 1):
        plain = rail_fence_decrypt(text, rails)
        rows.append((str(rails), plain, _english_score(plain)))
    key, plain, score = _unique_best(rows)
    return SolveResult(
        method="rail_fence_exhaustive",
        plaintext=plain,
        key=key,
        score=score,
        details={
            "rails": int(key),
            "keyspace_size": RAIL_FENCE_KEYSPACE_SIZE,
            "rails_from": RAIL_FENCE_MIN_RAILS,
            "rails_through": RAIL_FENCE_MAX_RAILS,
            "trials": len(rows),
            "search": "exhaustive",
            "scope": _SCOPE,
        },
    )


__all__ = [
    "CAESAR_KEYSPACE_SIZE",
    "RAIL_FENCE_KEYSPACE_SIZE",
    "RAIL_FENCE_MAX_RAILS",
    "RAIL_FENCE_MIN_RAILS",
    "brute_caesar",
    "brute_rail_fence",
]
