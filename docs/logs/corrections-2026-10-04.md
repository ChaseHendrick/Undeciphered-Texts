# Corrections an LLM can look up

4 October 2026. No letter string is stored.

Before this note, a wrong claim was only visible if you reread the later log that replaced it. `docs/logs/errors.md` is for crashed commands, not for a claim we withdrew. Subagent notes were not corrections unless a later measurement contradicted them.

The ledger is [engine/data/corrections.json](../../engine/data/corrections.json), schema `corrections-1`. Search it with `engine.corrections.search_corrections`. The query is matched against the id, the tags, the wrong claim, and the correction. A hit is a retracted claim, not a reading.

Append a record when a later measurement contradicts an earlier claim from this repo. Do not edit a record that is already there. Point at the old one from `supersedes`. `solved` stays false. `claimed_plaintext` stays null.

The eight records dated 2026-10-04:

| Id | Wrong claim |
| --- | --- |
| `sorting-is-not-progress` | A higher order score is progress toward a reading. |
| `ioc-cutoff-too-low` | Index of coincidence above 0.06 means language. |
| `private-symbols-are-not-filler` | The five last-column symbols are filler. |
| `period-7-is-the-last-column` | Period 7 is its own key length. |
| `seam-was-double-counted` | The row-end seam is a second pattern. |
| `score-692-has-no-formula` | The score -692.13 converts onto our scale. |
| `repair-04-to-75-is-worse` | Replacing 04 with 75 improves the chi-square. |
| `not-the-lead-on-a-solution` | Beating chi-square 49.23 means we lead a solution. |

No letter string is stored.
