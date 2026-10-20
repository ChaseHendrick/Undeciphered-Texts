"""The declared substitution screen for the Voynich transcriptions.

Family 4 of the Voynich ledger asks: is it a simple cipher of a known
language? This unit tests one declared hypothesis class, with its power
measured on synthetic controls before any real-text number is interpreted:

    one-to-one substitution of running text in a known natural language,
    with the text's word divisions carried through the cipher, where the
    plaintext alphabet's cipher symbols all lie inside the 26 most
    frequent glyph characters of the file's training text plus the
    word-boundary mark.

Hypothesis classes outside this declaration are not tested here; they are
listed in the ledger and log as the declared next directions. Nothing in
this module produces or proposes a reading.

Material: the shared worded loci outside the reserved folios (delegated to
the family 1 module). The ten reserved folios are excluded wholesale, the
conservative choice, although a screen of this shape has no holdout role
for them. Each file keeps its own transcription's glyph characters.

Declared machinery, identical for real and synthetic inputs:

- stream: every word's glyph characters (family 1's declared glyph form),
  with the word-boundary mark between every two adjacent words, whether
  they sit inside one locus or across a locus edge, so every word division
  the transcriptions record becomes a plaintext-space position under the
  carried-word-divisions hypothesis.
- mapped set: per file, the most frequent glyph characters by training
  count (ties broken by character order), up to 26, plus the boundary
  mark, which is appended after them as a mapped position. A file whose
  used-locus inventory has fewer than 26 distinct glyph characters maps
  its whole inventory (IT maps 23); rows and columns of its count matrix
  for absent positions stay at zero, and plants, which fill all 27
  positions, then carry three more symbols than IT's inventory holds.
  That asymmetry is recorded here as the declared inventory bound.
  Other glyph characters are declared outside the mapped set: their
  positions are gaps, and no bigram is counted across a gap, because
  under the hypothesis an unmapped glyph is a symbol whose letter never
  occurs anywhere in the scored stream.
- reference model: per language, a 27 by 27 bigram log-probability table
  with add-one smoothing, over the letters a to z (26 letters) and space
  (symbol 26), built from that language's declared reference prose after
  the declared processing below. Scores are natural-log nats.
- search: the mapping search is a greedy swap hill-climb over all ways to
  assign the 27 mapped positions to the 27 plaintext symbols, restarted
  from one frequency-rank initialisation and a declared number of seeded
  random restarts. The reported number is the best mean log-likelihood
  per counted pair. The recovered mappings are deliberately not recorded
  in the artifact: publishing an optimal relabelling of the real text
  would look like a reading, and this family produces exclusions, not
  readings.

Declared reference processing, for both languages: take the frozen source
file's body between the Project Gutenberg start and end markers, expand
the ligature letters aeDigraph oeDigraph into their letter pairs, case-
fold, reduce every non-letter to a space, collapse space runs, and count
bigrams over the letters and the space symbol.

Reference languages and sources, frozen in engine/data with the sha256 of
each file recorded in the artifact: English, Pride and Prejudice, Project
Gutenberg ebook 1342; Latin, Augustinus, Confessiones (S. Aurelii
Augustini Confessionum libri XIII), Project Gutenberg ebook 33849. One
prose source per language is a declared scope limit of this unit.

Power instruments, measured with the same machinery:

- plants (positive): 5 seeded plants per (file, language). The language's
  processed reference stream is encoded through a seeded permutation of
  the 27 mapped positions and truncated to the file's real stream length;
  a plant therefore has no gaps and its own count matrix. A substitution
  of that language must score at the level of the plant band if the
  machinery is to serve.
- floors (negative): 5 seeded floors per (file, language). The file's
  kept-position values are permuted over the kept slots, so the mapped
  multiset, the kept share, the boundary-symbol count, and the gap
  structure are exact while the adjacency structure is destroyed. A
  machinery that manufactures language structure from any stream would
  score the floors at plant level; instead they score far below.

Seeding: every cell draws from its own numpy default_rng seeded by the
declared base seed, the file, the kind, the language, and the replicate
index, so each number recomputes in isolation. Kind ids: real machinery 1
(replicate index 0), plant permutation 2, plant machinery 3, floor
permutation 4, floor machinery 5.

Verdict rule, declared before the run, applied per (file, language) on
the best mean log-likelihood per counted pair: real at or above the
smallest plant's best is `consistent-with-substitution`; real at or below
the largest floor's best is `not-consistent`; anything between is
`indeterminate`. The margins to both bands are recorded whatever the
verdict.
"""

from __future__ import annotations

import hashlib
import json
import unicodedata
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from engine import voynich_transcript_stats as base
from engine.voynich_compare import index_loci
from engine.voynich_ivtff import DATA_DIR, load

