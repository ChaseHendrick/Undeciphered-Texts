# Run-slot score

Unsupervised description of a transcription. New files only: `engine/run_slot_score.py` and `tests/test_run_slot_score.py`. This note does not change solvers, image assets, or other experiments. The README hero JPEG is not part of this change. These files are UTF-8 text — plain Unicode, not base64.

## Original to this repository

The run-slot score is original to this repository. It is not a published decipherment method, not a reimplementation of a named classical attack, and not a reading of an inscription. The formula below was written for this repo so a unit test can show that a planted repeating sign outranks signs that were not planted.

## What it does not do

This tool does not decipher ancient scripts. It is not a decipherment of an ancient script. It does not read Linear A, the Voynich manuscript, Rongorongo, the Indus script, Cypro-Minoan, the Phaistos disc, or any other undeciphered text. It does not name a language. It does not assign phonetic values.

A sign that ranks first has a longer repeated run, a more concentrated start column, or both, in the token spans you supplied. That is a count. It is not a word, a sound, or a translation. The same statistic lights up on a synthetic corpus built so that one invented sign repeats at a fixed column. Structure in a real inscription still needs an edition, a sign list, and an external check before anyone talks about a reading. See [methods.md](methods.md).

## What it computes

Each span is one line or one word. Inside a span, a run is a maximal stretch of the same sign. A run stops at the end of the span. The next span does not continue it.

For each sign that occurs:

- **Repeat length** is the longest of those runs.
- Each run contributes its start index (the column inside its span), once.
- **Peak share** is the fraction of that sign's runs that start in its favorite column.
- **Slot count** is the length of the widest span in the corpus. Every sign is compared with that same grid.
- **Position bias** is 0 when the slot count is less than 2. Otherwise it is

```text
(peak_share - 1/slot_count) / (1 - 1/slot_count)
```

clipped to the range 0 through 1. Bias is 1 when every run starts in one column. Bias is 0 when starts are spread evenly across the grid.

- **Run-slot score** combines the two terms:

```text
repeat_length * (1 + position_bias)
```

Ranking is score descending, then repeat length descending, then position bias descending, then the sign string. Unseen signs are omitted.

A long run locked to one start column outranks a longer run whose starts are uniform, and it outranks a sign that occurs only once. Both terms have to move for that to happen. Repeat length alone would prefer the longer run. Position bias alone would score a one-off sign as perfectly concentrated.

## Synthetic test

`tests/test_run_slot_score.py` builds a corpus of invented labels. On each of twelve lines the sign `RPT` is written four times at column 0. The other four columns are a rotation of `B0` through `B5`. Those background signs are never adjacent to themselves, so their repeat length is 1. The test requires `RPT` to rank strictly above every background sign.

A second check draws a random non-repeating tail for forty lines and repeats that draw on twenty seeds. `RPT` still has to rank first. Labels are not a historical sign list.

Passing that test means the ranker notices a repeating sign that was planted. It does not mean an ancient script was deciphered.

## How to run

```bash
python3 -m unittest tests.test_run_slot_score -v
```
