"""Compare the frozen Voynich MS transliterations at the locus level.

The three frozen files (engine/data/voynich) are ZL 3b, GC 2a and IT 2a, all
IVTFF 2.0 from voynich.nu. ZL and IT are written in EVA-family alphabets and
can be compared word by word. GC is written in the v101 alphabet, which
splits glyphs differently than any EVA variant, so for pairs involving GC
only the structural facts are compared: which loci each file covers, and
whether word counts per locus agree.

For each pair the comparison reports:
- locus coverage by (folio, locus number): shared loci, and loci each file
  has alone;
- for shared loci, the loci whose word count agrees;
- for the same-alphabet pair, loci whose word tuples are identical, and an
  order-preserving word alignment that reports per shared locus what share of
  its words match in place, by folio and in overall bands, plus examples of
  the loci with the least agreement.

Uncertain readings resolve to their first option in both files, uncertain
spaces join words, and ligature braces are removed, all under the same frozen
counting convention as `engine.voynich_ivtff`. This module answers the
transcription-robustness question in its descriptive part only. Nothing here
proposes a reading of the manuscript.
"""

from __future__ import annotations

import json
import difflib
from collections import Counter
from pathlib import Path

from engine.voynich_ivtff import (
    DATA_DIR,
    IVTFFFile,
    Locus,
    load,
    statistics,
)

EVA_PAIRS = frozenset({("ZL", "IT"), ("IT", "ZL")})

REPORT_PATH = (
    Path(DATA_DIR).resolve().parent.parent.parent
    / "docs" / "research-notes" / "voynich-transcript-agreement.json"
)


def index_loci(file: IVTFFFile) -> dict[tuple[str, int], Locus]:
    """The loci of one file keyed by (folio, locus number)."""
    index: dict[tuple[str, int], Locus] = {}
    for locus in file.loci:
        index.setdefault((locus.folio, locus.num), locus)
    return index


def _same_alphabet_words(locus_a: Locus, locus_b: Locus) -> dict:
    """Word-level facts for two loci of the same alphabet."""
    words_a, words_b = locus_a.words, locus_b.words
    if words_a == words_b:
        return {"matched": len(words_a), "total": len(words_a)}
    matcher = difflib.SequenceMatcher(None, words_a, words_b, autojunk=False)
    matched = sum(size for _, _, size in matcher.get_matching_blocks())
    return {"matched": matched, "total": max(len(words_a), len(words_b))}


def pair_alignment(code_a: str, code_b: str) -> dict:
    """Align two frozen transcription files locus by locus."""
    file_a, file_b = load(code_a), load(code_b)
    index_a, index_b = index_loci(file_a), index_loci(file_b)
    keys_a, keys_b = set(index_a), set(index_b)
    shared = sorted(keys_a & keys_b, key=lambda key: (key[0], key[1]))
    only_a = sorted(keys_a - keys_b, key=lambda key: (key[0], key[1]))
    only_b = sorted(keys_b - keys_a, key=lambda key: (key[0], key[1]))
    same_alphabet = (code_a, code_b) in EVA_PAIRS

    folio_totals: Counter[str] = Counter()
    folio_matched: Counter[str] = Counter()
    band_counts: Counter[str] = Counter()
    worst: list[tuple[str, str, float, Locus, Locus]] = []
    word_count_equal = 0
    words_matched = 0
    words_total = 0

    for key in shared:
        locus_a, locus_b = index_a[key], index_b[key]
        if same_alphabet:
            facts = _same_alphabet_words(locus_a, locus_b)
            words_matched += facts["matched"]
            words_total += facts["total"]
            bands = facts["matched"] / facts["total"] if facts["total"] else 1.0
            folio_totals[key[0]] += facts["total"]
            folio_matched[key[0]] += facts["matched"]
            band = ("under-one-third" if bands < 1 / 3 else
                    "one-third-to-two-thirds" if bands < 2 / 3 else
                    "two-thirds-to-one" if bands < 1 else "identical")
            band_counts[band] += 1
            if bands < 1 / 3 and len(worst) < 12:
                worst.append((key[0], key[1], bands, locus_a, locus_b))
        if len(locus_a.words) == len(locus_b.words):
            word_count_equal += 1

    report: dict = {
        "same_alphabet": same_alphabet,
        "kind": "same-alphabet" if same_alphabet else "cross-alphabet",
        "loci_a": file_a.locus_count,
        "loci_b": file_b.locus_count,
        "shared_loci": len(shared),
        "only_a": len(only_a),
        "only_b": len(only_b),
        "only_a_by_folio": Counter(folio for folio, _ in only_a).most_common(12),
        "only_b_by_folio": Counter(folio for folio, _ in only_b).most_common(12),
        "shared_word_count_equal": word_count_equal,
        "shared_word_count_equal_share": (
            round(word_count_equal / len(shared), 6) if shared else None
        ),
    }
    if same_alphabet:
        loci_identical = band_counts["identical"]
        report.update({
            "loci_word_identical": loci_identical,
            "loci_word_identical_share": (
                round(loci_identical / len(shared), 6) if shared else None
            ),
            "words_total": words_total,
            "words_matched_in_place": words_matched,
            "words_matched_share": (
                round(words_matched / words_total, 6) if words_total else None
            ),
            "agreement_band_counts": dict(sorted(band_counts.items())),
            "worst_folio_rates": sorted(
                (
                    {
                        "folio": folio,
                        "shared_words": folio_totals[folio],
                        "matched_share": round(
                            folio_matched[folio] / folio_totals[folio], 6
                        ),
                    }
                    for folio in folio_totals
                    if folio_totals[folio] >= 30
                ),
                key=lambda row: row["matched_share"],
            )[:8],
            "examples_under_one_third_match": [
                {
                    "folio": folio,
                    "num": num,
                    "match": round(bands, 3),
                    "A": " ".join(locus_a.words)[:90],
                    "B": " ".join(locus_b.words)[:90],
                }
                for folio, num, bands, locus_a, locus_b in worst
            ],
        })
    else:
        report["loci_word_identical"] = None
        report["loci_word_identical_share"] = None
        report["note"] = (
            "Different transliteration alphabets (EVA-family versus v101), so "
            "word strings are not compared; the word-count agreement is given "
            "without string evidence."
        )
    report["stats_a"] = statistics(file_a)
    report["stats_b"] = statistics(file_b)
    return report