FILES = ("ZL", "GC", "IT")
CELL_ID = {"ZL": 0, "GC": 1, "IT": 2}
BASE_SEED = 20261020
MAPPED = 26  # letters a to z; mapped position 26 is the space symbol
N_RESTARTS = 16
SWEEP_CAP = 200
N_PLANTS = 5
N_FLOORS = 5
LANGS = ("english", "latin")
LANG_ID = {"english": 0, "latin": 1}
KIND_ID = {"real": 1, "plant_perm": 2, "plant_mach": 3,
           "floor_perm": 4, "floor_mach": 5}

REFERENCE_FILES = {
    "english": ("substref_english_pg1342.txt", 1342),
    "latin": ("substref_latin_pg33849.txt", 33849),
}

# The declared boundary mark: never a glyph character of any corpus.
BOUNDARY = "\x00"

ARTIFACT_PATH = (
    Path(DATA_DIR).resolve().parent.parent.parent
    / "docs" / "research-notes" / "voynich-substitution-screen.json"
)


# --------------------------------------------------------------------------
# Reference language models
# --------------------------------------------------------------------------


def _reference_text(language: str) -> str:
    """The frozen source file's body between the Gutenberg markers."""
    name, _ebook = REFERENCE_FILES[language]
    text = (Path(DATA_DIR).resolve().parent / name).read_text(
        encoding="utf-8", errors="replace"
    )
    start = text.find("START OF THE PROJECT GUTENBERG")
    end = text.find("END OF THE PROJECT GUTENBERG")
    body_start = start + len("START OF THE PROJECT GUTENBERG")
    return text[body_start:end]


_LIGATURES = {
    "æ": "ae", "Æ": "ae",
    "œ": "oe", "Œ": "oe",
}


def _reference_stream(language: str) -> list[int]:
    """The declared processed stream: letters 0 to 25, space 26."""
    body = _reference_text(language)
    body = "".join(_LIGATURES.get(char, char) for char in body)
    body = unicodedata.normalize("NFD", body).casefold()
    stream: list[int] = []
    at_space = True
    for char in body:
        if "a" <= char <= "z":
            stream.append(ord(char) - 97)
            at_space = False
        elif not at_space:
            stream.append(26)
            at_space = True
    return stream


_REFERENCE: dict[str, tuple[np.ndarray, np.ndarray, list[int]]] = {}


def table_from_stream(stream: list[int]) -> tuple[np.ndarray, np.ndarray]:
    """The declared add-one bigram table and letter counts of one stream.

    Letters 0 to 25, space 26. Shared by the frozen references and by the
    tests' synthetic languages, so the score family stays one formula.
    """
    counts = np.bincount(np.array(stream, dtype=np.int64), minlength=27)
    pairs = np.array(stream, dtype=np.int64)
    matrix = np.zeros((27, 27))
    np.add.at(matrix, (pairs[:-1], pairs[1:]), 1.0)
    total = matrix.sum()
    table = np.log((matrix + 1.0) / (total + 729.0))
    return table, counts


def _reference(language: str) -> tuple[np.ndarray, np.ndarray, list[int]]:
    """Bigram table, letter counts, and processed stream, computed once."""
    if language in _REFERENCE:
        return _REFERENCE[language]
    stream = _reference_stream(language)
    table, counts = table_from_stream(stream)
    _REFERENCE[language] = (table, counts, stream)
    return _REFERENCE[language]


# --------------------------------------------------------------------------
# Streams and count matrices
# --------------------------------------------------------------------------


@dataclass
class FileStream:
    """One file's declared stream: kept ids, gaps, and boundary facts."""

    mapped_chars: tuple[str, ...]  # 26 glyph characters, then BOUNDARY
    kept_ids: np.ndarray  # mapped ids over kept slots
    kept_mask: np.ndarray
    total_events: int
    word_count: int
    boundary_count: int


_REAL_STREAMS: dict[str, FileStream] = {}


