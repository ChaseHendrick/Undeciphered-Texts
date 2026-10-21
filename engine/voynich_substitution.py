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

Second declared measurement, the cross-text calibration, declared after
the first screen's indeterminate verdicts and before its own run: the
first screen's plant band is self-parity, text and model of the same
prose, so a genuine member of the class scored against a different prose
of its language sits below self-parity by an unmeasured penalty, which
plausibly covers the first screen's margins. The cross screen calibrates
that band with second reference proeses, English (Frankenstein, Project
Gutenberg ebook 84) and Latin (C. Iuli Caesaris De Bello Gallico, I-IV,
Project Gutenberg ebook 218), processed by the identical declared rules
and frozen in engine/data with sha256 provenance. Cross plants, 5 per
(file, language): the second text's processed stream encoded through a
seeded permutation and truncated to min(the file's stream length, the
second text's processed length), scored by the same machinery under the
first language's table. The cross plant is exactly what the class says
the real text could be: another prose of the language under substitution,
fairly scored. Floors are recomputed from their declared seeds and must
reproduce the first artifact's values. Verdict rule, declared here
before the cross run: real at or above the smallest cross plant is
`consistent-with-substitution`; real at or below the largest floor is
`not-consistent`; real strictly between is `below-cross-band`, which is
not membership-grade evidence and excludes the class only with the
population caveat that the band is five draws from two cross texts.
Margins to both bands are recorded whatever the verdict. Kind ids: cross
permutation 6, cross machinery 7.

Third declared measurement, the widened band, declared after the cross
screen's six below-cross-band verdicts and before its own run: the band
is widened from two cross texts per language to four (English) and five
(Latin) class members, adding declared second-wave references frozen in
engine/data with sha256 provenance, processed by the identical declared
rules. English adds Moby Dick (Herman Melville, Project Gutenberg ebook
2701) and Le Morte D'Arthur volume 1 (Thomas Malory, the 1485 Caxton
prose, the sampled population's period-appropriate member, ebook 1251).
Latin adds Vulgate Daniel (ebook 828, late-antique biblical prose),
Colloquium heptaplomeres (Jean Bodin, Renaissance philosophical dialogue,
ebook 17859), and De Rariorum Animalium atque Stirpium Historia
(early-modern natural-history Latin, ebook 27655). Every member of the
widened band, including the cross screen's own cross texts, is scored by
the identical machinery and counts; five seeded plants per cross text
per (file, language); plant length min(the file's stream length, the
text's processed length), recorded per plant. The cross screen's own
plant values recompute here from their declared seeds and the tests pin
them equal to the cross artifact. Seed kinds for the added texts:
widened permutation 10, widened machinery 11, one rng per (file,
language, text) drawing the five permutations, and one per (file,
language, text) drawing the five machinery runs in plant order, declared
here before the run. Verdict rule, declared before this run: real at or
above the smallest best in the widened band is
`consistent-with-substitution`; real at or below the largest floor is
`not-consistent`; real strictly between is `below-widened-band`. The
verdict keeps the declared interpretation limits: the band is sampled,
not exhaustive, and its threshold is the weakest member, which the log
reads out with the per-text margins.

Fourth declared measurement, the trigram resolution pass, declared
after the widened band's six below-widened-band verdicts and before
its own run: the identical declared streams, mapped set and greedy
swap search are re-scored at trigram resolution. The language model is
the declared add-one trigram model of the first reference prose per
language (the same frozen files as the first screen): P(third symbol |
first two) = (n(first, second, third) + 1) / (n(first, second) + 27),
built once from the reference's processed stream under the identical
declared processing. Counts: a counted trigram is three consecutive
counted positions of a stream; in the real streams the three events
must be pairwise originally adjacent, gaps excluded exactly as the
bigram counts exclude them, and the statistic is the best mean nats
per counted trigram. The search machinery is the identical greedy swap
hill-climb (one rank init plus 16 seeded restarts, sweep cap 200) over
the 27 x 27 x 27 count tensor. Power instruments at this resolution,
measured and never assumed: five seeded self-parity plants of the
reference prose, where a planted substitution must again reach the
reference's own clean identity score, recorded per language alongside
the plants; and five seeded multiset floors of the real stream. The
widened cross band recomputes at this resolution: five plants per
(file, language, text) for every declared cross text of the third
measurement, truncated to min(the file's stream length, the text's
processed length), scored under the first language's trigram table.
Seed kinds, declared before the run: trigram plant permutation 12 and
trigram plant machinery 13 with the plant index in the seed; trigram
floor permutation 14 and trigram floor machinery 15 with the floor
index; for the cross texts trigram cross permutation 16 and trigram
cross machinery 17 with the text position in the seed, one rng per
(file, language, text) drawing the five permutations and one running
the five machinery calls in plant order. The real statistic recomputes
from its declared seed kind 1, the same seed as the first screen; the
machinery's internal consumption differs by resolution, and the value
reproduces by replay. Verdict rule, declared before this run: real at
or above the smallest cross plant best is
`consistent-with-substitution`; real at or below the largest floor is
`not-consistent`; real strictly between is `below-trigram-band`. The
declared reading limits: the sampled population is the third
measurement's, abbreviated scribal usage stays outside the class, and
a real text below the widened band at trigram resolution as well as
bigram resolution makes the class exclusion declinable in its own
declared format; no tie-breaker with the bigram artifact is material
and none is claimed. Plant parity anchor, resolved before the run by a
design probe: the plants are truncated streams, so the anchor per
(file, language) cell is the truncated plant stream's own identity
score under the same declared model, recorded alongside the plants.

Fifth declared measurement, the noise-controlled trigram band, declared
after the trigram pass's split verdicts and its disclosed search
pathology, and before its own run: the identical streams, model and
search, re-measured with a raised restart budget as a declared
parameter of this measurement - 48 restarts (one rank init plus 47
seeded permutations), sweep cap unchanged at 200 - and a declared
per-text convergence criterion. The criterion, declared here: a cross
text enters the band of its cell only when its five plant draws agree
to within 0.0001 nats per trigram; a text whose draws disagree is
recorded with its recovered best and spread, does not set the band
threshold, and the disclosure names the runs. The real statistic is
re-measured under the same raised budget, so the real and the plants
work under one budget rule; the real's declared seed stays kind 1 and
the search trajectory recomputes by replay. Power instruments at this
budget: five self-parity plants per (file, language) with their
per-cell truncated anchors (the plant draws must re-converge to the
anchors; recorded and pinned), and five multiset floors per (file,
language) under the raised budget. Seed kinds, declared before the
run: controlled plant permutation 18, controlled plant machinery 19
(the plant index in the seed); controlled floor permutation 20,
controlled floor machinery 21 (the floor index); controlled cross
permutation 22, controlled cross machinery 23 (the text position in
the seed, same text order as the trigram pass, one rng per (file,
language, text) drawing the five permutations and one running the five
machinery calls in plant order). Verdict rule, declared before this
run: real at or above the smallest entered-band value is
`consistent-with-substitution`; real at or below the largest floor is
`not-consistent`; real strictly between is `below-controlled-band`;
special outcome declared in advance - if a language cell's entered
band is empty after the criterion, the cell's verdict is
`band-unresolvable-noise` and no exclusion derives from it. Declared
exclusion format, agreed here before the run: if the real text stands
below the smallest entered-band value in all six (file, language)
cells, then the scoped class - one-to-one substitution of a known
language, word divisions carried, no abbreviation, no transposition,
no nulls, the sampled population of seven proeses - is excluded by
count for the manuscript's statistics as measured, and the family
closes with that wording plus the standing caveats (abbreviated
scribal usage outside the class, population sampled not exhaustive,
nothing is a reading, no mapping published). If any cell flips
otherwise, the family stays open with the disclosure.
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
           "floor_perm": 4, "floor_mach": 5,
           "cross_perm": 6, "cross_mach": 7,
           "tri_plant_perm": 12, "tri_plant_mach": 13,
           "tri_floor_perm": 14, "tri_floor_mach": 15,
           "tri_cross_perm": 16, "tri_cross_mach": 17,
           "ctrl_plant_perm": 18, "ctrl_plant_mach": 19,
           "ctrl_floor_perm": 20, "ctrl_floor_mach": 21,
           "ctrl_cross_perm": 22, "ctrl_cross_mach": 23}

REFERENCE_FILES = {
    "english": ("substref_english_pg1342.txt", 1342),
    "latin": ("substref_latin_pg33849.txt", 33849),
}

CROSS_REFERENCE_FILES = {
    "english": ("substref_english2_pg84.txt", 84),
    "latin": ("substref_latin2_pg218.txt", 218),
}

# Widened-band additions: (file, ebook, label). This list is the declared
# sampled population of the third measurement.
WIDENED_REFERENCE_FILES = {
    "english": [
        ("substref_english3_pg2701.txt", 2701, "Moby Dick (Melville)"),
        ("substref_english4_pg1251.txt", 1251, "Le Morte D'Arthur vol 1 (Malory, 1485 Caxton)"),
    ],
    "latin": [
        ("substref_latin3_pg828.txt", 828, "Vulgata Daniel"),
        ("substref_latin4_pg17859.txt", 17859, "Colloquium heptaplomeres (Bodin)"),
        ("substref_latin5_pg27655.txt", 27655, "De Rariorum Animalium atque Stirpium Historia"),
    ],
}

WIDENED_SEED_KINDS = (10, 11)  # widened permutation, widened machinery

# The declared boundary mark: never a glyph character of any corpus.
BOUNDARY = "\x00"

ARTIFACT_PATH = (
    Path(DATA_DIR).resolve().parent.parent.parent
    / "docs" / "research-notes" / "voynich-substitution-screen.json"
)


# --------------------------------------------------------------------------
# Reference language models
# --------------------------------------------------------------------------


def _reference_text(
    language: str, cross: bool = False, file: str | None = None
) -> str:
    """A frozen source file's body between the Gutenberg markers.

    An explicit file name takes precedence over the language's default
    (the first reference, or the cross text when cross is True).
    """
    if file is not None:
        name = file
    else:
        files = CROSS_REFERENCE_FILES if cross else REFERENCE_FILES
        name, _ebook = files[language]
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


def _reference_stream(
    language: str, cross: bool = False, file: str | None = None
) -> list[int]:
    """The declared processed stream: letters 0 to 25, space 26."""
    body = _reference_text(language, cross, file=file)
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
# The trigram resolution, the fourth declared measurement
# --------------------------------------------------------------------------


_TRI_REFERENCE: dict[str, tuple[np.ndarray, float, list[int]]] = {}


def tri_table_from_stream(stream: list[int]) -> np.ndarray:
    """The declared add-one trigram table of one stream, flat.

    P(third | first, second) = (n(first, second, third) + 1)
    / (n(first, second) + 27); position (a, b, c) lives at
    (a * 27 + b) * 27 + c in the flattened log table. Shared by the
    frozen references and by the tests' synthetic streams, so the score
    family stays one formula at both resolutions.
    """
    ids = np.array(stream, dtype=np.int64)
    codes = (ids[:-2] * 27 + ids[1:-1]) * 27 + ids[2:]
    counts = np.zeros(27 ** 3)
    np.add.at(counts, codes, 1.0)
    context = counts.reshape(27, 27, 27).sum(axis=2)
    flat_context = np.repeat(context.reshape(-1), 27)
    return np.log((counts + 1.0) / (flat_context + 27.0))


def _tri_decompose(codes: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Split flat codes back into their three symbol digits."""
    first = codes // 729
    rest = codes % 729
    return first, rest // 27, rest % 27


def _tri_bincount(flats: list[np.ndarray]) -> tuple[np.ndarray, np.ndarray, float]:
    """Observed trigram codes, their counts, and the trigram total."""
    codes = (flats[0] * 27 + flats[1]) * 27 + flats[2]
    counted = np.bincount(codes, minlength=27 ** 3)
    observed = np.nonzero(counted)[0].astype(np.int64)
    weights = counted[observed].astype(np.float64)
    return observed, weights, float(counted.sum())


def _tri_observed_full(stream_ids: np.ndarray):
    """Counted trigrams of a full stream: every consecutive triple."""
    ids = np.asarray(stream_ids, dtype=np.int64)
    return _tri_bincount([ids[:-2], ids[1:-1], ids[2:]])


def _tri_observed_masked(events_ids: np.ndarray, mask: np.ndarray):
    """Counted trigrams of a gapped stream, gaps excluded exactly as the
    bigram counts exclude them: the three positions are pairwise
    originally adjacent."""
    kept = np.where(mask)[0]
    values = events_ids[kept]
    adjacent = kept[1:] == kept[:-1] + 1
    triple = adjacent[:-1] & adjacent[1:]
    return _tri_bincount(
        [values[:-2][triple], values[1:-1][triple], values[2:][triple]]
    )


def _tri_score(
    decomposed: tuple[np.ndarray, np.ndarray, np.ndarray],
    weights: np.ndarray,
    logp_flat: np.ndarray,
    sigma: list[int],
) -> float:
    """Sum of weighted log probabilities under one candidate mapping."""
    mapped = np.asarray(sigma, dtype=np.int64)
    first, second, third = decomposed
    joined = (mapped[first] * 27 + mapped[second]) * 27 + mapped[third]
    return float((weights * logp_flat[joined]).sum())


def _tri_climb(
    decomposed: tuple[np.ndarray, np.ndarray, np.ndarray],
    weights: np.ndarray,
    logp_flat: np.ndarray,
    sigma0: list[int],
) -> tuple[float, int]:
    """The identical greedy swap hill-climb at trigram resolution."""
    sigma = np.array(sigma0, dtype=np.int64)
    best = _tri_score(decomposed, weights, logp_flat, sigma)
    sweeps = 0
    improved = True
    while improved and sweeps < SWEEP_CAP:
        improved = False
        sweeps += 1
        for first in range(26):
            for second in range(first + 1, 27):
                sigma[first], sigma[second] = sigma[second], sigma[first]
                score = _tri_score(decomposed, weights, logp_flat, sigma)
                if score > best + 1e-12:
                    best = score
                    improved = True
                else:
                    sigma[first], sigma[second] = sigma[second], sigma[first]
    return best, sweeps


def machinery_best_tri(
    codes: np.ndarray,
    weights: np.ndarray,
    logp_flat: np.ndarray,
    total_counts: np.ndarray,
    rng: np.random.Generator,
    restarts: int = N_RESTARTS,
) -> float:
    """Best mean nats per counted trigram over the declared restarts.

    Restarts consume the generator deterministically and identically to
    the bigram machinery: restart 0 is the rank initialisation, builds
    on the trigram marginals, and consumes no generator draws; restarts
    1 onward are seeded permutations.
    """
    decomposed = _tri_decompose(codes)
    marginals = sum(
        np.bincount(part, minlength=27) for part in decomposed
    ).astype(np.float64)
    glyph_rank = np.argsort(-marginals, kind="stable")
    letter_rank = np.argsort(-total_counts, kind="stable")
    sigma = [0] * 27
    for glyph_position, letter_position in zip(glyph_rank, letter_rank):
        sigma[int(glyph_position)] = int(letter_position)
    best, _sweeps = _tri_climb(decomposed, weights, logp_flat, sigma)
    for _index in range(restarts - 1):
        start = list(rng.permutation(27))
        score, _sweeps = _tri_climb(decomposed, weights, logp_flat, start)
        best = max(best, score)
    return best / weights.sum()


def _reference_tri(language: str) -> tuple[np.ndarray, float, np.ndarray]:
    """The declared trigram model, the reference's own clean identity
    score per counted trigram (the plant parity anchor), and the
    letter counts, computed once."""
    if language in _TRI_REFERENCE:
        return _TRI_REFERENCE[language]
    stream = _reference_stream(language)
    logp_flat = tri_table_from_stream(stream)
    codes, weights, _total = _tri_observed_full(np.array(stream, dtype=np.int64))
    clean = _tri_score(
        _tri_decompose(codes), weights, logp_flat, list(range(27))
    ) / weights.sum()
    _table_bigram, letter_counts, _stream = _reference(language)
    _TRI_REFERENCE[language] = (logp_flat, round(float(clean), 4), letter_counts)
    return _TRI_REFERENCE[language]


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


def substitution_cross_screen() -> dict:
    """The declared cross-text calibration, all three files, both languages.

    Cross plants are built from the declared second reference proeses and
    scored under the first language's table, so the band is a sample of
    what the hypothesis class actually looks like with this machinery:
    another prose of the language under substitution, fairly scored.
    Floors recompute from their declared seeds and are checked against
    the first artifact's values by the tests.
    """
    artifact: dict = {
        "what": "The declared cross-text calibration of the substitution "
        "screen: cross plants from the declared second reference proeses "
        "(Frankenstein for English, Caesar's De Bello Gallico I-IV for "
        "Latin), each encoded through a seeded permutation of the mapped "
        "positions, truncated to min(the file's stream length, the second "
        "text's processed length), and scored by the same machinery under "
        "the first language's table. The declared verdict rule: real at or "
        "above the smallest cross plant is consistent-with-substitution; "
        "real at or below the largest floor is not-consistent; real "
        "strictly between is below-cross-band, which is not grade to "
        "exclude the class because the band is five draws from two cross "
        "texts. Floors recompute from their declared seeds.",
        "declared": {
            "base_seed": BASE_SEED,
            "cross_plants": N_PLANTS,
            "cross_floors": N_FLOORS,
            "cross_references": {},
        },
        "files": {},
    }
    for language in LANGS:
        name, ebook = CROSS_REFERENCE_FILES[language]
        path = Path(DATA_DIR).resolve().parent / name
        stream = _reference_stream(language, cross=True)
        share = float(
            np.bincount(np.array(stream, dtype=np.int64), minlength=27)[26]
        ) / len(stream)
        artifact["declared"]["cross_references"][language] = {
            "file": name,
            "ebook": ebook,
            "url": "https://www.gutenberg.org/cache/epub/"
                   f"{ebook}/pg{ebook}.txt",
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "processed_symbols": len(stream),
            "space_share": round(share, 4),
        }
    for code in FILES:
        stream = _real_stream(code)
        total = int(stream.total_events)
        scoped = np.full(total, -1, dtype=np.int64)
        scoped[stream.kept_mask] = stream.kept_ids
        real_matrix = _count_matrix(scoped, stream.kept_mask)
        cell: dict = {
            "plant_length_rule": "min(stream length, cross text length)",
        }
        for language in LANGS:
            table, counts, _primary = _reference(language)
            real_rng = np.random.default_rng(
                _seed(CELL_ID[code], KIND_ID["real"], LANG_ID[language], 0)
            )
            real_best = machinery_best(real_matrix, table, counts, real_rng)
            cross_stream = _reference_stream(language, cross=True)
            plant_length = min(total, len(cross_stream))
            cross_plants = []
            plant_lengths = []
            for index in range(N_PLANTS):
                rng_perm = np.random.default_rng(
                    _seed(CELL_ID[code], KIND_ID["cross_perm"],
                          LANG_ID[language], index)
                )
                permutation = list(rng_perm.permutation(27))
                plant = np.array(
                    [permutation[value]
                     for value in cross_stream[:plant_length]],
                    dtype=np.int64,
                )
                plant_lengths.append(plant_length)
                matrix = _full_matrix(plant)
                rng_mach = np.random.default_rng(
                    _seed(CELL_ID[code], KIND_ID["cross_mach"],
                          LANG_ID[language], index)
                )
                cross_plants.append(
                    round(machinery_best(matrix, table, counts, rng_mach), 4)
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
            plant_min = min(cross_plants)
            plant_max = max(cross_plants)
            floor_max = max(floors)
            if real_best >= plant_min:
                verdict = "consistent-with-substitution"
            elif real_best <= floor_max:
                verdict = "not-consistent"
            else:
                verdict = "below-cross-band"
            real_rounded = round(real_best, 4)
            cell[language] = {
                "real_best_mean_nats": real_rounded,
                "cross_plants_best_mean_nats": cross_plants,
                "plant_lengths": plant_lengths,
                "floors_best_mean_nats": floors,
                "plant_floor_gap": round(plant_min - floor_max, 4),
                "real_margin_to_floor_max": round(real_best - floor_max, 4),
                "real_margin_to_cross_min": round(real_best - plant_min, 4),
                "real_margin_to_cross_max": round(real_best - plant_max, 4),
                "verdict": verdict,
            }
        artifact["files"][code] = cell
    return artifact


CROSS_ARTIFACT_PATH = (
    Path(DATA_DIR).resolve().parent.parent.parent
    / "docs" / "research-notes" / "voynich-substitution-crossband.json"
)

WIDENED_ARTIFACT_PATH = (
    Path(DATA_DIR).resolve().parent.parent.parent
    / "docs" / "research-notes" / "voynich-substitution-widened.json"
)


def main_cross() -> None:
    artifact = substitution_cross_screen()
    CROSS_ARTIFACT_PATH.write_text(json.dumps(artifact, indent=2) + "\n")
    print(CROSS_ARTIFACT_PATH)


def _screen_facts(code: str, total: int, stream: FileStream, language: str):
    """Real best, floor values, and the floor matrix share for one cell."""
    table, counts, _stream = _reference(language)
    real_rng = np.random.default_rng(
        _seed(CELL_ID[code], KIND_ID["real"], LANG_ID[language], 0)
    )
    scoped = np.full(total, -1, dtype=np.int64)
    scoped[stream.kept_mask] = stream.kept_ids
    real_matrix = _count_matrix(scoped, stream.kept_mask)
    real_best = machinery_best(real_matrix, table, counts, real_rng)
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
            round(machinery_best(floor_matrix, table, counts, rng_mach), 4)
        )
    return real_best, floors


def _plants_for(
    code: str,
    language: str,
    reference_stream: list[int],
    table: np.ndarray,
    counts: np.ndarray,
    seed_kind_perm: int,
    seed_kind_mach: int,
    seed_index: int,
    legacy: bool,
) -> tuple[list[float], int]:
    """Five seeded plants of one cross text, scored by the machinery.

    legacy=True reproduces the cross screen's declared per-plant seeds:
    one rng per plant, kinds 6 and 7, the plant index in the seed, so the
    cross screen's own texts recompute exactly their cross-artifact
    values. legacy=False is the widened scheme declared in the module
    header: one rng drawing the five permutations, and one rng running
    the five machinery runs in plant order, both seeded with the text
    position (kinds 10 and 11). The plant length is min(the file's
    stream length, the text's processed length); the truncated tail is
    not scored.
    """
    total_stream = _real_stream(code)
    length = min(int(total_stream.total_events), len(reference_stream))
    plants: list[float] = []
    generators: list[tuple] = []
    if legacy:
        for index in range(5):
            generators.append((
                np.random.default_rng(
                    _seed(CELL_ID[code], seed_kind_perm,
                          LANG_ID[language], index)
                ),
                np.random.default_rng(
                    _seed(CELL_ID[code], seed_kind_mach,
                          LANG_ID[language], index)
                ),
            ))
    else:
        # Widened scheme: five permutations drawn sequentially from one
        # rng, five machinery runs sequentially from one rng.
        rng_perm = np.random.default_rng(
            _seed(CELL_ID[code], seed_kind_perm,
                  LANG_ID[language], seed_index)
        )
        rng_mach = np.random.default_rng(
            _seed(CELL_ID[code], seed_kind_mach,
                  LANG_ID[language], seed_index)
        )
        for _index in range(5):
            generators.append((rng_perm, rng_mach))
    for rng_perm, rng_mach in generators:
        permutation = list(rng_perm.permutation(27))
        plant = np.array(
            [permutation[value] for value in reference_stream[:length]],
            dtype=np.int64,
        )
        matrix = _full_matrix(plant)
        plants.append(
            round(machinery_best(matrix, table, counts, rng_mach), 4)
        )
    return plants, length


def substitution_widened_screen() -> dict:
    """The declared widened-band measurement, all three files, both languages.

    The band holds every declared cross text: the cross screen's two
    references (their plants recompute from the declared seeds and stay
    identical to the cross artifact) plus the widened additions. The
    verdict rule and interpretation limits are those declared in the
    module header before this run.
    """
    artifact: dict = {
        "what": "The declared widened substitution band: the hypothesis "
        "class's sampled members now number three proeses (English: Pride "
        "and Prejudice as model with Frankenstein, Moby Dick and Le Morte "
        "D'Arthur vol 1 as cross plants) and five proeses (Latin: "
        "Confessiones as model with Caesar's De Bello Gallico I-IV, "
        "Vulgate Daniel, Colloquium heptaplomeres, De Rariorum Animalium "
        "as cross plants), all scored by the identical machinery. The "
        "declared verdict rule: real at or above the smallest band best "
        "is consistent-with-substitution; real at or below the largest "
        "floor is not-consistent; strictly between is "
        "below-widened-band. The threshold is the weakest sampled "
        "member, and the per-text margins carry the interpretation. No "
        "mapping is published; nothing here is a reading.",
        "declared": {
            "base_seed": BASE_SEED,
            "plants_per_text": N_PLANTS,
            "floors": N_FLOORS,
            "seed_kinds": {"cross_screen": [6, 7], "widened": [10, 11]},
            "legacy_rule": (
                "The cross screen's own texts replay their declared "
                "per-plant seeds; their plants must equal the cross "
                "artifact's values exactly."
            ),
            "widened_scheme": (
                "For the added texts, one rng per (file, language, text) "
                "draws the five permutations, and one rng per (file, "
                "language, text) runs the five machinery calls in plant "
                "order."
            ),
            "verdict_rule": (
                "real at or above the smallest band best is "
                "consistent-with-substitution; real at or below the "
                "largest floor is not-consistent; strictly between is "
                "below-widened-band."
            ),
            "references": {},
        },
        "files": {},
    }
    for language in LANGS:
        entries = []
        name, ebook = CROSS_REFERENCE_FILES[language]
        entries.append((name, ebook, "cross screen text"))
        for name_w, ebook_w, label in WIDENED_REFERENCE_FILES[language]:
            entries.append((name_w, ebook_w, label))
        for name, ebook, label in entries:
            path = Path(DATA_DIR).resolve().parent / name
            stream = _reference_stream(language, file=name)
            share = float(
                np.bincount(np.array(stream, dtype=np.int64),
                            minlength=27)[26]
            ) / len(stream)
            artifact["declared"]["references"].setdefault(language, []).append({
                "file": name,
                "ebook": ebook,
                "label": label,
                "url": "https://www.gutenberg.org/cache/epub/"
                       f"{ebook}/pg{ebook}.txt",
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "processed_symbols": len(stream),
                "space_share": round(share, 4),
            })
    for code in FILES:
        stream = _real_stream(code)
        total = int(stream.total_events)
        cell: dict = {}
        for language in LANGS:
            real_best, floors = _screen_facts(code, total, stream, language)
            table, counts, _primary = _reference(language)
            entries: list[tuple[str, int, bool, int]] = []
            name, ebook = CROSS_REFERENCE_FILES[language]
            # The cross screen's own text: legacy per-plant seeds so its
            # values recompute exactly the cross artifact's numbers.
            entries.append((name, ebook, True, 0))
            for text_position, (name_w, ebook_w, _label) in enumerate(
                WIDENED_REFERENCE_FILES[language]
            ):
                entries.append((name_w, ebook_w, False, text_position))
            band = []
            for name, ebook, legacy_mode, seed_index in entries:
                text_stream = _reference_stream(language, file=name)
                plants, length = _plants_for(
                    code, language, text_stream, table, counts,
                    KIND_ID["cross_perm"] if legacy_mode
                    else WIDENED_SEED_KINDS[0],
                    KIND_ID["cross_mach"] if legacy_mode
                    else WIDENED_SEED_KINDS[1],
                    seed_index, legacy_mode,
                )
                band.append({
                    "file": name,
                    "ebook": ebook,
                    "plant_length": length,
                    "plants": plants,
                })
            plant_min = min(min(entry["plants"]) for entry in band)
            plant_max = max(max(entry["plants"]) for entry in band)
            floor_max = max(floors)
            if real_best >= plant_min:
                verdict = "consistent-with-substitution"
            elif real_best <= floor_max:
                verdict = "not-consistent"
            else:
                verdict = "below-widened-band"
            cell[language] = {
                "real_best_mean_nats": round(real_best, 4),
                "band": band,
                "floors_best_mean_nats": floors,
                "band_min": round(plant_min, 4),
                "band_max": round(plant_max, 4),
                "real_margin_to_floor_max": round(real_best - floor_max, 4),
                "real_margin_to_band_min": round(real_best - plant_min, 4),
                "real_margin_to_band_max": round(real_best - plant_max, 4),
                "verdict": verdict,
            }
        artifact["files"][code] = cell
    return artifact


def main_widened() -> None:
    artifact = substitution_widened_screen()
    WIDENED_ARTIFACT_PATH.write_text(json.dumps(artifact, indent=2) + "\n")
    print(WIDENED_ARTIFACT_PATH)


TRIGRAM_ARTIFACT_PATH = (
    Path(DATA_DIR).resolve().parent.parent.parent
    / "docs" / "research-notes" / "voynich-substitution-trigram.json"
)


def _tri_cell_facts(code: str, stream: FileStream, language: str):
    """Real trigram score, self-parity plants with their anchor, and
    floors for one cell."""
    logp_flat, clean, letter_counts = _reference_tri(language)
    total = int(stream.total_events)
    scoped = np.full(total, -1, dtype=np.int64)
    scoped[stream.kept_mask] = stream.kept_ids
    codes, weights, counted = _tri_observed_masked(scoped, stream.kept_mask)
    real_rng = np.random.default_rng(
        _seed(CELL_ID[code], KIND_ID["real"], LANG_ID[language], 0)
    )
    real_best = machinery_best_tri(
        codes, weights, logp_flat, letter_counts, real_rng
    )
    reference_stream = _reference_stream(language)
    truncation = np.array(reference_stream[:total], dtype=np.int64)
    target_codes, target_weights, _total = _tri_observed_full(truncation)
    anchor = round(
        _tri_score(_tri_decompose(target_codes), target_weights,
                   logp_flat, list(range(27))) / target_weights.sum(),
        4,
    )
    plants = []
    for index in range(5):
        rng_perm = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["tri_plant_perm"],
                  LANG_ID[language], index)
        )
        permutation = list(rng_perm.permutation(27))
        plant = np.array(
            [permutation[value] for value in truncation],
            dtype=np.int64,
        )
        plant_codes, plant_weights, _total = _tri_observed_full(plant)
        rng_mach = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["tri_plant_mach"],
                  LANG_ID[language], index)
        )
        plants.append(round(machinery_best_tri(
            plant_codes, plant_weights, logp_flat, letter_counts, rng_mach
        ), 4))
    floors = []
    for index in range(N_FLOORS):
        rng_perm = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["tri_floor_perm"],
                  LANG_ID[language], index)
        )
        values = stream.kept_ids.copy()
        rng_perm.shuffle(values)
        floor = np.full(total, -1, dtype=np.int64)
        floor[stream.kept_mask] = values
        floor_codes, floor_weights, _total = _tri_observed_masked(
            floor, stream.kept_mask
        )
        rng_mach = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["tri_floor_mach"],
                  LANG_ID[language], index)
        )
        floors.append(round(machinery_best_tri(
            floor_codes, floor_weights, logp_flat, letter_counts, rng_mach
        ), 4))
    return (
        round(real_best, 4), int(counted), anchor, plants, floors,
    )


def _tri_band_for(
    code: str,
    language: str,
    text_stream: list[int],
    logp_flat: np.ndarray,
    letter_counts: np.ndarray,
    seed_index: int,
) -> tuple[list[float], int]:
    """Five widened-band plants of one cross text at trigram resolution.

    The declared sequential scheme: one rng per (file, language, text)
    draws the five permutations, and one runs the five machinery calls
    in plant order; the plant length is min(the file's stream length,
    the text's processed length).
    """
    total = int(_real_stream(code).total_events)
    length = min(total, len(text_stream))
    rng_perm = np.random.default_rng(
        _seed(CELL_ID[code], KIND_ID["tri_cross_perm"],
              LANG_ID[language], seed_index)
    )
    rng_mach = np.random.default_rng(
        _seed(CELL_ID[code], KIND_ID["tri_cross_mach"],
              LANG_ID[language], seed_index)
    )
    plants = []
    for _index in range(5):
        permutation = list(rng_perm.permutation(27))
        plant = np.array(
            [permutation[value] for value in text_stream[:length]],
            dtype=np.int64,
        )
        codes, weights, _total = _tri_observed_full(plant)
        plants.append(
            round(machinery_best_tri(
                codes, weights, logp_flat, letter_counts, rng_mach
            ), 4)
        )
    return plants, length


def substitution_trigram_screen() -> dict:
    """The declared trigram resolution pass, all three files, both
    languages.

    The identical declared streams, mapped set and search machinery,
    re-scored under the declared add-one trigram model of the first
    reference prose. The widened cross band recomputes here with
    cross-text rngs declared for this run; the verdict rule and the
    reading limits are those declared in the module header before the
    run.
    """
    artifact: dict = {
        "what": "The declared trigram resolution pass: the substitution "
        "class as scoped, and the widened cross band of the third "
        "measurement, re-scored at trigram resolution under the add-one "
        "trigram model of the first reference prose per language. The "
        "declared verdict rule: real at or above the smallest cross "
        "plant best is consistent-with-substitution; real at or below "
        "the largest floor is not-consistent; strictly between is "
        "below-trigram-band. The recovered mappings are not recorded; "
        "nothing here is a reading.",
        "declared": {
            "base_seed": BASE_SEED,
            "plants_per_text": N_PLANTS,
            "floors": N_FLOORS,
            "seed_kinds": {
                "tri_plant": [KIND_ID["tri_plant_perm"],
                              KIND_ID["tri_plant_mach"]],
                "tri_floor": [KIND_ID["tri_floor_perm"],
                              KIND_ID["tri_floor_mach"]],
                "tri_cross": [KIND_ID["tri_cross_perm"],
                              KIND_ID["tri_cross_mach"]],
            },
            "smoothing_rule": "P(third | first, second) = (n(first, "
            "second, third) + 1) / (n(first, second) + 27), flat table "
            "position (a * 27 + b) * 27 + c",
            "cross_scheme": "one rng per (file, language, text) draws "
            "the five permutations, and one runs the five machinery "
            "calls in plant order, the text position in the seed",
            "verdict_rule": "real at or above the smallest cross plant "
            "best is consistent-with-substitution; real at or below the "
            "largest floor is not-consistent; strictly between is "
            "below-trigram-band",
            "models": {},
        },
        "files": {},
    }
    for language in LANGS:
        logp_flat, clean, _counts = _reference_tri(language)
        artifact["declared"]["models"][language] = {
            "file": REFERENCE_FILES[language][0],
            "ebook": REFERENCE_FILES[language][1],
            "clean_identity_mean_nats_per_trigram": clean,
        }
    for code in FILES:
        stream = _real_stream(code)
        cell: dict = {}
        for language in LANGS:
            logp_flat, clean, letter_counts = _reference_tri(language)
            real, counted, anchor, self_plants, floors = _tri_cell_facts(
                code, stream, language
            )
            band_texts: list[tuple[str, int, int]] = []
            name_c, ebook_c = CROSS_REFERENCE_FILES[language]
            band_texts.append((name_c, ebook_c, 0))
            for addition, (name_w, ebook_w, _label) in enumerate(
                WIDENED_REFERENCE_FILES[language]
            ):
                band_texts.append((name_w, ebook_w, addition + 1))
            band = []
            for name, ebook, seed_index in band_texts:
                text_stream = _reference_stream(language, file=name)
                plants, length = _tri_band_for(
                    code, language, text_stream, logp_flat,
                    letter_counts, seed_index,
                )
                band.append({
                    "file": name,
                    "ebook": ebook,
                    "plant_length": length,
                    "plants": plants,
                })
            plant_min = min(min(entry["plants"]) for entry in band)
            plant_max = max(max(entry["plants"]) for entry in band)
            floor_max = max(floors)
            if real >= plant_min:
                verdict = "consistent-with-substitution"
            elif real <= floor_max:
                verdict = "not-consistent"
            else:
                verdict = "below-trigram-band"
            cell[language] = {
                "real_best_mean_nats": real,
                "counted_trigrams": counted,
                "self_plants_best_mean_nats": self_plants,
                "plant_parity_anchor_mean_nats": anchor,
                "reference_clean_mean_nats": clean,
                "floors_best_mean_nats": floors,
                "band": band,
                "band_min": round(plant_min, 4),
                "band_max": round(plant_max, 4),
                "real_margin_to_floor_max": round(real - floor_max, 4),
                "real_margin_to_band_min": round(real - plant_min, 4),
                "real_margin_to_band_max": round(real - plant_max, 4),
                "verdict": verdict,
            }
        artifact["files"][code] = cell
    return artifact


def main_trigram() -> None:
    artifact = substitution_trigram_screen()
    TRIGRAM_ARTIFACT_PATH.write_text(json.dumps(artifact, indent=2) + "\n")
    print(TRIGRAM_ARTIFACT_PATH)


RESTARTS_CONTROL = 48  # the fifth declared measurement's restart budget

CONTROLLED_ARTIFACT_PATH = (
    Path(DATA_DIR).resolve().parent.parent.parent
    / "docs" / "research-notes" / "voynich-substitution-controlled.json"
)


def _tri_control_cell_facts(code: str, stream: FileStream, language: str):
    """Real, self-parity plants with anchor, and floors for one cell,
    all under the fifth measurement's declared 48-restart budget."""
    logp_flat, clean, letter_counts = _reference_tri(language)
    total = int(stream.total_events)
    scoped = np.full(total, -1, dtype=np.int64)
    scoped[stream.kept_mask] = stream.kept_ids
    codes, weights, counted = _tri_observed_masked(scoped, stream.kept_mask)
    real_rng = np.random.default_rng(
        _seed(CELL_ID[code], KIND_ID["real"], LANG_ID[language], 0)
    )
    real_best = machinery_best_tri(
        codes, weights, logp_flat, letter_counts, real_rng,
        restarts=RESTARTS_CONTROL,
    )
    reference_stream = _reference_stream(language)
    truncation = np.array(reference_stream[:total], dtype=np.int64)
    target_codes, target_weights, _total = _tri_observed_full(truncation)
    anchor = round(
        _tri_score(_tri_decompose(target_codes), target_weights,
                   logp_flat, list(range(27))) / target_weights.sum(),
        4,
    )
    plants = []
    for index in range(5):
        rng_perm = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["ctrl_plant_perm"],
                  LANG_ID[language], index)
        )
        permutation = list(rng_perm.permutation(27))
        plant = np.array(
            [permutation[value] for value in truncation],
            dtype=np.int64,
        )
        plant_codes, plant_weights, _total = _tri_observed_full(plant)
        rng_mach = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["ctrl_plant_mach"],
                  LANG_ID[language], index)
        )
        plants.append(round(machinery_best_tri(
            plant_codes, plant_weights, logp_flat, letter_counts, rng_mach,
            restarts=RESTARTS_CONTROL,
        ), 4))
    floors = []
    for index in range(N_FLOORS):
        rng_perm = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["ctrl_floor_perm"],
                  LANG_ID[language], index)
        )
        values = stream.kept_ids.copy()
        rng_perm.shuffle(values)
        floor = np.full(total, -1, dtype=np.int64)
        floor[stream.kept_mask] = values
        floor_codes, floor_weights, _total = _tri_observed_masked(
            floor, stream.kept_mask
        )
        rng_mach = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["ctrl_floor_mach"],
                  LANG_ID[language], index)
        )
        floors.append(round(machinery_best_tri(
            floor_codes, floor_weights, logp_flat, letter_counts, rng_mach,
            restarts=RESTARTS_CONTROL,
        ), 4))
    return (
        round(real_best, 4), int(counted), anchor, plants, floors,
    )


