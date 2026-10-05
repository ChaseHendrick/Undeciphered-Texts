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
from engine.dagapeyeff_contact import contact_report
from engine.dagapeyeff_meeting import meeting_report
from engine.dagapeyeff_sandwich import sandwich_report
from engine.dagapeyeff_outside import outside_report
from engine.dagapeyeff_modulo import modulo_report
from engine.dagapeyeff_halves import halves_report
from engine.dagapeyeff_repeat import repeat_report
from engine.dagapeyeff_held import held_report
from engine.dagapeyeff_seats import seats_report
from engine.dagapeyeff_extras import extras_report
from engine.dagapeyeff_heldsand import heldsand_report
from engine.dagapeyeff_heldwait import heldwait_report
from engine.dagapeyeff_quartet import quartet_report
from engine.dagapeyeff_squares import squares_report
from engine.dagapeyeff_twospace import twospace_report
from engine.dagapeyeff_echo import echo_report
from engine.dagapeyeff_ride import ride_report
from engine.dagapeyeff_span import span_report
from engine.dagapeyeff_successive import successive_report
from engine.dagapeyeff_counts import counts_report
from engine.dagapeyeff_tile import tile_report
from engine.bob_pair import bob_pair_report
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
    contact = contact_report()
    meeting = meeting_report()
    sandwich = sandwich_report()
    outside = outside_report()
    modulo = modulo_report()
    halves = halves_report()
    repeat = repeat_report()
    held = held_report()
    seats = seats_report()
    extras = extras_report()
    heldsand = heldsand_report()
    heldwait = heldwait_report()
    quartet = quartet_report()
    squares = squares_report()
    twospace = twospace_report()
    echo = echo_report()
    ride = ride_report()
    span = span_report()
    successive = successive_report()
    counts = counts_report()
    tile = tile_report()
    pair = bob_pair_report()
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
        {
            "id": "aligned-contact",
            "kind": "comparison",
            "tags": ["order", "grid"],
            "statement": (
                "The two runs that share a starting column each sit next to a rare cell. "
                f"The cells after them are {contact['following'][0]} and {contact['following'][1]}. "
                f"Of {contact['draws']} shuffles, {contact['aligned']} already have the alignment, "
                f"and {contact['contact']} of those also sit next to rare cells."
            ),
            "do_not_claim": "Contact with a rare cell is not a reading.",
        },
        {
            "id": "run-meeting",
            "kind": "comparison",
            "tags": ["order", "grid"],
            "statement": (
                f"The most common cell, {meeting['mode']}, repeats down column {meeting['vertical_column']} "
                f"in rows {meeting['vertical_top']}, {meeting['vertical_top'] + 1}, and {meeting['vertical_bottom']}. "
                f"That run meets the run of {meeting['cell']} in row {meeting['row']}. "
                f"A king's move counts. {meeting['as_many']} of {meeting['draws']} shuffles have such a meeting."
            ),
            "do_not_claim": "A meeting of two runs is not a reading.",
        },
        {
            "id": "mode-sandwich",
            "kind": "comparison",
            "tags": ["order", "grid"],
            "statement": (
                f"The most common cell is {sandwich['mode']}. "
                f"Twice, {sandwich['middle']} sits between two of them, both times in a row. "
                f"{sandwich['middle']} is also a run of three. A vertical gap would have counted. "
                f"{sandwich['as_many']} of {sandwich['draws']} shuffles have at least two such gaps."
            ),
            "do_not_claim": "A cell between two copies of another is not a reading.",
        },
        {
            "id": "aligned-spare",
            "kind": "comparison",
            "tags": ["order", "grid"],
            "statement": (
                "Each aligned run of three has two further copies of that cell in the same row. "
                f"The cells are {outside['cells'][0]} and {outside['cells'][1]}. "
                f"Of {outside['draws']} shuffles, {outside['aligned']} already have the alignment, "
                f"and {outside['spare']} of those also have two outside copies in every such row."
            ),
            "do_not_claim": "Copies outside an aligned run are not a reading.",
        },
        {
            "id": "modulo-diagonal-is-ordinary",
            "kind": "negative",
            "tags": ["order", "grid"],
            "statement": (
                f"The {modulo['digit']} digit matches the "
                f"{'column' if modulo['axis'] == 'x' else 'row'} of the grid, modulo 5, "
                f"in {modulo['hits']} cells. That is the best of {modulo['alignments']} alignments. "
                f"{modulo['early_as_high']} of {modulo['early_draws']} shuffles reach it, and "
                f"{modulo['as_high']} of {modulo['draws']} do. "
                f"Scored as whole tables, {modulo['chi_as_high']} of {modulo['chi_draws']} shuffles match. "
                f"The solved exercise is {modulo['control_as_high']} of {modulo['control_draws']}."
            ),
            "do_not_claim": "A diagonal of an ordinary table is not a reading.",
        },
        {
            "id": "even-odd-is-the-private-column",
            "kind": "negative",
            "tags": ["order", "grid"],
            "statement": (
                f"Even positions use {halves['even_support']} symbols and odd positions use "
                f"{halves['odd_support']}. "
                f"{halves['as_high']} of {halves['draws']} shuffles have a gap at least that large. "
                "The five symbols only on the odd side never leave the last column. "
                f"Leave them out and the gap is {halves['residual_gap']}. "
                f"A period of 7 has a gap of {halves['period7_gap']}, "
                f"matched by {halves['period7_as_high']} of {halves['draws']} shuffles. "
                f"Leave the same five out and that gap is {halves['period7_residual_gap']}, "
                f"matched by {halves['period7_residual_as_high']} of {halves['draws']}."
            ),
            "do_not_claim": "An even and odd split is not a reading.",
        },
        {
            "id": "second-run-needs-a-long-run",
            "kind": "negative",
            "tags": ["order", "grid"],
            "statement": (
                "One column holds a run of three and another disjoint run of two of the same cell. "
                f"{repeat['as_high']} of {repeat['draws']} shuffles have at least one such line. "
                "That raw rate is under 5 percent. Every such line already has a long run. "
                f"{repeat['vertical_runs']} shuffles have a vertical run of three, "
                "and the rate inside them is not under 5 percent. "
                f"{repeat['any_long']} shuffles have a long run in either direction, "
                f"and all {repeat['as_high']} of the raw matches sit in that set, "
                "which is also not under 5 percent."
            ),
            "do_not_claim": "A second run beside a long run is not a reading.",
        },
        {
            "id": "aligned-runs-survive-the-pin",
            "kind": "comparison",
            "tags": ["order", "grid"],
            "statement": (
                "The five cells that appear at most three times stay in their seats. "
                f"The other cells are shuffled. Two runs still share a starting column in "
                f"{held['as_aligned']} of {held['draws']} draws. "
                f"A plain count of two runs, aligned or not, is {held['as_many_runs']} of {held['draws']}."
            ),
            "do_not_claim": "Aligned runs with the rare cells held still are not a reading.",
        },
        {
            "id": "rare-seats-still-touch",
            "kind": "comparison",
            "tags": ["order", "grid"],
            "statement": (
                "The rare cells stay in their seats. "
                f"Of {seats['aligned']} shuffles that already have two runs in one starting column, "
                f"{seats['contact']} also have both runs next to a rare cell. "
                f"Of {seats['vertical_runs']} shuffles that already have a vertical run of the common cell, "
                f"{seats['meeting_given_vertical']} also meet a different run. "
                "The contact is under 5 percent. The meeting is not."
            ),
            "do_not_claim": "Contact with the rare seats is not a reading.",
        },
        {
            "id": "two-copies-outside-the-runs",
            "kind": "comparison",
            "tags": ["order", "grid"],
            "statement": (
                "The rare cells stay in their seats. "
                f"Of {extras['aligned']} shuffles that already have two runs in one starting column, "
                f"{extras['at_least_one']} have at least one further copy in the row, "
                f"and {extras['at_least_two']} have two. "
                f"{extras['also_touching']} of those two-copy rows are also the rows that touch a rare cell. "
                "One further copy does not clear. Two do."
            ),
            "do_not_claim": "Two copies outside an aligned run are not a reading.",
        },
        {
            "id": "sandwich-survives-the-pin",
            "kind": "comparison",
            "tags": ["order", "grid"],
            "statement": (
                "The rare cells stay in their seats. "
                f"{heldsand['as_many']} of {heldsand['draws']} draws still have the common cell on both sides "
                f"of a cell that also has a run of three. "
                f"A plain gap, with any other cell in the middle, is {heldsand['plain_as_many']} of {heldsand['draws']}. "
                f"{heldsand['also_aligned']} of the {heldsand['as_many']} also have two aligned runs. "
                "The sandwich stays under 5 percent. The plain gap does not."
            ),
            "do_not_claim": "The sandwich with the rare cells held still is not a reading.",
        },
        {
            "id": "short-wait-needs-the-rare-cells",
            "kind": "comparison",
            "tags": ["order", "grid"],
            "statement": (
                "The rare cells stay in their seats. "
                f"The longest wait for a new cell is {heldwait['wait']}, and {heldwait['as_short']} of "
                f"{heldwait['draws']} draws are that short or shorter. "
                f"Ignore the rare cells and the wait is {heldwait['skip_wait']}, matched by "
                f"{heldwait['skip_as_short']} of {heldwait['draws']}. "
                "The short wait does not survive once the rare cells are left out of the count."
            ),
            "do_not_claim": "The introduction wait with the rare cells held still is not a reading.",
        },
        {
            "id": "four-cells-share-a-count",
            "kind": "comparison",
            "tags": ["order", "grid"],
            "statement": (
                "Four cells share the count 17: "
                + ", ".join(quartet["cells"])
                + f". No row holds more than {quartet['row_most']} of them, "
                f"and no column holds more than {quartet['column_most']}. "
                f"Taking the more even direction, {quartet['as_even']} of {quartet['draws']} scrambles are that even. "
                f"The most common cell reaches that bar in {quartet['mode_as_even']} of {quartet['draws']}, "
                f"and the next four cells in {quartet['next_as_even']} of {quartet['draws']}. "
                "Those two do not clear."
            ),
            "do_not_claim": "Four cells that share a count are not a reading.",
        },
        {
            "id": "tied-cell-color-split",
            "kind": "comparison",
            "tags": ["order", "grid"],
            "statement": (
                "Of the four cells that appear 17 times, "
                f"{squares['cell']} has {squares['even']} copies on the even squares of the grid "
                f"and {squares['odd']} on the odd squares. "
                "A scramble may pick the most uneven of the four. "
                "3.615 percent of 20,000 scrambles match that split. "
                "A straight run alternates the two colors, so the runs do not cause it."
            ),
            "do_not_claim": "A color split of a tied cell is not a reading.",
        },
        {
            "id": "two-spaced-triples",
            "kind": "comparison",
            "tags": ["order", "grid"],
            "statement": (
                f"{twospace['lines'][0]['axis'].capitalize()} {twospace['lines'][0]['index']} holds "
                + " and ".join(
                    f"three copies of {item['cell']}, at seats {item['seats'][0]}, {item['seats'][1]} and {item['seats'][2]}"
                    for item in twospace["lines"][0]["cells"]
                )
                + ". Each triple is equally spaced, and neither is three adjacent cells. "
                f"A scramble may use any row or any column, and any cells. "
                f"{twospace['as_many']} of {twospace['draws']} scrambles have such a line."
            ),
            "do_not_claim": "Two spaced triples in one line are not a reading.",
        },
        {
            "id": "echoed-spaced-triple",
            "kind": "comparison",
            "tags": ["order", "grid"],
            "statement": (
                "Row 11 holds 62 at seats 6, 8 and 10, and row 5 repeats it at seats 6 and 8. "
                "Column 2 holds 82 at seats 0, 6 and 12, and column 7 repeats it at seats 6 and 12. "
                "Neither triple is three adjacent cells. "
                "A scramble may use any cell and any row or column. "
                f"{echo['as_many']} of {echo['draws']} scrambles have two such echoes."
            ),
            "do_not_claim": "An echoed spaced triple is not a reading.",
        },
        {
            "id": "echo-rides-a-triple",
            "kind": "comparison",
            "tags": ["order", "grid"],
            "statement": (
                "Row 11 holds 62 at columns 6, 8 and 10, and row 5 repeats it at two of those columns. "
                "Rows 5 and 11 are also two seats of 85 in column 2, whose three seats are rows 5, 8 and 11. "
                "A scramble may use any cell for either triple. "
                f"{ride['as_many']} of {ride['draws']} scrambles have such a pair of lines."
            ),
            "do_not_claim": "An echo riding on a spaced triple is not a reading.",
        },
        {
            "id": "palindrome-on-a-span",
            "kind": "comparison",
            "tags": ["order", "grid"],
            "statement": (
                "Row 11 holds 62 at columns 6, 8 and 10. "
                "Columns 6 through 10 of row 0 read 91, 64, 81, 64, 91, the same forwards and backwards. "
                "The triple is not three adjacent cells. "
                "A scramble may use any cell and any row or column. "
                f"{span['as_many']} of {span['draws']} scrambles have such a span."
            ),
            "do_not_claim": "A palindrome on a spaced span is not a reading.",
        },
        {
            "id": "successive-singleton-rows",
            "kind": "comparison",
            "tags": ["order", "grid"],
            "statement": (
                "The three cells that appear once are 04, 71 and 94. "
                "They sit in column 13 at rows 6, 7 and 8, which are successive. "
                "Given that those three cells share a column, "
                f"{successive['successive_choices']} of {successive['choices']} choices of rows are successive."
            ),
            "do_not_claim": "Successive rows in the private column are not a reading.",
        },
        {
            "id": "counts-in-order-on-the-square",
            "kind": "comparison",
            "tags": ["order", "grid"],
            "statement": (
                "The only symbol that appears three times is 92. "
                "The only symbol that appears twice is 93. "
                "Three symbols appear once, and 94 is one of them. "
                "On the square, 92, 93 and 94 sit in a row in that order of counts. "
                "A placement may use either order, a row or a column, and a step of one or two. "
                f"{counts['favorable']} of {counts['placements']} placements do that."
            ),
            "do_not_claim": "Counts in order on the square are not a reading.",
        },
        {
            "id": "two-blocks-copy-a-square",
            "kind": "comparison",
            "tags": ["grid", "square"],
            "statement": (
                "Rows 12 and 13 hold two neighboring blocks. "
                "One is 85, 84 over 75, 74. The other is 84, 75 over 74, 85. "
                "Each block is four different cells, and each is the 2 by 2 of the square "
                "on row digits 7 and 8 and column digits 4 and 5. "
                "A shuffle may put such a block anywhere, and the two blocks may be different squares. "
                f"{tile['as_many']} of {tile['draws']} shuffles have two or more."
            ),
            "do_not_claim": "Two blocks that copy a square are not a reading.",
        },
        {
            "id": "bob-side-vote",
            "kind": "comparison",
            "tags": ["router"],
            "statement": (
                "A side vote on six M-209 scores, fit on training keys, would move the 480 from "
                f"{pair['held_before']} to {pair['held_after']} and the older 204 from "
                f"{pair['benchmark_before']} to {pair['benchmark_after']}. "
                "The older bar drops, so the weights stay."
            ),
            "do_not_claim": "A side vote is not a reading, and it does not replace Bob.",
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