def _real_stream(code: str) -> FileStream:
    """Parse once per file; tests patch load, index_loci and clear the cache."""
    if code in _REAL_STREAMS:
        return _REAL_STREAMS[code]
    index = index_loci(load(code))
    loci = [
        (key, tuple(index[key].words))
        for key in base.used_keys()
        if key in index and index[key].words
    ]
    counts: dict[str, int] = {}
    word_count = 0
    for _key, words in loci:
        for word in words:
            for char in base._word_glyphs(word):
                counts[char] = counts.get(char, 0) + 1
            word_count += 1
    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    mapped_chars = tuple(char for char, _count in ranked[:MAPPED]) + (BOUNDARY,)
    glyph_id = {char: position for position, char in enumerate(mapped_chars)}
    boundary_position = len(mapped_chars) - 1
    events: list[tuple[int, bool]] = []
    boundary_count = 0
    word_seen = 0
    for _key, words in loci:
        for word in words:
            if word_seen:
                events.append((boundary_position, True))
                boundary_count += 1
            word_seen += 1
            for char in base._word_glyphs(word):
                held = glyph_id.get(char)
                if held is None:
                    events.append((-1, False))
                    continue
                events.append((held, True))
    ids = np.array([value for value, _kept in events], dtype=np.int64)
    mask = np.array([kept for _value, kept in events], dtype=bool)
    stream = FileStream(
        mapped_chars=mapped_chars,
        kept_ids=ids[mask],
        kept_mask=mask,
        total_events=len(events),
        word_count=word_count,
        boundary_count=boundary_count,
    )
    _REAL_STREAMS[code] = stream
    return stream


