"""Six training-only pair-fit scores for a fixed public M209 internal setting.

Unknown external wheel phases are marginalized algebraically. The internal
LP pins/lugs come from the existing sourced M209 module, not an input key or
heldout example. These features do not decrypt or recover a machine key.
"""
from __future__ import annotations

import math
from collections.abc import Mapping
from functools import lru_cache
from numbers import Real

from engine.solvers.m209 import (
    BOUCHAUDY_PINS, BOUCHAUDY_LUGS, WHEEL_ALPHABETS,
    pins_from_pattern, lugs_from_specs,
)

LAGS = (17, 19, 21, 23, 25, 26)
MAX_CHARACTERS = 8192
_PINS = tuple(tuple(pins_from_pattern(pattern, alphabet))
              for pattern, alphabet in zip(BOUCHAUDY_PINS, WHEEL_ALPHABETS))
_BARS = tuple(lugs_from_specs(BOUCHAUDY_LUGS))
_ASCII = frozenset("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
_UNIFORM_PAIR_LOG = -2 * math.log(26)


def _probabilities(english):
    if isinstance(english, (str, bytes, Mapping)) or not hasattr(english, "__len__") or len(english) != 26:
        raise ValueError("english must contain26 training probabilities")
    values = []
    for value in english:
        if isinstance(value, bool) or not isinstance(value, Real):
            raise TypeError("english probabilities must be real numbers")
        try:
            number = float(value)
        except (OverflowError, ValueError) as exc:
            raise ValueError("english probabilities must be representable") from exc
        if not math.isfinite(number) or not 1e-100 <= number <= 1:
            raise ValueError("english probabilities must be finite in1e-100..1")
        values.append(number)
    total = sum(values)
    if abs(total - 1) > 1e-6:
        raise ValueError("english probabilities must sum to one")
    return tuple(value / total for value in values)


def _joint_keystream_pairs(pins, bars, lag):
    """Exact displacement-pair law under independent uniform wheel phases."""
    pairs = []
    for wheel in pins:
        frequencies = [[0., 0.], [0., 0.]]
        for position, bit in enumerate(wheel):
            frequencies[bit][wheel[(position + lag) % len(wheel)]] += 1 / len(wheel)
        pairs.append(frequencies)
    states = tuple(tuple((mask >> wheel) & 1 for wheel in range(len(pins)))
                   for mask in range(1 << len(pins)))
    kicks = tuple(sum(bool((left and bits[left - 1]) or (right and bits[right - 1]))
                      for left, right in bars) % 26 for bits in states)
    result = [[0.] * 26 for _ in range(26)]
    for first, left_bits in enumerate(states):
        for second, right_bits in enumerate(states):
            probability = math.prod(pairs[wheel][left][right]
                                    for wheel, (left, right) in enumerate(zip(left_bits, right_bits)))
            result[kicks[first]][kicks[second]] += probability
    return tuple(tuple(row) for row in result)


def _cipher_pair_distribution(keypair, english):
    """Marginalize two independent training-unigram plaintext letters."""
    # R[k][c] = Pr(P =25+k-c mod26). Matrix multiplication gives R.T D R.
    distribution = tuple(tuple(english[(25 + key - cipher) % 26] for cipher in range(26))
                         for key in range(26))
    intermediate = tuple(tuple(sum(distribution[key][cipher] * keypair[key][other]
                                   for key in range(26)) for other in range(26))
                         for cipher in range(26))
    return tuple(tuple(sum(intermediate[first][key] * distribution[key][second]
                           for key in range(26)) for second in range(26))
                 for first in range(26))


@lru_cache(maxsize=6)
def _key_pairs(lag):
    return _joint_keystream_pairs(_PINS, _BARS, lag)


@lru_cache(maxsize=4)
def _pair_tables(english):
    return tuple(tuple(tuple(math.log(value) for value in row)
                       for row in _cipher_pair_distribution(_key_pairs(lag), english))
                 for lag in LAGS)


def m209_pair_tables(english):
    """Return immutable log-pair tables fitted only to supplied training rates.

    The6 table order follows LAGS. This assumes independent plaintext
    letters at each lag and the fixed source-backed LP pin/lug settings.
    """
    return _pair_tables(_probabilities(english))


def m209_pair_features(text, tables):
    """Return6 mean pair log-fit lifts against uniform independent ciphertext.

    tables['english'] must come from the training split. External phases
    and plaintext letters are marginalized, never looked up from examples.
    Overlapping pairs make these composite fitness scores, not calibrated
    class probabilities or likelihoods of the complete ciphertext.
    """
    if not isinstance(text, str):
        raise TypeError("ciphertext must be text")
    if len(text) > MAX_CHARACTERS or any(ch.isalpha() and ch not in _ASCII for ch in text):
        raise ValueError("ciphertext requires bounded A-Z letters")
    values = [ord(ch.upper()) - 65 for ch in text if ch in _ASCII]
    if len(values) < 16:
        raise ValueError("ciphertext requires at least16 A-Z letters")
    if not isinstance(tables, Mapping) or "english" not in tables:
        raise ValueError("tables requires an english training probability vector")
    models = m209_pair_tables(tables["english"])
    scores = []
    for lag, model in zip(LAGS, models):
        if len(values) <= lag:
            scores.append(0.)
        else:
            scores.append(sum(model[values[index]][values[index + lag]] for index in range(len(values) - lag))
                          / (len(values) - lag) - _UNIFORM_PAIR_LOG)
    return scores
