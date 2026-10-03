"""Bounded plaintext-autokey primer inference and training-table trial scores.

For primer length L, P[i] = C[i] - P[i-L] modulo26 after the primer.
Each residue column therefore has26 possible first plaintext letters.
Cribs constrain those seeds exactly; language scoring selects example seeds.
Primary definitions: https://cs-people.bu.edu/tromer/SKC2006/
https://cs.uri.edu/cryptography/classical-ciphers/vigenere/article.html
"""
from __future__ import annotations

import hashlib
import math
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass
from functools import lru_cache
from numbers import Real
from pathlib import Path

from engine.language import get_model
from engine.reverse_engineer import Crib
from engine.solvers.autokey import autokey_encrypt

MAX_CHARACTERS = 8192
MAX_INFERENCE_LETTERS = 512
MAX_PERIOD = 128
MAX_FEATURE_PERIOD = 16
MAX_CANDIDATES = 128
_ASCII = frozenset("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
_CORPUS = Path(__file__).resolve().parents[1] / "data/english.txt"
SOURCE_URL = "https://cs-people.bu.edu/tromer/SKC2006/"
SCOPE = (
    "Plaintext-autokey hypotheses within the tested primer lengths. Language "
    "scores select examples and do not prove uniqueness or historical plaintext. "
    "Only crib propagation supplies forced letters. No unsolved-text claim."
)


def _integer(value, name, maximum):
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an integer")
    if not 1 <= value <= maximum:
        raise ValueError(f"{name} must be in1..{maximum}")


def _letters(text, *, minimum, maximum):
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if len(text) > MAX_CHARACTERS or any(ch.isalpha() and ch not in _ASCII for ch in text):
        raise ValueError(f"text requires A-Z letters and at most{MAX_CHARACTERS} raw characters")
    result = "".join(ch.upper() for ch in text if ch in _ASCII)
    if not minimum <= len(result) <= maximum:
        raise ValueError(f"text must contain{minimum}..{maximum} A-Z letters")
    return result


def _finite(value, name, minimum, maximum):
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must contain real numbers")
    try:
        result = float(value)
    except (OverflowError, ValueError) as exc:
        raise ValueError(f"{name} must be representable") from exc
    if not math.isfinite(result) or not minimum <= result <= maximum:
        raise ValueError(f"{name} must be finite in{minimum}..{maximum}")
    return result


def _log_weights(values):
    if isinstance(values, (str, bytes, Mapping)) or not hasattr(values, "__len__") or len(values) != 26:
        raise ValueError("log_unigram must contain26 finite log weights")
    return tuple(_finite(value, "log_unigram", -1000., 0.) for value in values)


@lru_cache(maxsize=1)
def _default_weights():
    raw = _CORPUS.read_bytes()
    letters = "".join(ch for ch in raw.decode("utf-8").upper() if "A" <= ch <= "Z")
    if len(letters) < 26:
        raise ValueError("English training corpus is too short")
    counts = Counter(letters)
    weights = tuple(math.log((counts[chr(65 + i)] + .5) / (len(letters) + 13)) for i in range(26))
    return weights, hashlib.sha256(raw).hexdigest()


def _columns(cipher, period):
    columns = []
    for offset in range(period):
        positions = tuple(range(offset, len(cipher), period))
        base = [0] * len(positions)
        for index in range(1, len(positions)):
            base[index] = (cipher[positions[index]] - base[index - 1]) % 26
        columns.append((positions, base))
    return columns


def _fit_plaintext(cipher, period, weights, known):
    plain = [0] * len(cipher)
    forced = ["?"] * len(cipher)
    unconstrained = 0
    for positions, base in _columns(cipher, period):
        allowed = []
        for seed in range(26):
            if all((base[j] + (seed if j % 2 == 0 else -seed)) % 26 == known[index]
                   for j, index in enumerate(positions) if index in known):
                allowed.append(seed)
        if not allowed:
            return None
        if len(allowed) != 1:
            unconstrained += 1
        seed = max(allowed, key=lambda value: sum(weights[(base[j] + (value if j % 2 == 0 else -value)) % 26]
                                                   for j in range(len(base))))
        for j, index in enumerate(positions):
            letter = (base[j] + (seed if j % 2 == 0 else -seed)) % 26
            plain[index] = letter
            if len(allowed) == 1:
                forced[index] = chr(65 + letter)
    return plain, "".join(forced), unconstrained


def _known_positions(cribs, length):
    if isinstance(cribs, (str, bytes)) or not isinstance(cribs, Sequence):
        raise TypeError("cribs must be a finite sequence of Crib objects")
    if len(cribs) > MAX_PERIOD:
        raise ValueError(f"at most{MAX_PERIOD} cribs are supported")
    known = {}
    for crib in cribs:
        if not isinstance(crib, Crib):
            raise TypeError("cribs must contain engine.reverse_engineer.Crib objects")
        if not isinstance(crib.offset, int) or isinstance(crib.offset, bool) or crib.offset < 0:
            raise ValueError("crib offset must be a nonnegative integer")
        plaintext = _letters(crib.plaintext, minimum=1, maximum=MAX_INFERENCE_LETTERS)
        if crib.offset + len(plaintext) > length:
            raise ValueError("crib extends beyond normalized ciphertext")
        for index, letter in enumerate(plaintext, crib.offset):
            value = ord(letter) - 65
            if index in known and known[index] != value:
                raise ValueError("overlapping cribs disagree")
            known[index] = value
    return known


@dataclass(frozen=True)
class AutokeyCandidate:
    period: int
    key: str
    plaintext: str
    score: float
    forced_plaintext: str
    unresolved_seed_columns: int
    compatible_primers: int
    forward_verified: bool = True
    example_only: bool = True


@dataclass(frozen=True)
class AutokeyInferenceReport:
    ciphertext_length: int
    known_positions: int
    candidates: tuple[AutokeyCandidate, ...]
    compatible_period_count: int
    compatible_primer_count: int
    consensus_plaintext: str
    constraint_space_complete: bool
    ranking_exhaustive: bool
    candidates_truncated: bool
    bounds: dict
    scoring: dict
    claimed_plaintext: None = None
    scope: str = SCOPE

    @property
    def plaintext_unique_within_period_bounds(self):
        return self.compatible_period_count > 0 and "?" not in self.consensus_plaintext

    def to_dict(self):
        result = asdict(self)
        result["plaintext_unique_within_period_bounds"] = self.plaintext_unique_within_period_bounds
        result["ambiguous_within_period_bounds"] = self.compatible_period_count > 0 and not self.plaintext_unique_within_period_bounds
        return result


def infer_autokey(text, *, max_period=16, cribs=(), max_candidates=20, log_unigram=None):
    """Fit all bounded primer lengths without a supplied primer.

    Cribs use zero-based normalized A-Z coordinates. For each compatible
    period, select one example seed per column by unigram likelihood, then
    rank these examples with the independent repository quadgram model.
    Constraint counts and consensus cover all possible primers algebraically;
    ranking does not enumerate their Cartesian product.
    """
    _integer(max_period, "max_period", MAX_PERIOD)
    _integer(max_candidates, "max_candidates", MAX_CANDIDATES)
    ciphertext = _letters(text, minimum=4, maximum=MAX_INFERENCE_LETTERS)
    cipher = [ord(ch) - 65 for ch in ciphertext]
    known = _known_positions(cribs, len(cipher))
    default, corpus_hash = _default_weights()
    weights = default if log_unigram is None else _log_weights(log_unigram)
    model = get_model()
    candidates = []
    period_bound = min(max_period, len(cipher))
    for period in range(1, period_bound + 1):
        fitted = _fit_plaintext(cipher, period, weights, known)
        if fitted is None:
            continue
        plain, forced, unresolved = fitted
        plaintext = "".join(chr(65 + value) for value in plain)
        key = "".join(chr(65 + (cipher[i] - plain[i]) % 26) for i in range(period))
        if autokey_encrypt(plaintext, key) != ciphertext:
            raise RuntimeError("autokey candidate failed forward verification")
        candidates.append(AutokeyCandidate(period, key, plaintext, model.score(plain) / (len(plain) - 3),
                                           forced, unresolved, 26 ** unresolved))
    known_mask = "".join(chr(65 + known[i]) if i in known else "?" for i in range(len(cipher)))
    consensus = known_mask
    if candidates:
        consensus = "".join(candidates[0].forced_plaintext[i]
                            if all(item.forced_plaintext[i] == candidates[0].forced_plaintext[i] for item in candidates)
                            else "?" for i in range(len(cipher)))
    candidates.sort(key=lambda item: (-item.score, item.period, item.key))
    return AutokeyInferenceReport(len(cipher), len(known), tuple(candidates[:max_candidates]), len(candidates),
        sum(item.compatible_primers for item in candidates), consensus, True, False, len(candidates) > max_candidates,
        {"max_period": max_period, "periods_tested": period_bound, "max_candidates": max_candidates,
         "max_normalized_letters": MAX_INFERENCE_LETTERS, "seeds_per_column": 26,
         "seed_checks_upper_bound": 26 * period_bound * (period_bound + 1) // 2},
        {"seed_selection": "maximum column log-unigram likelihood; smallest seed on exact tie",
         "ranking": "quadgram mean log score from engine/data/english.txt; example ranking only",
         "unigram_origin": "engine/data/english.txt" if log_unigram is None else "caller supplied",
         "quadgram_corpus_sha256": corpus_hash, "cribs_are_hard_constraints": True})


def _load_numpy():
    try:
        import numpy as np
    except ImportError:
        return None
    return np


def _tables(tables):
    if not isinstance(tables, Mapping) or "english" not in tables or "logdig" not in tables:
        raise ValueError("tables requires english and logdig training tables")
    english = tables["english"]
    if isinstance(english, (str, bytes, Mapping)) or not hasattr(english, "__len__") or len(english) != 26:
        raise ValueError("english must contain26 probabilities")
    probabilities = tuple(_finite(value, "english", 0., 1.) for value in english)
    if min(probabilities) <= 0 or abs(sum(probabilities) - 1.) > 1e-6:
        raise ValueError("english probabilities must be positive and sum to one")
    digraph = tables["logdig"]
    if isinstance(digraph, (str, bytes, Mapping)) or not hasattr(digraph, "__len__") or len(digraph) != 26:
        raise ValueError("logdig must contain26 rows")
    rows = []
    for row in digraph:
        if isinstance(row, (str, bytes, Mapping)) or not hasattr(row, "__len__") or len(row) != 26:
            raise ValueError("logdig must be26 by26")
        rows.append(tuple(_finite(value, "logdig", -1000., 0.) for value in row))
    return tuple(math.log(value) for value in probabilities), tuple(rows)


def autokey_feature_scores(text, tables, *, max_period=16):
    """Return one bounded trial digraph score per primer length1..max_period.

    Only the caller's training-only english/logdig tables fit and score the
    trials. No plaintext, recovered key, or corpus text is returned. NumPy is
    optional and imported lazily for this feature extraction's fast path.
    """
    _integer(max_period, "max_period", MAX_FEATURE_PERIOD)
    ciphertext = _letters(text, minimum=16, maximum=MAX_CHARACTERS)
    weights, digraph = _tables(tables)
    cipher = [ord(ch) - 65 for ch in ciphertext]
    np = _load_numpy()
    scores = []
    if np is None:
        for period in range(1, max_period + 1):
            plain = _fit_plaintext(cipher, period, weights, {})[0]
            scores.append(sum(digraph[a][b] for a, b in zip(plain, plain[1:])) / (len(plain) - 1))
        return scores
    log_weights = np.asarray(weights)
    digraph_array = np.asarray(digraph)
    seeds = np.arange(26)
    for period in range(1, max_period + 1):
        plain = np.zeros(len(cipher), dtype=np.int64)
        for positions, base in _columns(cipher, period):
            signs = np.where(np.arange(len(base)) % 2 == 0, 1, -1)
            trials = (np.asarray(base)[:, None] + signs[:, None] * seeds) % 26
            best = int(log_weights[trials].sum(axis=0).argmax())
            plain[list(positions)] = trials[:, best]
        scores.append(float(digraph_array[plain[:-1], plain[1:]].mean()))
    return scores
