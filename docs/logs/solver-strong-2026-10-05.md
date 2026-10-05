# A larger English model for the solvers, 5 October 2026

The earlier drill found the substitution solver exact on 0 of 6 fresh 200-letter windows, with the default search and with a longer one. The search was not the cause. The English model was.

The legacy model is fit on `engine/data/english.txt`, 8,689 letters. A new model is fit on `engine/data/neural_train_public.txt`, 1,916,398 public-domain letters that already exclude the Doyle, Wells, Grimm and certificate windows. It is a quadgram model with interpolated absolute discounting, discount 0.75. An unseen three-letter context falls back to the two-letter one instead of to a flat 1/26.

The flat fallback matters. A first draft of the larger model used it. A key that turns every context into one never seen then scores exactly log(1/26), -3.258 per letter, and that beats a nearly right key. Twenty random restarts all stopped at -3.258.

`engine.solver_strong` runs the same solver, 10 restarts and 4000 steps, on eight training windows with one fixed permutation, once with each model.

| Letters | Legacy exact | Legacy wrong letters | New exact | New wrong letters |
| --- | --- | --- | --- | --- |
| 200 | 1 of 8 | 194 | 7 of 8 | 1 |
| 150 | 0 of 8 | 533 | 6 of 8 | 63 |
| 100 | 0 of 8 | 475 | 0 of 8 | 131 |

Both models recover the 620-letter substitution certificate. The new model is now what `engine.language.get_model()` returns. `get_legacy_model()` returns the old one, and `solve_substitution(..., model="legacy")` replays it.

Every D'Agapeyeff probe that called the model, and `engine.pooled_substitution`, now names the legacy model, so its recorded numbers replay. Probes that call a solver, such as the solver swarm and the anneal swarm, were frozen under the legacy model and are read from their cache. Deleting one of those cache files would recompute it under the new model.

The fixed-temperature homophonic solver also stays on the legacy model. Under the new model it collapses to frequent letters and recovers its own fixture for 0 of 6 seeds, where the legacy model recovers 2 of 6. A penalty on letter counts raised the legacy model to 5 of 6 on the fixture. On a harder 400-letter Austen fixture with seven doubled letters, the legacy model recovered 0 of 6 at every setting and the new model with the penalty recovered 2 of 6. That trade was not adopted. The solver is unchanged and pinned.

The 1,274 tests that ran before this change were rerun after it. The only new failures were the four probes that replay legacy numbers and the homophonic certificate, and pinning fixed all five. Bob's features use only his own training tables, so his scores do not move.

This is a drill on known training text. It is not a reading.
