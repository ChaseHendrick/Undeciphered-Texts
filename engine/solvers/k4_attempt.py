"""Bounded Kryptos K4 search over certified classical ciphers.

The search uses only decrypt functions and the Vigenere crib slide already
in this repo. It tries short repeating keys and small transposition widths
against the public Sanborn cribs. It does not claim a K4 plaintext.
"""

from __future__ import annotations

import hashlib
from collections.abc import Callable
from dataclasses import dataclass

from engine.alphabet import letters_only, to_ints
from engine.ciphers import vigenere_decrypt
from engine.language import get_model
from engine.solvers.beaufort import beaufort_decrypt
from engine.solvers.columnar import (
    KRYPTOS_K3_PLAINTEXT,
    columnar_decrypt_right_to_left,
    double_columnar_decrypt,
)
from engine.solvers.crib import search_vigenere_crib
from engine.solvers.keyed_vigenere import keyed_vigenere_decrypt
from engine.solvers.route import route_decrypt
from engine.solvers.vigenere import solve_vigenere

# Sculpture passage 4, letters only, as transcribed on Wikipedia "Kryptos"
# (fetched 2026-10-02): https://en.wikipedia.org/wiki/Kryptos
# The CIA artifact page was fetched the same day and does not print the letters:
# https://www.cia.gov/legacy/museum/artifact/kryptos/
K4_CIPHERTEXT = (
    "OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTT"
    "MZFPKWGDKZXTJCDIGKUHUAUEKCAR"
)

# 1-based starts. Cipher fragments are the ones named on the fetched Wikipedia page.
CRIBS: tuple[tuple[int, str, str], ...] = (
    (22, "EAST", "FLRV"),
    (26, "NORTHEAST", "QQPRNGKSS"),
    (64, "BERLIN", "NYPVTT"),
    (70, "CLOCK", "MZFPK"),
)

# Known-phrase English floor, fixed before any K4 decrypt is scored.
# First 97 letters of the published K3 plaintext already in this repo.
ENGLISH_CONTROL = KRYPTOS_K3_PLAINTEXT[:97]

PERIOD_MIN = 1
PERIOD_MAX = 12
COLUMNAR_WIDTH_MIN = 2
COLUMNAR_WIDTH_MAX = 12
ROUTE_WIDTH_MIN = 1
ROUTE_WIDTH_MAX = 12
KEYED_ALPHABET_KEYWORD = "KRYPTOS"
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

DecryptFn = Callable[[str, str], str]


@dataclass(frozen=True)
class MethodTally:
    """Counts only. No plaintext is stored."""

    method: str
    bound: str
    tried: int
    decrypted: int
    crib_consistent: int
    english_pass: int

    def line(self) -> str:
        return (
            f"{self.method}: bound {self.bound}; tried {self.tried}; "
            f"decrypted {self.decrypted}; crib-consistent {self.crib_consistent}; "
            f"english-pass {self.english_pass}"
        )


@dataclass(frozen=True)
class K4SearchReport:
    """Public result of the bounded attempt. claimed_plaintext stays None."""

    result: str
    solved: bool
    claimed_plaintext: None
    tallies: tuple[MethodTally, ...]
    ciphertext_sha256: str

    def lines(self) -> tuple[str, ...]:
        return tuple(tally.line() for tally in self.tallies)


def cribs_in_place(text: str) -> bool:
    """True only when all four public cribs sit at their published positions."""
    letters = letters_only(text)
    if len(letters) != len(K4_CIPHERTEXT):
        return False
    for start, word, _cipher in CRIBS:
        end = start - 1 + len(word)
        if letters[start - 1 : end] != word:
            return False
    return True


def english_pass(text: str) -> bool:
    """True when a 97-letter string scores at least as high as the K3 control.

    The model is the repo quadgram scorer. The control is ENGLISH_CONTROL,
    not a threshold fit to K4. Higher (less negative) is better. Equal length
    keeps the comparison a sum over the same number of quadgrams.
    """
    letters = letters_only(text)
    if len(letters) != len(ENGLISH_CONTROL):
        return False
    model = get_model()
    return model.score(to_ints(letters)) >= model.score(to_ints(ENGLISH_CONTROL))


