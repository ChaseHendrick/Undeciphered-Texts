"""Bounded investigative planning around existing, separately tested tools.

The ledger exposes program facts and a plan, not private thought or conscious
emotion. Scores guide candidate review. Neither score nor forward consistency
establishes a historical solution or supplies independent correctness evidence.
"""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import asdict, dataclass
import importlib
import json
import math
from time import monotonic

from engine.language import get_model
from engine.reverse_engineer import Crib, infer_cipher_models
from engine.solvers.affine import affine_decrypt, affine_encrypt
from engine.solvers.morbit import _MORSE, morbit_encrypt
from engine.solvers.morse_constraints import MorseCrib, search_morse_constraints
from engine.solvers.pollux import pollux_encrypt
from engine.transposition_ensemble import search_transposition_ensemble

OBJECTIVE = "seek independently verifiable solutions to unresolved ciphers"
SCOPE = (
    "Repository-specific investigative composition of bounded known cipher models. "
    "Supplied constraints, English scores, neural family advice, and re-encryption "
    "do not independently verify a decipherment. No unknown-script reading or "
    "solution to army message Nr. 86 is claimed."
)
MAX_SYMBOLS = 512
MULTIPLIERS = (1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25)
LATIN_COORDINATES = "zero-based A-Z plaintext letters after removing spaces and punctuation"
MORSE_COORDINATES = "zero-based uppercase decoded characters including word spaces and punctuation"


def _integer(value, name: str, low: int, high: int) -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an integer")
    if not low <= value <= high:
        raise ValueError(f"{name} must be in {low}..{high}")


def score_reward(correct: int, total: int, checks: int, budget: int) -> float | None:
    """Reward supplied independent evaluation counts, never plausibility.

    Unknown correctness returns None. Any checked error earns zero. Passing
    every supplied case earns 0.9..1.0, with efficiency only a tie-breaker.
    This function trusts the caller to supply genuinely independent cases.
    """
    for name, value in (("correct", correct), ("total", total), ("checks", checks), ("budget", budget)):
        _integer(value, name, 0, 10**12)
    if correct > total or checks > budget:
        raise ValueError("correct cannot exceed total and checks cannot exceed budget")
    if total == 0:
        return None
    if correct != total:
        return 0.0
    return 0.9 + 0.1 * (1 - checks / budget if budget else 1.0)


def evaluation_policy(correct: int, total: int, *, min_cases: int = 20,
                      min_accuracy: float = 0.8, max_failures: int = 5) -> dict:
    """Suggest demotion only from adequate, independently checked cases.

    A model rejection, an unresolved cipher, or unverified candidate is not an
    incorrect evaluation case. Eligibility is unknown until min_cases is met.
    """
    _integer(correct, "correct", 0, 10**12)
    _integer(total, "total", 0, 10**12)
    _integer(min_cases, "min_cases", 1, 10**12)
    _integer(max_failures, "max_failures", 1, 10**12)
    if correct > total:
        raise ValueError("correct cannot exceed total")
    if (not isinstance(min_accuracy, (int, float)) or isinstance(min_accuracy, bool)
            or not math.isfinite(min_accuracy) or not 0 <= min_accuracy <= 1):
        raise ValueError("min_accuracy must be finite and in 0..1")
    failures = total - correct
    accuracy = correct / total if total else None
    adequate = total >= min_cases
    eligible = (accuracy >= min_accuracy and failures < max_failures) if adequate else None
    return {"independent_cases": total, "correct": correct if total else None,
            "failures": failures if total else None, "accuracy": accuracy,
            "eligible": eligible,
            "recommendation": "collect_independent_cases" if not adequate else "continue" if eligible else "retire_or_demote",
            "policy": {"min_cases": min_cases, "min_accuracy": min_accuracy, "max_failures": max_failures},
            "scope": "Caller-supplied independent evaluations only; unresolved searches do not count as wrong answers."}


def _input(text: str) -> tuple[str, str]:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not text or len(text) > 4096:
        raise ValueError("text must contain 1..4096 raw characters")
    if any(ch.isalnum() and not ch.isascii() for ch in text):
        raise ValueError("unsupported alphabet; this tool accepts ASCII Latin letters or digit ciphertext")
    letters = "".join(ch.upper() for ch in text if ch.isascii() and ch.isalpha())
    digits = "".join(ch for ch in text if "0" <= ch <= "9")
    if letters and digits:
        raise ValueError("mixed letters and digits require an explicit cipher-specific framing model")
    if letters:
        if not 4 <= len(letters) <= MAX_SYMBOLS:
            raise ValueError(f"Latin ciphertext must contain 4..{MAX_SYMBOLS} letters")
        return "latin", letters
    framed = text.strip()
    if framed.endswith("."):
        framed = framed[:-1]
    if not digits or len(digits) > MAX_SYMBOLS or any(not (ch.isspace() or "0" <= ch <= "9") for ch in framed):
        raise ValueError(f"numeric ciphertext must contain 1..{MAX_SYMBOLS} digits, whitespace, and at most one final framing period")
    return "numeric", digits


