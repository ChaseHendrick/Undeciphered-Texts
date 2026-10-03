# Inheritance clue investigator

`investigate_inheritance` performs bounded classical cipher searches. It uses caller-supplied clues and records unverified hypotheses. The separate legacy `choose` and `covers` functions remain sentence preferences described in [persona-preferences.md](persona-preferences.md); their `fortune`, `heir` and `estate` word list supplies no investigator clues or default keys.

```python
from engine.reverse_engineer import Crib
from engine.solvers.persona_inheritance import investigate_inheritance

report = investigate_inheritance(
    ciphertext,
    cribs=(Crib(0, "THEHEIR"),),
    keywords=("FORTUNE", "CABINET", "ESTATE"),
    max_checks=5000,
    max_candidates=20,
)
```

Cribs use zero-based plaintext positions after ASCII A-Z normalization. Duplicate cribs add no evidence; contradictory overlaps fail validation. The input source is not repaired or transliterated. Unicode letters and digits are rejected. This model deliberately supports Latin letter ciphers, not unknown scripts.

The search shares one check budget in round-robin order across applicable branches:

- **Supplied-lexicon substitution.** Original source word divisions are assumed to survive encryption. Same-length repetition patterns restrict each ciphertext word to the caller's lexicon. Backtracking enforces a bijection and any supplied cribs. One check tests one word assignment; a missing pattern or incompatible crib map can reject this branch during setup. No default dictionary is invented, and spaces are not inferred for an unspaced cryptogram.
- **Supplied keyword guesses.** Ordinary straight-alphabet Vigenere and plaintext autokey each test every supplied keyword. Condi tests each distinct keyed-alphabet guess with alphabet shifts 0 through 25 and initial offsets 0 through 25. Those are guesses in finite bounds, not a selected key supplied as an answer. One complete key/setting trial is one check.
- **Exact plaintext-autokey crib propagation.** Primer lengths 1 through 32, capped by message length, are tested. The recurrence `P[i] + P[i-L] = C[i] mod 26` propagates each crib in both directions along its residue column. One bounded-period propagation is one check. A full candidate is emitted only if every plaintext position is forced and consistent. Partial columns are counted in diagnostics; a language score never fills their unknown seeds.

All retained candidates pass every supplied crib and a forward encryption check. These checks establish model consistency, not independent historical correctness. Candidate fields contain normalized `plaintext`, `family`, a structured `key`, mean quadgram `score`, `forward_consistent`, `crib_match` and `evidence`. A substitution key uses `?` for plaintext alphabet letters absent from the message; those unknown slots are not used to predict the full candidate.

Candidates are ranked by the repository's [language model](../engine/language.py), then deterministic family/text/key order. The retention cap keeps the best examples seen and does not stop other branches. Same-family, same-plaintext examples are deduplicated among retained candidates. The report counts compatible trials, not an exhaustive count of distinct keys or plaintexts. With no clues it performs zero checks and reports `no_clues`; with unfinished work at the budget it reports `check_budget` and `search_complete: false`. Completed branches do not prove that an untested family or missing dictionary word is impossible.

Bounds are 4..512 normalized ciphertext letters, 4,096 raw characters, 128 typed cribs, 0..100,000 checks and 1..100 retained candidates. Lexicons contain at most 512 words, keyword lists at most 128, each word 1..64 ASCII letters, and either supplied list at most16,384 letters. Check units bound search work; word-pattern setup, scoring and per-trial letter operations also take time. Word search stops at the shared budget without unbounded retries.

The [certificate](../engine/data/persona_inheritance_solver_certificate.json) contains five literal constructed controls whose ciphertexts were generated with separate modular arithmetic before this API existed. They cover word-pattern substitution, guessed-key Vigenere, guessed-primer autokey, crib-only autokey and guessed-key Condi. The crib-only fixture fits seven letters and recovers 58 additional letters without being given the primer. Tests hash actual recovered candidates and independently reconstruct encryption. These are useful unknown-selected-key controls within supplied clue bounds, not published historical decipherments. Scores, persona agreement and recovery of constructed controls supply no K4 or Nr. 86 solution claim.

This is a repository-specific composition, not a claim of a newly invented cipher algorithm. Condi's underlying supplied-key behavior follows the [ACA worksheet](https://www.cryptogram.org/downloads/aca.info/ciphers/Condi.pdf); the recurrence is the implemented plaintext-autokey definition. Reports always leave `claimed_plaintext` null, `correctness_known` false and `happiness` null. Independent plaintext/key evidence is required before treating an unknown real text as solved. See [AI-AGENTS.md](AI-AGENTS.md) and [QUALITY.md](QUALITY.md).
