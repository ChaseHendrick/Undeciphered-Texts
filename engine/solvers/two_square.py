"""Two-square (Truppenschlüssel) solver: keyword search and hill-climbing.

The cipher uses two 5×5 squares that omit J. Encipherment follows the single-
stage rule described by Ostwald and Weierud (Cryptologia; author PDF
https://cryptocellar.org/pubs/mcts.pdf): first plaintext letter in the left
square, second in the right; rectangle or same-row right-neighbour; ciphertext
letter from the right square first.

This module recovers **synthetic** keyword-keyed English by trying keyword
pairs from a word list and ranking decrypts with the English quadgram model
in ``engine.language``. A
shotgun hill-climber is included for random-square experiments. Neither path
claims a historical decipherment of an unsolved wartime message.
"""

from __future__ import annotations

import random
from collections import Counter
from functools import lru_cache
from pathlib import Path

from engine.alphabet import letters_only
from engine.ciphers import (
    TWO_SQUARE_ALPHABET,
    square_from_keyword,
    two_square_decrypt,
    two_square_encrypt,
    two_square_letters,
)
from engine.german import german_letters, get_german_model
from engine.language import get_model
from engine.result import SolveResult

_ENGLISH_PATH = Path(__file__).resolve().parents[1] / "data" / "english.txt"

# Small default word list for keyword-keyed synthetic recovery. Not a crib for
# wartime German messages.
DEFAULT_KEYWORDS = (
    "HARBOR",
    "CANAL",
    "PAPER",
    "STONE",
    "RIVER",
    "FIELD",
    "SHORE",
    "PRESS",
    "BOARD",
    "TABLE",
    "LIGHT",
    "WATER",
    "NORTH",
    "SOUTH",
    "EAST",
    "WEST",
    "ALPHA",
    "BRAVO",
    "DELTA",
    "OCEAN",
)


@lru_cache(maxsize=1)
def _english_trigram_table() -> tuple[int, ...]:
    prose = _ENGLISH_PATH.read_text(encoding="utf-8")
    letters = letters_only(prose)
    counts: Counter[str] = Counter()
    for i in range(len(letters) - 2):
        counts[letters[i : i + 3]] += 1
    table = [0] * (26**3)
    for gram, count in counts.items():
        a = ord(gram[0]) - 65
        b = ord(gram[1]) - 65
        c = ord(gram[2]) - 65
        table[(a * 26 + b) * 26 + c] = count
    return tuple(table)


def trigram_count_score(text: str, table: tuple[int, ...] | None = None) -> int:
    """Sum of English trigram counts on an A-Z stream (J already folded)."""
    stream = two_square_letters(text)
    if len(stream) < 3:
        return 0
    tbl = table if table is not None else _english_trigram_table()
    total = 0
    a = ord(stream[0]) - 65
    b = ord(stream[1]) - 65
    for ch in stream[2:]:
        c = ord(ch) - 65
        total += tbl[(a * 26 + b) * 26 + c]
        a, b = b, c
    return total


def german_trigram_score(text: str) -> float:
    """German quadgram log-score from engine.german (higher is more like Grimm)."""
    model = get_german_model()
    seq = [ord(ch) - 65 for ch in german_letters(text)]
    return model.quadgram_score(seq)


def _cells_from_square(square: str) -> list[int]:
    stream = two_square_letters(square)
    if len(stream) != 25 or len(set(stream)) != 25:
        raise ValueError("square must be 25 distinct letters without J")
    return [ord(ch) - 65 for ch in stream]


def _square_string(cells: list[int]) -> str:
    return "".join(chr(65 + n) for n in cells)


def _positions(cells: list[int]) -> list[int]:
    pos = [0] * 26
    for i, letter in enumerate(cells):
        pos[letter] = i
    return pos


def _decrypt_cells(ct: list[int], left: list[int], right: list[int]) -> list[int]:
    lp = _positions(left)
    rp = _positions(right)
    out = [0] * len(ct)
    for i in range(0, len(ct), 2):
        c1, c2 = ct[i], ct[i + 1]
        r1, c1p = divmod(rp[c1], 5)
        r2, c2p = divmod(lp[c2], 5)
        if r1 != r2:
            out[i] = left[r1 * 5 + c2p]
            out[i + 1] = right[r2 * 5 + c1p]
        else:
            out[i] = left[r1 * 5 + (c2p - 1) % 5]
            out[i + 1] = right[r1 * 5 + (c1p - 1) % 5]
    return out


