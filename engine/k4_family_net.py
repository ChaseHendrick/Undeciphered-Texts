"""Cipher-family prior for Kryptos K4 from a small numpy network.

The question is narrow: which of a fixed list of generated cipher families
do K4's 97 letters statistically resemble? The answer is a prior for
choosing which searches to run first. It is not evidence for any key, any
method or any plaintext.

The repo's general nets (engine/solver_net.py, engine/neural_grade.py)
deliberately refuse K4 labels. This module is a separate, K4-specific tool.
It never reads K4 and never prints a K4 plaintext.

Generator. Each training ciphertext comes from a 97-letter plaintext window
with the two public clues planted at their zero-based positions,
EASTNORTHEAST at 21 and BERLINCLOCK at 63 (CRIB_SPANS in
engine/k4_gromark_obstruction.py). Windows come from
engine/data/neural_train_public.txt (English) and, when present, the German
Gutenberg texts in work/k4_running_key_texts/raw/ (letters only, umlauts
expanded). Train and validation windows come from the first 80 percent of
each corpus; test windows come from the last 20 percent with fresh seeds.
The "random" class is uniform random letters with no cipher. Every other
class encrypts the planted window with random keys. Repo encryptors are
used where they exist (engine/ciphers.py and engine/solvers/*); the local
encryptors here are ciphertext autokey, Hill 3x3 and the keyed columnar
transposition wrapper over engine.k4_transposition_sub.columnar_perm.

Features. Index of coincidence, periodic IC for periods 1..30, kappa at
shifts 1..30, the sorted letter frequency profile, chi-square to English,
digraph ICs, repeated trigrams and distinct letters (93 "statistics"
features), plus crib-key features: for Vigenere (k = c - p) and
Beaufort (k = c + p) on A-Z, the 24 key letters implied by the clues, their
IC and chi-square to English, the share of same-residue clue pairs whose
key letters agree for periods 1..30, the best progressive-key agreement for
periods 1..30, and ciphertext and plaintext autokey agreement at lags 1..30,
plus one alphabet-free block: for periods 1..30, the number of same-column
clue pairs that break a one-to-one substitution (322 crib features in all).

Model. A two-hidden-layer ReLU MLP with softmax, trained with Adam and
early stopping on a validation split, for several seeds; temperature
scaling on validation; expected calibration error on the test set. A second
"statistics only" model drops the crib-key features as a check on how much
the clues drive the posterior.

The posterior can only name one of the generated families. Ninety-seven
letters is short. A statistical resemblance is not a method.

This is not a K4 decipherment. solved stays false. claimed_plaintext stays None.
"""

from __future__ import annotations

import os

for _var in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_var, "1")

import argparse
import json
import random
import re
import time
from functools import lru_cache
from pathlib import Path

import numpy as np

from engine.ciphers import (
    substitution_decrypt,
    substitution_encrypt,
    vigenere_decrypt,
    vigenere_encrypt,
)
from engine.k4_gromark_obstruction import CRIB_SPANS
from engine.k4_transposition_sub import columnar_perm
from engine.language import UNIGRAM
from engine.solvers.autokey import autokey_decrypt, autokey_encrypt
from engine.solvers.beaufort import beaufort_decrypt, beaufort_encrypt
from engine.solvers.bifid import BIFID_ALPHABET, bifid_decrypt, bifid_encrypt
from engine.solvers.columnar import KRYPTOS_K3_CIPHERTEXT, KRYPTOS_K3_PLAINTEXT
from engine.solvers.gromark import gromark_decrypt, gromark_encrypt
from engine.solvers.hill import hill_decrypt, hill_encrypt
from engine.solvers.k4_attempt import K4_CIPHERTEXT
from engine.solvers.keyed_vigenere import keyed_vigenere_decrypt, keyed_vigenere_encrypt
from engine.solvers.progressive_key import progressive_key_decrypt, progressive_key_encrypt
from engine.solvers.running_key import running_key_decrypt, running_key_encrypt
from engine.solvers.trifid import TRIFID_ALPHABET, trifid_decrypt, trifid_encrypt

AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LENGTH = 97
MAX_LAG = 30
_ROOT = Path(__file__).resolve().parent
ENGLISH_PATH = _ROOT / "data" / "neural_train_public.txt"
GERMAN_DIR = _ROOT.parent / "work" / "k4_running_key_texts" / "raw"
GERMAN_FILES = ("pg22367.txt", "pg2229.txt")  # Kafka, Die Verwandlung; Goethe, Faust I
GERMAN_FALLBACK = _ROOT / "data" / "german_excerpt.txt"
GERMAN_SHARE = 0.2
TRAIN_FRACTION = 0.8

FAMILIES = (
    "random",
    "monoalphabetic",
    "periodic_p2_12",
    "periodic_p13_30",
    "keyed_vigenere",
    "autokey_plain",
    "autokey_cipher",
    "running_key",
    "progressive_key",
    "gromark",
    "hill_2x2",
    "hill_3x3",
    "bifid",
    "trifid",
    "columnar",
    "columnar_then_periodic",
    "periodic_then_columnar",
)

