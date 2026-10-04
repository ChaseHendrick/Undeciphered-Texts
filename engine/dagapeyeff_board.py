"""What each D'Agapeyeff swarm is saying. Not a reading.

The sentences come from the solver. The "do not" line is the instruction
for the next pass. search_board matches a query against the id, the
finding, and that instruction. A hit is not a plaintext.
"""

from __future__ import annotations

from engine.solvers.dagapeyeff import (
    consider_bifid,
    consider_column_key,
    consider_columns,
    consider_frequency_claim,
    consider_language_model,
    consider_patterns,
    consider_period4,
    consider_regrouping,
    consider_running_key,
    consider_word_score,
)

_DO_NOT = {
    "frequency": "Do not treat a chi-square under the English line as a reading.",
    "regrouping": "Do not adopt regrouping 01432 because the counts look English.",
    "column-key": "Do not keep a column order of that regrouping that loses to repeated shuffles.",
    "language-model": "Do not prefer a labeling because its chi-square fell. Ask the word model.",
    "bifid": "Do not search more bifid periods on these coordinates.",
    "period-4": "Do not lengthen the repeating shift to chase friendlier counts.",
    "word-score": "Do not call -3.2713 a record. Prose is -2.5185.",
    "running-key": "Do not slide these five texts again.",
    "patterns": "Do not expect the printed order to be rich in dictionary shapes.",
    "columns": "Do not trust the column order with the most dictionary windows unless shuffled grids miss it.",
}


def _cards() -> list[tuple[str, dict]]:
    return [
        ("frequency", consider_frequency_claim(0, 100.0)),
        ("regrouping", consider_regrouping()),
        ("column-key", consider_column_key()),
        ("language-model", consider_language_model()),
        ("bifid", consider_bifid()),
        ("period-4", consider_period4()),
        ("word-score", consider_word_score()),
        ("running-key", consider_running_key()),
        ("patterns", consider_patterns()),
        ("columns", consider_columns()),
    ]


def _allowed(claim: dict) -> bool:
    flags = [value for key, value in claim.items() if key.endswith("_allowed")]
    if len(flags) != 1 or not isinstance(flags[0], bool):
        raise ValueError("a swarm card needs exactly one allowed flag")
    return flags[0]


def board() -> dict:
    records = []
    for name, claim in _cards():
        allowed = _allowed(claim)
        records.append({
            "id": name,
            "verdict": "open" if allowed else "refuse",
            "finding": claim["learned"],
            "do_not": _DO_NOT[name],
            "solved": False,
            "claimed_plaintext": None,
        })
    return {
        "schema": "swarm-board-1",
        "solved": False,
        "claimed_plaintext": None,
        "bar": "Prose scores -2.5185 per quadgram. A searched maximum counts only when the same search on shuffled cells does not reach it.",
        "records": records,
    }


def search_board(query: str) -> list[dict]:
    """Records whose id, finding, or instruction contain every word of the query."""
    words = [word.casefold() for word in query.split() if word]
    if not words:
        return []
    hits = []
    for record in board()["records"]:
        haystack = " ".join([record["id"], record["finding"], record["do_not"]]).casefold()
        if all(word in haystack for word in words):
            hits.append(record)
    return hits


def board_text() -> str:
    """One page. The solver sentences are not rewritten."""
    data = board()
    lines = [
        "# What the swarms are saying",
        "",
        "4 October 2026. Not a reading. No letter string is stored.",
        "",
        data["bar"],
        "",
        "Search this page from code with `engine.dagapeyeff_board.search_board`. A hit is not a plaintext.",
        "",
    ]
    for record in data["records"]:
        lines.append(f"## {record['id']}: {record['verdict']}")
        lines.append("")
        lines.append(record["finding"])
        lines.append("")
        lines.append(record["do_not"])
        lines.append("")
    from engine.dagapeyeff_infer import infer

    drawn = infer()
    lines.append("## Inference")
    lines.append("")
    for item in drawn["classes"]:
        lines.append(f"{item['id']}: {item['status']}. {item['because']} {item['do_not']}")
        lines.append("")
    lines.append(f"Not a next step: {drawn['not_a_next_step']}")
    lines.append("")
    lines.append(drawn["required"])
    lines.append("")
    from engine.dagapeyeff_foresight import foresight

    chosen = foresight()
    lines.append("## Next")
    lines.append("")
    lines.append(chosen["learned"])
    lines.append("")
    lines.append(chosen["do_not"])
    lines.append("")
    from engine.dagapeyeff_checks import checks_report

    checked = checks_report()
    lines.append(checked["learned"])
    lines.append("")
    lines.append("No letter string is stored.")
    lines.append("")
    return "\n".join(lines)
