"""Keyword panel on Kryptos K4. Not a claimed decipherment.

The only keywords are the published K1 key, the published K2 key, and the
KRYPTOS alphabet keyword already printed in this repo. This is not a search
over a dictionary. A crib match is not a K4 decipherment.
"""

from __future__ import annotations

from dataclasses import dataclass

from engine.alphabet import letters_only
from engine.solvers.gromark import gromark_decrypt
from engine.solvers.k4_attempt import (
    K4_CIPHERTEXT,
    KEYED_ALPHABET_KEYWORD,
    cribs_in_place,
    english_pass,
)
from engine.solvers.playfair import playfair_decrypt
from engine.solvers.porta import porta_decrypt
from engine.solvers.two_square import square_from_keyword, two_square_decrypt

# Published K1 and K2 keys, copied from tests/test_keyed_vigenere.py.
# KRYPTOS is KEYED_ALPHABET_KEYWORD in engine/solvers/k4_attempt.py.
K1_KEY = "PALIMPSEST"
K2_KEY = "ABSCISSA"
KEYWORDS: tuple[str, ...] = (K1_KEY, K2_KEY, KEYED_ALPHABET_KEYWORD)

UNVERIFIED_CAP = 20


@dataclass(frozen=True)
class MethodTally:
    """Counts for one decryptor.

    tried is the number of calls that returned 97 letters.
    rejected is the number that raised or returned another length.
    tried + rejected is the keyword count, or the ordered-pair count.
    """

    method: str
    bound: str
    tried: int
    rejected: int
    crib_consistent: int
    english_pass: int

    def line(self) -> str:
        return (
            f"{self.method}: bound {self.bound}; tried {self.tried}; "
            f"rejected {self.rejected}; crib-consistent {self.crib_consistent}; "
            f"english-pass {self.english_pass}"
        )


@dataclass(frozen=True)
class UnverifiedCandidate:
    """A 97-letter string that places the public cribs. Not a solution."""

    method: str
    key: str
    candidate: str
    english_pass: bool

    @property
    def status(self) -> str:
        return "unverified"


@dataclass(frozen=True)
class KeywordPanelReport:
    """Public result. solved stays false. claimed_plaintext stays None."""

    solved: bool
    claimed_plaintext: None
    tallies: tuple[MethodTally, ...]
    unverified: tuple[UnverifiedCandidate, ...]

    def __post_init__(self) -> None:
        if self.solved is not False:
            raise ValueError("solved stays false")
        if self.claimed_plaintext is not None:
            raise ValueError("claimed_plaintext stays None")

    def lines(self) -> tuple[str, ...]:
        return tuple(tally.line() for tally in self.tallies)


def _pairs() -> tuple[tuple[str, str], ...]:
    """Ordered pairs of two different keywords. Not the 9 same-keyword pairs."""
    return tuple(
        (left, right)
        for left in KEYWORDS
        for right in KEYWORDS
        if left != right
    )


def _accept(plain: object) -> str | None:
    """97-letter A-Z stream, or None when the call is not that length."""
    if not isinstance(plain, str):
        return None
    letters = letters_only(plain)
    if len(letters) != len(K4_CIPHERTEXT):
        return None
    return letters


def _call(decrypt, *args: str) -> str | None:
    """Run one decryptor. A raise is a rejection, not a crash."""
    try:
        plain = decrypt(*args)
    except Exception:
        return None
    return _accept(plain)


class _Bucket:
    def __init__(self, method: str, bound: str) -> None:
        self.method = method
        self.bound = bound
        self.tried = 0
        self.rejected = 0
        self.crib_consistent = 0
        self.english_pass = 0

    def add(self, plain: str | None, key: str, unverified: list[UnverifiedCandidate]) -> None:
        if plain is None:
            self.rejected += 1
            return
        self.tried += 1
        crib_ok = cribs_in_place(plain)
        english_ok = english_pass(plain)
        if crib_ok:
            self.crib_consistent += 1
            if len(unverified) < UNVERIFIED_CAP:
                unverified.append(
                    UnverifiedCandidate(
                        method=self.method,
                        key=key,
                        candidate=plain,
                        english_pass=english_ok,
                    )
                )
        if english_ok:
            self.english_pass += 1

    def tally(self) -> MethodTally:
        return MethodTally(
            method=self.method,
            bound=self.bound,
            tried=self.tried,
            rejected=self.rejected,
            crib_consistent=self.crib_consistent,
            english_pass=self.english_pass,
        )


def keyword_panel() -> KeywordPanelReport:
    """Decrypt K4 under the three published keywords. Never claims a plaintext.

    Playfair and two-square see an odd 97-letter string and are not padded.
    Gromark is called with the keyword alone. That function also requires a
    5-digit primer, which is not in this keyword list and is not invented.
    """
    if KEYWORDS != ("PALIMPSEST", "ABSCISSA", "KRYPTOS"):
        raise ValueError("keyword list is the three published strings only")
    if len(K4_CIPHERTEXT) != 97:
        raise ValueError("K4 ciphertext must be 97 letters")
    pairs = _pairs()
    if len(pairs) != 6:
        raise ValueError("two-square uses 6 ordered pairs, not 9")

    unverified: list[UnverifiedCandidate] = []
    playfair = _Bucket(
        "playfair",
        "one square per keyword PALIMPSEST, ABSCISSA, KRYPTOS; odd length rejected, not padded",
    )
    porta = _Bucket(
        "porta",
        "one repeating keyword per PALIMPSEST, ABSCISSA, KRYPTOS",
    )
    gromark = _Bucket(
        "gromark",
        "keyword alone for PALIMPSEST, ABSCISSA, KRYPTOS; no primer added",
    )
    two_square = _Bucket(
        "two-square",
        "6 ordered pairs of two different keywords; same-keyword pairs not called; odd length rejected, not padded",
    )

    for keyword in KEYWORDS:
        playfair.add(_call(playfair_decrypt, K4_CIPHERTEXT, keyword), keyword, unverified)
        porta.add(_call(porta_decrypt, K4_CIPHERTEXT, keyword), keyword, unverified)
        gromark.add(_call(gromark_decrypt, K4_CIPHERTEXT, keyword), keyword, unverified)

    for left_kw, right_kw in pairs:
        label = f"{left_kw}/{right_kw}"
        try:
            left = square_from_keyword(left_kw)
            right = square_from_keyword(right_kw)
        except Exception:
            two_square.add(None, label, unverified)
            continue
        two_square.add(
            _call(two_square_decrypt, K4_CIPHERTEXT, left, right),
            label,
            unverified,
        )

    # A crib match is not a K4 decipherment.
    return KeywordPanelReport(
        solved=False,
        claimed_plaintext=None,
        tallies=(
            playfair.tally(),
            porta.tally(),
            gromark.tally(),
            two_square.tally(),
        ),
        unverified=tuple(unverified),
    )


__all__ = [
    "K1_KEY",
    "K2_KEY",
    "KEYWORDS",
    "KeywordPanelReport",
    "MethodTally",
    "UNVERIFIED_CAP",
    "UnverifiedCandidate",
    "keyword_panel",
]
