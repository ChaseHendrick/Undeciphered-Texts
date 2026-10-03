"""Compare reserved evidence after generation, with optional dry narration.

Original suspicious humor changes only narration. It supplies no evidence,
copied character dialogue, paranoid premise, mathematical policy or score.
"""
from __future__ import annotations

from collections.abc import Sequence
from hashlib import sha256
import re

from engine.persona_solver_common import make_report, validate_inputs
from engine.solver_reasoning import investigate_cipher


def _review(plain, heldout, expected_hash, forward=None):
    actual_hash = sha256(plain.encode("ascii")).hexdigest()
    mismatches = [{"offset": i, "expected": expected, "predicted": plain[i]}
                  for i, expected in heldout.items() if plain[i] != expected]
    hash_match = actual_hash == expected_hash if expected_hash is not None else None
    if mismatches or hash_match is False or forward is False:
        status = "contradicted"
    elif hash_match is True:
        status = "exact-reference-match"
    elif heldout:
        status = "crib-supported"
    else:
        status = "unchecked"
    return {"plaintext": plain, "plaintext_sha256": actual_hash, "status": status,
        "verification_crib_positions": len(heldout), "mismatches": mismatches, "reference_hash_match": hash_match,
        "forward_consistent": forward, "evidence_authentication": "caller-supplied; not authenticated by this program",
        "evidence_used_for_generation": False, "historical_correctness_verified": False}


def investigate_skeptic(text, *, cribs=(), verification_cribs=(), expected_plaintext_sha256=None,
                       candidate_plaintexts=None, max_checks=5000, max_candidates=20, voice="dale"):
    """Search from training evidence only, or review explicit unkeyed texts.

    Every candidate review costs one check for its bounded combined crib/hash
    comparisons. Generation reserves review capacity before calling the
    existing ledger; no heldout content enters that call or its ranking.
    """
    cipher, training, known = validate_inputs(text, cribs, max_checks, max_candidates)
    _, reserved_cribs, heldout = validate_inputs(cipher, verification_cribs, max_checks, max_candidates)
    if set(known) & set(heldout):
        raise ValueError("verification cribs overlap training positions; reserved evidence must be separate")
    if not isinstance(voice, str):
        raise TypeError("voice must be dale or plain")
    if voice not in ("dale", "plain"):
        raise ValueError("voice must be dale or plain")
    expected_hash = expected_plaintext_sha256
    if expected_hash is not None:
        if not isinstance(expected_hash, str):
            raise TypeError("expected_plaintext_sha256 must be a hexadecimal string")
        if re.fullmatch(r"[0-9a-fA-F]{64}", expected_hash) is None:
            raise ValueError("expected_plaintext_sha256 requires exactly 64 hexadecimal characters")
        expected_hash = expected_hash.lower()
    explicit = None
    if candidate_plaintexts is not None:
        if (isinstance(candidate_plaintexts, (str, bytes)) or not isinstance(candidate_plaintexts, Sequence)
                or len(candidate_plaintexts) > 100):
            raise TypeError("candidate_plaintexts must be a finite sequence of at most 100 plaintexts")
        explicit = []
        for value in candidate_plaintexts:
            plain, _, _ = validate_inputs(value, (), 0, 1)
            if len(plain) != len(cipher):
                raise ValueError("reviewed plaintext must match normalized ciphertext length")
            if plain not in explicit:
                explicit.append(plain)

    ledger = None
    actions, assumptions = [], [
        "Reserved crib positions are disjoint from training evidence.",
        "Reserved letters and reference hashes are compared after generation and never used by search scoring.",
        "Reference evidence is caller-supplied; matching it does not authenticate provenance or establish historical correctness.",
        "Original persona narration does not change any search, score, comparison, status or answer."]
    reviews, candidates = [], []
    search_checks = verification_checks = 0
    if explicit is not None:
        for plain in explicit[:max_checks]:
            reviews.append(_review(plain, heldout, expected_hash))
            verification_checks += 1
        complete = verification_checks == len(explicit)
        requested = len(explicit)
        search_budget = 0
        reserved = min(max_checks, requested)
        reason = "completed" if complete else "check_budget"
        assumptions.append("Explicit texts have no supplied key; no forward consistency or cipher-model claim is made for them.")
        contradictions = []
    else:
        reserved = min(max_candidates, max_checks // 2)
        search_budget = max_checks - reserved if reserved else 0
        request_limit = min(max_candidates, reserved) if reserved else 1
        ledger = investigate_cipher(cipher, cribs=training, max_checks=search_budget,
                                     max_candidates=request_limit).to_dict()
        search_checks = ledger["checks"]
        actions.extend(ledger["actions"])
        assumptions.append(ledger["bounds"]["completion_scope"])
        requested = len(ledger["candidates"])
        if requested > reserved:
            raise RuntimeError("Skeptic search exceeded reserved candidate-review capacity")
        for item in ledger["candidates"]:
            plain, _, _ = validate_inputs(item["plaintext"], (), 0, 1)
            if len(plain) != len(cipher):
                raise RuntimeError("Skeptic ledger returned a witness of inconsistent length")
            if any(plain[i] != letter for i, letter in known.items()):
                raise RuntimeError("Skeptic ledger witness contradicts training evidence")
            verdict = _review(plain, heldout, expected_hash, item["re_encryption_matches"])
            reviews.append(verdict)
            verification_checks += 1
            if verdict["status"] == "contradicted" or not item["constraints_match"]:
                continue
            candidates.append({"plaintext": plain, "family": item["family"], "key": item["key"],
                "score": item["score"], "forward_consistent": item["re_encryption_matches"], "crib_match": True,
                "evidence": {"verification": verdict, "score_is_correctness": False,
                "reserved_evidence_used_for_fitting": False, "reference_authenticated": False}})
        complete = ledger["search_complete"]
        reason = ledger["stop_reason"]
        contradictions = list(ledger["contradictions"])
    actions.append({"stage": "post_generation_verification" if explicit is None else "explicit_text_review",
        "checks": verification_checks, "requested_candidates": requested,
        "complete": verification_checks == requested, "reserved_positions": len(heldout),
        "training_positions": len(known), "expected_hash_supplied": expected_hash is not None,
        "reserved_evidence_used_for_generation": False})
    report = make_report("skeptic", "post-generation reserved-evidence critic",
        candidates, search_checks + verification_checks, max_checks, complete, reason,
        actions, assumptions, contradictions)
    report.update({"reviews": reviews, "search_executed": explicit is None, "ledger": ledger,
        "search_checks": search_checks, "verification_checks": verification_checks,
        "search_budget": search_budget, "reserved_verification_checks": reserved,
        "unreviewed_candidates": requested - verification_checks,
        "validation_complete": verification_checks == requested,
        "known_positions": len(known), "verification_positions": len(heldout),
        "verification_cribs": [{"offset": c.offset, "plaintext": c.plaintext} for c in reserved_cribs],
        "expected_plaintext_sha256": expected_hash,
        "verification_used_for_generation": False, "verification_used_for_search_ranking": False,
        "reference_authenticated": False, "voice": voice,
        "narration": ("Nice theory. The reserved letters get a vote, and a mismatch gets a receipt."
                      if voice == "dale" else "Reserved evidence was compared after generation; inspect each recorded verdict."),
        "next_actions": ["Authenticate the supplied reference and review independent evidence before claiming a historical solution.",
                         "Unchecked texts remain unverified; absence of a returned alternative does not prove uniqueness."]})
    return report


__all__ = ["investigate_skeptic"]
