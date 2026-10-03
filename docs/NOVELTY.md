# Novelty and claim labels

Every substantive claim in this repository should carry one of these labels (in prose or in a table cell). Do not upgrade a label without a new source.

| Label | Meaning | Allowed locations |
| --- | --- | --- |
| **Sourced fact** | Checkable against a cited URL (museum, archive, peer-reviewed, or project page) | `docs/landscape.md`, `closest.md`, `recent-cracks.md`, `sources.md` |
| **Specialist consensus** | Widely taught status (e.g. Linear B deciphered; Linear A not) with citations | Landscape / closest |
| **Live hypothesis** | A published proposal that is not established (Dravidian Indus, Tyrsenian, etc.) | Landscape / closest — must say *hypothesis* |
| **Contested** | Serious specialists disagree in print | Landscape / closest — summarize both sides + URLs |
| **Engine result** | Known-plaintext recovery from `engine/` with a passing test | `DEMO.md`, test output, README does/does-not |
| **Untested idea** | Speculative note without a cite | **Only** `docs/logs/YYYY-MM-DD.md` — not rankings |
| **Not a decipherment** | Ink recovery, OCR of known Latin, CT unwrapping, etc. | `vesuvius-scrolls.md`, `image-reading.md`, `ai-already-helped.md` |

## Hard bans

- Do not label an unknown-script mapping as **Engine result**.
- Do not present a **Live hypothesis** as solved language.
- Do not invent readings of Voynich, Linear A, Indus, Rongorongo, Phaistos, etc.
- OCR of a generated Latin line is **Not a decipherment** of any manuscript.

See also [`QUALITY.md`](QUALITY.md) and [`AI-AGENTS.md`](AI-AGENTS.md).
