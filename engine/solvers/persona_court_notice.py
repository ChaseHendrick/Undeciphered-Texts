"""Bounded Emperor investigation and legacy court-notice sentence preference.

Persona: court notice. Reworded from a world-emperor label into plain speech
about a written order. The legacy word list is a preference among candidates.
These are preferences among candidates, not decipherments of Nr. 86, K4,
or an unknown script. investigate_emperor instead tests bounded cipher models
and records conditional predictions; it does not filter by the word list.
"""

from __future__ import annotations

import re

# Word list for the court-notice preference: empire, decree, throne.
WORD_LIST = ("empire", "decree", "throne")

DISCLAIMER = (
    "These are preferences among candidates, not decipherments of "
    "Nr. 86, K4, or an unknown script."
)


def covers(text: str) -> bool:
    """True when every court-notice word appears as its own word."""
    lowered = text.lower()
    return all(re.search(rf"\b{re.escape(word)}\b", lowered) for word in WORD_LIST)


def choose(left: str, right: str) -> str:
    """Pick the candidate that matches the court-notice word list.

    Exactly one of the two sentences must contain empire, decree, and throne.
    The other is a plain alternative. This does not decipher anything.
    """
    left_ok = covers(left)
    right_ok = covers(right)
    if left_ok == right_ok:
        raise ValueError("need exactly one candidate that matches the word list")
    return left if left_ok else right


def investigate_emperor(text, *, cribs=(), max_checks=5000, max_candidates=20) -> dict:
    """Run a systematic search under one shared cryptanalytic check budget.

    Aligned cribs enable affine, substitution and repeating-key inference.
    Otherwise every invertible affine key is tested as budget permits. A
    finite transposition portfolio uses the remaining budget. English scores
    and optional neural advice rank witnesses without establishing correctness.
    """
    from engine.persona_solver_common import make_report, validate_inputs
    from engine.solver_reasoning import investigate_cipher

    letters, normalized_cribs, _ = validate_inputs(text, cribs, max_checks, max_candidates)
    result = investigate_cipher(letters, cribs=normalized_cribs,
                                max_checks=max_checks, max_candidates=max_candidates)
    ledger = result.to_dict()
    candidates = []
    for candidate in ledger["candidates"]:
        candidates.append({
            "plaintext": candidate["plaintext"], "family": candidate["family"],
            "key": candidate["key"], "score": candidate["score"],
            "forward_consistent": candidate["re_encryption_matches"],
            "crib_match": candidate["constraints_match"],
            "evidence": {
                "forward_transform": "re-encryption compared with normalized ciphertext",
                "supplied_cribs": len(normalized_cribs),
                "score_scope": "repository English quadgram ranking, not correctness",
                "neural_probability": candidate["neural_probability"],
                "independent_correctness": False,
            },
        })
    report = make_report(
        "emperor", "systematic constraint fitting and finite affine/transposition enumeration",
        candidates, ledger["checks"], max_checks, ledger["search_complete"],
        ledger["stop_reason"], ledger["actions"],
        ["ASCII A-Z plaintext coordinates; formatting is removed",
         "Supplied cribs are premises, not independent validation",
         ledger["bounds"]["completion_scope"],
         "English scoring and neural family advice cannot prove a decipherment"],
        contradictions=ledger["contradictions"],
    )
    report.update(
        ledger=ledger,
        hypotheses=ledger["hypotheses"],
        conditional_predictions=ledger["hypotheses"],
        prediction_scope="Partial hypotheses keep unknown positions; complete witnesses are conditional on their cipher model",
        neural_advice=ledger["neural_advice"],
        next_actions=ledger["next_actions"],
        bounds=ledger["bounds"],
        legacy_preference_scope=DISCLAIMER,
    )
    return report


__all__ = ["WORD_LIST", "DISCLAIMER", "covers", "choose", "investigate_emperor"]
