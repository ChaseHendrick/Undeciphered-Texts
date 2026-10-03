"""Allocate a finite solver budget using independently checked prior outcomes.

This independent implementation adapts the baseline-relative lift and sample
maturity policy inspected in Fins' difficulty director. It does not copy that
game's code, neural weights or rewards. Adaptation strength is a policy weight,
not a probability of a correct decipherment. No current plaintext is learned.
"""
from __future__ import annotations

from collections.abc import Sequence
from fractions import Fraction
import hashlib
import json
import math
import re

_NAME = re.compile(r"[a-z][a-z0-9-]{0,63}\Z")
_SHA = re.compile(r"[a-fA-F0-9]{64}\Z")
_PROFILE_FIELDS = {"format_version", "baseline_name", "cases"}
_CASE_FIELDS = {"case_id", "ciphertext_sha256", "reference_sha256", "evidence_id",
                "partition", "independently_verified", "evaluation_budget",
                "baseline", "outcomes"}


def _integer(value, name, lower, upper):
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an integer")
    if not lower <= value <= upper:
        raise ValueError(f"{name} must be in {lower}..{upper}")
    return value


def _identifier(value, name, maximum=512):
    if not isinstance(value, str):
        raise TypeError(f"{name} must be text")
    if not value.strip() or len(value) > maximum or any(ord(ch) < 32 for ch in value):
        raise ValueError(f"{name} must be nonempty bounded text without control characters")
    return value


def _name(value, name):
    if not isinstance(value, str):
        raise TypeError(f"{name} must be text")
    if not _NAME.fullmatch(value):
        raise ValueError(f"{name} must be a lowercase strategy identifier")
    return value


def _sha(value, name):
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a SHA-256 string")
    if not _SHA.fullmatch(value):
        raise ValueError(f"{name} must contain 64 hexadecimal digits")
    return value.lower()


def _fields(value, expected, name):
    if not isinstance(value, dict):
        raise TypeError(f"{name} must be a JSON object")
    if set(value) != expected:
        raise ValueError(f"{name} fields must be exactly {', '.join(sorted(expected))}")


def _gate(error, baseline_error, samples):
    lift = max(Fraction(0), min(Fraction(1), 1 - error / baseline_error)) \
        if baseline_error > Fraction(1, 10000) else Fraction(0)
    maturity = min(Fraction(1), Fraction(samples, 18))
    strength = min(Fraction(1), lift / Fraction(4, 25)) * maturity
    return lift, maturity, strength


def baseline_relative_gate(error, baseline_error, samples):
    """Return finite policy lift and maturity, never a correctness probability.

    The 0.16 lift scale and 18-observation maturity reproduce the inspected
    Fins director policy. Error estimation is the caller's responsibility.
    """
    values = []
    for value, name in ((error, "error"), (baseline_error, "baseline_error")):
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise TypeError(f"{name} must be a finite number")
        if not 0 <= value <= 1 or not math.isfinite(value):
            raise ValueError(f"{name} must be finite and in 0..1")
        values.append(Fraction(str(value)))
    _integer(samples, "samples", 0, 100000)
    lift, maturity, strength = _gate(*values, samples)
    return {"relative_lift": float(lift), "sample_maturity": float(maturity),
            "adaptation_strength": float(strength)}


def _outcome(value, budget, name):
    _fields(value, {"correct", "checks"}, name)
    if not isinstance(value["correct"], bool):
        raise TypeError(f"{name} correctness must be independently known boolean feedback")
    return {"correct": value["correct"],
            "checks": _integer(value["checks"], f"{name} checks", 0, budget)}


def _profile(value, strategies):
    _fields(value, _PROFILE_FIELDS, "adaptive profile")
    if _integer(value["format_version"], "profile format_version", 1, 1) != 1:
        raise ValueError("unsupported profile version")
    baseline_name = _name(value["baseline_name"], "baseline_name")
    cases = value["cases"]
    if not isinstance(cases, list) or len(cases) > 512:
        raise TypeError("profile cases must be a list of at most 512 records")
    normalized, case_ids, ciphertexts = [], set(), set()
    for case in cases:
        _fields(case, _CASE_FIELDS, "calibration case")
        case_id = _identifier(case["case_id"], "case_id", 128)
        ciphertext = _sha(case["ciphertext_sha256"], "ciphertext_sha256")
        reference = _sha(case["reference_sha256"], "reference_sha256")
        evidence = _identifier(case["evidence_id"], "evidence_id")
        if case_id in case_ids or ciphertext in ciphertexts:
            raise ValueError("duplicate case_id or ciphertext cannot count as independent evidence")
        case_ids.add(case_id)
        ciphertexts.add(ciphertext)
        if case["partition"] != "calibration" or case["independently_verified"] is not True:
            raise ValueError("only independently verified calibration cases are allowed")
        budget = _integer(case["evaluation_budget"], "evaluation_budget", 1, 100000)
        baseline = _outcome(case["baseline"], budget, "baseline")
        outcomes = case["outcomes"]
        if not isinstance(outcomes, dict) or not 1 <= len(outcomes) <= 32:
            raise TypeError("case outcomes must be an object of 1..32 strategies")
        if not set(strategies).issubset(outcomes):
            raise ValueError("every selected strategy needs a measurement on each same-budget case")
        checked = {}
        for name, outcome in outcomes.items():
            _name(name, "outcome strategy")
            checked[name] = _outcome(outcome, budget, name)
        normalized.append({"case_id": case_id, "ciphertext_sha256": ciphertext,
                           "reference_sha256": reference, "evidence_id": evidence,
                           "partition": "calibration", "independently_verified": True,
                           "evaluation_budget": budget, "baseline": baseline,
                           "outcomes": checked})
    return {"format_version": 1, "baseline_name": baseline_name, "cases": normalized}