def _tri_control_band_for(
    code: str,
    language: str,
    text_stream: list[int],
    logp_flat: np.ndarray,
    letter_counts: np.ndarray,
    seed_index: int,
) -> list[float]:
    """Five controlled-band draws of one cross text at the 48-restart
    budget: the declared sequential scheme (one rng draws the five
    permutations, one runs the five machinery calls in plant order)."""
    total = int(_real_stream(code).total_events)
    length = min(total, len(text_stream))
    rng_perm = np.random.default_rng(
        _seed(CELL_ID[code], KIND_ID["ctrl_cross_perm"],
              LANG_ID[language], seed_index)
    )
    rng_mach = np.random.default_rng(
        _seed(CELL_ID[code], KIND_ID["ctrl_cross_mach"],
              LANG_ID[language], seed_index)
    )
    plants = []
    for _index in range(5):
        permutation = list(rng_perm.permutation(27))
        plant = np.array(
            [permutation[value] for value in text_stream[:length]],
            dtype=np.int64,
        )
        codes, weights, _total = _tri_observed_full(plant)
        plants.append(
            round(machinery_best_tri(
                codes, weights, logp_flat, letter_counts, rng_mach,
                restarts=RESTARTS_CONTROL,
            ), 4)
        )
    return plants


def substitution_control_screen() -> dict:
    """The declared noise-controlled trigram band, all three files,
    both languages, under the fifth measurement's 48-restart budget and
    the declared per-text convergence criterion."""
    artifact: dict = {
        "what": "The declared noise-controlled trigram band: identical "
        "streams, model and search as the trigram pass, re-measured "
        "under the declared 48-restart budget with the declared "
        "per-text convergence criterion (a cross text enters the band "
        "only when its five plant draws agree within 0.0001 nats per "
        "trigram; failing texts are recorded and do not set the "
        "threshold). The declared verdict rule: real at or above the "
        "smallest entered-band value is consistent-with-substitution; "
        "real at or below the largest floor is not-consistent; "
        "strictly between is below-controlled-band; an empty entered "
        "band is band-unresolvable-noise. No mapping is published; "
        "nothing here is a reading.",
        "declared": {
            "base_seed": BASE_SEED,
            "restarts": RESTARTS_CONTROL,
            "sweep_cap": SWEEP_CAP,
            "plants_per_text": N_PLANTS,
            "floors": N_FLOORS,
            "convergence_criterion": "max(plant draws) - min(plant "
            "draws) <= 0.0001 nats per trigram, all on identical data",
            "seed_kinds": {
                "ctrl_plant": [KIND_ID["ctrl_plant_perm"],
                               KIND_ID["ctrl_plant_mach"]],
                "ctrl_floor": [KIND_ID["ctrl_floor_perm"],
                               KIND_ID["ctrl_floor_mach"]],
                "ctrl_cross": [KIND_ID["ctrl_cross_perm"],
                               KIND_ID["ctrl_cross_mach"]],
            },
            "smoothing_rule": "P(third | first, second) = (n(first, "
            "second, third) + 1) / (n(first, second) + 27), flat table "
            "position (a * 27 + b) * 27 + c",
            "verdict_rule": "real at or above the smallest entered-band "
            "value is consistent-with-substitution; real at or below "
            "the largest floor is not-consistent; strictly between is "
            "below-controlled-band; empty entered band is "
            "band-unresolvable-noise",
            "exclusion_rule": "if the real text stands below the "
            "smallest entered-band value in all six cells, the scoped "
            "class is excluded by count for the measured statistics, "
            "with the standing caveats (abbreviated scribal usage "
            "outside the class, population sampled not exhaustive)",
            "models": {},
        },
        "files": {},
    }
    for language in LANGS:
        logp_flat, clean, _counts = _reference_tri(language)
        artifact["declared"]["models"][language] = {
            "file": REFERENCE_FILES[language][0],
            "ebook": REFERENCE_FILES[language][1],
            "clean_identity_mean_nats_per_trigram": clean,
            "restarts": RESTARTS_CONTROL,
        }
    for code in FILES:
        stream = _real_stream(code)
        cell: dict = {}
        for language in LANGS:
            logp_flat, clean, letter_counts = _reference_tri(language)
            real, counted, anchor, self_plants, floors = (
                _tri_control_cell_facts(code, stream, language)
            )
            band_texts: list[tuple[str, int, int]] = []
            name_c, ebook_c = CROSS_REFERENCE_FILES[language]
            band_texts.append((name_c, ebook_c, 0))
            for addition, (name_w, ebook_w, _label) in enumerate(
                WIDENED_REFERENCE_FILES[language]
            ):
                band_texts.append((name_w, ebook_w, addition + 1))
            band = []
            for name, ebook, seed_index in band_texts:
                text_stream = _reference_stream(language, file=name)
                plants = _tri_control_band_for(
                    code, language, text_stream, logp_flat,
                    letter_counts, seed_index,
                )
                spread = round(max(plants) - min(plants), 4)
                band.append({
                    "file": name,
                    "ebook": ebook,
                    "plant_length": min(
                        int(stream.total_events), len(text_stream)),
                    "plants": plants,
                    "recovered_best": max(plants),
                    "spread": spread,
                    "enters_band": bool(spread <= 0.0001),
                })
            entered = [entry["recovered_best"]
                       for entry in band if entry["enters_band"]]
            floor_max = max(floors)
            if entered:
                band_min = min(entered)
                band_max = max(entered)
                if real >= band_min:
                    verdict = "consistent-with-substitution"
                elif real <= floor_max:
                    verdict = "not-consistent"
                else:
                    verdict = "below-controlled-band"
            else:
                band_min = None
                band_max = None
                verdict = "band-unresolvable-noise"
            cell[language] = {
                "real_best_mean_nats": real,
                "counted_trigrams": counted,
                "self_plants_best_mean_nats": self_plants,
                "plant_parity_anchor_mean_nats": anchor,
                "floors_best_mean_nats": floors,
                "band": band,
                "band_min": band_min,
                "band_max": band_max,
                "verdict": verdict,
            }
        artifact["files"][code] = cell
    return artifact


def main_control() -> None:
    artifact = substitution_control_screen()
    CONTROLLED_ARTIFACT_PATH.write_text(json.dumps(artifact, indent=2) + "\n")
    print(CONTROLLED_ARTIFACT_PATH)


if __name__ == "__main__":
    main()
    main_cross()
    main_widened()
    main_trigram()
    main_control()
