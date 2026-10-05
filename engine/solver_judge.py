"""A judge for solver claims. It does not produce a reading.

A historical name cannot be marked solved here. A stored plaintext is blocked
and is not copied out. Caesar, Vigenere, and Beaufort claims are checked by
re-encryption. A match is a forward check, not a decipherment of an unsolved text.
"""

from __future__ import annotations

import hashlib
import math
from typing import Any

from engine.alphabet import letters_only
from engine.ciphers import caesar_encrypt, vigenere_encrypt
from engine.result import SolveResult
from engine.solvers.beaufort import beaufort_encrypt

_HISTORICAL = (
    "k4",
    "kryptos",
    "dagapeyeff",
    "voynich",
    "beale",
    "zodiac",
    "rongorongo",
    "linear a",
    "phaistos",
    "indus",
)


def _blocked_name(value: str) -> bool:
    folded = value.lower().replace("'", "")
    return any(name in folded for name in _HISTORICAL)


def _sha(text: str) -> str:
    return hashlib.sha256(letters_only(text).encode("ascii")).hexdigest()


def judge_claim(claim: dict) -> dict:
    """Block a claim that says solved, stores plaintext, or names an unsolved text."""
    if not isinstance(claim, dict):
        raise TypeError("a claim must be a dictionary")
    blocks: list[str] = []
    if claim.get("solved") is True:
        blocks.append("solved_flag")
    plain = claim.get("claimed_plaintext")
    if isinstance(plain, str) and plain.strip():
        blocks.append("plaintext_stored")
    pieces = " ".join(str(claim.get(key, "")) for key in ("target", "method", "family", "cipher", "name"))
    if _blocked_name(pieces) and claim.get("solved") is True:
        blocks.append("historical_solved")
    score = claim.get("score")
    if score is not None and (isinstance(score, bool) or not isinstance(score, (int, float)) or not math.isfinite(float(score))):
        blocks.append("nonfinite_score")
    if claim.get("reencryption_matches") is False and claim.get("solved") is True:
        blocks.append("reencryption_failed")
    return {
        "solved": False,
        "claimed_plaintext": None,
        "accepted": not blocks,
        "blocks": blocks,
        "scope": "A judge blocks a claim. It does not produce a reading.",
    }


def reencryption_matches(method: str, plaintext: str, key: str, ciphertext: str) -> bool | None:
    """Whether the forward map rebuilds the ciphertext. None if this judge has no map."""
    if not all(isinstance(value, str) for value in (method, plaintext, key, ciphertext)):
        raise TypeError("roundtrip fields must be text")
    kind = method.strip().lower()
    plain = letters_only(plaintext)
    cipher = letters_only(ciphertext)
    if kind == "caesar":
        try:
            shift = int(key)
        except ValueError:
            return False
        return letters_only(caesar_encrypt(plain, shift)) == cipher
    if kind == "vigenere":
        if not letters_only(key):
            return False
        return letters_only(vigenere_encrypt(plain, key)) == cipher
    if kind == "beaufort":
        if not letters_only(key):
            return False
        return letters_only(beaufort_encrypt(plain, key)) == cipher
    return None


def judge_solve_result(result: SolveResult, ciphertext: str) -> dict:
    """Judge one solver result. The plaintext is hashed and not returned."""
    if not isinstance(result, SolveResult):
        raise TypeError("result must be a SolveResult")
    if not isinstance(ciphertext, str):
        raise TypeError("ciphertext must be text")
    blocks: list[str] = []
    if not isinstance(result.method, str) or not result.method.strip():
        blocks.append("missing_method")
    if not isinstance(result.score, (int, float)) or isinstance(result.score, bool) or not math.isfinite(float(result.score)):
        blocks.append("nonfinite_score")
    if _blocked_name(result.method):
        blocks.append("historical_method")
    matched = reencryption_matches(result.method, result.plaintext, result.key, ciphertext)
    if matched is False:
        blocks.append("reencryption_failed")
    return {
        "solved": False,
        "claimed_plaintext": None,
        "method": result.method,
        "accepted": not blocks,
        "blocks": blocks,
        "reencryption_matches": matched,
        "plaintext_sha256": _sha(result.plaintext),
        "scope": "A matching forward map is not a historical decipherment.",
    }


def judge_any(value: Any, ciphertext: str | None = None) -> dict:
    """Dispatch a claim dictionary or a SolveResult. Plaintext is not copied."""
    if isinstance(value, SolveResult):
        if ciphertext is None:
            raise ValueError("a solver result needs the ciphertext it was fit to")
        return judge_solve_result(value, ciphertext)
    if isinstance(value, dict):
        return judge_claim(value)
    raise TypeError("unsupported claim")
