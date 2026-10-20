"""Held-out prediction of the reserved folios against seeded permutation nulls.

Family 3 of the Voynich ledger asks whether the text predicts unseen folios
better than shuffled text. Ten whole folios were reserved statistics-blind
on 20 October 2026 (frozen list in the ledger); they appear in no previous
family measurement, and they appear here only as scored material, never as
training material.

Declared statistics, per file, on each file's own glyph identities:

- glyph statistic: total negative log-likelihood of the reserved folios'
  glyphs at word positions 2 onward, conditioned on the two preceding
  glyphs inside the same word, under a trigram model with add-one
  smoothing trained on the shared worded loci outside the reservation.
  Measures within-word glyph-order structure carried to unseen folios.
- token statistic: total negative log-likelihood of adjacent word pairs
  inside the reserved loci, under an add-one smoothed bigram model over
  word types trained the same way, with pairs scored inside loci only.
  Measures word-adjacency (line) structure carried to unseen folios.

Declared nulls, one per statistic, seeded:

- word-glyph null: each training word has its glyphs permuted inside the
  word, so every word keeps its exact length, the training glyph multiset
  is unchanged, and only order structure is destroyed. This isolates order
  structure from frequency.
- token null: the training token stream is permuted over all token slots
  of the training loci, so every locus keeps its token count and the
  training word multiset is unchanged, and only adjacency is destroyed.
  Locus glyph totals may shift in this null; that is stated here and
  accepted as the declared line-length null, because permuting glyphs
  inside kept words is the first null's job instead.

Replication budget and seeding: 1,000 seeded permutations per (file,
statistic) cell, at most 2,000 per test as planned, each replicate with
its own numpy default_rng seeded by the declared base seed, the cell, and
the replicate index. Every replicate is therefore reproducible in
isolation, and any prefix of a cell's null values is the prefix of a
longer run.

Scoring uses add-one smoothing over the union of training and reserved
glyphs (glyph statistic) or the union of training and reserved word types
(token statistic). The verdict rule, declared here: p is (one plus the
number of nulls at or below the real value) over (permutations plus one),
lower negative log-likelihood meaning better prediction; p at or below
0.01 verdicts `detected`, above 0.05 `not detected`, otherwise `marginal`.

Nothing here proposes a reading. Detection says that order structure built
on the seen folios transfers to the unseen reserved folios better than
shuffling the same material; nothing about language, cipher or meaning
follows from it. Undetection says no transferable order structure at the
measured order.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from engine import voynich_transcript_stats as base
from engine.voynich_compare import index_loci
from engine.voynich_ivtff import DATA_DIR, load

_word_glyphs = base._word_glyphs
_used_keys = base.used_keys

FILES = ("ZL", "GC", "IT")
BASE_SEED = 20261020
N_PERM = 1000
HEAD = 5  # null values stored per cell for reproducibility checks
CELL_ID = {"ZL": 0, "GC": 1, "IT": 2}
STAT_ID = {"glyph": 0, "token": 1}

ARTIFACT_PATH = (
    Path(DATA_DIR).resolve().parent.parent.parent
    / "docs" / "research-notes" / "voynich-heldout-prediction.json"
)


@dataclass
class CellData:
    """One file prepared once: key sets, encodings, and scored frames."""

    absent_shared_loci: int
    train_keys: tuple
    reserved_keys: tuple
    train_loci: tuple
    reserved_loci: tuple
    train_tokens: int
    reserved_tokens: int
    g_train_flat: np.ndarray
    g_train_lens: np.ndarray
    g_reserved_flat: np.ndarray
    g_reserved_lens: np.ndarray
    g_v: int
    t_ids: np.ndarray
    t_lens: np.ndarray
    t_a: np.ndarray
    t_b: np.ndarray
    r_a: np.ndarray
    r_b: np.ndarray
    v_types: int


_PREPARED: dict[str, CellData] = {}


def _reserved_folios():
    """The frozen reservation, delegated to the family 1 module."""
    return base.reserved_folios()


def _prepare(code: str) -> CellData:
    """Parse once per file; all encoding is derived from this snapshot.

    Tests patch load and index_loci in this module's namespace and clear
    _PREPARED before use.
    """
    if code in _PREPARED:
        return _PREPARED[code]
    index = index_loci(load(code))
    absent = 0
    train_keys = []
    for key in _used_keys():
        if key in index:
            train_keys.append(key)
        else:
            absent += 1
    reserved_set = set(_reserved_folios())
    reserved_keys = [
        key
        for folio, loci in base.shared_worded_keys().items()
        if folio in reserved_set
        for key in loci
        if key in index
    ]
    train_loci = tuple(tuple(index[key].words) for key in train_keys)
    reserved_loci = tuple(tuple(index[key].words) for key in reserved_keys)

    # Glyph side: one shared alphabet, per-word glyph runs in one array.
    normalized_train = [_word_glyphs(w) for w in _flat_words(train_loci)]
    normalized_reserved = [_word_glyphs(w) for w in _flat_words(reserved_loci)]
    glyphs = sorted(
        {c for w in normalized_train + normalized_reserved for c in w}
    )
    glyph_code = {char: position for position, char in enumerate(glyphs)}

    def _encode(normalized: list[str]) -> tuple[np.ndarray, np.ndarray]:
        flat = np.array(
            [glyph_code[c] for w in normalized for c in w], dtype=np.int64
        )
        lens = np.array([len(w) for w in normalized], dtype=np.int64)
        return flat, lens

    g_train_flat, g_train_lens = _encode(normalized_train)
    g_r_flat, g_r_lens = _encode(normalized_reserved)

    types = sorted(set(_flat_words(train_loci)) | set(_flat_words(reserved_loci)))
    type_index = {word: position for position, word in enumerate(types)}
    t_ids, t_lens, t_a, t_b = _encode_tokens(train_loci, type_index)
    _, _, r_a, r_b = _encode_tokens(reserved_loci, type_index)

    data = CellData(
        absent_shared_loci=absent,
        train_keys=tuple(train_keys),
        reserved_keys=tuple(reserved_keys),
        train_loci=train_loci,
        reserved_loci=reserved_loci,
        train_tokens=sum(len(locus) for locus in train_loci),
        reserved_tokens=sum(len(locus) for locus in reserved_loci),
        g_train_flat=g_train_flat,
        g_train_lens=g_train_lens,
        g_reserved_flat=g_r_flat,
        g_reserved_lens=g_r_lens,
        g_v=len(glyphs),
        t_ids=t_ids,
        t_lens=t_lens,
        t_a=t_a,
        t_b=t_b,
        r_a=r_a,
        r_b=r_b,
        v_types=len(types),
    )
    _PREPARED[code] = data
    return data


def _flat_words(loci) -> list[str]:
    return [word for locus in loci for word in locus]


def _starts(lens: np.ndarray) -> np.ndarray:
    if lens.size == 0:
        return np.zeros(0, dtype=np.int64)
    ends = np.cumsum(lens)
    return ends - lens


def _pairs(values: np.ndarray, lens: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """(a, b) values of every adjacent in-run pair."""
    starts = np.repeat(_starts(lens), lens)
    positions = np.arange(values.size) - starts
    mask = positions < np.repeat(lens - 1, lens)
    at = np.where(mask)[0]
    return values[at], values[at + 1]


def _triples(values: np.ndarray, lens: np.ndarray):
    """(a, b, c) values at every in-run position 1 onward."""
    starts = np.repeat(_starts(lens), lens)
    positions = np.arange(values.size) - starts
    mask = positions < np.repeat(lens - 2, lens)
    at = np.where(mask)[0]
    return values[at], values[at + 1], values[at + 2]


def _encode_tokens(loci, type_index: dict):
    """Token ids with locus run lengths and the scored adjacent pairs."""
    ids = np.array(
        [type_index[word] for locus in loci for word in locus], dtype=np.int64
    )
    lens = np.array([len(locus) for locus in loci], dtype=np.int64)
    a, b = _pairs(ids, lens)
    return ids, lens, a, b


def _glyph_model(flat: np.ndarray, lens: np.ndarray, v: int):
    """Add-one inputs: counts of every in-word adjacent glyph pair and of
    the triples in the same frame the scorer uses (position 1 onward)."""
    a, b = _pairs(flat, lens)
    pair_counts = np.bincount(a * v + b, minlength=v * v)
    ta, tb, tc = _triples(flat, lens)
    tri_counts = np.bincount(ta * v * v + tb * v + tc, minlength=v * v * v)
    return pair_counts, tri_counts


def _glyph_nll(pair_counts: np.ndarray, tri_counts: np.ndarray,
               a: np.ndarray, b: np.ndarray, c: np.ndarray, v: int) -> float:
    probability = (tri_counts[a * v * v + b * v + c] + 1.0) / (
        pair_counts[a * v + b] + v
    )
    return float(-np.log(probability).sum())


def _token_model(ids: np.ndarray, a: np.ndarray, b: np.ndarray, v: int):
    counts = np.bincount(ids, minlength=v)
    uniq, counts_ab = np.unique(a * v + b, return_counts=True)
    return counts, uniq, counts_ab


def _token_nll(model, a: np.ndarray, b: np.ndarray, v: int) -> float:
    counts, uniq, counts_ab = model
    query = a * v + b
    if uniq.size == 0:
        return float(-np.log(1.0 / v) * query.size)
    position = np.minimum(np.searchsorted(uniq, query), uniq.size - 1)
    pair_counts = np.where(uniq[position] == query, counts_ab[position], 0)
    probability = (pair_counts + 1.0) / (counts[a] + v)
    return float(-np.log(probability).sum())


def _shuffle_within_words(flat: np.ndarray, token_ids: np.ndarray,
                          rng: np.random.Generator) -> np.ndarray:
    """Permuted glyphs inside each word via one stable sort of random keys."""
    keys = rng.random(flat.size)
    order = np.lexsort((keys, token_ids))
    return flat[order]


def real_nlls(code: str) -> tuple[float, float]:
    """The two real statistics for one file over its held-out folios."""
    data = _prepare(code)
    pair_counts, tri_counts = _glyph_model(
        data.g_train_flat, data.g_train_lens, data.g_v
    )
    ra, rb, rc = _triples(data.g_reserved_flat, data.g_reserved_lens)
    glyph_nll = _glyph_nll(pair_counts, tri_counts, ra, rb, rc, data.g_v)
    model = _token_model(data.t_ids, data.t_a, data.t_b, data.v_types)
    token_nll = _token_nll(model, data.r_a, data.r_b, data.v_types)
    return glyph_nll, token_nll


def glyph_null_nll(code: str, index: int) -> float:
    """One declared word-glyph null replicate for one file."""
    data = _prepare(code)
    token_ids = np.repeat(np.arange(data.g_train_lens.size), data.g_train_lens)
    rng = np.random.default_rng(
        [BASE_SEED, CELL_ID[code], STAT_ID["glyph"], index]
    )
    shuffled = _shuffle_within_words(data.g_train_flat, token_ids, rng)
    pair_counts, tri_counts = _glyph_model(shuffled, data.g_train_lens, data.g_v)
    ra, rb, rc = _triples(data.g_reserved_flat, data.g_reserved_lens)
    return _glyph_nll(pair_counts, tri_counts, ra, rb, rc, data.g_v)


def token_null_nll(code: str, index: int) -> float:
    """One declared token-null replicate for one file."""
    data = _prepare(code)
    rng = np.random.default_rng(
        [BASE_SEED, CELL_ID[code], STAT_ID["token"], index]
    )
    shuffled = data.t_ids[rng.permutation(data.t_ids.size)]
    a, b = _pairs(shuffled, data.t_lens)
    model = _token_model(shuffled, a, b, data.v_types)
    return _token_nll(model, data.r_a, data.r_b, data.v_types)


def heldout_report(n_perm: int = N_PERM) -> dict:
    """The family 3 measurement: real statistics against declared nulls."""
    report = {"reserved_folios": _reserved_folios(), "n_perm": n_perm, "cells": {}}
    for code in FILES:
        data = _prepare(code)
        glyph_real, token_real = real_nlls(code)
        cell = {
            "absent_shared_loci": data.absent_shared_loci,
            "train_loci": len(data.train_keys),
            "reserved_loci": len(data.reserved_keys),
            "train_tokens": data.train_tokens,
            "reserved_tokens": data.reserved_tokens,
        }
        for statistic, real, null_fn in (
            ("glyph", glyph_real, glyph_null_nll),
            ("token", token_real, token_null_nll),
        ):
            values = [null_fn(code, i) for i in range(n_perm)]
            at_or_below = int(sum(value <= real for value in values))
            p_value = (1.0 + at_or_below) / (n_perm + 1.0)
            verdict = (
                "detected" if p_value <= 0.01
                else "not detected" if p_value > 0.05
                else "marginal"
            )
            cell[statistic] = {
                "real_nll": real,
                "null_min": min(values),
                "null_mean": float(np.mean(values)),
                "null_max": max(values),
                "nulls_at_or_below_real": at_or_below,
                "p_value": p_value,
                "verdict": verdict,
                "stored_null_head": values[:HEAD],
            }
        report["cells"][code] = cell
    return report


if __name__ == "__main__":
    report = heldout_report()
    ARTIFACT_PATH.write_text(json.dumps(report, indent=1, sort_keys=True) + "\n")
    print("wrote", ARTIFACT_PATH)
    for code, cell in sorted(report["cells"].items()):
        print(
            f"{code}: reserved {cell['reserved_loci']} loci "
            f"/ {cell['reserved_tokens']} tokens, absent {cell['absent_shared_loci']}"
        )
        for statistic in ("glyph", "token"):
            facts = cell[statistic]
            print(
                f"  {statistic}: real {facts['real_nll']:.1f} "
                f"nulls [{facts['null_min']:.1f}, {facts['null_max']:.1f}] "
                f"at_or_below {facts['nulls_at_or_below_real']} "
                f"p {facts['p_value']:.4f} {facts['verdict']}"
            )
