"""Attacks on the swarm gates. Not a reading.

A disguised check tries to change the cells while wearing the check label.
A refusal card with a letter string, or with solved set, tries to keep a
class closed. A frequency claim that clears the line tries to become a
reading. Each attack is blocked, or the report says so. No letter string
is stored.
"""

from __future__ import annotations

from engine.dagapeyeff_board import board
from engine.dagapeyeff_checks import checks_report
from engine.dagapeyeff_foresight import after_training, foresight, judge_job
from engine.dagapeyeff_infer import infer
from engine.solvers.dagapeyeff import (
    consider_angles,
    consider_autokey,
    consider_bifid,
    consider_bob,
    consider_branch,
    consider_bookkey,
    consider_column_key,
    consider_columns,
    consider_column_null,
    consider_classic_swarm,
    consider_clump,
    consider_widths,
    consider_delay,
    consider_depth3,
    consider_depth4,
    consider_digit_routes,
    consider_frequency_claim,
    consider_groups,
    consider_keystream,
    consider_language_model,
    consider_large_swarm,
    consider_patterns,
    consider_places,
    consider_period4,
    consider_placed,
    consider_regrouping,
    consider_refined,
    consider_repair,
    consider_running_key,
    consider_router_swarm,
    consider_solver_swarm,
    consider_word_score,
)

_DISGUISED = {
    "id": "disguised",
    "family": "parity",
    "changes_cells": True,
    "score": "word",
    "has_null": True,
    "budget": "small",
    "kind": "check",
}


def _poison(record_id: str, **changes: object) -> list[dict]:
    records = [dict(record) for record in board()["records"]]
    for record in records:
        if record["id"] == record_id:
            record.update(changes)
    return records


def adversary_report() -> dict:
    disguised = judge_job(_DISGUISED)
    plaintext = infer(_poison("frequency", claimed_plaintext="X"))
    solved_flag = infer(_poison("word-score", solved=True))
    counts = next(item for item in plaintext["classes"] if item["id"] == "counts")
    short_keys = next(item for item in solved_flag["classes"] if item["id"] == "short-keys")
    claims = [
        consider_frequency_claim(4, 0.0),
        consider_regrouping(),
        consider_column_key(),
        consider_language_model(),
        consider_bifid(),
        consider_period4(),
        consider_word_score(),
        consider_running_key(),
        consider_patterns(),
        consider_columns(),
        consider_autokey(),
        consider_digit_routes(),
        consider_angles(),
        consider_delay(),
        consider_bookkey(),
        consider_groups(),
        consider_places(),
        consider_solver_swarm(),
        consider_classic_swarm(),
        consider_router_swarm(),
        consider_column_null(),
        consider_large_swarm(),
        consider_refined(),
        consider_bob(),
        consider_keystream(),
        consider_depth3(),
        consider_depth4(),
        consider_placed(),
        consider_repair(),
        consider_clump(),
        consider_widths(),
        consider_branch(),
    ]
    frequency = claims[0]
    readings = [claim for claim in claims if claim["solved"] is not False or claim["claimed_plaintext"] is not None]
    data = board()
    checked = checks_report()
    trained = after_training()
    first = foresight()
    attacks = [
        {
            "id": "disguised-check",
            "blocked": disguised["rejected"] and disguised["solved"] is False,
        },
        {
            "id": "plaintext-on-a-refusal",
            "blocked": counts["status"] == "open" and plaintext["solved"] is False,
        },
        {
            "id": "solved-flag-on-a-refusal",
            "blocked": short_keys["status"] == "open" and solved_flag["solved"] is False,
        },
        {
            "id": "frequency-clears-the-line",
            "blocked": frequency["frequency_claim_allowed"] is True and frequency["solved"] is False and frequency["claimed_plaintext"] is None,
        },
        {
            "id": "solver-claims",
            "blocked": readings == [],
        },
        {
            "id": "regression",
            "blocked": (
                checked["sound"] is True
                and len(data["records"]) == 10
                and all(record["verdict"] == "refuse" for record in data["records"])
                and infer()["all_listed_closed"] is True
                and first["accepted"] == ["group-digit"]
                and trained["accepted"] == ["end-pairs"]
            ),
        },
    ]
    return {
        "solved": False,
        "claimed_plaintext": None,
        "attacks": attacks,
        "all_blocked": all(attack["blocked"] for attack in attacks),
        "learned": (
            "A job labeled as a check used to skip the closer even when it changed the cells. "
            "The closer now refuses that disguise. "
            "A refusal card that carries a letter string, or solved set to true, no longer closes its class. "
            "Clearing the frequency line still does not solve anything. "
            "Six attacks, all blocked."
        ),
    }
