"""Word-segmentation range for the frozen Voynich transliterations.

Family 2 of the Voynich ledger asks whether the declared statistics survive
a change of word segmentation. The frozen parser follows the corpus
source's published convention: an uncertain space (a comma in the locus
body) joins two half words into one long word, matching the published word
counts. This module recomputes the declared statistics under two declared
segmentations of the same locus text:

- 'join': the baseline convention, delegated verbatim to the frozen parser,
  with a lock test asserting equality with every locus of all three files;
- 'split': the same normalisation chain, with every uncertain space treated
  as a definite separator.

Statistics run on the same worded loci shared by ZL and IT, outside the ten
reserved folios, in three files: ZL and IT (EVA family, word strings
comparable) and GC (v101 alphabet, included for its within-file
segmentation range only; its word strings are never compared to the other
two). IT carries no uncertain spaces in this transcript, so its two
policies must agree exactly, which makes IT the built-in zero-join control.

The result is the range of each statistic across segmentations: sign
frequencies must be invariant by construction (the glyph multiset of a
locus does not depend on where the tokens are cut), every higher n-gram
loses only the n-grams that used to cross an uncertain space, and the
token, type, length and word-frequency measures move by exactly the size
of the ambiguity. Nothing here is a reading of the manuscript, and no
conclusion about language or meaning follows.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from engine import voynich_transcript_stats
from engine.voynich_compare import index_loci
from engine.voynich_ivtff import DATA_DIR, _ALT_READING_RE, _resolve_reading, load

# The private counters and the rank metric are the frozen machinery of the
# family 1 measurement, reused so both families measure identical things;
# delegation and lock tests keep this use honest.
_counts = voynich_transcript_stats._counts
_length_facts = voynich_transcript_stats._length_facts
_reserved = voynich_transcript_stats.reserved_folios
_spearman = voynich_transcript_stats._spearman
_used_keys = voynich_transcript_stats.used_keys

STATS_PATH = (
    Path(DATA_DIR).resolve().parent.parent.parent
    / "docs" / "research-notes" / "voynich-segmentation-range.json"
)

_POLICIES = ("join", "split")
_FILES = ("ZL", "GC", "IT")
_EVA_FILES = ("ZL", "IT")
_ORDERS = (1, 2, 3, 4)


def join_words(raw: str) -> tuple[str, ...]:
    """The frozen parser's own words for one locus: zero drift by delegation."""
    from engine.voynich_ivtff import _split_text

    return _split_text(raw)[0]


def _normalised_work(raw: str) -> str:
    """The normalisation chain both policies share, mirroring the parser."""
    work = raw.replace("<->", ".").replace("<~>", ".")
    work = work.replace("<%>", "").replace("<$>", "")
    work = re.sub(r"<@[^>]*>", "", work)
    work = re.sub(r"<![^>]*>", "", work)
    return _ALT_READING_RE.sub(_resolve_reading, work)


def split_words(raw: str) -> tuple[str, ...]:
    """The same normalisation with every uncertain space cut as definite."""
    words: list[str] = []
    for token in re.split(r"[.]", _normalised_work(raw)):
        for half in token.split(","):
            half = half.replace("{", "").replace("}", "")
            if half:
                words.append(half)
    return tuple(words)


def locus_words(raw: str, policy: str) -> tuple[str, ...]:
    """Words for one locus under one declared segmentation policy."""
    if policy == "join":
        return join_words(raw)
    if policy == "split":
        return split_words(raw)
    raise ValueError(f"unknown policy: {policy!r}")


def file_counts(code: str, keys: list[tuple[str, int]], policy: str) -> dict:
    """Aggregate declared counts for one file over the keys, under policy.

    A file may lack a few of the shared ZL-IT keys entirely (GC does);
    absent loci are skipped and counted, so every policy sees the same
    loci for its file and the range stays within one and the same text.
    """
    index = index_loci(load(code))
    all_words: list[str] = []
    joins = 0
    absent = 0
    for key in keys:
        locus = index.get(key)
        if locus is None:
            absent += 1
            continue
        all_words.extend(locus_words(locus.raw, policy))
        joins += locus.uncertain_joins
    counts = _counts(all_words)
    counts["loci_absent"] = absent
    counts["glyphs"] = sum(counts["ngram"][1].values())
    counts["ngram_totals"] = {
        f"ngram{order}": sum(counts["ngram"][order].values())
        for order in _ORDERS if order > 1
    }
    counts["ngram_types"] = {
        f"ngram{order}": len(counts["ngram"][order])
        for order in _ORDERS if order > 1
    }
    counts["types"] = len(counts["words"])
    counts["token_ratio"] = round(counts["types"] / counts["tokens"], 6)
    counts["lengths"] = _length_facts(counts["lengths"])
    counts["uncertain_joins"] = joins
    return counts


