# Cross-repository learning audit, 2026-10-03

This audit inspected public first-party code from ChaseHendrick's GitHub repositories. It implements a useful Fins-inspired budget policy in the existing cipher engine. It does not transfer game weights, change Bob's family classifier, train on historical guesses, or claim improved classification or decipherment accuracy.

## Verified Fins source

Live `main` was `a1739af33b3da1bb6609fbd8bcaaaa67eba12e21`, confirmed with `git ls-remote` and fetched by its immutable commit. The two supplied local checkouts were older: `b576dcb904e5dd41f599df2ff97cf2df652573e3` and `0c2dc7957710a6972378a7c1354e52bc335d86b6`. Neither local checkout was changed. No `AGENTS.md` appeared in the current Fins tree or local checkout ancestors.

The maintained [neural module](https://github.com/ChaseHendrick/Fins/blob/a1739af33b3da1bb6609fbd8bcaaaa67eba12e21/src/layers/nn.js) contains actual numeric forward passes and updates:

- The difficulty director uses three residual multilayer perceptrons with nine inputs, hidden widths 48 and 32, and two outputs. Its implementation includes GELU, Huber gradients, AdamW updates, bounded replay and ensemble disagreement.
- Fish code includes recurrent gates, eligibility-based weight updates and temporal-difference value/replay updates. These are game policies; their rewards are not cryptanalytic evidence.
- The director compares its error with the error from retaining the previous skill value. Its blend is gated by relative error improvement and observation count. No bandit or tournament solver selector was identified in this module.
- The [live layer](https://github.com/ChaseHendrick/Fins/blob/a1739af33b3da1bb6609fbd8bcaaaa67eba12e21/src/layers/live.js) contains a seeded linear congruential generator. The new scheduler uses deterministic integer apportionment and does not need random exploration.

Source SHA-256 for `src/layers/nn.js`: `2d1f13b6b04d5c8f9de68492641d4521e2e5c344405873be4ab61e7dcbba3b04`.

The actual [Fins license](https://github.com/ChaseHendrick/Fins/blob/a1739af33b3da1bb6609fbd8bcaaaa67eba12e21/LICENSE) is PolyForm Small Business 1.0.0, not MIT. Its existing required notice identifies Copyright Chaos and the former SharpMeow/Fins URL. This audit reports the source's notice; it does not assign that identity to new work. The Python scheduler is an independent implementation of the inspected policy mathematics, with no copied Fins source or weights.

## Implemented policy

[solver_scheduler.py](../engine/solver_scheduler.py) exposes:

```python
allocate_solver_budget(
    strategies, *, max_checks=5000, adaptive_profile=None,
    minimum_exploration=1, ciphertext_sha256=None,
)
baseline_relative_gate(error, baseline_error, samples)
```

The gate uses `lift = clamp(1 - error / baseline_error, 0, 1)`, capped lift scaled by `0.16`, and maturity capped at `samples / 18`. A negligible baseline error gives zero lift. These policy constants match the inspected director. The scheduler uses exact same-case reference error rates rather than Fins' moving averages, and uses no game-state inputs or moods. `adaptation_strength` is a budget blend weight, not a probability that the current answer is correct.

The strongest prior accuracy improvement gets additional budget. Check efficiency breaks accuracy ties among those improved strategies; fast wrong answers cannot win. Every selected strategy retains a minimum allocation when the budget permits. Remaining checks use exact rational largest-remainder apportionment, with caller strategy order breaking exact ties. Allocations always sum to the supplied integer budget. Small budgets use a balanced fallback and explicitly report that minimum exploration is infeasible.

Check fractions measure strategy-specific work units, not measured wall-clock speed. Comparing real speed requires a separate timed benchmark under the same machine and input conditions.

Without a profile the allocation stays uniform. A perfect or dominating baseline also prevents adaptation. The report includes metrics, fallback reason, profile digest and current-case exclusion count. It never claims plaintext or current correctness. The profile's independent-evidence flag is a caller attestation, not an external signature or an automatic verifier.

## Evidence profile contract

The profile has exactly `format_version: 1`, `baseline_name`, and `cases`. Each calibration record has:

```json
{
  "case_id": "independent-control-id",
  "ciphertext_sha256": "64 hexadecimal digits",
  "reference_sha256": "64 hexadecimal digits",
  "evidence_id": "reference source or independent verification record",
  "partition": "calibration",
  "independently_verified": true,
  "evaluation_budget": 5000,
  "baseline": {"correct": false, "checks": 5000},
  "outcomes": {
    "normal-man": {"correct": true, "checks": 24},
    "hallucinogens": {"correct": false, "checks": 5000}
  }
}
```

This is a shape example, not measured evidence; replace placeholder hashes and outcomes. Hash ciphertext and reference plaintext as normalized uppercase A-Z letters, matching council coordinates. Every selected strategy needs an outcome on every retained case under the same evaluation cap as the baseline. The scheduler requires the current ciphertext hash and excludes a matching prior case. It rejects duplicate case IDs/ciphertexts, unknown correctness, missing measurements, fitting/final partitions, unverified flags, unsupported fields, nonfinite values and out-of-budget counts. At most 512 cases, 32 strategies and 100000 total allocated checks are accepted.

Only independently checked calibration data may tune allocation. Withheld final cases remain outside the profile. A rejected hypothesis for an unresolved cipher supplies no known correctness label. Re-encryption, family agreement, English scores and fitting cribs cannot establish successful feedback. Keep independent reference material in the verification stage.

## Council integration

The existing council accepts the optional profile directly:

```python
from engine.persona_solvers import investigate_personas

# profile is a validated calibration profile, not the placeholder shape above.
report = investigate_personas(
    "KHOORZRUOG", personas=("normal-man", "hallucinogens"),
    max_checks=100, adaptive_profile=profile,
)
initial_plan = report["budget_schedule"]["allocations"]
realized_work = report["actions"]
```

The council hashes its normalized ciphertext and passes that hash to the scheduler. `budget_schedule` records the initial plan, which sums exactly to `max_checks`. The council redistributes unused earlier allocations across later policies. Consequently, `actions[*].allocated_checks` records the realized allocation, while `actions[*].executed_checks` and the report's `checks` record actual work. Adding realized allocations can count reused budget twice; actual executed checks remain within the global cap. Prior outcomes affect allocation only and do not enter plaintext fitting. Omitting `adaptive_profile` preserves the council's existing default allocation path and does not import the scheduler.

## Other public code inspected

| Repository and immutable source | Concrete finding | Reuse decision |
| --- | --- | --- |
| [GENChase `6dbecf5`](https://github.com/ChaseHendrick/GENChase/blob/6dbecf518e7de18a634698d7ee1dec69851ea424/tools/science-harness.js), Apache-2.0 | Its harness executes maintained calculations and hashes their exact source. The inspected [neural field](https://github.com/ChaseHendrick/GENChase/blob/6dbecf518e7de18a634698d7ee1dec69851ea424/src/modules/neural-field.js) is a cortical differential-equation simulation. | Useful provenance practice; those neural-field states are not trained decipherer weights. No code copied. |
| [ThermalPilot `46f7172`](https://github.com/ChaseHendrick/ThermalPilot/blob/46f7172aafbe3456d3367aa3654183d02750699a/Sources/ThermalCore/FanPolicy.swift), MIT with Commons Clause | Explicit finite bounds, nullable sensor state and deterministic control curves. | Useful validation pattern; inspected fan policy has no learned classifier. No code copied. |
| [Haywire `e4061b7`](https://github.com/ChaseHendrick/Haywire/blob/e4061b7a5cf1be2336bc0a42a2141a5976717974/engine.js), MIT | Inspected game engine implements simulation and state transitions. | No relevant learned cipher policy identified in that file. No code copied. |
| [TinyLaps `787965c`](https://github.com/ChaseHendrick/TinyLaps/blob/787965cb2dc12d44382677640040318a648c5b55/race.js) | Inspected race logic uses driver profiles and deterministic physics/control rules. No standalone license file was listed in its fetched tree. | Driver personality is not evidence of neural learning. No code copied. |

These findings cover the named files, not every function across these repositories. Relevant GENChase/TinyLaps agent instructions were read; neither repository was changed.

## Actual checks and limits

Executing current Fins `nn.js` in a bounded Node VM passed its finite-output self-check. A controlled director call gave error `0.1472`, baseline error `0.1952`, lift about `0.2459016393`, and one-observation strength `1/18`; the fresh-state strength was zero. This verifies the inspected mathematics, not long-term game learning quality.

The new regression first failed with `ModuleNotFoundError` before implementation. Then:

```sh
.venv/bin/python -m unittest tests.test_solver_scheduler
```

passed 13 focused tests. Controls cover baseline dominance, maturity, correctness before speed, equivalent winners, exact and small budgets, exploration, current-case exclusion, unknown/fitting/final feedback, duplicate evidence, provenance, finite bounds, deterministic serialization and unchanged input records. These are policy controls. No classifier benchmark, solver-speed benchmark, training, deployment or new historical solve was performed by this audit.

The scheduler plus council integration/audit command also passed 24 tests:

```sh
.venv/bin/python -m unittest tests.test_solver_scheduler tests.test_persona_adaptive_schedule tests.test_persona_council tests.test_persona_council_audit
```

A real backend adapter smoke on `KHOORZRUOG` used constructed policy-control records, not measured training feedback. Its initial plan was `37/32/31` checks for Normal Man/Hallucinogens/Mechanic. Realized allocations were `37/35/33` after redistribution; actual work was `32/35/0`, or 67 of 100 checks. Current correctness remained unknown. This checks integration and bookkeeping, not adaptive performance.

# Outside cipher projects, 2026-10-06

Public cipher projects were searched for parts this engine could adopt. Licences decide what may be ported: this repository is MIT, so MIT or Apache code may be adapted with attribution, while GPL code is used for ideas only and reimplemented. Nothing below was run here; only Colossus and dagapeyeff-cipher-solver were cloned and read.

| Project | Licence | What it has | Use here |
| --- | --- | --- | --- |
| [stblake/colossus](https://github.com/stblake/colossus), commit `68d45e0` | MIT | C solvers for about 60 classical types; slippery shotgun hill climbing with backtracking to the best state; a two-square solver annealing both keyed squares with cell, row and column moves; a Nihilist-substitution solver that rewards the share of legal coordinates to decouple the additive key from the square; ACA-convention generators for every type | The two-square move set was adapted for `engine/dagapeyeff_keyedsquares.c` (credited in its header). The Nihilist validity trick and the generators are candidates for later work and for Bob's training families. Its turning-grille solver is a pure transposition with no letter key, so it does not address the open grille problem. |
| [ajejfiejof/dagapeyeff-cipher-solver](https://github.com/ajejfiejof/dagapeyeff-cipher-solver), commit `2009392` | AGPL-3.0 | Polybius statistics, a 14 by 14 split, a Kerckhoffs keyword scan | Nothing to adopt; its index-of-coincidence argument is answered in the D'Agapeyeff manuscript. |
| [doranchak/azdecrypt](https://github.com/doranchak/azdecrypt) | see its repository | Fast homophonic and periodic-transposition hill climbing; scores n-gram sums weighted by entropy | Entropy weighting is an alternative to the letter cap used in `engine.dagapeyeff_homophone`; ideas only until its licence is checked. |
| [arielb57/homophone](https://github.com/arielb57/homophone) | see its repository | A Rust homophonic solver that measures how much ciphertext it needs before its answers can be trusted | The same idea as this repository's planted-text power checks; worth comparing thresholds. |
| [beldenge/zenith](https://github.com/beldenge/zenith) | GPL-3.0 | Homophonic solver with simulated annealing and a web interface | Ideas only. |
| [notPlancha/ciphersleuth](https://github.com/notPlancha/ciphersleuth) | see its repository | Identifies the cipher family from statistics, then breaks it; standard-library Python | A comparison point for Bob, the family router. |
| [matthewdgreen/decipher](https://github.com/matthewdgreen/decipher) | see its repository | Composite pipelines of substitution, polyalphabetic and transposition stages, with grille masks | Composite pipelines are the shape of the open D'Agapeyeff families; worth reading before a joint grille method. |
| [CrypTool 2](https://github.com/cryptool-org) | Apache-2.0 | Lasry's analyzers (columnar, Playfair, double transposition) | Reference implementations for divide-and-conquer double transposition. |

Not a reading of any cipher.
