"""Bounded unknown-start search around the existing three-rotor Enigma.

Rotor order, reflector, ring settings, and plugboard are supplied. Missing
ciphertext slots step the machine and remain unknown in every prediction.
This is a repository composition, not a general Enigma break or a historical
solution claim. Machine explanation: https://www.cryptomuseum.com/crypto/enigma/working.htm
"""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import asdict, dataclass
from itertools import product
from time import monotonic

from engine.reverse_engineer import Crib
from engine.solvers.enigma import _machine, parse_plugboard

MAX_SLOTS = 512
START_SPACE = 26**3
MAX_LETTER_STEPS = 1000000
CRYPTO_MUSEUM_URL = "https://www.cryptomuseum.com/crypto/enigma/working.htm"
SCOPE = (
    "Unknown starts for the supplied three-rotor Enigma I settings and aligned cribs. "
    "Missing slots stay unknown. Crib fit and re-encryption establish transform "
    "consistency only, not an independently verified historical plaintext. "
    "No solution to army message Nr. 86 or an unknown script is claimed."
)


def _integer(value, name: str, low: int, high: int) -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an integer")
    if not low <= value <= high:
        raise ValueError(f"{name} must be in {low}..{high}")


def _slots(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not 1 <= len(text) <= 4 * MAX_SLOTS:
        raise ValueError(f"text must contain 1..{4 * MAX_SLOTS} raw characters")
    if any(not (ch.isspace() or ch in "?-" or ch.isascii() and ch.isalpha()) for ch in text):
        raise ValueError("ciphertext accepts only ASCII letters, whitespace, and ? or - missing-letter slots")
    stream = "".join("?" if ch in "?-" else ch.upper() for ch in text if not ch.isspace())
    if not 1 <= len(stream) <= MAX_SLOTS or not any(ch != "?" for ch in stream):
        raise ValueError(f"ciphertext requires 1..{MAX_SLOTS} slots and at least one known letter")
    return stream


def _plugboard(value) -> tuple[tuple[str, str], ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        if len(value) > 100 or any(not (ch.isascii() and ch.isalpha() or ch.isspace() or ch in ",-") for ch in value):
            raise ValueError("plugboard must contain bounded ASCII letter pairs")
        pairs = value.replace(",", " ").replace("-", " ").split()
    elif isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        pairs = value
    else:
        raise TypeError("plugboard must be a pair string or finite sequence")
    if len(pairs) > 13:
        raise ValueError("plugboard accepts at most 13 disjoint pairs")
    checked = []
    for pair in pairs:
        if isinstance(pair, str):
            letters = pair
        elif isinstance(pair, Sequence) and not isinstance(pair, (bytes, bytearray)):
            if len(pair) != 2 or any(not isinstance(ch, str) or len(ch) != 1 for ch in pair):
                raise ValueError("each plugboard pair requires two single ASCII letters")
            letters = "".join(pair)
        else:
            raise TypeError("each plugboard pair must be a string or two-letter sequence")
        if len(letters) != 2 or any(not (ch.isascii() and ch.isalpha()) for ch in letters):
            raise ValueError("each plugboard pair requires two ASCII letters")
        checked.append(letters.upper())
    return parse_plugboard(checked)


def _settings(rotors, reflector, rings, plugboard) -> dict:
    if not isinstance(rotors, Sequence) or isinstance(rotors, (str, bytes, bytearray)) or len(rotors) != 3:
        raise TypeError("rotors must be a finite sequence of three rotor names")
    if any(not isinstance(name, str) or not 1 <= len(name) <= 8 for name in rotors):
        raise ValueError("rotor names must be bounded strings")
    names = tuple(name.strip().upper() for name in rotors)
    if any(name not in ("I", "II", "III", "IV", "V") for name in names) or len(set(names)) != 3:
        raise ValueError("rotors must be three distinct names from I through V")
    if not isinstance(reflector, str) or len(reflector) > 8 or reflector.strip().upper() not in ("B", "C"):
        raise ValueError("reflector must be B or C")
    if not isinstance(rings, str) or len(rings) != 3 or any(not (ch.isascii() and ch.isalpha()) for ch in rings):
        raise ValueError("rings must be exactly three ASCII letters")
    return {"rotors": names, "reflector": reflector.strip().upper(), "rings": rings.upper(), "plugboard": _plugboard(plugboard)}


def _cribs(cribs: Sequence[Crib], cipher: str, skip_missing: bool) -> tuple[dict[int, str], int]:
    if not isinstance(cribs, Sequence) or isinstance(cribs, (str, bytes, bytearray)):
        raise TypeError("cribs must be a finite sequence of Crib objects")
    if not 1 <= len(cribs) <= 128:
        raise ValueError("search requires 1..128 aligned cribs")
    known, skipped = {}, set()
    for crib in cribs:
        if not isinstance(crib, Crib):
            raise TypeError("cribs must contain engine.reverse_engineer.Crib objects")
        _integer(crib.offset, "crib offset", 0, len(cipher) - 1)
        if (not isinstance(crib.plaintext, str) or not 1 <= len(crib.plaintext) <= 4 * MAX_SLOTS
                or any(not (ch.isspace() or ch.isascii() and ch.isalpha()) for ch in crib.plaintext)):
            raise ValueError("crib plaintext must contain bounded ASCII letters and whitespace")
        plain = "".join(ch.upper() for ch in crib.plaintext if not ch.isspace())
        if not plain or crib.offset + len(plain) > len(cipher):
            raise ValueError("crib exceeds plaintext slot coordinates, which include missing letters")
        for position, character in enumerate(plain, crib.offset):
            if cipher[position] == "?":
                if not skip_missing:
                    raise ValueError("crib touches a missing ciphertext slot; split the crib or explicitly set skip_missing=True")
                skipped.add(position)
                continue
            if position in known and known[position] != character:
                raise ValueError("overlapping cribs disagree")
            known[position] = character
    if not known:
        raise ValueError("at least one crib position must align with a known ciphertext letter")
    return known, len(skipped)


def _process_slots(machine, text: str, advance) -> str:
    return "".join(advance(machine, None if character == "?" else character) for character in text)


@dataclass(frozen=True)
class EnigmaStartCandidate:
    positions: str
    key: dict
    plaintext: str
    re_encryption_matches: bool
    score: float = 0.0
    family: str = "enigma"

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class EnigmaStartSearchReport:
    candidates: tuple[EnigmaStartCandidate, ...]
    checks: int
    checked_starts: int
    accepted_start_count: int
    letter_steps: int
    search_complete: bool
    stop_reason: str
    incomplete_start: str | None
    ciphertext_length: int
    gap_positions: tuple[int, ...]
    known_positions: int
    skipped_crib_positions: int
    supplied_settings: dict
    contradictions: tuple[dict, ...]
    re_encryption_mismatches: int
    candidates_truncated: bool
    start_ambiguity: bool | None
    plaintext_ambiguity: bool | None
    elapsed_seconds: float
    bounds: dict
    claimed_plaintext: None = None
    ranking: str = "lexicographic start positions; score is zero and is not a correctness estimate"
    scope: str = SCOPE

    @property
    def unique_start_within_settings(self) -> bool:
        return self.search_complete and self.accepted_start_count == 1

    @property
    def unique_plaintext_within_settings(self) -> bool:
        return self.search_complete and self.accepted_start_count > 0 and self.plaintext_ambiguity is False

    def to_dict(self) -> dict:
        result = asdict(self)
        result.update(unique_start_within_settings=self.unique_start_within_settings,
                      unique_plaintext_within_settings=self.unique_plaintext_within_settings)
        return result


class _WorkLimit(Exception):
    pass


def search_enigma_starts(text: str, *, cribs: Sequence[Crib], rotors: Sequence[str] = ("I", "II", "III"),
                         reflector: str = "B", rings: str = "AAA", plugboard=(),
                         max_checks: int = START_SPACE, max_candidates: int = 20,
                         skip_missing: bool = False, max_letter_steps: int = MAX_LETTER_STEPS) -> EnigmaStartSearchReport:
    """Test all or a bounded prefix of 26**3 unknown rotor starts.

    One check is an initiated start; checked_starts excludes any interrupted
    trial. Work counts every machine slot advance, including gap steps and
    accepted-candidate replay. Missing slots never receive guessed plaintext.
    Retention limits do not stop enumeration or establish uniqueness.
    """
    start_time = monotonic()
    _integer(max_checks, "max_checks", 0, START_SPACE)
    _integer(max_candidates, "max_candidates", 1, 100)
    _integer(max_letter_steps, "max_letter_steps", 0, MAX_LETTER_STEPS)
    if not isinstance(skip_missing, bool):
        raise TypeError("skip_missing must be a boolean")
    cipher = _slots(text)
    settings = _settings(rotors, reflector, rings, plugboard)
    known, skipped = _cribs(cribs, cipher, skip_missing)
    contradictions = tuple({"kind": "self_encryption", "position": position,
                            "scope": "The supplied Enigma reflector model cannot encipher a letter to itself."}
                           for position, character in sorted(known.items()) if cipher[position] == character)
    checks = checked = accepted = steps = mismatches = 0
    candidates, first_plain = [], None
    different_plain = False
    stop_reason, incomplete_start = "complete", None

    def advance(machine, letter):
        nonlocal steps
        if steps >= max_letter_steps:
            raise _WorkLimit
        steps += 1
        if letter is None:
            machine.step()
            return "?"
        return machine.encrypt_letter(letter)

    if contradictions:
        stop_reason = "structural_rejection"
        complete = True
    else:
        machine, *_ = _machine(**settings, positions="AAA")
        replay, *_ = _machine(**settings, positions="AAA")
        final_crib = max(known)
        for values in product(range(26), repeat=3):
            if checks >= max_checks:
                stop_reason = "check_limit"
                break
            positions = "".join(chr(65 + value) for value in values)
            checks += 1
            machine.positions[:] = values
            failed = False
            try:
                for index in range(final_crib + 1):
                    expected = known.get(index)
                    decoded = advance(machine, cipher[index] if expected is not None else None)
                    if expected is not None and decoded != expected:
                        failed = True
                        break
                if failed:
                    checked += 1
                    continue
                # Reserve both complete replays before producing a witness.
                if max_letter_steps - steps < 2 * len(cipher):
                    raise _WorkLimit
                machine.positions[:] = values
                plain = _process_slots(machine, cipher, advance)
                replay.positions[:] = values
                forward = _process_slots(replay, plain, advance)
                checked += 1
                if forward != cipher:
                    mismatches += 1
                    continue
                accepted += 1
                if first_plain is None:
                    first_plain = plain
                elif plain != first_plain:
                    different_plain = True
                if len(candidates) < max_candidates:
                    candidates.append(EnigmaStartCandidate(positions, {**settings, "positions": positions}, plain, True))
            except _WorkLimit:
                stop_reason, incomplete_start = "work_limit", positions
                break
        complete = checked == START_SPACE
    if mismatches:
        contradictions += ({"kind": "transform_inconsistency", "count": mismatches,
                            "scope": "Candidate replay failed to reproduce every known ciphertext slot and was rejected."},)
    return EnigmaStartSearchReport(tuple(candidates), checks, checked, accepted, steps, complete,
                                   stop_reason, incomplete_start, len(cipher),
                                   tuple(index for index, ch in enumerate(cipher) if ch == "?"), len(known), skipped,
                                   settings, contradictions, mismatches, accepted > len(candidates),
                                   True if accepted > 1 else False if complete else None,
                                   True if different_plain else False if complete else None,
                                   monotonic() - start_time,
                                   {"max_checks": max_checks, "start_space": START_SPACE, "max_candidates": max_candidates,
                                    "max_letter_steps": max_letter_steps, "max_slots": MAX_SLOTS, "skip_missing": skip_missing,
                                    "check_unit": "one initiated start; checked_starts counts completed start trials",
                                    "work_unit": "one machine slot advance, including gaps and forward replay",
                                    "crib_coordinates": "zero-based normalized plaintext slots including missing letters",
                                    "gap_semantics": "each ? or - records exactly one missing cipher letter; unknown gap lengths are not searched",
                                    "missing_slot_output": "?", "search_order": "AAA through ZZZ",
                                    "settings_searched": ["positions"], "settings_supplied": list(settings),
                                    "source_url": CRYPTO_MUSEUM_URL})


__all__ = ["EnigmaStartCandidate", "EnigmaStartSearchReport", "search_enigma_starts"]
