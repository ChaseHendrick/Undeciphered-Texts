# Frozen ARC v1 solver methods

The core consists of `engine/arc/{grid,dsl,solver,__init__}.py` and uses Python 3.10+ standard-library facilities. It adds a bounded grid program search to the existing engine. New files declare MIT-0; they do not change the license of any other repository material.

## Representation and grammar

A grid is an immutable tuple of rectangular integer rows, each side in 1..30, colors in 0..9. Booleans and nonintegral numeric types are rejected. Every intermediate result remains a valid bounded grid or is undefined. An operation that expands beyond 30 cells on either axis returns undefined; subsequent cropping cannot rescue that program. Empty color/background selections and nonexistent components are undefined.

The primitive list is ordered exactly as follows:

1. `identity`, clockwise `rot90`, `rot180`, `rot270`, `flip_rows`, `flip_cols`, `transpose`, `anti_transpose`.
2. Demonstration-fitted color maps, deduplicated and sorted lexicographically by their ten target colors. A map is proposed after each of the eight D4 transforms if all demonstration cells with the same transformed input color have the same output color and all paired shapes agree. Unobserved input colors are explicitly mapped to themselves. This is a grammar assumption, not a fact forced by the examples. Identity maps are omitted.
3. `crop_background` with background 0, then the most frequent color. Frequency ties choose the smallest color value.
4. `component`, with nested parameter order: background `(0, mode)`, monochrome `(True, False)`, selection `(largest, smallest)`. Components use four-neighbor connectivity. Monochrome components cannot cross color boundaries; multicolor components may join different foreground colors. Size ties use lexicographic order of sorted `(row, col)` component coordinates, hence the earliest component. The result is its bounding rectangle with other pixels replaced by the chosen background.
5. `compress` consecutive identical rows, consecutive identical columns, then both (rows first). Nonconsecutive duplicates are preserved.
6. `scale`, `tile`, `repeat_rows`, `repeat_cols`, each with factors 2 then 3. Scale repeats individual cells on both axes; tile repeats the complete grid.
7. `crop_color` for colors 0 through 9. These crops preserve all original pixels within the selected color's bounding rectangle.
8. Single-color `replace`, with old color 0 through 9 and new color 0 through 9, excluding equal pairs.
9. `swap` with first color 0 through 9 and second color strictly greater than the first.

There are 174 fixed primitives and zero to eight fitted color-map primitives. The fitted parameters use demonstration pairs only. No test input or answer is used to fit them.

Programs contain one or two primitives. All single-primitive programs precede all two-primitive programs. Two-step programs exclude identity in either position, then enumerate primitive index pairs by increasing sum of indices, and increasing left index within a sum. Thus a grammar with N primitives contains `N+(N-1)^2` programs. No literal program receives duplicate votes. Algebraically or semantically equivalent programs can remain distinct and can bias syntax counts. This is a stated limitation of voting.

## Search and result semantics

The study's candidate budget is 4,096 programs per task, fixed independently of runtime. Every attempted program consumes one candidate, including programs rejected immediately by a demonstration. Demonstrations are tested in their supplied order, stopping at the first mismatch. Every compatible program is evaluated on every test input. Operations are memoized in an 8,192-entry per-task LRU cache. Search counters distinguish candidate checks, demonstration checks, cache-miss primitive applications and cache hits. Primitive-application counters cover search execution after grammar instantiation, not the initial fitted-color-map construction.

All three policies use the identical candidate stream and compatible set. `first_programs` takes the first two defined compatible-program predictions for each test input and can repeat an output. `first_distinct` takes the first two distinct outputs. `group_vote` ranks distinct output groups by compatible-program count, then shortest representative program, then its lexical canonical JSON serialization. Votes are counts under this grammar, not calibrated probabilities. The last policy supplies the default competition predictions. If fewer than two outputs exist, remaining slots are null. A separate adapter may add a documented legal fallback; the core does not invent a solution for that slot.

Compatible programs whose result is undefined on a test input do not vote for that input. They remain counted and prevent a uniqueness claim. Predictions are grouped separately per test input, while each retained program records its joint vector of output-group IDs across all test inputs.

`unique_within_declared_grammar` requires the complete finite grammar to have been enumerated, at least one consistent program, all consistent programs to be defined on that test input, and a single distinct output. Prefix agreement is `incomplete_agreement`. An exhausted grammar with no compatible programs reports `no_solution_within_declared_grammar`; a truncated search with none reports `unknown`. Neither means that an ARC task has no general solution. Ambiguous results contain a witness: the test input, two demonstration-consistent programs, their differing outputs, and the first differing cell or output shape.

The explicit finite-program-list option is for independent tiny-grammar oracle controls. It deduplicates literal programs before enumeration. The normal benchmark and competition path uses the default grammar. The parser ignores `test.output`, including its value in neither validation nor input hashes.

## Verification before dataset evaluation

Nineteen standard-library unit tests passed. These include literal rectangular D4 answers, recoloring and cropping, explicit object-connectivity/tie controls, expansion limits, actual default search recovering a rotation and a composed crop-plus-rotation, an ambiguity witness with voting/diversity separation, incomplete-versus-complete status, undefined-test hypotheses, duplicate-vote rejection, two-test-input behavior, JSON serialization and input immutability. An independent literal oracle checks all 16 binary 2x2 source grids under a declared four-program grammar. No real evaluation task was used in this verification.

The logical-contract transfer from the cipher engine is limited and explicit: demonstration consistency is separated from correctness, incomplete search stays unknown, and a conditional uniqueness statement is restricted to an exhaustively searched finite hypothesis class. The closest existing implementations are `engine/solvers/hill_inference.py` and `engine/cipher_synthesis.py`. This does not imply that the DSL or voting procedure is novel or generally competitive on ARC.
