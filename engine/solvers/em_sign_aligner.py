"""Knight-style EM aligner from unknown signs to English letters.

The source is a fixed English letter bigram. Each letter emits one observed
sign through a channel this module learns by expectation-maximization
(Baum-Welch with the language model held fixed). That is the small noisy
channel in Knight and Yamada, "A Computational Approach to Deciphering
Unknown Scripts" (1999): a known language, an unknown symbol inventory, and
no claim about what any historical inscription says.

This aligner does not read Linear A, the Indus script, or the Voynich
manuscript. Those corpora are not inputs. A recovered map is evidence only
about a synthetic sign text built by substituting a random sign for each
letter of ordinary English. It is not registered in ``engine.solvers.SOLVERS``
and it is not a classical cipher solver.

Numpy is required for the matrix updates. The rest of the engine still runs
without it. If numpy is missing, ``align_signs`` raises ImportError.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

from engine.alphabet import letters_only

try:
    import numpy as np
except ImportError:  # pragma: no cover - exercised only without numpy
    np = None

# Private-use labels U+E000..U+E019. They are not Latin letters.
SIGN_BASE = 0xE000
N_LETTERS = 26
SCOPE = (
    "This aligner does not read Linear A, the Indus script, or the Voynich "
    "manuscript. It only estimates a sign-to-letter channel on a synthetic "
    "corpus generated from English by a random symbol map."
)


def _need_numpy():
    if np is None:
        raise ImportError(
            "engine.solvers.em_sign_aligner requires numpy for EM updates"
        )
    return np


def sign_label(index: int) -> str:
    """ASCII label for one synthetic sign, e.g. ``U+E00A``. Not a letter."""
    if index < 0 or index >= N_LETTERS:
        raise ValueError(f"sign index out of range: {index}")
    return f"U+{SIGN_BASE + index:04X}"


def fit_bigram_channel(letters: str, alpha: float = 0.25):
    """Row-stochastic English bigram and unigram from known plaintext letters.

    ``letters`` must already be the language-model sample. Do not pass the
    hidden plaintext that the signs were generated from.
    """
    np = _need_numpy()
    cleaned = "".join(ch for ch in letters_only(letters) if "A" <= ch <= "Z")
    if len(cleaned) < 2:
        raise ValueError("need at least two English letters to fit a bigram")
    if alpha <= 0.0:
        raise ValueError("alpha must be positive")
    ints = np.fromiter((ord(ch) - 65 for ch in cleaned), dtype=np.int16, count=len(cleaned))
    counts = np.zeros((N_LETTERS, N_LETTERS), dtype=np.float64)
    uni = np.zeros(N_LETTERS, dtype=np.float64)
    np.add.at(uni, ints, 1.0)
    np.add.at(counts, (ints[:-1], ints[1:]), 1.0)
    transition = counts + alpha
    transition /= transition.sum(axis=1, keepdims=True)
    initial = uni + alpha
    initial /= initial.sum()
    return transition, initial


def random_letter_to_sign(seed: int) -> dict[str, str]:
    """Bijection from A-Z onto 26 synthetic sign labels. Seeded, not secret."""
    np = _need_numpy()
    order = np.random.default_rng(seed).permutation(N_LETTERS)
    return {chr(65 + letter): sign_label(int(order[letter])) for letter in range(N_LETTERS)}


def encode_letters(letters: str, letter_to_sign: Mapping[str, str]) -> list[str]:
    """Replace each A-Z letter with its sign. Drops non-letters."""
    cleaned = "".join(ch for ch in letters_only(letters) if "A" <= ch <= "Z")
    if not cleaned:
        raise ValueError("no English letters to encode")
    missing = sorted({ch for ch in cleaned if ch not in letter_to_sign})
    if missing:
        raise ValueError("letter map is missing " + "".join(missing))
    return [letter_to_sign[ch] for ch in cleaned]


def holdout_letters(prose: str, split: float = 0.45) -> tuple[str, str]:
    """Split English letters into a language-model prefix and a hidden suffix.

    The suffix is what a caller enciphers. The prefix is the only text the
    bigram channel may see.
    """
    if not 0.2 <= split <= 0.8:
        raise ValueError("split must stay between 0.2 and 0.8")
    letters = "".join(ch for ch in letters_only(prose) if "A" <= ch <= "Z")
    cut = int(len(letters) * split)
    if cut < 400 or len(letters) - cut < 800:
        raise ValueError("prose is too short for a held-out sign corpus")
    return letters[:cut], letters[cut:]


@dataclass(frozen=True)
class SignAlignment:
    """MAP sign-to-letter channel after EM. Not a reading of a real script."""

    sign_to_letter: dict[str, str]
    plaintext: str
    log_likelihood: float
    iterations: int
    observed_signs: int


def _index_signs(signs: Sequence[str]) -> tuple[list[str], "np.ndarray"]:
    np = _need_numpy()
    if not signs:
        raise ValueError("sign sequence is empty")
    if any(not isinstance(sign, str) or sign == "" for sign in signs):
        raise ValueError("every sign must be a non-empty string")
    vocab = sorted(set(signs))
    index = {sign: i for i, sign in enumerate(vocab)}
    observed = np.fromiter((index[sign] for sign in signs), dtype=np.int32, count=len(signs))
    return vocab, observed


def _forward_backward(observed, transition, initial, emission):
    """Scaled Baum-Welch posteriors. Returns (gamma, log_likelihood)."""
    np = _need_numpy()
    length = len(observed)
    alpha = np.empty((length, N_LETTERS), dtype=np.float64)
    scale = np.empty(length, dtype=np.float64)
    alpha[0] = initial * emission[:, observed[0]]
    scale[0] = alpha[0].sum()
    if scale[0] < 1e-300:
        scale[0] = 1e-300
    alpha[0] /= scale[0]
    for time in range(1, length):
        alpha[time] = (alpha[time - 1] @ transition) * emission[:, observed[time]]
        scale[time] = alpha[time].sum()
        if scale[time] < 1e-300:
            scale[time] = 1e-300
        alpha[time] /= scale[time]
    beta = np.empty((length, N_LETTERS), dtype=np.float64)
    beta[-1] = 1.0
    for time in range(length - 2, -1, -1):
        beta[time] = transition @ (emission[:, observed[time + 1]] * beta[time + 1])
        beta[time] /= scale[time + 1]
    gamma = alpha * beta
    gamma /= gamma.sum(axis=1, keepdims=True)
    return gamma, float(np.log(scale).sum())


def _emission_counts(gamma, observed, n_signs: int):
    np = _need_numpy()
    counts = np.zeros((N_LETTERS, n_signs), dtype=np.float64)
    for sign_id in range(n_signs):
        mask = observed == sign_id
        if np.any(mask):
            counts[:, sign_id] = gamma[mask].sum(axis=0)
    return counts


def _initial_emission(observed, initial, n_signs: int, rng, kind: str, noise: float):
    np = _need_numpy()
    if kind == "frequency":
        sign_freq = np.bincount(observed, minlength=n_signs).astype(np.float64)
        letter_order = np.argsort(-initial)
        sign_order = np.argsort(-sign_freq)
        emission = np.full((N_LETTERS, n_signs), 0.02, dtype=np.float64)
        for rank in range(min(N_LETTERS, n_signs)):
            emission[letter_order[rank], sign_order[rank]] = 1.0
        emission *= rng.random((N_LETTERS, n_signs)) * noise + (1.0 - noise / 2.0)
    elif kind == "random":
        emission = rng.random((N_LETTERS, n_signs)) + 0.05
    else:
        raise ValueError(f"unknown initialization {kind}")
    emission /= emission.sum(axis=1, keepdims=True)
    return emission


def _em_restart(observed, transition, initial, rng, iterations: int, smooth: float, kind: str):
    n_signs = int(observed.max()) + 1
    emission = _initial_emission(observed, initial, n_signs, rng, kind, noise=0.3)
    previous = None
    counts = None
    likelihood = float("-inf")
    used = 0
    for step in range(iterations):
        gamma, likelihood = _forward_backward(observed, transition, initial, emission)
        counts = _emission_counts(gamma, observed, n_signs)
        emission = counts + smooth
        emission /= emission.sum(axis=1, keepdims=True)
        used = step + 1
        if previous is not None and abs(likelihood - previous) < 0.05:
            break
        previous = likelihood
    return counts, likelihood, used


def align_signs(
    signs: Sequence[str],
    transition,
    initial,
    *,
    iterations: int = 30,
    restarts: int = 2,
    seed: int = 20261002,
    smooth: float = 0.05,
) -> SignAlignment:
    """Learn P(sign | letter) by EM and return the MAP letter for each sign.

    ``transition[i, j]`` is P(letter j | letter i). ``initial`` is P(letter).
    Both are 26-vectors over A-Z and are not updated. Only the channel changes.

    The first restart seeds the channel by frequency rank. Later restarts draw
    a random channel. The restart with the highest sequence likelihood is kept.
    The true sign map is not an argument.
    """
    np = _need_numpy()
    if iterations < 1 or restarts < 1:
        raise ValueError("iterations and restarts must be at least 1")
    if smooth < 0.0:
        raise ValueError("smooth must be non-negative")
    vocab, observed = _index_signs(signs)
    transition = np.asarray(transition, dtype=np.float64)
    initial = np.asarray(initial, dtype=np.float64)
    if transition.shape != (N_LETTERS, N_LETTERS):
        raise ValueError("transition must be 26 by 26")
    if initial.shape != (N_LETTERS,):
        raise ValueError("initial must have 26 letters")
    rng = np.random.default_rng(seed)
    kinds = ["frequency"] + ["random"] * (restarts - 1)
    best_counts = None
    best_ll = float("-inf")
    best_iters = 0
    for kind in kinds:
        counts, likelihood, used = _em_restart(
            observed, transition, initial, rng, iterations, smooth, kind
        )
        if likelihood > best_ll:
            best_ll = likelihood
            best_counts = counts
            best_iters = used
    assert best_counts is not None
    chosen = best_counts.argmax(axis=0)
    sign_to_letter = {sign: chr(65 + int(chosen[index])) for index, sign in enumerate(vocab)}
    plaintext = "".join(sign_to_letter[sign] for sign in signs)
    return SignAlignment(
        sign_to_letter=sign_to_letter,
        plaintext=plaintext,
        log_likelihood=best_ll,
        iterations=best_iters,
        observed_signs=len(vocab),
    )


def map_accuracy(
    predicted: Mapping[str, str],
    truth: Mapping[str, str],
    signs: Sequence[str],
) -> float:
    """Fraction of observed signs whose predicted letter matches ``truth``."""
    present = set(signs)
    scored = [sign for sign in present if sign in truth]
    if not scored:
        raise ValueError("no overlapping signs to score")
    correct = sum(1 for sign in scored if predicted.get(sign) == truth[sign])
    return correct / len(scored)


def character_accuracy(predicted_letters: str, plaintext: str) -> float:
    """Fraction of positions where the decoded letter matches the English source."""
    if not plaintext or len(predicted_letters) != len(plaintext):
        raise ValueError("predicted and plaintext letter strings must be the same length")
    matches = sum(1 for left, right in zip(predicted_letters, plaintext) if left == right)
    return matches / len(plaintext)
