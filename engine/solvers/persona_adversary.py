"""Search for concrete competing witnesses using the same caller evidence.

Adversary means testing unsupported uniqueness, never inventing wrong answers.
The finite ledger, supplied cribs and optional proposal determine work; persona
flavor is not a key, scoring signal or source of cryptographic evidence.
"""
from __future__ import annotations

from engine.persona_solver_common import make_report, validate_inputs
from engine.solver_reasoning import investigate_cipher


def investigate_adversary(text, *, cribs=(), candidate=None, max_checks=5000, max_candidates=20):
    """Find bounded alternatives without fitting or accepting a caller proposal."""
    cipher, training, known = validate_inputs(text, cribs, max_checks, max_candidates)
    proposal = None
    if candidate is not None:
        proposal, _, _ = validate_inputs(candidate, (), 0, 1)
        if len(proposal) != len(cipher):
            raise ValueError("candidate must match the normalized ciphertext length")
    proposal_checks = int(proposal is not None and max_checks > 0)
    search_budget = max_checks - proposal_checks
    ledger = investigate_cipher(cipher, cribs=training, max_checks=search_budget,
        max_candidates=min(100, max_candidates + int(proposal is not None))).to_dict()
    mismatches = ([{"offset": i, "expected": letter, "proposed": proposal[i]}
                   for i, letter in known.items() if proposal[i] != letter]
                  if proposal_checks else [])
    alternatives = []
    observed = set()
    proposal_seen = False
    for item in ledger["candidates"]:
        if not item["re_encryption_matches"] or not item["constraints_match"]:
            continue
        plain = item["plaintext"]
        observed.add(plain)
        if proposal is not None and plain == proposal:
            proposal_seen = True
            continue
        if any(plain[i] != letter for i, letter in known.items()):
            raise RuntimeError("Adversary ledger witness contradicts caller evidence")
        if any(c["plaintext"] == plain for c in alternatives):
            continue
        alternatives.append({"plaintext": plain, "family": item["family"], "key": item["key"],
            "score": item["score"], "forward_consistent": True, "crib_match": True, "evidence": {
            "method": "bounded competing witness under the same training cribs",
            "proposal_used_for_fitting": False, "known_positions": len(known),
            "alternative_to_proposal": proposal is not None, "independently_verified": False,
            "score_is_correctness": False}})
    alternatives = alternatives[:max_candidates]
    actions = list(ledger["actions"])
    if proposal is not None:
        actions.append({"stage": "proposal_crib_review", "checks": proposal_checks,
            "compared": bool(proposal_checks), "mismatches": len(mismatches),
            "scope": "Caller proposal is excluded after generation and never becomes a fitted constraint"})
    report = make_report("adversary", "search concrete competing witnesses under unchanged caller evidence",
        alternatives, ledger["checks"] + proposal_checks, max_checks, ledger["search_complete"], ledger["stop_reason"],
        actions, [ledger["bounds"]["completion_scope"],
        "A proposed plaintext is an object to challenge, not independent evidence or a hidden key.",
        "Retained examples and English ranking do not enumerate all plaintexts or all cipher families.",
        "A concrete competing witness can refute uniqueness inside stated models; absence cannot prove global uniqueness."],
        ledger["contradictions"])
    report.update({"ledger": ledger, "search_checks": ledger["checks"], "proposal_checks": proposal_checks,
        "proposed_plaintext": proposal,
        "known_positions": len(known), "proposed_witness_seen": proposal_seen,
        "proposal_contradicted_by_supplied_cribs": bool(mismatches), "proposal_crib_mismatches": mismatches,
        "proposal_review_complete": proposal is None or bool(proposal_checks),
        "alternative_count_retained": len(alternatives), "ambiguity_observed": len(observed) >= 2,
        "uniqueness_refuted_within_observed_models": len(observed) >= 2,
        "exhaustive_all_cipher_uniqueness": False,
        "next_actions": ["Check competing witnesses against evidence that was not used for fitting.",
                         "Do not infer uniqueness from an exhausted budget or a short retained list."],
        "narration": "A polished answer can still have company. Here are the actual witnesses."})
    return report


__all__ = ["investigate_adversary"]
