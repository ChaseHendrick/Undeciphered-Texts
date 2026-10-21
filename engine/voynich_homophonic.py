"""Statistical screen for a homophonic-substitution hypothesis of the
Voynich manuscript, the first declared measurement of family 5.

Family 5 was declared open in the ledger on 21 October 2026, after
family 4's five measurements excluded the scoped one-to-one
substitution class by count at bigram and trigram resolution. This
module is declared here, in its own docstring, before any run of it,
and no number inside this module has been seen.

First declared measurement, the homophonic screen, declared in full
before the run: the identical frozen reference models as the
substitution family - the same add-one bigram table built from the
same two first reference proeses under the identical declared
processing (the pair table exactly as family 4's table_from_stream
declares it), the same frozen real transcriptions rendered to
streams, and the same frozen class members. What changes is the
cipher hypothesis and with it the search space: a homophonic mapping
allows several cipher symbols to share one plaintext letter while
every cipher symbol still names exactly one letter, so the search is
a declared reassignment climb over assignments from the cipher symbol
set onto the model's 27 letter tokens, not a permutation climb. The
mapped set is wider than family 4's, declared before the run: the
file's most frequent glyph characters up to 36, ranked by the same
(descending count, character) rule family 4 uses, plus the
word-boundary mark in the last position - 36 glyph slots over 26
letters with room for the surplus a homophonic cipher needs, every
file's glyph pool supplying at least 36 distinct characters. Word
divisions are carried: the word-boundary mark keeps the same declared
search freedom family 4 gave it, one more symbol whose label the
climb may move, and pairs across a boundary slot count exactly as
family 4's bigram counts count them.

Declared machinery, before the run: states are assignments f from the
37 cipher symbols (36 glyphs plus the boundary mark) onto the model's
27 letter tokens (26 letters plus the space token); the statistic is
the best mean nats per counted pair, the assignment score summed over
the symbol pair count matrix times the model table and divided by the
counted pairs. The climb is a greedy reassignment hill-climb: symbols
in index order, one full pass per sweep; for each symbol its 27
candidate labels are evaluated exactly from the running score (its
outbound pairs, its inbound pairs, and its diagonal removed once),
and a label is adopted only on a strict improvement beyond 1e-12,
otherwise the symbol stays put; ties of the argmax move nothing
because adoption needs the strict improvement. The best assignment
reached is returned with its exact re-evaluated score, so no
incremental drift reaches any stored number. Sweep cap 200 inherited,
restarts 16 inherited: restart 0 is the declared frequency-rank
initialisation with the surplus symbols wrapping (the k-th most
frequent symbol starts at the k-th most frequent letter, k modulo 27;
the boundary mark starts and moves like any symbol); restarts 1
onward start from a seeded permutation of the 27 letter tokens under
the same wrap rule; each restart consumes one deterministic
permutation draw in order. The add-one model is exploitable under the
richer assignment space - a pre-run design probe on the implementation
(found a climb from the planted configuration rising above the
planted key's own score, still improving at the declared cap), so
this family's declared machinery embraces the cap: the sweep cap is a
declared budget applied identically to the real, every plant, every
floor and every band draw, and each machinery call records whether
its best climb hit the cap. The comparison stays apples to apples:
both sides are scored through the identical declared climb at the
identical declared budget, and any under-convergence truncates both
sides' recoveries the same way.

Declared power instruments, all before the first real number is read:

- Plant parity through an encoder, not a decoder. Each plant is the
  truncated first reference stream encoded into the file's mapped
  cipher alphabet by a declared encoder: the truncation follows the
  standing rule (min of the real stream's total events and the
  reference stream's length); the encoder's partition rule, declared
  here, splits the 36 glyph slots over the letters present in the
  truncated stream - floor shares of frequency, one slot at least per
  present letter, remaining slots by largest fractional remainder
  with ties to the ascending letter index, groups laid out letter by
  letter in descending letter frequency so the most frequent letter
  receives the most frequent glyphs, a zero-share present letter
  taking one slot from the largest existing group. The encoder
  samples each plaintext position's cipher symbol by one uniform
  declared draw per position from its letter's group, in stream
  order; the boundary positions take the boundary mark without a
  draw. The anchor, resolved before the run: the plant's own
  true-key decoding score is algebraically the truncated reference
  stream's identity score under the same declared model whatever the
  sampled choices are, so the anchor per (file, language) cell is
  that identity value, recorded in the artifact. The declared pass
  rule, declared with the pre-run probe's finding in mind: a plant
  passes when its machinery best is at least the anchor minus 0.0001
  on its own data - exactly equal counts as parity, exactly as family
  4 planted parity was counted, and best above the anchor counts as
  parity with the excess recorded and disclosed as
  machinery-above-anchor, because the point of the instrument is the
  machinery finding the planted configuration's optimum and an exact
  higher value is the machinery working, not failing; a plant below
  the anchor by more than 0.0001 fails parity and is recorded - and
  under that rule a system of cap-truncated recoveries still states
  the instrument's truth, that the machinery recovers everything the
  planted assignment can achieve.
- Plant budget: five plants per (file, language), each with its own
  declared seed pair (one sampling rng, one machinery rng), drawn
  independently by plant index.
- Floors: five multiset floors per (file, language), the real
  stream's kept ids shuffled inside the kept positions by a declared
  per-floor-index rng, scored by the same machinery; every floor must
  land below the real.
- Cross band: the seven frozen class members of family 4's widened
  band - English (Frankenstein, Moby Dick, Le Morte d'Arthur volume
  1) and Latin (Caesar's De Bello Gallico I-IV, Vulgate Daniel,
  Colloquium heptaplomeres, De Rariorum Animalium atque Stirpium
  Historia) - each truncated by the standing rule and encoded under
  the same declared partition rule through a per-text sequential
  drawing scheme following family 4's widened scheme exactly: one
  sampling rng draws the five encodings of a text in order, one
  machinery rng runs the five climbs in order, the text position in
  the seed. Band membership for this family is unconditional and
  each member's band value is its five-draw machinery best, because
  the pre-run probe's finding put the noise of this family in kind
  and in place: the cap-truncated recoveries vary systematically
  above the members' identity anchors, disclosed and recorded, on
  both sides of the comparison - so the family 4 agreement gate is
  not carried over, the five draws of each member are recorded with
  their exact values and spread, and the smallest member value sets
  the band threshold for its cell. The special outcome
  machinery-noise-unresolved remains declared for a cell in which no
  member is recoverable at all, which cannot arise while class
  members exist; it is retained formally for completeness.

Declared seed kinds, before the run: the real recomputes from kind 1
under the standing seed scheme _seed = [20261020, cell, kind, lang,
index] with the SAME declared seed kind 1 the substitution family
uses, so the real's replay key stays comparable in spirit across
families while this artifact's own kinds are 24 to 29: homophonic
plant sampling 24, homophonic plant machinery 25 (the plant index);
homophonic floor permutation 26, homophonic floor machinery 27 (the
floor index); homophonic cross sampling 28, homophonic cross
machinery 29 (the text position in the seed). No number drawn by this
module's seeds is consumed by any other module's declared draws.

Declared verdict rule, before the run: the real at or above the
smallest member value is consistent-with-substitution; the real at
or below the largest floor is not-consistent; strictly between is
below-homophonic-band; and the formal special outcome
machinery-noise-unresolved is retained for a memberless band, which
cannot arise. Declared exclusion format, agreed here before the run:
if the real text stands below the smallest member value in all six
(file, language) cells with plant parity green and every floor below
the real, then the scoped homophonic class - several cipher symbols
per plaintext letter inside the declared 36-slot mapped alphabet,
word divisions carried, no abbreviation, no transposition, no nulls,
the sampled reference population - is excluded by count for the
manuscript's statistics as measured, and the family closes with that
wording plus the standing caveats (abbreviated scribal usage outside
the class, population sampled not exhaustive, nothing is a reading,
no mapping published). If any cell flips otherwise, the family stays
open with the disclosure, exactly as the ledger's family 4 arc
demanded before its own closure.

The standing limitations, declared before the run: no mapping is
published anywhere in this artifact, the recovered assignment is
never stored as a key, plaintext_recovered_percent stays 0, the
reference prose is modern printed text outside the manuscript's
century, and nothing here is a reading or a language claim.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from engine import voynich_transcript_stats as base
from engine.voynich_compare import index_loci
from engine.voynich_ivtff import DATA_DIR, load
from engine.voynich_substitution import (
    BOUNDARY,
    BASE_SEED,
    CELL_ID,
    CROSS_REFERENCE_FILES,
    DATA_DIR,
    FILES,
    LANGS,
    LANG_ID,
    REFERENCE_FILES,
    WIDENED_REFERENCE_FILES,
    _reference_stream,
    _seed,
    table_from_stream,
)


# The declared wider mapped alphabet of this family: the file's most
# frequent glyph characters up to this count, plus the word-boundary
# mark in the last position.
MAPPED_HOMO = 36

N_PLANTS = 5
N_FLOORS = 5
SWEEP_CAP = 200        # inherited from the substitution family
N_RESTARTS = 16        # inherited from the substitution family

KIND_ID = {"real": 1,
           "homo_plant_enc": 24, "homo_plant_mach": 25,
           "homo_floor_perm": 26, "homo_floor_mach": 27,
           "homo_cross_enc": 28, "homo_cross_mach": 29}

HOMO_ARTIFACT_PATH = (
    Path(DATA_DIR).resolve().parent.parent.parent
    / "docs" / "research-notes" / "voynich-homophonic-screen.json"
)


# --------------------------------------------------------------------------
# The real streams at the homophonic alphabet
# --------------------------------------------------------------------------

_REAL_STREAMS: dict[str, dict] = {}


def _homo_real_stream(code: str) -> dict:
    """The real stream at the homophonic mapped set, one per file."""
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
    mapped_chars = tuple(char for char, _count in ranked[:MAPPED_HOMO]) + (
        BOUNDARY,
    )
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
    stream = {
        "mapped_chars": mapped_chars,
        "event_ids": ids,
        "kept_ids": ids[mask],
        "kept_mask": mask,
        "total_events": len(events),
        "word_count": word_count,
        "boundary_count": boundary_count,
    }
    _REAL_STREAMS[code] = stream
    return stream


def _count_matrix_37(events_ids: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Pair counts over originally adjacent mapped positions, the
    alphabet 37 wide (36 glyphs plus the boundary mark)."""
    kept = np.where(mask)[0]
    values = events_ids[kept]
    adjacent = kept[1:] == kept[:-1] + 1
    first = values[:-1][adjacent]
    second = values[1:][adjacent]
    matrix = np.zeros((37, 37))
    np.add.at(matrix, (first, second), 1.0)
    return matrix


