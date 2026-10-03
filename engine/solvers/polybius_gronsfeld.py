"""Polybius square plus digit Gronsfeld, with the null periods named in Codes and Ciphers.

Alexander D'Agapeyeff's 1939 challenge is a digit cryptogram. The same book
shows a Polybius square (coordinates A–E) and, on p. 111, says a dummy may be
inserted at every third, fourth, or fifth letter after a message is enciphered.
Wikipedia quotes both and still calls the challenge unsolved:

  https://en.wikipedia.org/wiki/D%27Agapeyeff_cipher

This module is that family, built so a search can be tested:

  1. 5×5 keyword Polybius, I/J merged, row-major coordinates 1..5.
  2. A repeating numeric key added to each coordinate digit, modulo 10.
  3. Optional null digits in one residue class of every 3rd, 4th, or 5th place.

`solve_polybius_gronsfeld` is not given the keyword, the numeric key, or the
null period. It keeps only streams whose every digit falls back into 1..5,
then ranks those plaintexts with the English quadgram model. A historical
digit string that never lands entirely in 1..5 has no decryption in this
family. Nothing here claims the 1939 challenge.
"""

from __future__ import annotations

from pathlib import Path

from engine.alphabet import letters_only, to_ints
from engine.ciphers import square_from_keyword, two_square_letters
from engine.language import get_model
from engine.result import SolveResult

# Wikipedia "D'Agapeyeff cipher", fetched 2026-10-02. Groups of five as printed.
# https://en.wikipedia.org/wiki/D%27Agapeyeff_cipher
DAGAPEYEFF_GROUPED = (
    "75628 28591 62916 48164 91748 58464 74748 28483 81638 18174 "
    "74826 26475 83828 49175 74658 37575 75936 36565 81638 17585 "
    "75756 46282 92857 46382 75748 38165 81848 56485 64858 56382 "
    "72628 36281 81728 16463 75828 16483 63828 58163 63630 47481 "
    "91918 46385 84656 48565 62946 26285 91859 17491 72756 46575 "
    "71658 36264 74818 28462 82649 18193 65626 48484 91838 57491 "
    "81657 27483 83858 28364 62726 26562 83759 27263 82827 27283 "
    "82858 47582 81837 28462 82837 58164 75748 58162 92000"
)
DAGAPEYEFF_SOURCE = "https://en.wikipedia.org/wiki/D%27Agapeyeff_cipher"

# Worked Polybius example on the same page (letter coordinates, not the challenge).
# Square rows A–E, columns A–E. Blank cells are the page's asterisks.
BOOK_POLYBIUS_SQUARE = (
    ("S", "D", "U", "M", "I"),
    ("F", "W", "A", "O", "Y"),
    ("V", "N", None, "T", "E"),
    ("L", "H", "R", "C", "Q"),
    ("B", "P", "K", None, None),
)
BOOK_POLYBIUS_CIPHER = (
    "CDDBC ECBCE BBEBD ABCCB BDBAB CCDCD BCDDE CAECB DDDAA CABCE "
    "AABDE BCEDC BCCDA EBDCB AAEAB ECDDB DCCEC EEABD ADEAD CAADE "
    "ACABD CBDCB AABDC ACEDC BABCD DCDBD DCBEB CDCBE BCAAB DACCD "
    "DBBBC EAACD BDCDD BCEDC AECAC EDC"
)
BOOK_POLYBIUS_NOTE = (
    "Wikipedia prints the intended reading, including a mis-encoding of E as BE "
    "rather than CE, and glosses ARYA as AREA."
)

NULL_PERIODS = (3, 4, 5)
_CORPUS = Path(__file__).resolve().parent.parent / "data" / "english.txt"
_COORD = {ch: i for i, ch in enumerate("ABCDE")}


def digits_only(text: str) -> str:
    return "".join(ch for ch in text if ch.isdigit())


def dagapeyeff_digits() -> str:
    return digits_only(DAGAPEYEFF_GROUPED)


def fold_plain(text: str) -> str:
    return two_square_letters(text)


def polybius_digits(text: str, square: str) -> list[int]:
    """Row-major coordinates in 1..5. J is folded to I. Non-letters drop."""
    if len(square) != 25 or len(set(square)) != 25:
        raise ValueError("Polybius square must be 25 distinct letters")
    pos = {ch: i for i, ch in enumerate(square)}
    stream = fold_plain(text)
    if not stream:
        raise ValueError("plaintext has no letters")
    out: list[int] = []
    for ch in stream:
        row, col = divmod(pos[ch], 5)
        out.append(row + 1)
        out.append(col + 1)
    return out


