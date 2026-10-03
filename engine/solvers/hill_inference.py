"""Bounded unknown 2x2 Hill matrix inference from aligned plaintext letters.

Each inverse row is enumerated over Z/26Z, followed by compatible row pairs.
The resulting determinant must be coprime to 26. The column-vector convention
and published HELP -> HIAT example are from Arkadii Slinko's Auckland slides:
https://www.math.auckland.ac.nz/~slinko/Talks/AfC.pdf
"""

from __future__ import annotations

from collections.abc import Sequence
from functools import lru_cache
import heapq
from math import gcd

from engine.language import get_model
from engine.reverse_engineer import Crib
from engine.solvers.hill import _multiply_pairs, hill_encrypt

SOURCE_URL = "https://www.math.auckland.ac.nz/~slinko/Talks/AfC.pdf"
SCOPE = (
    "Aligned-crib inference inside the 2x2 column-vector Hill model modulo 26. "
    "English scores, supplied cribs and forward consistency are not independent "
    "evidence of a historical decipherment. No unknown-script or Nr. 86 solution is claimed."
)


def _integer(value, name, low, high):
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an integer")
    if not low <= value <= high:
        raise ValueError(f"{name} must be in {low}..{high}")


def _letters(text, name, minimum, maximum, raw_limit):
    if not isinstance(text, str):
        raise TypeError(f"{name} must be text")
    if len(text) > raw_limit or any(ch.isalnum() and not (ch.isascii() and ch.isalpha()) for ch in text):
        raise ValueError(f"{name} requires ASCII letters within the raw size bound")
    letters = "".join(ch.upper() for ch in text if ch.isascii() and ch.isalpha())
    if not minimum <= len(letters) <= maximum:
        raise ValueError(f"{name} requires {minimum}..{maximum} A-Z letters")
    return letters


def _inputs(text, cribs, max_checks, max_candidates):
    cipher = _letters(text, "ciphertext", 4, 512, 4096)
    if len(cipher) % 2:
        raise ValueError("Hill ciphertext requires complete two-letter blocks; missing letters are not padded")
    _integer(max_checks, "max_checks", 0, 100000)
    _integer(max_candidates, "max_candidates", 1, 100)
    if not isinstance(cribs, Sequence) or isinstance(cribs, (str, bytes, bytearray)):
        raise TypeError("cribs must be a finite sequence of Crib objects")
    if not 1 <= len(cribs) <= 128:
        raise ValueError("at least one and at most 128 aligned cribs are required")
    known = {}
    for crib in cribs:
        if not isinstance(crib, Crib):
            raise TypeError("cribs must contain engine.reverse_engineer.Crib objects")
        _integer(crib.offset, "crib offset", 0, len(cipher) - 1)
        plain = _letters(crib.plaintext, "crib", 1, 512, 2048)
        if crib.offset + len(plain) > len(cipher):
            raise ValueError("crib exceeds normalized plaintext length")
        for position, ch in enumerate(plain, crib.offset):
            if position in known and known[position] != ch:
                raise ValueError("overlapping cribs contradict each other")
            known[position] = ch
    return cipher, known