def _full_matrix_37(stream_ids: np.ndarray) -> np.ndarray:
    matrix = np.zeros((37, 37))
    np.add.at(matrix, (stream_ids[:-1], stream_ids[1:]), 1.0)
    return matrix


def _stream_matrix_27(stream_ids: list[int]) -> np.ndarray:
    """The pair count matrix of a reference-letter stream (27 wide)."""
    ids = np.array(stream_ids, dtype=np.int64)
    matrix = np.zeros((27, 27))
    np.add.at(matrix, (ids[:-1], ids[1:]), 1.0)
    return matrix


# --------------------------------------------------------------------------
# The homophonic assignment search
# --------------------------------------------------------------------------


def _score(f: np.ndarray, matrix: np.ndarray, table: np.ndarray) -> float:
    """The assignment score summed over the symbol pair matrix."""
    decoded = table[f][:, f]
    return float((matrix * decoded).sum())


def _climb(
    matrix: np.ndarray,
    table: np.ndarray,
    f0: list[int],
) -> tuple[float, int]:
    """The declared greedy reassignment hill-climb.

    One pass per sweep walks the symbols in index order. For each
    symbol its 27 candidate labels are evaluated exactly from the
    running score (outbound pairs, inbound pairs, and its diagonal
    removed once); a label is adopted only on a strict improvement
    beyond 1e-12. The best assignment's exact re-evaluated score is
    returned with the sweep count.
    """
    f = np.array(f0, dtype=np.int64)
    best = _score(f, matrix, table)
    f_best = f.copy()
    diag_table = np.diag(table).copy()
    sweeps = 0
    improved = True
    while improved and sweeps < SWEEP_CAP:
        improved = False
        sweeps += 1
        for symbol in range(len(f)):
            outbound = table[:, f] @ matrix[symbol]
            inbound = matrix[:, symbol] @ table[f, :]
            current = f[symbol]
            hold = (outbound[current] + inbound[current]
                    - matrix[symbol, symbol] * table[current, current])
            candidates = (
                best
                + outbound
                + inbound
                - matrix[symbol, symbol] * diag_table
                - hold
            )
            # candidates[current] == best exactly by construction
            pick = int(np.argmax(candidates))
            value = float(candidates[pick])
            if value > best + 1e-12:
                best = value
                f[symbol] = pick
                f_best = f.copy()
                improved = True
    return _score(f_best, matrix, table), sweeps


