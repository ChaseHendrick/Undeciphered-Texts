# Dorabella: larger frozen English corpus, 2026-10-03

**No verified historical reading.** This is an executed conditional search,
with known-answer controls reported as **Engine results**. Its target candidates
are unverified mappings, never a recovered historical plaintext.

The [machine record](dorabella-corpus-2026-10-03.json) preserves every run's
settings, actual work, retained candidates, mappings and source hashes. The
[independent audit](dorabella-corpus-audit-2026-10-03.json) reconstructs the exact
score table and checks 59 top and retained candidate records across 13 runs.
All forward replays and independently recomputed full scores agree.

## Training data fixed before search

The existing conditional quadgram/backoff implementation was fitted once to
1,352,054 ASCII letters from [Jane Austen's Pride and Prejudice](https://www.gutenberg.org/ebooks/1342)
and [Charlotte Brontë's Jane Eyre](https://www.gutenberg.org/ebooks/1260).
Both official listings mark their texts public domain in the USA. Snapshot and
body SHA-256 values are recorded. Gutenberg headers/footers were removed at
their explicit markers; chapter headings remain. Non-ASCII characters were
discarded, including accented letters, without phonetic transliteration.

No reference controls or proposed Dorabella plaintext were used for fitting.
There was no neural training and no change to Bob's weights. The wider corpus
is a separate experimental scorer, not a promoted replacement for the default.

The score table's little-endian float64 SHA-256 is
`b1faefa99148d86e185e6b9b0e110120a8aa5640114a51cbb042c51d4ac8e07b`.
Scores from this table must not be compared numerically with scores from the
smaller default corpus as though they used one common objective.

## Actual searches

All three constructed 87-letter controls and two shuffled null inputs were
searched before Dorabella. Control keys and plaintexts were withheld from the
optimizer. Each null independently shuffles the same 87 glyph labels, retaining
the exact symbol inventory and frequency counts. Eight frozen target seeds
then received one million swap proposals each. Each run used four temperature
ladders, eight temperatures and a polishing allowance sharing the proposal cap.

| Group | Runs | Actual swap proposals | Outcome |
| --- | ---: | ---: | --- |
| Independent 87-letter controls | 3 | 1,500,000 | 84/87, 85/87, 87/87 positions correct |
| Same-count shuffled nulls | 2 | 2,000,000 | English-looking fragments also appear |
| Original Dorabella stream | 8 | 8,000,000 | No verified reading |
| Total | 13 | 11,500,000 | 58.256 seconds of search in this local run |

The global declared ceilings were 12 million proposals and 180 seconds. Every
run stopped at its finite proposal cap before all requested sweeps could finish;
the JSON reports this explicitly. Repeated states are possible. Proposals are
not distinct keys, exhaustive coverage or a correctness percentage.

The two imperfect controls are particularly useful: their wrong candidates
actually score **higher** than their true plaintext, by 3.7225 and 0.2013 log-score
units. More optimization of this same objective cannot fix that ranking. The
third control recovered exactly. This small result establishes neither general
87-letter recovery accuracy nor the language or mechanism of Dorabella.

Best target fitness was -229.1018; the best shuffled null was -244.4324. Their
15.3306 difference is exploratory. Two nulls, unequal run counts and no
historical answer do not establish a significance level or solution confidence.

## Reproduction

Download the plain-text versions linked from the official book pages. The
recorded snapshot hashes must match to reproduce this exact scoring table;
Gutenberg editions can change. Keep snapshots outside the repository.

```sh
python3 tools/dorabella_corpus_campaign.py --austen /path/to/pg1342.txt --bronte /path/to/pg1260.txt --output /tmp/dorabella-corpus.json
python3 tools/audit_dorabella_corpus.py --austen /path/to/pg1342.txt --bronte /path/to/pg1260.txt --report /tmp/dorabella-corpus.json --output /tmp/dorabella-corpus-audit.json
```

The first script preserves the 87 neutral labels from the author-deposited
[Hauer et al. research archive](https://doi.org/10.5281/zenodo.4819086), member
`dorabella-experiments/LanguageIdentification/IsDorabellaEnglish/DorabellaTranscription.txt`.
Uppercasing is bijective and inserts no symbols or word boundaries. Original
transcription SHA-256:
`ed1b7d3391cbe06bc52d023643860a0795624836cb7efe155d0af59e269d5a50`.
Source hashes pin the implementation actually executed even though the initial
Git HEAD predates the new uncommitted modules. The audit is a consistency check;
it supplies no independent historical key or plaintext.

See the [combined campaign](dorabella-force-2026-10-03.md) for the alternate
transcriptions, physical row orders, default-corpus tempering and dictionary
constraints.