def disagreement_report(codes: tuple[str, ...] = ("ZL", "GC", "IT")) -> dict:
    """The full pair table over the frozen transcription files."""
    pairs: dict[str, dict] = {}
    for i, code_a in enumerate(codes):
        for code_b in codes[i + 1:]:
            pairs[f"{code_a}-{code_b}"] = pair_alignment(code_a, code_b)
    return {
        "method": {
            "convention": (
                "Words are the frozen-count long words: definite separators "
                "'.' '<->' '<~>'; commas, the uncertain spaces, join; "
                "uncertain readings resolve to their first option; ligature "
                "braces are removed; one '@nnn;' is one glyph."),
            "locus_key": "(folio, locus num)",
            "string_comparison": "allowed for ZL-IT only (both EVA-family)",
            "word_similarity": (
                "order-preserving difflib match over the words of one shared "
                "locus, for the same-alphabet pair"),
        },
        "files": {code: statistics(load(code)) for code in codes},
        "pairs": pairs,
    }


def headline(report: dict) -> str:
    """The one-line summary for the handoff."""
    zl_it = report["pairs"]["ZL-IT"]
    zl_gc = report["pairs"]["ZL-GC"]
    gc_it = report["pairs"]["GC-IT"]
    return (
        "ZL vs IT: shared loci "
        f"{zl_it['shared_loci']}, word tuples identical "
        f"{zl_it['loci_word_identical_share']}, words matched in place "
        f"{zl_it['words_matched_share']}; ZL vs GC: shared "
        f"{zl_gc['shared_loci']}, word counts equal "
        f"{zl_gc['shared_word_count_equal_share']}; GC vs IT: shared "
        f"{gc_it['shared_loci']}, word counts equal "
        f"{gc_it['shared_word_count_equal_share']}"
    )


if __name__ == "__main__":
    report = disagreement_report()
    REPORT_PATH.write_text(json.dumps(report, indent=1, sort_keys=True) + "\n")
    print("wrote", REPORT_PATH)
    for pair_code, pair in report["pairs"].items():
        zl_it = pair
        print(
            f"--- pair {pair_code} "
            f"({pair['stats_a']['alphabet_code']} vs "
            f"{pair['stats_b']['alphabet_code']}) ---"
        )
        print(
            f"loci {pair['loci_a']} vs {pair['loci_b']} | shared "
            f"{pair['shared_loci']} | only A {pair['only_a']} | only B "
            f"{pair['only_b']}"
        )
        print(
            f"shared loci with equal word count: {pair['shared_word_count_equal']} "
            f"({pair['shared_word_count_equal_share']})"
        )
        if "loci_word_identical" in pair:
            print("loci with identical word tuples: "
                  f"{pair['loci_word_identical']}")
            print("words matched in place: "
                  f"{pair['words_matched_in_place']} of {pair['words_total']} "
                  f"({pair['words_matched_share']})")
            print("agreement bands:", pair["agreement_band_counts"])
            print("worst folios by matched share:",
                  [(row["folio"], row["matched_share"])
                   for row in pair["worst_folio_rates"]])
    print(headline(report))