def _glyph_counter_delta(counts_a: dict, counts_b: dict) -> int:
    """Total absolute difference of the sign frequency counters."""
    return sum(
        abs(count - counts_b["ngram"][1][glyph])
        for glyph, count in counts_a["ngram"][1].items()
    ) + sum(
        abs(counts_a["ngram"][1][glyph])
        for glyph in counts_b["ngram"][1]
        if glyph not in counts_a["ngram"][1]
    )


def segmentation_range() -> dict:
    """The family 2 measurement: statistics under both declared policies."""
    keys = _used_keys()
    per_policy: dict[str, dict[str, dict]] = {}
    for code in _FILES:
        per_policy[code] = {
            policy: file_counts(code, keys, policy) for policy in _POLICIES
        }

    facts = {}
    for code in _FILES:
        facts[code] = {}
        for policy in _POLICIES:
            counts = per_policy[code][policy]
            facts[code][policy] = {
                "glyphs": counts["glyphs"],
                "tokens": counts["tokens"],
                "types": counts["types"],
                "token_ratio": counts["token_ratio"],
                "mean_length": counts["lengths"]["mean_length"],
                "share_length_over_12": counts["lengths"]["share_length_over_12"],
                "length_shares": counts["lengths"]["shares"],
                "ngram_totals": counts["ngram_totals"],
                "ngram_types": counts["ngram_types"],
                "uncertain_joins": counts["uncertain_joins"],
                "loci_absent": counts["loci_absent"],
            }

    word_moves = {}
    for code in _FILES:
        joined = per_policy[code]["join"]["words"]
        split = per_policy[code]["split"]["words"]
        value, shared = _spearman(joined, split)
        word_moves[code] = {
            "word_frequency_rho_join_vs_split": value,
            "shared_word_types": shared,
            "token_delta": per_policy[code]["split"]["tokens"]
            - per_policy[code]["join"]["tokens"],
            "sign_frequency_delta": _glyph_counter_delta(
                per_policy[code]["join"], per_policy[code]["split"]
            ),
        }

    cross_file = {}
    for policy in _POLICIES:
        cross_file[policy] = {}
        for order in _ORDERS:
            name = f"ngram{order}" if order > 1 else "char1"
            value, shared = _spearman(
                per_policy["ZL"][policy]["ngram"][order],
                per_policy["IT"][policy]["ngram"][order],
            )
            cross_file[policy][name] = value
        value, shared = _spearman(
            per_policy["ZL"][policy]["words"], per_policy["IT"][policy]["words"]
        )
        cross_file[policy]["word1"] = value
        cross_file[policy]["shared_word_types"] = shared

    return {
        "reserved_folios": _reserved(),
        "used_loci": len(keys),
        "files": facts,
        "word_statistic_movement": word_moves,
        "cross_file_agreement": cross_file,
    }


if __name__ == "__main__":
    report = segmentation_range()
    STATS_PATH.write_text(json.dumps(report, indent=1, sort_keys=True) + "\n")
    print("wrote", STATS_PATH)
    for code in _FILES:
        facts = report["files"][code]
        movement = report["word_statistic_movement"][code]
        print(
            f"{code}: tokens join {facts['join']['tokens']} split "
            f"{facts['split']['tokens']} delta {movement['token_delta']} "
            f"joins {facts['join']['uncertain_joins']} "
            f"sign_delta {movement['sign_frequency_delta']} "
            f"word_rho {movement['word_frequency_rho_join_vs_split']:.4f}"
        )
    for policy in _POLICIES:
        print(f"cross-file {policy}:", {
            name: round(value, 4)
            for name, value in report["cross_file_agreement"][policy].items()
        })