def _score_ints(seq: list[int], table: tuple[int, ...]) -> int:
    if len(seq) < 3:
        return 0
    total = 0
    a, b = seq[0], seq[1]
    for c in seq[2:]:
        total += table[(a * 26 + b) * 26 + c]
        a, b = b, c
    return total


def _quadgram_score(text: str) -> float:
    """English quadgram log-likelihood. Higher is better. Not a decipherment claim."""
    stream = two_square_letters(text)
    if len(stream) < 4:
        return float("-inf")
    return get_model().score([ord(ch) - 65 for ch in stream])


def solve_two_square_keywords(
    text: str,
    keywords: tuple[str, ...] | list[str] = DEFAULT_KEYWORDS,
) -> SolveResult:
    """Try every keyword pair; keep the decrypt with the best English quadgram score.

    The squares are built from the word list. The true keywords are not passed
    separately. Raw trigram counts are not used here: on a long synthetic
    English text they can rank a wrong pair above the real plaintext.
    """
    stream = two_square_letters(text)
    if len(stream) < 8 or len(stream) % 2 == 1:
        raise ValueError("two-square ciphertext needs an even length of at least 8 letters")
    words = tuple(dict.fromkeys(two_square_letters(w) for w in keywords if two_square_letters(w)))
    if len(words) < 2:
        raise ValueError("need at least two distinct keywords")
    best_score = float("-inf")
    best_plain = ""
    best_left = ""
    best_right = ""
    best_pair = ("", "")
    trials = 0
    for left_kw in words:
        left = square_from_keyword(left_kw)
        for right_kw in words:
            if right_kw == left_kw:
                continue
            right = square_from_keyword(right_kw)
            plain = two_square_decrypt(stream, left, right)
            score = _quadgram_score(plain)
            trials += 1
            if score > best_score:
                best_score = score
                best_plain = plain
                best_left = left
                best_right = right
                best_pair = (left_kw, right_kw)
    return SolveResult(
        method="two_square_keywords",
        plaintext=best_plain,
        key=f"{best_pair[0]}/{best_pair[1]}",
        score=float(best_score),
        details={
            "left_keyword": best_pair[0],
            "right_keyword": best_pair[1],
            "left_square": best_left,
            "right_square": best_right,
            "letters": len(stream),
            "trials": trials,
            "scoring": "english_quadgram_log",
        },
    )


def _kick(left: list[int], right: list[int], rng: random.Random, swaps: int) -> None:
    for _ in range(swaps):
        cells = left if rng.randrange(2) == 0 else right
        i = rng.randrange(25)
        j = rng.randrange(25)
        if i != j:
            cells[i], cells[j] = cells[j], cells[i]


def _hill_pass(
    ct: list[int],
    left: list[int],
    right: list[int],
    table: tuple[int, ...],
) -> int:
    """One local-improvement pass: row/col swaps and within-row/col letter swaps."""
    plain = _decrypt_cells(ct, left, right)
    score = _score_ints(plain, table)

    def try_swap(cells: list[int], i: int, j: int) -> bool:
        nonlocal score, plain
        if i == j:
            return False
        cells[i], cells[j] = cells[j], cells[i]
        trial_plain = _decrypt_cells(ct, left, right)
        trial = _score_ints(trial_plain, table)
        if trial > score:
            score = trial
            plain = trial_plain
            return True
        cells[i], cells[j] = cells[j], cells[i]
        return False

    improved = True
    while improved:
        improved = False
        for cells in (left, right):
            for r1 in range(5):
                for r2 in range(r1 + 1, 5):
                    for c in range(5):
                        i, j = r1 * 5 + c, r2 * 5 + c
                        cells[i], cells[j] = cells[j], cells[i]
                    trial_plain = _decrypt_cells(ct, left, right)
                    trial = _score_ints(trial_plain, table)
                    if trial > score:
                        score = trial
                        plain = trial_plain
                        improved = True
                    else:
                        for c in range(5):
                            i, j = r1 * 5 + c, r2 * 5 + c
                            cells[i], cells[j] = cells[j], cells[i]
            for c1 in range(5):
                for c2 in range(c1 + 1, 5):
                    for r in range(5):
                        i, j = r * 5 + c1, r * 5 + c2
                        cells[i], cells[j] = cells[j], cells[i]
                    trial_plain = _decrypt_cells(ct, left, right)
                    trial = _score_ints(trial_plain, table)
                    if trial > score:
                        score = trial
                        plain = trial_plain
                        improved = True
                    else:
                        for r in range(5):
                            i, j = r * 5 + c1, r * 5 + c2
                            cells[i], cells[j] = cells[j], cells[i]
            for r in range(5):
                idx = [r * 5 + c for c in range(5)]
                for a in range(5):
                    for b in range(a + 1, 5):
                        if try_swap(cells, idx[a], idx[b]):
                            improved = True
            for c in range(5):
                idx = [r * 5 + c for r in range(5)]
                for a in range(5):
                    for b in range(a + 1, 5):
                        if try_swap(cells, idx[a], idx[b]):
                            improved = True
    return score


