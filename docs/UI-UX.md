# UI / UX notes

This repo is **CLI + Markdown**, not a web app. "UI" here means the command-line surface and how docs present results.

## CLI principles

- **One entry point:** `python -m engine` (see `engine/cli.py`). Prefer subcommands (`demo`, `analyze`, `solve`) over many scripts.
- **Stdout is the product.** Solvers print recovered plaintext, key/shift/period, and short stats. No silent success.
- **Witness files.** `python -m engine demo` rewrites `DEMO.md` so a reader can see ciphertext → recovery without re-running.
- **Fail loudly on mismatch.** Tests and the demo treat exact letter recovery as the bar for classical fixtures.
- **No fake progress UI.** Do not print "deciphering Linear A…" or similar. The engine only claims classical ciphers in its solver set.

## Docs presentation

- README leads with **honest limits** and a **start-here** path (DECODE / Crypto Cellar), not hype.
- Tables for layout and does/does-not; deep material lives under `docs/`.
- Hero art is optional ornament (`docs/assets/readme-hero.svg`). Do not use decorative "glyph" images to imply a real decipherment.
- Research logs (`docs/logs/`) stay visually and semantically separate from landscape / closest claims.

## Accessibility / portability

- Stdlib-only engine: no GUI toolkit, no browser requirement to verify solvers.
- Prefer UTF-8 Markdown; avoid binary docs that MCP/git cannot verify.
- Keep terminal output readable in a plain 80–120 column terminal (no dependency on color for correctness).

## Out of scope

- Studio / canvas UIs (GENChase is a structure reference only).
- Interactive WebCipher playgrounds inside this repo (link out to CrypTool 2 / CTTS instead; see `docs/external.md`).