FAMILY_NOTES = {
    "random": "uniform random letters, no cipher, no clues planted",
    "monoalphabetic": "random simple substitution",
    "periodic_p2_12": "Vigenere or Beaufort on A-Z, random key, period 2 to 12",
    "periodic_p13_30": "Vigenere or Beaufort on A-Z, random key, period 13 to 30",
    "keyed_vigenere": "Kryptos-style keyed Vigenere: random mixed or keyword-mixed alphabet, period 2 to 15",
    "autokey_plain": "Vigenere plaintext autokey, primer 1 to 15 letters",
    "autokey_cipher": "Vigenere ciphertext autokey, primer 1 to 15 letters",
    "running_key": "Vigenere running key from another window of the same language",
    "progressive_key": "progressive key, keyword 1 to 12 letters, progression 1 to 25",
    "gromark": "Gromark, keyword 5 to 10 letters, random 5-digit primer",
    "hill_2x2": "Hill 2x2 on letters 1 to 96, letter 97 random",
    "hill_3x3": "Hill 3x3 on letters 1 to 96, letter 97 random",
    "bifid": "Bifid 5x5 (J folded to I), period 2 to 15 or whole text",
    "trifid": "Trifid 3x3x3, period 2 to 15 or whole text; the 27th symbol is shown as a duplicate letter",
    "columnar": "keyed columnar transposition only, width 2 to 20, either direction",
    "columnar_then_periodic": "columnar transposition, then Vigenere or Beaufort period 2 to 12",
    "periodic_then_columnar": "Vigenere or Beaufort period 2 to 12, then columnar transposition",
}

DEFAULTS = {
    "train_per_class": 8000,
    "val_per_class": 1000,
    "test_per_class": 1000,
    "seeds": (11, 23, 37, 41),
    "stats_seeds": (11, 23, 37),
    "hidden": (256, 128),
    "epochs": 40,
    "patience": 6,
    "batch": 256,
    "lr": 3e-4,
    "l2": 3e-3,
    "data_seed": 20261018,
    "test_seed": 97_000_001,
}
SANITY_RANDOM = 50
SANITY_RANDOM_SEED = 4_242_424
NOT_A_DECIPHERMENT = (
    "Prior over generated cipher families only. Not a K4 decipherment, not a key, "
    "not a method. solved is false and claimed_plaintext is None."
)


# ------------------------------------------------------------------ texts


def _letters(text: str) -> str:
    return re.sub("[^A-Z]", "", text.upper())


def german_letters(text: str) -> str:
    """Letters only, umlauts expanded (AE, OE, UE), sharp s as SS."""
    for src, dst in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("Ä", "AE"), ("Ö", "OE"),
                     ("Ü", "UE"), ("ß", "ss"), ("ẞ", "SS")):
        text = text.replace(src, dst)
    return _letters(text)


def _gutenberg_body(text: str) -> str:
    start = text.find("*** START OF")
    end = text.find("*** END OF")
    if start >= 0:
        start = text.find("\n", start) + 1
    else:
        start = 0
    return text[start:end if end > start else len(text)]


@lru_cache(maxsize=1)
def corpora() -> dict:
    """{'english': str, 'german': str, 'german_source': [...]} as A-Z letters."""
    english = _letters(ENGLISH_PATH.read_text(encoding="utf-8"))
    parts, sources = [], []
    for name in GERMAN_FILES:
        path = GERMAN_DIR / name
        if path.exists():
            parts.append(german_letters(_gutenberg_body(path.read_text(encoding="utf-8"))))
            sources.append(f"work/k4_running_key_texts/raw/{name}")
    if not parts:
        parts.append(german_letters(GERMAN_FALLBACK.read_text(encoding="utf-8")))
        sources.append("engine/data/german_excerpt.txt")
    return {"english": english, "german": "".join(parts), "german_source": sources}


def region(text: str, split: str) -> str:
    cut = int(len(text) * TRAIN_FRACTION)
    return text[:cut] if split == "train" else text[cut:]


def plant(window: str, spans=CRIB_SPANS) -> str:
    out = list(window)
    for start, word in spans:
        out[start:start + len(word)] = word
    return "".join(out)


# ------------------------------------------------------------ encryptors


def _rand_letters(rng: random.Random, n: int, alphabet: str = AZ) -> str:
    return "".join(rng.choice(alphabet) for _ in range(n))


def _perm(rng: random.Random, alphabet: str = AZ) -> str:
    cells = list(alphabet)
    rng.shuffle(cells)
    return "".join(cells)


def ciphertext_autokey_encrypt(plain: str, primer: str) -> str:
    """Vigenere ciphertext autokey: key is the primer, then the ciphertext itself."""
    out: list[int] = []
    for i, ch in enumerate(plain):
        k = ord(primer[i]) - 65 if i < len(primer) else out[i - len(primer)]
        out.append((ord(ch) - 65 + k) % 26)
    return "".join(AZ[v] for v in out)


def ciphertext_autokey_decrypt(cipher: str, primer: str) -> str:
    out = []
    for i, ch in enumerate(cipher):
        k = ord(primer[i]) if i < len(primer) else ord(cipher[i - len(primer)])
        out.append(AZ[(ord(ch) - k) % 26])
    return "".join(out)


def _det3(m) -> int:
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def hill3_inverse(m) -> list[list[int]]:
    det = _det3(m) % 26
    inv_det = pow(det, -1, 26)
    adj = [[0] * 3 for _ in range(3)]
    for r in range(3):
        for c in range(3):
            minor = [[m[i][j] for j in range(3) if j != c] for i in range(3) if i != r]
            cof = (-1) ** (r + c) * (minor[0][0] * minor[1][1] - minor[0][1] * minor[1][0])
            adj[c][r] = cof
    return [[(inv_det * adj[r][c]) % 26 for c in range(3)] for r in range(3)]


