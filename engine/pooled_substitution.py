"""Pooled bijective substitution, kept separate from Bob.

Alice, Shen and Smith (arXiv:2509.07282) pool each symbol and force a
permutation. This module is that constraint only: one count per ciphertext
letter, a hard one-to-one assignment, and a bounded swap polish. It is not
their Transformer, and a higher score is not a historical reading.
"""

from __future__ import annotations

import random

from engine.alphabet import letters_only, to_ints
from engine.german import get_german_model
from engine.language import ENGLISH_ORDER, get_legacy_model

SWAPS = 200
SEED = 20261004


def _order_from_weights(weights: tuple[float, ...] | list[float]) -> str:
    ranks = sorted(range(26), key=lambda index: (-weights[index], index))
    return "".join(chr(65 + index) for index in ranks)


def german_unigram_order() -> str:
    """Most common Grimm letter first. Not a military frequency table."""
    return _order_from_weights(get_german_model().unigram)


def _counts(seq: list[int]) -> list[int]:
    counts = [0] * 26
    for index in seq:
        counts[index] += 1
    return counts


def pooled_key(seq: list[int], order: str, *, bijective: bool) -> list[int]:
    """Map cipher index to plain index. Counts are pooled across the text.

    Bijective keys are a permutation. Colliding keys reuse the most common
    plaintext letter for every cipher letter after the first eight.
    """
    if len(order) != 26 or len(set(order)) != 26:
        raise ValueError("letter order must be 26 distinct letters")
    cipher_order = sorted(range(26), key=lambda index: (-_counts(seq)[index], index))
    plain = [ord(char) - 65 for char in order]
    key = [0] * 26
    for rank, cipher_index in enumerate(cipher_order):
        key[cipher_index] = plain[rank if bijective else min(rank, 7)]
    return key


def _apply(seq: list[int], key: list[int]) -> list[int]:
    return [key[index] for index in seq]


def _quadgram(seq: list[int], language: str) -> float:
    if language == "english":
        return get_legacy_model().score(seq)
    if language == "german":
        return get_german_model().quadgram_score(seq)
    raise ValueError("language must be english or german")


def polish(
    seq: list[int],
    key: list[int],
    language: str,
    *,
    bijective: bool,
    seed: int,
) -> tuple[list[int], float]:
    """Keep a swap only when the pooled decrypt scores higher. ``SWAPS`` tries."""
    rng = random.Random(seed)
    current = key[:]
    score = _quadgram(_apply(seq, current), language)
    for _ in range(SWAPS):
        trial = current[:]
        left = rng.randrange(26)
        right = rng.randrange(26)
        if left == right:
            continue
        if bijective:
            trial[left], trial[right] = trial[right], trial[left]
        else:
            trial[left] = trial[right]
        trial_score = _quadgram(_apply(seq, trial), language)
        if trial_score > score:
            current = trial
            score = trial_score
    return current, score


def character_accuracy(plain: list[int], recovered: list[int]) -> float:
    if len(plain) != len(recovered) or not plain:
        raise ValueError("accuracy needs two equal nonempty strings")
    hits = sum(left == right for left, right in zip(plain, recovered))
    return hits / len(plain)


def encrypt_permutation(plain: str, key: list[int]) -> str:
    """Encrypt with the inverse of a bijective decrypt key."""
    if len(key) != 26 or len(set(key)) != 26:
        raise ValueError("encryption needs a permutation")
    inverse = [0] * 26
    for cipher_index, plain_index in enumerate(key):
        inverse[plain_index] = cipher_index
    letters = letters_only(plain)
    return "".join(chr(65 + inverse[ord(char) - 65]) for char in letters)


def search_pooled(text: str, language: str, *, seed: int = SEED) -> dict:
    """Score one text. The decrypt is not returned."""
    seq = to_ints(letters_only(text))
    if len(seq) < 16:
        raise ValueError("text needs at least 16 letters")
    order = ENGLISH_ORDER if language == "english" else german_unigram_order()
    bijective_key = pooled_key(seq, order, bijective=True)
    colliding_key = pooled_key(seq, order, bijective=False)
    _, bijective_score = polish(seq, bijective_key, language, bijective=True, seed=seed)
    _, colliding_score = polish(seq, colliding_key, language, bijective=False, seed=seed)
    shuffled = seq[:]
    random.Random(seed).shuffle(shuffled)
    shuffle_key = pooled_key(shuffled, order, bijective=True)
    _, control_score = polish(shuffled, shuffle_key, language, bijective=True, seed=seed)
    return {
        "language": language,
        "letters": len(seq),
        "bijective_score": bijective_score,
        "colliding_score": colliding_score,
        "control_score": control_score,
        "beats_control": bijective_score > control_score,
        "beats_colliding": bijective_score > colliding_score,
    }


def search_pooled_swarm() -> dict:
    """Run the pooled key on two unread texts. No plaintext is stored."""
    from engine.solvers.k4_attempt import K4_CIPHERTEXT
    from engine.ts_close_pairs import IASRZ_129

    rows = []
    for name, text in (("IASRZ_129", IASRZ_129), ("K4", K4_CIPHERTEXT)):
        for language in ("english", "german"):
            row = search_pooled(text, language)
            row["text"] = name
            rows.append(row)
    return {
        "claimed_plaintext": None,
        "solved": False,
        "swaps": SWAPS,
        "seed": SEED,
        "rows": rows,
        "scope": "Pooled substitution scores against a shuffled control. Beating it is not a reading.",
    }
