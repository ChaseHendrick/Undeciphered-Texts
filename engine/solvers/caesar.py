"""Caesar: try all 26 shifts and keep the best English unigram score."""

from __future__ import annotations

from engine.alphabet import from_ints, letters_only, reinject, to_ints
from engine.language import chi_square, unigram_score
from engine.result import SolveResult


def solve_caesar(text: str) -> SolveResult:
    letters = letters_only(text)
    if not letters:
        raise ValueError("ciphertext has no letters")
    seq = to_ints(letters)
    best_shift = 0
    best_score = float("-inf")
    best_chi = float("inf")
    best_plain: list[int] = seq
    trials: list[tuple[int, float, float]] = []
    for shift in range(26):
        plain = [(c - shift) % 26 for c in seq]
        score = unigram_score(plain)
        chi = chi_square(plain)
        trials.append((shift, score, chi))
        if score > best_score:
            best_shift = shift
            best_score = score
            best_chi = chi
            best_plain = plain
    rendered = reinject(text, from_ints(best_plain))
    return SolveResult(
        method="caesar",
        plaintext=rendered,
        key=str(best_shift),
        score=best_score,
        details={
            "shift": best_shift,
            "chi_square": round(best_chi, 3),
            "letters": len(letters),
            "trials": len(trials),
        },
    )
