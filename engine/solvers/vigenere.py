"""Vigenère: Kasiski factors and column IC propose periods; n-grams pick the key.

Each column of a candidate period is a Caesar cipher and is solved by unigram
score. The full plaintext is then scored with the quadgram model. Multiples of
the true period also decipher, so the shortest period within a small likelihood
gap of the best score is reported.
"""

from __future__ import annotations

from engine.alphabet import from_ints, letters_only, reinject, to_ints
from engine.language import get_model, unigram_score
from engine.result import SolveResult
from engine.stats import column_mean_ic, friedman_period, index_of_coincidence, kasiski_factors


def _crack_period(seq: list[int], period: int) -> tuple[list[int], str, float]:
    plain = [0] * len(seq)
    shifts: list[int] = []
    for offset in range(period):
        column = seq[offset::period]
        best_shift = 0
        best_score = float("-inf")
        best_col: list[int] = column
        for shift in range(26):
            decoded = [(c - shift) % 26 for c in column]
            score = unigram_score(decoded)
            if score > best_score:
                best_shift = shift
                best_score = score
                best_col = decoded
        shifts.append(best_shift)
        for index, value in enumerate(best_col):
            plain[offset + index * period] = value
    key = "".join(chr(65 + shift) for shift in shifts)
    return plain, key, get_model().score(plain)


def solve_vigenere(text: str, max_period: int = 12) -> SolveResult:
    letters = letters_only(text)
    if len(letters) < 8:
        raise ValueError("ciphertext is too short for a Vigenère search")
    if max_period < 1:
        raise ValueError("max_period must be positive")
    max_period = min(max_period, max(1, len(letters) // 4))
    seq = to_ints(letters)
    ic = index_of_coincidence(letters)
    friedman = friedman_period(letters)
    kasiski = kasiski_factors(letters, max_period=max_period)
    column_ics = {p: round(column_mean_ic(letters, p), 5) for p in range(1, max_period + 1)}

    ranked: list[tuple[float, int, str, list[int]]] = []
    for period in range(1, max_period + 1):
        plain, key, score = _crack_period(seq, period)
        ranked.append((score, period, key, plain))
    ranked.sort(key=lambda item: item[0], reverse=True)
    best_score = ranked[0][0]
    # Likelihood gap of 12 nats keeps a shorter equivalent keyword (key repeated).
    close = [item for item in ranked if best_score - item[0] <= 12.0]
    close.sort(key=lambda item: (item[1], -item[0]))
    score, period, key, plain = close[0]
    rendered = reinject(text, from_ints(plain))
    return SolveResult(
        method="vigenere",
        plaintext=rendered,
        key=key,
        score=score,
        details={
            "period": period,
            "index_of_coincidence": round(ic, 5),
            "friedman_period": round(friedman, 3),
            "kasiski": kasiski[:8],
            "column_ic": column_ics,
            "period_scores": [(item[1], round(item[0], 2)) for item in ranked],
            "letters": len(letters),
        },
    )
