# Substitution with replica exchange

The `substitution-tempering` tool searches an unknown bijective A-Z substitution key using exact incremental quadgram scoring, multiple temperatures and fresh key restarts. It returns the best fitness candidate as a `SolveResult`, with bounded alternatives and a run record. No plaintext, key or crib is supplied to the search. A returned candidate is not automatically a historical solution.

```python
from engine.solvers.substitution_parallel_tempering import solve_substitution_parallel_tempering

result = solve_substitution_parallel_tempering(
    ciphertext,
    seed=20261003,
    restarts=4,
    sweeps=5000,
    max_proposals=2_000_000,
    timeout_seconds=30,
)
print(result.plaintext)
print(result.details["stop_reason"])
```

The public registry tool name is `substitution-tempering`; the Python function is `solve_substitution_parallel_tempering` and its method/internal algorithm identifier is `substitution_parallel_tempering`. The [Dorabella campaign](logs/dorabella-tempering-2026-10-03.md) retains its original internal identifier `substitution-parallel-tempering` in the frozen JSON metadata.

The literal constructed 87-letter certificate fixture also runs through the public CLI:

```sh
.venv/bin/python -m engine run substitution-tempering \
  CEIOPFIFCIKIGCEIKDDOPFGCEIFCEIDCEIKOIFQPOICDOIICEAOCEIKIAFCEIODKFAFMCEIWTIKIPNNKIPGWPFG \
  --params '{"seed":1729,"restarts":4,"sweeps":5000,"max_proposals":180000,"timeout_seconds":20}'
```

This example recovered the certificate plaintext in the actual integration smoke. The output is a JSON envelope whose `result` is a serialized `SolveResult`; `claimed_plaintext` remains null because the tool itself has no independent historical reference.

The search maximizes the existing English quadgram model. Each key swap updates only windows containing changed glyphs. Eight default logical replicas use temperatures `0.25, 0.5, 0.9, 1.5, 2.5, 4, 7, 12`. Adjacent replicas exchange states every 25 sweeps. A sweep makes one swap proposal per replica, and each restart initializes a fresh ladder. Greedy polishing after each restart shares the proposal budget. These are logical replicas in one process; the implementation does not launch threads or processes.

Replica exchange is established methodology, described by [Wang and Swendsen](https://arxiv.org/abs/cond-mat/0407273). For maximizing score, the exchange log ratio is `(1/T_i - 1/T_j)*(S_j - S_i)`. The local sparse-delta implementation is independently written using the standard library. It is distinct from the existing cooled annealing solver, but uses the same default language objective.

The API accepts an optional `logp=` dense list or tuple of `26**4` finite numeric scores, each with absolute value at most `1e100`. This replaces the default objective and is not modified by the solver. The caller must freeze it during search and record its corpus/table provenance. Supplying known target plaintext to fit such a table would invalidate a blind recovery claim. No neural fitting occurs in this solver.

Inputs need 40..4096 ASCII letters and at most 16,384 total characters. Unicode alphabetic symbols are rejected rather than silently treated as Latin. ASCII case and punctuation are restored in `result.plaintext`; scoring and candidate alternatives use the normalized uppercase letter stream.

| Setting | Bounds | Default |
| --- | --- | --- |
| `seed` | Signed 64-bit integer | 20261003 |
| `restarts` | 1..128 | 4 |
| `sweeps` per restart | 1..2,000,000 | 5000 |
| `temperatures` | 2..16 strictly increasing finite values, each 0.01..1000 | Eight-value ladder above |
| `exchange_interval` | 1..100,000 sweeps | 25 |
| `max_proposals` | 1..50,000,000 swaps including polish | 2,000,000 |
| `timeout_seconds` | Greater than zero, at most 180 | 30 |
| `max_candidates` | 1..100 distinct normalized plaintexts | 10 |
| `polish_passes` per restart | 0..32 | 8 |

Booleans are not accepted as integers. Timeout checks are cooperative in small batches; initialization and final rescoring/serialization can add overhead. The exact proposal cap is enforced even inside the greedy polish. `proposals` counts repeated key states again; affected windows, full-score calls and replica exchanges have separate counts.

`result.key` maps plaintext A-Z to cipher letters. `details.decrypt_map` maps cipher A-Z to plaintext. Candidate alternatives retain plaintext, both mapping directions, full objective score and `claimed_plaintext=null`. Alternatives are bounded and deduplicated by normalized plaintext. Unobserved cipher labels can still have arbitrary key values, so a complete permutation does not prove the complete historical key.

`configured_search_complete` means the requested ladders and applicable polish finished. It does not mean exhaustive keyspace search. `stop_reason` is `configured_work_completed`, `proposal_limit` or `time_limit`; `exhaustive_key_search` is always false. A candidate remains unverified until independent reference evidence is checked. Exact forward transformation is consistency evidence, and a high English score is not a correctness probability.

The [certificate](../engine/data/substitution_parallel_tempering_certificate.json) records blind recovery of a literal independently constructed 87-letter control, plus a recovered-output SHA-256. It is a relatively restricted 15-letter inventory. The [focused tests](../tests/test_substitution_parallel_tempering.py) also recover the 496-letter repository fixture and explicitly preserve a same-length courier failure whose wrong answer scores higher than truth. These controls prevent the implementation from presenting optimization quality as general decipherment accuracy.
