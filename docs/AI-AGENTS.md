# Guidelines for AI agents (and humans editing with AI)

This repository mixes **sourced research notes** about undeciphered scripts / open historical ciphers with a **tested classical cipher engine**. Agents must keep those layers separate.

## Hard rules

1. **Cite real URLs** for historical claims. Prefer museum, archive, peer-reviewed, or well-known project pages. Do not invent links.
2. **Do not invent decipherments.** Never present an unknown-script “solution,” Linear A / Indus / Rongorongo / Voynich “reading,” or similar as fact.
3. **Unknown-script output is hypothesis only.** If you explore mappings or models, label them clearly as untested hypotheses and keep them out of landscape / closest rankings unless sourced.
4. **Script vs language.** Distinguish “signs can be transcribed” from “language is understood.” Etruscan and Meroitic are not “fully cracked languages” just because signs are readable.
5. **Solvers need known-plaintext tests.** An unknown-key search must recover fixture ciphertext without being given the key. A supplied-key helper must match a published vector and be labeled supplied-key. Add a failing-then-passing test in `tests/` and a certificate that hashes recovered output. Never describe supplied-key decryption as unknown-key recovery.
6. **Research logs ≠ claims.** Dated notes go in `docs/logs/YYYY-MM-DD.md`. Do not promote log speculation into `docs/landscape.md` / `docs/closest.md` without sources.
7. **Do not commit broken binaries.** Image uploads via some MCP GitHub tools can corrupt JPEG/PNG (base64 stored as text). Prefer `git add` of binary blobs. Verify magic bytes after push (`FF D8 FF` for JPEG).
8. **One engine.** Do not publish two competing cipher engines. Extend `engine/` here.
9. **Honesty in README and DEMO.md.** `DEMO.md` must be produced by `python -m engine demo`, not hand-written as if it were a run.

## Quality bar

See [`docs/QUALITY.md`](QUALITY.md) and [`docs/NOVELTY.md`](NOVELTY.md). Link any new historical ranking or “closest to cracking” claim to sources; otherwise omit the ranking.

## Allowed work

- Improve docs with citations.
- Add classical solvers + fixtures + tests.
- When someone brings a ciphertext, use `.claude/skills/unsolved-attack/SKILL.md`. Run the solvers on their text. Report a plaintext only when a solver prints it. Do not declare a catalogued unread cipher solved.
- Point to external tools (CrypTool 2, CTTS, DECODE/DECRYPT, Crypto Cellar) without vendoring them.
- Summarize published cracks (Copiale, Z340, Enigma challenges, etc.) with links.

## Disallowed work

- Claiming a breakthrough on an undeciphered script or language inside this repo.
- Shipping stub “solvers” that do not recover known plaintext.