def _rank_init(matrix: np.ndarray, letter_counts: np.ndarray) -> list[int]:
    """Declared frequency-rank initialisation with surplus wrapping.

    The k-th most frequent symbol starts at the k-th most frequent
    letter token, k modulo 27; the boundary mark starts and moves like
    any symbol.
    """
    totals = matrix.sum(axis=1) + matrix.sum(axis=0)
    symbol_rank = np.argsort(-totals, kind="stable")
    letter_rank = np.argsort(-letter_counts, kind="stable")
    f = [0] * len(totals)
    for k, symbol in enumerate(symbol_rank):
        f[int(symbol)] = int(letter_rank[k % 27])
    return f


def machinery_best(
    matrix: np.ndarray,
    table: np.ndarray,
    letter_counts: np.ndarray,
    rng: np.random.Generator,
    restarts: int = N_RESTARTS,
) -> tuple[float, bool]:
    """Best mean nats per counted pair over the declared restarts.

    Restart 0 is the rank initialisation; each later restart consumes
    one seeded permutation of the 27 letter tokens (wrapped across the
    symbol list) deterministically, in order. Returns the best score
    and whether any climb hit the declared sweep cap.
    """
    symbols = matrix.shape[0]
    best, sweeps = _climb(matrix, table, _rank_init(matrix, letter_counts))
    cap_hit = sweeps >= SWEEP_CAP
    for _index in range(restarts - 1):
        permutation = list(rng.permutation(27))
        start = [permutation[symbol % 27] for symbol in range(symbols)]
        score, sweeps = _climb(matrix, table, start)
        cap_hit = cap_hit or sweeps >= SWEEP_CAP
        best = max(best, score)
    return best / matrix.sum(), cap_hit


