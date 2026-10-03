# Bob research plan, 2026-10-03

This is a proposed experiment plan, not an implemented model or a new decipherment. Bob predicts cipher families and advises bounded tools. A family probability does not establish plaintext correctness. Preserve the accepted model and existing benchmark artifacts while testing separate candidates.

## What the primary research supports

- [Alice, Shen and Smith, September 2025](https://arxiv.org/html/2509.07282v1) studies monoalphabetic substitution decipherment. Its generalization experiment uses an 85 million parameter Transformer, with unseen substitution keys and spaces and punctuation retained. Pooling occurrences of each symbol enforces repeated-letter consistency; its bijective head exposes a permutation. Short inputs still produce errors, and bijective decoding trades some accuracy for structural validity. This is a separate decipherer, not a replacement weight file for Bob's family classifier.
- [Korrapati and colleagues, August 2025](https://arxiv.org/abs/2508.10235) train Transformers to infer classical substitution and Vigenere behavior from known ciphertext/plaintext pairs in context. Their setup motivates controlled known-pair experiments. It does not demonstrate breaking modern secure encryption or recovering arbitrary historical plaintext without clues.
- [Leierzopf's CrypTool thesis, June 2021](https://www.cryptool.org/media/publications/theses/MA_Leierzopf.pdf) compares engineered features, neural architectures and ensembles for 56 classical cipher types. Use its feature ablations as a baseline design reference. Different classes, text lengths, sources and sample counts make its reported percentages unsuitable for direct comparison with Bob's benchmarks.
- [Podkopaev and Ramdas, UAI 2021](https://proceedings.mlr.press/v161/podkopaev21a.html) address uncertainty under label shift, where class frequencies change but the input distribution conditioned on each class remains fixed. New key distributions, languages and transcription damage can change that conditional distribution. Applying their guarantees to those changes requires additional justification; softmax scores alone do not supply it.

## First experiment: broaden the generator, freeze the evaluation

The inspected [generator](../engine/neural_grade.py) samples four Enigma rotor orders with an empty plugboard. M209 samples external positions using fixed published pins and lugs. These restricted settings can create shortcuts. Their importance must be measured rather than assumed.

Create a separate versioned benchmark manifest before training: record plaintext source/hash, family, exact key/settings, generator version, seed, normalized length, noise transform and expected output hash. Hold out source documents and keys, not merely another passage from the same source. Existing evaluation material used to select a trial becomes development evidence; obtain untouched material for final evaluation.

Add legal Enigma rotor orders, rings and nonempty plugboards, plus varied legal M209 pins and lugs. Check generated vectors against an independent implementation or published control. Evaluate clean inputs separately from punctuation changes, substitutions, missing characters and preserved gap slots. Record unsupported inputs and model failures explicitly. Keep the existing 480-case and 204-case comparisons frozen, and report the new distribution separately.

## Second experiment: constrained decipherment

Prototype a small substitution-only model separately from Bob. Compare pooled-symbol predictions and a hard bijective assignment against the existing word-pattern and language-search baselines under identical budgets. Evaluate fresh permutations, withheld source documents and both retained-space and letters-only inputs. Measure complete-message recovery, character errors, observed-symbol key recovery, runtime and forward consistency. Unseen symbols remain unconstrained; re-encryption confirms a transformation, not a historical reading.

A later known-pair experiment may test in-context inference on substitution and Vigenere. Separate supplied examples from withheld messages and their independently known answers. Compare against deterministic key inference before adding a larger model.

## Acceptance checklist

- Preserve incumbent weights; hash model, source, class order, features, normalization and all manifests.
- Freeze training, selection, calibration and final evaluation partitions; record every trial and rejection.
- Report per-family and per-length errors, source transfer, calibration and out-of-family behavior alongside total accuracy.
- Check finite gradients, reproducible seeds, resource limits and exact incumbent regression cases.
- Promote only with independent reference correctness and a declared speed comparison. Fast wrong answers and plausible language earn no correctness reward.
- Keep unresolved historical candidates unverified until independent evidence supports them; document uncertainty and failed hypotheses.
