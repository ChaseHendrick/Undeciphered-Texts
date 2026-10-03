# Baconian with explicit extraction

The [ACA Baconian sheet](https://www.cryptogram.org/downloads/aca.info/ciphers/Baconian.pdf) maps each letter to a five-unit a/b code. Its 24-letter alphabet merges I/J and U/V. The sheet gives two textual carriers: one uses each word's initial letter, while the other uses every letter. In both, A-M supplies `a` and N-Z supplies `b`.

```python
from engine.solvers.baconian import solve_baconian

result = solve_baconian(carrier, extraction="word_initials", variant="24")
result = solve_baconian(carrier, extraction="every_letter", variant="24")
result = solve_baconian("baaab baabb aaaba aaaba aabaa baaab baaab", extraction="direct", variant="24")
```

`solve_baconian` requires both settings; there is no hidden automatic extraction or alphabet choice. `baconian_extract(text, extraction=...)`, `baconian_decode(units, variant=...)`, and `baconian_encode(text, variant=...)` expose the steps independently. Codes are interpreted in their supplied order with `a=0`, `b=1`, most significant unit first. Complete five-unit groups are required, and unused codes fail validation.

Extraction rules are explicit:

- `direct`: a/b letters only, case insensitive, with whitespace allowed. A continuous stream must have length divisible by five. When more than one whitespace token is supplied, each must contain exactly five units; a split such as `a aaab` is rejected.
- `word_initials`: one unit from the first ASCII letter in each whitespace-separated token. Leading/trailing punctuation is ignored. Apostrophes and hyphens inside a token do not split it into multiple words. Tokens without ASCII letters are ignored. Commas without whitespace therefore do not create additional word tokens.
- `every_letter`: one unit from every ASCII letter in order; spaces, punctuation, and digits are omitted.

Non-ASCII alphabetic characters are rejected by these textual strategies. Input is limited to 100,000 characters, extracted code to 10,000 units, and decoded output to 2,000 letters. No trailing code fragment is silently discarded. Carrier positions are never interpreted as inferred typography, font weight, image pixels, or hidden visual marks. If a real carrier uses such a channel, transcribe its two classes independently before using direct decoding.

`variant="24"` uses `ABCDEFGHIKLMNOPQRSTUWXYZ`, with I and U as canonical output representatives. It cannot distinguish I from J or U from V. Metadata lists every merged-letter position and its alternatives. Plaintext spaces are not encoded and cannot be recovered; `plaintext_spacing_lost` states that limitation. Carrier words are not plaintext word boundaries.

`variant="26"` is an explicit implementation alternative using ordinary A-Z codes 0 through 25. It retains J and V as separate letters. The ACA examples certify the 24-letter table only; the alternative has synthetic full-alphabet tests and is not attributed to that printed table.

## Independently printed verification

The first source carrier decodes to the printed seven-letter answer `SUCCESS` from 35 word initials. The second decodes to the printed eleven-letter answer `NOWISAGOODT` from 55 carrier letters. The final T is the actual end of that printed example; no continuation is inferred. [The certificate](../engine/data/baconian_certificate.json) records both literal carriers, their a/b streams, exact printed answers, and SHA-256 over uppercase ASCII plaintext bytes. The PDF and table were visually checked on 3 October 2026, and the download hash is recorded.

The wrapper returns `mode: specified_extraction` and an informational score equal to the output letter count. Its result means the supplied transcription fits the caller's chosen binary extraction and alphabet. It does not demonstrate automatic carrier discovery, unknown-key recovery, or historical decipherment. It remains outside ordinary text-only solve dispatch because its convention must be explicit.

```sh
.venv/bin/python -m unittest tests.test_baconian -v
```