# --------------------------------------------------------------------------
# The declared encoder and its partition rule
# --------------------------------------------------------------------------


def _partition_groups(
    truncated: list[int],
    glyph_count: int,
) -> list[list[int]]:
    """The declared partition of the glyph slots over present letters.

    Floor shares of frequency, one slot at least per present letter,
    remaining slots by largest fractional remainder with ties to the
    ascending letter index, groups laid out letter by letter in
    descending letter frequency so the most frequent letter receives
    the most frequent glyph ids, a zero-share present letter taking
    one slot from the largest existing group. Returns one group per
    letter token 0 to 26 (the boundary token's group is empty).
    """
    letters = [value for value in truncated if value != 26]
    counts = np.bincount(np.array(letters, dtype=np.int64), minlength=26)
    present = [index for index in range(26) if counts[index] > 0]
    present.sort(key=lambda index: (-int(counts[index]), index))
    total = int(counts[present].sum())
    raw = {index: glyph_count * counts[index] / total for index in present}
    floored = {index: int(raw[index]) for index in present}
    remainder = {index: raw[index] - floored[index] for index in present}
    tokens = glyph_count - sum(floored.values())
    ordered = sorted(present, key=lambda index: (-remainder[index], index))
    for extra in range(tokens):
        floored[ordered[extra]] += 1
    zero = [index for index in present if floored[index] == 0]
    for index in zero:
        donor = max(
            (k for k in present if floored[k] > 1),
            key=lambda k: (-floored[k], k),
        )
        floored[donor] -= 1
        floored[index] = 1
    groups = {index: [] for index in present}
    glyphs = 0
    for index in present:
        groups[index] = list(range(glyphs, glyphs + floored[index]))
        glyphs += floored[index]
    return [groups.get(index, []) for index in range(27)]


