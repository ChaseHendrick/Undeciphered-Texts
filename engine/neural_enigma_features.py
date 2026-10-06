"""A bounded Enigma trial for Bob. Only scalars leave this module.

The training generator draws Enigma with reflector B, rotors I, II and III in
four orders, random rings, random start positions and no plugboard. Rings and
positions only matter through their difference, the rotor offset, and through
when the right rotor carries the middle one. This trial tries every left,
middle and right offset and every phase of that carry, for each of the four
orders: 4 x 17,576 x 26 settings. The left rotor's step and the middle
rotor's double step are not modeled, so a text that crosses one scores worse
after it. A plugboard, another reflector or another rotor set defeats the
trial. It ranks families. It is not a break of any intercept and it keeps no
key or plaintext.

Scores use the training-only tables Bob already has, so no held-out text
enters. Three numbers come back: the best mean digraph log-likelihood, how
many standard deviations that best stands above every tried setting, and the
mean unigram log-likelihood of that best setting's letters.
"""

from __future__ import annotations

from functools import lru_cache

import numpy as np

from engine.solvers.enigma import _REFLECTORS, _ROTOR_WIRING

ORDERS = (("I", "II", "III"), ("II", "I", "III"), ("III", "II", "I"), ("I", "III", "II"))
FEATURE_COUNT = 3
# The trial reads at most this many letters. Every training, benchmark and audit
# text is 240 letters or fewer, so the cap changes none of them; it keeps a long
# input from allocating hundreds of megabytes, and the unmodeled double step
# would spoil a long text anyway.
MAX_LETTERS = 480


def _wiring(name: str) -> np.ndarray:
    return np.array([ord(ch) - 65 for ch in _ROTOR_WIRING[name]], dtype=np.int64)


@lru_cache(maxsize=len(ORDERS))
def offset_table(order: tuple[str, str, str]) -> np.ndarray:
    """table[left, middle, right, letter] for reflector B and no plugboard."""
    left, middle, right = (_wiring(name) for name in order)
    left_back, middle_back, right_back = (np.argsort(wiring) for wiring in (left, middle, right))
    reflector = np.array([ord(ch) - 65 for ch in _REFLECTORS["B"]], dtype=np.int64)
    a = np.arange(26)[:, None, None, None]
    b = np.arange(26)[None, :, None, None]
    c = np.arange(26)[None, None, :, None]
    x = np.arange(26)[None, None, None, :]
    t = (right[(x + c) % 26] - c) % 26
    t = (middle[(t + b) % 26] - b) % 26
    t = (left[(t + a) % 26] - a) % 26
    t = reflector[t]
    t = (left_back[(t + a) % 26] - a) % 26
    t = (middle_back[(t + b) % 26] - b) % 26
    t = (right_back[(t + c) % 26] - c) % 26
    return t.astype(np.int8)


def _decryptions(values: np.ndarray, order: tuple[str, str, str]) -> np.ndarray:
    """letters[left, middle, start_right, position] with the right rotor stepping each letter."""
    table = offset_table(order)
    n = len(values)
    right = (np.arange(26)[:, None] + np.arange(n)[None, :]) % 26
    return table[:, :, right, np.broadcast_to(values, (26, n))]


def _carry_bounds(n: int, phase: int) -> list[int]:
    first = 26 - phase if phase else 26
    return [0, *range(first, n, 26), n]


def _phase_totals(cumulative: np.ndarray, n: int):
    """Yield the total for every setting at each carry phase."""
    for phase in range(26):
        bounds = _carry_bounds(n, phase)
        total = np.zeros(cumulative.shape[:3], dtype=np.float32)
        for step in range(len(bounds) - 1):
            start, stop = bounds[step], bounds[step + 1]
            segment = cumulative[..., stop] - cumulative[..., start]
            total += np.roll(segment, -step, axis=1)
        yield total


def enigma_trial(values: np.ndarray, logdig: np.ndarray, logenglish: np.ndarray) -> dict:
    """Best scores over the bounded Enigma settings. Returns scalars and the best setting."""
    values = np.asarray(values, dtype=np.int64)
    n = len(values)
    if n < 20:
        raise ValueError("the Enigma trial needs at least 20 letters")
    logdig32 = np.asarray(logdig, dtype=np.float32)
    best_pair = -np.inf
    best_setting = None
    best_letters = None
    pair_sum = pair_square = 0.0
    count = 0
    for order in ORDERS:
        letters = _decryptions(values, order)
        cumulative = np.zeros(letters.shape[:3] + (n + 1,), dtype=np.float32)
        np.cumsum(logdig32[letters[..., :-1], letters[..., 1:]], axis=3, out=cumulative[..., 2:])
        for phase, total in enumerate(_phase_totals(cumulative, n)):
            pair_sum += float(total.sum())
            pair_square += float(np.square(total).sum())
            count += total.size
            top = float(total.max())
            if top > best_pair:
                best_pair = top
                where = np.unravel_index(int(total.argmax()), total.shape)
                best_setting = (order, tuple(int(v) for v in where), phase)
                best_letters = letters[where[0], :, where[2], :]
    mean = pair_sum / count
    spread = max(pair_square / count - mean * mean, 1e-12) ** 0.5
    order, (left, middle, right), phase = best_setting
    bounds = _carry_bounds(n, phase)
    single = 0.0
    for step in range(len(bounds) - 1):
        start, stop = bounds[step], bounds[step + 1]
        single += float(logenglish[best_letters[(middle + step) % 26, start:stop]].sum())
    return {
        "pair_per_letter": best_pair / (n - 1),
        "pair_z": (best_pair - mean) / spread,
        "single_per_letter": single / n,
        "setting": best_setting,
    }


def enigma_features(text: str, tables: dict) -> list[float]:
    """Three scalars for the router. The setting and decryption are discarded."""
    values = np.array([ord(ch) - 65 for ch in text.upper() if "A" <= ch <= "Z"], dtype=np.int64)[:MAX_LETTERS]
    logenglish = np.log(np.maximum(np.asarray(tables["english"], dtype=np.float64), 1e-300))
    found = enigma_trial(values, np.asarray(tables["logdig"], dtype=np.float64), logenglish)
    return [float(found["pair_per_letter"]), float(found["pair_z"]), float(found["single_per_letter"])]
