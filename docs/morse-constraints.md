# Bounded unknown Morse digit maps

`engine/solvers/morse_constraints.py` connects the strict [Morbit](morbit.md) and [Pollux](pollux.md) transformations to supplied lexicons or aligned plaintext evidence. The cipher definitions come from the primary [ACA Morbit sheet](https://www.cryptogram.org/downloads/aca.info/ciphers/Morbit.pdf) and [ACA Pollux sheet](https://www.cryptogram.org/downloads/aca.info/ciphers/Pollux.pdf). The combined enumeration, evidence filters, and bounded ranking are a repository tool. No historical decipherment or priority novelty is claimed.

The caller supplies ciphertext, the families to test, and plaintext evidence. There is no key or digit-map input. Every candidate map is checked against strict Morse character codes, character/word separators, and the chosen evidence. A lexicon requires every complete decoded word to be one of its supplied ASCII entries. Cribs require exact characters at declared decoded-text positions. These are assumptions, not automatically verified facts.

```python
from engine.solvers.morse_constraints import MorseCrib, search_morse_constraints

report = search_morse_constraints(
    "27435 88151 28274 65679 378.",
    families=("morbit",),
    lexicon=("ONCE", "UPON", "A", "TIME"),
    max_maps=400000,
    timeout_seconds=60,
    terminal_period=True,
)
assert report.search_complete
assert any(candidate.plaintext == "ONCE UPON A TIME" for candidate in report.candidates)

partial = search_morse_constraints(
    "08639 34257 02417 68596 30414 56234 90874 5360.",
    families=("pollux",),
    cribs=(MorseCrib(5, "HELPS"),),
    max_maps=10000,
    terminal_period=True,
)
print(partial.stop_reason, partial.candidates)
```

`MorseCrib` offsets count uppercase decoded characters **including recovered word spaces and punctuation**. They differ from the letter-only offsets used by baseline reverse engineering. Crib case becomes uppercase; literal spaces retain their positions. Non-ASCII letters, other whitespace, conflicting overlaps, and out-of-bound coordinates are rejected. A lexicon or at least one crib is required. A candidate fitting these inputs still needs independent heldout evidence and a correct family assumption.

Morbit enumerates all `9! = 362880` ranked digit permutations. Pollux enumerates all `3**10 = 59049` complete digit-to-symbol assignments, including structurally invalid assignments that omit a symbol type; those are counted and rejected. The usual 4/3/3 symbol allocation is not imposed. If a zero digit occurs, Morbit has no viable maps and is excluded with an explicit reason when comparing families. Selecting only Morbit for that input raises a domain error. Both families receive alternating enumeration turns so a partial budget does not silently spend every map on one family.

Reports expose per-family spaces, examined maps, structural rejections, Morse-valid maps, evidence rejections, accepted maps, and completion. `accepted_map_count` is exact on completion and a lower bound otherwise. `map_ambiguity` becomes true after two accepted maps; `plaintext_ambiguity` becomes true after two distinct plaintexts. With an incomplete search and no second witness, either unresolved ambiguity value remains null. Unobserved digits can leave many compatible keys even when the completed search proves one plaintext within the supplied evidence.

Only `max_candidates` ranked witnesses are stored; truncating storage does not end map enumeration or erase an observed ambiguity. With a lexicon, score is the sum of squared decoded word lengths: a disclosed preference for longer dictionary words. With cribs alone, score is zero. Ties follow requested family order and deterministic map order. Scores are not language probabilities or confidence estimates.

`solve_morse_constraints` returns populated `SolveResult.plaintext` only when a completed search proves one plaintext among all accepted maps. The certainty scope remains the tested models and supplied evidence. The report's historical `claimed_plaintext` stays null. `search_morse_constraints` always exposes ranked candidates, including partial searches, without choosing a claimed reading.

Defaults are 10,000 map checks, 20 stored candidates, and a five-second global monotonic time budget. Limits are 512 ciphertext digits, 500,000 map checks, 1,000 stored candidates, 10,000 lexicon words of up to 256 letters, 128 cribs, and 60 seconds. Zero map checks returns an incomplete report. Time is checked before each map; one bounded decode and final bookkeeping can add return overhead. `map_limit` and `time_limit` never prove incompatibility or uniqueness. An exact final map budget can still complete. The standard library is sufficient.

The certificate uses the independently printed ACA Morbit ciphertext and recovered-output SHA-256. Inference receives its explicit four-word lexicon, without the printed keyword or map. This deliberately strong lexicon is a control, not an unrestricted-language attack. Additional tests recover the printed Pollux map from aligned decoded text, distinguish unseen-map ambiguity from plaintext uniqueness, verify exact combinatorial counts, enforce fair budgets, and inject a deadline. Tests first failed before the module existed. Run `.venv/bin/python -m unittest tests.test_morse_constraints -v`.