def _lexicon(value: Sequence[str] | None) -> tuple[str, ...] | None:
    if value is None:
        return None
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise TypeError("lexicon must be a finite sequence of ASCII words")
    if not 1 <= len(value) <= 10000:
        raise ValueError("lexicon must contain 1..10000 entries")
    if any(not isinstance(word, str) or not 1 <= len(word) <= 256
           or any(not (ch.isascii() and ch.isalpha()) for ch in word) for word in value):
        raise ValueError("lexicon entries must be single ASCII words of 1..256 letters")
    return tuple(dict.fromkeys(word.upper() for word in value))


def _constraints(cribs: Sequence[Crib], kind: str, length: int) -> tuple[tuple[Crib, ...], dict[int, str], list[dict]]:
    if not isinstance(cribs, Sequence) or isinstance(cribs, (str, bytes, bytearray)):
        raise TypeError("cribs must be a finite sequence of Crib objects")
    if len(cribs) > 128:
        raise ValueError("at most 128 cribs are accepted")
    normalized, known, conflicts = [], {}, []
    maximum = length if kind == "latin" else 2 * length
    for crib in cribs:
        if not isinstance(crib, Crib):
            raise TypeError("each crib must be an engine.reverse_engineer.Crib")
        _integer(crib.offset, "crib offset", 0, maximum - 1)
        if not isinstance(crib.plaintext, str) or not 1 <= len(crib.plaintext) <= 4096:
            raise ValueError("crib plaintext must contain 1..4096 characters")
        if kind == "latin":
            if any(ch.isalpha() and not ch.isascii() or ch.isdigit() for ch in crib.plaintext):
                raise ValueError("Latin cribs must use ASCII letters and letter coordinates")
            plain = "".join(ch.upper() for ch in crib.plaintext if ch.isascii() and ch.isalpha())
        else:
            plain = crib.plaintext.upper()
            if any(ch != " " and ch not in _MORSE for ch in plain):
                raise ValueError("numeric cribs must use supported Morse characters and literal word spaces")
        if not plain or crib.offset + len(plain) > maximum:
            raise ValueError("crib exceeds the plaintext coordinate bound")
        normalized.append(Crib(crib.offset, plain))
        for position, character in enumerate(plain, crib.offset):
            if position in known and known[position] != character:
                conflicts.append({"kind": "overlapping_cribs", "position": position,
                                  "values": [known[position], character],
                                  "scope": "Contradiction between supplied premises, not proof about the cipher."})
            else:
                known[position] = character
    return tuple(normalized), known, conflicts


def _neural_advice(cipher: str, kind: str) -> dict:
    unavailable = {"status": "not_applicable", "candidates": [], "claimed_plaintext": None,
                   "scope": "Family advice is conditional on the trained corpus and does not validate plaintext."}
    if kind != "latin" or len(cipher) < 16:
        return {**unavailable, "reason": "The neural router requires at least 16 A-Z letters"}
    try:
        importlib.import_module("numpy")
    except ImportError:
        return {**unavailable, "status": "unavailable", "reason": "NumPy is unavailable"}
    try:
        router = importlib.import_module("engine.neural_router_v2")
        advice = router.route_probabilities(cipher)
        rows = advice["candidates"]
        if (not isinstance(rows, list) or not rows or any(not isinstance(row.get("family"), str)
                or not isinstance(row.get("probability"), (int, float)) or isinstance(row["probability"], bool)
                or not math.isfinite(row["probability"]) or not 0 <= row["probability"] <= 1 for row in rows)):
            raise ValueError("invalid family ranking")
        return {**advice, "status": "available"}
    except (ImportError, OSError, ValueError, KeyError, TypeError) as exc:
        return {**unavailable, "status": "unavailable", "reason": f"Neural router unavailable: {type(exc).__name__}: {exc}"}


