"""Simple substitution by simulated annealing and hill-climbing.

The start key maps ciphertext letter frequencies onto English unigram order.
Search then swaps letters to raise quadgram log-likelihood. A final exhaustive
swap polish walks the neighborhood of the best key until it is a local maximum.

The learned trigram network in engine.neural is not the search objective. It
scores the finished candidate as a second opinion beside the quadgram score.
That number is an English-letter fitness, not a decipherment of an unknown script.

The order gate is separate from the search. Renaming symbols cannot make one
symbol predict the next. If the ciphertext order is no more dependent than a
shuffle of itself, ``reading`` is false and the returned plaintext is only
the best candidate, not a solution.
"""

from __future__ import annotations

import math
import random

from engine.alphabet import from_ints, letters_only, reinject, to_ints
from engine.language import ENGLISH_ORDER, get_model
from engine.neural import get_neural_model
from engine.result import SolveResult
from engine.stats import successive_information

_GATE_DRAWS = 200


def substitution_order_gate(text: str, *, draws: int = _GATE_DRAWS, seed: int = 20261004) -> dict:
    """Whether the ciphertext order could carry a substitution reading.

    The score is unchanged by the decrypt key. ``reading`` is true only when
    fewer than one draw in twenty is at least as dependent. It is not a claim
    that the key is correct.
    """
    symbols = list(letters_only(text))
    observed = successive_information(symbols)
    if len(symbols) < 8:
        return {
            "order_mi": round(observed, 4),
            "order_draws": draws,
            "order_as_predictable": draws,
            "reading": False,
        }
    drawn = random.Random(seed)
    as_high = 0
    for _ in range(draws):
        shuffled = symbols[:]
        drawn.shuffle(shuffled)
        if successive_information(shuffled) >= observed - 1e-15:
            as_high += 1
    return {
        "order_mi": round(observed, 4),
        "order_draws": draws,
        "order_as_predictable": as_high,
        "reading": as_high * 20 < draws,
    }


def frequency_decrypt_key(seq: list[int]) -> list[int]:
    """key[cipher_index] = plaintext_index, seeded from English letter order."""
    counts = [0] * 26
    for idx in seq:
        counts[idx] += 1
    cipher_order = sorted(range(26), key=lambda i: (-counts[i], i))
    english = [ord(ch) - 65 for ch in ENGLISH_ORDER]
    key = [0] * 26
    for rank, cipher_idx in enumerate(cipher_order):
        key[cipher_idx] = english[rank]
    return key


def _score(seq: list[int], key: list[int], logp: list[float]) -> float:
    n = len(seq)
    if n < 4:
        return 0.0
    total = 0.0
    a = key[seq[0]]
    b = key[seq[1]]
    c = key[seq[2]]
    for i in range(3, n):
        d = key[seq[i]]
        total += logp[((a * 26 + b) * 26 + c) * 26 + d]
        a, b, c = b, c, d
    return total


def _anneal(
    seq: list[int],
    key: list[int],
    logp: list[float],
    rng: random.Random,
    steps: int,
    temperature: float,
    cooling: float,
) -> tuple[list[int], float]:
    key = key[:]
    score = _score(seq, key, logp)
    best_key = key[:]
    best_score = score
    for _ in range(steps):
        i = rng.randrange(26)
        j = rng.randrange(26)
        if i == j:
            temperature *= cooling
            continue
        key[i], key[j] = key[j], key[i]
        trial = _score(seq, key, logp)
        delta = trial - score
        if delta >= 0.0 or rng.random() < math.exp(delta / max(temperature, 1e-9)):
            score = trial
            if trial > best_score:
                best_score = trial
                best_key = key[:]
        else:
            key[i], key[j] = key[j], key[i]
        temperature *= cooling
    return best_key, best_score


def _polish(seq: list[int], key: list[int], logp: list[float], max_passes: int = 16) -> tuple[list[int], float]:
    key = key[:]
    score = _score(seq, key, logp)
    for _ in range(max_passes):
        improved = False
        for i in range(25):
            for j in range(i + 1, 26):
                key[i], key[j] = key[j], key[i]
                trial = _score(seq, key, logp)
                if trial > score + 1e-9:
                    score = trial
                    improved = True
                else:
                    key[i], key[j] = key[j], key[i]
        if not improved:
            break
    return key, score


def solve_substitution(
    text: str,
    restarts: int = 10,
    steps: int = 4000,
    seed: int = 20261002,
    temperature: float = 30.0,
    cooling: float = 0.997,
) -> SolveResult:
    letters = letters_only(text)
    if len(letters) < 40:
        raise ValueError("ciphertext is too short for substitution search (need at least 40 letters)")
    seq = to_ints(letters)
    model = get_model()
    logp = model.logp
    rng = random.Random(seed)
    base = frequency_decrypt_key(seq)
    starts: list[list[int]] = [base[:]]
    for r in range(max(0, restarts - 1)):
        if r < 4:
            start = base[:]
            swaps = 2 + r
        else:
            start = list(range(26))
            rng.shuffle(start)
            swaps = 0
        for _ in range(swaps):
            i = rng.randrange(26)
            j = rng.randrange(26)
            start[i], start[j] = start[j], start[i]
        starts.append(start)

    best_key = base[:]
    best_score = float("-inf")
    for start in starts:
        climbed, _score_now = _anneal(seq, start, logp, rng, steps, temperature, cooling)
        if _score_now > best_score:
            best_key = climbed
            best_score = _score_now

    best_key, best_score = _polish(seq, best_key, logp)
    # A few shakes escape a remaining local maximum, then polish again.
    for _ in range(4):
        shaken = best_key[:]
        for _swap in range(2):
            i = rng.randrange(26)
            j = rng.randrange(26)
            shaken[i], shaken[j] = shaken[j], shaken[i]
        shaken, shake_score = _anneal(seq, shaken, logp, rng, steps // 2, temperature / 4, cooling)
        shaken, shake_score = _polish(seq, shaken, logp)
        if shake_score > best_score:
            best_key, best_score = shaken, shake_score

    plain_ints = [best_key[c] for c in seq]
    encrypt_key = ["?"] * 26
    for cipher_i, plain_i in enumerate(best_key):
        encrypt_key[plain_i] = chr(65 + cipher_i)
    rendered = reinject(text, from_ints(plain_ints))
    neural = get_neural_model()
    neural_score = neural.score(plain_ints)
    gate = substitution_order_gate(letters, seed=seed)
    return SolveResult(
        method="substitution",
        plaintext=rendered,
        key="".join(encrypt_key),
        score=best_score,
        details={
            "seed": seed,
            "restarts": len(starts),
            "anneal_steps": steps,
            "letters": len(letters),
            "decrypt_map": "".join(chr(65 + p) for p in best_key),
            "fitness": "quadgram",
            "neural_score": neural_score,
            "neural_backend": neural.backend,
            "second_opinion": "neural_trigram",
            "order_mi": gate["order_mi"],
            "order_draws": gate["order_draws"],
            "order_as_predictable": gate["order_as_predictable"],
            "reading": gate["reading"],
        },
    )
