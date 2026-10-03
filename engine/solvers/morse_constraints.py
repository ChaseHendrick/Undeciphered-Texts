"""Bounded unknown-map composition of Morbit/Pollux and plaintext evidence.

This repository tool combines the sourced Morse transformations with exact
lexicon membership or aligned decoded-text cribs. It enumerates complete
digit maps without a supplied key. Ranking is an explicit length preference,
not a language probability, and uniqueness needs a completed map search.
No historical decipherment or priority claim is made for this composition.
"""

from __future__ import annotations

import heapq
import math
from collections import deque
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from itertools import permutations, product
from time import monotonic as _monotonic

from engine.result import SolveResult
from engine.solvers.morbit import ACA_MORBIT_URL, _ASCII_LETTERS, _MORSE, _PAIRS, _decode_morse, _digit_stream
from engine.solvers.pollux import ACA_POLLUX_URL

MAX_CIPHER_DIGITS = 512
MAX_MAPS = 500_000
MAX_CANDIDATES = 1000
MAX_LEXICON_WORDS = 10_000
_MAP_SPACES = {"morbit": math.factorial(9), "pollux": 3 ** 10}


@dataclass(frozen=True)
class MorseCrib:
    """Zero-based coordinates in uppercase decoded text INCLUDING word spaces."""

    offset: int
    plaintext: str


@dataclass(frozen=True)
class MorseMapCandidate:
    family: str
    key: str
    plaintext: str
    score: float


@dataclass(frozen=True)
class MorseFamilySummary:
    family: str
    map_space: int
    maps_examined: int
    structurally_rejected: int
    morse_valid_maps: int
    evidence_rejected: int
    accepted_map_count: int
    search_complete: bool
    excluded_reason: str | None


@dataclass(frozen=True)
class MorseConstraintReport:
    candidates: tuple[MorseMapCandidate, ...]
    families: tuple[MorseFamilySummary, ...]
    maps_examined: int
    accepted_map_count: int
    search_complete: bool
    stop_reason: str
    plaintext_ambiguity: bool | None
    map_ambiguity: bool | None
    candidates_truncated: bool
    elapsed_seconds: float
    bounds: dict
    evidence: dict
    ranking: str
    claimed_plaintext: None = None
    scope: str = "Conditional on supplied lexicon/cribs, strict Morse table, tested families, and completed map bounds; not a historical decipherment."

    @property
    def unique_plaintext_within_models(self) -> bool:
        return self.search_complete and self.accepted_map_count > 0 and self.plaintext_ambiguity is False

    @property
    def unique_map_within_models(self) -> bool:
        return self.search_complete and self.accepted_map_count == 1

    def to_dict(self) -> dict:
        result = asdict(self)
        result.update(unique_plaintext_within_models=self.unique_plaintext_within_models,
                      unique_map_within_models=self.unique_map_within_models)
        return result


def _integer(value: int, name: str, minimum: int, maximum: int) -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an integer")
    if not minimum <= value <= maximum:
        raise ValueError(f"{name} must be in {minimum}..{maximum}")


def _sequence(value, name: str, maximum: int) -> tuple:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise TypeError(f"{name} must be a finite sequence")
    if len(value) > maximum:
        raise ValueError(f"{name} must contain at most {maximum} entries")
    return tuple(value)


def _evidence(lexicon: Sequence[str] | None, cribs: Sequence[MorseCrib], max_decoded: int) -> tuple[set[str] | None, dict[int, str]]:
    words = None
    if lexicon is not None:
        entries = _sequence(lexicon, "lexicon", MAX_LEXICON_WORDS)
        if not entries:
            raise ValueError("lexicon must contain at least one ASCII word")
        if any(not isinstance(word, str) or not 1 <= len(word) <= 256 or any(ch not in _ASCII_LETTERS for ch in word) for word in entries):
            raise ValueError("lexicon entries must be single ASCII words of 1..256 letters")
        words = {word.upper() for word in entries}
    known = {}
    for crib in _sequence(cribs, "cribs", 128):
        if not isinstance(crib, MorseCrib):
            raise TypeError("cribs must contain MorseCrib values")
        _integer(crib.offset, "crib offset", 0, max_decoded)
        if (not isinstance(crib.plaintext, str) or not 1 <= len(crib.plaintext) <= max_decoded
                or any(ch != " " and ch not in _ASCII_LETTERS and ch not in _MORSE for ch in crib.plaintext)):
            raise ValueError("crib plaintext must contain supported ASCII Morse characters or literal spaces")
        if crib.offset + len(crib.plaintext) > max_decoded:
            raise ValueError("crib extends beyond the maximum possible decoded length")
        for index, character in enumerate(crib.plaintext.upper(), crib.offset):
            if index in known and known[index] != character:
                raise ValueError("overlapping Morse cribs contradict one another")
            known[index] = character
    if words is None and not known:
        raise ValueError("unknown-map inference requires a supplied lexicon or at least one aligned Morse crib")
    return words, known


def _candidate_maps(family: str):
    if family == "morbit":
        return ("".join(values) for values in permutations("123456789"))
    return ("".join(values) for values in product(".-x", repeat=10))