def climb_two_square(
    text: str,
    *,
    restarts: int = 8,
    kicks: int = 12,
    seed: int = 20261002,
) -> SolveResult:
    """Shotgun hill-climb on random 5×5 squares (Ostwald-style kicks/restarts).

    Scores with English trigram counts. Useful on long synthetic English. Short
    or corrupt wartime ciphertext will not uniquely recover, and a high score
    alone is not a claimed reading.
    """
    stream = two_square_letters(text)
    if len(stream) < 8 or len(stream) % 2 == 1:
        raise ValueError("two-square ciphertext needs an even length of at least 8 letters")
    ct = [ord(ch) - 65 for ch in stream]
    table = _english_trigram_table()
    alphabet = [ord(ch) - 65 for ch in TWO_SQUARE_ALPHABET]
    rng = random.Random(seed)
    best_score = -1
    best_left: list[int] = alphabet[:]
    best_right: list[int] = alphabet[:]
    best_plain = stream
    for restart in range(restarts):
        left = alphabet[:]
        right = alphabet[:]
        rng.shuffle(left)
        rng.shuffle(right)
        kick_n = 1
        local_best = -1
        local_left = left[:]
        local_right = right[:]
        for _ in range(kicks):
            score = _hill_pass(ct, left, right, table)
            if score > local_best:
                local_best = score
                local_left = left[:]
                local_right = right[:]
                kick_n = 1
            _kick(left, right, rng, kick_n)
            kick_n = min(10, kick_n + 1)
        if local_best > best_score:
            best_score = local_best
            best_left = local_left
            best_right = local_right
            best_plain = "".join(chr(65 + n) for n in _decrypt_cells(ct, best_left, best_right))
    return SolveResult(
        method="two_square_climb",
        plaintext=best_plain,
        key=f"{_square_string(best_left)}/{_square_string(best_right)}",
        score=float(best_score),
        details={
            "left_square": _square_string(best_left),
            "right_square": _square_string(best_right),
            "letters": len(stream),
            "restarts": restarts,
            "kicks": kicks,
            "seed": seed,
            "scoring": "english_trigram_count",
        },
    )


def solve_two_square(
    text: str,
    *,
    keywords: tuple[str, ...] | list[str] | None = None,
    left: str | None = None,
    right: str | None = None,
) -> SolveResult:
    """Recover two-square plaintext.

    - If ``left`` and ``right`` are given, decrypt with those squares.
    - Otherwise search keyword-keyed squares from ``keywords`` (default list).
    """
    stream = two_square_letters(text)
    if left is not None and right is not None:
        plain = two_square_decrypt(stream, left, right)
        score = trigram_count_score(plain)
        return SolveResult(
            method="two_square",
            plaintext=plain,
            key=f"{two_square_letters(left)}/{two_square_letters(right)}",
            score=float(score),
            details={
                "left_square": two_square_letters(left),
                "right_square": two_square_letters(right),
                "letters": len(stream),
                "mode": "known_squares",
            },
        )
    return solve_two_square_keywords(stream, keywords or DEFAULT_KEYWORDS)


__all__ = [
    "DEFAULT_KEYWORDS",
    "climb_two_square",
    "german_trigram_score",
    "solve_two_square",
    "solve_two_square_keywords",
    "trigram_count_score",
    "two_square_decrypt",
    "two_square_encrypt",
    "square_from_keyword",
]
