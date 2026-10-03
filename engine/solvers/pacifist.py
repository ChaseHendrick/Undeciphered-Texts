"""Pacifist preference among candidate plaintexts for a known Caesar ciphertext.

Given two or more candidate plaintexts for one known Caesar ciphertext, this
module picks the peaceful sentence over a violent one using a small word list
(peace, calm, garden versus attack, war, kill). It is a preference among
candidates, not a decipherment of army message Nr. 86, Kryptos K4, or an
unknown script.
"""

from __future__ import annotations

import re
from collections.abc import Sequence

from engine.alphabet import letters_only, reinject, to_ints, from_ints
from engine.result import SolveResult

METHOD_NAME = "pacifist_preference"

PEACE_WORDS = frozenset({"peace", "calm", "garden"})
VIOLENCE_WORDS = frozenset({"attack", "war", "kill"})

# Fixture: one known Caesar ciphertext and two candidate plaintexts.
# The peaceful sentence is the certificate plaintext.
CAESAR_SHIFT = 7
PEACEFUL_PLAINTEXT = "The calm garden keeps peace under soft light."
VIOLENT_PLAINTEXT = "The attack will kill foes in a brutal war!"
CANDIDATE_PLAINTEXTS = (PEACEFUL_PLAINTEXT, VIOLENT_PLAINTEXT)

_SCOPE = (
    "Preference among candidate plaintexts for a known Caesar ciphertext only. "
    "Not a decipherment of army message Nr. 86, Kryptos K4, or an unknown script."
)

_WORD_RE = re.compile(r"[A-Za-z]+")


def _words(text: str) -> list[str]:
    return [match.group(0).lower() for match in _WORD_RE.finditer(text)]


def pacifist_score(text: str) -> int:
    """Peace word hits minus violence word hits."""
    tokens = _words(text)
    peace_hits = sum(1 for token in tokens if token in PEACE_WORDS)
    violence_hits = sum(1 for token in tokens if token in VIOLENCE_WORDS)
    return peace_hits - violence_hits


def caesar_encrypt(text: str, shift: int) -> str:
    """Encrypt with a known Caesar shift. Non-letters keep their places."""
    letters = letters_only(text)
    if not letters:
        raise ValueError("text has no letters")
    cipher = [(index + shift) % 26 for index in to_ints(letters)]
    return reinject(text, from_ints(cipher))


def known_caesar_ciphertext() -> str:
    """Caesar ciphertext for the peaceful fixture plaintext."""
    return caesar_encrypt(PEACEFUL_PLAINTEXT, CAESAR_SHIFT)


def choose_pacifist(candidates: Sequence[str]) -> str:
    """Pick the candidate with the highest pacifist score.

    Ties keep the earlier candidate. At least one non-empty candidate is
    required.
    """
    cleaned = [text for text in candidates if text and text.strip()]
    if not cleaned:
        raise ValueError("at least one candidate plaintext is required")
    best = cleaned[0]
    best_score = pacifist_score(best)
    for text in cleaned[1:]:
        score = pacifist_score(text)
        if score > best_score:
            best = text
            best_score = score
    return best


def solve_pacifist(
    candidates: Sequence[str],
    *,
    ciphertext: str | None = None,
) -> SolveResult:
    """Prefer the peaceful candidate among proposed plaintexts.

    The optional ciphertext is recorded for the known Caesar fixture. This
    does not decipher Nr. 86, K4, or an unknown script.
    """
    chosen = choose_pacifist(candidates)
    score = float(pacifist_score(chosen))
    details = {
        "mode": "preference_among_candidates",
        "peace_words": sorted(PEACE_WORDS),
        "violence_words": sorted(VIOLENCE_WORDS),
        "pacifist_score": int(score),
        "candidate_count": len([c for c in candidates if c and c.strip()]),
        "scope": _SCOPE,
    }
    if ciphertext is not None:
        details["ciphertext"] = ciphertext
        details["caesar_shift"] = CAESAR_SHIFT
    return SolveResult(
        method=METHOD_NAME,
        plaintext=chosen,
        key="pacifist",
        score=score,
        details=details,
    )


__all__ = [
    "CAESAR_SHIFT",
    "CANDIDATE_PLAINTEXTS",
    "METHOD_NAME",
    "PEACE_WORDS",
    "PEACEFUL_PLAINTEXT",
    "VIOLENCE_WORDS",
    "VIOLENT_PLAINTEXT",
    "caesar_encrypt",
    "choose_pacifist",
    "known_caesar_ciphertext",
    "pacifist_score",
    "solve_pacifist",
]
