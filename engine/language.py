"""English letter model: published unigrams plus a quadgram model fit on original prose.

The quadgram table is conditional log-likelihood with backoff to trigrams,
bigrams, and unigrams. It is the objective for substitution search and for
choosing a Vigenère period. Unigram frequencies alone cannot rank substitution
keys, because every key with the same letter counts scores the same.
"""

from __future__ import annotations

import math
from functools import lru_cache
from pathlib import Path

from engine.alphabet import letters_only

# Standard English unigram frequencies (A-Z). Factual letter rates, not a text.
UNIGRAM = (
    0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094,
    0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929,
    0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150,
    0.01974, 0.00074,
)
LOG_UNIGRAM = tuple(math.log(p) for p in UNIGRAM)
ENGLISH_ORDER = "ETAOINSHRDLCUMWFGYPBVKJXQZ"

_DATA = Path(__file__).resolve().parent / "data" / "english.txt"
_LARGE = Path(__file__).resolve().parent / "data" / "neural_train_public.txt"


def unigram_score(seq: list[int]) -> float:
    total = 0.0
    for idx in seq:
        total += LOG_UNIGRAM[idx]
    return total


def chi_square(seq: list[int]) -> float:
    """Pearson chi-square against English unigram frequencies. Lower is better."""
    n = len(seq)
    if n == 0:
        return 0.0
    observed = [0] * 26
    for idx in seq:
        observed[idx] += 1
    score = 0.0
    for i in range(26):
        expected = UNIGRAM[i] * n
        diff = observed[i] - expected
        score += (diff * diff) / expected
    return score


class LanguageModel:
    """Quadgram log-likelihood with stupid backoff to shorter contexts."""

    def __init__(self, prose: str, alpha: float = 0.1) -> None:
        letters = letters_only(prose)
        if len(letters) < 4:
            raise ValueError("language sample is too short to fit an n-gram model")
        ints = [ord(ch) - 65 for ch in letters]
        uni = [0] * 26
        bi = [0] * (26 * 26)
        tri = [0] * (26 ** 3)
        quad = [0] * (26 ** 4)
        for a in ints:
            uni[a] += 1
        for i in range(len(ints) - 1):
            bi[ints[i] * 26 + ints[i + 1]] += 1
        for i in range(len(ints) - 2):
            a, b, c = ints[i], ints[i + 1], ints[i + 2]
            tri[(a * 26 + b) * 26 + c] += 1
        for i in range(len(ints) - 3):
            a, b, c, d = ints[i], ints[i + 1], ints[i + 2], ints[i + 3]
            quad[((a * 26 + b) * 26 + c) * 26 + d] += 1

        uni_sum = sum(uni) + 26 * alpha
        logp = [0.0] * (26 ** 4)
        strength = 8.0
        for a in range(26):
            for b in range(26):
                bi_ab = bi[a * 26 + b]
                for c in range(26):
                    tc = tri[(a * 26 + b) * 26 + c]
                    bc = bi[b * 26 + c]
                    uc = uni[c]
                    wq = tc / (tc + strength)
                    remain = 1.0 - wq
                    wt = remain * (bc / (bc + strength))
                    remain = 1.0 - wq - wt
                    wb = remain * (uc / (uc + strength))
                    wu = 1.0 - wq - wt - wb
                    den_q = tc + 26 * alpha
                    den_t = bc + 26 * alpha
                    den_b = uc + 26 * alpha
                    base = ((a * 26 + b) * 26 + c) * 26
                    for d in range(26):
                        pq = (quad[base + d] + alpha) / den_q
                        pt = (tri[(b * 26 + c) * 26 + d] + alpha) / den_t
                        pb = (bi[c * 26 + d] + alpha) / den_b
                        pu = (uni[d] + alpha) / uni_sum
                        logp[base + d] = math.log(wq * pq + wt * pt + wb * pb + wu * pu)
        self.logp = logp
        self.sample_letters = len(letters)

    def score(self, seq: list[int]) -> float:
        n = len(seq)
        if n < 4:
            return unigram_score(seq)
        logp = self.logp
        total = 0.0
        a, b, c = seq[0], seq[1], seq[2]
        for i in range(3, n):
            d = seq[i]
            total += logp[((a * 26 + b) * 26 + c) * 26 + d]
            a, b, c = b, c, d
        return total


@lru_cache(maxsize=1)
def get_model() -> LanguageModel:
    prose = _DATA.read_text(encoding="utf-8")
    return LanguageModel(prose)


@lru_cache(maxsize=1)
def get_large_model() -> LanguageModel:
    """The same quadgram model fit on 1,916,398 public-domain letters.

    ``get_model`` is fit on about 8,500 letters. On short texts it can prefer a
    wrong substitution key to the right one. This model is opt-in, so frozen
    scores computed with ``get_model`` keep their meaning. Its corpus excludes
    the Doyle, Wells and Grimm held-out windows and every certificate plaintext.
    """
    return LanguageModel(_LARGE.read_text(encoding="utf-8"))