@dataclass(frozen=True)
class InvestigationCandidate:
    family: str
    key: dict
    plaintext: str
    score: float
    neural_probability: float | None
    re_encryption_matches: bool
    constraints_match: bool

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class SolverReasoningReport:
    input_kind: str
    coordinate_system: str
    candidates: tuple[InvestigationCandidate, ...]
    hypotheses: tuple[dict, ...]
    checks: int
    consistency_checks: int
    search_complete: bool
    stop_reason: str
    elapsed_seconds: float
    bounds: dict
    neural_advice: dict
    premises: tuple[dict, ...]
    actions: tuple[dict, ...]
    results: tuple[dict, ...]
    contradictions: tuple[dict, ...]
    next_actions: tuple[dict, ...]
    simulated_affect: dict
    thought: dict
    evaluation: dict
    objective: str = OBJECTIVE
    correctness_known: bool = False
    happiness: None = None
    claimed_plaintext: None = None
    solved_status: str = "unverified"
    ranking: str = "English quadgram score, then available neural family probability as advice; neither is correctness"
    scope: str = SCOPE

    def to_dict(self) -> dict:
        return asdict(self)


def _forward_hypothesis(plain: str, family: str, key: dict) -> str:
    if family in ("caesar", "affine"):
        return affine_encrypt(plain, key["multiplier"], key["offset"])
    if family == "substitution":
        return "".join(key["mapping"][ch] for ch in plain)
    slots = key["key_slots"]
    if family == "vigenere":
        return "".join(chr(65 + (ord(ch) - 65 + slots[index % len(slots)]) % 26) for index, ch in enumerate(plain))
    return "".join(chr(65 + (slots[index % len(slots)] - ord(ch) + 65) % 26) for index, ch in enumerate(plain))


