# Contributing

Thanks for interest in **undeciphered-texts**. Please read [`docs/AI-AGENTS.md`](docs/AI-AGENTS.md) and [`docs/QUALITY.md`](docs/QUALITY.md) first.

## Ground rules

1. **No invented decipherments** of unknown scripts or languages.
2. **Cite URLs** for historical claims.
3. **Classical solvers** need known-plaintext tests (`docs/TESTING.md`).
4. **One engine** — extend `engine/`; do not add a second competing package.
5. **Binaries:** commit real image blobs with git (`FF D8 FF` for JPEG). Do not upload images through tools that store base64 as text.

## Practical workflow

```bash
python -m unittest discover -s tests -v
python -m engine demo
```

- Docs-only PRs: keep landscape / closest conservative and sourced.
- Speculative notes belong in `docs/logs/YYYY-MM-DD.md`, not promoted to rankings without sources.
- UI/CLI expectations: `docs/UI-UX.md`.

## Scope that fits

- Better classical cryptanalysis (fixtures + tests).
- Clearer sourced research notes and external pointers.
- Doc / CLI clarity.

## Scope that does not fit

- “I deciphered Voynich / Linear A” commits presented as fact.
- Vendoring large external apps (link to CrypTool 2 / CTTS / DECODE instead).
- Copying domain code from GENChase or JustLetMeRead (layout inspiration only).
