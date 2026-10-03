"""ACA Redefence: ranked rail readout, cyclic offset, and bounded key search.

Source: https://www.cryptogram.org/downloads/aca.info/ciphers/Redefence.pdf
The supplied-key vector and its equivalent key follow the printed diagram.
Search candidates are English-score hypotheses, never verified unique readings.
"""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import asdict, dataclass
from itertools import permutations
import math

from engine.language import get_model
from engine.result import SolveResult

ACA_REDEFENCE_URL = "https://www.cryptogram.org/downloads/aca.info/ciphers/Redefence.pdf"
ACA_REDEFENCE_PLAIN = "CIVILWARFIELDCIPHER"
ACA_REDEFENCE_CIPHER = "IIWRILCPECLFDHVAEIR"
ACA_REDEFENCE_KEY = "213"
ACA_REDEFENCE_OFFSET = 0
MAX_LETTERS = 4096
MAX_SEARCH_LETTERS = 1024


def _integer(value, name: str, low: int, high: int) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an integer")
    if not low <= value <= high:
        raise ValueError(f"{name} must be in {low}..{high}")
    return value


def _letters(text: str, maximum: int = MAX_LETTERS) -> str:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if len(text) > 4 * maximum or any(ch.isalpha() and not ch.isascii() for ch in text):
        raise ValueError("text must use ASCII letters within the input size bound")
    result = "".join(ch.upper() for ch in text if ch.isascii() and ch.isalpha())
    if not 1 <= len(result) <= maximum:
        raise ValueError(f"text must contain 1..{maximum} A-Z letters")
    return result


def parse_redefence_key(key: str | Sequence[int]) -> tuple[int, ...]:
    """Top-to-bottom row ranks, a permutation of 1..r for 3..7 rails."""
    if isinstance(key, str):
        if len(key) > 32:
            raise ValueError("rank string exceeds the key size bound")
        value = key.strip()
        if not 3 <= len(value) <= 7 or any(ch not in "1234567" for ch in value):
            raise ValueError("Redefence key must contain ASCII row-rank digits")
        ranks = tuple(int(ch) for ch in value)
    elif isinstance(key, Sequence) and not isinstance(key, (bytes, bytearray)):
        if len(key) > 7:
            raise ValueError("Redefence supports 3..7 rails")
        ranks = tuple(key)
        if any(not isinstance(rank, int) or isinstance(rank, bool) for rank in ranks):
            raise TypeError("row ranks must be integers")
    else:
        raise TypeError("key must be a rank string or finite integer sequence")
    if not 3 <= len(ranks) <= 7 or set(ranks) != set(range(1, len(ranks) + 1)):
        raise ValueError("key must be a permutation of 1..r for 3..7 rails")
    return ranks


def _rows(length: int, rails: int, offset: int) -> list[int]:
    cycle = 2 * (rails - 1)
    return [min((index + offset) % cycle, cycle - (index + offset) % cycle) for index in range(length)]


def _decrypt(cipher: str, ranks: tuple[int, ...], rows: list[int]) -> str:
    counts = [0] * len(ranks)
    for row in rows:
        counts[row] += 1
    buckets = [""] * len(ranks)
    cursor = 0
    for row in sorted(range(len(ranks)), key=ranks.__getitem__):
        buckets[row] = cipher[cursor:cursor + counts[row]]
        cursor += counts[row]
    used = [0] * len(ranks)
    plain = []
    for row in rows:
        plain.append(buckets[row][used[row]])
        used[row] += 1
    return "".join(plain)


def redefence_encrypt(text: str, key: str | Sequence[int], *, offset: int = 0) -> str:
    ranks = parse_redefence_key(key)
    _integer(offset, "offset", 0, 2 * (len(ranks) - 1) - 1)
    plain = _letters(text)
    buckets = [[] for _ in ranks]
    for ch, row in zip(plain, _rows(len(plain), len(ranks), offset)):
        buckets[row].append(ch)
    return "".join("".join(buckets[row]) for row in sorted(range(len(ranks)), key=ranks.__getitem__))