def search_morse_constraints(
    text: str, *, families: Sequence[str] = ("morbit", "pollux"),
    lexicon: Sequence[str] | None = None, cribs: Sequence[MorseCrib] = (),
    max_maps: int = 10_000, max_candidates: int = 20, timeout_seconds: float = 5.0,
    terminal_period: bool = False,
) -> MorseConstraintReport:
    """Enumerate unknown maps fairly, retaining bounded ranked witnesses.

    Morbit tries 9! permutations; Pollux tries 3**10 complete assignments.
    Missing-symbol Pollux maps are counted and rejected. Stored candidates
    do not limit search or prove uniqueness. A single returned plaintext is
    unique only when all map candidates in every viable family are exhausted.
    """
    start = _monotonic()
    _integer(max_maps, "max_maps", 0, MAX_MAPS)
    _integer(max_candidates, "max_candidates", 1, MAX_CANDIDATES)
    if (not isinstance(timeout_seconds, (int, float)) or isinstance(timeout_seconds, bool)
            or not math.isfinite(timeout_seconds) or not 0 < timeout_seconds <= 60):
        raise ValueError("timeout_seconds must be finite, positive, and at most 60")
    selected = _sequence(families, "families", 2)
    if not selected or any(not isinstance(family, str) or family not in _MAP_SPACES for family in selected):
        raise ValueError("families must contain morbit or pollux")
    selected = tuple(dict.fromkeys(selected))
    digits = _digit_stream(text, terminal_period=terminal_period)
    if len(digits) > MAX_CIPHER_DIGITS:
        raise ValueError(f"unknown-map inference is limited to {MAX_CIPHER_DIGITS} ciphertext digits")
    if selected == ("morbit",) and "0" in digits:
        raise ValueError("Morbit ciphertext cannot contain digit zero")
    words, known = _evidence(lexicon, cribs, 2 * len(digits))
    digit_indices = tuple(map(int, digits))
    rows = {family: {"map_space": 0 if family == "morbit" and "0" in digits else _MAP_SPACES[family],
                     "maps_examined": 0, "structurally_rejected": 0, "morse_valid_maps": 0,
                     "evidence_rejected": 0, "accepted_map_count": 0,
                     "excluded_reason": "digit zero cannot occur in Morbit" if family == "morbit" and "0" in digits else None}
            for family in selected}
    active = deque((index, family, _candidate_maps(family)) for index, family in enumerate(selected) if rows[family]["map_space"])
    heap = []
    examined = accepted = 0
    first_plain = None
    different_plain = False
    stop_reason = "complete"
    while active:
        family_index, family, iterator = active.popleft()
        try:
            key = next(iterator)
        except StopIteration:
            continue
        if examined >= max_maps:
            stop_reason = "map_limit"
            break
        if _monotonic() - start >= timeout_seconds:
            stop_reason = "time_limit"
            break
        active.append((family_index, family, iterator))
        row = rows[family]
        ordinal = row["maps_examined"]
        row["maps_examined"] += 1
        examined += 1
        if family == "pollux" and set(key) != set(".-x"):
            row["structurally_rejected"] += 1
            continue
        if family == "morbit":
            inverse = dict(zip(key, _PAIRS))
            stream = "".join(inverse[digit] for digit in digits)
        else:
            stream = "".join(key[index] for index in digit_indices)
        try:
            plain = _decode_morse(stream, allow_padding=family == "morbit")
        except ValueError:
            continue
        row["morse_valid_maps"] += 1
        tokens = plain.split(" ")
        if (any(index >= len(plain) or plain[index] != character for index, character in known.items())
                or words is not None and any(word not in words for word in tokens)):
            row["evidence_rejected"] += 1
            continue
        row["accepted_map_count"] += 1
        accepted += 1
        if first_plain is None:
            first_plain = plain
        elif plain != first_plain:
            different_plain = True
        score = float(sum(len(word) ** 2 for word in tokens)) if words is not None else 0.0
        candidate = MorseMapCandidate(family, key, plain, score)
        entry = ((score, -family_index, -ordinal), candidate)
        if len(heap) < max_candidates:
            heapq.heappush(heap, entry)
        elif entry[0] > heap[0][0]:
            heapq.heapreplace(heap, entry)
    complete = stop_reason == "complete"
    summaries = tuple(MorseFamilySummary(family=family, search_complete=rows[family]["maps_examined"] == rows[family]["map_space"], **rows[family])
                      for family in selected)
    candidates = tuple(entry[1] for entry in sorted(heap, key=lambda entry: entry[0], reverse=True))
    return MorseConstraintReport(
        candidates, summaries, examined, accepted, complete, stop_reason,
        True if different_plain else False if complete else None,
        True if accepted > 1 else False if complete else None,
        accepted > len(candidates), _monotonic() - start,
        {"ciphertext_digits": len(digits), "max_ciphertext_digits": MAX_CIPHER_DIGITS,
         "max_maps": max_maps, "max_candidates": max_candidates, "timeout_seconds": timeout_seconds,
         "terminal_period_is_framing": terminal_period, "family_enumeration": "round robin"},
        {"lexicon_words": None if words is None else len(words), "known_crib_positions": len(known),
         "crib_coordinates": "uppercase decoded characters including word spaces",
         "lexicon_rule": "every complete decoded word must belong to the supplied lexicon" if words is not None else None,
         "source_urls": [ACA_MORBIT_URL if family == "morbit" else ACA_POLLUX_URL for family in selected]},
        "sum of squared lexicon word lengths; explicit length preference, not probability" if words is not None else "zero score; deterministic family and map order",
    )


def solve_morse_constraints(text: str, **parameters) -> SolveResult:
    """Populate plaintext only for completed, evidence-scoped unique plaintext."""
    report = search_morse_constraints(text, **parameters)
    details = report.to_dict()
    details["certainty_scope"] = "completed supplied models and evidence only"
    unique = report.unique_plaintext_within_models
    return SolveResult("morse-constraints", report.candidates[0].plaintext if unique else "",
                       report.candidates[0].key if report.unique_map_within_models else "multiple or unresolved maps",
                       report.candidates[0].score if unique else 0.0, details)


__all__ = ["MorseCrib", "MorseMapCandidate", "MorseFamilySummary", "MorseConstraintReport", "search_morse_constraints", "solve_morse_constraints"]
