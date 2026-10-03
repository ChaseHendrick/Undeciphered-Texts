# Cartographer: layout-focused search

`engine.solvers.persona_cartographer.investigate_cartographer` explores rail
paths, rectangular routes, limited single/double columnar transforms and
Redefence row orders. It reuses the [existing portfolio](transposition-ensemble.md)
with a wider default rectangle limit of 32, leaving letter values unchanged.
This is a repository search policy, not a new historical cipher algorithm.

Every retained candidate satisfies caller cribs and re-encrypts to the original
normalized ciphertext. Equivalent keys remain bounded witnesses, not extra
evidence or an identified historical family. English quadgrams rank candidates.
No score proves correctness. The report keeps the underlying portfolio ledger,
per-family check counts and incomplete status.

```sh
.venv/bin/python -m engine run cartographer "IIWRILCPECLFDHVAEIR" --params '{"cribs":[{"offset":0,"plaintext":"CIVIL"}],"max_width":32}'
```

ASCII input is limited to 4 through 512 normalized letters and 4,096 raw
characters. Widths are 2 through 32, maximum rail counts 3 through 7, work
0 through 100,000 checks, retained candidates 1 through 100. A completed
search covers these finite transforms only. Arbitrary keyed column orders,
irregular routes, nulls and extra encryption layers remain outside it.

Tests first failed on the missing API, then recovered a frozen blind synthetic
control and the published K3 example under declared widths with a six-letter
crib and no supplied widths/key. K3 is already solved; that test is a known
control. The [certificate](../engine/data/persona_cartographer_solver_certificate.json)
hashes actual recovered output from the shared synthetic harbor fixture.
Sharing that fixture with other modes does not make their agreement independent.

`claimed_plaintext` remains null. Historical verification uses separate evidence
and the case workflow. No K4, unknown script or Nr. 86 solution is claimed.
