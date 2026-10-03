"""ACA Progressive Key Vigenere helpers and bounded crib-based inference.

https://www.cryptogram.org/downloads/aca.info/ciphers/ProgressiveKey.pdf
Each keyword-length group adds progression * group_number modulo 26,
starting with zero. The certificate covers the 30 independently printed
plaintext letters, rather than inventing the remaining ciphertext's answer.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import asdict, dataclass
from engine.alphabet import ALPHABET
from engine.result import SolveResult
from engine.reverse_engineer import Crib

ACA_URL = "https://www.cryptogram.org/downloads/aca.info/ciphers/ProgressiveKey.pdf"
ACA_PDF_SHA256 = "87e7f9561b8da2d5f14dd37e68331ed89a2d9a2d331f474d171f98e5e6778270"
ACA_PLAIN = "THISCIPHERCANBEUSEDWITHANYOFTH"
ACA_CIPHER = "ZYIHGNGBMKJSORJAKZMQQMJRTFHBDC"
ACA_PRINTED_FULL_CIPHER = "ZYIHG NGBMK JSORJ AKZMQ QMJRT FHBDC NJHJP WXFNO."
MAX_PERIOD = 128
MAX_INFERENCE_LETTERS = 512
MAX_TEXT_CHARACTERS = 1_000_000
MAX_CHECKS = 100_000
MAX_CANDIDATES = 10_000
_ASCII = frozenset(ALPHABET + ALPHABET.lower())


def _integer(value: int, name: str, minimum: int, maximum: int) -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an integer")
    if not minimum <= value <= maximum:
        raise ValueError(f"{name} must be in {minimum}..{maximum}")


def _letters(value: str, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if len(value) > MAX_TEXT_CHARACTERS or any(ch.isalpha() and ch not in _ASCII for ch in value):
        raise ValueError(f"{name} must use A-Z letters and at most {MAX_TEXT_CHARACTERS} characters")
    result = "".join(ch.upper() for ch in value if ch in _ASCII)
    if not result:
        raise ValueError(f"{name} must contain A-Z letters")
    return result


def _settings(keyword: str, progression: int) -> tuple[str, int]:
    key = _letters(keyword, "keyword")
    if len(key) > MAX_PERIOD:
        raise ValueError(f"keyword must contain at most {MAX_PERIOD} letters")
    _integer(progression, "progression", 0, 25)
    return key, progression


def _transform(text: str, keyword: str, progression: int, decrypt: bool) -> str:
    key, progression = _settings(keyword, progression)
    letters = _letters(text, "text")
    shifts = [ord(letter) - 65 for letter in key]
    return "".join(ALPHABET[(ord(letter) - 65 + (-1 if decrypt else 1)
                            * (shifts[index % len(key)] + progression * (index // len(key)))) % 26]
                   for index, letter in enumerate(letters))


def progressive_key_encrypt(text: str, *, keyword: str, progression: int = 1) -> str:
    """Encrypt with repeated keyword letters retained and zero initial progression."""
    return _transform(text, keyword, progression, False)


def progressive_key_decrypt(text: str, *, keyword: str, progression: int = 1) -> str:
    return _transform(text, keyword, progression, True)


def solve_progressive_key(text: str, *, keyword: str, progression: int = 1) -> SolveResult:
    key, progression = _settings(keyword, progression)
    plaintext = progressive_key_decrypt(text, keyword=key, progression=progression)
    label = f"keyword={key} progression={progression}"
    return SolveResult("progressive-key", plaintext, label, float(len(plaintext)), {
        "mode": "known_key", "keyword": key, "period": len(key), "progression": progression,
        "initial_progression": 0, "source_url": ACA_URL,
        "scope": "Supplied-key Vigenere Progressive Key; no unknown-key or historical recovery is claimed by this helper.",
    })


@dataclass(frozen=True)
class ProgressiveKeyCandidate:
    period: int
    progression: int
    key: str
    key_complete: bool
    unresolved_key_slots: int
    predicted_plaintext: str


@dataclass(frozen=True)
class ProgressiveKeyInferenceReport:
    ciphertext_length: int
    known_positions: int
    candidates: tuple[ProgressiveKeyCandidate, ...]
    checks: int
    search_complete: bool
    exhausted: bool
    exhaustion_reason: str
    bounds: dict
    claimed_plaintext: None = None
    scope: str = "Conditional crib-compatible Progressive Key Vigenere candidates within stated bounds. Unknown key slots stay ?. Crib fit and a single candidate do not verify unknown plaintext."

    def to_dict(self) -> dict:
        return asdict(self)


def _sequence(value, name: str, maximum: int) -> tuple:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise TypeError(f"{name} must be a finite sequence")
    if not 1 <= len(value) <= maximum:
        raise ValueError(f"{name} must contain 1..{maximum} entries")
    return tuple(value)


def infer_progressive_key(
    ciphertext: str, *, cribs: Sequence[Crib], max_period: int = 16,
    progressions: Sequence[int] = tuple(range(26)), max_checks: int = 4096,
    max_candidates: int = 1000,
) -> ProgressiveKeyInferenceReport:
    """Infer compatible keyword slots, period, and progression without a key.

    Each period/progression pair consumes one check. All supplied cribs use
    zero-based normalized A-Z positions. Repeated positions add no evidence.
    Parameters are hypotheses; missing slots and exhaustion remain explicit.
    """
    _integer(max_period, "max_period", 1, MAX_PERIOD)
    _integer(max_checks, "max_checks", 0, MAX_CHECKS)
    _integer(max_candidates, "max_candidates", 1, MAX_CANDIDATES)
    cipher = _letters(ciphertext, "ciphertext")
    if len(cipher) > MAX_INFERENCE_LETTERS:
        raise ValueError(f"inference accepts at most {MAX_INFERENCE_LETTERS} A-Z letters")
    steps = tuple(dict.fromkeys(_sequence(progressions, "progressions", 26)))
    for step in steps:
        _integer(step, "progression", 0, 25)
    known = {}
    for crib in _sequence(cribs, "cribs", MAX_INFERENCE_LETTERS):
        if not isinstance(crib, Crib):
            raise TypeError("cribs must contain engine.reverse_engineer.Crib objects")
        _integer(crib.offset, "crib offset", 0, len(cipher) - 1)
        plain = _letters(crib.plaintext, "crib plaintext")
        if crib.offset + len(plain) > len(cipher):
            raise ValueError("crib extends beyond the A-Z ciphertext stream")
        for index, letter in enumerate(plain, start=crib.offset):
            value = ord(letter) - 65
            if index in known and known[index] != value:
                raise ValueError("overlapping cribs disagree")
            known[index] = value
    period_bound = min(max_period, len(cipher))
    candidates = []
    checks = 0
    reason = ""
    for period in range(1, period_bound + 1):
        for step in steps:
            if checks >= max_checks:
                reason = "check_limit"
                break
            if len(candidates) >= max_candidates:
                reason = "candidate_limit"
                break
            checks += 1
            slots = [None] * period
            for index, plain in sorted(known.items()):
                shift = (ord(cipher[index]) - 65 - plain - step * (index // period)) % 26
                slot = index % period
                if slots[slot] is not None and slots[slot] != shift:
                    break
                slots[slot] = shift
            else:
                key = "".join("?" if shift is None else ALPHABET[shift] for shift in slots)
                prediction = "".join("?" if slots[index % period] is None else
                                     ALPHABET[(ord(letter) - 65 - slots[index % period] - step * (index // period)) % 26]
                                     for index, letter in enumerate(cipher))
                unresolved = slots.count(None)
                candidates.append(ProgressiveKeyCandidate(period, step, key, unresolved == 0, unresolved, prediction))
        if reason:
            break
    return ProgressiveKeyInferenceReport(len(cipher), len(known), tuple(candidates), checks, not reason, bool(reason), reason,
                                         {"max_period": max_period, "tested_period_bound": period_bound,
                                          "progressions": list(steps), "max_checks": max_checks,
                                          "max_candidates": max_candidates, "max_letters": MAX_INFERENCE_LETTERS,
                                          "initial_progression": 0})
