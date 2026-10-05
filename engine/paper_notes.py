"""Facts a later paper can cite. Not a paper, and not a reading.

The notes are built from the frozen scores. A search is a substring over
the id, the statement, and the tags. Nothing here is a plaintext.
"""

from __future__ import annotations

from engine.bob_branch import bob_branch_report
from engine.bob_caution import bob_caution_report
from engine.bob_exercise import bob_exercise_report
from engine.dagapeyeff_clump import clump_report
from engine.dagapeyeff_widths import widths_report
from engine.dagapeyeff_hole import hole_report
from engine.dagapeyeff_clerical import clerical_report
from engine.dagapeyeff_intro import intro_report
from engine.dagapeyeff_block import block_report
from engine.dagapeyeff_digraph import digraph_report
from engine.dagapeyeff_trigram import trigram_report
from engine.dagapeyeff_triples import triples_report
from engine.dagapeyeff_monotone import monotone_report
from engine.dagapeyeff_straight import straight_report
from engine.dagapeyeff_diagonal import diagonal_report
from engine.dagapeyeff_heavy import heavy_report
from engine.dagapeyeff_spread import spread_report
from engine.dagapeyeff_residual import residual_report
from engine.dagapeyeff_sharp import sharp_report
from engine.dagapeyeff_rest import rest_report
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
    hole = hole_report()
    clerical = clerical_report()
    intro = intro_report()
    block = block_report()
    digraph = digraph_report()
    trigram = trigram_report()
    triples = triples_report()
    monotone = monotone_report()
    straight = straight_report()
    diagonal = diagonal_report()
    heavy = heavy_report()
    spread = spread_report()
    residual = residual_report()
    sharp = sharp_report()
    rest = rest_report()
    caution = bob_caution_report()
    exercise = bob_exercise_report()
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
        {
            "id": "frequency-hole",
            "kind": "constraint",
            "tags": ["column-14", "gap", "period-7"],
            "statement": (
                f"Occupied counts jump by {hole['gap']} between {hole['low_max']} and {hole['high_min']}. "
                f"All {hole['low_cells']} low-side cells sit in column 14. "
                f"{hole['already_recorded_cells']} were already recorded. "
                f"The other {hole['new_cells']}, given those, sit there in "
                f"{hole['step_numerator']} of {hole['step_denominator']} placements. "
                f"Count {hole['high_min']} does not follow: {hole['high_in_named_column']} of {hole['high_cells']}. "
                f"Lag 7 is {hole['period7_as_high']} of {hole['period7_draws']} shuffles."
            ),
            "do_not_claim": "A rare column placement is not a reading, and an ordinary period is not a key.",
        },
        {
            "id": "clerical-line",
            "kind": "negative",
            "tags": ["check-digit", "column", "row"],
            "statement": (
                f"Seven check rules were fixed first. The best one is "
                f"{clerical['first_digit_as_high']} of {clerical['check_draws']} shuffles, "
                f"and the best of the seven is {clerical['family_as_high']} of {clerical['check_draws']}. "
                f"A column holds one symbol {clerical['column_mode']} times, "
                f"{clerical['column_as_high']} of {clerical['line_draws']} shuffles. "
                "Allowing a row as well, 7.2 percent of the shuffles still reach that height."
            ),
            "do_not_claim": "A column that looks rare until a row is allowed is not a reading.",
        },
        {
            "id": "new-cell-wait",
            "kind": "comparison",
            "tags": ["introduction", "hole", "exercise"],
            "statement": (
                f"The longest wait for a new cell is {intro['longest_wait']}. "
                f"{intro['as_short']} of {intro['draws']} shuffles wait that little or less. "
                f"Given the low side of the frequency hole, {intro['hole_as_short']} of {intro['draws']} still do. "
                f"The solved exercise waits {intro['control_longest_wait']}, "
                f"and {intro['control_as_short']} of {intro['draws']} of its shuffles do as well."
            ),
            "do_not_claim": "A short wait that the solved exercise shares is not a reading.",
        },
        {
            "id": "singleton-block",
            "kind": "comparison",
            "tags": ["column-14", "singleton", "block"],
            "statement": (
                f"The three cells that appear once sit in rows {block['rows'][0] + 1}, "
                f"{block['rows'][1] + 1}, and {block['rows'][2] + 1}, consecutively. "
                f"{block['named_numerator']} of {block['named_denominator']} seatings do that. "
                f"If the pair or the triple may be packed instead, "
                f"{block['union_numerator']} of {block['union_denominator']} arrangements pack some class."
            ),
            "do_not_claim": "A block that is rare only when the other rare cells are ignored is not a reading.",
        },
        {
            "id": "digraph-variety",
            "kind": "comparison",
            "tags": ["digraph", "exercise"],
            "statement": (
                f"The solved exercise has {digraph['control_repeated_digraphs']} digraphs that repeat. "
                f"{digraph['control_repeated_as_high']} of {digraph['draws']} shuffles have that many. "
                f"With the most common digraph included, "
                f"{digraph['control_either_as_high']} of {digraph['draws']} match. "
                f"The challenge has {digraph['repeated_digraphs']} repeated digraphs, "
                f"and {digraph['repeated_as_high']} of {digraph['draws']} shuffles do as well."
            ),
            "do_not_claim": "A repeat count that fails once a second count is included is not a reading.",
        },
        {
            "id": "three-cell-habit",
            "kind": "comparison",
            "tags": ["trigram", "exercise"],
            "statement": (
                f"The solved exercise has {trigram['control_repeated_trigrams']} three-cell sequences that repeat. "
                f"{trigram['control_trigrams_as_high']} of {trigram['draws']} shuffles have that many. "
                f"Four cells in a row do not repeat, and {trigram['control_tetragrams_as_few']} of {trigram['draws']} shuffles also have none. "
                f"The challenge has {trigram['repeated_trigrams']} repeated three-cell sequences, "
                f"and {trigram['trigrams_as_high']} of {trigram['draws']} shuffles do as well."
            ),
            "do_not_claim": "A three-cell habit in the solved exercise is not a reading of the challenge.",
        },
        {
            "id": "monotone-row",
            "kind": "comparison",
            "tags": ["square", "monotone"],
            "statement": (
                "One row of the square has counts "
                + ", ".join(str(count) for count in monotone["strict_row"])
                + ". "
                f"{monotone['rows_with_one']} of {monotone['draws']} re-pairings have a strict row. "
                f"If a column may be the line instead, "
                f"{monotone['either_with_one']} of {monotone['draws']} re-pairings have a strict line."
            ),
            "do_not_claim": "A staircase that fails once columns are allowed is not a reading.",
        },
        {
            "id": "unit-straight",
            "kind": "comparison",
            "tags": ["square", "straight"],
            "statement": (
                "Four successive counts differ by one in the row "
                + ", ".join(str(count) for count in straight["strict_row"])
                + ". "
                f"{straight['either_as_long']} of {straight['draws']} re-pairings have a straight that long, "
                f"including columns. "
                f"The solved exercise has one too, and {straight['control_rows_as_long']} of {straight['draws']} of its re-pairings do."
            ),
            "do_not_claim": "A run of counts that differ by one is not a reading.",
        },
        {
            "id": "diagonal-holes",
            "kind": "comparison",
            "tags": ["square", "diagonal"],
            "statement": (
                f"The main diagonal has {diagonal['main_zeros']} empty cells and the other has {diagonal['anti_zeros']}. "
                f"{diagonal['either_zeros_as_many']} of {diagonal['draws']} re-pairings have a diagonal with at least that many. "
                f"The sums of the diagonals do not clear the bar: {diagonal['sum_either']} of {diagonal['draws']}. "
                f"The solved exercise has the same empty-cell counts, "
                f"and {diagonal['control_either_zeros_as_many']} of {diagonal['draws']} of its re-pairings do."
            ),
            "do_not_claim": "Empty cells on a diagonal are not a reading.",
        },
        {
            "id": "heavy-row",
            "kind": "comparison",
            "tags": ["square", "margins"],
            "statement": (
                f"The fullest row that still has an empty cell has {heavy['row_full']} entries. "
                "That chance is rarer than 1 in 37005. "
                f"The fullest column that still has an empty cell has {heavy['column_full']} entries, "
                "and that chance is 76.7 percent. "
                f"The solved exercise's fullest such row has {heavy['control_row_full']} entries, "
                "and that chance is under 1 percent."
            ),
            "do_not_claim": "A full row with an empty cell is not a reading.",
        },
        {
            "id": "uneven-line",
            "kind": "comparison",
            "tags": ["square", "spread"],
            "statement": (
                "The solved exercise's most uneven line stays rare when columns count: "
                f"{spread['control_either_as_uneven']} of {spread['draws']}. "
                f"The challenge's most uneven row is {spread['row_line']}, "
                f"and {spread['rows_as_uneven']} of {spread['draws']} re-pairings match that row. "
                f"With its column included, {spread['either_as_uneven']} of {spread['draws']} match."
            ),
            "do_not_claim": "An uneven row is not a reading of the challenge.",
        },
        {
            "id": "pinned-order",
            "kind": "comparison",
            "tags": ["order", "swarm"],
            "statement": (
                "Cells that appear at most three times stay in their seats. "
                "Seven order scores were taken on the rest. "
                f"The closest is {residual['best_name']}, {residual['best_tail']} of {residual['draws']}. "
                f"The same trigram score on the solved exercise is {residual['control_trigram_high']} of {residual['draws']}."
            ),
            "do_not_claim": "An ordinary leftover order is not a reading.",
        },
        {
            "id": "sharp-cell",
            "kind": "comparison",
            "tags": ["square", "pairing"],
            "statement": (
                f"The sharpest of the 25 cells is {sharp['cell']}, with {sharp['observed']} "
                "where the digit totals expect about 3. "
                f"None of {sharp['draws']} re-pairings has a cell that far out. "
                f"The solved exercise's sharpest cell is matched by {sharp['control_as_sharp']} of {sharp['draws']}."
            ),
            "do_not_claim": "The sharpest cell is not a reading.",
        },
        {
            "id": "leftover-mismatch",
            "kind": "comparison",
            "tags": ["square", "pairing"],
            "statement": (
                f"After the sharpest cell is set aside, {rest['rest']} remains. "
                f"None of {rest['draws']} re-pairings reach it. "
                f"The solved exercise keeps {rest['control_rest']}, "
                f"and {rest['control_as_large']} of {rest['draws']} reach that."
            ),
            "do_not_claim": "A leftover mismatch is not a reading.",
        },
        {
            "id": "bob-on-the-exercise",
            "kind": "comparison",
            "tags": ["bob", "order"],
            "statement": (
                f"Bob calls the solved exercise {exercise['exercise_family']}, "
                f"and {exercise['exercise_shuffles_same_family']} of {exercise['draws']} shuffles agree. "
                f"He calls the challenge {caution['challenge_family']}, "
                f"and {caution['challenge_shuffles_same_family']} of {caution['draws']} shuffles agree."
            ),
            "do_not_claim": "A family name is not a reading of the challenge.",
        },
        {
            "id": "aligned-triples",
            "kind": "comparison",
            "tags": ["order", "grid"],
            "statement": (
                f"Two runs of three identical cells start in column {triples['columns'][0]}. "
                f"The cells are {triples['cells'][0]} and {triples['cells'][1]}. "
                f"{triples['as_aligned']} of {triples['draws']} shuffles put two such runs in one starting column."
            ),
            "do_not_claim": "Two runs in one column band are not a reading.",
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