def investigate_cipher(text: str, *, cribs: Sequence[Crib] = (), lexicon: Sequence[str] | None = None,
                       max_checks: int = 5000, max_candidates: int = 20,
                       temperament: str = "balanced") -> SolverReasoningReport:
    """Generate constrained witnesses, a falsifiable ledger, and a review plan.

    Checks count tested keys or model settings, including applicable forward
    consistency comparisons. Neural feature inference is advisory overhead,
    measured in elapsed_seconds, not a cryptanalytic key check. Temperament
    only adjusts displayed simulated control states, never evidence or search.
    """
    start = monotonic()
    _integer(max_checks, "max_checks", 0, 100000)
    _integer(max_candidates, "max_candidates", 1, 100)
    if not isinstance(temperament, str) or temperament not in ("balanced", "curious", "cautious"):
        raise ValueError("temperament must be balanced, curious, or cautious")
    kind, cipher = _input(text)
    words = _lexicon(lexicon)
    normalized, known, contradictions = _constraints(cribs, kind, len(cipher))
    coordinates = LATIN_COORDINATES if kind == "latin" else MORSE_COORDINATES
    advice = _neural_advice(cipher, kind) if not contradictions else {"status": "not_applicable", "candidates": [], "reason": "Supplied cribs contradict one another"}
    priors = {row["family"]: row["probability"] for row in advice["candidates"]}
    premises = [{"kind": "input", "alphabet": kind, "symbols": len(cipher), "coordinates": coordinates},
                {"kind": "constraints", "known_positions": len(known), "lexicon_words": len(words) if words else None,
                 "independent_validation": False, "scope": "Supplied premises constrain the search and are not held-out evidence."},
                {"kind": "objective", "value": OBJECTIVE},
                {"kind": "neural_advice", "status": advice["status"], "validation_evidence": False}]
    actions, results, hypotheses, next_actions = [], [], [], []
    candidates: dict[tuple, InvestigationCandidate] = {}
    checks = consistency = mismatches = 0
    completed, stop_reason = [], "complete"
    model = None

    def add(family: str, key: dict, plain: str, matches: bool = True) -> None:
        nonlocal model
        if not matches or any(position >= len(plain) or plain[position] != letter for position, letter in known.items()):
            return
        letters = [ord(ch) - 65 for ch in plain if "A" <= ch <= "Z"]
        if model is None:
            model = get_model()
        score = model.score(letters) if letters else 0.0
        candidate = InvestigationCandidate(family, key, plain, score, priors.get(family), True, True)
        identity = (family, plain, json.dumps(key, sort_keys=True))
        candidates[identity] = candidate
        # Keep at most max_candidates per family before global ranking.
        peers = [(identity, value) for identity, value in candidates.items() if value.family == family]
        if len(peers) > max_candidates:
            worst = min(peers, key=lambda item: (item[1].score, item[1].plaintext, item[0]))
            del candidates[worst[0]]

    if contradictions:
        stop_reason = "constraint_conflict"
        completed.append(False)
        next_actions.append({"stage": "review_constraints", "reason": "Resolve conflicting supplied cribs before testing models"})
    elif kind == "latin":
        requested_period = min(16, len(cipher))
        if normalized and max_checks >= 315:
            period = min(requested_period, (max_checks - 313) // 2)
            inference = infer_cipher_models(cipher, cribs=normalized, max_period=period)
            checks += 313 + 2 * period
            completed.append(period == requested_period)
            actions.append({"tool": "infer_cipher_models", "checks": checks, "periods_tested": period,
                            "periods_requested": requested_period, "search_complete": period == requested_period,
                            "reason": "Aligned cribs permit falsifiable affine, substitution, Vigenere, and Beaufort models"})
            partial_count = 0
            for hypothesis in inference.hypotheses:
                if hypothesis.unresolved_parameters or "?" in hypothesis.predicted_plaintext:
                    partial_count += 1
                    if len(hypotheses) < max_candidates:
                        hypotheses.append(asdict(hypothesis))
                    continue
                consistency += 1
                key = hypothesis.parameters.copy()
                if hypothesis.family in ("vigenere", "beaufort"):
                    key["keyword"] = hypothesis.key
                match = _forward_hypothesis(hypothesis.predicted_plaintext, hypothesis.family, key) == cipher
                if match:
                    add(hypothesis.family, key, hypothesis.predicted_plaintext)
                else:
                    mismatches += 1
            results.append({"tool": "infer_cipher_models", "compatible_hypotheses": len(inference.hypotheses),
                            "partial_hypotheses": partial_count, "partial_hypotheses_retained": len(hypotheses),
                            "scope": "Unresolved parameters remain unknown; complete predictions remain conditional on the model."})
        else:
            examined = rejected = 0
            for multiplier in MULTIPLIERS:
                for offset in range(26):
                    if checks >= max_checks:
                        break
                    checks += 1
                    examined += 1
                    consistency += 1
                    plain = affine_decrypt(cipher, multiplier, offset)
                    if affine_encrypt(plain, multiplier, offset) != cipher:
                        mismatches += 1
                    elif any(plain[position] != character for position, character in known.items()):
                        rejected += 1
                    else:
                        add("caesar" if multiplier == 1 else "affine", {"multiplier": multiplier, "offset": offset}, plain)
                if checks >= max_checks:
                    break
            completed.append(examined == 312)
            actions.append({"tool": "affine_key_enumeration", "checks": examined, "models_requested": 312,
                            "search_complete": examined == 312, "reason": "Finite invertible affine keys include every Caesar shift"})
            results.append({"tool": "affine_key_enumeration", "crib_rejections": rejected})
            if normalized:
                completed.append(False)
                actions.append({"tool": "infer_cipher_models", "checks": 0, "search_complete": False,
                                "reason": "Remaining plan cannot reserve the minimum 315 model checks"})
        transpositions = search_transposition_ensemble(cipher, cribs=normalized,
                                                       max_checks=max_checks - checks, max_candidates=max_candidates)
        checks += transpositions.checks
        consistency += transpositions.checks
        mismatches += transpositions.re_encryption_mismatches
        completed.append(transpositions.search_complete)
        actions.append({"tool": "transposition_ensemble", "checks": transpositions.checks,
                        "models_requested": transpositions.total_checks, "search_complete": transpositions.search_complete,
                        "family_checks": transpositions.family_checks,
                        "reason": "Test alternative order-changing models against the same constraints"})
        results.append({"tool": "transposition_ensemble", "crib_rejections": transpositions.crib_rejections,
                        "duplicate_plaintexts": transpositions.duplicate_candidates})
        for candidate in transpositions.candidates:
            add(candidate.family, candidate.key, candidate.plaintext, candidate.re_encryption_matches)
        if words:
            results.append({"kind": "unused_evidence", "reason": "Lexicon membership is used only by numeric Morse inference in this tool"})
    elif not words and not normalized:
        completed.append(False)
        stop_reason = "requires_evidence"
        next_actions.append({"stage": "supply_evidence", "reason": "Morse inference requires aligned cribs or a lexicon"})
    else:
        morse = search_morse_constraints(cipher, lexicon=words,
                                         cribs=tuple(MorseCrib(c.offset, c.plaintext) for c in normalized),
                                         max_maps=max_checks, max_candidates=max_candidates, timeout_seconds=5.0)
        checks += morse.maps_examined
        completed.append(morse.search_complete)
        actions.append({"tool": "morse_constraints", "checks": morse.maps_examined,
                        "search_complete": morse.search_complete, "stop_reason": morse.stop_reason,
                        "reason": "Digit stream and supplied plaintext evidence support testing Morbit and Pollux maps"})
        results.append({"tool": "morse_constraints", "accepted_maps": morse.accepted_map_count,
                        "families": [asdict(family) for family in morse.families],
                        "plaintext_ambiguity_within_models": morse.plaintext_ambiguity})
        for candidate in morse.candidates:
            consistency += 1
            try:
                forward = (morbit_encrypt(candidate.plaintext, candidate.key) if candidate.family == "morbit"
                           else pollux_encrypt(candidate.plaintext, candidate.key, choices=cipher))
                match = forward == cipher
            except ValueError:
                match = False
            if match:
                add(candidate.family, {"map": candidate.key}, candidate.plaintext)
            else:
                mismatches += 1
        if not morse.search_complete:
            stop_reason = "time_limit" if morse.stop_reason == "time_limit" else "check_limit"

    complete = bool(completed) and all(completed)
    if not complete and stop_reason == "complete":
        stop_reason = "check_limit"
    if mismatches:
        contradictions.append({"kind": "transform_inconsistency", "count": mismatches,
                               "scope": "Returned decryptions failed an independent forward transform and were rejected."})
    ranked = tuple(sorted(candidates.values(), key=lambda c: (-c.score, -(c.neural_probability or 0), c.family, c.plaintext, str(c.key)))[:max_candidates])
    if not ranked and complete:
        contradictions.append({"kind": "no_compatible_model", "scope": "No witness inside the completed stated models and supplied constraints; other models remain possible."})
    results.append({"kind": "candidate_summary", "retained": len(ranked), "partial_hypotheses_retained": len(hypotheses),
                    "consistency_checks": consistency, "correctness_known": False, "independent_cases": 0})
    if not complete and stop_reason in ("check_limit", "time_limit"):
        next_actions.append({"stage": "extend_search", "reason": "Review exhausted bounds before increasing a finite search budget"})
    if (not ranked and not contradictions) or any(item["kind"] == "no_compatible_model" for item in contradictions):
        next_actions.append({"stage": "alternative_models", "reason": "Review transcription, constraint alignment, and untested cipher families rather than invent a reading"})
    next_actions.append({"stage": "verify_case", "reason": "Seek an independent key, archival plaintext, or held-out evidence that was not supplied to candidate generation"})
    caution = 1.0  # Every result lacks independent correctness evidence.
    curiosity = 0.8 if not complete else 0.5
    frustration = 0.6 if not ranked else 0.2
    if temperament == "curious":
        curiosity = min(1.0, curiosity + 0.1)
    elif temperament == "cautious":
        frustration *= 0.5
    affect = {"simulated": True, "literal_feelings_or_sentience": False, "temperament": temperament,
              "states": {"curiosity": curiosity, "caution": caution, "frustration": frustration},
              "happiness": None, "meaning": "Display-only control telemetry, with no verified reward until independent correctness evidence exists."}
    thought = {"kind": "program_generated_plan_summary", "literal_private_thought": False,
               "plan": [step["stage"] for step in next_actions],
               "basis": "Recorded constraints, bounded model results, missing independent evidence, and alternative explanations."}
    return SolverReasoningReport(kind, coordinates, ranked, tuple(hypotheses), checks, consistency,
                                 complete, stop_reason, monotonic() - start,
                                 {"max_checks": max_checks, "max_candidates": max_candidates,
                                  "max_symbols": MAX_SYMBOLS, "max_period": min(16, len(cipher)) if kind == "latin" else None,
                                  "transposition_max_width": 8 if kind == "latin" else None,
                                  "transposition_max_rails": 5 if kind == "latin" else None,
                                  "morse_timeout_seconds": 5.0 if kind == "numeric" else None,
                                  "check_unit": "one tested key or model setting, with applicable forward consistency comparison",
                                  "completion_scope": ("all invertible affine keys and the default finite transposition portfolio; with cribs, also substitution and repeating Vigenere/Beaufort periods through min(16, length)"
                                                       if kind == "latin" else "viable Morbit and Pollux maps under the supplied lexicon or decoded-character cribs"),
                                  "numeric_terminal_period_is_framing": text.strip().endswith(".") if kind == "numeric" else None,
                                  "neural_inference_is_advisory_overhead": True},
                                 advice, tuple(premises), tuple(actions), tuple(results), tuple(contradictions),
                                 tuple(next_actions), affect, thought, evaluation_policy(0, 0))


__all__ = ["InvestigationCandidate", "SolverReasoningReport", "investigate_cipher", "score_reward", "evaluation_policy"]
