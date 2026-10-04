"""What the swarm board implies. Not a reading.

A class closes only when every card it cites is a refusal. Opening one
card opens the class again. The requirement at the bottom is a rule for
the next pass, not a claim that such a rule has been found.
"""

from __future__ import annotations

from engine.dagapeyeff_board import board

_CLASSES = (
    {
        "id": "counts",
        "supports": ("frequency", "regrouping", "period-4"),
        "because": "Friendlier counts were scored three ways, and each was refused.",
        "do_not": "Do not bring a lower chi-square back as progress.",
    },
    {
        "id": "same-cells",
        "supports": ("column-key", "patterns", "columns"),
        "because": "Another order of the same cells was scored, and the shuffles matched it.",
        "do_not": "Do not search another reading order of these cells.",
    },
    {
        "id": "short-keys",
        "supports": ("language-model", "bifid", "word-score", "running-key"),
        "because": "The word score was asked on a short shift, a bifid, and a running key, and none beat prose.",
        "do_not": "Do not lengthen that shift, add a bifid period, or reuse those five texts.",
    },
)


def infer(records: list[dict] | None = None) -> dict:
    if records is None:
        records = board()["records"]
    by_id = {record["id"]: record for record in records}
    classes = []
    for spec in _CLASSES:
        missing = [name for name in spec["supports"] if name not in by_id]
        if missing:
            raise ValueError(f"inference cites a missing card: {missing}")
        refused = all(
            by_id[name]["verdict"] == "refuse"
            and by_id[name]["solved"] is False
            and by_id[name]["claimed_plaintext"] is None
            for name in spec["supports"]
        )
        classes.append({
            "id": spec["id"],
            "supports": list(spec["supports"]),
            "status": "closed" if refused else "open",
            "because": spec["because"] if refused else "A supporting card is not a refusal.",
            "do_not": spec["do_not"] if refused else "The class is open. Read the card that is not a refusal.",
        })
    return {
        "solved": False,
        "claimed_plaintext": None,
        "classes": classes,
        "all_listed_closed": all(item["status"] == "closed" for item in classes),
        "not_a_next_step": (
            "Another order of the same cells, a longer repeat of the same shift, "
            "another bifid period, or the five texts already used as a running key."
        ),
        "required": (
            "A rule outside the closed classes. It has to beat prose at -2.5185, "
            "and the same search on shuffled cells has to miss it. "
            "Meeting that bar is still not a reading until the control is checked."
        ),
    }
