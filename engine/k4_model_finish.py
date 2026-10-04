"""Finish the finite K4 composition space left partial on 2026-10-03.

Each call searches one substitution family under both fixed alphabets, both
composition orders, periods 1 through 32, and layouts through width 32.
One family is 8128 hypotheses, which fits under the 10000 check cap.
Four families times two crib folds are eight searches.

The reserved crib is not passed to search. Afterwards each returned candidate
is compared with that reserved word. A reserved exact prediction requires
every reserved letter to be present and equal, and a complete key with no
unknown slots. A question mark is not a match. Determined mismatches are
contradictions and are counted, not dropped.

No historical plaintext is claimed. claimed_plaintext stays None. solved
stays false. A crib fit is not a decipherment.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

from engine.k4_models import AZ, FAMILIES, KRYPTOS_MIXED, ORDERS, search_k4_models
from engine.reverse_engineer import Crib
from engine.solvers.k4_attempt import K4_CIPHERTEXT

CIPHERTEXT_SHA256 = "eea813570c7f1fd3b34674e47b5c3da8948026f5cefee612a0b38ffaa515ceab"
EAST = Crib(21, "EASTNORTHEAST")
BERLIN = Crib(63, "BERLINCLOCK")
EAST_CIPHER_SPAN = "FLRVQQPRNGKSS"
BERLIN_CIPHER_SPAN = "NYPVTTMZFPK"
FOLDS = (
    ("A", EAST, BERLIN),
    ("B", BERLIN, EAST),
)
FAMILY_HYPOTHESES = 8128
FOLD_HYPOTHESES = 32512
MAX_CHECKS = 10000
MAX_PERIOD = 32
MAX_WIDTH = 32
MAX_CANDIDATES = 10000

_CLASS_KEYS = (
    "contradiction",
    "underdetermined",
    "incomplete_span_match",
    "exact",
)


def _lock_transcription(ciphertext: str) -> None:
    if len(ciphertext) != 97:
        raise RuntimeError("K4 ciphertext must be 97 letters")
    if ciphertext[EAST.offset:EAST.offset + len(EAST_CIPHER_SPAN)] != EAST_CIPHER_SPAN:
        raise RuntimeError("EASTNORTHEAST ciphertext span does not match the frozen transcription")
    if ciphertext[BERLIN.offset:BERLIN.offset + len(BERLIN_CIPHER_SPAN)] != BERLIN_CIPHER_SPAN:
        raise RuntimeError("BERLINCLOCK ciphertext span does not match the frozen transcription")
    digest = hashlib.sha256(ciphertext.encode("ascii")).hexdigest()
    if digest != CIPHERTEXT_SHA256:
        raise RuntimeError("K4 ciphertext SHA-256 does not match the frozen transcription")


def _complete_key(candidate: dict) -> tuple[bool, bool]:
    """Return (complete, flag_matches_slots).

    A complete key has key_complete true and no unknown shift slots.
    """
    slots = candidate["key_shift_indices"]
    flag = candidate["key_complete"] is True
    slots_full = all(slot is not None for slot in slots)
    return flag and slots_full, flag == slots_full


def classify_reserved(candidate: dict, reserved: Crib) -> str:
    """Classify one candidate against a reserved crib that was not fitted.

    exact: every reserved letter is present and equal, and the key is complete.
    incomplete_span_match: those letters are present and equal, but the key is not.
    contradiction: at least one determined letter disagrees. Unknown letters
    do not erase a determined mismatch.
    underdetermined: no determined mismatch, and at least one reserved letter
    is still '?'. Question marks are not matches.
    """
    word = reserved.plaintext
    predicted = candidate["predicted_plaintext"]
    if not isinstance(predicted, str):
        return "contradiction"
    stop = reserved.offset + len(word)
    if reserved.offset < 0 or stop > len(predicted):
        return "contradiction"
    span = predicted[reserved.offset:stop]
    mismatches = 0
    unknowns = 0
    for got, expected in zip(span, word):
        if got == "?":
            unknowns += 1
        elif got != expected:
            mismatches += 1
    if mismatches:
        return "contradiction"
    if unknowns or len(span) != len(word):
        return "underdetermined"
    complete, _agree = _complete_key(candidate)
    if complete:
        return "exact"
    return "incomplete_span_match"


def _unverified_agreement(candidate: dict, fold: str, fitted: Crib, reserved: Crib) -> dict:
    """Model fields for a reserved exact prediction. Not a decipherment."""
    return {
        "verification": "unverified",
        "plaintext_label": "unverified crib agreement, not a solve",
        "claimed_plaintext": None,
        "solved": False,
        "fold": fold,
        "fitted_crib": {"offset": fitted.offset, "plaintext": fitted.plaintext},
        "reserved_crib": {"offset": reserved.offset, "plaintext": reserved.plaintext},
        "family": candidate["family"],
        "period": candidate["period"],
        "order": candidate["order"],
        "layout": dict(candidate["layout"]),
        "alphabet": candidate["alphabet"],
        "key_shift_indices": list(candidate["key_shift_indices"]),
        "key_complete": True,
        "unverified_predicted_plaintext": candidate["predicted_plaintext"],
        "re_encryption_matches": candidate["re_encryption_matches"],
        "replay_note": "Forward replay checks transform consistency only. It is not historical verification.",
    }


def _search_family(fold: str, family: str, fitted: Crib, reserved: Crib) -> tuple[dict, list[dict]]:
    started = time.perf_counter()
    result = search_k4_models(
        K4_CIPHERTEXT,
        cribs=(fitted,),
        families=(family,),
        alphabets=(AZ, KRYPTOS_MIXED),
        orders=ORDERS,
        max_checks=MAX_CHECKS,
        max_period=MAX_PERIOD,
        max_width=MAX_WIDTH,
        max_candidates=MAX_CANDIDATES,
    )
    if result["claimed_plaintext"] is not None:
        raise RuntimeError("search_k4_models returned a claimed plaintext")
    counts = {key: 0 for key in _CLASS_KEYS}
    complete_keys = 0
    complete_contradictions = 0
    complete_underdetermined = 0
    flag_disagreements = 0
    agreements = []
    for candidate in result["candidates"]:
        if candidate["claimed_plaintext"] is not None:
            raise RuntimeError("a candidate carried a claimed plaintext")
        kind = classify_reserved(candidate, reserved)
        counts[kind] += 1
        complete, flags_agree = _complete_key(candidate)
        if complete:
            complete_keys += 1
            if kind == "contradiction":
                complete_contradictions += 1
            elif kind == "underdetermined":
                complete_underdetermined += 1
            elif kind != "exact":
                raise RuntimeError("complete key had an unexpected reserved class")
        if not flags_agree:
            flag_disagreements += 1
        if kind == "exact":
            agreements.append(_unverified_agreement(candidate, fold, fitted, reserved))
    evaluated = sum(counts.values())
    if evaluated != len(result["candidates"]):
        raise RuntimeError("reserved classification dropped a returned candidate")
    call = {
        "fold": fold,
        "family": family,
        "fitted_crib": {"offset": fitted.offset, "plaintext": fitted.plaintext},
        "reserved_crib": {"offset": reserved.offset, "plaintext": reserved.plaintext},
        "reserved_crib_passed_to_search": False,
        "checks": result["checks"],
        "requested_models": result["requested_models"],
        "search_complete": result["search_complete"],
        "stop_reason": result["stop_reason"],
        "compatible_models": result["compatible_models"],
        "rejected_models": result["rejected_models"],
        "candidates_returned": len(result["candidates"]),
        "candidates_truncated": result["candidates_truncated"],
        "reserved_counts_cover_returned_candidates": True,
        "complete_keys": complete_keys,
        "complete_key_reserved_contradictions": complete_contradictions,
        "complete_key_reserved_underdetermined": complete_underdetermined,
        "reserved_contradictions": counts["contradiction"],
        "reserved_underdetermined": counts["underdetermined"],
        "reserved_span_matches_incomplete_key": counts["incomplete_span_match"],
        "reserved_exact_predictions": counts["exact"],
        "key_complete_flag_disagrees_with_slots": flag_disagreements,
        "elapsed_seconds": round(time.perf_counter() - started, 6),
    }
    return call, agreements


def finish_k4_models(*, progress: bool = False) -> dict:
    """Run four families on both reserved-crib folds and return the counts.

    This is the full finite family space from the 3 October experiment.
    It does not claim a historical plaintext.
    """
    _lock_transcription(K4_CIPHERTEXT)
    started = time.perf_counter()
    checks_per_call = []
    agreements = []
    for fold, fitted, reserved in FOLDS:
        for family in FAMILIES:
            call, found = _search_family(fold, family, fitted, reserved)
            checks_per_call.append(call)
            agreements.extend(found)
            if progress:
                print(
                    f"fold {fold} {family}: checks={call['checks']} "
                    f"complete={call['search_complete']} "
                    f"compatible={call['compatible_models']} "
                    f"contradictions={call['reserved_contradictions']} "
                    f"exact={call['reserved_exact_predictions']}",
                    file=sys.stderr,
                )
    incomplete = [
        {
            "fold": call["fold"],
            "family": call["family"],
            "checks": call["checks"],
            "requested_models": call["requested_models"],
            "search_complete": False,
            "stop_reason": call["stop_reason"],
        }
        for call in checks_per_call
        if not call["search_complete"]
    ]
    truncated = [
        {"fold": call["fold"], "family": call["family"], "candidates_returned": call["candidates_returned"],
         "compatible_models": call["compatible_models"]}
        for call in checks_per_call
        if call["candidates_truncated"]
    ]

    def _sum(field: str) -> int:
        return sum(call[field] for call in checks_per_call)

    exact_count = _sum("reserved_exact_predictions")
    if exact_count != len(agreements):
        raise RuntimeError("reserved exact predictions were dropped from the agreement list")
    if _sum("complete_keys") != (
        _sum("complete_key_reserved_contradictions")
        + _sum("complete_key_reserved_underdetermined")
        + exact_count
    ):
        raise RuntimeError("complete keys were not fully classified against the reserved crib")
    report = {
        "schema_version": 1,
        "experiment": "K4 finite family completion of the 2026-10-03 partial model space",
        "date": "2026-10-04",
        "status": "not_solved",
        "solved": False,
        "claimed_plaintext": None,
        "new_verified_plaintext": False,
        "ciphertext": K4_CIPHERTEXT,
        "ciphertext_length": len(K4_CIPHERTEXT),
        "ciphertext_sha256": CIPHERTEXT_SHA256,
        "coordinates": "Zero-based original plaintext letter positions, before any tested transposition.",
        "fitted_and_reserved": [
            {
                "fold": fold,
                "fitted_crib": {"offset": fitted.offset, "plaintext": fitted.plaintext},
                "reserved_crib": {"offset": reserved.offset, "plaintext": reserved.plaintext},
                "reserved_crib_passed_to_search": False,
            }
            for fold, fitted, reserved in FOLDS
        ],
        "hypothesis_space": {
            "per_family": FAMILY_HYPOTHESES,
            "per_fold": FOLD_HYPOTHESES,
            "families": list(FAMILIES),
            "alphabets": [AZ, KRYPTOS_MIXED],
            "orders": list(ORDERS),
            "max_period": MAX_PERIOD,
            "max_width": MAX_WIDTH,
            "max_checks_per_call": MAX_CHECKS,
            "max_candidates_per_call": MAX_CANDIDATES,
            "calls": len(FAMILIES) * len(FOLDS),
        },
        "checks_per_call": checks_per_call,
        "search_complete": all(call["search_complete"] for call in checks_per_call),
        "incomplete_searches": incomplete,
        "truncated_candidate_lists": truncated,
        "compatible_counts": {
            "per_call": [
                {
                    "fold": call["fold"],
                    "family": call["family"],
                    "compatible_models": call["compatible_models"],
                    "rejected_models": call["rejected_models"],
                    "complete_keys": call["complete_keys"],
                }
                for call in checks_per_call
            ],
            "total": _sum("compatible_models"),
        },
        "reserved_exact_prediction_count": exact_count,
        "reserved_contradiction_count": _sum("reserved_contradictions"),
        "reserved_underdetermined_count": _sum("reserved_underdetermined"),
        "reserved_span_matches_incomplete_key_count": _sum("reserved_span_matches_incomplete_key"),
        "complete_key_count": _sum("complete_keys"),
        "complete_key_reserved_contradictions": _sum("complete_key_reserved_contradictions"),
        "complete_key_reserved_underdetermined": _sum("complete_key_reserved_underdetermined"),
        "key_complete_flag_disagrees_with_slots": _sum("key_complete_flag_disagrees_with_slots"),
        "unverified_crib_agreements": agreements,
        "totals": {
            "calls": len(checks_per_call),
            "checks": _sum("checks"),
            "compatible_models": _sum("compatible_models"),
            "rejected_models": _sum("rejected_models"),
            "complete_keys": _sum("complete_keys"),
            "complete_key_reserved_contradictions": _sum("complete_key_reserved_contradictions"),
            "complete_key_reserved_underdetermined": _sum("complete_key_reserved_underdetermined"),
            "reserved_contradictions": _sum("reserved_contradictions"),
            "reserved_underdetermined": _sum("reserved_underdetermined"),
            "reserved_span_matches_incomplete_key": _sum("reserved_span_matches_incomplete_key"),
            "reserved_exact_predictions": exact_count,
        },
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "scope": (
            "Eight searches cover the declared families, two alphabets, two orders, "
            "periods 1 through 32, and the distinct layouts through width 32, once per fold. "
            "Search completion is coverage of that finite hypothesis list, not a unique key "
            "and not a historical plaintext. Free completions of an incomplete key are not "
            "enumerated. Contradictions on the reserved crib are counted. A crib fit is not "
            "a decipherment."
        ),
    }
    if report["claimed_plaintext"] is not None or report["solved"] is not False:
        raise RuntimeError("finish report must not claim a plaintext")
    for agreement in report["unverified_crib_agreements"]:
        if agreement["claimed_plaintext"] is not None or agreement["solved"] is not False:
            raise RuntimeError("an unverified agreement was marked solved")
        if agreement["verification"] != "unverified":
            raise RuntimeError("a reserved exact prediction was not labeled unverified")
    return report


def render_model_finish_markdown(report: dict) -> str:
    """Summarize finish_k4_models counts. No historical plaintext is claimed."""

    def comma(value: int) -> str:
        return f"{value:,}"

    lines = [
        "# K4 finite model space finish, 4 October 2026",
        "",
        "**No historical plaintext is claimed.** This run finishes the family space left partial by the [3 October 2026 model experiment](model-experiments-2026-10-03.md). `claimed_plaintext` is null and `solved` is false. A crib fit is not a decipherment.",
        "",
        "The machine-readable record is [model-finish-2026-10-04.json](model-finish-2026-10-04.json).",
        "",
        "## What was searched",
        "",
        f"The ciphertext is the 97-letter `K4_CIPHERTEXT` constant in `engine/solvers/k4_attempt.py`. Its ASCII SHA-256 is `{report['ciphertext_sha256']}`.",
        "",
        "Each call uses one family, alphabets A-Z and `KRYPTOSABCDEFGHIJLMNQUVWXZ`, orders substitute-then-transpose and transpose-then-substitute, `max_period=32`, `max_width=32`, `max_checks=10000`, and `max_candidates=10000`. One family is 8,128 hypotheses, so it finishes under the check cap. Four families are the 32,512 hypotheses of one fold. Two folds make eight searches.",
        "",
        "Fold A fits only EASTNORTHEAST at offset 21 and afterwards checks BERLINCLOCK at offset 63. Fold B fits only BERLINCLOCK at offset 63 and afterwards checks EASTNORTHEAST at offset 21. The reserved word is not passed into search. Comparison uses original plaintext coordinates. A question mark is not a match. A determined mismatch is a contradiction and is counted; those candidates are not dropped.",
        "",
        "A reserved exact prediction means every letter of the reserved word is present and equal, and the candidate has a complete key (`key_complete` true and no unknown key slots). A full reserved-span match with an incomplete key is counted separately. It is not an exact prediction and not a solve.",
        "",
        "## Counts",
        "",
        "| Fold | Family | Checks | Search complete | Compatible | Complete keys | Reserved contradictions | Underdetermined | Incomplete span matches | Reserved exact predictions |",
        "| --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for call in report["checks_per_call"]:
        lines.append(
            "| {fold} | {family} | {checks} | {complete} | {compatible} | {keys} | {contra} | {under} | {span} | {exact} |".format(
                fold=call["fold"],
                family=call["family"],
                checks=comma(call["checks"]),
                complete="yes" if call["search_complete"] else "no",
                compatible=comma(call["compatible_models"]),
                keys=comma(call["complete_keys"]),
                contra=comma(call["reserved_contradictions"]),
                under=comma(call["reserved_underdetermined"]),
                span=comma(call["reserved_span_matches_incomplete_key"]),
                exact=comma(call["reserved_exact_predictions"]),
            )
        )
    totals = report["totals"]
    lines.append(
        "| both | all | {checks} | {complete} | {compatible} | {keys} | {contra} | {under} | {span} | {exact} |".format(
            checks=comma(totals["checks"]),
            complete="yes" if report["search_complete"] else "no",
            compatible=comma(totals["compatible_models"]),
            keys=comma(totals["complete_keys"]),
            contra=comma(totals["reserved_contradictions"]),
            under=comma(totals["reserved_underdetermined"]),
            span=comma(totals["reserved_span_matches_incomplete_key"]),
            exact=comma(totals["reserved_exact_predictions"]),
        )
    )
    lines.extend([
        "",
        f"Checks per call are in the JSON `checks_per_call` list. Compatible models total {comma(report['compatible_counts']['total'])}. Reserved contradictions total {comma(report['reserved_contradiction_count'])}. Reserved exact predictions total {comma(report['reserved_exact_prediction_count'])}.",
        "",
        "## Result",
        "",
    ])
    evaluated_all = not report["incomplete_searches"] and not report["truncated_candidate_lists"]
    if not evaluated_all:
        lines.append("The family space was not fully evaluated.")
        lines.append("")
        for item in report["incomplete_searches"]:
            lines.append(
                f"- Search incomplete: fold {item['fold']}, family {item['family']}, "
                f"checks {comma(item['checks'])} of {comma(item['requested_models'])} "
                f"({item['stop_reason']})."
            )
        for item in report["truncated_candidate_lists"]:
            lines.append(
                f"- Candidate list truncated: fold {item['fold']}, family {item['family']}, "
                f"returned {comma(item['candidates_returned'])} of {comma(item['compatible_models'])} compatible models. "
                "Reserved counts for that call do not cover every compatible model."
            )
        lines.append("")
    else:
        per_call = {call["checks"] for call in report["checks_per_call"]}
        requested = {call["requested_models"] for call in report["checks_per_call"]}
        if per_call == requested == {FAMILY_HYPOTHESES} and totals["checks"] == FAMILY_HYPOTHESES * 8:
            lines.append(
                "Every call returned `search_complete` true. Each call used "
                f"{comma(FAMILY_HYPOTHESES)} checks, matching its requested model count. "
                f"Eight calls used {comma(totals['checks'])} checks. "
                "That is one full 32,512-hypothesis fold for EASTNORTHEAST and one full fold for BERLINCLOCK."
            )
        else:
            lines.append(
                "Every call returned `search_complete` true. "
                f"Eight calls used {comma(totals['checks'])} checks. "
                "Per-call checks are in the table above."
            )
        lines.append("")
    exact = report["reserved_exact_prediction_count"]
    if exact == 0 and evaluated_all:
        lines.append(
            "The completed family space produced no reserved exact predictions. "
            "No model with a complete key predicted the reserved word at its public offset."
        )
    elif exact == 0:
        lines.append(
            "No reserved exact prediction was found among the candidates that were evaluated. "
            "That is not a completed-space result."
        )
    else:
        lines.append(
            f"The search recorded {comma(exact)} reserved exact prediction"
            f"{'s' if exact != 1 else ''}. "
            "Each one below is an unverified crib agreement, not a solve. "
            "No historical plaintext is claimed."
        )
        if not evaluated_all:
            lines.append("")
            lines.append("These agreements are only from the candidates that were returned.")
        lines.append("")
        for index, item in enumerate(report["unverified_crib_agreements"], 1):
            layout = item["layout"]
            lines.extend([
                f"### Unverified crib agreement {index}",
                "",
                "Not a solve. `verification` is `unverified`. `claimed_plaintext` is null.",
                "",
                f"- fold: {item['fold']}",
                f"- fitted crib: {item['fitted_crib']['plaintext']} at offset {item['fitted_crib']['offset']}",
                f"- reserved crib: {item['reserved_crib']['plaintext']} at offset {item['reserved_crib']['offset']}",
                f"- family: {item['family']}",
                f"- period: {item['period']}",
                f"- order: {item['order']}",
                f"- layout: `{json.dumps(layout, sort_keys=True)}`",
                f"- alphabet: `{item['alphabet']}`",
                f"- key_complete: true",
                f"- key_shift_indices: `{json.dumps(item['key_shift_indices'])}`",
                f"- re_encryption_matches: {json.dumps(item['re_encryption_matches'])}",
                f"- unverified predicted plaintext: `{item['unverified_predicted_plaintext']}`",
                "",
            ])
    incomplete_spans = report["reserved_span_matches_incomplete_key_count"]
    complete_keys = report["complete_key_count"]
    complete_contradictions = report["complete_key_reserved_contradictions"]
    complete_unknown = report["complete_key_reserved_underdetermined"]
    accounted = complete_contradictions + complete_unknown + exact
    if accounted == complete_keys and complete_unknown == 0 and exact == 0:
        complete_sentence = (
            f"Complete keys: {comma(complete_keys)}. "
            f"All {comma(complete_keys)} contradicted the reserved crib. "
            "None left a reserved letter unknown, and none was a reserved exact prediction."
        )
    elif accounted == complete_keys:
        complete_sentence = (
            f"Complete keys: {comma(complete_keys)}. "
            f"{comma(complete_contradictions)} contradicted the reserved crib, "
            f"{comma(complete_unknown)} left a reserved letter unknown, "
            f"and {comma(exact)} were reserved exact predictions."
        )
    else:
        complete_sentence = (
            f"Complete keys: {comma(complete_keys)}. "
            f"Reserved classes account for {comma(accounted)}, which does not match that count."
        )
    if incomplete_spans == 0:
        span_sentence = (
            f"Incomplete-key reserved span matches: {comma(incomplete_spans)}. "
            "No compatible model spelled the full reserved word while leaving a key slot unknown."
        )
    else:
        span_sentence = (
            f"Incomplete-key reserved span matches: {comma(incomplete_spans)}. "
            "Those candidates spell the reserved word in full, but at least one key slot is unknown, "
            "so they are not reserved exact predictions."
        )
    lines.extend([
        "",
        complete_sentence,
        "",
        span_sentence,
        "",
        f"Underdetermined reserved comparisons: {comma(report['reserved_underdetermined_count'])}. "
        "At least one reserved letter stayed unknown, and no determined letter disagreed.",
        "",
        "Completing an unknown key slot from the reserved letters would change the experiment and remove that group's heldout role. This run does not do that.",
        "",
        "Coverage of this finite list is not a unique key and not a historical reading. Other alphabets, arbitrary column permutations, extra layers, transcription edits, and other mechanisms stay outside this space. The 3 October run stopped at `check_limit` after 4,916 checks per fold. Where this record shows `search_complete` true, those previously untested combinations in the same family list were included.",
        "",
        "No historical plaintext is claimed.",
        "",
    ])
    text = "\n".join(lines)
    if "\u2014" in text or "\u2013" in text:
        raise RuntimeError("summary used a forbidden dash character")
    return text


def write_model_finish_records(report: dict, root: Path | None = None) -> tuple[Path, Path]:
    """Write the result dict and the count summary next to the October 3 record."""
    base = Path(__file__).resolve().parents[1] if root is None else root
    folder = base / "docs" / "k4-focus"
    json_path = folder / "model-finish-2026-10-04.json"
    md_path = folder / "model-finish-2026-10-04.md"
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_model_finish_markdown(report), encoding="utf-8")
    return json_path, md_path


def main() -> None:
    report = finish_k4_models(progress=True)
    json_path, md_path = write_model_finish_records(report)
    print(json.dumps({
        "solved": report["solved"],
        "claimed_plaintext": report["claimed_plaintext"],
        "search_complete": report["search_complete"],
        "checks": report["totals"]["checks"],
        "compatible_models": report["totals"]["compatible_models"],
        "reserved_contradictions": report["totals"]["reserved_contradictions"],
        "reserved_exact_predictions": report["totals"]["reserved_exact_predictions"],
        "incomplete_searches": report["incomplete_searches"],
        "json": str(json_path),
        "markdown": str(md_path),
    }, indent=2))


if __name__ == "__main__":
    main()