def redefence_decrypt(text: str, key: str | Sequence[int], *, offset: int = 0) -> str:
    ranks = parse_redefence_key(key)
    _integer(offset, "offset", 0, 2 * (len(ranks) - 1) - 1)
    cipher = _letters(text)
    return _decrypt(cipher, ranks, _rows(len(cipher), len(ranks), offset))


@dataclass(frozen=True)
class RedefenceCandidate:
    plaintext: str
    key: str
    offset: int
    score: float


@dataclass(frozen=True)
class RedefenceSearchResult:
    candidates: tuple[RedefenceCandidate, ...]
    keys_examined: int
    total_keys: int
    search_complete: bool
    stop_reason: str
    min_rails: int
    max_rails: int
    max_keys: int
    max_candidates: int
    top_score_tied: bool
    uniqueness: str = "not_established"
    scope: str = "English-score-ranked finite key search; no unique or verified historical solve."

    def to_dict(self) -> dict:
        return asdict(self)


def search_redefence(text: str, *, min_rails: int = 3, max_rails: int = 5,
                     max_keys: int = 5000, max_candidates: int = 10) -> RedefenceSearchResult:
    """Enumerate rail ranks and every cyclic offset, retaining top scored keys.

    Completion means the requested finite range was exhausted, not that the
    cipher family is proved or the top English score establishes uniqueness.
    Equivalent keys and tied plaintexts may occur. No key or plaintext is given.
    """
    _integer(min_rails, "min_rails", 3, 7)
    _integer(max_rails, "max_rails", min_rails, 7)
    _integer(max_keys, "max_keys", 1, 100000)
    _integer(max_candidates, "max_candidates", 1, 100)
    cipher = _letters(text, MAX_SEARCH_LETTERS)
    if len(cipher) < 4:
        raise ValueError("score-ranked search requires at least four letters")
    total = sum(math.factorial(rails) * 2 * (rails - 1) for rails in range(min_rails, max_rails + 1))
    model = get_model()
    best: list[RedefenceCandidate] = []
    examined = 0
    best_score = -math.inf
    top_count = 0
    for rails in range(min_rails, max_rails + 1):
        paths = [_rows(len(cipher), rails, offset) for offset in range(2 * (rails - 1))]
        for ranks in permutations(range(1, rails + 1)):
            key = "".join(map(str, ranks))
            for offset, rows in enumerate(paths):
                if examined >= max_keys:
                    break
                plain = _decrypt(cipher, ranks, rows)
                score = model.score([ord(ch) - 65 for ch in plain])
                candidate = RedefenceCandidate(plain, key, offset, score)
                examined += 1
                if score > best_score:
                    best_score, top_count = score, 1
                elif score == best_score:
                    top_count += 1
                best.append(candidate)
                best.sort(key=lambda item: (-item.score, item.key, item.offset))
                if len(best) > max_candidates:
                    best.pop()
            if examined >= max_keys:
                break
        if examined >= max_keys:
            break
    complete = examined == total
    return RedefenceSearchResult(tuple(best), examined, total, complete,
                                "complete" if complete else "key_limit", min_rails, max_rails,
                                max_keys, max_candidates, top_count > 1)


def solve_redefence(text: str, *, key: str | Sequence[int] | None = None,
                   offset: int = 0, min_rails: int = 3, max_rails: int = 5,
                   max_keys: int = 5000, max_candidates: int = 10) -> SolveResult:
    if key is not None:
        ranks = parse_redefence_key(key)
        plain = redefence_decrypt(text, ranks, offset=offset)
        key_text = "".join(map(str, ranks))
        return SolveResult("redefence", plain, f"{key_text} {offset}", float(len(plain)),
                           {"mode": "supplied_key", "key": key_text, "offset": offset,
                            "source_url": ACA_REDEFENCE_URL, "scope": "Supplied-key classical decryption."})
    _integer(offset, "offset without a supplied key", 0, 0)
    report = search_redefence(text, min_rails=min_rails, max_rails=max_rails,
                             max_keys=max_keys, max_candidates=max_candidates)
    top = report.candidates[0]
    details = report.to_dict()
    details.update(mode="score_ranked_search", verified_historical_solve=False, source_url=ACA_REDEFENCE_URL)
    return SolveResult("redefence", top.plaintext, f"{top.key} {top.offset}", top.score, details)