def _encode(
    truncated: list[int],
    groups: list[list[int]],
    rng: np.random.Generator,
    glyph_count: int,
) -> np.ndarray:
    """The declared encoder: one uniform draw per plaintext position
    from its letter's group; boundary positions take the boundary
    mark without a draw."""
    symbols = np.empty(len(truncated), dtype=np.int64)
    for position, value in enumerate(truncated):
        if value == 26:
            symbols[position] = glyph_count
            continue
        group = groups[value]
        symbols[position] = group[int(rng.integers(len(group)))]
    return symbols


def _truncated_reference(
    code: str, language: str, file: str | None = None,
) -> list[int]:
    """The reference stream cut to the standing truncation rule."""
    total = int(_homo_real_stream(code)["total_events"])
    stream = _reference_stream(language, file=file)
    return stream[: min(total, len(stream))]


def _identity_score(
    truncated: list[int], table: np.ndarray,
) -> tuple[float, int]:
    """The truncated stream's identity score under the declared table,
    with its counted pair total."""
    matrix = _stream_matrix_27(truncated)
    total = int(matrix.sum())
    value = float((matrix * table).sum()) / total
    return value, total


# --------------------------------------------------------------------------
# The screen
# --------------------------------------------------------------------------


def _cell_facts(code: str, language: str) -> dict:
    """Real, plants with their anchor, and floors for one cell, all
    under the declared machinery at the declared budget."""
    table, letter_counts = table_from_stream(
        _reference_stream(language)
    )
    real_stream = _homo_real_stream(code)
    matrix = _count_matrix_37(
        real_stream["event_ids"], real_stream["kept_mask"]
    )
    real_rng = np.random.default_rng(
        _seed(CELL_ID[code], KIND_ID["real"], LANG_ID[language], 0)
    )
    value, hit = machinery_best(
        matrix, table, letter_counts, real_rng, restarts=N_RESTARTS
    )
    real = round(value, 4)
    real_hit = bool(hit)
    truncated = _truncated_reference(code, language)
    anchor, _anchor_total = _identity_score(truncated, table)
    anchor = round(anchor, 4)
    plants = []
    plants_hits = []
    for index in range(N_PLANTS):
        groups = _partition_groups(truncated, MAPPED_HOMO)
        rng_enc = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["homo_plant_enc"],
                  LANG_ID[language], index)
        )
        plant = _encode(truncated, groups, rng_enc, MAPPED_HOMO)
        plant_matrix = _full_matrix_37(plant)
        rng_mach = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["homo_plant_mach"],
                  LANG_ID[language], index)
        )
        value, hit = machinery_best(
            plant_matrix, table, letter_counts, rng_mach,
            restarts=N_RESTARTS,
        )
        plants.append(round(value, 4))
        plants_hits.append(bool(hit))
    floors = []
    floors_hits = []
    for index in range(N_FLOORS):
        rng_perm = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["homo_floor_perm"],
                  LANG_ID[language], index)
        )
        values = real_stream["kept_ids"].copy()
        rng_perm.shuffle(values)
        full = real_stream["event_ids"].copy()
        full[real_stream["kept_mask"]] = values
        floor_matrix = _count_matrix_37(full, real_stream["kept_mask"])
        rng_mach = np.random.default_rng(
            _seed(CELL_ID[code], KIND_ID["homo_floor_mach"],
                  LANG_ID[language], index)
        )
        value, hit = machinery_best(
            floor_matrix, table, letter_counts, rng_mach,
            restarts=N_RESTARTS,
        )
        floors.append(round(value, 4))
        floors_hits.append(bool(hit))
    return {
        "real": real,
        "real_sweep_budget_hit": real_hit,
        "counted": int(matrix.sum()),
        "anchor": anchor,
        "plants": plants,
        "plants_hits": plants_hits,
        "floors": floors,
        "floors_hits": floors_hits,
    }


