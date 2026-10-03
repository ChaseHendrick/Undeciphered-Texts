"""Supplied-key ACA Periodic Gromark, with explicit numeric framing.

https://www.cryptogram.org/downloads/aca.info/ciphers/PeriodicGromark.pdf
The deduplicated keyword determines both the period and rank-digit primer.
Each period group's keyword letter rotates the Gromark ciphertext alphabet.
This implementation supports 2..9 distinct keyword letters, so each rank
is one unambiguous decimal digit. No wider-rank convention is assumed.
"""

from __future__ import annotations

import re
from engine.alphabet import ALPHABET
from engine.result import SolveResult
from engine.solvers.gromark import gromark_cipher_alphabet

ACA_URL = "https://www.cryptogram.org/downloads/aca.info/ciphers/PeriodicGromark.pdf"
ACA_PDF_SHA256 = "0c9e566b76a61af11d36572560a468550cf7b49501150c8523e06091436e7a13"
ACA_PLAIN = "WINTRYSHOWERSWILLCONTINUEFORTHENEXTFEWDAYSACCORDINGTOTHEFORECAST"
ACA_CIPHER = "RHNAAXNRUZBNIUARXCRTPATBRLIGDSVCIRCVOYPVRAAZZMUSREQYEVMMURGWTLUD"
ACA_PRINTED_CIPHER = "264351 RHNAAX NRUZBN IUARXC RTPATB RLIGDS VCIRCV OYPVRA AZZMUS REQYEV MMURGW TLUD 4."
MAX_LETTERS = 1_000_000
MAX_FRAMED_CHARACTERS = 1_500_032
_ASCII = frozenset(ALPHABET + ALPHABET.lower())


def _letters(value: str, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if len(value) > MAX_LETTERS:
        raise ValueError(f"{name} must not exceed {MAX_LETTERS} characters")
    if any((ch.isalpha() and ch not in _ASCII) or ch.isdigit() for ch in value):
        raise ValueError(f"{name} must contain A-Z letters without numeric framing")
    cleaned = "".join(ch.upper() for ch in value if ch in _ASCII)
    if not cleaned:
        raise ValueError(f"{name} must contain A-Z letters")
    return cleaned


def periodic_gromark_keyword(keyword: str) -> str:
    """Deduplicate repeated letters, as the ACA REPEATED -> REPATD example."""
    head = "".join(dict.fromkeys(_letters(keyword, "keyword")))
    if not 2 <= len(head) <= 9:
        raise ValueError("Periodic Gromark supports 2..9 distinct keyword letters")
    return head


def periodic_gromark_primer(keyword: str) -> str:
    head = periodic_gromark_keyword(keyword)
    ranks = {letter: index + 1 for index, letter in enumerate(sorted(head))}
    return "".join(str(ranks[letter]) for letter in head)


def periodic_gromark_alphabet(keyword: str) -> str:
    return gromark_cipher_alphabet(periodic_gromark_keyword(keyword))


def periodic_gromark_running_key(keyword: str, length: int) -> str:
    """Extend the rank primer by adjacent chain addition modulo ten."""
    if not isinstance(length, int) or isinstance(length, bool):
        raise TypeError("running key length must be an integer")
    if not 0 <= length <= MAX_LETTERS:
        raise ValueError(f"running key length must be in 0..{MAX_LETTERS}")
    digits = [int(ch) for ch in periodic_gromark_primer(keyword)]
    width = len(digits)
    while len(digits) < length:
        digits.append((digits[-width] + digits[-width + 1]) % 10)
    return "".join(str(digit) for digit in digits[:length])


def _transform(text: str, keyword: str, decrypt: bool) -> str:
    head = periodic_gromark_keyword(keyword)
    letters = _letters(text, "text")
    alphabet = periodic_gromark_alphabet(head)
    positions = {letter: index for index, letter in enumerate(alphabet)}
    running = periodic_gromark_running_key(head, len(letters))
    starts = [positions[letter] for letter in head]
    output = []
    for index, (letter, digit) in enumerate(zip(letters, running)):
        shift = starts[(index // len(head)) % len(head)] + int(digit)
        output.append(ALPHABET[(positions[letter] - shift) % 26] if decrypt
                      else alphabet[(ord(letter) - 65 + shift) % 26])
    return "".join(output)


def periodic_gromark_frame(ciphertext: str, *, keyword: str) -> str:
    head = periodic_gromark_keyword(keyword)
    body = _letters(ciphertext, "ciphertext body")
    groups = " ".join(body[index:index + len(head)] for index in range(0, len(body), len(head)))
    check = periodic_gromark_running_key(head, len(body))[-1]
    return f"{periodic_gromark_primer(head)} {groups} {check}."


def periodic_gromark_unframe(text: str, *, keyword: str) -> str:
    head = periodic_gromark_keyword(keyword)
    if not isinstance(text, str):
        raise TypeError("framed ciphertext must be a string")
    if len(text) > MAX_FRAMED_CHARACTERS:
        raise ValueError("framed ciphertext exceeds the character bound")
    tokens = text.split()
    if len(tokens) < 3 or tokens[0] != periodic_gromark_primer(head) or not re.fullmatch(r"[0-9]\.?", tokens[-1]):
        raise ValueError("frame must contain the derived rank primer, ciphertext body, and final check digit")
    body = _letters("".join(tokens[1:-1]), "ciphertext body")
    expected = periodic_gromark_running_key(head, len(body))[-1]
    if tokens[-1][0] != expected:
        raise ValueError("frame check digit disagrees with the chain-added key")
    return body


def periodic_gromark_encrypt(text: str, *, keyword: str, framed: bool = False) -> str:
    if not isinstance(framed, bool):
        raise TypeError("framed must be a boolean")
    body = _transform(text, keyword, False)
    return periodic_gromark_frame(body, keyword=keyword) if framed else body


def periodic_gromark_decrypt(text: str, *, keyword: str, framed: bool = False) -> str:
    if not isinstance(framed, bool):
        raise TypeError("framed must be a boolean")
    body = periodic_gromark_unframe(text, keyword=keyword) if framed else text
    return _transform(body, keyword, True)


def solve_periodic_gromark(text: str, *, keyword: str, framed: bool = False) -> SolveResult:
    head = periodic_gromark_keyword(keyword)
    plaintext = periodic_gromark_decrypt(text, keyword=head, framed=framed)
    primer = periodic_gromark_primer(head)
    return SolveResult("periodic-gromark", plaintext, head, float(len(plaintext)), {
        "mode": "known_key", "keyword": head, "primer": primer, "period": len(head),
        "ciphertext_alphabet": periodic_gromark_alphabet(head), "framing_checked": framed,
        "source_url": ACA_URL, "scope": "Supplied-key classical Periodic Gromark; no unknown-key recovery or historical decipherment is claimed.",
    })