def random_hill3(rng: random.Random) -> list[list[int]]:
    while True:
        m = [[rng.randrange(26) for _ in range(3)] for _ in range(3)]
        det = _det3(m) % 26
        if det % 2 and det % 13:
            return m


def hill3_apply(text: str, m) -> str:
    """c = M p on column vectors of three letters. Length must be a multiple of 3."""
    if len(text) % 3:
        raise ValueError("Hill 3x3 text length must be a multiple of 3")
    out = []
    for i in range(0, len(text), 3):
        p = [ord(ch) - 65 for ch in text[i:i + 3]]
        out.extend(AZ[sum(m[r][c] * p[c] for c in range(3)) % 26] for r in range(3))
    return "".join(out)


def random_hill2_key(rng: random.Random) -> str:
    while True:
        a, b, c, d = (rng.randrange(26) for _ in range(4))
        det = (a * d - b * c) % 26
        if det % 2 and det % 13:
            return f"{a} {b} {c} {d}"


def columnar_encrypt(text: str, order, direction: int) -> str:
    """Keyed columnar transposition with an incomplete last row (columnar_perm)."""
    perm = columnar_perm(len(text), list(order), direction)
    out = [""] * len(text)
    for j, t in enumerate(perm):
        out[t] = text[j]
    return "".join(out)


def columnar_decrypt(text: str, order, direction: int) -> str:
    perm = columnar_perm(len(text), list(order), direction)
    return "".join(text[t] for t in perm)


def _random_order(rng: random.Random, lo: int = 2, hi: int = 20) -> tuple[list[int], int]:
    order = list(range(rng.randint(lo, hi)))
    rng.shuffle(order)
    return order, rng.randrange(2)


def _periodic(text: str, rng: random.Random, lo: int, hi: int) -> str:
    key = _rand_letters(rng, rng.randint(lo, hi))
    return vigenere_encrypt(text, key) if rng.random() < 0.5 else beaufort_encrypt(text, key)


def encrypt_family(family: str, plain: str, rng: random.Random, key_text: str) -> str:
    """Encrypt a 97-letter planted plaintext under `family` with random keys."""
    n = len(plain)
    if family == "random":
        return _rand_letters(rng, n)
    if family == "monoalphabetic":
        return substitution_encrypt(plain, _perm(rng))
    if family == "periodic_p2_12":
        return _periodic(plain, rng, 2, 12)
    if family == "periodic_p13_30":
        return _periodic(plain, rng, 13, 30)
    if family == "keyed_vigenere":
        if rng.random() < 0.5:
            alpha_kw = _perm(rng)
        else:
            alpha_kw = _rand_letters(rng, rng.randint(5, 10))
        key = _rand_letters(rng, rng.randint(2, 15))
        return keyed_vigenere_encrypt(plain, key, alpha_kw, rng.choice(AZ))
    if family == "autokey_plain":
        return autokey_encrypt(plain, _rand_letters(rng, rng.randint(1, 15)))
    if family == "autokey_cipher":
        return ciphertext_autokey_encrypt(plain, _rand_letters(rng, rng.randint(1, 15)))
    if family == "running_key":
        return running_key_encrypt(plain, key_text)
    if family == "progressive_key":
        return progressive_key_encrypt(plain, keyword=_rand_letters(rng, rng.randint(1, 12)),
                                       progression=rng.randint(1, 25))
    if family == "gromark":
        primer = "".join(str(rng.randrange(10)) for _ in range(5))
        if primer == "00000":
            primer = "00001"
        return gromark_encrypt(plain, f"{_rand_letters(rng, rng.randint(5, 10))} {primer}")
    if family == "hill_2x2":
        return hill_encrypt(plain[:96], random_hill2_key(rng)) + rng.choice(AZ)
    if family == "hill_3x3":
        return hill3_apply(plain[:96], random_hill3(rng)) + rng.choice(AZ)
    if family == "bifid":
        period = n if rng.random() < 0.2 else rng.randint(2, 15)
        return bifid_encrypt(plain, _perm(rng, BIFID_ALPHABET), period)
    if family == "trifid":
        period = n if rng.random() < 0.2 else rng.randint(2, 15)
        cipher = trifid_encrypt(plain, _perm(rng, TRIFID_ALPHABET), period)
        return cipher.replace(".", rng.choice(AZ))
    if family == "columnar":
        return columnar_encrypt(plain, *_random_order(rng))
    if family == "columnar_then_periodic":
        return _periodic(columnar_encrypt(plain, *_random_order(rng)), rng, 2, 12)
    if family == "periodic_then_columnar":
        return columnar_encrypt(_periodic(plain, rng, 2, 12), *_random_order(rng))
    raise ValueError(f"unknown family {family}")


