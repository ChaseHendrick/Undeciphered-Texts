# Solver and workflow continuation, 3 October 2026

Started from verified commit `1ce3727dd419c80fd7983f2a81cc0621943633f0`. Added sourced cipher helpers, bounded searches, exact symbolic constraints, case intake and candidate comparisons, local OCR support, puzzle tools, and dated target research. See [HANDOFF.md](../HANDOFF.md) for scope and remaining research paths.

## Executed local checks

- Python 3.12.14 full discovery: 747 tests in 21.360 seconds, exit 0, `OK`, no skips. Optional Z3 and real Tesseract OCR were available.
- Follow-up discovery without Z3, with Pillow, NumPy, and local Tesseract available: 747 tests in 20.800 seconds, exit 0, `OK (skipped=12)`. Those twelve skips are exact symbolic checks.
- Recovery demo to a temporary witness: exit 0, no fixture failures. The existing checked-in witness was preserved.
- Actual case CLI: intake, structure validation, explicit Latin baseline, symbolic candidates, and independent heldout comparison passed. Saved report hashes matched manifests; case status remained unsolved and claimed plaintext remained null.
- Forty independent exhaustive affine/layout comparisons matched symbolic consensus. Peer audits also checked randomized Sudoku, word search, anagram, word-pattern, and Quagmire examples against independent oracles. These are bounded fixture checks, not historical decipherments.
- Optional-dependency absence: synthesis validation and CLI error checks passed with exact SMT tests explicitly skipped; actual case inference saved unavailable, unexecuted, incomplete output.
- Python 3.10 grammar, JSON parsing, Markdown paths, new-text punctuation, and whitespace checks passed. Local runtime execution used 3.12; grammar parsing is not a 3.10 runtime test.
- The existing hero JPEG matched its starting Git blob byte for byte and retained `ff d8 ff` magic. Runtime downloads and raw case directories stayed ignored.

## OCR boundary

Tesseract 5.5.3 recovered the actual generated PNG phrase under the normal execution sandbox. The project-local runtime was extracted from hash-verified official bottles, with no system install. Native Apple Vision compiled but failed inference or timed out here. It remains unvalidated. Neither result establishes accuracy on arbitrary historical manuscript glyphs.

## Research boundary

The [target triage](../target-triage.md) checked current primary pages and records source conflicts. No checked named unresolved target was established as easy. No unknown historical plaintext, script reading, or language identification is claimed.

The [first remote run](https://github.com/ChaseHendrick/Undeciphered-Texts/actions/runs/37099839729) passed the extended Python 3.12 suite and recovery demo. Core Python 3.10 reached test execution but failed because its initial setup omitted Pillow and NumPy, which the existing image and neural tests require. The workflow now installs both in core as well. Inspect the corrected run before claiming a complete CI pass.
