# Quality standard

## Claims

| Kind of claim | Required |
| --- | --- |
| Historical / archaeological / cryptographic fact | Source URL in the same doc (or `docs/sources.md` with an in-doc pointer) |
| “Closest to cracking” or similar ranking | Explicit criteria + sources; no vibes-only lists |
| Script is readable | Clarify whether *script* or *language* is understood |
| Engine recovered plaintext | Known-plaintext test or demo run that matches fixtures |
| Untested idea | Mark as hypothesis; prefer `docs/logs/` |

## Engine

- Runtime: Python 3.10+, **stdlib only** for solvers / tests / demo.
- `python -m unittest discover -s tests` must pass.
- `python -m engine demo` must rewrite `DEMO.md` with recovered PT matching fixtures.
- Passing tests means recovery of **classical** ciphers in this set only, not modern crypto, not ancient scripts.

## Docs

- Landscape and starter projects stay sourced and conservative.
- Vesuvius Challenge / ink recovery is **not** unknown-script decipherment (known Greek).
- AI-assisted historical cryptanalysis examples belong in `docs/ai-already-helped.md` with citations; they do not license fake script solutions.

## Novelty labels

Use the vocabulary in [`NOVELTY.md`](NOVELTY.md). Rankings in `closest.md` must not promote **Untested idea** entries from logs.

## Binaries

- Prefer SVG for simple heroes when git auth is unavailable.
- JPEG/PNG must be real binary blobs (`FF D8 FF` / `89 50 4E 47`). Never commit base64-as-text “images.”
