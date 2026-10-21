# Dorabella: a heavier attack, 2026-10-03

**No verified reading was recovered.** The new work substantially increases
search effort, tests different assumptions and adds two working unknown-key
tools. Its candidates remain unverified. Exact forward transformations and
English-looking fragments do not establish Elgar's plaintext.

## Executed branches

| Branch | Target work | What changed | Record |
| --- | --- | --- | --- |
| Original-stream replica exchange | 10 seeds; 10,016,740 key-swap proposals | Several temperatures exchange keys; exact sparse quadgram deltas replace repeated full scoring | [Protocol, controls and candidates](dorabella-tempering-2026-10-03.md) |
| Physical reading orders | 96 baseline runs; 4,080,012 target full-score calls, plus 31 runs with 1,252,175 swap proposals | Two separately sourced transcriptions, each with 16 reversible physical-row layouts | [Source inspection and replay](dorabella-layouts-2026-10-03.md) |
| Larger frozen English scorer | 8 target seeds; 8,000,000 key-swap proposals | Existing language-model algorithm fitted before search to 1,352,054 public-domain letters; three short controls and two same-count shuffled nulls | [Corpus campaign and independent audit](dorabella-corpus-2026-10-03.md) |
| Unknown word boundaries | 5 models; 1,000,000 trie-search nodes in the original campaign | Global substitution bijection plus supplied-vocabulary constraints; separate model removes non-A/I singleton initials | [Dictionary campaign, validation replay and limits](dorabella-word-constraints-2026-10-03.md) |

The three tempering branches made **19,268,915 target swap proposals**.
The baseline layout branch made an additional **4,080,012 target full-score
calls**. These are different work units. Counts include repeated states and
are neither distinct keys nor a percentage of the keyspace. Controls, shuffled
nulls, independent score checks and the word-report validation replay are
recorded separately. Finishing requested heuristic work is not exhaustive
cryptanalysis.

The original-stream, layout and larger-corpus campaigns took 65.139, 61.008
and 58.256 seconds respectively, including their own disclosed controls and
accounting. They ran concurrently on this desktop, so their times should not
be added as though they were one elapsed wall time or a portable speed claim.

## Why the controls matter

**Engine results:** the default tempering objective recovered an independently
constructed 87-letter control and the 496-letter repository fixture exactly.
The dictionary method recovered another independent 87-letter control, including
all word breaks and its observed key, within its separate 28-word vocabulary.
Each has a recovered-output SHA-256 certificate and key-withheld tests.

Failures were kept. The default tempering courier control recovered 79/87
letters. Larger-corpus controls recovered 84/87, 85/87 and 87/87. Only one of
four distinct layout controls recovered exactly; the others recovered 83, 86
and 86 of 87 letters. These small, heterogeneous controls are not a benchmark
accuracy estimate and do not establish that Dorabella is English substitution.

In every imperfect control audited against its reference score, the wrong
candidate scored **above the true plaintext**. This reveals an objective
limitation: more swaps can improve English fitness while moving away from the
correct message. The dictionary branch addresses a different constraint, but
missing vocabulary and finite search limits still prevent an exclusion of
English. Initials extracted from a book can also create trivial segmentations;
those candidates were recorded as diagnostics, not plausible historical readings.

The larger-corpus branch independently shuffled Dorabella twice while preserving
all glyph counts. Those null searches also produced English fragments. Their
small exploratory comparison supplies no p-value or solution probability.

## Transcription and evidence

The [Hauer et al. primary research archive](https://doi.org/10.5281/zenodo.4819086)
supplies the frozen 87-symbol stream with 20 neutral labels. The
[Schmeh primary paper](https://ep.liu.se/ecp/149/026/ecp18149026.pdf) supplies a
different 21-label transcription. Their equality patterns disagree; candidates
were not used to decide which glyphs are authentic. The layout log records
direct inspection of both published facsimiles and their three physical rows.

The current [community challenge workbench](https://decipher.nu/challenges/elgars-dorabella-cipher/workbench)
lists no accepted systematic decipherment. That source describes public status,
not every unpublished proposal. This campaign acquired no independently
authenticated historical plaintext, key or heldout fragment. `claimed_plaintext`
therefore stays null throughout the target records.

Geometry remains an evidence gap. Row lengths can be checked from facsimiles;
the arbitrary Latin transcription labels do not themselves encode arc counts,
orientations, phonetic values or musical pitches. The checked sources did not
provide a verified label-to-geometry table for a further numeric/music attack.

## Connected tools and validation

`python3 -m engine tools` now exposes both new methods through the same
allowlisted invocation gateway:

```sh
python3 -m engine run substitution-tempering CEIOPFIFCIKIGCEIKDDOPFGCEIFCEIDCEIKOIFQPOICDOIICEAOCEIKIAFCEIODKFAFMCEIWTIKIPNNKIPGWPFG --params '{"seed":1729,"restarts":4,"sweeps":5000,"max_proposals":180000,"timeout_seconds":20}'
python3 -m engine run unspaced-substitution DTTZQZZITUQZT --params '{"lexicon":["MEET","AT","THE","GATE"],"max_nodes":10000}'
```

Both commands are executed constructed hidden-key controls. The second yields
`MEET AT THE GATE`. Tempering requires at least 40 ASCII letters.
Larger lexicons and supplied
dense language tables use the documented Python APIs because the JSON adapter
has narrower input limits. See [tempering](../substitution-parallel-tempering.md),
[word constraints](../unspaced-substitution.md) and the [interface](../tool-interface.md).

Independent review checked sparse deltas against full scores, replica exchange
against direct probability algebra, and dictionary search against exhaustive
small mapping/partition oracles. Review caught and corrected a reporting bug:
different plaintexts can share one unique set of word boundaries. Plaintext,
full-parse and boundary-placement ambiguity now have separate counts and tests.
The word campaign's validation replay preserves that correction and its source
provenance; it does not add independent evidence for Dorabella.

Final local validation passed **1,128 tests in 38.067 seconds** with the optional
OCR and symbolic dependencies available. The actual recovery demo regenerated
`DEMO.md` and recovered all three built-in fixtures exactly. Both public CLI
examples above ran successfully. These checks verify the implemented controls
and contracts; they provide no historical plaintext validation.

## Next discriminating work

Further English scoring should first demonstrate reliable recovery on a wider
set of short, independently held-out letters and resist shuffled-input false
positives. Higher-order word context or multiple independent scoring objectives
are possible follow-ups, not implemented claims in this log. A checked glyph
inventory with geometry would enable a genuinely different orientation/music
branch. Independently authenticated related correspondence or plaintext clues
would be more decisive than selecting a pleasing candidate from many searches.

This work adds reproducible algorithms and identifies concrete limits. It does
not establish that a new Dorabella reading is close to acceptance.
