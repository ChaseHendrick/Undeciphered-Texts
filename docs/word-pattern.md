# Word-pattern substitution search

`engine/solvers/word_pattern.py` searches word-separated monoalphabetic substitution without a supplied key. Callers provide a lexicon of single A-Z words. The search preserves case, spaces, punctuation, and digits. It requires every ciphertext word to resolve to a lexicon entry, so names, misspellings, missing words, and lost word boundaries can prevent recovery.

Each distinct ciphertext word is a constraint variable. Its domain contains dictionary words with the same repeated-letter pattern: `NOON` and `DEED` both have pattern `0,1,1,0`. A tentative assignment extends a shared one-to-one cipher-to-plain letter map. Forward checking removes inconsistent choices from the remaining domains, and minimum remaining values chooses the next word. The algorithm reference is [AIMA Python's CSP backtracking, MRV, and forward checking](https://github.com/aimacode/aima-python/blob/master/aima/csp.py), inspected on 2026-10-03. This implementation is independent and uses only the standard library.

This complements the existing n-gram beam search: it uses hard dictionary and substitution constraints, with no statistical ranking. Candidate order is deterministic and carries no confidence score.

```python
from engine.solvers.word_pattern import search_word_pattern, solve_word_pattern

report = search_word_pattern("AB BA", ["AN", "NA", "AT", "TA"], max_nodes=100)
print(report.search_complete)  # True
print(report.ambiguous)        # True: four consistent answers
print([candidate.plaintext for candidate in report.candidates])

result = solve_word_pattern("AB BA", ["AN", "NA", "AT", "TA"])
print(result.plaintext)        # Empty: no unique answer established
print(result.details["candidates"])
```

`search_word_pattern` returns candidates and diagnostics. `solve_word_pattern` returns a `SolveResult` with a populated plaintext only if completed search finds exactly one answer within the supplied lexicon. Its score then counts distinct resolved words. It does not estimate the probability that the plaintext is correct. Unobserved ciphertext letters remain `?` in the cipher-to-plain key, and `key_complete` reports whether all 26 assignments are determined.

`max_nodes` bounds attempted word assignments, excluding initial lexicon indexing and domain preparation. `max_candidates` bounds stored answers. The search stops if one more answer would exceed that storage limit. It checks exhausted branches before enforcing the node limit, so finishing exactly on the last allowed node can still establish completion. The search uses an explicit stack to avoid Python recursion-depth limits.

`stop_reason` is `complete`, `node_limit`, or `candidate_limit`. `search_complete` means every branch under the supplied lexicon and substitution model was considered. `solutions_found` is exact only on completion; otherwise it is a lower bound and can exceed the retained candidate count by one. `ambiguous` is true if multiple solutions were found, false if completed search found at most one, and null when an incomplete search has not resolved that question. An incomplete search with one answer never reports uniqueness. An empty completed search means no answer within the lexicon; an empty incomplete search remains unresolved.

The certificate in `engine/data/word_pattern_certificate.json` records the existing `SUBSTITUTION_PLAIN` repository fixture, a literal ciphertext, and a small explicit lexicon with decoys. Recovery uses no expected key or plaintext input. It completes after 87 word assignments and recovers the fixture's full 26-letter decryption key. This is a constructed regression fixture, not a published historical solve. The certificate's source URL cites the search algorithm rather than the plaintext.

`tests/test_word_pattern.py` checks that recovery and its SHA-256, dictionary omissions, injective letter constraints, MRV selection, ambiguity, partial keys, and both search limits. Run:

```bash
python3 -m unittest tests.test_word_pattern -v
```

The separate CLI command accepts a UTF-8 file of whitespace-separated A-Z words:

```bash
python3 -m engine word-pattern "AB BA" --lexicon words.txt --max-nodes 10000
```

It emits JSON with completion, ambiguity, and candidate details. No default dictionary is shipped, so the helper is outside the keyless `SOLVERS` registry. It makes no claim about an unknown script, Kryptos K4, Zodiac, Beale, McCormick, Voynich, or army message Nr. 86.