def round_trip_checks(seed: int = 5) -> dict:
    """Encrypt then decrypt one planted window per encryptor; True means recovered."""
    rng = random.Random(seed)
    text = region(corpora()["english"], "train")
    start = rng.randrange(len(text) - 2 * LENGTH)
    plain = plant(text[start:start + LENGTH])
    other = text[start + LENGTH:start + 2 * LENGTH]
    checks = {}
    key = _rand_letters(rng, 7)
    checks["vigenere"] = vigenere_decrypt(vigenere_encrypt(plain, key), key) == plain
    checks["beaufort"] = beaufort_decrypt(beaufort_encrypt(plain, key), key) == plain
    mono = _perm(rng)
    checks["monoalphabetic"] = substitution_decrypt(substitution_encrypt(plain, mono), mono) == plain
    alpha = _perm(rng)
    checks["keyed_vigenere"] = keyed_vigenere_decrypt(
        keyed_vigenere_encrypt(plain, key, alpha, "Q"), key, alpha, "Q") == plain
    checks["autokey_plain"] = autokey_decrypt(autokey_encrypt(plain, key), key) == plain
    checks["autokey_cipher"] = ciphertext_autokey_decrypt(ciphertext_autokey_encrypt(plain, key), key) == plain
    checks["running_key"] = running_key_decrypt(running_key_encrypt(plain, other), other) == plain
    checks["progressive_key"] = progressive_key_decrypt(
        progressive_key_encrypt(plain, keyword=key, progression=3), keyword=key, progression=3) == plain
    checks["gromark"] = gromark_decrypt(gromark_encrypt(plain, "KRYPTOS 31415"), "KRYPTOS 31415") == plain
    h2 = random_hill2_key(rng)
    checks["hill_2x2"] = hill_decrypt(hill_encrypt(plain[:96], h2), h2) == plain[:96]
    h3 = random_hill3(rng)
    checks["hill_3x3"] = hill3_apply(hill3_apply(plain[:96], h3), hill3_inverse(h3)) == plain[:96]
    sq = _perm(rng, BIFID_ALPHABET)
    checks["bifid"] = bifid_decrypt(bifid_encrypt(plain, sq, 7), sq, 7) == plain.replace("J", "I")
    cube = _perm(rng, TRIFID_ALPHABET)
    checks["trifid"] = trifid_decrypt(trifid_encrypt(plain, cube, 5), cube, 5) == plain
    ok = True
    for width in (2, 7, 13, 20):
        for direction in (0, 1):
            order = list(range(width))
            rng.shuffle(order)
            ok &= columnar_decrypt(columnar_encrypt(plain, order, direction), order, direction) == plain
    checks["columnar"] = ok
    return checks


def sample_texts(per_class: int, seed: int, split: str, families=FAMILIES) -> tuple[list[str], np.ndarray]:
    """Planted, encrypted 97-letter texts, `per_class` per family, from `split` windows."""
    rng = random.Random(seed)
    corp = corpora()
    sources = {"english": region(corp["english"], split), "german": region(corp["german"], split)}
    texts, labels = [], []
    for label, family in enumerate(families):
        for _ in range(per_class):
            lang = "german" if rng.random() < GERMAN_SHARE else "english"
            src = sources[lang]
            a = rng.randrange(len(src) - LENGTH)
            b = rng.randrange(len(src) - LENGTH)
            while abs(a - b) < LENGTH:
                b = rng.randrange(len(src) - LENGTH)
            plain = plant(src[a:a + LENGTH])
            texts.append(encrypt_family(family, plain, rng, src[b:b + LENGTH]))
            labels.append(label)
    return texts, np.array(labels, dtype=np.int64)


# --------------------------------------------------------------- features

_ENG = np.array(UNIGRAM) / np.sum(UNIGRAM)
STAT_FEATURES = 1 + MAX_LAG + MAX_LAG + 26 + 1 + 3 + 1 + 1
CRIB_FEATURES_PER_TABLEAU = 24 + 2 + MAX_LAG * 4


def _ic_counts(counts: np.ndarray, n) -> np.ndarray:
    n = np.asarray(n, dtype=float)
    denom = np.where(n > 1, n * (n - 1), 1.0)
    return (counts * (counts - 1)).sum(-1) / denom


def _batch_counts(codes: np.ndarray, size: int) -> np.ndarray:
    rows = codes.shape[0]
    flat = (codes + size * np.arange(rows)[:, None]).ravel()
    return np.bincount(flat, minlength=rows * size).reshape(rows, size).astype(float)


def stat_features(X: np.ndarray) -> np.ndarray:
    N, n = X.shape
    cols = []
    counts = _batch_counts(X, 26)
    cols.append(_ic_counts(counts, n)[:, None])
    pic = np.zeros((N, MAX_LAG))
    for p in range(1, MAX_LAG + 1):
        lengths = np.array([len(range(r, n, p)) for r in range(p)])
        codes = (np.arange(n) % p)[None, :] * 26 + X
        c = _batch_counts(codes, p * 26).reshape(N, p, 26)
        pic[:, p - 1] = _ic_counts(c, lengths[None, :]).mean(1)
    cols.append(pic)
    cols.append(np.stack([(X[:, s:] == X[:, :-s]).mean(1) for s in range(1, MAX_LAG + 1)], 1))
    cols.append(-np.sort(-counts, 1) / n)
    expected = n * _ENG
    cols.append(np.log1p(((counts - expected) ** 2 / expected).sum(1))[:, None])
    dig = X[:, :-1] * 26 + X[:, 1:]
    cols.append(_ic_counts(_batch_counts(dig, 676), n - 1)[:, None] * 26)
    even = X[:, 0:96:2] * 26 + X[:, 1:96:2]
    odd = X[:, 1:97:2] * 26 + X[:, 2:97:2]
    cols.append(_ic_counts(_batch_counts(even, 676), even.shape[1])[:, None] * 26)
    cols.append(_ic_counts(_batch_counts(odd, 676), odd.shape[1])[:, None] * 26)
    tri = np.sort(X[:, :-2] * 676 + X[:, 1:-1] * 26 + X[:, 2:], 1)
    cols.append((tri[:, 1:] == tri[:, :-1]).sum(1, keepdims=True).astype(float))
    cols.append(((counts > 0).sum(1, keepdims=True)) / 26.0)
    out = np.concatenate(cols, 1)
    assert out.shape[1] == STAT_FEATURES
    return out


