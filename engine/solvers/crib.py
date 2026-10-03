"""Slide a known crib through a standard A–Z Vigenère ciphertext.

At each alignment the crib implies a keystream. A period is kept only when
those shifts agree with each other and every key position is filled at least
once. The repeating key is then applied to the whole letter stream. A crib
hit writes the crib back by construction; letters outside the crib are only
a Vigenère hypothesis. This is not a solver for a digraph cipher.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from engine.alphabet import from_ints, letters_only, reinject, to_ints
from engine.language import get_model


@dataclass(frozen=True)
class CribHit:
    offset: int
    period: int
    key: str
    checks: int
    score: float
    plaintext: str


def search_vigenere_crib(
    text: str,
    crib: str,
    max_period: int = 12,
    min_checks: int = 1,
    scorer: Callable[[list[int]], float] | None = None,
) -> list[CribHit]:
    """Return consistent, fully determined Vigenère keys, best score first.

    ``min_checks`` is the number of crib letters that must confirm a key
    letter already implied by an earlier crib letter. The default rejects a
    period that the crib only paints once.
    """
    cipher = letters_only(text)
    plain_crib = letters_only(crib)
    if len(plain_crib) < 2:
        raise ValueError("crib must contain at least two letters")
    if len(plain_crib) > len(cipher):
        raise ValueError("crib is longer than the ciphertext")
    if max_period < 1:
        raise ValueError("max_period must be positive")
    if min_checks < 1:
        raise ValueError("min_checks must be positive")
    score_fn = scorer or (lambda seq: get_model().score(seq))
    cipher_seq = to_ints(cipher)
    crib_seq = to_ints(plain_crib)
    limit = min(max_period, len(plain_crib) - min_checks)
    hits: list[CribHit] = []
    for start in range(len(cipher) - len(plain_crib) + 1):
        stream = [(cipher_seq[start + i] - crib_seq[i]) % 26 for i in range(len(plain_crib))]
        for period in range(1, limit + 1):
            key_slots: list[int | None] = [None] * period
            checks = 0
            consistent = True
            for index, shift in enumerate(stream):
                slot = (start + index) % period
                current = key_slots[slot]
                if current is None:
                    key_slots[slot] = shift
                elif current != shift:
                    consistent = False
                    break
                else:
                    checks += 1
            if not consistent or checks < min_checks:
                continue
            if any(slot is None for slot in key_slots):
                continue
            key = [int(slot) for slot in key_slots]
            plain = [(cipher_seq[i] - key[i % period]) % 26 for i in range(len(cipher_seq))]
            hits.append(
                CribHit(
                    offset=start,
                    period=period,
                    key="".join(chr(65 + shift) for shift in key),
                    checks=checks,
                    score=score_fn(plain),
                    plaintext=reinject(text, from_ints(plain)),
                )
            )
    hits.sort(key=lambda hit: (-hit.score, hit.period, hit.offset))
    return hits
