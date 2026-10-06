# Zodiac Z13 and Z32: ambiguity, with Z340 as a solved control
<!--
index-id: zodiac
index-title: Zodiac Z13 and Z32
index-problem: Short cryptograms with many compatible readings
index-data: FBI documents and the Z340 solvers' account
index-next: Replay the published Z340 substitution and transposition, with its documented irregularities, against every symbol
-->

Source check: **2026-10-03**. Category: short historical cryptograms. A killer's identity is not inferred here.

<!-- generated-status:start -->
## How close is this to solved?

**Unsolved. Plaintext recovered: 0 percent. 0 of 3 hypothesis families listed (0 percent) are closed with shown power; 3 are open. Reviewed through 2026-10-03.**

**In plain words.** The Zodiac killer sent several ciphers to newspapers in 1969 and 1970. The long 340-symbol cipher was solved in 2020 and confirmed by the FBI. Two short ones, of 13 and 32 symbols, remain unread. They are too short to have a unique answer under simple substitution, so many readings fit. We have not run these yet; the plan is to measure how many readings fit rather than to pick one.

These ciphers are so short that many different readings fit the same symbols. Progress means measuring that ambiguity honestly, not picking a favorite reading. Nothing here names or accuses anyone.

| Status | Families | Share |
| --- | --- | --- |
| Open | 3 | 100 percent |
| Tested without shown power | 0 | 0 percent |
| Closed with shown power | 0 | 0 percent |

### Open (3)

| Family | Evidence |
| --- | --- |
| Z340 reproduced as a solved control | Not yet reproduced here. |
| Z13 under simple substitution | The source reports many compatible readings; not counted here. |
| Z32 under simple substitution, with or without the map as a constraint | 32 symbols with many distinct ones; not counted here. |

Generated from [`zodiac-status.json`](zodiac-status.json) by `tools/refresh_docs.py`.
<!-- generated-status:end -->

Oranchak, Blake and Van Eycke describe their Z340 solution and the FBI's independent verification in 2020. Their discussion labels Z13 and Z32 unresolved and explains their lack of unique recovery under simple substitution assumptions: many compatible readings remain, especially with so many distinct Z32 symbols. This is the status in the cited authors' account, not an assertion that all subsequent proposals were exhaustively inspected. [Primary solution account, sections 5.5 and 8.2](https://arxiv.org/html/2403.17350v1).

The current HTML title page displays 24 August 2026 while its arXiv version label records March 2024. Both observations are recorded rather than guessing a revision history. The source's Z13/Z32 status is therefore quoted with a source boundary and the actual access date.

## Corpus and controls

The [FBI Vault collection](https://vault.fbi.gov/The%20Zodiac%20Killer) is an archival entry point for original case documents, not a transcription supplied by this note. Its collection page was accessible, but individual document PDFs were not newly extracted here. The authors' paper provides cipher figures, referenced case-file locations and methodological context.

Freeze each glyph position, distinct-symbol inventory, original letter/map association and transcription version. Keep Z408 and Z340 in a **solved-controls** category, separate from target inference. Do not use the known Z340 plaintext or a published full key as hidden guesses when claiming unknown-key recovery of another cipher.

## Proposed next experiment, not executed here

1. Reproduce Z340's published full substitution and transposition, including explicitly documented irregularities. Check the forward transform against every cipher symbol. Record this as reproduction of an established solution, not a new solve.
2. For each short target, freeze a finite substitution hypothesis and a caller-supplied candidate lexicon with a source and hash. Cap pattern-compatible candidate or node checks at 10,000 and stored witnesses at 20. Report total compatible witnesses separately from saved examples and disclose any incomplete enumeration.
3. Demonstrate ambiguity with multiple concrete readings consistent with the same evidence. If map measurements or additional letter content are used as constraints, declare their source and uncertainty before ranking. Do not search suspect names and then treat a matching name as independent confirmation.

## Evidence standard

A readable short string is a candidate. Agreement among search policies is still agreement on the same evidence. Establishing a unique historical reading would require external confirming material or a separately supported construction linking these symbols to an authenticated method. A public claim without such evidence does not supersede the source boundary in this note.

The tractable research task is controlled ambiguity analysis and exact solved-control replay. Its output should include alternatives and model limits, without accusing any individual or reporting an unverified location as a recovered fact.

## Next steps

<!-- generated-next:start -->
Open families, in the order they are planned:

1. **Z340 reproduced as a solved control.** Replay the published Z340 substitution and transposition, with its documented irregularities, against every symbol.
2. **Z13 under simple substitution.** Freeze a sourced lexicon with its hash, cap pattern checks at 10,000, and report the total number of compatible readings with several examples.
3. **Z32 under simple substitution, with or without the map as a constraint.** Run the same count, declaring any map-derived constraint and its uncertainty before ranking.

Generated from [`zodiac-status.json`](zodiac-status.json) by `tools/refresh_docs.py`.
<!-- generated-next:end -->
