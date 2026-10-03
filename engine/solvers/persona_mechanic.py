"""Aligned-crib algebra and recurrence portfolio under one work budget.

Progressive Key, exact plaintext-autokey propagation and Hill inference use
their existing model definitions. Unknown slots remain unknown; scores rank
complete forward-consistent witnesses without proving historical correctness.
"""
from __future__ import annotations

from engine.language import get_model
from engine.persona_solver_common import make_report, validate_inputs
from engine.solvers.autokey import autokey_encrypt
from engine.solvers.autokey_inference import _columns
from engine.solvers.hill_inference import infer_hill
from engine.solvers.progressive_key import infer_progressive_key, progressive_key_encrypt


def _autokey_trial(cipher, known, period):
    """Derive a residue-column seed only when supplied letters force it."""
    values = [ord(ch) - 65 for ch in cipher]
    forced = ["?"] * len(cipher)
    unresolved = 0
    for positions, base in _columns(values, period):
        seeds = {(ord(known[index]) - 65 - base[j]) * (1 if j % 2 == 0 else -1) % 26
                 for j, index in enumerate(positions) if index in known}
        if len(seeds) > 1:
            return None
        if not seeds:
            unresolved += 1
            continue
        seed = next(iter(seeds))
        for j, index in enumerate(positions):
            forced[index] = chr(65 + (base[j] + (seed if j % 2 == 0 else -seed)) % 26)
    keyword = "".join("?" if forced[i] == "?" else
                      chr(65 + (values[i] - ord(forced[i]) + 65) % 26) for i in range(period))
    return {"family": "autokey", "period": period, "key_slots": keyword,
            "unresolved_parameters": unresolved, "complete_key": unresolved == 0,
            "compatible_primers": 26 ** unresolved, "predicted_plaintext": "".join(forced)}


