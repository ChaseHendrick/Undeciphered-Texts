"""Connect complementary search policies under one work budget.

Agreement records shared candidates. It does not supply an independent
plaintext reference or rename the separate neural router.
"""
from __future__ import annotations

from collections.abc import Sequence
import importlib
import math
from engine.language import get_model
from engine.persona_solver_common import make_report, validate_inputs

PERSONAS = ("emperor", "inheritance", "hallucinogens", "pacifist", "detective",
            "cartographer", "mechanic", "normal-man", "adversary", "skeptic")


def _strategies():
    specifications = {name: ("engine.solvers.persona_" + name,"investigate_" + name)
                      for name in PERSONAS}
    specifications['emperor'] = ('engine.solvers.persona_court_notice','investigate_emperor')
    specifications['pacifist'] = ('engine.solvers.pacifist','investigate_pacifist')
    specifications['normal-man'] = ('engine.solvers.persona_normal_man','investigate_normal_man')
    def lazy(module, function):
        def run(text, **params):
            return getattr(importlib.import_module(module),function)(text,**params)
        return run
    return {name:lazy(*spec) for name,spec in specifications.items()}


def investigate_personas(text, *, cribs=(), lexicon=None, keywords=None,
                        max_checks=9000, max_candidates=20, max_rotations=8,
                        personas=None, unplaced_crib=None, verification_cribs=(),
                        expected_plaintext_sha256=None, proposed_plaintext=None):
    """Run systematic, clue-based and compositional search without hidden keys.

Each successive policy receives a share of the remaining work. Unspent work
is reallocated. Check units remain tool-specific bounded operations, not a
wall-clock guarantee. No claim of independent evidence follows from votes.
    """
    _, cribs, known = validate_inputs(text, cribs, max_checks, max_candidates)
    _, _, heldout = validate_inputs(text,verification_cribs,max_checks,max_candidates)
    if set(known) & set(heldout):
        raise ValueError("reserved verification cribs overlap training positions")
    if personas is None:
        selected = PERSONAS
    elif (not isinstance(personas, Sequence) or isinstance(personas,(str,bytes))
          or not 1 <= len(personas) <= len(PERSONAS)
          or any(not isinstance(name,str) or name not in PERSONAS for name in personas)
          or len(set(personas)) != len(personas)):
        raise ValueError("personas must be a nonempty finite sequence of distinct supported names")
    else:
        selected = tuple(personas)
    if "skeptic" in selected:
        selected = tuple(name for name in selected if name != "skeptic") + ("skeptic",)
    elif verification_cribs or expected_plaintext_sha256 is not None:
        raise ValueError("reserved verification evidence requires the Skeptic persona")
    if not isinstance(max_rotations, int) or isinstance(max_rotations, bool) or not 0 <= max_rotations <= 32:
        raise ValueError("max_rotations must be an integer in 0..32")
    strategies = _strategies()
    spent, reports, actions, merged = 0, {}, [], {}
    review_shortlist = None
    for index, persona in enumerate(selected):
        remaining = max_checks - spent
        allocation = (remaining + len(selected) - index - 1) // (len(selected) - index)
        params = dict(cribs=cribs, max_checks=allocation, max_candidates=max_candidates)
        if persona == "inheritance":
            params.update(lexicon=lexicon, keywords=keywords)
        elif persona == "hallucinogens":
            params["max_rotations"] = max_rotations
        elif persona == "adversary":
            params["candidate"] = proposed_plaintext
        elif persona == "skeptic":
            shortlist = sorted(merged.values(),key=lambda row:(-row['score'],row['plaintext']))[:max_candidates]
            review_shortlist = {row['plaintext'] for row in shortlist}
            params.update(candidate_plaintexts=[row['plaintext'] for row in shortlist],
                          verification_cribs=verification_cribs,
                          expected_plaintext_sha256=expected_plaintext_sha256)
        elif persona == "detective":
            params.pop("cribs")
            params["crib"] = unplaced_crib or (max(cribs,key=lambda entry:len(entry.plaintext)).plaintext if cribs else None)
        if persona == "detective" and params["crib"] is None:
            report = make_report(persona,"unplaced crib alignment search",[],0,allocation,
                False,"missing_crib",[],["Detective requires a supplied unplaced crib."])
        else:
            report = strategies[persona](text, **params)
        checks = report.get("checks")
        if not isinstance(checks, int) or isinstance(checks, bool) or not 0 <= checks <= allocation:
            raise RuntimeError("persona backend violated its work allocation")
        spent += checks
        reports[persona] = report
        actions.append({"persona": persona, "allocated_checks": allocation,
                        "executed_checks": checks, "stop_reason": report.get("stop_reason")})
        for candidate in report["candidates"]:
            if not candidate.get("forward_consistent") or not candidate.get("crib_match"):
                raise RuntimeError("persona backend retained an unchecked candidate")
            plain, score = candidate["plaintext"], candidate["score"]
            if not isinstance(plain, str) or not isinstance(score, (int, float)) or isinstance(score, bool) or not math.isfinite(score):
                raise RuntimeError("persona backend returned malformed candidate data")
            if any(position >= len(plain) or plain[position] != letter for position,letter in known.items()):
                # Detective may search a supplied crib at other offsets.
                # The council still enforces all original aligned premises.
                continue
            if persona == 'detective':
                offset = candidate['key']['crib_offset']
                fitted = range(offset,offset + len(candidate['evidence']['supplied_crib']))
                if set(fitted) & set(heldout):
                    raise ValueError("reserved verification cribs overlap Detective fit positions")
            # Backends may use sum/mean scores or no semantic score at all.
            # Compare every merged plaintext with one shared language model.
            score = get_model().score([ord(ch) - 65 for ch in plain if "A" <= ch <= "Z"])
            witness = {"persona": persona, "family": candidate["family"],
                       "key": candidate["key"], "evidence": candidate["evidence"],
                       "backend_score": candidate["score"]}
            if plain not in merged:
                merged[plain] = {**candidate, "score": score, "supporting_personas": [], "witnesses": []}
            combined = merged[plain]
            combined["score"] = max(combined["score"], score)
            if persona not in combined["supporting_personas"]:
                combined["supporting_personas"].append(persona)
            if len(combined["witnesses"]) < 12:
                combined["witnesses"].append(witness)
    if review_shortlist is not None:
        # Never backfill a rejected finalist with an unreviewed lower candidate.
        merged = {plain:row for plain,row in merged.items() if plain in review_shortlist}
    reviews = {row['plaintext']:row for row in reports.get('skeptic',{}).get('reviews',[])}
    rejected=[]
    for plain,review in reviews.items():
        if plain not in merged:
            continue
        merged[plain]['skeptic_review']=review
        if review['status'] in ('contradicted','rejected'):
            rejected.append(merged.pop(plain))
    if review_shortlist is not None:
        for plain,row in merged.items():
            if plain not in reviews:
                row['skeptic_review'] = {'status':'unreviewed','reason':'review budget exhausted',
                                        'historical_correctness_verified':False}
    candidates = sorted(merged.values(), key=lambda row: (-row["score"], row["plaintext"]))[:max_candidates]
    complete = all(report["search_complete"] for report in reports.values())
    result = make_report("council", "complementary systematic, clue-based and compositional search",
                         candidates, spent, max_checks, complete,
                         "complete_within_declared_models" if complete else "incomplete_or_missing_evidence",
                         actions, ["Caller clues are not independently authenticated.",
                                   "Agreement between strategies is not independent evidence.",
                                   "Shared English scores rank examples rather than verify plaintext."])
    result.update(persona_reports=reports, selected_personas=list(selected),
                  agreement_is_independent_evidence=False, contradicted_candidates=rejected,
                  neural_advice=reports.get('emperor',{}).get('neural_advice',{'status':'not_used','candidates':[]}),
                  ranking='one shared English quadgram score, independent of backend score units',
                  candidate_count_before_cap=len(merged), retained_candidates=len(candidates),
                  bounds={"max_checks": max_checks, "max_candidates": max_candidates,
                          "max_rotations": max_rotations, "max_letters": 512})
    return result


__all__ = ["investigate_personas", "PERSONAS"]
