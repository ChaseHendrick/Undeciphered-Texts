"""Infer compatible letter-cipher rules from aligned known plaintext cribs.

Models are Caesar/affine, monoalphabetic substitution, and repeating
Vigenere or Beaufort. Every supplied position must agree. Missing key slots
stay unknown. Predicted text is conditional on the model, never a claimed
decipherment. The period cap makes this a finite model test.

ACA formulas: https://www.cryptogram.org/downloads/aca.info/ciphers/Vigenere.pdf
https://www.cryptogram.org/downloads/aca.info/ciphers/Beaufort.pdf
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from math import gcd
from collections.abc import Sequence

from engine.alphabet import ALPHABET

MAX_PERIOD = 128
_ASCII = frozenset(ALPHABET + ALPHABET.lower())
SCOPE = (
    "Compatible hypotheses inside the stated A-Z cipher families and period bound. "
    "Fitting a crib does not verify the model or the text outside it. "
    "Unknown slots remain ?. No unknown-script or unsolved-text decipherment is claimed."
)


@dataclass(frozen=True)
class Crib:
    offset: int
    plaintext: str


@dataclass(frozen=True)
class CipherHypothesis:
    family: str
    period: int | None
    key: str
    parameters: dict
    confirmations: int
    unresolved_parameters: int
    predicted_plaintext: str
    predicted_positions: int


@dataclass(frozen=True)
class ReverseEngineeringReport:
    ciphertext_length: int
    known_positions: int
    max_period: int
    hypotheses: tuple[CipherHypothesis, ...]
    claimed_plaintext: None = None
    scope: str = SCOPE

    def to_dict(self) -> dict:
        return asdict(self)


def _letters(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if any(ch.isalpha() and ch not in _ASCII for ch in text):
        raise ValueError("model inference accepts A-Z letters only")
    cleaned = "".join(ch.upper() for ch in text if ch in _ASCII)
    if not cleaned:
        raise ValueError("text must contain at least one A-Z letter")
    return cleaned


def _integer(value: int, name: str, minimum: int) -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an integer")
    if value < minimum:
        raise ValueError(f"{name} must be at least {minimum}")


def predict_plaintext(text: str, hypothesis: CipherHypothesis, *, offset: int = 0) -> str:
    """Conditional A-Z prediction. Unknown mappings or key slots produce ?."""
    _integer(offset, "offset", 0)
    cipher = _letters(text)
    params = hypothesis.parameters
    if hypothesis.family in ("caesar", "affine"):
        inverse = pow(params["multiplier"], -1, 26)
        return "".join(ALPHABET[((ord(ch) - 65 - params["offset"]) * inverse) % 26] for ch in cipher)
    if hypothesis.family == "substitution":
        inverse = {value: plain for plain, value in params["mapping"].items()}
        return "".join(inverse.get(ch, "?") for ch in cipher)
    if hypothesis.family not in ("vigenere", "beaufort"):
        raise ValueError("unsupported hypothesis family")
    slots = params["key_slots"]
    out = []
    for index, ch in enumerate(cipher):
        shift = slots[(offset + index) % hypothesis.period]
        if shift is None:
            out.append("?")
        elif hypothesis.family == "vigenere":
            out.append(ALPHABET[(ord(ch) - 65 - shift) % 26])
        else:
            out.append(ALPHABET[(shift - ord(ch) + 65) % 26])
    return "".join(out)


def infer_cipher_models(
    ciphertext: str, *, cribs: Sequence[Crib], max_period: int = 16,
) -> ReverseEngineeringReport:
    """Fit all supported models to all cribs, using zero-based letter offsets.

    Offsets refer to the ciphertext after spaces and punctuation are removed.
    Affine trials use the 12 invertible multipliers and 26 offsets. Repeating
    models test periods 1 through min(max_period, ciphertext length). The
    substitution model keeps a partial one-to-one map, without filling gaps.
    """
    cipher = _letters(ciphertext)
    _integer(max_period, "max_period", 1)
    if max_period > MAX_PERIOD:
        raise ValueError(f"max_period must not exceed {MAX_PERIOD}")
    if not cribs:
        raise ValueError("at least one aligned crib is required")
    known: dict[int, int] = {}
    for crib in cribs:
        if not isinstance(crib, Crib):
            raise TypeError("cribs must contain Crib objects")
        _integer(crib.offset, "crib offset", 0)
        plain = _letters(crib.plaintext)
        if crib.offset + len(plain) > len(cipher):
            raise ValueError("crib extends beyond the ciphertext letter stream")
        for index, ch in enumerate(plain, start=crib.offset):
            value = ord(ch) - 65
            if index in known and known[index] != value:
                raise ValueError("overlapping cribs disagree")
            known[index] = value
    if not known:
        raise ValueError("at least one aligned crib is required")
    constraints = [(index, plain, ord(cipher[index]) - 65) for index, plain in sorted(known.items())]
    hypotheses: list[CipherHypothesis] = []

    def add(family: str, period: int | None, key: str, parameters: dict,
            confirmations: int, unresolved: int) -> None:
        draft = CipherHypothesis(family, period, key, parameters, confirmations, unresolved, "", 0)
        prediction = predict_plaintext(cipher, draft)
        hypotheses.append(CipherHypothesis(
            family, period, key, parameters, confirmations, unresolved,
            prediction, len(prediction) - prediction.count("?"),
        ))

    for multiplier in range(26):
        if gcd(multiplier, 26) != 1:
            continue
        for shift in range(26):
            if all((multiplier * plain + shift) % 26 == encoded for _, plain, encoded in constraints):
                add("caesar" if multiplier == 1 else "affine", None,
                    f"a={multiplier} b={shift}", {"multiplier": multiplier, "offset": shift},
                    max(0, len(constraints) - (1 if multiplier == 1 else 2)), 0)

    mapping: dict[str, str] = {}
    inverse: dict[str, str] = {}
    for _, plain, encoded in constraints:
        source, dest = ALPHABET[plain], ALPHABET[encoded]
        if (source in mapping and mapping[source] != dest) or (dest in inverse and inverse[dest] != source):
            break
        mapping[source], inverse[dest] = dest, source
    else:
        add("substitution", None, "".join(mapping.get(ch, "?") for ch in ALPHABET),
            {"mapping": mapping}, len(constraints) - len(mapping), 26 - len(mapping))

    for family in ("vigenere", "beaufort"):
        for period in range(1, min(max_period, len(cipher)) + 1):
            slots: list[int | None] = [None] * period
            confirmations = 0
            for index, plain, encoded in constraints:
                shift = (encoded - plain if family == "vigenere" else encoded + plain) % 26
                slot = index % period
                if slots[slot] is not None:
                    if slots[slot] != shift:
                        break
                    confirmations += 1
                slots[slot] = shift
            else:
                add(family, period, "".join("?" if slot is None else ALPHABET[slot] for slot in slots),
                    {"key_slots": slots}, confirmations, slots.count(None))

    return ReverseEngineeringReport(len(cipher), len(known), max_period, tuple(hypotheses))


__all__ = ["Crib", "CipherHypothesis", "ReverseEngineeringReport", "infer_cipher_models", "predict_plaintext"]
