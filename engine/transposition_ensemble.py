"""Bounded repository composition of existing transposition transforms.

This is a portfolio, not a new historical cipher or verified decipherment.
Candidates must re-encrypt, satisfy any supplied cribs, and rank by the same
English score. Different keys yielding the same plaintext are deduplicated.
"""
from __future__ import annotations

from collections import deque
from collections.abc import Sequence
from dataclasses import asdict, dataclass, replace
from hashlib import sha256
from itertools import permutations, product
import math

from engine.language import get_model
from engine.reverse_engineer import Crib
from engine.solvers.columnar import (
    columnar_decrypt_right_to_left, columnar_encrypt_right_to_left,
    double_columnar_decrypt, double_columnar_encrypt,
)
from engine.solvers.rail_fence import rail_fence_decrypt, rail_fence_encrypt
from engine.solvers.redefence import redefence_decrypt, redefence_encrypt
from engine.solvers.route import route_decrypt, route_encrypt

FAMILIES = ("rail-fence", "route", "columnar", "redefence")
MAX_LETTERS = 1024
MAX_KEY_EXAMPLES = 8
SCOPE = (
    "Repository-specific composition of bounded classical transposition searches. "
    "English-score candidates and forward consistency do not establish family, "
    "unique plaintext, or a verified historical solve."
)


def _integer(value, name: str, low: int, high: int) -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an integer")
    if not low <= value <= high:
        raise ValueError(f"{name} must be in {low}..{high}")


def _letters(text: str, *, minimum: int = 4) -> str:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if len(text) > 4 * MAX_LETTERS or any(ch.isalpha() and not ch.isascii() for ch in text):
        raise ValueError("text must use ASCII letters within the input size bound")
    letters = "".join(ch.upper() for ch in text if ch.isascii() and ch.isalpha())
    if not minimum <= len(letters) <= MAX_LETTERS:
        raise ValueError(f"text must contain {minimum}..{MAX_LETTERS} A-Z letters")
    return letters


def _crib_positions(cribs: Sequence[Crib], length: int) -> dict[int, str]:
    if not isinstance(cribs, Sequence) or isinstance(cribs, (str, bytes, bytearray)):
        raise TypeError("cribs must be a finite sequence of Crib objects")
    if len(cribs) > 512:
        raise ValueError("at most 512 cribs are accepted")
    known: dict[int, str] = {}
    for crib in cribs:
        if not isinstance(crib, Crib):
            raise TypeError("each crib must be an engine.reverse_engineer.Crib")
        _integer(crib.offset, "crib offset", 0, length - 1)
        plain = _letters(crib.plaintext, minimum=1)
        if crib.offset + len(plain) > length:
            raise ValueError("crib exceeds normalized plaintext length")
        for position, ch in enumerate(plain, crib.offset):
            if position in known and known[position] != ch:
                raise ValueError("overlapping cribs disagree")
            known[position] = ch
    return known


@dataclass(frozen=True)
class TranspositionCandidate:
    family: str
    key: dict
    plaintext: str
    score: float
    re_encryption_matches: bool
    equivalent_keys: tuple[dict, ...]
    equivalent_keys_seen: int

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class TranspositionEnsembleReport:
    candidates: tuple[TranspositionCandidate, ...]
    checks: int
    total_checks: int
    search_complete: bool
    stop_reason: str
    family_checks: dict[str, int]
    duplicate_candidates: int
    crib_rejections: int
    re_encryption_mismatches: int
    crib_positions: int
    ciphertext_length: int
    max_candidates: int
    max_checks: int
    max_width: int
    max_rails: int
    uniqueness: str = "not_established"
    claimed_plaintext: None = None
    scope: str = SCOPE

    def to_dict(self) -> dict:
        return asdict(self)


def _keys(widths: tuple[int, ...], max_rails: int) -> dict:
    def rail():
        for rails in range(2, max_rails + 1):
            yield {"rails": rails}

    def route():
        for width in widths:
            for fill in ("rows", "cols"):
                yield {"width": width, "fill": fill, "route": "spiral-cw-top-right"}

    def columnar():
        for width in widths:
            yield {"width": width}
        for first, second in product(widths, repeat=2):
            yield {"widths": (first, second)}

    def redefence():
        for rails in range(3, max_rails + 1):
            for ranks in permutations(range(1, rails + 1)):
                for offset in range(2 * (rails - 1)):
                    yield {"ranks": "".join(map(str, ranks)), "offset": offset}

    return {"rail-fence": rail(), "route": route(), "columnar": columnar(), "redefence": redefence()}


def _route_key(key: dict) -> str:
    return f"width={key['width']};fill={key['fill']};route={key['route']}"


