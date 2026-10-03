# Plaintext-autokey primer inference

`infer_autokey` accepts ciphertext without a primer. It tests bounded primer lengths, propagates aligned plaintext cribs exactly, selects one language-scored example per compatible length, and verifies each example by re-encryption.

The [Boston University Secret Key Cryptography course](https://cs-people.bu.edu/tromer/SKC2006/) defines an autokey as a secret prefix followed by shifted plaintext. The [University of Rhode Island teaching page](https://cs.uri.edu/cryptography/classical-ciphers/vigenere/article.html) independently prints the single-letter-primer example `EHPFSFEBHMHPF`, plaintext `TOBEORNOTTOBE`, and primer `L`. These primary teaching sources were inspected on 2026-10-03. The implementation targets plaintext autokey with addition modulo26. Ciphertext autokey is a different model.

```python
from engine.reverse_engineer import Crib
from engine.solvers.autokey_inference import infer_autokey

report = infer_autokey(ciphertext, max_period=16, max_candidates=20)
examples = report.candidates

# Coordinates count normalized A-Z letters, excluding spaces and punctuation.
constrained = infer_autokey("EHPFS FEBHM HPF", max_period=1,
                           cribs=[Crib(4, "O")])
assert constrained.candidates[0].plaintext == "TOBEORNOTTOBE"
```

For primer length L, every letter after the primer satisfies `P[i] = C[i] - P[i-L] mod26`. Each residue column consequently has26 possible first plaintext letters. A seed determines the entire column, with its sign alternating at each step. One crib letter fixes that column's seed; incompatible crib letters eliminate the period. The exact compatible-primer count is `26**unresolved_seed_columns` for each compatible period. Counts sum assignments across periods and do not count distinct plaintexts.

Without cribs, column log-unigram scoring selects the global unigram optimum independently in each column. The result then receives a quadgram score for ranking the period examples. This does not optimize quadgrams over the full Cartesian product of column seeds. `ranking_exhaustive` remains false, and retaining one example does not prove uniqueness. Default unigram statistics and quadgrams use the existing `engine/data/english.txt` training corpus; an optional26-entry `log_unigram` vector may replace the seed-selection weights.

`forced_plaintext` reports only letters fixed by the supplied cribs within one period. `consensus_plaintext` agrees across all compatible periods and all their possible seeds, including periods whose examples the output limit omits. Unknown positions remain `?`. `plaintext_unique_within_period_bounds` proves uniqueness only under the supplied plaintext-autokey model, cribs, and primer-length bound. `claimed_plaintext` always remains null. If no period is compatible, the report returns the original crib mask and zero compatible periods, without a uniqueness claim.

The inference accepts4..512 normalized letters and at most8192 raw characters,128 cribs, primer bounds1..128, and output limits1..128. It scans all periods up to the smaller of the requested bound and ciphertext length. The finite workload is at most26 seed checks per residue column and one quadgram evaluation per compatible period. Output truncation affects displayed examples only. Log weights must be finite in -1000..0. ASCII letters normalize to uppercase; Unicode letters are rejected.

The separate `autokey_feature_scores(text, tables, max_period=16)` helper returns one digraph fitness value for every tested length1..max_period. It accepts16..8192 normalized letters and a period bound1..16. `tables["english"]` must contain26 positive probabilities summing to one; `tables["logdig"]` must be a26 by26 finite log table in -1000..0. Both tables must come from the caller's training split. The helper fits and scores trials using only those tables and returns scores without plaintexts or primers. NumPy is imported lazily for faster feature extraction; the standard-library fallback implements the same computation. Core inference requires no optional dependency.

The certificate freezes a423-letter original synthetic paragraph and independently constructed ciphertext. Blind inference receives neither its primer nor plaintext and recovers the exact paragraph with primer `MONDAY` ranked first. Its SHA-256 hashes the recovered ASCII plaintext. Separate tests recover the university's printed13-letter vector from one aligned plaintext letter, check12 independently constructed random crib cases, and compare both feature implementations against a26-seed modular oracle. This validates those controls and result contracts. The method is a new composition in this repository, with no historical solve or priority claim.