def _check_inputs() -> None:
    if len(K4_CIPHERTEXT) != 97 or letters_only(K4_CIPHERTEXT) != K4_CIPHERTEXT:
        raise ValueError("K4 ciphertext must be 97 letters")
    if len(ENGLISH_CONTROL) != 97:
        raise ValueError("English control must be 97 letters")
    for start, word, cipher in CRIBS:
        got = K4_CIPHERTEXT[start - 1 : start - 1 + len(word)]
        if got != cipher:
            raise ValueError(f"ciphertext at {start} is {got}, expected {cipher}")
    if not K4_CIPHERTEXT.startswith("OBKR"):
        raise ValueError("K4 ciphertext must start with OBKR")


def _forced_key(decrypt: DecryptFn, period: int) -> str | None:
    """Repeating key implied by the cribs, or None if the period conflicts.

    Every residue class in 1..period is covered by the cribs for periods
    1 through 12, so a returned key is fully determined. Two key letters
    that both map one cipher letter onto the crib is treated as a conflict.
    """
    columns: list[str | None] = [None] * period
    for start, word, _cipher in CRIBS:
        for offset, plain_ch in enumerate(word):
            pos = start - 1 + offset
            cipher_ch = K4_CIPHERTEXT[pos]
            residue = pos % period
            matches = [
                key_letter
                for key_letter in AZ
                if decrypt(cipher_ch, key_letter) == plain_ch
            ]
            if len(matches) != 1:
                return None
            chosen = matches[0]
            if columns[residue] is None:
                columns[residue] = chosen
            elif columns[residue] != chosen:
                return None
    if any(slot is None for slot in columns):
        return None
    return "".join(str(slot) for slot in columns)


def _tally_periodic(method: str, bound: str, decryptors: tuple[DecryptFn, ...]) -> MethodTally:
    tried = 0
    decrypted = 0
    crib_ok = 0
    english_ok = 0
    for decrypt in decryptors:
        for period in range(PERIOD_MIN, PERIOD_MAX + 1):
            tried += 1
            key = _forced_key(decrypt, period)
            if key is None:
                continue
            plain = decrypt(K4_CIPHERTEXT, key)
            decrypted += 1
            if not cribs_in_place(plain):
                continue
            crib_ok += 1
            if english_pass(plain):
                english_ok += 1
    return MethodTally(method, bound, tried, decrypted, crib_ok, english_ok)


def _keyed_decryptors() -> tuple[DecryptFn, ...]:
    def make(index_letter: str) -> DecryptFn:
        def decrypt(text: str, key: str) -> str:
            return keyed_vigenere_decrypt(
                text,
                key,
                KEYED_ALPHABET_KEYWORD,
                index_letter,
            )

        return decrypt

    return tuple(make(letter) for letter in AZ)


def _tally_crib_slide() -> MethodTally:
    """Certified single-crib slide. Only the published EASTNORTHEAST offset can pass."""
    hits = search_vigenere_crib(
        K4_CIPHERTEXT,
        "EASTNORTHEAST",
        max_period=PERIOD_MAX,
    )
    known_offset = 21  # 0-based index of 1-based position 22
    eligible = [hit for hit in hits if hit.offset == known_offset]
    crib_ok = 0
    english_ok = 0
    for hit in eligible:
        # Re-decrypt with the certified Vigenere function. Do not keep hit.plaintext.
        plain = vigenere_decrypt(K4_CIPHERTEXT, hit.key)
        if not cribs_in_place(plain):
            continue
        crib_ok += 1
        if english_pass(plain):
            english_ok += 1
    return MethodTally(
        method="vigenere-crib-slide",
        bound=(
            "search_vigenere_crib EASTNORTHEAST, periods 1 through 12, "
            "accept only offset 21"
        ),
        tried=1,
        decrypted=len(eligible),
        crib_consistent=crib_ok,
        english_pass=english_ok,
    )


