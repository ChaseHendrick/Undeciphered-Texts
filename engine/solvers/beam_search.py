"""Beam-search decipherment for a synthetic monoalphabetic substitution.

The search extends a partial cipher-to-plain key one ciphertext symbol at a
time, most frequent symbol first, and keeps the best partial keys under an
English unigram and bigram model. Scores use only A-Z letters. Word spaces in
the ciphertext are preserved and bigrams are counted inside words, not across
spaces.

This beam search does not decipher ancient scripts — it does not read Linear A,
the Indus script, Rongorongo, the Voynich manuscript, or any other unknown
writing system. A high score only means the Latin-letter string looks more
like English under this model than the alternatives in the beam.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from engine.alphabet import from_ints, reinject

_DATA = Path(__file__).resolve().parent.parent / "data" / "beam_english.txt"
_A = ord("A")


def _az_words(text: str) -> list[str]:
    """Uppercase A-Z words. Accented letters and other symbols are separators."""
    words: list[str] = []
    buf: list[str] = []
    for ch in text:
        if "A" <= ch <= "Z" or "a" <= ch <= "z":
            buf.append(ch.upper())
        elif buf:
            words.append("".join(buf))
            buf = []
    if buf:
        words.append("".join(buf))
    return words


@dataclass(frozen=True)
class BigramModel:
    """Add-k smoothed English unigram and bigram log probabilities."""

    log_unigram: tuple[float, ...]
    log_bigram: tuple[float, ...]
    train_letters: int

    def sequence_score(self, words: list[list[int]]) -> float:
        total = 0.0
        uni = self.log_unigram
        bi = self.log_bigram
        for word in words:
            if not word:
                continue
            total += uni[word[0]]
            for i in range(len(word) - 1):
                total += bi[word[i] * 26 + word[i + 1]]
            for idx in word[1:]:
                total += uni[idx]
        return total


def fit_bigram_model(prose: str, alpha: float = 0.5) -> BigramModel:
    """Fit unigram and bigram logs from included English prose."""
    words = _az_words(prose)
    uni = [0] * 26
    bi = [0] * (26 * 26)
    letters = 0
    for word in words:
        ints = [ord(ch) - _A for ch in word]
        letters += len(ints)
        for idx in ints:
            uni[idx] += 1
        for i in range(len(ints) - 1):
            bi[ints[i] * 26 + ints[i + 1]] += 1
    if letters < 200:
        raise ValueError("English sample is too short to fit a unigram/bigram model")
    uni_den = sum(uni) + 26 * alpha
    log_uni = tuple(math.log((uni[i] + alpha) / uni_den) for i in range(26))
    log_bi_list: list[float] = []
    for a in range(26):
        den = uni[a] + 26 * alpha
        for b in range(26):
            log_bi_list.append(math.log((bi[a * 26 + b] + alpha) / den))
    return BigramModel(log_uni, tuple(log_bi_list), letters)


@lru_cache(maxsize=1)
def get_beam_model() -> BigramModel:
    prose = _DATA.read_text(encoding="utf-8")
    return fit_bigram_model(prose)


@dataclass(frozen=True)
class BeamDecipherResult:
    """Plaintext recovered by beam search. Not a reading of an ancient script."""

    plaintext: str
    decrypt_key: str
    score: float
    beam_width: int
    letters: int

    @property
    def limitation(self) -> str:
        return (
            "This beam search does not decipher ancient scripts. "
            "It compares Latin-letter substitution keys with an English model."
        )


def _events(words: list[list[int]]) -> tuple[list[int], list[list[int]], list[list[int]]]:
    """Counts plus, for each cipher symbol, left-hand and right-hand partners."""
    counts = [0] * 26
    left: list[list[int]] = [[] for _ in range(26)]
    right: list[list[int]] = [[] for _ in range(26)]
    for word in words:
        for idx in word:
            counts[idx] += 1
        for i in range(len(word) - 1):
            a, b = word[i], word[i + 1]
            left[a].append(b)
            if a != b:
                right[b].append(a)
    return counts, left, right


def beam_search_decipher(
    ciphertext: str,
    beam_width: int = 80,
    model: BigramModel | None = None,
) -> BeamDecipherResult:
    """Recover a monoalphabetic plaintext by unigram/bigram beam search.

    This beam search does not decipher ancient scripts. Feed it a synthetic
    or classical Latin-letter substitution, not an unknown writing system.
    """
    if beam_width < 1:
        raise ValueError("beam_width must be at least 1")
    words = [[ord(ch) - _A for ch in word] for word in _az_words(ciphertext)]
    letters = sum(len(word) for word in words)
    if letters < 40:
        raise ValueError("ciphertext is too short for beam-search decipherment (need at least 40 letters)")
    model = model if model is not None else get_beam_model()
    counts, left_partners, right_partners = _events(words)
    order = [i for i in range(26) if counts[i] > 0]
    order.sort(key=lambda i: (-counts[i], i))

    # key[cipher] = plain, or -1 if still free. used is a bitmask of plain letters.
    beams: list[tuple[float, tuple[int, ...], int]] = [(0.0, tuple([-1] * 26), 0)]
    log_uni = model.log_unigram
    log_bi = model.log_bigram

    for cipher_sym in order:
        nxt: list[tuple[float, tuple[int, ...], int]] = []
        partners_l = left_partners[cipher_sym]
        partners_r = right_partners[cipher_sym]
        weight = counts[cipher_sym]
        for score, key, used in beams:
            for plain in range(26):
                bit = 1 << plain
                if used & bit:
                    continue
                delta = weight * log_uni[plain]
                for other in partners_l:
                    if other == cipher_sym:
                        delta += log_bi[plain * 26 + plain]
                        continue
                    mapped = key[other]
                    if mapped >= 0:
                        delta += log_bi[plain * 26 + mapped]
                for other in partners_r:
                    mapped = key[other]
                    if mapped >= 0:
                        delta += log_bi[mapped * 26 + plain]
                updated = list(key)
                updated[cipher_sym] = plain
                nxt.append((score + delta, tuple(updated), used | bit))
        nxt.sort(key=lambda item: (-item[0], item[1]))
        # Identical keys can arise only from equal assignments; keep the first.
        beams = nxt[:beam_width]

    best_score, best_key, _used = beams[0]
    plain_ints: list[int] = []
    for word in words:
        plain_ints.extend(best_key[c] for c in word)
    # Fill unused plaintext letters so the published key is a total map.
    used_plains = {p for p in best_key if p >= 0}
    free_plains = [p for p in range(26) if p not in used_plains]
    free_ciphers = [c for c, p in enumerate(best_key) if p < 0]
    filled = list(best_key)
    for cipher_sym, plain in zip(free_ciphers, free_plains):
        filled[cipher_sym] = plain
    rendered_letters = from_ints(plain_ints)
    # reinject walks every alphabetic character, including non A-Z.
    # Ciphertext for this solver is A-Z plus separators, so the skeleton matches.
    plaintext = reinject(ciphertext, rendered_letters)
    decrypt_key = "".join(chr(_A + p) for p in filled)
    return BeamDecipherResult(
        plaintext=plaintext,
        decrypt_key=decrypt_key,
        score=best_score,
        beam_width=beam_width,
        letters=letters,
    )


def letter_accuracy(guess: str, truth: str) -> float:
    """Fraction of A-Z letters that match, in order."""
    g = [ch for ch in guess.upper() if "A" <= ch <= "Z"]
    t = [ch for ch in truth.upper() if "A" <= ch <= "Z"]
    if len(g) != len(t) or not t:
        raise ValueError("guess and truth must contain the same number of A-Z letters")
    hits = sum(a == b for a, b in zip(g, t))
    return hits / len(t)
