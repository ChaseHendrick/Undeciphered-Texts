# Ten complementary persona solvers

These fictional research personas run bounded search or review policies. Their voices never override cribs, arithmetic or independent references. The separate classifier is **Bob the Neural Net**.

| Persona | Useful role | Evidence needed |
| --- | --- | --- |
| [Emperor](persona-emperor-solver.md) | Systematic classical investigation and factual ledger | Ciphertext and optional aligned cribs |
| [Inheritance](persona-inheritance-solver.md) | Word-pattern, keyword and crib inference | Caller lexicon, keywords or cribs |
| [Hallucinogens](persona-hallucinogens-solver.md) | Finite reverse/rotation and affine compositions | Ciphertext and optional aligned cribs |
| [Pacifist](persona-pacifist-solver.md) | Exact affine consensus without vocabulary preference | Ciphertext and optional aligned cribs |
| [Detective](persona-detective-solver.md) | Place a supplied crib and infer repeated keys | Unplaced crib and repeated-key evidence |
| [Cartographer](persona-cartographer-solver.md) | Explore transposition layouts | Ciphertext and optional aligned cribs |
| [Mechanic](persona-mechanic-solver.md) | Progressive keys, autokey and Hill constraints | Supplied cribs |
| [Normal Human Man](persona-normal-man-solver.md) | Plain Caesar and rail-fence baseline | Ciphertext and optional aligned cribs |
| [Adversary](persona-adversary-solver.md) | Find alternatives consistent with the same evidence | Ciphertext, cribs and optionally a proposal |
| [Skeptic](persona-skeptic-solver.md) | Check readings against reserved evidence | Candidate readings, reserved cribs or reference hash |

Adversary and Skeptic are separate modes. Skeptic's original dry, suspicious narration follows the user's requested fictional style. `voice="plain"` preserves the factual review. Normal Human Man is an ordinary fictional human persona. No mode has subjective feelings or thoughts.

```sh
python3 -m engine run normal-man KHOORZRUOG --params '{"max_checks":32}'
python3 -m engine run inheritance LXFOPVEFRNHR --params '{"keywords":["LEMON","ORANGE"],"cribs":[{"offset":0,"plaintext":"ATTACK"}]}'
python3 -m engine run persona-council LXFOPVEFRNHR --params '{"keywords":["LEMON","ORANGE"],"cribs":[{"offset":0,"plaintext":"ATTACK"}],"max_checks":9000}'
```

Short demonstrations produce compatible candidates without guaranteeing that the highest English score is correct. Certificates hash actual recovered controls within each mode's documented scope.

## Shared council

`engine.persona_solvers.investigate_personas` connects all ten modes under one check budget. `personas` selects a smaller explicit list; only selected modules load. Remaining work is shared and unused budget redistributes. Checks have backend-specific costs rather than a wall-time guarantee.

Candidates merge by normalized plaintext with bounded witnesses and `supporting_personas`. One shared English score replaces incompatible backend score units. Agreement is not independent verification: equivalent transforms, shared language tables and the same supplied crib can explain it.

`cribs` constrain fitting. `verification_cribs` and `expected_plaintext_sha256` are reserved for Skeptic's final review. Fitting and verification positions must be disjoint. Detective's inferred crib placement is also rejected if it overlaps reserved positions. `unplaced_crib` supplies its clue; missing evidence is reported. `lexicon`, `keywords` and `proposed_plaintext` remain explicit caller assumptions.

Skeptic runs last on a frozen shortlist. Rejection never backfills unreviewed candidates. Exhausted review budgets leave explicit unreviewed statuses. An exact caller-reference match establishes agreement with that reference, not historical authenticity.

Reports expose checks, assumptions, actions, contradictions, missing evidence and bounds. Program-generated `thought` summarizes execution. `claimed_plaintext` stays null, `correctness_known` stays false and `happiness` stays null without independent checked evidence. Personality is narration and a declared search policy, never a substitute for correctness.

## Limits and older APIs

Common inputs contain 4 through 512 normalized A-Z letters, at most 4,096 raw characters and 128 aligned cribs. Reports retain at most 100 candidates and use at most 100,000 checks. Digits and unsupported alphabets fail explicitly. Offsets count plaintext letters after removing spaces and punctuation. Every mode has narrower documented model bounds.

Legacy `choose(left, right)` and `covers(text)` remain separate [sentence-preference demonstrations](persona-preferences.md). Their certificates do not certify decryption or add neural training families. Historical verification belongs to the [case workflow](WORKFLOW.md): `--solver-profile council` fits confirmed training evidence only and preserves heldout checks separately. No new historical decipherment is claimed.
