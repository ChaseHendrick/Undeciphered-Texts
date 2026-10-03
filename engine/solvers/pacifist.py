"""Pacifist preference among candidate plaintexts for a known Caesar ciphertext.

Given two or more candidate plaintexts for one known Caesar ciphertext, this
module picks the peaceful sentence over a violent one using a small word list
(peace, calm, garden versus attack, war, kill). It is a preference among
candidates, not a decipherment of army message Nr. 86, Kryptos K4, or an
unknown script.

The separate investigate_pacifist API exhaustively tests a finite affine
model using aligned caller cribs. It does not use the legacy preference
scores or a language model, and it requires complete enumeration before
reporting conditional key uniqueness or forced plaintext consensus.
"""

from __future__ import annotations

import re
from collections.abc import Sequence

from engine.alphabet import letters_only, reinject, to_ints, from_ints
from engine.result import SolveResult
from engine.persona_solver_common import make_report, validate_inputs
from engine.solvers.affine import affine_decrypt, affine_encrypt

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


def investigate_pacifist(text, *, cribs=(), max_checks=5000, max_candidates=20):
    """Exhaust all 312 invertible A-Z affine keys with no semantic ranking.

    Every key trial is one check. Retention never terminates enumeration,
    and consensus includes every compatible key. Incomplete searches expose
    literal witnesses without claiming an exact count or forced prediction.
    """
    cipher, _, known = validate_inputs(text, cribs, max_checks, max_candidates)
    multipliers = (1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25)
    candidates = []
    consensus = None
    compatible = checks = 0
    for multiplier in multipliers:
        for shift in range(26):
            if checks >= max_checks:
                break
            checks += 1
            plain = affine_decrypt(cipher, multiplier, shift)
            if not all(plain[i] == letter for i, letter in known.items()):
                continue
            if affine_encrypt(plain, multiplier, shift) != cipher:
                raise RuntimeError("Pacifist affine witness failed forward verification")
            compatible += 1
            if consensus is None:
                consensus = list(plain)
            else:
                for i, letter in enumerate(plain):
                    if consensus[i] != letter:
                        consensus[i] = "?"
            if len(candidates) < max_candidates:
                candidates.append({"plaintext": plain, "family": "affine",
                    "key": {"a": multiplier, "b": shift}, "score": 0.0,
                    "forward_consistent": True, "crib_match": True, "evidence": {
                    "method": "exact invertible affine enumeration with caller aligned cribs",
                    "known_positions": len(known), "predicted_letters_beyond_crib": len(cipher) - len(known),
                    "semantic_ranking_used": False, "independently_verified": False,
                    "witness_is_forced_by_itself": False}})
        if checks >= max_checks:
            break

    complete = checks == 312
    forced = "".join(consensus) if complete and consensus is not None else "?" * len(cipher)
    unique_key = compatible == 1 if complete else None
    unique_plaintext = "?" not in forced if complete and compatible else False if complete else None
    if not complete:
        next_actions = ["Finish the remaining affine key checks before interpreting counts, uniqueness or consensus."]
    elif not known:
        next_actions = ["Supply independently justified aligned plaintext cribs; all 312 affine keys remain compatible."]
    elif compatible == 0:
        next_actions = ["Review the transcription, crib alignment and affine model assumption; no tested key fits."]
    elif compatible == 1:
        next_actions = ["Test independent heldout plaintext or a cited reference before treating the conditional candidate as verified."]
    else:
        next_actions = ["Seek another independent aligned letter to distinguish the remaining keys.",
                        "Use consensus only as a consequence of the declared affine model and supplied cribs."]
    contradictions = (["No invertible affine key satisfies the supplied aligned cribs."]
                      if complete and compatible == 0 else [])
    report = make_report("pacifist", "conservative exact affine constraints without semantic scoring", candidates,
        checks, max_checks, complete, "completed" if complete else "check_budget",
        [{"branch": "affine", "declared_keys": 312, "checks": checks, "search_complete": complete,
          "retained_witnesses": len(candidates), "ranking": "literal multiplier-then-shift enumeration order"}],
        ["Ciphertext is an invertible affine substitution over normalized A-Z letters.",
         "Caller cribs are aligned hard constraints, not independently verified by this search.",
         "Consensus uses all compatible keys; retained witness storage does not affect it.",
         "No peace, violence, English-language score or persona preference selects a key.",
         "Complete affine enumeration does not test other cipher families or prove historical correctness."],
        contradictions)
    report.update({"compatible_key_count": compatible if complete else None,
        "compatible_keys_found": compatible, "compatibility_count_is_exact": complete,
        "unique_key_within_model": unique_key, "plaintext_unique_within_model": unique_plaintext,
        "consensus_plaintext": forced, "consensus_complete": complete and compatible > 0,
        "consensus_scope": "all compatible keys after complete affine enumeration" if complete else "withheld until complete enumeration",
        "known_positions": len(known), "known_evidence_count": len(known),
        "provided_crib_mask": "".join(known.get(i, "?") for i in range(len(cipher))),
        "abstained": not bool(complete and known and unique_plaintext),
        "untested_keys": 312 - checks, "candidates_truncated": compatible > len(candidates),
        "ranking": "none; literal key witnesses only", "semantic_confidence": None,
        "next_actions": next_actions})
    report["thought"]["next_action"] = next_actions[0]
    return report


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
    "investigate_pacifist",
]
