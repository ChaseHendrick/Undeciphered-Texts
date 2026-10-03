"""Interrupted Vigenere with supplied resets, and unknown-key crib inference.

ACA specifies restarting the keyword at each interruption and using the whole
keyword at least once. This module implements the worksheet's Vigenere mode;
other periodic tableaux and unknown reset patterns are outside its scope.
https://www.cryptogram.org/downloads/aca.info/ciphers/InterruptedKey.pdf
"""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import asdict, dataclass

from engine.result import SolveResult
from engine.reverse_engineer import Crib

ACA_INTERRUPTED_KEY_URL = "https://www.cryptogram.org/downloads/aca.info/ciphers/InterruptedKey.pdf"
MAX_LETTERS = 4096
MAX_KEYWORD = 64


def _integer(value, name: str, low: int, high: int) -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an integer")
    if not low <= value <= high:
        raise ValueError(f"{name} must be in {low}..{high}")


def _letters(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if len(text) > 4 * MAX_LETTERS or any(ch.isalnum() and not (ch.isascii() and ch.isalpha()) for ch in text):
        raise ValueError("text must use ASCII letters within the input bound")
    letters = "".join(ch.upper() for ch in text if ch.isascii() and ch.isalpha())
    if not 1 <= len(letters) <= MAX_LETTERS:
        raise ValueError(f"text must contain 1..{MAX_LETTERS} ASCII letters")
    return letters


def _keyword(keyword: str) -> str:
    if not isinstance(keyword, str):
        raise TypeError("keyword must be a string")
    if not 1 <= len(keyword) <= MAX_KEYWORD or any(not (ch.isascii() and ch.isalpha()) for ch in keyword):
        raise ValueError(f"keyword must contain 1..{MAX_KEYWORD} ASCII letters")
    return keyword.upper()


def _runs(segment_lengths: Sequence[int], length: int | None = None) -> tuple[int, ...]:
    if not isinstance(segment_lengths, Sequence) or isinstance(segment_lengths, (str, bytes, bytearray)):
        raise TypeError("segment_lengths must be a finite sequence of positive integers")
    if not 1 <= len(segment_lengths) <= MAX_LETTERS:
        raise ValueError(f"segment_lengths must contain 1..{MAX_LETTERS} entries")
    for value in segment_lengths:
        _integer(value, "segment length", 1, MAX_LETTERS)
    runs = tuple(segment_lengths)
    total = sum(runs)
    if total > MAX_LETTERS or length is not None and total != length:
        raise ValueError("segment lengths must partition the complete normalized text within the size bound")
    return runs


def _slots(runs: tuple[int, ...], keyword_length: int) -> tuple[int, ...]:
    if max(runs) < keyword_length:
        raise ValueError("the entire keyword must be used in at least one segment")
    return tuple(index % keyword_length for count in runs for index in range(count))


def interrupted_key_stream(keyword: str, segment_lengths: Sequence[int]) -> str:
    """Restart the normal repeating Vigenere keyword at each segment boundary."""
    word = _keyword(keyword)
    runs = _runs(segment_lengths)
    return "".join(word[index] for index in _slots(runs, len(word)))


def _transform(text: str, keyword: str, segment_lengths: Sequence[int], decrypt: bool) -> str:
    letters, word = _letters(text), _keyword(keyword)
    runs = _runs(segment_lengths, len(letters))
    slots = _slots(runs, len(word))
    sign = -1 if decrypt else 1
    return "".join(chr(65 + (ord(character) - 65 + sign * (ord(word[slot]) - 65)) % 26)
                   for character, slot in zip(letters, slots))


def interrupted_key_encrypt(text: str, keyword: str, *, segment_lengths: Sequence[int]) -> str:
    return _transform(text, keyword, segment_lengths, False)


def interrupted_key_decrypt(text: str, keyword: str, *, segment_lengths: Sequence[int]) -> str:
    return _transform(text, keyword, segment_lengths, True)


def solve_interrupted_key(text: str, *, keyword: str, segment_lengths: Sequence[int]) -> SolveResult:
    word = _keyword(keyword)
    plain = interrupted_key_decrypt(text, word, segment_lengths=segment_lengths)
    return SolveResult("interrupted-key", plain, word, float(len(plain)),
                       {"mode": "supplied_key_and_reset_pattern", "segment_lengths": tuple(segment_lengths),
                        "source_url": ACA_INTERRUPTED_KEY_URL,
                        "scope": "Supplied-key interrupted Vigenere only; not unknown reset recovery or a historical decipherment."})


@dataclass(frozen=True)
class InterruptedKeyInferenceReport:
    key: str
    keyword_length: int
    segment_lengths: tuple[int, ...]
    predicted_plaintext: str
    predicted_positions: int
    unresolved_parameters: int
    compatible: bool | None
    known_positions: int
    checks: int
    search_complete: bool
    stop_reason: str
    contradictions: tuple[dict, ...]
    re_encryption_matches: bool | None
    bounds: dict
    claimed_plaintext: None = None
    scope: str = "Unknown keyword inference for supplied interruption pattern and keyword length. Unknown slots remain ?. Crib fit and re-encryption do not independently verify a historical decipherment."

    @property
    def unique_key_within_pattern(self) -> bool:
        return self.search_complete and self.compatible is True and self.unresolved_parameters == 0 and self.re_encryption_matches is True

    def to_dict(self) -> dict:
        result = asdict(self)
        result["unique_key_within_pattern"] = self.unique_key_within_pattern
        return result


def infer_interrupted_key(ciphertext: str, *, segment_lengths: Sequence[int], cribs: Sequence[Crib],
                          keyword_length: int | None = None, max_checks: int = 4096) -> InterruptedKeyInferenceReport:
    """Propagate aligned crib equations into unknown keyword slots.

    One check is one distinct known position's Vigenere equation. If length is
    omitted, the explicit prefix model assumes the longest run uses the entire
    keyword. Supply keyword_length for repeated keyword cycles inside a run.
    Completion means every supplied equation was checked, not a search over
    unknown reset patterns or key lengths.
    """
    _integer(max_checks, "max_checks", 0, MAX_LETTERS)
    cipher = _letters(ciphertext)
    runs = _runs(segment_lengths, len(cipher))
    assumed = keyword_length is None
    length = max(runs) if assumed else keyword_length
    _integer(length, "keyword_length", 1, MAX_KEYWORD)
    positions = _slots(runs, length)
    if not isinstance(cribs, Sequence) or isinstance(cribs, (str, bytes, bytearray)):
        raise TypeError("cribs must be a finite sequence of Crib objects")
    if not 1 <= len(cribs) <= 128:
        raise ValueError("inference requires 1..128 aligned cribs")
    known = {}
    for crib in cribs:
        if not isinstance(crib, Crib):
            raise TypeError("cribs must contain engine.reverse_engineer.Crib objects")
        _integer(crib.offset, "crib offset", 0, len(cipher) - 1)
        plain = _letters(crib.plaintext)
        if crib.offset + len(plain) > len(cipher):
            raise ValueError("crib exceeds normalized plaintext coordinates")
        for position, character in enumerate(plain, crib.offset):
            if position in known and known[position] != character:
                raise ValueError("overlapping cribs disagree")
            known[position] = character
    key_slots: list[int | None] = [None] * length
    contradictions, checks = [], 0
    for position, character in sorted(known.items()):
        if checks >= max_checks:
            break
        checks += 1
        shift = (ord(cipher[position]) - ord(character)) % 26
        slot = positions[position]
        if key_slots[slot] is not None and key_slots[slot] != shift:
            contradictions.append({"kind": "incompatible_keyword_slot", "position": position, "slot": slot,
                                   "required_shift": shift, "previous_shift": key_slots[slot]})
        else:
            key_slots[slot] = shift
    complete = checks == len(known)
    compatible = False if contradictions else True if complete else None
    key = "".join("?" if value is None else chr(65 + value) for value in key_slots) if not contradictions else ""
    prediction = ("".join("?" if key_slots[slot] is None else chr(65 + (ord(character) - 65 - key_slots[slot]) % 26)
                          for character, slot in zip(cipher, positions)) if not contradictions else "")
    unresolved = sum(value is None for value in key_slots) if not contradictions else length
    forward_match = None
    if complete and compatible and unresolved == 0:
        forward_match = interrupted_key_encrypt(prediction, key, segment_lengths=runs) == cipher
    return InterruptedKeyInferenceReport(key, length, runs, prediction, len(prediction) - prediction.count("?"),
                                         unresolved, compatible, len(known), checks, complete,
                                         "complete" if complete else "check_limit", tuple(contradictions), forward_match,
                                         {"max_checks": max_checks, "ciphertext_length": len(cipher), "max_letters": MAX_LETTERS,
                                          "max_keyword_length": MAX_KEYWORD, "keyword_length_assumed_from_longest_run": assumed,
                                          "check_unit": "one distinct supplied plaintext-position equation",
                                          "crib_coordinates": "zero-based normalized A-Z plaintext letters",
                                          "search_scope": "supplied reset pattern and fixed keyword length only",
                                          "source_url": ACA_INTERRUPTED_KEY_URL})


__all__ = ["ACA_INTERRUPTED_KEY_URL", "InterruptedKeyInferenceReport", "interrupted_key_stream",
           "interrupted_key_encrypt", "interrupted_key_decrypt", "solve_interrupted_key", "infer_interrupted_key"]