def _count_matrix(events_ids: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Bigrams over originally adjacent positions where both sides mapped."""
    kept = np.where(mask)[0]
    values = events_ids[kept]
    adjacent = kept[1:] == kept[:-1] + 1
    first = values[:-1][adjacent]
    second = values[1:][adjacent]
    matrix = np.zeros((27, 27))
    np.add.at(matrix, (first, second), 1.0)
    return matrix


def _full_matrix(stream_ids: np.ndarray) -> np.ndarray:
    matrix = np.zeros((27, 27))
    np.add.at(matrix, (stream_ids[:-1], stream_ids[1:]), 1.0)
    return matrix


# --------------------------------------------------------------------------
# The mapping search
# --------------------------------------------------------------------------


def _score(matrix: np.ndarray, table: np.ndarray, sigma: np.ndarray) -> float:
    decoded = table[sigma][:, sigma]
    return float((matrix * decoded).sum())


def _climb(
    matrix: np.ndarray,
    table: np.ndarray,
    sigma0: list[int],
) -> tuple[float, int]:
    """Greedy swap hill-climb; returns the best score and the sweep count."""
    sigma = np.array(sigma0, dtype=np.int64)
    best = _score(matrix, table, sigma)
    sweeps = 0
    improved = True
    while improved and sweeps < SWEEP_CAP:
        improved = False
        sweeps += 1
        for first in range(26):
            for second in range(first + 1, 27):
                sigma[first], sigma[second] = sigma[second], sigma[first]
                score = _score(matrix, table, sigma)
                if score > best + 1e-12:
                    best = score
                    improved = True
                else:
                    sigma[first], sigma[second] = sigma[second], sigma[first]
    return best, sweeps


def _rank_init(matrix: np.ndarray, total_counts: np.ndarray) -> list[int]:
    """Frequency-rank initialisation: glyph rank to plaintext rank.

    Glyph ranks come from the stream matrix's row-plus-column totals;
    plaintext ranks come from the reference's letter counts. The boundary
    glyph is free to land wherever its two-side totals rank it, and the
    hill-climb can move it afterwards.
    """
    totals = matrix.sum(axis=1) + matrix.sum(axis=0)
    glyph_rank = np.argsort(-totals, kind="stable")
    letter_rank = np.argsort(-total_counts, kind="stable")
    sigma = [0] * 27
    for glyph_position, letter_position in zip(glyph_rank, letter_rank):
        sigma[int(glyph_position)] = int(letter_position)
    return sigma


def machinery_best(
    matrix: np.ndarray,
    table: np.ndarray,
    total_counts: np.ndarray,
    rng: np.random.Generator,
    restarts: int = N_RESTARTS,
) -> float:
    """Best mean nats per counted pair over the declared restarts.

    Restarts consume the generator deterministically: restart 0 is the
    rank initialisation, restarts 1 onward are seeded permutations.
    """
    best, _sweeps = _climb(matrix, table, _rank_init(matrix, total_counts))
    for _index in range(restarts - 1):
        start = list(rng.permutation(27))
        score, _sweeps = _climb(matrix, table, start)
        best = max(best, score)
    return best / matrix.sum()


def _seed(file_cell: int, kind: int, language: int, index: int) -> list[int]:
    return [BASE_SEED, file_cell, kind, language, index]


# --------------------------------------------------------------------------
# The screen
# --------------------------------------------------------------------------


def substitution_screen() -> dict:
    """The declared measurement, all three files by both references."""
    artifact: dict = {
        "what": "The declared substitution screen: family 4's hypothesis "
        "class is one-to-one substitution of a known language with carried "
        "word divisions, the alphabet's cipher symbols inside the 26 most "
        "frequent glyph characters plus the word-boundary mark, scored as "
        "the best mean bigram nats per counted pair under an add-one model "
        "of the declared reference language. Power instruments: seeded "
        "substitution plants of the same reference and seeded multiset "
        "floors of the same stream. The recovered mappings are not "
        "recorded; nothing here is a reading.",
        "declared": {
            "base_seed": BASE_SEED,
            "mapped_letters": MAPPED,
            "restarts": N_RESTARTS,
            "sweep_cap": SWEEP_CAP,
            "plants": N_PLANTS,
            "floors": N_FLOORS,
            "reserved_folios_excluded": True,
            "verdict_rule": "real >= min(plants): "
            "consistent-with-substitution; real <= max(floors): "
            "not-consistent; otherwise indeterminate.",
            "references": {},
        },
        "files": {},
    }
    for language in LANGS:
        name, ebook = REFERENCE_FILES[language]
        table, counts, stream = _reference(language)
        path = Path(DATA_DIR).resolve().parent / name
        artifact["declared"]["references"][language] = {
            "file": name,
            "ebook": ebook,
            "url": "https://www.gutenberg.org/cache/epub/"
                   f"{ebook}/pg{ebook}.txt",
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "processed_symbols": len(stream),
            "space_share": round(float(counts[26]) / len(stream), 4),
        }
    for code in FILES:
        stream = _real_stream(code)
        kept = int(stream.kept_ids.size)
        total = int(stream.total_events)
        scoped = np.full(total, -1, dtype=np.int64)
        scoped[stream.kept_mask] = stream.kept_ids
        real_matrix = _count_matrix(scoped, stream.kept_mask)
        cell: dict = {
            "mapped_chars": list(stream.mapped_chars),
            "stream": {
                "total_events": total,
                "kept_events": kept,
                "kept_share": round(kept / total, 4) if total else 0.0,
                "word_count": stream.word_count,
                "boundary_share": round(
                    stream.boundary_count / total, 4
                ) if total else 0.0,
            },
        }
        for language in LANGS:
            table, counts, _stream = _reference(language)
            real_rng = np.random.default_rng(
                _seed(CELL_ID[code], KIND_ID["real"], LANG_ID[language], 0)
            )
            real_best = machinery_best(real_matrix, table, counts, real_rng)
            plants = []
            for index in range(N_PLANTS):
                _table, _counts, reference = _reference(language)
                rng_perm = np.random.default_rng(
                    _seed(CELL_ID[code], KIND_ID["plant_perm"],
                          LANG_ID[language], index)
                )
                permutation = list(rng_perm.permutation(27))
                plant = np.array(
                    [permutation[value] for value in reference[:total]],
                    dtype=np.int64,
                )
                plant_matrix = _full_matrix(plant)
                rng_mach = np.random.default_rng(
                    _seed(CELL_ID[code], KIND_ID["plant_mach"],
                          LANG_ID[language], index)
                )
                plants.append(
                    round(machinery_best(
                        plant_matrix, table, counts, rng_mach
                    ), 4)
                )
            floors = []
            for index in range(N_FLOORS):
                rng_perm = np.random.default_rng(
                    _seed(CELL_ID[code], KIND_ID["floor_perm"],
                          LANG_ID[language], index)
                )
                values = stream.kept_ids.copy()
                rng_perm.shuffle(values)
                floor = np.full(total, -1, dtype=np.int64)
                floor[stream.kept_mask] = values
                floor_matrix = _count_matrix(floor, stream.kept_mask)
                rng_mach = np.random.default_rng(
                    _seed(CELL_ID[code], KIND_ID["floor_mach"],
                          LANG_ID[language], index)
                )
                floors.append(
                    round(machinery_best(
                        floor_matrix, table, counts, rng_mach
                    ), 4)
                )
            plant_min = min(plants)
            floor_max = max(floors)
            if real_best >= plant_min:
                verdict = "consistent-with-substitution"
            elif real_best <= floor_max:
                verdict = "not-consistent"
            else:
                verdict = "indeterminate"
            real_rounded = round(real_best, 4)
            cell[language] = {
                "real_best_mean_nats": real_rounded,
                "plants_best_mean_nats": plants,
                "floors_best_mean_nats": floors,
                "plant_floor_gap": round(plant_min - floor_max, 4),
                "real_margin_to_floor_max": round(real_best - floor_max, 4),
                "real_margin_to_plant_min": round(real_best - plant_min, 4),
                "verdict": verdict,
            }
        artifact["files"][code] = cell
    return artifact


def main() -> None:
    artifact = substitution_screen()
    ARTIFACT_PATH.write_text(json.dumps(artifact, indent=2) + "\n")
    print(ARTIFACT_PATH)


if __name__ == "__main__":
    main()