@lru_cache(maxsize=64)
def _crib_layout(positions: tuple[int, ...]) -> dict:
    P = np.array(positions)
    I, J = np.triu_indices(len(P), 1)
    gaps = P[J] - P[I]
    per_g = []
    for g in range(1, MAX_LAG + 1):
        sel = np.nonzero(gaps % g == 0)[0]
        per_g.append((sel, gaps[sel] // g))
    pt_pairs = []
    index = {p: i for i, p in enumerate(positions)}
    for L in range(1, MAX_LAG + 1):
        pairs = [(i, index[p - L]) for i, p in enumerate(positions) if p - L in index]
        pt_pairs.append(np.array(pairs, dtype=int).reshape(-1, 2))
    return {"P": P, "I": I, "J": J, "per_g": per_g, "pt_pairs": pt_pairs}


def crib_pairs(spans) -> tuple[tuple[int, ...], np.ndarray]:
    positions, letters = [], []
    for start, word in spans:
        for off, ch in enumerate(word):
            positions.append(start + off)
            letters.append(ord(ch) - 65)
    return tuple(positions), np.array(letters)


def crib_features(X: np.ndarray, spans=CRIB_SPANS) -> np.ndarray:
    positions, A = crib_pairs(spans)
    lay = _crib_layout(positions)
    P, I, J = lay["P"], lay["I"], lay["J"]
    N = X.shape[0]
    C = X[:, P]
    blocks = []
    d = np.arange(26)
    for sign in (-1, 1):  # Vigenere k = c - p, Beaufort k = c + p
        K = (C + sign * A[None, :]) % 26
        kc = _batch_counts(K, 26)
        expected = len(P) * _ENG
        feats = [K / 25.0, _ic_counts(kc, len(P))[:, None],
                 np.log1p(((kc - expected) ** 2 / expected).sum(1))[:, None]]
        diff = (K[:, J] - K[:, I]) % 26
        per = np.zeros((N, MAX_LAG))
        prog = np.zeros((N, MAX_LAG))
        for g, (sel, m) in enumerate(lay["per_g"]):
            if len(sel) == 0:
                continue
            dsel = diff[:, sel]
            per[:, g] = (dsel == 0).mean(1)
            target = (m[None, :] * d[:, None]) % 26  # (26, pairs)
            prog[:, g] = (dsel[:, None, :] == target[None, :, :]).mean(2).max(1)
        feats += [per, prog]
        ct = np.zeros((N, MAX_LAG))
        pt = np.zeros((N, MAX_LAG))
        for L in range(1, MAX_LAG + 1):
            ok = P - L >= 0
            if ok.any():
                ct[:, L - 1] = (K[:, ok] == X[:, P[ok] - L]).mean(1)
            pairs = lay["pt_pairs"][L - 1]
            if len(pairs):
                pt[:, L - 1] = (K[:, pairs[:, 0]] == A[pairs[:, 1]][None, :]).mean(1)
        feats += [ct, pt]
        blocks.append(np.concatenate(feats, 1))
    # Alphabet-free bijection test: in one column of period g, equal plaintext
    # letters must give equal ciphertext letters and unequal ones unequal.
    same_p = (A[J] == A[I])[None, :]
    same_c = C[:, J] == C[:, I]
    bad = (same_p != same_c)
    viol = np.zeros((N, MAX_LAG))
    for g, (sel, _m) in enumerate(lay["per_g"]):
        if len(sel):
            viol[:, g] = bad[:, sel].sum(1)
    blocks.append(np.log1p(viol))
    out = np.concatenate(blocks, 1)
    assert out.shape[1] == 2 * CRIB_FEATURES_PER_TABLEAU + MAX_LAG
    return out


def encode(texts) -> np.ndarray:
    return np.array([[ord(ch) - 65 for ch in t] for t in texts], dtype=np.int64)


def features(texts, spans=CRIB_SPANS, chunk: int = 2000) -> np.ndarray:
    """Raw (unstandardized) feature matrix: statistics then crib-key features."""
    for t in texts:
        if len(t) != LENGTH or not re.fullmatch("[A-Z]+", t):
            raise ValueError("each text must be 97 letters A-Z")
    X = encode(texts)
    parts = []
    for s in range(0, len(X), chunk):
        x = X[s:s + chunk]
        parts.append(np.concatenate([stat_features(x), crib_features(x, spans)], 1))
    return np.concatenate(parts, 0)


# ------------------------------------------------------------------ model


def _init(sizes, rng: np.random.Generator) -> list[np.ndarray]:
    params = []
    for a, b in zip(sizes[:-1], sizes[1:]):
        params += [rng.normal(0, np.sqrt(2.0 / a), (a, b)), np.zeros(b)]
    return params


def logits(params, X: np.ndarray) -> np.ndarray:
    h = X
    for i in range(0, len(params) - 2, 2):
        h = np.maximum(h @ params[i] + params[i + 1], 0.0)
    return h @ params[-2] + params[-1]


def softmax(z: np.ndarray) -> np.ndarray:
    z = z - z.max(1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(1, keepdims=True)


def nll(z: np.ndarray, y: np.ndarray) -> float:
    z = z - z.max(1, keepdims=True)
    lse = np.log(np.exp(z).sum(1))
    return float((lse - z[np.arange(len(y)), y]).mean())


def train_mlp(Xtr, ytr, Xva, yva, n_classes: int, seed: int, hidden=(128, 64), epochs=60,
              patience=6, batch=256, lr=1e-3, l2=1e-4) -> dict:
    """Adam on softmax cross entropy; keeps the best validation-loss weights."""
    rng = np.random.default_rng(seed)
    params = _init((Xtr.shape[1], *hidden, n_classes), rng)
    m = [np.zeros_like(p) for p in params]
    v = [np.zeros_like(p) for p in params]
    b1, b2, eps, step = 0.9, 0.999, 1e-8, 0
    best = (np.inf, [p.copy() for p in params], 0)
    history = []
    for epoch in range(epochs):
        order = rng.permutation(len(Xtr))
        for s in range(0, len(order), batch):
            idx = order[s:s + batch]
            xb, yb = Xtr[idx], ytr[idx]
            acts = [xb]
            h = xb
            for i in range(0, len(params) - 2, 2):
                h = np.maximum(h @ params[i] + params[i + 1], 0.0)
                acts.append(h)
            z = h @ params[-2] + params[-1]
            g = softmax(z)
            g[np.arange(len(yb)), yb] -= 1.0
            g /= len(yb)
            grads = [None] * len(params)
            for layer in range(len(params) // 2 - 1, -1, -1):
                W = params[2 * layer]
                grads[2 * layer] = acts[layer].T @ g + l2 * W
                grads[2 * layer + 1] = g.sum(0)
                if layer:
                    g = (g @ W.T) * (acts[layer] > 0)
            step += 1
            for i, gr in enumerate(grads):
                m[i] = b1 * m[i] + (1 - b1) * gr
                v[i] = b2 * v[i] + (1 - b2) * gr * gr
                mh = m[i] / (1 - b1 ** step)
                vh = v[i] / (1 - b2 ** step)
                params[i] -= lr * mh / (np.sqrt(vh) + eps)
        val_loss = nll(logits(params, Xva), yva)
        history.append(round(val_loss, 4))
        if val_loss < best[0] - 1e-4:
            best = (val_loss, [p.copy() for p in params], epoch + 1)
        elif epoch + 1 - best[2] >= patience:
            break
    return {"params": best[1], "val_loss": best[0], "best_epoch": best[2],
            "epochs_run": len(history), "history": history}


def fit_temperature(z: np.ndarray, y: np.ndarray) -> float:
    grid = np.exp(np.linspace(np.log(0.2), np.log(5.0), 121))
    losses = [nll(z / t, y) for t in grid]
    return float(grid[int(np.argmin(losses))])


def expected_calibration_error(prob: np.ndarray, y: np.ndarray, bins: int = 15) -> float:
    conf = prob.max(1)
    correct = prob.argmax(1) == y
    edges = np.linspace(0, 1, bins + 1)
    ece = 0.0
    for lo, hi in zip(edges[:-1], edges[1:]):
        sel = (conf > lo) & (conf <= hi)
        if sel.any():
            ece += sel.mean() * abs(conf[sel].mean() - correct[sel].mean())
    return float(ece)


class Ensemble:
    """Standardizer plus several temperature-scaled MLPs on a feature subset."""

    def __init__(self, mean, std, columns, members, families=FAMILIES):
        self.mean, self.std, self.columns = mean, std, columns
        self.members = members  # list of (params, temperature)
        self.families = tuple(families)

    def standardize(self, F: np.ndarray) -> np.ndarray:
        return (F[:, self.columns] - self.mean) / self.std

    def member_probs(self, F: np.ndarray) -> np.ndarray:
        Z = self.standardize(F)
        return np.stack([softmax(logits(p, Z) / t) for p, t in self.members])

    def probs(self, F: np.ndarray) -> np.ndarray:
        return self.member_probs(F).mean(0)


def fit_ensemble(Ftr, ytr, Fva, yva, columns, seeds, families=FAMILIES, **kw) -> tuple[Ensemble, list]:
    mean = Ftr[:, columns].mean(0)
    std = Ftr[:, columns].std(0)
    std = np.where(std < 1e-8, 1.0, std)
    Ztr = (Ftr[:, columns] - mean) / std
    Zva = (Fva[:, columns] - mean) / std
    members, logs = [], []
    for seed in seeds:
        t0 = time.time()
        fit = train_mlp(Ztr, ytr, Zva, yva, len(families), seed, **kw)
        zva = logits(fit["params"], Zva)
        temp = fit_temperature(zva, yva)
        members.append((fit["params"], temp))
        logs.append({"seed": seed, "best_epoch": fit["best_epoch"], "epochs_run": fit["epochs_run"],
                     "val_loss": round(fit["val_loss"], 4),
                     "val_accuracy": round(float((zva.argmax(1) == yva).mean()), 4),
                     "temperature": round(temp, 3), "seconds": round(time.time() - t0, 1)})
    return Ensemble(mean, std, columns, members, families), logs


def evaluate(ens: Ensemble, Fte, yte) -> dict:
    mp = ens.member_probs(Fte)
    Z = ens.standardize(Fte)
    raw = np.stack([softmax(logits(p, Z)) for p, _ in ens.members])
    prob = mp.mean(0)
    pred = prob.argmax(1)
    k = len(ens.families)
    conf = np.zeros((k, k), dtype=int)
    np.add.at(conf, (yte, pred), 1)
    per_class = {f: round(float(conf[i, i] / max(conf[i].sum(), 1)), 4) for i, f in enumerate(ens.families)}
    confusions = []
    for i in range(k):
        for j in range(k):
            if i != j and conf[i, j]:
                confusions.append((int(conf[i, j]), ens.families[i], ens.families[j]))
    confusions.sort(reverse=True)
    return {
        "ensemble_accuracy": round(float((pred == yte).mean()), 4),
        "member_accuracy": [round(float((m.argmax(1) == yte).mean()), 4) for m in mp],
        "per_class_recall": per_class,
        "confusion": conf.tolist(),
        "top_confusions": [{"true": t, "predicted": p, "count": c} for c, t, p in confusions[:12]],
        "ece_uncalibrated_members": [round(expected_calibration_error(r, yte), 4) for r in raw],
        "ece_calibrated_members": [round(expected_calibration_error(m, yte), 4) for m in mp],
        "ece_calibrated_ensemble": round(expected_calibration_error(prob, yte), 4),
        "test_nll_ensemble": round(float(-np.log(np.clip(prob[np.arange(len(yte)), yte], 1e-12, 1)).mean()), 4),
    }


def posterior(ens: Ensemble, text: str, spans=CRIB_SPANS) -> dict:
    mp = ens.member_probs(features([text], spans))[:, 0, :]
    mean, sd = mp.mean(0), mp.std(0)
    order = np.argsort(-mean)
    return {
        "argmax": ens.families[int(order[0])],
        "member_argmax": [ens.families[int(i)] for i in mp.argmax(1)],
        "posterior": {ens.families[int(i)]: {"mean": round(float(mean[i]), 4), "sd": round(float(sd[i]), 4),
                                             "min": round(float(mp[:, i].min()), 4),
                                             "max": round(float(mp[:, i].max()), 4)} for i in order},
    }


# ---------------------------------------------------------- sanity texts


def kryptos_sanity_texts() -> list[dict]:
    """Known Kryptos 97-letter windows with their own plaintext as the positional clue."""
    here = _ROOT / "data"
    k1 = json.loads((here / "kryptos_k1_certificate.json").read_text(encoding="utf-8"))
    k2 = json.loads((here / "kryptos_k2_certificate.json").read_text(encoding="utf-8"))
    k1c, k1p = _letters(k1["ciphertext"]), _letters(k1["plaintext"])
    k2c, k2p = _letters(k2["ciphertext"]), _letters(k2["plaintext"])
    k3c, k3p = KRYPTOS_K3_CIPHERTEXT, KRYPTOS_K3_PLAINTEXT
    items = []

    def add(name, family, cipher, plain, note):
        spans = ((21, plain[21:34]), (63, plain[63:74]))
        items.append({"name": name, "known_family": family, "cipher": cipher, "spans": spans, "note": note})

    add("K1+K2 sculpture window", "keyed_vigenere", k1c + k2c[:34], k1p + k2p[:34],
        "K1 is 63 letters, so the window is all of K1 then the first 34 letters of K2 (key change at 63)")
    for off in (0, 97, 194, len(k2c) - LENGTH):
        add(f"K2 letters {off}-{off + 96}", "keyed_vigenere", k2c[off:off + LENGTH], k2p[off:off + LENGTH],
            "K2 window, ABSCISSA on the KRYPTOS tableau")
    for off in (0, 97, 194, len(k3c) - LENGTH):
        add(f"K3 letters {off}-{off + 96}", "columnar", k3c[off:off + LENGTH], k3p[off:off + LENGTH],
            "K3 window; plaintext at the same positions is used as the positional clue")
    return items


# ------------------------------------------------------------------ report


def run(train_per_class=None, val_per_class=None, test_per_class=None, seeds=None, stats_seeds=None,
        hidden=None, epochs=None, patience=None, verbose=True, families=FAMILIES) -> dict:
    cfg = dict(DEFAULTS)
    for key, val in (("train_per_class", train_per_class), ("val_per_class", val_per_class),
                     ("test_per_class", test_per_class), ("seeds", seeds), ("stats_seeds", stats_seeds),
                     ("hidden", hidden), ("epochs", epochs), ("patience", patience)):
        if val is not None:
            cfg[key] = val
    say = print if verbose else (lambda *a, **k: None)
    timing = {}
    t0 = time.time()
    tr_texts, ytr = sample_texts(cfg["train_per_class"], cfg["data_seed"], "train", families)
    va_texts, yva = sample_texts(cfg["val_per_class"], cfg["data_seed"] + 1, "train", families)
    te_texts, yte = sample_texts(cfg["test_per_class"], cfg["test_seed"], "test", families)
    timing["generate_s"] = round(time.time() - t0, 1)
    t0 = time.time()
    Ftr, Fva, Fte = features(tr_texts), features(va_texts), features(te_texts)
    timing["features_s"] = round(time.time() - t0, 1)
    say(f"data: {len(ytr)} train, {len(yva)} val, {len(yte)} test, {Ftr.shape[1]} features "
        f"({timing['generate_s']}s gen, {timing['features_s']}s features)")
    kw = {k: cfg[k] for k in ("hidden", "epochs", "patience", "batch", "lr", "l2")}
    all_cols = np.arange(Ftr.shape[1])
    stat_cols = np.arange(STAT_FEATURES)
    t0 = time.time()
    full, full_logs = fit_ensemble(Ftr, ytr, Fva, yva, all_cols, cfg["seeds"], families, **kw)
    timing["train_full_s"] = round(time.time() - t0, 1)
    say(f"full model trained in {timing['train_full_s']}s: {full_logs}")
    t0 = time.time()
    stats, stats_logs = fit_ensemble(Ftr, ytr, Fva, yva, stat_cols, cfg["stats_seeds"], families, **kw)
    timing["train_stats_s"] = round(time.time() - t0, 1)
    say(f"statistics-only model trained in {timing['train_stats_s']}s")
    report = {
        "solved": False,
        "claimed_plaintext": None,
        "note": NOT_A_DECIPHERMENT,
        "families": list(families),
        "family_notes": {f: FAMILY_NOTES[f] for f in families},
        "config": {k: (list(v) if isinstance(v, tuple) else v) for k, v in cfg.items()},
        "data": {"train": int(len(ytr)), "val": int(len(yva)), "test": int(len(yte)),
                 "features_total": int(Ftr.shape[1]), "features_statistics": STAT_FEATURES,
                 "german_share": GERMAN_SHARE, "german_source": corpora()["german_source"],
                 "english_letters": len(corpora()["english"]), "german_letters": len(corpora()["german"])},
        "training": {"full": full_logs, "statistics_only": stats_logs},
        "test": {"full": evaluate(full, Fte, yte), "statistics_only": evaluate(stats, Fte, yte)},
    }
    k4 = {"full": posterior(full, K4_CIPHERTEXT), "statistics_only": posterior(stats, K4_CIPHERTEXT)}
    report["k4"] = {"ciphertext_length": len(K4_CIPHERTEXT), "spans": [list(s) for s in CRIB_SPANS],
                    "solved": False, "claimed_plaintext": None, **k4}
    rng = random.Random(SANITY_RANDOM_SEED)
    rand_texts = [_rand_letters(rng, LENGTH) for _ in range(SANITY_RANDOM)]
    Fr = features(rand_texts)
    sanity = {}
    for name, ens in (("full", full), ("statistics_only", stats)):
        pr = ens.probs(Fr)
        top = np.bincount(pr.argmax(1), minlength=len(families))
        sanity[name] = {
            "random_strings": SANITY_RANDOM,
            "argmax_counts": {families[i]: int(c) for i, c in enumerate(top) if c},
            "mean_posterior_random": round(float(pr[:, 0].mean()), 4),
        }
    kry = []
    for item in kryptos_sanity_texts():
        row = {"name": item["name"], "known_family": item["known_family"], "note": item["note"]}
        for name, ens in (("full", full), ("statistics_only", stats)):
            post = posterior(ens, item["cipher"], item["spans"])
            row[name] = {"argmax": post["argmax"],
                         "top3": {k: v["mean"] for k, v in list(post["posterior"].items())[:3]},
                         "p_known_family": post["posterior"][item["known_family"]]["mean"]}
        kry.append(row)
    sanity["kryptos"] = kry
    report["sanity"] = sanity
    report["timing"] = timing
    report["round_trips"] = round_trip_checks()
    return report


def _print(report: dict) -> None:
    print("solved:", report["solved"], "claimed_plaintext:", report["claimed_plaintext"])
    for name in ("full", "statistics_only"):
        t = report["test"][name]
        print(f"[{name}] test accuracy {t['ensemble_accuracy']} members {t['member_accuracy']} "
              f"ECE calibrated {t['ece_calibrated_ensemble']}")
        print("  top confusions:", [(c["true"], c["predicted"], c["count"]) for c in t["top_confusions"][:6]])
        post = report["k4"][name]["posterior"]
        print("  K4:", [(f, v["mean"], v["sd"]) for f, v in list(post.items())[:6]])
        print("  random:", report["sanity"][name])
    for row in report["sanity"]["kryptos"]:
        print(" ", row["name"], row["known_family"], "->", row["full"]["argmax"], row["full"]["p_known_family"],
              "| stats:", row["statistics_only"]["argmax"], row["statistics_only"]["p_known_family"])
    print("timing:", report["timing"])


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--quick", action="store_true", help="small run for a smoke check")
    ap.add_argument("--json", type=Path, help="write the full report here")
    args = ap.parse_args(argv)
    if args.quick:
        report = run(train_per_class=300, val_per_class=100, test_per_class=100, seeds=(1,), stats_seeds=(1,),
                     epochs=15)
    else:
        report = run()
    _print(report)
    if args.json:
        args.json.write_text(json.dumps(report, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
