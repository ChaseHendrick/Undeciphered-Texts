# Normal Human Man solver

An ordinary fictional human research persona: try the obvious keys, show the checks, and ask for independent evidence. This is a transparent baseline, not a claim that a person or conscious mind exists inside the engine.

`engine.solvers.persona_normal_man.investigate_normal_man` tests all 26 Caesar shifts and rail-fence heights 2 through 7. Every retained candidate reproduces the ciphertext under its disclosed key and matches supplied aligned cribs. The English score orders candidates; it cannot prove the plaintext. A complete search uses 32 checks, with honest partial reports below that budget.

```sh
python3 -m engine run normal-man KHOORZRUOG --params '{"max_checks":32}'
```

The [certificate](../engine/data/persona_normal_man_solver_certificate.json) records actual recovered hashes on the same frozen synthetic controls used by Emperor. Shared controls do not establish independent evidence or a new historical solve. Input and council limits follow the [persona solver guide](persona-solvers.md).
