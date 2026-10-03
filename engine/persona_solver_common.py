"""Shared bounded inputs and factual reports for complementary search personas.

Personality selects a search policy. It supplies no plaintext evidence,
independent correctness, subjective feelings or neural-network identity.
"""
from __future__ import annotations

from collections.abc import Sequence
from engine.reverse_engineer import Crib

COORDINATES = "zero-based A-Z plaintext letters after removing spaces and punctuation"
SCOPE = (
    "Repository-specific search composition. Personality, agreement, English "
    "scores and re-encryption are not independent evidence of a historical "
    "decipherment. No unknown-script reading or Nr. 86 solution is claimed."
)


def _integer(value, name, low, high):
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an integer")
    if not low <= value <= high:
        raise ValueError(f"{name} must be in {low}..{high}")


def _letters(text, name, *, minimum, maximum, raw_limit):
    if not isinstance(text, str):
        raise TypeError(f"{name} must be text")
    if len(text) > raw_limit or any(ch.isalnum() and not (ch.isascii() and ch.isalpha()) for ch in text):
        raise ValueError(f"{name} requires ASCII letters and at most {raw_limit} raw characters")
    letters = "".join(ch.upper() for ch in text if ch.isascii() and ch.isalpha())
    if not minimum <= len(letters) <= maximum:
        raise ValueError(f"{name} requires {minimum}..{maximum} A-Z letters")
    return letters


def validate_inputs(text, cribs, max_checks, max_candidates):
    """Return normalized letters, shared typed cribs and known letter positions."""
    letters = _letters(text, "ciphertext", minimum=4, maximum=512, raw_limit=4096)
    _integer(max_checks, "max_checks", 0, 100000)
    _integer(max_candidates, "max_candidates", 1, 100)
    if not isinstance(cribs, Sequence) or isinstance(cribs, (str, bytes)) or len(cribs) > 128:
        raise TypeError("cribs must be a finite sequence of at most 128 Crib objects")
    normalized, known = [], {}
    for crib in cribs:
        if not isinstance(crib, Crib):
            raise TypeError("cribs must contain shared Crib objects")
        _integer(crib.offset, "crib offset", 0, len(letters) - 1)
        plain = _letters(crib.plaintext, "crib", minimum=1, maximum=512, raw_limit=2048)
        if crib.offset + len(plain) > len(letters):
            raise ValueError("crib exceeds normalized plaintext length")
        normalized.append(Crib(crib.offset, plain))
        for index, letter in enumerate(plain, crib.offset):
            if index in known and known[index] != letter:
                raise ValueError("overlapping cribs contradict each other")
            known[index] = letter
    return letters, tuple(normalized), known


def make_report(persona, strategy, candidates, checks, budget, search_complete,
                stop_reason, actions, assumptions, contradictions=()):
    """Record completed program work without inferring verified correctness."""
    _integer(checks, "checks", 0, 100000)
    _integer(budget, "budget", 0, 100000)
    if checks > budget:
        raise ValueError("persona checks exceed the shared budget")
    if not isinstance(search_complete, bool):
        raise TypeError("search_complete must be boolean")
    return {
        "persona": persona, "strategy": strategy, "candidates": list(candidates),
        "checks": checks, "max_checks": budget, "search_complete": search_complete,
        "stop_reason": stop_reason, "coordinate_system": COORDINATES,
        "actions": list(actions), "assumptions": list(assumptions),
        "contradictions": list(contradictions),
        "thought": {"kind": "program-generated search summary", "strategy": strategy,
                    "tested_checks": checks, "candidate_count": len(candidates),
                    "next_action": "independently verify candidates" if candidates else "review evidence and untested models"},
        "claimed_plaintext": None, "correctness_known": False, "happiness": None,
        "solved_status": "unverified", "scope": SCOPE,
    }


__all__ = ["validate_inputs", "make_report", "COORDINATES", "SCOPE"]
