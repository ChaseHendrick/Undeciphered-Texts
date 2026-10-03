"""Supplied-key Condi with one-based plaintext feedback and punctuation.

ACA source: https://www.cryptogram.org/downloads/aca.info/ciphers/Condi.pdf
The previous plaintext letter's one-based position becomes the next offset.
The printed STRANGE alphabet is rotated left 21; initial offset is 25.
This helper does not recover an unknown keyword or claim a decipherment.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import asdict, dataclass
from engine.alphabet import ALPHABET
from engine.result import SolveResult
from engine.reverse_engineer import Crib

ACA_URL = "https://www.cryptogram.org/downloads/aca.info/ciphers/Condi.pdf"
ACA_PDF_SHA256 = "7a1bb5f1b64b8fedb20c09864535804ea83f53078426480808060eefa27156c8"
ACA_MESSAGE = "OURS IS A VERY GREEN PASTIME. THE WIDE VARIETY OF CIPHERS WE USE CAN ALL BE SOLVED WITH PENCIL AND PAPER."
ACA_PLAIN = "OURSISAVERYGREENPASTIMETHEWIDEVARIETYOFCIPHERSWEUSECANALLBESOLVEDWITHPENCILANDPAPER"
ACA_CIPHER = "MORC PP D NBKE DJKPM RTDBQCR. JPX CKTV BNHUYJG VB YSFDXKC RC ESI UOJ JYF RQ IXIMBV HKQP DNMPSB YJQ BTTNK."
MAX_TEXT_CHARACTERS = 1_000_000
_ASCII = frozenset(ALPHABET + ALPHABET.lower())


def _integer(value: int, name: str, maximum: int) -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an integer")
    if not 0 <= value <= maximum:
        raise ValueError(f"{name} must be in 0..{maximum}")


def _text(value: str, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if len(value) > MAX_TEXT_CHARACTERS:
        raise ValueError(f"{name} must not exceed {MAX_TEXT_CHARACTERS} characters")
    if any(ch.isalpha() and ch not in _ASCII for ch in value):
        raise ValueError(f"{name} must use only A-Z letters")
    if not any(ch in _ASCII for ch in value):
        raise ValueError(f"{name} must contain at least one A-Z letter")
    return value


def condi_alphabet(keyword: str, *, shift: int = 0) -> str:
    """Deduplicate the keyword, append unused A-Z, and rotate left by shift."""
    _integer(shift, "alphabet shift", 25)
    keyword = _text(keyword, "keyword")
    head = "".join(dict.fromkeys(ch.upper() for ch in keyword if ch in _ASCII))
    alphabet = head + "".join(ch for ch in ALPHABET if ch not in head)
    return alphabet[shift:] + alphabet[:shift]


def _transform(text: str, *, keyword: str, initial_offset: int, alphabet_shift: int, decrypt: bool) -> str:
    _integer(initial_offset, "initial_offset", 26)
    alphabet = condi_alphabet(keyword, shift=alphabet_shift)
    text = _text(text, "text")
    positions = {letter: index for index, letter in enumerate(alphabet)}
    offset = initial_offset
    output = []
    for character in text:
        if character not in _ASCII:
            output.append(character)
            continue
        position = positions[character.upper()]
        plain_position = (position - offset) % 26 if decrypt else position
        output.append(alphabet[plain_position] if decrypt else alphabet[(position + offset) % 26])
        offset = plain_position + 1
    return "".join(output)


def condi_encrypt(text: str, *, keyword: str, initial_offset: int, alphabet_shift: int = 0) -> str:
    """Encrypt A-Z letters, retaining non-letter separators and word divisions."""
    return _transform(text, keyword=keyword, initial_offset=initial_offset, alphabet_shift=alphabet_shift, decrypt=False)


def condi_decrypt(text: str, *, keyword: str, initial_offset: int, alphabet_shift: int = 0) -> str:
    """Decrypt with the supplied keyed alphabet settings and feedback offset."""
    return _transform(text, keyword=keyword, initial_offset=initial_offset, alphabet_shift=alphabet_shift, decrypt=True)


def solve_condi(text: str, *, keyword: str, initial_offset: int, alphabet_shift: int = 0) -> SolveResult:
    plaintext = condi_decrypt(text, keyword=keyword, initial_offset=initial_offset, alphabet_shift=alphabet_shift)
    alphabet = condi_alphabet(keyword, shift=alphabet_shift)
    key = f"alphabet={alphabet} initial_offset={initial_offset}"
    return SolveResult("condi", plaintext, key, float(sum(ch in _ASCII for ch in plaintext)), {
        "mode": "known_key", "alphabet": alphabet, "initial_offset": initial_offset,
        "alphabet_shift": alphabet_shift, "feedback_positions": "one-based", "source_url": ACA_URL,
        "scope": "Supplied-key classical Condi. No unknown keyword recovery or unknown-script reading is claimed.",
    })


@dataclass(frozen=True)
class CondiCandidate:
    keyword: str
    alphabet_shift: int
    initial_offset: int
    predicted_plaintext: str


@dataclass(frozen=True)
class CondiInferenceReport:
    ciphertext_length: int
    known_positions: int
    candidates: tuple[CondiCandidate, ...]
    checks: int
    search_complete: bool
    exhausted: bool
    exhaustion_reason: str
    bounds: dict
    claimed_plaintext: None = None
    scope: str = "Conditional crib-compatible Condi candidates from the supplied finite keyword list and settings. No exhaustive alphabet search or historical decipherment is claimed."

    def to_dict(self) -> dict:
        return asdict(self)


def _sequence(value, name: str, maximum: int) -> tuple:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise TypeError(f"{name} must be a finite sequence")
    if not 1 <= len(value) <= maximum:
        raise ValueError(f"{name} must contain 1..{maximum} entries")
    return tuple(value)


def infer_condi(
    ciphertext: str, *, keywords: Sequence[str], cribs: Sequence[Crib],
    alphabet_shifts: Sequence[int] = tuple(range(26)), initial_offsets: Sequence[int] = tuple(range(26)),
    max_checks: int = 4096, max_candidates: int = 1000,
) -> CondiInferenceReport:
    """Test supplied dictionary keywords and bounded shifts/starting offsets.

    Uses the same Crib and zero-based normalized A-Z positions as the
    Progressive Key inference API. The keyword itself is not given as a
    selected key. Every dictionary entry is explicitly part of the bounds.
    """
    _integer(max_checks, "max_checks", 100_000)
    _integer(max_candidates, "max_candidates", 10_000)
    if max_candidates == 0:
        raise ValueError("max_candidates must be positive")
    original = _text(ciphertext, "ciphertext")
    cipher = "".join(ch.upper() for ch in original if ch in _ASCII)
    if len(cipher) > 512:
        raise ValueError("Condi inference accepts at most 512 A-Z letters")
    heads = []
    for keyword in _sequence(keywords, "keywords", 256):
        if not isinstance(keyword, str):
            raise TypeError("dictionary keywords must be strings")
        if len(keyword) > 128:
            raise ValueError("dictionary keywords must contain at most 128 characters")
        head = "".join(dict.fromkeys(ch.upper() for ch in _text(keyword, "keyword") if ch in _ASCII))
        if head not in heads:
            heads.append(head)
    shifts = _sequence(alphabet_shifts, "alphabet_shifts", 26)
    offsets = _sequence(initial_offsets, "initial_offsets", 27)
    for shift in shifts:
        _integer(shift, "alphabet shift", 25)
    for offset in offsets:
        _integer(offset, "initial offset", 26)
    shifts = tuple(dict.fromkeys(shifts))
    offsets = tuple(dict.fromkeys(offset % 26 for offset in offsets))
    known = {}
    for crib in _sequence(cribs, "cribs", 512):
        if not isinstance(crib, Crib):
            raise TypeError("cribs must contain engine.reverse_engineer.Crib objects")
        _integer(crib.offset, "crib offset", len(cipher) - 1)
        plain = "".join(ch.upper() for ch in _text(crib.plaintext, "crib plaintext") if ch in _ASCII)
        if crib.offset + len(plain) > len(cipher):
            raise ValueError("crib extends beyond the A-Z ciphertext stream")
        for index, letter in enumerate(plain, start=crib.offset):
            if index in known and known[index] != letter:
                raise ValueError("overlapping cribs disagree")
            known[index] = letter
    candidates = []
    checks = 0
    reason = ""
    for head in heads:
        for shift in shifts:
            for offset in offsets:
                if checks >= max_checks:
                    reason = "check_limit"
                    break
                if len(candidates) >= max_candidates:
                    reason = "candidate_limit"
                    break
                checks += 1
                prediction = condi_decrypt(cipher, keyword=head, initial_offset=offset, alphabet_shift=shift)
                if all(prediction[index] == letter for index, letter in known.items()):
                    candidates.append(CondiCandidate(head, shift, offset, prediction))
            if reason:
                break
        if reason:
            break
    return CondiInferenceReport(len(cipher), len(known), tuple(candidates), checks, not reason, bool(reason), reason,
                                {"keywords": heads, "alphabet_shifts": list(shifts), "initial_offsets": list(offsets),
                                 "max_checks": max_checks, "max_candidates": max_candidates, "max_letters": 512})