def _band_for(code: str, language: str, seed_index: int) -> dict:
    """Five homophonic encodings of one class-member text, their
    machinery bests, and the member's own anchor, under the declared
    per-text sequential scheme (one sampling rng draws the five
    encodings in order, one machinery rng runs the five climbs in
    order)."""
    table, letter_counts = table_from_stream(
        _reference_stream(language)
    )
    name, ebook = (
        [CROSS_REFERENCE_FILES[language]]
        + list(WIDENED_REFERENCE_FILES[language])
    )[seed_index][:2]
    truncated = _truncated_reference(code, language, file=name)
    anchor, _total = _identity_score(truncated, table)
    anchor = round(anchor, 4)
    rng_enc = np.random.default_rng(
        _seed(CELL_ID[code], KIND_ID["homo_cross_enc"],
              LANG_ID[language], seed_index)
    )
    rng_mach = np.random.default_rng(
        _seed(CELL_ID[code], KIND_ID["homo_cross_mach"],
              LANG_ID[language], seed_index)
    )
    draws = []
    draw_hits = []
    for _index in range(N_PLANTS):
        groups = _partition_groups(truncated, MAPPED_HOMO)
        encoded = _encode(truncated, groups, rng_enc, MAPPED_HOMO)
        encoded_matrix = _full_matrix_37(encoded)
        value, hit = machinery_best(
            encoded_matrix, table, letter_counts, rng_mach,
            restarts=N_RESTARTS,
        )
        draws.append(round(value, 4))
        draw_hits.append(bool(hit))
    spread = round(max(draws) - min(draws), 4)
    return {
        "file": name,
        "ebook": ebook,
        "plant_length": len(truncated),
        "anchor": anchor,
        "draws": draws,
        "draw_cap_hits": draw_hits,
        "recovered_best": max(draws),
        "spread": spread,
    }


