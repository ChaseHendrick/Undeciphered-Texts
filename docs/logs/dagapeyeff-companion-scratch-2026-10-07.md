# The companion repository's scratch branch, brought home, 7 October 2026

Not a reading. No letter string is stored.

Before the paper was ever published, a session pushed Latin scratch work to the companion repository,
`ChaseHendrick/dagapeyeff`, on the branch `claude/inspiring-gates-hzi15a` (commit `4e95bdd`). That branch
became the companion's default branch, so the companion showed research scratch instead of the paper. The
companion is now only the paper's published copy (`docs/PUBLISHING-PAPERS.md`), and everything the branch held
lives here.

The branch's tree is kept verbatim in
[`dagapeyeff-companion-scratch-2026-10-07/`](dagapeyeff-companion-scratch-2026-10-07/) as a frozen record. Its
programs are superseded by the engine probes below and are not maintained; its `README.md` is the scratch
write-up as it stood.

| Scratch file | Where it lives now | Note |
| --- | --- | --- |
| `results/latin_small_widths.json` | `engine/data/swarm_cache/dagapeyeff-latinsmall.json`, written by `engine.dagapeyeff_latinsmall` | Identical content |
| `latin/latin_grille.py`, `.c`, `results/latin_grille.json` | `engine.dagapeyeff_latingrille`, `dagapeyeff-latingrille.json` | Rerun as an engine probe; the paper cites the engine run |
| `latin/latin_double.py`, `.c` | `engine.dagapeyeff_latindouble`, `dagapeyeff-latindouble.json` | Same |
| `latin/latin_words.py`, `results/latin_words.json` | `engine.dagapeyeff_latinwords`, `dagapeyeff-latinwords.json` | Same; Figure 3 of the paper |
| `latin/rare_column.py`, `results/rare_column.json` | `engine.dagapeyeff_rarecolumn`, `dagapeyeff-rarecolumn.json` | Same |
| `latin/latin_errors.py`, `results/latin_errors.json` | Not ported | The error-tolerance curve below; the paper uses `dagapeyeff-latinwords` for errors instead |

## The error-tolerance curve (scratch, not cited by the paper)

Planted held-out Latin under a random key had k cells replaced by random symbols, and the keyed-square search
of `engine.dagapeyeff_latin` and the width-7 columnar joint search of `engine.dagapeyeff_latinsmall` were run on
each. Recovery means at least 90 percent of the clean cells right. Seed 20261107, 6 texts a cell of the table.

| Wrong cells (of 196) | Keyed square | Width-7 columnar |
| --- | --- | --- |
| 0 | 6 of 6 | 6 of 6 |
| 8 | 6 of 6 | 5 of 6 |
| 16 | 6 of 6 | 6 of 6 |
| 24 | 5 of 6 | 5 of 6 |
| 32 | 4 of 6 | 3 of 6 |
| 48 | 2 of 6 | 0 of 6 |

The scratch write-up notes that past about 16 wrong cells a recovered text's found score falls to about -3.3
to -4.0 a letter (across both searches the frozen file has -2.76 to -4.11 at 16 and -3.00 to -4.48 at 24, recovered or not), inside the range of the
cells' best scores, so the score alone stops separating heavily mistaken Latin from noise. That is why the
word-coverage test (`engine.dagapeyeff_latinwords`, 2026-10-07) was written, and it is what the paper reports.
This curve was run once, by a script outside the engine, and is recorded here only so nothing from the
companion branch is lost.

Not a reading. No letter string is stored.
