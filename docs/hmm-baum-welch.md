# First-order HMM (Baum–Welch)

`engine/hmm_baum_welch.py` fits a small first-order hidden Markov model to a sequence of discrete symbols and decodes a hidden-state path with the Viterbi algorithm. Parameters are estimated by Baum–Welch (expectation–maximization) from the symbols alone. Several random restarts are kept by observation log-likelihood. State labels are arbitrary, so a two-state path is scored after the better of the two label flips.

**This tool does not decipher ancient scripts.** It does not read Linear A, the Voynich manuscript, Rongorongo, the Indus script, the Phaistos disk, or any other undeciphered text. A recovered state sequence is a clustering of positions under a first-order Markov assumption. It is not a translation, a phonetic value, or evidence about a historical inscription.

## Synthetic check, not a reading

`generate_two_state_corpus` draws symbols from a known sticky two-state HMM whose emission rows prefer opposite ends of a small alphabet. The unit test in `tests/test_hmm_baum_welch.py` fits the model without the generating states and requires the decoded path to agree with those states **better than chance**.

Chance here is the accuracy of labeling every position with the majority state (about one half when the chain is balanced, higher if one state dominates the draw). The test also requires a margin over that constant baseline. Beating chance on this synthetic corpus only shows that the estimator can recover a path when the data really were produced by a two-state HMM. It says nothing about Voynich, Linear A, or any other real undeciphered corpus, and those corpora are not inputs.

## What it will not do

- It will not assign sound values or word readings.
- It will not decide how many real “languages” or scribal hands a manuscript has.
- It will not turn a symbol inventory into plaintext.

Use it as a stdlib numerical check. Do not cite its output as a decipherment.
