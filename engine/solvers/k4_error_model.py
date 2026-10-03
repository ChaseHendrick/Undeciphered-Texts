"""Bounded K4 ciphertext-error search. Not a claimed solve.

One edit at a time (a substituted crib letter, a neighbor swap that
touches a crib, or a deletion or insertion that keeps each crib word
contiguous by shifting only the tail). Each edited string is paired
only with Vigenere periods 1 through 8 and Beaufort periods 1 through 8.
The cribs determine the repeating key. A free key letter is not searched.

A hit would need all four public cribs in place after the edit and a
quadgram score at least as high as the K3 control bar in k4_attempt.py.
Hits are stored as unverified candidates, never as a claimed plaintext.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from engine.alphabet import to_ints
from engine.ciphers import vigenere_decrypt
from engine.language import get_model
from engine.solvers.beaufort import beaufort_decrypt
from engine.solvers.k4_attempt import (
    CRIBS,
    ENGLISH_CONTROL,
    K4_CIPHERTEXT,
    english_pass,
)

PERIOD_MIN = 1
PERIOD_MAX = 8
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# 0-based, end exclusive. Same words and order as CRIBS.
_SPANS: tuple[tuple[int, int, str], ...] = tuple(
    (start - 1, start - 1 + len(word), word) for start, word, _cipher in CRIBS
)


@dataclass(frozen=True)
class MethodTally:
    """Counts only. No plaintext is stored on a tally."""

    method: str
    bound: str
    tried: int
    key_consistent: int
    crib_consistent: int
    bar_pass: int

    def line(self) -> str:
        return (
            f"{self.method}: bound {self.bound}; tried {self.tried}; "
            f"key-consistent {self.key_consistent}; "
            f"crib-consistent {self.crib_consistent}; "
            f"bar-pass {self.bar_pass}"
        )


@dataclass(frozen=True)
class UnverifiedCandidate:
    """A string that cleared the cribs and the bar. Not a solution."""

    model: str
    edit: str
    cipher: str
    period: int
    key: str
    candidate: str
    score: float

    @property
    def status(self) -> str:
        return "unverified"


@dataclass(frozen=True)
class K4ErrorReport:
    """Public result. claimed_plaintext stays None even if a candidate exists."""

    result: str
    solved: bool
    claimed_plaintext: None
    tallies: tuple[MethodTally, ...]
    unverified: tuple[UnverifiedCandidate, ...]
    ciphertext_sha256: str
    bar_score: float
    bar_mean: float

    def lines(self) -> tuple[str, ...]:
        return tuple(tally.line() for tally in self.tallies)


def _vig_key(cipher_ch: str, plain_ch: str) -> int:
    """K such that Vigenere decrypt of cipher_ch under K is plain_ch."""
    return (ord(cipher_ch) - ord(plain_ch)) % 26


def _beau_key(cipher_ch: str, plain_ch: str) -> int:
    """K such that Beaufort decrypt of cipher_ch under K is plain_ch."""
    return (ord(plain_ch) - 65 + ord(cipher_ch) - 65) % 26


def _decrypt(cipher: str, key: tuple[int, ...], beau: bool) -> str:
    out: list[str] = []
    period = len(key)
    for i, ch in enumerate(cipher):
        c = ord(ch) - 65
        k = key[i % period]
        p = (k - c) % 26 if beau else (c - k) % 26
        out.append(chr(65 + p))
    return "".join(out)


def _shifted_spans(kind: str, index: int) -> tuple[tuple[int, int, str], ...] | None:
    """Crib spans on the edited string, or None if a crib word is broken.

    kind is "sub", "swap", "del", or "ins". index is the edit site.
    A deletion or insertion inside a crib word is rejected. A deletion
    or insertion strictly before a crib shifts that crib and everything
    after it, which is how the tail stays consistent.
    """
    if kind in ("sub", "swap"):
        return _SPANS
    shifted: list[tuple[int, int, str]] = []
    for start, end, word in _SPANS:
        if kind == "del":
            if start <= index < end:
                return None
            delta = -1 if index < start else 0
        elif kind == "ins":
            if start < index < end:
                return None
            delta = 1 if index <= start else 0
        else:
            raise ValueError(kind)
        shifted.append((start + delta, end + delta, word))
    return tuple(shifted)


def _forced_key(
    cipher: str,
    spans: tuple[tuple[int, int, str], ...],
    period: int,
    beau: bool,
) -> tuple[int, ...] | None:
    """Repeating key implied by the cribs, or None on a column conflict.

    Periods 1 through 8 are covered by the 13-letter EASTNORTHEAST run,
    so a returned key has no free letter. Callers do not search a free letter.
    """
    columns: list[int | None] = [None] * period
    key_of = _beau_key if beau else _vig_key
    for start, _end, word in spans:
        for offset, plain_ch in enumerate(word):
            pos = start + offset
            residue = pos % period
            chosen = key_of(cipher[pos], plain_ch)
            if columns[residue] is None:
                columns[residue] = chosen
            elif columns[residue] != chosen:
                return None
    if any(slot is None for slot in columns):
        raise RuntimeError(
            "period was not fully crib-covered; refusing a free-key search"
        )
    return tuple(int(slot) for slot in columns)


def _cribs_match(plain: str, spans: tuple[tuple[int, int, str], ...]) -> bool:
    for start, end, word in spans:
        if plain[start:end] != word:
            return False
    return True


def _quadgram_stats(text: str, model) -> tuple[float, float]:
    seq = to_ints(text)
    total = model.score(seq)
    nquads = len(seq) - 3
    return total, total / nquads


def clears_bar(text: str, model, bar_score: float, bar_mean: float) -> bool:
    """True when the text meets the k4-attempt English bar.

    Length 97 uses the same total-score comparison as english_pass.
    A deletion or insertion is judged on the mean per quadgram, which
    is the same bar with the length factored out. A shorter string does
    not pass just because it sums fewer terms.
    """
    total, mean = _quadgram_stats(text, model)
    if len(text) == len(ENGLISH_CONTROL):
        return total >= bar_score
    return mean >= bar_mean


def _key_text(key: tuple[int, ...]) -> str:
    return "".join(chr(65 + k) for k in key)


def _check_inputs() -> None:
    if len(K4_CIPHERTEXT) != 97:
        raise ValueError("K4 ciphertext must be 97 letters")
    for start, end, word in _SPANS:
        if K4_CIPHERTEXT[start:end] != CRIBS[_SPANS.index((start, end, word))][2]:
            raise ValueError("span does not match the ciphertext crib fragment")
        if end - start != len(word):
            raise ValueError("span length does not match the crib word")
    # EASTNORTHEAST is 13 consecutive letters, so periods 1..8 are covered.
    if _SPANS[0][0] != 21 or _SPANS[1][1] != 34 or _SPANS[1][1] - _SPANS[0][0] != 13:
        raise ValueError("EASTNORTHEAST block is not the expected 13 letters")
    if PERIOD_MAX > 13:
        raise ValueError("period max exceeds the crib block that covers the key")


def _consider(
    cipher: str,
    spans: tuple[tuple[int, int, str], ...],
    *,
    model_name: str,
    edit: str,
    model,
    bar_score: float,
    bar_mean: float,
    hits: list[UnverifiedCandidate],
) -> tuple[int, int, int, int]:
    """Try both ciphers and periods 1..8. Returns tried, key-ok, crib-ok, bar-ok."""
    tried = 0
    key_ok = 0
    crib_ok = 0
    bar_ok = 0
    for beau, cipher_name in ((False, "vigenere"), (True, "beaufort")):
        for period in range(PERIOD_MIN, PERIOD_MAX + 1):
            tried += 1
            key = _forced_key(cipher, spans, period, beau)
            if key is None:
                continue
            key_ok += 1
            plain = _decrypt(cipher, key, beau)
            if not _cribs_match(plain, spans):
                continue
            crib_ok += 1
            if not clears_bar(plain, model, bar_score, bar_mean):
                continue
            bar_ok += 1
            total, _mean = _quadgram_stats(plain, model)
            hits.append(
                UnverifiedCandidate(
                    model=model_name,
                    edit=edit,
                    cipher=cipher_name,
                    period=period,
                    key=_key_text(key),
                    candidate=plain,
                    score=total,
                )
            )
    return tried, key_ok, crib_ok, bar_ok


def _crib_indexes() -> tuple[int, ...]:
    indexes: list[int] = []
    for start, end, _word in _SPANS:
        indexes.extend(range(start, end))
    return tuple(indexes)


def _swap_indexes() -> tuple[int, ...]:
    """Neighbor swaps that touch at least one crib letter. Others cannot change the key."""
    covered = set(_crib_indexes())
    return tuple(
        i for i in range(len(K4_CIPHERTEXT) - 1) if i in covered or (i + 1) in covered
    )


def _deletion_indexes() -> tuple[int, ...]:
    return tuple(
        i
        for i in range(len(K4_CIPHERTEXT))
        if _shifted_spans("del", i) is not None
    )


def _insertion_indexes() -> tuple[int, ...]:
    return tuple(
        i
        for i in range(len(K4_CIPHERTEXT) + 1)
        if _shifted_spans("ins", i) is not None
    )


def search_k4_errors() -> K4ErrorReport:
    """Run the bounded error models. Never sets a claimed plaintext."""
    _check_inputs()
    model = get_model()
    bar_score, bar_mean = _quadgram_stats(ENGLISH_CONTROL, model)
    if not english_pass(ENGLISH_CONTROL):
        raise RuntimeError("K3 control must clear its own bar")
    hits: list[UnverifiedCandidate] = []

    # Precondition: unmodified cribs already conflict for these periods.
    # That is why a substitution outside a crib cannot create a new key.
    base_spans = _shifted_spans("sub", 0)
    assert base_spans is not None
    base_counts = _consider(
        K4_CIPHERTEXT,
        base_spans,
        model_name="unmodified",
        edit="none",
        model=model,
        bar_score=bar_score,
        bar_mean=bar_mean,
        hits=hits,
    )
    if base_counts[1] != 0:
        raise RuntimeError("unmodified K4 produced a crib key; early stop is invalid")
    # The precondition check is not an error model and must not record a hit.
    if hits:
        raise RuntimeError("unmodified K4 recorded a candidate")

    sub_tried = sub_key = sub_crib = sub_bar = 0
    for index in _crib_indexes():
        original = K4_CIPHERTEXT[index]
        for letter in AZ:
            if letter == original:
                continue
            edited = K4_CIPHERTEXT[:index] + letter + K4_CIPHERTEXT[index + 1 :]
            counts = _consider(
                edited,
                base_spans,
                model_name="substitution",
                edit=f"substitute 1-based {index + 1} {original}->{letter}",
                model=model,
                bar_score=bar_score,
                bar_mean=bar_mean,
                hits=hits,
            )
            sub_tried += counts[0]
            sub_key += counts[1]
            sub_crib += counts[2]
            sub_bar += counts[3]

    swap_tried = swap_key = swap_crib = swap_bar = 0
    for index in _swap_indexes():
        edited_list = list(K4_CIPHERTEXT)
        edited_list[index], edited_list[index + 1] = edited_list[index + 1], edited_list[index]
        edited = "".join(edited_list)
        counts = _consider(
            edited,
            base_spans,
            model_name="adjacent-swap",
            edit=f"swap 1-based {index + 1} and {index + 2}",
            model=model,
            bar_score=bar_score,
            bar_mean=bar_mean,
            hits=hits,
        )
        swap_tried += counts[0]
        swap_key += counts[1]
        swap_crib += counts[2]
        swap_bar += counts[3]

    del_tried = del_key = del_crib = del_bar = 0
    for index in _deletion_indexes():
        spans = _shifted_spans("del", index)
        assert spans is not None
        edited = K4_CIPHERTEXT[:index] + K4_CIPHERTEXT[index + 1 :]
        counts = _consider(
            edited,
            spans,
            model_name="deletion",
            edit=f"delete 1-based {index + 1} ({K4_CIPHERTEXT[index]})",
            model=model,
            bar_score=bar_score,
            bar_mean=bar_mean,
            hits=hits,
        )
        del_tried += counts[0]
        del_key += counts[1]
        del_crib += counts[2]
        del_bar += counts[3]

    ins_tried = ins_key = ins_crib = ins_bar = 0
    for index in _insertion_indexes():
        spans = _shifted_spans("ins", index)
        assert spans is not None
        for letter in AZ:
            edited = K4_CIPHERTEXT[:index] + letter + K4_CIPHERTEXT[index:]
            counts = _consider(
                edited,
                spans,
                model_name="insertion",
                edit=f"insert {letter} before 1-based {index + 1}",
                model=model,
                bar_score=bar_score,
                bar_mean=bar_mean,
                hits=hits,
            )
            ins_tried += counts[0]
            ins_key += counts[1]
            ins_crib += counts[2]
            ins_bar += counts[3]

    outside = len(K4_CIPHERTEXT) - len(_crib_indexes())
    tallies = (
        MethodTally(
            "unmodified-precondition",
            "no edit; Vigenere and Beaufort periods 1 through 8; must be key-inconsistent",
            base_counts[0],
            base_counts[1],
            base_counts[2],
            base_counts[3],
        ),
        MethodTally(
            "substitution",
            (
                "one substituted letter at a crib position only "
                f"({len(_crib_indexes())} positions, 25 other letters); "
                f"{outside} non-crib positions skipped because the forced key cannot change; "
                "Vigenere and Beaufort periods 1 through 8"
            ),
            sub_tried,
            sub_key,
            sub_crib,
            sub_bar,
        ),
        MethodTally(
            "adjacent-swap",
            (
                "one neighbor swap that touches a crib letter "
                f"({len(_swap_indexes())} swaps); swaps outside the cribs skipped; "
                "Vigenere and Beaufort periods 1 through 8"
            ),
            swap_tried,
            swap_key,
            swap_crib,
            swap_bar,
        ),
        MethodTally(
            "deletion",
            (
                "one deleted letter that leaves every crib word contiguous, "
                "tail cribs shifted "
                f"({len(_deletion_indexes())} sites); "
                "Vigenere and Beaufort periods 1 through 8; "
                "bar is the per-quadgram mean of the K3 control"
            ),
            del_tried,
            del_key,
            del_crib,
            del_bar,
        ),
        MethodTally(
            "insertion",
            (
                "one inserted A-Z letter that leaves every crib word contiguous, "
                "tail cribs shifted "
                f"({len(_insertion_indexes())} sites, 26 letters); "
                "Vigenere and Beaufort periods 1 through 8; "
                "bar is the per-quadgram mean of the K3 control"
            ),
            ins_tried,
            ins_key,
            ins_crib,
            ins_bar,
        ),
    )
    digest = hashlib.sha256(K4_CIPHERTEXT.encode("ascii")).hexdigest()
    bar_hits = [hit for hit in hits if hit.model != "unmodified"]
    return K4ErrorReport(
        result="unverified" if bar_hits else "not solved",
        solved=False,
        claimed_plaintext=None,
        tallies=tallies,
        unverified=tuple(bar_hits),
        ciphertext_sha256=digest,
        bar_score=bar_score,
        bar_mean=bar_mean,
    )


def formulas_match_certified() -> bool:
    """The integer maps agree with the certified decrypt functions on one key."""
    sample_key = "KRYPTOS"
    vig = vigenere_decrypt(K4_CIPHERTEXT, sample_key)
    beau = beaufort_decrypt(K4_CIPHERTEXT, sample_key)
    vig_key = tuple((ord(ch) - 65) % 26 for ch in sample_key)
    # vigenere_decrypt uses the complementary key, so the integer map
    # must use the original keyword shifts, not the complement.
    beau_key = vig_key
    return (
        _decrypt(K4_CIPHERTEXT, vig_key, False) == vig
        and _decrypt(K4_CIPHERTEXT, beau_key, True) == beau
    )