def apply_gronsfeld(coords: list[int], key: tuple[int, ...]) -> list[int]:
    if not key:
        raise ValueError("Gronsfeld key must contain at least one digit")
    return [(digit + key[i % len(key)]) % 10 for i, digit in enumerate(coords)]


def insert_nulls(digits: list[int], period: int, phase: int, dummy: int) -> list[int]:
    """Put `dummy` at every output index congruent to `phase` modulo `period`."""
    if period < 2:
        raise ValueError("null period must be at least 2")
    if not 0 <= phase < period:
        raise ValueError("null phase must lie in 0..period-1")
    if not 0 <= dummy <= 9:
        raise ValueError("dummy digit must be 0..9")
    out: list[int] = []
    src = 0
    index = 0
    while src < len(digits):
        if index % period == phase:
            out.append(dummy)
        else:
            out.append(digits[src])
            src += 1
        index += 1
    return out


def strip_nulls(digits: list[int], period: int, phase: int) -> list[int]:
    if period == 0:
        return list(digits)
    if period < 2 or not 0 <= phase < period:
        raise ValueError("null period and phase are not a searched residue")
    return [digit for index, digit in enumerate(digits) if index % period != phase]


def undo_gronsfeld(digits: list[int], key: tuple[int, ...]) -> list[int] | None:
    """Subtract the key mod 10. Return None unless every digit is in 1..5."""
    coords: list[int] = []
    width = len(key)
    for index, digit in enumerate(digits):
        value = (digit - key[index % width]) % 10
        if value < 1 or value > 5:
            return None
        coords.append(value)
    return coords


def coords_to_text(coords: list[int], square: str) -> str:
    if len(coords) % 2 != 0:
        raise ValueError("Polybius coordinates must come in pairs")
    chars: list[str] = []
    for index in range(0, len(coords), 2):
        row = coords[index] - 1
        col = coords[index + 1] - 1
        chars.append(square[row * 5 + col])
    return "".join(chars)


def decrypt_book_polybius(text: str) -> str:
    """Decrypt the book's letter-coordinate Polybius example (known square)."""
    letters = letters_only(text)
    if len(letters) % 2 != 0:
        raise ValueError("book Polybius ciphertext must have an even number of letters")
    out: list[str] = []
    for index in range(0, len(letters), 2):
        row = _COORD.get(letters[index])
        col = _COORD.get(letters[index + 1])
        if row is None or col is None:
            raise ValueError("book Polybius coordinates must be letters A–E")
        cell = BOOK_POLYBIUS_SQUARE[row][col]
        if cell is None:
            raise ValueError(f"pair {letters[index:index + 2]} hits an empty cell")
        out.append(cell)
    return "".join(out)


def corpus_keywords() -> list[str]:
    """Lowercase words of at least four letters in the repo English sample."""
    words = {
        token.lower()
        for token in _CORPUS.read_text(encoding="utf-8").split()
        if token.isalpha() and len(token) >= 4
    }
    return sorted(words)


def keyword_squares(keywords: list[str] | None = None) -> list[tuple[str, str]]:
    """Unique squares as (label, square). Empty keyword is the straight alphabet."""
    labels = [""] if keywords is None else list(keywords)
    if keywords is None:
        labels.extend(corpus_keywords())
    seen: dict[str, str] = {}
    for label in labels:
        square = square_from_keyword(label)
        seen.setdefault(square, label if label else "straight")
    return [(label, square) for square, label in seen.items()]


def null_specs() -> list[tuple[int, int]]:
    specs = [(0, 0)]
    for period in NULL_PERIODS:
        for phase in range(period):
            specs.append((period, phase))
    return specs


def _key_from_int(value: int, length: int) -> tuple[int, ...]:
    digits = [0] * length
    for index in range(length - 1, -1, -1):
        digits[index] = value % 10
        value //= 10
    return tuple(digits)


def legal_keys(digits: list[int], max_key_len: int) -> list[tuple[int, ...]]:
    """Numeric keys of length 1..max_key_len that restore only coordinates 1..5."""
    if max_key_len < 1:
        raise ValueError("max_key_len must be at least 1")
    if len(digits) % 2 != 0:
        return []
    found: list[tuple[int, ...]] = []
    for length in range(1, max_key_len + 1):
        span = 10 ** length
        for value in range(span):
            key = _key_from_int(value, length)
            if undo_gronsfeld(digits, key) is not None:
                found.append(key)
    return found


