# Neural router upgrades and measured limits

**Bob the Neural Net** is the residual router. Bob ranks 20 supported cipher families. It does not recover
plaintext or establish the family of an unknown historical message. The saved
format 5 ensemble reaches **428/480 top one**, **477/480 top three** on the fixed
Doyle development cases and **193/204** on the exact earlier benchmark. The
requested 480/480 has not been reached. These are family labels, not 480 solved
historical ciphers.

The Wells audit used previously unused H. G. Wells prose and fresh synthetic
keys after the earlier model selection stage. That saved format 5 model gets **429/480 top one** and
**476/480 top three**. Its model SHA-256 is
`d8c985dfdaf2d1dd0e17cfdb8412d0f947221b3f9e30318169d9183145c5c825`.
The [audit report](../engine/data/neural_router_v2_audit.json),
[source metadata](../engine/data/neural_audit_wells_source.json), and
[extracted corpus](../engine/data/neural_audit_wells.txt) make this replayable.
[Project Gutenberg](https://www.gutenberg.org/ebooks/35) identifies the source
as public domain in the USA. Later authorized training stages excluded Wells
from fitting and selection. The audit remains specific to the hashed format 5
artifact; it is not a globally untouched final audit of all later experiments.
Future tuning against it would make it another development comparison.

## Training and features

Three seeded residual networks use tanh layers, an additive residual connection,
AdamW, cosine learning rates, 0.03 label smoothing and 0.05 dropout. The saved
model has 96 hidden units per network and was fitted for 250 epochs with 256
generated training cases per family. It contains 142 features: cipher
statistics, repeated-pattern and lag measurements, 44 bounded unknown-key trial
fitness scores, and 16 plaintext-autokey trial scores. Trial plaintexts and keys
are discarded; only scalar features reach the classifier. Language tables come
from the training slice.

Three actual training objectives are used: supervised label smoothing, curriculum
weights from training errors, and consistency between two independently dropped
views of each training example. See [the objective and gradient definitions](neural-training.md).
These methods are established techniques, not a claim of a new state of the art.

ASCII Austen prose is split 60/20/20 percent for fitting, checkpoint selection,
and temperature calibration. Validation checkpoints maximize correct labels,
then minimize negative log likelihood. Doyle prose is excluded from those
gradients, but repeated development decisions based on Doyle results mean it is
no longer an untouched generalization test. Certificate text is excluded
recursively, including nested expected and predicted plaintext fields. Partial
predictions containing unknown letters are not treated as complete texts.

## Experiments on 3 October 2026

| Candidate | Fixed 480 top one | Top three | Exact earlier 204 | Decision |
| --- | --- | --- | --- | --- |
| Format 2, 58 features | 347 | 452 | 160 | Initial accepted residual model |
| Format 3, 82 features | 358 | 459 | 171 | Accepted |
| Format 4, 126 features | 411 | 473 | 191 | Accepted |
| Format 5, 142 features | 428 | 477 | 193 | Saved incumbent |
| Format 6, 222 features | 428 | 474 | 189 | Rejected; original gate defect corrected and format 5 restored |
| Five-network format 5/6 blend | 434 | 476 | 192 | Rejected |
| Format 7, 228 features | 431 | 470 | 187 | Rejected |
| Format 8 warm start, 148 features, rate 0.01 | 433 | 477 | 191 | Rejected; format 5 retained |
| Format 8 conservative warm start, rate 0.0003 | 432 | 476 | 191 | Rejected; format 5 retained |
| Format 5 warm start, same 142 features, rate 0.0005, 80 epochs, distillation 0.25 | 429 | 477 | 193 | Promoted. SHA-256 `5c271f426812d6307f208a636b80f820201e25b3dc6778333e5d08d4d5aaaf4b` |

An earlier expanded 23-family trial scored 362/552 but regressed to 335/480
on the identical prior 20-family cases against 347/480, so it was rejected.
The blend selected its five constituent networks on Austen validation only
and calibrated on the separate Austen slice; it still failed the earlier
benchmark. It remains a local experiment, not a public training API or saved model.

The original promotion gate checked the earlier benchmark against the original
158/204 baseline only. That allowed a format 6 regression relative to the
193/204 incumbent. The gate now replays both fixed comparisons on the actual
incumbent and requires no additional errors on either. A regression test covers
this exact failure, and an independent matrix replay confirms the restored
format 5 scores. Model size is checked before replacement; candidates above
4 MiB cannot overwrite the loadable incumbent. Rejected candidates receive
the requested "axe" decision in recorded policy, with no destructive deletion.

Formats 2 through 8 remain loadable. The current format 8 source uses the exact
142-feature format 5 prefix plus six conditional M209 pair measurements,
for 148 features. It omits the 80 additional format 6 letter/lag measurements.
The M209 values assume fixed public internal settings and use training-only
English frequencies. Feature availability does not establish an improvement.

## A smaller residual mix, 4 October 2026

DeepSeek's mHC projects a widened residual mix onto doubly stochastic matrices
so a deep stack cannot amplify. A later look at DeepSeek-V4-Flash found that a
block usually uses about two of four streams, and that late mixing is nearly
the identity. Bob is two layers, so four streams are the unused part of that
result. `engine.neural_manifold` is a two-stream Sinkhorn mix. A stack of 32
mixes does not raise the L1 norm. It is not wired into the format 5 forward
pass, and the shipped weights were not replaced. See
[the note](logs/bob-manifold-2026-10-04.md).


The first format 8 warm trial used 256 samples per family, 250 epochs, three
96-unit members and the existing rate 0.01. It took 101.727 seconds locally and
selected epochs 55,45,0. Its 433/480 score improved the larger development
comparison, but 191/204 regressed against the incumbent 193/204, so the gate
rejected it. The rejected serialized candidate was 1,598,673 bytes with SHA-256
`e16275216d982d3dc2d74b5089d2b8599943d58da72fc071ffdaf9b204f62be3`.
The shipped format 5 SHA remained
`d8c985dfdaf2d1dd0e17cfdb8412d0f947221b3f9e30318169d9183145c5c825`.

A later authorized conservative warm trial kept 256 samples per family,
250 epochs and three 96-unit members, with rate 0.0003. It took 91.310 seconds,
selected epochs 75,95,15, and scored 432/480 top one, 476/480 top three, 191/204
legacy. It also failed the legacy gate and was rejected without retuning.
Its 1,611,059-byte candidate had SHA-256
`fd35a67bf2702cbc3631fb84a447c1986a81181a34e128db3fb04bad702f44b0`.
Both later trials used Austen fitting, validation and calibration with reused
Doyle promotion comparisons. Neither evaluated Wells; neither changed the
shipped format 5 artifact or its earlier artifact-specific Wells report.

Warm start algebraically rebases the incumbent normalization and appends
zero-weight rows for new inputs, preserving its initial logits to floating-point
precision. The incumbent is validation checkpoint 0, with earliest exact ties
retained. Optimizer moments restart. Warm start requires unchanged output
classes and order, hidden width, ensemble size and training-only language tables.
Formats 2 through 5 and 8 have compatible feature prefixes; formats 6 and 7 remain
replayable but cannot warm-start format 8 by discarding their weighted inputs.

Enigma and M209 are the weakest families: the independent audit gets 7/24 and
12/24 respectively. Short ciphertexts can have similar statistics, and cipher
families can overlap mathematically. A classifier's top choice or confidence
cannot resolve that evidence gap. Known machine settings, related intercepts,
credible cribs and independent checks remain more useful than claiming perfect
identification. The other new catalog helpers are not automatically extra
trained output classes.

## Shuffle check, 4 October 2026

Bob's confidence can describe the alphabet rather than the order. `engine.bob_caution` asks the shipped model, then asks it again on shuffled copies. If the same family wins on most shuffles, the call does not use the order. On the D'Agapeyeff cells the call is substitution, and 40 of 40 shuffles agree, so that call is refused. On a Caesar of known prose the call is caesar, and 0 of 40 shuffles agree. That check did not itself replace the weights. See [the note](logs/bob-caution-2026-10-04.md).

## Promoted warm start, 4 October 2026

A later pass kept the 142 features, warmed up for 80 epochs at learning rate 0.0005, and distilled the previous model at strength 0.25. The gate accepted it: 429 of 480 top one, 477 of 480 top three, and 193 of 204 on the earlier benchmark. The gain is one rail-fence case. Enigma and the M-209 stay at 12 of 24. The new SHA-256 is `5c271f426812d6307f208a636b80f820201e25b3dc6778333e5d08d4d5aaaf4b`. The Wells audit still belongs to the previous file. See [the note](logs/bob-warm-2026-10-04.md).

## More prose and six wheel lags, 4 October 2026

`engine/data/neural_train_public.txt` adds 1,916,398 public-domain letters. `cipher_statistics_v9` adds the five missing M-209 wheel lags and one contrast. A cold fit on that prose scored 427 of 480 and 188 of 204. A warm start onto the new features scored 432 of 480 and 191 of 204. Both lose the older benchmark, so the saved weights stay. See [the note](logs/bob-prose-2026-10-04.md).


## Use and reproducibility

```sh
.venv/bin/python -m engine route LXFOPVEFRNHRLXFOPVEFRNHR
.venv/bin/python -m engine train-router --samples 256 --epochs 250 --hidden 96 --ensemble-size 3 --dry-run
.venv/bin/python -m engine train-router --warm-start --learning-rate 0.0003 --samples 256 --epochs 250 --hidden 96 --ensemble-size 3 --dry-run
```

`train-router` runs one bounded local pass. It creates no scheduler or recurring
routine. `--dry-run` reports candidate metrics without replacing files. The
current source computes format 8 features, while the saved incumbent remains
format 5. Rerunning a training command is an experiment and does not promise to
recreate the incumbent. `--warm-start` starts from a compatible saved model;
the default starts a cold fit. `--learning-rate` sets the maximum cosine-schedule
rate, default 0.01, finite and in `(0,0.1]`; the schedule decreases toward one
tenth of that maximum. The legacy weights remain preserved separately.

To replay the artifact-specific Wells audit with the current saved model:

```python
from pathlib import Path
from engine.neural_router_v2 import evaluate_router
report = evaluate_router(Path("engine/data/neural_audit_wells.txt").read_text())
```

The evaluation rejects sliding 48-letter overlaps with Austen or Doyle and
complete certificate texts. It records corpus/model hashes, seed, per-family
counts, timing and negative log likelihood, without writing weights. Its scope
is the disclosed synthetic family generators, not arbitrary languages,
unknown scripts, unseen methods or historical keys.

The [investigation planner](solver-reasoning.md) uses these rankings as advice
alongside constraints and forward checks. Its `thought` field records a plan;
emotion names are simulated telemetry. Correctness and happiness remain
unknown for unresolved messages. A separate independently checked-case policy
can recommend retirement; speed never compensates for a wrong answer.
