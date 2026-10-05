"""Hash the cells and the scores that depend on them. Not a reading.

The heavy scores are read from engine/data/swarm_cache. A later hash does
not repeat the search. The encoding is part of the result. Tuples become
lists. Floats become the 17-digit general format. Object keys are sorted.
SHA-256 of that JSON is the content hash. Each step's chain hash is SHA-256
of the previous chain hash, a newline, and the new content hash. The first
step's chain hash is its content hash. No letter string is stored.
"""

from __future__ import annotations

import hashlib
import json
import math
from functools import lru_cache
from typing import Any

from engine.corrections import load_corrections
from engine.dagapeyeff_adversary import adversary_report
from engine.dagapeyeff_angles import angle_report
from engine.dagapeyeff_autokey import autokey_report
from engine.dagapeyeff_balls import ball_report
from engine.dagapeyeff_bifid import bifid_report
from engine.bob_branch import bob_branch_report
from engine.bob_caution import bob_caution_report
from engine.bob_exercise import bob_exercise_report
from engine.dagapeyeff_bookkey import bookkey_report
from engine.dagapeyeff_board import board
from engine.dagapeyeff_columns import column_report
from engine.dagapeyeff_column_null import column_null_report
from engine.dagapeyeff_convert import convert_report
from engine.dagapeyeff_delay import delay_report
from engine.dagapeyeff_depth3 import depth3_report
from engine.dagapeyeff_depth4 import depth4_report
from engine.dagapeyeff_digit_routes import digit_route_report
from engine.dagapeyeff_checks import checks_report
from engine.dagapeyeff_classic_swarm import classic_swarm_report
from engine.dagapeyeff_clump import clump_report
from engine.dagapeyeff_widths import widths_report
from engine.dagapeyeff_hole import hole_report
from engine.dagapeyeff_clerical import clerical_report
from engine.dagapeyeff_intro import intro_report
from engine.dagapeyeff_block import block_report
from engine.dagapeyeff_digraph import digraph_report
from engine.dagapeyeff_trigram import trigram_report
from engine.dagapeyeff_triples import triples_report
from engine.dagapeyeff_contact import contact_report
from engine.dagapeyeff_meeting import meeting_report
from engine.dagapeyeff_monotone import monotone_report
from engine.dagapeyeff_straight import straight_report
from engine.dagapeyeff_diagonal import diagonal_report
from engine.dagapeyeff_heavy import heavy_report
from engine.dagapeyeff_spread import spread_report
from engine.dagapeyeff_residual import residual_report
from engine.dagapeyeff_sharp import sharp_report
from engine.dagapeyeff_rest import rest_report
from engine.dagapeyeff_edits import edit_report
from engine.dagapeyeff_foresight import foresight
from engine.dagapeyeff_groups import group_report
from engine.dagapeyeff_infer import infer
from engine.dagapeyeff_keys import key_report
from engine.dagapeyeff_keystream import keystream_report
from engine.dagapeyeff_large_swarm import large_swarm_report
from engine.dagapeyeff_model import model_report
from engine.paper_notes import paper_notes
from engine.dagapeyeff_patterns import pattern_report
from engine.dagapeyeff_period4 import period4_report
from engine.dagapeyeff_placed import placed_report
from engine.dagapeyeff_places import place_report
from engine.dagapeyeff_record import record_report
from engine.dagapeyeff_refined import refined_report
from engine.dagapeyeff_regroup import regroup_report
from engine.dagapeyeff_repair import repair_report
from engine.dagapeyeff_running import running_report
from engine.dagapeyeff_router_swarm import router_swarm_report
from engine.dagapeyeff_solver_swarm import solver_swarm_report
from engine.dagapeyeff_swarm import challenge_pairs
from engine.dagapeyeff_word import word_report
from engine.dagapeyeff_yardstick import yardstick_report


def freeze(value: Any) -> Any:
    if value is None or isinstance(value, (bool, int, str)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("a provenance hash cannot cover a non-finite float")
        return format(value, ".17g")
    if isinstance(value, (list, tuple)):
        return [freeze(item) for item in value]
    if isinstance(value, dict):
        return {str(key): freeze(value[key]) for key in sorted(value, key=str)}
    raise TypeError(f"no provenance encoding for {type(value).__name__}")


def content_hash(value: Any) -> str:
    payload = json.dumps(freeze(value), separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def chain_hash(previous: str | None, content: str) -> str:
    if previous is None:
        return content
    return hashlib.sha256(f"{previous}\n{content}".encode("utf-8")).hexdigest()


@lru_cache(maxsize=1)
def provenance_report() -> dict:
    steps = (
        ("cells", list(challenge_pairs())),
        ("yardstick", yardstick_report()),
        ("balls", ball_report()),
        ("record", record_report()),
        ("convert", convert_report()),
        ("edits", edit_report()),
        ("corrections", load_corrections()),
        ("regroup", regroup_report()),
        ("keys", key_report()),
        ("model", model_report()),
        ("bifid", bifid_report()),
        ("period4", period4_report()),
        ("word", word_report()),
        ("running", running_report()),
        ("patterns", pattern_report()),
        ("columns", column_report()),
        ("board", board()),
        ("infer", infer()),
        ("foresight", foresight()),
        ("checks", checks_report()),
        ("adversary", adversary_report()),
        ("autokey", autokey_report()),
        ("digit-routes", digit_route_report()),
        ("angles", angle_report()),
        ("delay", delay_report()),
        ("bookkey", bookkey_report()),
        ("groups", group_report()),
        ("places", place_report()),
        ("solver-swarm", solver_swarm_report()),
        ("classic-swarm", classic_swarm_report()),
        ("router-swarm", router_swarm_report()),
        ("column-null", column_null_report()),
        ("large-swarm", large_swarm_report()),
        ("refined-swarm", refined_report()),
        ("bob-caution", bob_caution_report()),
        ("keystream", keystream_report()),
        ("depth3", depth3_report()),
        ("depth4", depth4_report()),
        ("placed", placed_report()),
        ("repair", repair_report()),
        ("clump", clump_report()),
        ("bob-branch", bob_branch_report()),
        ("paper", paper_notes()),
        ("widths", widths_report()),
        ("hole", hole_report()),
        ("clerical", clerical_report()),
        ("intro", intro_report()),
        ("block", block_report()),
        ("digraph", digraph_report()),
        ("trigram", trigram_report()),
        ("monotone", monotone_report()),
        ("straight", straight_report()),
        ("diagonal", diagonal_report()),
        ("heavy", heavy_report()),
        ("spread", spread_report()),
        ("residual", residual_report()),
        ("sharp", sharp_report()),
        ("rest", rest_report()),
        ("bob-exercise", bob_exercise_report()),
        ("triples", triples_report()),
        ("contact", contact_report()),
        ("meeting", meeting_report()),
    )
    entries = []
    previous = None
    for name, value in steps:
        content = content_hash(value)
        previous = chain_hash(previous, content)
        entries.append({"name": name, "content_sha256": content, "chain_sha256": previous})
    return {
        "solved": False,
        "claimed_plaintext": None,
        "entries": entries,
        "chain_sha256": previous,
        "scope": (
            "A matching hash means the cells and these scores were recomputed, not that they were read. "
            "No letter string is stored."
        ),
    }
