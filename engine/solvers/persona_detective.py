"""Bounded unknown-offset Vigenere crib search with repeated confirmation.

This applies the existing engine.solvers.crib equations under an explicit
alignment/period work budget. It supplies no default crib, keyword or reading.
"""
from __future__ import annotations

import heapq
from engine.language import get_model
from engine.persona_solver_common import make_report, validate_inputs
from engine.reverse_engineer import Crib
from engine.solvers.crib import CribHit


def _integer(value, name, maximum):
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an integer")
    if not 1 <= value <= maximum:
        raise ValueError(f"{name} must be in 1..{maximum}")


def investigate_detective(text, *, crib, max_period=16, min_checks=2,
                          max_checks=5000, max_candidates=20) -> dict:
    """Test unknown crib offsets, requiring a filled and confirmed periodic key.

    min_checks counts repeated crib letters confirming a prior key slot.
    Report checks counts alignment/period trials, with applicable forward
    replay included. Recovered letters outside the crib remain conditional.
    """
    cipher, normalized, _ = validate_inputs(text, (Crib(0, crib),), max_checks, max_candidates)
    plain_crib = normalized[0].plaintext
    if len(plain_crib) < 2:
        raise ValueError("crib must contain at least two ASCII letters")
    _integer(max_period, "max_period", 128)
    _integer(min_checks, "min_checks", 512)
    period_limit = min(max_period, max(0, len(plain_crib) - min_checks))
    alignments = len(cipher) - len(plain_crib) + 1
    total = alignments * period_limit
    checks = compatible = 0
    heap = []
    model = None
    cipher_values = [ord(ch) - 65 for ch in cipher]
    crib_values = [ord(ch) - 65 for ch in plain_crib]
    for start in range(alignments):
        stream = [(cipher_values[start + i] - value) % 26 for i, value in enumerate(crib_values)]
        for period in range(1, period_limit + 1):
            if checks >= max_checks:
                break
            checks += 1
            slots = [None] * period
            confirmations = 0
            for index, shift in enumerate(stream):
                slot = (start + index) % period
                previous = slots[slot]
                if previous is None:
                    slots[slot] = shift
                elif previous != shift:
                    break
                else:
                    confirmations += 1
            else:
                if confirmations < min_checks or any(shift is None for shift in slots):
                    continue
                key = [int(shift) for shift in slots]
                plain = [(value - key[index % period]) % 26 for index, value in enumerate(cipher_values)]
                plaintext = "".join(chr(65 + value) for value in plain)
                forward = "".join(chr(65 + (value + key[index % period]) % 26) for index, value in enumerate(plain))
                if forward != cipher or plaintext[start:start + len(plain_crib)] != plain_crib:
                    raise RuntimeError("Detective witness failed forward or crib verification")
                if model is None:
                    model = get_model()
                hit = CribHit(start, period, "".join(chr(65 + shift) for shift in key),
                              confirmations, model.score(plain), plaintext)
                compatible += 1
                candidate = {
                    "plaintext": hit.plaintext, "family": "vigenere",
                    "key": {"keyword": hit.key, "period": hit.period, "crib_offset": hit.offset},
                    "score": hit.score, "forward_consistent": True, "crib_match": True,
                    "evidence": {"supplied_crib": plain_crib, "repeated_confirmations": hit.checks,
                                 "all_key_slots_filled": True, "offset_supplied": False,
                                 "independent_correctness": False},
                }
                entry = (hit.score, -hit.period, -hit.offset, checks, candidate)
                if len(heap) < max_candidates:
                    heapq.heappush(heap, entry)
                elif entry[:4] > heap[0][:4]:
                    heapq.heapreplace(heap, entry)
        if checks >= max_checks:
            break
    complete = checks == total
    candidates = [row[4] for row in sorted(heap, reverse=True)]
    report = make_report(
        "detective", "unknown-offset repeated-key crib confirmation",
        candidates, checks, max_checks, complete, "complete" if complete else "check_limit",
        [{"tool": "bounded_vigenere_crib", "checks": checks, "models_requested": total,
          "search_complete": complete}],
        ["Ordinary straight-alphabet Vigenere with period measured from message position zero",
         "Supplied crib letters are premises and their position is unknown",
         "Repeated crib confirmations are internal consistency, not held-out validation",
         "Letters outside the aligned crib are conditional on the repeating-key model"],
    )
    report.update(
        compatible_trials=compatible, candidates_truncated=compatible > len(candidates),
        bounds={"max_checks": max_checks, "max_candidates": max_candidates, "max_period": max_period,
                "eligible_periods": list(range(1, period_limit + 1)), "alignments_requested": alignments,
                "min_repeated_confirmations": min_checks, "total_declared_checks": total,
                "check_unit": "one crib alignment and period, including applicable forward replay",
                "completion_scope": "all offsets and eligible periods under the confirmation policy"},
        neural_advice={"status": "not_used", "candidates": [], "claimed_plaintext": None,
                       "reason": "This persona applies crib equations without neural inference"},
        ranking="summed repository English quadgram score, then shorter period and earlier offset; not correctness",
        scope=report["scope"] + " No uniqueness is inferred from a ranked or solitary crib match.",
    )
    return report


__all__ = ["investigate_detective"]