def _decrypt(family: str, key: dict, cipher: str) -> str:
    if family == "rail-fence":
        return rail_fence_decrypt(cipher, key["rails"])
    if family == "route":
        return route_decrypt(cipher, _route_key(key))
    if family == "columnar":
        if "widths" in key:
            return double_columnar_decrypt(cipher, *key["widths"])
        return columnar_decrypt_right_to_left(cipher, key["width"])
    if family == "redefence":
        return redefence_decrypt(cipher, key["ranks"], offset=key["offset"])
    raise ValueError("unsupported transposition family")


def _encrypt(family: str, key: dict, plain: str) -> str:
    if family == "rail-fence":
        return rail_fence_encrypt(plain, key["rails"])
    if family == "route":
        return route_encrypt(plain, _route_key(key))
    if family == "columnar":
        if "widths" in key:
            return double_columnar_encrypt(plain, *key["widths"])
        return columnar_encrypt_right_to_left(plain, key["width"])
    if family == "redefence":
        return redefence_encrypt(plain, key["ranks"], offset=key["offset"])
    raise ValueError("unsupported transposition family")


def reencrypt_transposition(candidate: TranspositionCandidate) -> str:
    """Reapply the selected existing forward transform to a returned candidate."""
    if not isinstance(candidate, TranspositionCandidate):
        raise TypeError("candidate must be a TranspositionCandidate")
    return _encrypt(candidate.family, candidate.key, candidate.plaintext)


def search_transposition_ensemble(text: str, *, max_candidates: int = 20,
                                 max_checks: int = 5000, max_width: int = 8,
                                 max_rails: int = 5, cribs: Sequence[Crib] = ()) -> TranspositionEnsembleReport:
    """Search a finite portfolio under one deterministic round-robin budget.

    A check is one decryption and independent forward-transform comparison.
    Completed search means every requested model was tested, not a unique
    reading. Only widths dividing the letter count are tested; no padding or
    null removal is invented. Cribs refer to normalized plaintext positions.
    """
    _integer(max_candidates, "max_candidates", 1, 100)
    _integer(max_checks, "max_checks", 0, 100000)
    _integer(max_width, "max_width", 2, 32)
    _integer(max_rails, "max_rails", 3, 7)
    cipher = _letters(text)
    known = _crib_positions(cribs, len(cipher))
    widths = tuple(width for width in range(2, min(max_width, len(cipher)) + 1) if len(cipher) % width == 0)
    total = (max_rails - 1 + 2 * len(widths) + len(widths) + len(widths) ** 2
             + sum(math.factorial(rails) * 2 * (rails - 1) for rails in range(3, max_rails + 1)))
    active = deque(_keys(widths, max_rails).items())
    family_checks = dict.fromkeys(FAMILIES, 0)
    checks = duplicates = rejected = mismatches = 0
    seen: set[bytes] = set()
    kept: dict[bytes, TranspositionCandidate] = {}
    model = get_model() if max_checks else None
    while active and checks < max_checks:
        family, keys = active.popleft()
        try:
            key = next(keys)
        except StopIteration:
            continue
        active.append((family, keys))
        checks += 1
        family_checks[family] += 1
        plain = _decrypt(family, key, cipher)
        if _encrypt(family, key, plain) != cipher:
            mismatches += 1
            continue
        if any(plain[position] != letter for position, letter in known.items()):
            rejected += 1
            continue
        digest = sha256(plain.encode("ascii")).digest()
        representation = {"family": family, "key": key.copy()}
        if digest in seen:
            duplicates += 1
            if digest in kept:
                candidate = kept[digest]
                examples = candidate.equivalent_keys
                if len(examples) < MAX_KEY_EXAMPLES:
                    examples += (representation,)
                kept[digest] = replace(candidate, equivalent_keys=examples,
                                       equivalent_keys_seen=candidate.equivalent_keys_seen + 1)
            continue
        seen.add(digest)
        assert model is not None
        score = model.score([ord(ch) - 65 for ch in plain])
        kept[digest] = TranspositionCandidate(family, key.copy(), plain, score, True, (representation,), 1)
        if len(kept) > max_candidates:
            weakest = min(kept, key=lambda d: (kept[d].score, tuple(-ord(ch) for ch in kept[d].plaintext)))
            del kept[weakest]
    candidates = tuple(sorted(kept.values(), key=lambda candidate: (-candidate.score, candidate.plaintext)))
    complete = checks == total
    return TranspositionEnsembleReport(candidates, checks, total, complete,
                                       "complete" if complete else "check_limit", family_checks,
                                       duplicates, rejected, mismatches, len(known), len(cipher),
                                       max_candidates, max_checks, max_width, max_rails)
