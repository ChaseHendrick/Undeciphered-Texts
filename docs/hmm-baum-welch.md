# First-order HMM (Baum–Welch)

`engine/hmm_baum_welch.py` fits a small first-order hidden Markov model to a sequence of discrete symbols. Parameters (start, transition, emission) are estimated by Baum–Welch (expectation–maximization) from the symbols alone. Several random restarts are kept by observation log-likelihood. The returned state path is not raw Viterbi: it walks the smoothed posterior from left to right and switches only when another state's posterior is at least 0.6. State labels are arbitrary, so a two-state path is scored after the better of the two label flips. `viterbi` is still in the module for the joint MAP path.

**This tool does not decipher ancient scripts.** It does not read Linear A, the Voynich manuscript, Rongorongo, the Indus script, the Phaistos disk, or any other undeciphered text. A recovered state sequence is a clustering of positions under a first-order Markov assumption. It is not a translation, a phonetic value, or evidence about a historical inscription.

## Synthetic check, not a reading

`generate_two_state_corpus` draws symbols from a known sticky two-state HMM whose emission rows prefer opposite ends of a small alphabet. The unit test in `tests/test_hmm_baum_welch.py` fits the model without the generating states and requires the decoded path to agree with those states **better than chance**.

Chance here is the accuracy of labeling every position with the majority state (about one half when the chain is balanced, higher if one state dominates the draw). The test also requires a margin over that constant baseline. Beating chance on this synthetic corpus only shows that the estimator can recover a path when the data really were produced by a two-state HMM. It says nothing about Voynich, Linear A, or any other real undeciphered corpus, and those corpora are not inputs.

## Why the path uses a 0.6 switch margin

On `generate_two_state_corpus(length=500, seed=0)`, fit with `n_iter=30`, `restarts=4`, and `seed=0`:

| Decoder | Agreement with the generating states |
| --- | --- |
| Constant majority label (chance on this draw) | 293/500 |
| Viterbi, or posterior mode at 0.5, on the Baum–Welch fit | 494/500 |
| Posterior hysteresis, switch only at posterior ≥ 0.6 | 496/500 |

The two extra agreements are one boundary. There the smoothed posterior for the entering state is only about 0.55 for two symbols, and Viterbi switches early. Requiring 0.6 keeps those symbols in the previous state. Four other positions stay wrong; the margin does not fix them. The same corpus and seed are unchanged. The observation log-likelihood is still the Baum–Welch figure; the margin changes the path, not the fitted parameters.

The unit test requires accuracy strictly above 494/500 and still above the constant-state baseline (including a 0.2 margin over that baseline).

## What it will not do

- It will not assign sound values or word readings.
- It will not decide how many real “languages” or scribal hands a manuscript has.
- It will not turn a symbol inventory into plaintext.

Use it as a stdlib numerical check. Do not cite its output as a decipherment.