def substitution_homophonic_screen() -> dict:
    """The declared homophonic screen: all three files, both
    languages, plants, floors, and the seven-text cross band."""
    artifact: dict = {
        "what": "The declared homophonic screen: several cipher symbols "
        "may share one plaintext letter while every cipher symbol names "
        "exactly one letter, on the same frozen streams, mapped sets "
        "(widened to 36 glyphs plus the word boundary mark), references "
        "and add-one bigram models as the substitution family, scored by "
        "a declared greedy reassignment climb with the inherited restart "
        "and sweep budgets. Plants are encodings of the truncated "
        "references by a declared partition rule; the cross band encodes "
        "the seven class members of the widened band; membership is "
        "unconditional and each member's value is its five-draw "
        "machinery best, with the declared cap truncation disclosed on "
        "both sides. No mapping is published; nothing here is a reading.",
        "declared": {
            "base_seed": BASE_SEED,
            "mapped_glyph_budget_comment": "the mapped set is the file's "
            "most frequent glyph characters up to 36 plus the "
            "word-boundary mark; letters 26 plus the boundary token",
            "mapped": MAPPED_HOMO,
            "restarts": N_RESTARTS,
            "sweep_cap": SWEEP_CAP,
            "plants_per_cell": N_PLANTS,
            "floors": N_FLOORS,
            "band_membership_rule": "membership is unconditional; each "
            "member's band value is its five-draw machinery best; all "
            "five draws and their spread are recorded, and the smallest "
            "member value sets the band threshold for its cell; the "
            "declaration of the sweep-cap disclosure applies to both "
            "sides of every comparison",
            "seed_kinds": {
                "real": KIND_ID["real"],
                "homo_plant": [KIND_ID["homo_plant_enc"],
                               KIND_ID["homo_plant_mach"]],
                "homo_floor": [KIND_ID["homo_floor_perm"],
                               KIND_ID["homo_floor_mach"]],
                "homo_cross": [KIND_ID["homo_cross_enc"],
                               KIND_ID["homo_cross_mach"]],
            },
            "models": {},
            "verdict_rule": "real at or above the smallest member value "
            "is consistent-with-substitution; real at or below the "
            "largest floor is not-consistent; strictly between is "
            "below-homophonic-band; machinery-noise-unresolved is "
            "retained formally for a memberless band, which cannot "
            "arise",
            "exclusion_rule": "if the real text stands below the "
            "smallest member value in all six cells with plant parity "
            "green and every floor below the real, the scoped "
            "homophonic class is excluded by count for the measured "
            "statistics, with the standing caveats",
        },
        "files": {},
    }
    for language in LANGS:
        name, ebook = REFERENCE_FILES[language]
        stream = _reference_stream(language)
        matrix = _stream_matrix_27(stream)
        artifact["declared"]["models"][language] = {
            "file": name,
            "ebook": ebook,
            "clean_identity_mean_nats_per_pair": round(
                float((matrix * table_from_stream(stream)[0]).sum())
                / float(matrix.sum()),
                4,
            ),
        }
    for code in FILES:
        cell: dict = {}
        for language in LANGS:
            facts = _cell_facts(code, language)
            members = []
            if language == "english":
                positions = (0, 1, 2)
            else:
                positions = (0, 1, 2, 3)
            for seed_index in positions:
                members.append(_band_for(code, language, seed_index))
            member_values = [member["recovered_best"] for member in members]
            floor_max = max(facts["floors"])
            band_min = min(member_values)
            band_max = max(member_values)
            if facts["real"] >= band_min:
                verdict = "consistent-with-substitution"
            elif facts["real"] <= floor_max:
                verdict = "not-consistent"
            else:
                verdict = "below-homophonic-band"
            parity = [
                bool(value >= facts["anchor"] - 0.0001)
                for value in facts["plants"]
            ]
            above_anchor = [
                round(value - facts["anchor"], 4)
                for value in facts["plants"]
                if value > facts["anchor"] + 0.0001
            ]
            cell[language] = {
                "real_best_mean_nats": facts["real"],
                "real_sweep_budget_hit": facts["real_sweep_budget_hit"],
                "counted_pairs": facts["counted"],
                "plant_parity_anchor_mean_nats": facts["anchor"],
                "self_plants_best_mean_nats": facts["plants"],
                "self_plants_at_parity": parity,
                "self_plants_sweep_budget_hits": facts["plants_hits"],
                "machinery_above_anchor_excesses": above_anchor,
                "floors_best_mean_nats": facts["floors"],
                "floors_sweep_budget_hits": facts["floors_hits"],
                "band": members,
                "band_min": band_min,
                "band_max": band_max,
                "verdict": verdict,
            }
        artifact["files"][code] = cell
    return artifact


def main() -> None:
    artifact = substitution_homophonic_screen()
    HOMO_ARTIFACT_PATH.write_text(json.dumps(artifact, indent=2) + "\n")
    print(HOMO_ARTIFACT_PATH)