def _tally_ngram() -> MethodTally:
    """Certified period search. The returned string is checked, then dropped."""
    found = solve_vigenere(K4_CIPHERTEXT, max_period=PERIOD_MAX)
    plain = found.plaintext
    crib_ok = 1 if cribs_in_place(plain) else 0
    english_ok = 1 if crib_ok and english_pass(plain) else 0
    return MethodTally(
        method="vigenere-ngram",
        bound="solve_vigenere max_period 12, one run",
        tried=1,
        decrypted=1,
        crib_consistent=crib_ok,
        english_pass=english_ok,
    )


def _tally_jobs(
    method: str,
    bound: str,
    jobs: tuple[Callable[[], str], ...],
) -> MethodTally:
    decrypted = 0
    crib_ok = 0
    english_ok = 0
    for job in jobs:
        try:
            plain = job()
        except ValueError:
            continue
        decrypted += 1
        if not cribs_in_place(plain):
            continue
        crib_ok += 1
        if english_pass(plain):
            english_ok += 1
    return MethodTally(method, bound, len(jobs), decrypted, crib_ok, english_ok)


def _columnar_jobs() -> tuple[Callable[[], str], ...]:
    jobs: list[Callable[[], str]] = []
    for width in range(COLUMNAR_WIDTH_MIN, COLUMNAR_WIDTH_MAX + 1):
        def single(width: int = width) -> str:
            return columnar_decrypt_right_to_left(K4_CIPHERTEXT, width)

        jobs.append(single)
    for width1 in range(COLUMNAR_WIDTH_MIN, COLUMNAR_WIDTH_MAX + 1):
        for width2 in range(COLUMNAR_WIDTH_MIN, COLUMNAR_WIDTH_MAX + 1):
            def double(width1: int = width1, width2: int = width2) -> str:
                return double_columnar_decrypt(K4_CIPHERTEXT, width1, width2)

            jobs.append(double)
    return tuple(jobs)


def _route_jobs() -> tuple[Callable[[], str], ...]:
    jobs: list[Callable[[], str]] = []
    for width in range(ROUTE_WIDTH_MIN, ROUTE_WIDTH_MAX + 1):
        for fill in ("rows", "cols"):
            key = f"width={width};fill={fill};route=spiral-cw-top-right"

            def run(key: str = key) -> str:
                return route_decrypt(K4_CIPHERTEXT, key)

            jobs.append(run)
    return tuple(jobs)


def search_k4() -> K4SearchReport:
    """Run the bounded attempt. Never returns a plaintext."""
    _check_inputs()
    tallies = (
        _tally_periodic(
            "vigenere",
            "periods 1 through 12",
            (vigenere_decrypt,),
        ),
        _tally_crib_slide(),
        _tally_ngram(),
        _tally_periodic(
            "beaufort",
            "periods 1 through 12",
            (beaufort_decrypt,),
        ),
        _tally_periodic(
            "keyed-alphabet",
            "KRYPTOS mixed alphabet, index A through Z, periods 1 through 12",
            _keyed_decryptors(),
        ),
        _tally_jobs(
            "columnar",
            "widths 2 through 12, single and double right-to-left columnar",
            _columnar_jobs(),
        ),
        _tally_jobs(
            "route",
            "widths 1 through 12, fill rows or cols, route spiral-cw-top-right",
            _route_jobs(),
        ),
    )
    solved = any(tally.english_pass > 0 for tally in tallies)
    digest = hashlib.sha256(K4_CIPHERTEXT.encode("ascii")).hexdigest()
    return K4SearchReport(
        result="not solved" if not solved else "criteria met",
        solved=solved,
        claimed_plaintext=None,
        tallies=tallies,
        ciphertext_sha256=digest,
    )
