"""ACA Homophonic: four cyclic numeric rows, plus bounded crib inference.

Primary source: https://www.cryptogram.org/downloads/aca.info/ciphers/Homophonic.pdf
This structured four-row family differs from arbitrary homophonic substitution.
"""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import asdict, dataclass
from math import prod
import string
from engine.result import SolveResult
from engine.reverse_engineer import Crib

SOURCE_URL = "https://www.cryptogram.org/downloads/aca.info/ciphers/Homophonic.pdf"
ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
MAX_LETTERS = 4096
MAX_INFERENCE_LETTERS = 512


def _letters(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("plaintext, key and crib must be strings")
    if len(text) > 16384 or any(ch not in string.ascii_letters + string.whitespace + string.punctuation for ch in text):
        raise ValueError("letter input must use bounded ASCII letters, whitespace or punctuation, without digits")
    letters = "".join(ch.upper() for ch in text if ch in string.ascii_letters).replace("J", "I")
    if not 1 <= len(letters) <= MAX_LETTERS:
        raise ValueError("letter input must contain 1..4096 letters")
    return letters


def _key(key: str) -> str:
    if not isinstance(key, str):
        raise TypeError("key must be a string")
    if len(key) > 128 or any(ch not in string.ascii_letters + string.whitespace for ch in key):
        raise ValueError("key must contain exactly four ASCII letters with optional whitespace")
    letters = _letters(key)
    if len(letters) != 4:
        raise ValueError("key must contain exactly four letters after the I/J merge")
    return letters


def homophonic_table(key: str) -> tuple[tuple[int, ...], ...]:
    """Return four numeric rows under the straight 25-letter alphabet."""
    shifts = tuple(ALPHABET.index(letter) for letter in _key(key))
    return tuple(tuple(((column - shift) % 25 + 1 + 25 * row) % 100
                       for column in range(25)) for row, shift in enumerate(shifts))


def homophonic_encrypt(text: str, *, key: str, rows: Sequence[int] | None = None) -> str:
    plain = _letters(text)
    table = homophonic_table(key)
    if rows is None:
        selections = (0,) * len(plain)
    elif isinstance(rows, Sequence) and not isinstance(rows, (str, bytes, bytearray)):
        if len(rows) != len(plain):
            raise ValueError("rows must provide one homophone row per plaintext letter")
        selections = rows
    else:
        raise TypeError("rows must be a finite integer sequence")
    output = []
    for letter, row in zip(plain, selections):
        if not isinstance(row, int) or isinstance(row, bool):
            raise TypeError("row choices must be integers")
        if not 0 <= row <= 3:
            raise ValueError("row choices must be in 0..3")
        output.append(f"{table[row][ALPHABET.index(letter)]:02d}")
    return " ".join(output)


def _codes(text: str, terminal_period: bool) -> tuple[int, ...]:
    if not isinstance(text, str):
        raise TypeError("ciphertext must be a string of two-digit code tokens")
    if not isinstance(terminal_period, bool):
        raise TypeError("terminal_period must be Boolean")
    if len(text) > 16384:
        raise ValueError("ciphertext exceeds 16384 raw characters")
    body = text.strip()
    if terminal_period and body.endswith("."):
        body = body[:-1]
    if any(ch not in string.digits + string.whitespace for ch in body):
        raise ValueError("ciphertext must contain ASCII digit tokens and whitespace")
    tokens = body.split()
    if not 1 <= len(tokens) <= MAX_LETTERS or any(len(token) != 2 for token in tokens):
        raise ValueError("ciphertext must contain 1..4096 two-digit codes 00..99")
    return tuple(int(token) for token in tokens)


def _row_position(code: int) -> tuple[int, int]:
    # 00 denotes the hundredth entry, not an entry before 01.
    return divmod((code - 1) % 100, 25)


def homophonic_decrypt(text: str, *, key: str, terminal_period: bool = False) -> str:
    shifts = tuple(ALPHABET.index(letter) for letter in _key(key))
    return "".join(ALPHABET[(position + shifts[row]) % 25]
                   for row, position in map(_row_position, _codes(text, terminal_period)))


def solve_homophonic(text: str, *, key: str, terminal_period: bool = False) -> SolveResult:
    plain = homophonic_decrypt(text, key=key, terminal_period=terminal_period)
    return SolveResult("homophonic", plain, _key(key), float(len(plain)),
                       {"mode": "supplied_key", "lost_word_spaces": True,
                        "letter_merges": {"J": "I"}, "source_url": SOURCE_URL,
                        "scope": "The ACA four-row homophonic family with supplied keyword; not arbitrary homophonic recovery."})


@dataclass(frozen=True)
class HomophonicInferenceReport:
    checks: int
    search_complete: bool
    stop_reason: str
    key_pattern: str | None
    key_slots: tuple[int | None, ...] | None
    row_key_options: tuple[str, ...] | None
    compatible_key_count: int | None
    predicted_plaintext: str | None
    known_positions: int
    ciphertext_length: int
    bounds: dict
    claimed_plaintext: None = None
    scope: str = "Conditional on the ACA four-row construction and supplied aligned cribs; no historical solution is claimed."

    def to_dict(self) -> dict:
        return asdict(self)


def infer_homophonic(text: str, *, cribs: Sequence[Crib], max_checks: int = 100,
                     terminal_period: bool = False) -> HomophonicInferenceReport:
    """Test the 25 possible key letters per row, retaining unobserved rows.

    One check tests one row/shift against all aligned evidence in that row.
    Independent rows give an exact compatible-key count on completion without
    enumerating up to 25**4 full keys. Exhaustion makes no partial prediction.
    """
    if not isinstance(max_checks, int) or isinstance(max_checks, bool):
        raise TypeError("max_checks must be an integer")
    if not 0 <= max_checks <= 100:
        raise ValueError("max_checks must be in 0..100")
    codes = _codes(text, terminal_period)
    if len(codes) > MAX_INFERENCE_LETTERS:
        raise ValueError("inference accepts at most 512 code tokens")
    if not isinstance(cribs, Sequence) or isinstance(cribs, (str, bytes, bytearray)):
        raise TypeError("cribs must be a finite sequence of Crib objects")
    if not 1 <= len(cribs) <= 128:
        raise ValueError("inference requires 1..128 aligned cribs")
    known = {}
    for crib in cribs:
        if not isinstance(crib, Crib):
            raise TypeError("each crib must be an engine.reverse_engineer.Crib")
        if not isinstance(crib.offset, int) or isinstance(crib.offset, bool):
            raise TypeError("crib offsets must be integer letter positions")
        plain = _letters(crib.plaintext)
        if crib.offset < 0 or crib.offset + len(plain) > len(codes):
            raise ValueError("crib exceeds the normalized plaintext letter coordinates")
        for position, letter in enumerate(plain, crib.offset):
            if position in known and known[position] != letter:
                raise ValueError("overlapping cribs contradict one another")
            known[position] = letter
    constraints = [[] for _ in range(4)]
    for index, letter in known.items():
        row, position = _row_position(codes[index])
        constraints[row].append((position, ALPHABET.index(letter)))
    bounds = {"max_checks": max_checks, "total_row_shift_checks": 100,
              "max_ciphertext_letters": MAX_INFERENCE_LETTERS,
              "check_unit": "one row/key-letter shift against all aligned cribs in that row"}
    options = [[] for _ in range(4)]
    checks = 0
    for row in range(4):
        for shift in range(25):
            if checks >= max_checks:
                return HomophonicInferenceReport(checks, False, "check_limit", None, None, None,
                                                  None, None, len(known), len(codes), bounds)
            checks += 1
            if all((position + shift) % 25 == expected for position, expected in constraints[row]):
                options[row].append(shift)
    count = prod(len(row) for row in options)
    option_letters = tuple("".join(ALPHABET[index] for index in row) for row in options)
    if count == 0:
        return HomophonicInferenceReport(checks, True, "incompatible_cribs", None, None,
                                          option_letters, 0, None, len(known), len(codes), bounds)
    slots = tuple(row[0] if len(row) == 1 else None for row in options)
    pattern = "".join(ALPHABET[index] if index is not None else "?" for index in slots)
    prediction = "".join(ALPHABET[(position + slots[row]) % 25] if slots[row] is not None else "?"
                         for row, position in map(_row_position, codes))
    return HomophonicInferenceReport(checks, True, "complete", pattern, slots, option_letters,
                                      count, prediction, len(known), len(codes), bounds)