def _apportion(weights, budget, reserve=0):
    remaining = budget - reserve * len(weights)
    exact = [weight * remaining for weight in weights]
    floors = [value.numerator // value.denominator for value in exact]
    residual = remaining - sum(floors)
    order = sorted(range(len(weights)), key=lambda index: (-(exact[index] - floors[index]), index))
    for index in order[:residual]:
        floors[index] += 1
    return [value + reserve for value in floors]


def allocate_solver_budget(strategies, *, max_checks=5000, adaptive_profile=None,
                           minimum_exploration=1, ciphertext_sha256=None):
    """Return JSON allocations whose integer values sum exactly to max_checks.

    Profiles contain reference hashes and prior boolean outcomes, never fitting
    plaintext or final evaluation records. Independently verified is a caller
    attestation, not a cryptographic proof. The current ciphertext hash is
    mandatory with a profile so its prior results cannot influence its budget.
    All selected strategies share the same retained cases and evaluation caps.
    """
    if not isinstance(strategies, Sequence) or isinstance(strategies, (str, bytes)):
        raise TypeError("strategies must be a finite sequence")
    if not 1 <= len(strategies) <= 32:
        raise ValueError("choose 1..32 strategies")
    names = tuple(_name(value, "strategy") for value in strategies)
    if len(set(names)) != len(names):
        raise ValueError("strategies must be distinct")
    _integer(max_checks, "max_checks", 0, 100000)
    _integer(minimum_exploration, "minimum_exploration", 1, 100000)
    current = _sha(ciphertext_sha256, "current ciphertext_sha256") \
        if ciphertext_sha256 is not None else None
    normalized_profile, profile_hash, cases, excluded = None, None, [], 0
    if adaptive_profile is not None:
        if current is None:
            raise ValueError("current ciphertext_sha256 is required with an adaptive profile")
        normalized_profile = _profile(adaptive_profile, names)
        profile_hash = hashlib.sha256(json.dumps(normalized_profile, sort_keys=True,
                                                 separators=(",", ":"), allow_nan=False).encode()).hexdigest()
        cases = [case for case in normalized_profile["cases"]
                 if case["ciphertext_sha256"] != current]
        excluded = len(normalized_profile["cases"]) - len(cases)
    count = len(cases)
    base_error = Fraction(sum(not case["baseline"]["correct"] for case in cases), count) \
        if count else Fraction(0)
    metrics, gates, correct_counts, costs = {}, {}, {}, {}
    for name in names:
        correct = sum(case["outcomes"][name]["correct"] for case in cases)
        error = Fraction(count - correct, count) if count else Fraction(0)
        lift, maturity, strength = _gate(error, base_error, count)
        successful = [Fraction(case["outcomes"][name]["checks"], case["evaluation_budget"])
                      for case in cases if case["outcomes"][name]["correct"]]
        cost = sum(successful, Fraction(0)) / len(successful) if successful else None
        gates[name], correct_counts[name], costs[name] = strength, correct, cost
        metrics[name] = {
            "checked_cases": count, "correct_cases": correct, "incorrect_cases": count - correct,
            "correct_rate": float(Fraction(correct, count)) if count else None,
            "error": float(error) if count else None,
            "baseline_error": float(base_error) if count else None,
            "relative_lift": float(lift), "sample_maturity": float(maturity),
            "evidence_strength": float(strength),
            "mean_successful_check_fraction": float(cost) if cost is not None else None,
        }
    eligible = [name for name in names if gates[name] > 0]
    winners, strength = [], Fraction(0)
    if eligible:
        best_correct = max(correct_counts[name] for name in eligible)
        best_accuracy = [name for name in eligible if correct_counts[name] == best_correct]
        best_cost = min(costs[name] for name in best_accuracy)
        winners = [name for name in best_accuracy if costs[name] == best_cost]
        strength = gates[winners[0]]
    feasible = max_checks >= minimum_exploration * len(names)
    reason = None
    if not feasible:
        strength, reason = Fraction(0), "insufficient budget for minimum exploration"
    elif not count:
        reason = "no eligible prior calibration cases"
    elif not winners:
        reason = "no verified accuracy improvement over the same-case baseline"
    uniform = Fraction(1, len(names))
    weights = [(1 - strength) * uniform + (strength / len(winners) if name in winners else 0)
               for name in names]
    reserve = minimum_exploration if feasible else 0
    amounts = _apportion(weights, max_checks, reserve)
    return {
        "format_version": 1, "policy": "baseline-relative gated allocation",
        "allocations": dict(zip(names, amounts)), "max_checks": max_checks,
        "minimum_exploration": minimum_exploration, "minimum_exploration_feasible": feasible,
        "adaptation_strength": float(strength), "winning_strategies": winners,
        "fallback_reason": reason, "feedback_case_count": count,
        "excluded_current_case_count": excluded, "strategy_metrics": metrics,
        "profile_sha256": profile_hash,
        "baseline_name": normalized_profile["baseline_name"] if normalized_profile else None,
        "evidence_contract": "caller-attested independent calibration outcomes; source truth is not verified by this allocator",
        "strength_meaning": "allocation policy weight, not probability of correctness",
        "check_cost_meaning": "tool-specific work fractions, not measured wall-clock speed",
        "claimed_plaintext": None, "current_case_correctness_known": False,
        "scope": "A bounded scheduler, not a neural classifier or proof of a historical decipherment.",
    }


__all__ = ["allocate_solver_budget", "baseline_relative_gate"]
