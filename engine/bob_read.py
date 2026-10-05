"""Bob tries a reader after he names a family. This is not a historical decipherment.

He writes each step on a scratch pad. Caesar and Vigenere are the families
he can search. Any other family is withheld, including a digit cipher that
is too short to featurize. The pad stores a key and a hash when the judge
accepts the forward map. It does not store the letters. A matching key on
a synthetic drill is not a reading of an unsolved text, and solved stays false.
"""

from __future__ import annotations

import hashlib

from engine.alphabet import letters_only
from engine.bob_lift import lifted_family
from engine.bob_scratch import open_pad, pad_digest, write_note
from engine.ciphers import caesar_encrypt, substitution_encrypt, vigenere_encrypt
from engine.dagapeyeff_cache import frozen
from engine.neural_grade import letters_az, load_training_prose
from engine.solver_judge import judge_solve_result
from engine.solvers.beaufort import beaufort_encrypt
from engine.solvers.caesar import solve_caesar
from engine.solvers.vigenere import solve_vigenere

_READABLE = ("caesar", "vigenere")
_SHIFTS = (3, 7, 11, 13, 17, 19, 23, 25)
_KEYS = ("KEY", "CODE", "QUARK", "LEMON", "NIGHT", "STONE")
_PERMUTATION = "QWERTYUIOPASDFGHJKLZXCVBNM"
_WIDTH = 160


def _sha(text: str) -> str:
    return hashlib.sha256(letters_only(text).encode("ascii")).hexdigest()


def _window(prose: str, index: int) -> str:
    start = index * 350
    return prose[start : start + _WIDTH]


def try_read(text: str) -> dict:
    """Name a family, then search only if Bob has a reader. No plaintext comes back."""
    if not isinstance(text, str):
        raise TypeError("ciphertext must be text")
    pad = open_pad()
    letters = letters_only(text)
    if len(letters) < 16:
        write_note(pad, step="reject", note="too short")
        return _closed(pad, withheld=True, reason="too short")
    family = lifted_family(text)
    write_note(pad, step="route", family=family)
    if family not in _READABLE:
        write_note(pad, step="withhold", family=family, note="no reader")
        return _closed(pad, withheld=True, reason="no reader", family=family)
    result = solve_caesar(text) if family == "caesar" else solve_vigenere(text)
    judged = judge_solve_result(result, text)
    accepted = bool(judged["accepted"])
    write_note(
        pad,
        step="read",
        method=result.method,
        key=result.key if accepted else None,
        score=round(float(result.score), 3),
        matched=accepted,
        sha256=judged["plaintext_sha256"] if accepted else None,
    )
    return _closed(
        pad,
        withheld=not accepted,
        reason=None if accepted else "judge withheld",
        family=family,
        method=result.method,
        key=result.key if accepted else None,
        score=round(float(result.score), 6),
        consistent=judged["reencryption_matches"] is True,
        sha256=judged["plaintext_sha256"] if accepted else None,
    )


def _closed(pad: list[dict], **fields) -> dict:
    body = {
        "solved": False,
        "claimed_plaintext": None,
        "family": fields.get("family"),
        "method": fields.get("method"),
        "key": fields.get("key"),
        "score": fields.get("score"),
        "consistent": bool(fields.get("consistent")),
        "withheld": bool(fields.get("withheld")),
        "reason": fields.get("reason"),
        "sha256": fields.get("sha256"),
        "pad_lines": len(pad),
        "pad_digest": pad_digest(pad),
        "scope": (
            "A key from a Caesar or Vigenere search is a forward check on the family Bob named. "
            "It is not a reading, and the pad does not keep the letters."
        ),
    }
    return body


def _matched(original: str, reading: dict) -> bool:
    return bool(reading["sha256"]) and reading["sha256"] == _sha(original) and reading["consistent"]


@frozen("bob-read")
def bob_read_report() -> dict:
    """Drill the reader on training prose. Counts only. The weight file stays."""
    prose = letters_az(load_training_prose())
    if len(prose) < 8 * 350 + _WIDTH:
        raise RuntimeError("training prose is shorter than the reader drill")
    caesar_routed = caesar_matched = 0
    for index, shift in enumerate(_SHIFTS):
        original = _window(prose, index)
        reading = try_read(caesar_encrypt(original, shift))
        caesar_routed += reading["family"] == "caesar"
        caesar_matched += _matched(original, reading) and reading["key"] == str(shift)
    vigenere_routed = vigenere_matched = 0
    for index, key in enumerate(_KEYS):
        original = _window(prose, index + 8)
        reading = try_read(vigenere_encrypt(original, key))
        vigenere_routed += reading["family"] == "vigenere"
        vigenere_matched += _matched(original, reading) and reading["key"] == key
    substitution_withheld = substitution_false = substitution_misroute = 0
    for index in range(4):
        original = _window(prose, index + 14)
        reading = try_read(substitution_encrypt(original, _PERMUTATION))
        if reading["family"] not in _READABLE:
            substitution_withheld += 1
        elif _matched(original, reading):
            substitution_false += 1
        else:
            substitution_misroute += 1
    beaufort_withheld = beaufort_false = beaufort_misroute = 0
    for index, key in enumerate(_KEYS[:4]):
        original = _window(prose, index + 18)
        reading = try_read(beaufort_encrypt(original, key))
        if reading["family"] not in _READABLE:
            beaufort_withheld += 1
        elif _matched(original, reading):
            beaufort_false += 1
        else:
            beaufort_misroute += 1
    short = try_read("AAAA")
    digits = try_read("5" * 24)
    proverb = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG " * 3
    proverb_reading = try_read(caesar_encrypt(proverb.strip(), 5))
    return {
        "solved": False,
        "claimed_plaintext": None,
        "weights_replaced": False,
        "caesar_texts": len(_SHIFTS),
        "caesar_routed": caesar_routed,
        "caesar_matched": caesar_matched,
        "vigenere_texts": len(_KEYS),
        "vigenere_routed": vigenere_routed,
        "vigenere_matched": vigenere_matched,
        "substitution_texts": 4,
        "substitution_withheld": substitution_withheld,
        "substitution_false_match": substitution_false,
        "substitution_misroute": substitution_misroute,
        "beaufort_texts": 4,
        "beaufort_withheld": beaufort_withheld,
        "beaufort_false_match": beaufort_false,
        "beaufort_misroute": beaufort_misroute,
        "short_withheld": short["withheld"] and short["reason"] == "too short",
        "digit_withheld": digits["withheld"] and digits["reason"] == "too short",
        "proverb_family": proverb_reading["family"],
        "proverb_withheld": proverb_reading["withheld"],
        "proverb_matched": _matched(proverb, proverb_reading),
        "promoted": False,
        "scope": (
            "Bob can search Caesar and Vigenere after he names them. "
            "A match on this drill is not a reading. The weight file stays."
        ),
    }
