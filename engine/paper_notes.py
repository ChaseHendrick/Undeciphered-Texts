"""Facts a later paper can cite. Not a paper, and not a reading.

The notes are built from the frozen scores. A search is a substring over
the id, the statement, and the tags. Nothing here is a plaintext.
"""

from __future__ import annotations

from engine.bob_branch import bob_branch_report
from engine.dagapeyeff_clump import clump_report
from engine.dagapeyeff_widths import widths_report
from engine.dagapeyeff_depth3 import depth3_report
from engine.dagapeyeff_depth4 import depth4_report
from engine.dagapeyeff_placed import placed_report
from engine.dagapeyeff_repair import repair_report


def paper_notes() -> dict:
    third = depth3_report()
    fourth = depth4_report()
    placed = placed_report()
    repair = repair_report()
    branch = bob_branch_report()
    clump = clump_report()
    widths = widths_report()
    notes = [
        {
            "id": "three-moves-cannot-clear",
            "kind": "bound",
            "tags": ["counts", "chi-square", "ball"],
            "statement": (
                f"{third['states']} three-move count changes were scored. "
                f"The best chi-square is {third['best_chi']}. "
                f"Its ball runs from {third['ball_lo']} to {third['ball_hi']}, "
                f"entirely above the English line at {third['english_line']}."
            ),
            "do_not_claim": "Three moves cannot counterfeit English counts. This is not a reading.",
        },
        {
            "id": "four-moves-clear-counts-only",
            "kind": "bound",
            "tags": ["counts", "chi-square", "ball"],
            "statement": (
                f"{fourth['tied_after_three']} three-move states tie. "
                f"{fourth['fourth_states']} fourth moves were scored. "
                f"The best chi-square is {fourth['best_chi']}. "
                f"Its ball runs from {fourth['ball_lo']} to {fourth['ball_hi']} "
                f"and does clear {fourth['english_line']}. "
                f"{fourth['point_under_line']} states have a point score under the line. "
                "The edited positions were not kept."
            ),
            "do_not_claim": "A count under the English line is not a reading.",
        },
        {
            "id": "placed-edits-match-a-shuffle",
            "kind": "negative",
            "tags": ["order", "quadgram", "shuffle"],
            "statement": (
                f"{placed['targets']} count vectors were placed on the cells, "
                f"{placed['placements']} ways. The best order scores {placed['best_quadgram']}. "
                f"Prose is {placed['prose_quadgram']}. "
                f"{placed['shuffles_as_high']} of {placed['draws']} shuffled orders do as well."
            ),
            "do_not_claim": "Matching the counts does not make the order English.",
        },
        {
            "id": "repairs-share-one-loss",
            "kind": "constraint",
            "tags": ["counts", "repair", repair["shared_symbol"]],
            "statement": (
                f"{repair['targets']} best count vectors each touch {repair['touched_each']} symbols. "
                f"The union is {repair['union']} symbols and the intersection is {repair['intersection']}. "
                f"The shared symbol is {repair['shared_symbol']}, and its role is {repair['shared_role']}. "
                f"Losses come from {repair['loss_symbols']} symbols and gains go to {repair['gain_symbols']}. "
                f"Each vector moves {repair['transfer']} counts."
            ),
            "do_not_claim": "A symbol that every count repair reduces is not identified as a wrong letter.",
        },
        {
            "id": "neighbor-edits-are-not-rare",
            "kind": "negative",
            "tags": ["order", "neighbor", "quadgram"],
            "statement": (
                f"Four neighbor edits, chosen to raise the order score, reach {repair['neighbor_quadgram']}. "
                f"{repair['neighbor_shuffles_as_high']} of {repair['neighbor_draws']} shuffles do as well. "
                f"Four free edits reach {repair['free_quadgram']}, and "
                f"{repair['free_shuffles_as_high']} of {repair['free_draws']} do as well. "
                f"One neighbor edit reaches {repair['one_quadgram']}, and "
                f"{repair['one_shuffles_as_high']} of {repair['one_draws']} do as well. "
                f"Prose is {repair['prose_quadgram']}."
            ),
            "do_not_claim": "A score a shuffle can reach is not a reading.",
        },
        {
            "id": "residual-branch-is-alive",
            "kind": "method",
            "tags": ["bob", "residual", "router"],
            "statement": (
                "The shipped residual router was not replaced. "
                f"On the challenge the branch shares are {branch['challenge_branch_share']}. "
                f"On a Caesar of known prose they are {branch['control_branch_share']}. "
                "The second layer is in use on both."
            ),
            "do_not_claim": "A live residual branch does not name a plaintext or a family for this cipher.",
        },
        {
            "id": "pair-72-window",
            "kind": "correction",
            "tags": ["72", "window", "multiple-testing"],
            "statement": (
                f"Six of the nine 72 pairs sit in rows 11 through 14. "
                f"That fixed window is {clump['fixed_shuffles_as_high']} of {clump['draws']} shuffles, "
                "but the window was chosen after looking. "
                f"Every window of that height reaches {clump['every_window_count']}, "
                f"and {clump['every_window_shuffles_as_high']} of {clump['draws']} shuffles do as well."
            ),
            "do_not_claim": "A window chosen after looking is not a clump and not a reading.",
        },
        {
            "id": "column-widths",
            "kind": "negative",
            "tags": ["widths", "131", "exercise"],
            "statement": (
                f"Of {widths['widths']} column widths, the fully legal ones are "
                f"{', '.join(str(width) for width in widths['fully_legal'])}. "
                f"Width 131 scores {widths['width_131_chi']}, and "
                f"{widths['re_pairings_as_flat']} of {widths['draws']} random re-pairings are at least that flat. "
                f"On the solved exercise the printed score is {widths['control_printed_chi']}. "
                f"Width 3 moves it to {widths['control_width_3_chi']} and width 131 moves it to {widths['control_width_131_chi']}."
            ),
            "do_not_claim": "A width that stays on the square is not a reading, and these widths hurt the solved exercise.",
        },
    ]
    return {
        "schema": "paper-notes-1",
        "solved": False,
        "claimed_plaintext": None,
        "notes": notes,
    }


def search_notes(query: str) -> list[dict]:
    if not query:
        return []
    needle = query.casefold()
    hits = []
    for note in paper_notes()["notes"]:
        haystack = " ".join([note["id"], note["kind"], note["statement"], note["do_not_claim"], *note["tags"]])
        if needle in haystack.casefold():
            hits.append(note)
    return hits