def max_in_range_key(digits: list[int], key_len: int) -> tuple[tuple[int, ...], int]:
    """Key of this length maximizing how many undone digits lie in 1..5.

    Each key position is an independent 10-way choice, so the maximum is exact.
    """
    if key_len < 1:
        raise ValueError("key_len must be at least 1")
    choice = [0] * key_len
    total = 0
    for residue in range(key_len):
        best_digit = 0
        best_hits = -1
        for key_digit in range(10):
            hits = 0
            for index in range(residue, len(digits), key_len):
                value = (digits[index] - key_digit) % 10
                if 1 <= value <= 5:
                    hits += 1
            if hits > best_hits:
                best_hits = hits
                best_digit = key_digit
        choice[residue] = best_digit
        total += best_hits
    return tuple(choice), total


def _score_text(model, text: str) -> float:
    if len(text) < 4:
        return float("-inf")
    return model.score(to_ints(text))


def solve_polybius_gronsfeld(
    text: str,
    max_key_len: int = 4,
    keywords: list[str] | None = None,
) -> SolveResult:
    """Search null phase, numeric key, and keyword square. No key is supplied."""
    raw = [int(ch) for ch in digits_only(text)]
    if len(raw) < 2:
        raise ValueError("ciphertext needs at least two digits")
    squares = keyword_squares(keywords)
    model = get_model()
    best: SolveResult | None = None
    trials = 0
    for period, phase in null_specs():
        stripped = strip_nulls(raw, period, phase)
        keys = legal_keys(stripped, max_key_len)
        trials += sum(10 ** length for length in range(1, max_key_len + 1))
        if not keys:
            continue
        coord_rows = [(key, undo_gronsfeld(stripped, key)) for key in keys]
        for label, square in squares:
            for key, coords in coord_rows:
                if coords is None:
                    continue
                plain = coords_to_text(coords, square)
                score = _score_text(model, plain)
                candidate = SolveResult(
                    method="polybius-gronsfeld",
                    plaintext=plain,
                    key="".join(str(digit) for digit in key),
                    score=score,
                    details={
                        "keyword": label,
                        "null_period": period,
                        "null_phase": phase,
                        "letters": len(plain),
                        "family": "polybius-1-5 + digit Gronsfeld mod 10 + optional nulls",
                        "solved_historical": False,
                    },
                )
                if best is None or _better(candidate, best):
                    best = candidate
    if best is None:
        return SolveResult(
            method="polybius-gronsfeld",
            plaintext="",
            key="",
            score=float("-inf"),
            details={
                "keyword": "",
                "null_period": None,
                "null_phase": None,
                "letters": 0,
                "legal": 0,
                "digits": len(raw),
                "trials_per_square_bound": trials,
                "family": "polybius-1-5 + digit Gronsfeld mod 10 + optional nulls",
                "solved_historical": False,
                "outcome": "no key in the searched family restores only coordinates 1..5",
            },
        )
    best.details["legal_keys_at_best_null"] = len(
        legal_keys(strip_nulls(raw, best.details["null_period"], best.details["null_phase"]), max_key_len)
    )
    best.details["squares"] = len(squares)
    best.details["solved_historical"] = False
    return best


def _better(left: SolveResult, right: SolveResult) -> bool:
    if left.score != right.score:
        return left.score > right.score
    if len(left.key) != len(right.key):
        return len(left.key) < len(right.key)
    if left.key != right.key:
        return left.key < right.key
    return str(left.details.get("keyword", "")) < str(right.details.get("keyword", ""))


def partial_candidate(text: str, max_key_len: int = 4) -> dict:
    """Best in-range key for each null spec. Not a decryption unless coverage is 1."""
    raw = [int(ch) for ch in digits_only(text)]
    best: dict | None = None
    for period, phase in null_specs():
        stripped = strip_nulls(raw, period, phase)
        if len(stripped) < 2:
            continue
        for length in range(1, max_key_len + 1):
            key, hits = max_in_range_key(stripped, length)
            undone = [(digit - key[index % length]) % 10 for index, digit in enumerate(stripped)]
            preview: list[str] = []
            square = square_from_keyword("")
            for index in range(0, len(undone) - 1, 2):
                row, col = undone[index], undone[index + 1]
                if 1 <= row <= 5 and 1 <= col <= 5:
                    preview.append(square[(row - 1) * 5 + (col - 1)])
                else:
                    preview.append(".")
            if len(undone) % 2:
                preview.append(".")
            row = {
                "null_period": period,
                "null_phase": phase,
                "key": "".join(str(digit) for digit in key),
                "key_len": length,
                "in_range": hits,
                "digits": len(stripped),
                "coverage": hits / len(stripped) if stripped else 0.0,
                "straight_square_preview": "".join(preview),
            }
            if best is None or (row["coverage"], row["in_range"], -length) > (
                best["coverage"],
                best["in_range"],
                -best["key_len"],
            ):
                best = row
    if best is None:
        raise ValueError("no digits to score")
    best["full_legal"] = best["coverage"] == 1.0 and best["digits"] % 2 == 0
    return best