def investigate_mechanic(text, *, cribs=(), max_checks=5000, max_candidates=20) -> dict:
    """Allocate remaining checks among three finite clue-dependent model searches.

    Progressive Key tests period/progression settings. Autokey tests exact
    column propagation once per primer length. Hill tests inverse rows and row
    pairs, with no supplied matrix. Check units are disclosed per branch.
    """
    cipher, normalized, known = validate_inputs(text, cribs, max_checks, max_candidates)
    strategy = "aligned-crib modular algebra and exact recurrence propagation"
    assumptions = [
        "Supplied aligned letters are premises, not independent correctness evidence",
        "Progressive Key starts its progression at zero and tests periods through 16",
        "Plaintext-autokey primer lengths are bounded at 32; unforced columns stay unknown",
        "Hill uses complete two-letter blocks and an unknown invertible 2x2 column-vector matrix",
        "English quadgrams rank complete witnesses; they never fill unknown letters",
    ]
    advice = {"status": "not_used", "candidates": [], "claimed_plaintext": None,
              "reason": "This persona applies algebraic constraints without neural inference"}
    if not normalized:
        report = make_report("mechanic", strategy, [], 0, max_checks, False,
                             "requires_aligned_cribs", [], assumptions)
        report.update(hypotheses=[], hypotheses_truncated=False, partial_hypotheses_seen=0,
                      branch_reports={}, neural_advice=advice)
        return report
    active = ["progressive-key", "autokey"] + (["hill"] if len(cipher) % 2 == 0 else [])
    actions, branch_reports, hypotheses = [], {}, []
    retained = {}
    checks = compatible = partial_count = 0
    model = None

    def retain(family, key, plain, forward, evidence):
        nonlocal model, compatible, retained
        if forward != cipher or any(plain[position] != letter for position, letter in known.items()):
            raise RuntimeError("Mechanic witness failed forward or crib verification")
        if "?" in plain:
            raise RuntimeError("Mechanic cannot retain an incomplete plaintext as a full candidate")
        compatible += 1
        if model is None:
            model = get_model()
        candidate = {"plaintext": plain, "family": family, "key": key,
                     "score": model.score([ord(ch) - 65 for ch in plain]),
                     "forward_consistent": True, "crib_match": True,
                     "evidence": {**evidence, "known_positions": len(known),
                                  "independent_correctness": False}}
        identity = (family, plain)
        old = retained.get(identity)
        if old is None or _order(candidate) < _order(old):
            retained[identity] = candidate
        retained = {(c["family"], c["plaintext"]): c
                    for c in sorted(retained.values(), key=_order)[:max_candidates]}

    def partial(hypothesis):
        nonlocal partial_count
        partial_count += 1
        if len(hypotheses) < max_candidates:
            hypotheses.append(hypothesis)

    for index, branch in enumerate(active):
        remaining = max_checks - checks
        allocation = (remaining + len(active) - index - 1) // (len(active) - index)
        if branch == "progressive-key":
            bound = min(16, len(cipher))
            result = infer_progressive_key(cipher, cribs=normalized, max_period=bound,
                                          max_checks=allocation, max_candidates=26 * bound)
            raw = result.to_dict()
            branch_reports[branch] = raw
            used, complete = result.checks, result.search_complete
            for item in result.candidates:
                if not item.key_complete:
                    partial({"family": branch, "period": item.period, "progression": item.progression,
                             "key_slots": item.key, "unresolved_parameters": item.unresolved_key_slots,
                             "predicted_plaintext": item.predicted_plaintext})
                else:
                    key = {"keyword": item.key, "period": item.period, "progression": item.progression}
                    forward = progressive_key_encrypt(item.predicted_plaintext, keyword=item.key,
                                                      progression=item.progression)
                    retain(branch, key, item.predicted_plaintext, forward,
                           {"method": "aligned Progressive Key modular constraints", "complete_key": True})
        elif branch == "autokey":
            period_bound = min(32, len(cipher))
            used = min(allocation, period_bound)
            rows = []
            rejected = 0
            for period in range(1, used + 1):
                hypothesis = _autokey_trial(cipher, known, period)
                if hypothesis is None:
                    rejected += 1
                else:
                    rows.append(hypothesis)
                    if hypothesis["complete_key"]:
                        plain, keyword = hypothesis["predicted_plaintext"], hypothesis["key_slots"]
                        retain(branch, {"keyword": keyword, "period": period}, plain,
                               autokey_encrypt(plain, keyword),
                               {"method": "exact plaintext-autokey residue-column propagation",
                                "all_letters_forced_within_period": True})
                    else:
                        partial(hypothesis)
            complete = used == period_bound
            branch_reports[branch] = {"checks": used, "periods_requested": period_bound,
                                      "search_complete": complete, "inconsistent_periods": rejected,
                                      "hypotheses": rows}
        else:
            raw = infer_hill(cipher, cribs=normalized, max_checks=allocation, max_candidates=max_candidates)
            branch_reports[branch] = raw
            used, complete = raw["checks"], raw["search_complete"]
            for item in raw["candidates"]:
                # infer_hill already included its forward replay in this key trial.
                key = {"matrix": item["matrix"], "inverse_matrix": item["inverse_matrix"]}
                retain(branch, key, item["plaintext"], cipher if item["forward_consistent"] else "",
                       {"method": "unknown Hill inverse-row and matrix inference",
                        "key_count_if_search_complete": raw["compatible_key_count"],
                        "example_from_incomplete_search": not complete})
        if not 0 <= used <= allocation:
            raise RuntimeError("Mechanic branch exceeded its work allocation")
        checks += used
        actions.append({"tool": branch, "allocated_checks": allocation, "checks": used,
                        "search_complete": complete,
                        "check_unit": "one period/progression setting" if branch == "progressive-key"
                        else "one bounded-period exact recurrence propagation" if branch == "autokey"
                        else "one inverse-row or compatible-row pair trial with applicable forward replay"})
    if len(cipher) % 2:
        branch_reports["hill"] = {"status": "not_applicable", "checks": 0,
                                  "reason": "Ciphertext has an incomplete two-letter block; no padding is invented"}
    complete = all(action["search_complete"] for action in actions)
    report = make_report("mechanic", strategy, sorted(retained.values(), key=_order),
                         checks, max_checks, complete, "complete" if complete else "check_limit",
                         actions, assumptions)
    report.update(hypotheses=hypotheses, conditional_predictions=hypotheses,
                  hypotheses_truncated=partial_count > len(hypotheses), partial_hypotheses_seen=partial_count,
                  branch_reports=branch_reports, neural_advice=advice, compatible_trials=compatible,
                  bounds={"max_checks": max_checks, "max_candidates": max_candidates,
                          "progressive_max_period": min(16, len(cipher)), "progressions": list(range(26)),
                          "autokey_max_period": min(32, len(cipher)), "hill_block": 2,
                          "completion_scope": "the applicable declared models, not arbitrary ciphers or unbounded key periods"},
                  ranking="summed repository English quadgram score; no unknown letters filled by ranking")
    return report


def _order(candidate):
    return (-candidate["score"], candidate["family"], candidate["plaintext"], repr(candidate["key"]))


__all__ = ["investigate_mechanic"]
