# Skeptic reserved-evidence critic

`investigate_skeptic` separates candidate generation from independent comparison with caller-reserved evidence. Its optional dry suspicious narration uses original quips and a high-level Dale-like demeanor. It uses no dialogue from the show and supplies no paranoia as a premise. `voice="dale"` and `voice="plain"` change only `voice` and `narration`; every answer, check, score, verdict and evidence field is identical, apart from measured ledger elapsed time.

```python
from engine.reverse_engineer import Crib
from engine.solvers.persona_skeptic import investigate_skeptic

report = investigate_skeptic(
    ciphertext,
    cribs=(Crib(0, "THE"),),
    verification_cribs=(Crib(11, "THESEALEDLETTER"),),
    expected_plaintext_sha256=reference_hash,
    max_checks=5000,
    max_candidates=20,
    voice="plain",
)
```

Generation calls the [existing ledger](solver-reasoning.md) with **training cribs only**. Reserved letters and the reference hash never enter its arguments, neural feature tables or ranking. Verification crib positions must be disjoint from training positions; overlap is rejected so fitted evidence cannot masquerade as an independent check. The program trusts the caller's provenance and does not authenticate a reference by matching it.

After generation, one check reviews a full candidate against all bounded reserved positions and an optional SHA-256 over normalized ASCII A-Z plaintext. Before generation, the program reserves up to `max_candidates` checks, capped at half the total budget, and limits returned search witnesses to that capacity. The rest goes to the ledger. A budget smaller than two cannot reserve both a model check and a review; it performs no cryptanalytic key checks. Actual `checks` equals `search_checks + verification_checks` and never exceeds the single supplied cap. Unused reserved capacity is not claimed as executed work.

Each review records one of four verdicts:

- `contradicted`: a reserved letter, declared reference hash or returned forward check disagrees.
- `crib-supported`: reserved letters match and no reference hash was supplied.
- `exact-reference-match`: the computed hash matches the supplied reference and no reserved check contradicts it.
- `unchecked`: no reserved letters or reference hash was supplied.

The common candidate list drops contradicted generated witnesses and preserves the search's original order and scores for the others. All reviews, including rejected texts and specific mismatch coordinates, remain visible in `reviews`. Hash matches and crib support remain conditional on caller-supplied evidence; `correctness_known` stays false, `claimed_plaintext` stays null, and no historical solved state is produced.

For a council or an existing candidate list, pass `candidate_plaintexts=(...)`. This activates **review-only** mode: no search executes, and each explicit normalized text costs one review check. Up to 100 supplied texts are accepted, with duplicates removed. The reviewer has no keys, so `forward_consistent` is null and common `candidates` remains empty. `reviews` supplies the verdicts for council annotation/filtering. An exhausted review budget leaves `unreviewed_candidates` explicit and completion false. The generation storage cap does not truncate an explicit review request.

Inputs use the shared 4..512 normalized ASCII-letter / 4,096 raw-character bounds, up to 128 cribs in either separately validated set, 0..100,000 checks and 1..100 retained generated candidates. Explicit review texts must match the normalized ciphertext length. Reference hashes require 64 hexadecimal characters. Unsupported scripts, malformed hashes, overlapping heldout positions and invalid bounds fail before work. `validation_complete` describes reviews of returned/requested texts, not exhaustive search, authenticated reference provenance or proof that a real cipher is solved.

The [certificate](../engine/data/persona_skeptic_solver_certificate.json) uses an independently constructed literal Caesar ciphertext. Three fitted letters drive search, while fifteen reserved letters and a plaintext hash are compared afterward. Tests hash actual recovered output, prove reserved contents never enter the search call, reject an injected higher-scoring wrong candidate, preserve the true control, exercise review-only mode and optional neural fallback, and compare plain versus flavored narration. This critic is a repository-specific verification strategy, not a separate neural cipher family. See [QUALITY.md](QUALITY.md) and [AI-AGENTS.md](AI-AGENTS.md).