def infer_hill(text, *, cribs=(), max_checks=100000, max_candidates=20) -> dict:
    """Infer invertible matrices with one budget for row and row-pair trials.

    A crib may begin or end halfway through a block. Only its supplied letters
    constrain a row. Output counts and consensus cover every compatible key
    only after both row enumerations and all compatible pairs are exhausted.
    Prefix candidates are examples, without global uniqueness or consensus.
    """
    cipher, known = _inputs(text, cribs, max_checks, max_candidates)
    numbers = [ord(ch) - 65 for ch in cipher]
    constraints = [[], []]
    for position, letter in sorted(known.items()):
        block = position - position % 2
        constraints[position % 2].append((numbers[block], numbers[block + 1], ord(letter) - 65))
    rows = [[], []]
    row_checks = [0, 0]
    checks = pair_checks = accepted = mismatches = 0
    for row in range(2):
        for a in range(26):
            for b in range(26):
                if checks >= max_checks:
                    break
                checks += 1
                row_checks[row] += 1
                if all((a * x + b * y) % 26 == plain for x, y, plain in constraints[row]):
                    rows[row].append((a, b))
            if checks >= max_checks:
                break
    rows_complete = row_checks == [676, 676]
    pair_total = len(rows[0]) * len(rows[1]) if rows_complete else None
    heap = []
    consensus = first_plaintext = None
    plaintext_unique = True
    language = None

    @lru_cache(maxsize=1024)
    def score(plain):
        nonlocal language
        if language is None:
            language = get_model()
        return language.score([ord(ch) - 65 for ch in plain])

    if rows_complete:
        for a, b in rows[0]:
            for c, d in rows[1]:
                if checks >= max_checks:
                    break
                checks += 1
                pair_checks += 1
                determinant = (a * d - b * c) % 26
                if gcd(determinant, 26) != 1:
                    continue
                inverse_det = pow(determinant, -1, 26)
                encryption = tuple(v % 26 for v in
                                   (inverse_det * d, -inverse_det * b,
                                    -inverse_det * c, inverse_det * a))
                plain = _multiply_pairs(cipher, (a, b, c, d))
                key_text = " ".join(str(value) for value in encryption)
                if (hill_encrypt(plain, key_text) != cipher
                        or any(plain[position] != ch for position, ch in known.items())):
                    mismatches += 1
                    continue
                accepted += 1
                if consensus is None:
                    consensus = list(plain)
                    first_plaintext = plain
                else:
                    plaintext_unique = plaintext_unique and plain == first_plaintext
                    consensus = [old if old == new else "?" for old, new in zip(consensus, plain)]
                candidate = {
                    "family": "hill", "matrix": [list(encryption[:2]), list(encryption[2:])],
                    "inverse_matrix": [[a, b], [c, d]], "key": key_text,
                    "plaintext": plain, "score": score(plain),
                    "forward_consistent": True, "crib_match": True,
                    "evidence": "invertible key, supplied aligned letters, and forward replay; correctness unverified",
                }
                entry = (candidate["score"], tuple(-v for v in encryption), pair_checks, candidate)
                if len(heap) < max_candidates:
                    heapq.heappush(heap, entry)
                elif entry[:3] > heap[0][:3]:
                    heapq.heapreplace(heap, entry)
            if checks >= max_checks:
                break
    complete = rows_complete and pair_checks == pair_total and mismatches == 0
    candidates = [entry[3] for entry in sorted(heap, reverse=True)]
    premise_plaintext = "".join(known.get(position, "?") for position in range(len(cipher)))
    return {
        "kind": "hill_crib_key_inference", "method": "hill-inference",
        "mode": "unknown_key_with_aligned_cribs", "candidates": candidates,
        "checks": checks, "row_checks": row_checks, "key_pair_checks": pair_checks,
        "compatible_rows_seen": [len(row) for row in rows], "rows_complete": rows_complete,
        "compatible_keys_seen": accepted, "compatible_key_count": accepted if complete else None,
        "key_unique_within_model": accepted == 1 if complete else None,
        "plaintext_unique_within_model": bool(accepted) and plaintext_unique if complete else None,
        "consensus_plaintext": "".join(consensus) if complete and consensus is not None else None,
        "supplied_plaintext_positions": premise_plaintext,
        "candidates_truncated": accepted > len(candidates),
        "search_complete": complete,
        "stop_reason": "transform_inconsistency" if mismatches else "complete" if complete else "check_limit",
        "forward_mismatches": mismatches, "claimed_plaintext": None,
        "correctness_known": False,
        "ranking": "repository English quadgram score, then encryption matrix order; not correctness",
        "coordinate_system": "zero-based A-Z plaintext letters after removing spaces and punctuation",
        "bounds": {
            "max_checks": max_checks, "max_candidates": max_candidates, "max_letters": 512,
            "inverse_row_trials": [676, 676], "compatible_row_pair_trials": pair_total,
            "total_declared_checks": 1352 + pair_total if pair_total is not None else None,
            "check_unit": "one inverse-row coefficient trial or one compatible-row pair with applicable forward replay",
            "completion_scope": "all invertible 2x2 column-vector Hill keys modulo 26 compatible with supplied aligned letters",
            "padding": "No padding is added or removed; a recovered trailing X is retained",
        },
        "source_url": SOURCE_URL, "scope": SCOPE,
    }


__all__ = ["infer_hill", "SOURCE_URL", "SCOPE"]
