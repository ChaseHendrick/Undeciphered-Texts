# Adversary alternative-witness investigator

`investigate_adversary(text, *, cribs=(), candidate=None, max_checks=5000, max_candidates=20)` tests whether a proposed answer has concrete competitors under the same caller evidence. It reuses the existing [bounded investigative ledger](solver-reasoning.md), preserving its explicit affine, crib-model and transposition bounds. Adversary describes a research role, not a preference for contrarian or intentionally wrong answers. Personality flavor does not change math, ranking, evidence or results.

Aligned cribs enter the search as hard constraints. A supplied candidate is normalized and validated against the ciphertext length, then excluded **after** generation. It is never treated as a key or fitted plaintext. Returned alternatives must have passed the ledger's forward encryption and crib checks. English scores order review examples; they do not measure correctness.

```python
from engine.reverse_engineer import Crib
from engine.solvers.persona_adversary import investigate_adversary

report = investigate_adversary(
    ciphertext,
    cribs=(Crib(0, "THE"),),
    candidate=proposed_plaintext,
    max_checks=5000,
    max_candidates=20,
)
```

The shared validator supports 4..512 normalized ASCII letters, at most 4,096 raw characters, up to 128 typed cribs, 0..100,000 checks and 1..100 retained candidates. Candidate text must have the same normalized length and alphabet. Contradictory cribs and unsupported alphanumeric scripts fail before search. Coordinates count zero-based normalized plaintext letters.

With a proposal and nonzero budget, one check is reserved to compare the proposal with the supplied cribs; search receives the remaining budget. The report separates `search_checks` and `proposal_checks`. Proposal exclusion and retained-list deduplication are bounded postprocessing, not additional model trials. The ledger requests one extra witness when storage limits permit, so retaining the proposed answer does not immediately consume the desired alternative slots. Ranking/storage still limit which alternatives are observed.

`proposed_witness_seen` means the ledger actually generated a forward-consistent witness matching the proposal. `ambiguity_observed` requires at least two distinct generated texts under the same evidence, including the proposal if witnessed. A bare caller assertion of a plaintext does not become a second validated model witness. `proposal_contradicted_by_supplied_cribs` records an explicit contradiction with the caller's premises.

Neither zero alternatives nor completion of the declared finite models establishes uniqueness across all ciphers. `exhaustive_all_cipher_uniqueness` stays false. Even concrete alternatives are model witnesses rather than independently authenticated historical readings. The report records search bounds, ledger actions and missing independent evidence; all claimed plaintext and correctness fields remain unverified.

The [certificate](../engine/data/persona_adversary_solver_certificate.json) contains a literal constructed Caesar ciphertext produced with separate modular arithmetic before implementation. No selected key or expected plaintext enters search. It recovers the expected plaintext as a concrete alternative to an all-A proposal and hashes the actual generated candidate. Tests also check normalization, same-evidence fitting, budgets and unavailable optional neural advice. This is a repository-specific composition of established search tools, not a new cipher algorithm, neural class or historical decipherment. See [QUALITY.md](QUALITY.md) and [AI-AGENTS.md](AI-AGENTS.md).
