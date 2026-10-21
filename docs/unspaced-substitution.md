# Unspaced substitution with dictionary constraints

`engine.solvers.unspaced_substitution.infer_unspaced_substitution` searches for both an unknown bijective letter map and unknown word boundaries. The caller supplies a finite vocabulary, not a key, plaintext, crib, or phrase template. This extends the spaced-word constraints in `word_pattern.py` to ciphertext with no given spaces.

```python
from engine.solvers.unspaced_substitution import infer_unspaced_substitution

report = infer_unspaced_substitution(
    "ZRCSWFRCPGCCFULCZZCPUSAVUWUZCVZ",
    lexicon=["THE", "CIPHER", "KEEPS", "LETTERS", "CONSISTENT",
             "OTHER", "PEERS", "KEEP", "SENT", "LINE", "REST", "THERE"],
    max_nodes=100000,
    max_states=4096,
    max_candidates=20,
    min_word_length=1,
    max_word_length=32,
    max_lexicon_entries=20000,
    timeout_seconds=30.0,
)
```

The trie represents vocabulary prefixes. Each search state holds a ciphertext position, trie position, observed-symbol mapping, used plaintext letters, and boundary offsets. A repeated ciphertext symbol must use its earlier plaintext letter. Different symbols must use different letters. A terminal trie node permits a word boundary or continued traversal into a longer word. A solution must consume the entire ciphertext and end on a dictionary word. Every returned candidate is independently replayed through its inverse observed-symbol map.

The implementation uses deterministic depth-first backtracking. Alphabetical order determines which witnesses appear first; there is no language score or persona vocabulary preference. The [AIMA project](https://github.com/aimacode/aima-python/blob/master/aima/csp.py) provides a general reference for constraint backtracking. This implementation does not copy that code or claim a new cryptanalytic method.

One popped state consumes one search node, including boundary transitions. Pending states are capped; exceeding `max_states` stops the search without dropping branches and calling the remaining search complete. A candidate cap permits one additional witness to establish observed ambiguity, then stops if work remains. Completing exactly on the final allowed node can still establish exhaustion. Input preparation has separate finite entry, character, and trie limits; the cooperative deadline includes preparation and is checked before each search node. This is a bounded local algorithm, not a security sandbox for arbitrary caller iterators.

| Parameter | Default | Hard bound |
| --- | --- | --- |
| Normalized ciphertext | Required | 4 through 512 ASCII letters; at most 4,096 raw characters |
| `max_nodes` | 100,000 | 1 through 1,000,000 |
| `max_states` | 4,096 | 1 through 16,384 pending states |
| `max_candidates` | 20 | 1 through 100 retained witnesses |
| `min_word_length`, `max_word_length` | 1, 32 | Ordered interval within 1 through 64 |
| `max_lexicon_entries` | 20,000 | 1 through 50,000 consumed entries |
| `timeout_seconds` | 30 | Finite value from 0.001 through 120 |
| Lexicon preparation | Fixed | 1,000,000 supplied characters and 250,000 trie nodes |

Formatting whitespace in ciphertext is ignored, not treated as known word boundaries. Punctuation and non-ASCII letters are rejected. Vocabulary entries are single ASCII words of at most 64 letters, normalized to uppercase and deduplicated. Oversized iterables are rejected after consuming at most the entry bound plus one. Empty supplied vocabulary is invalid. A nonempty vocabulary whose words all lie outside the declared length interval gives a complete, zero-node `unsat` result relative to that empty effective model.

The direct Python API accepts the larger declared vocabulary bounds above. The generic JSON tool adapter additionally limits each list to 1,000 entries and parameters to 64 KiB. Use direct Python or the reproduction driver for the larger corpus vocabularies in the Dorabella log.

`solutions_found` counts distinct `(plaintext_letters, word_boundaries)` witnesses. `plaintexts_found` counts distinct unspaced plaintexts. `segmentations_found` counts distinct boundary tuples, even when different plaintexts share the same boundaries. Consequently, `NOON` and `DEED` can be different plaintexts with the same one-word segmentation. Candidates retain their spaced text, words, end offsets, observed mapping, forward replay status, and a SHA-256 hash of recovered unspaced ASCII output. Unobserved key slots remain `?`.

`model_status` is `sat` after any witness, `unsat` only after exhaustive failure, and `unknown` when an incomplete search found none. Exhaustion controls uniqueness and `forced_plaintext`. A capped search can establish observed ambiguity but cannot establish uniqueness or forced letters. Complete-search forced letters are common to every compatible plaintext in this finite model. `claimed_plaintext` always remains null, and historical correctness remains unverified.

The [certificate](../engine/data/unspaced_substitution_certificate.json) freezes a constructed 87-letter ciphertext. Search receives only its separate 28-word vocabulary, including unrelated distractors. It recovers the exact letters and boundaries in 883 exhausted nodes. Its hash is calculated from recovered bytes. The independent encoder and expected answer appear only in validation, not inference. This measures joint map and boundary recovery within a covered finite vocabulary, not general English performance or a Dorabella solution.

The [Dorabella campaign](logs/dorabella-word-constraints-2026-10-03.md) applies the method to a source-backed 87-symbol transcription. Missing vocabulary, transcription uncertainty, other languages, homophonic mappings, and other cipher families remain outside the search model. Even a complete failure within a supplied dictionary cannot exclude English.
