# Hashes for the cells and the scores

4 October 2026. No letter string is stored.

Each result is reduced to canonical JSON. Tuples become lists, object keys are sorted, and a float is written with 17 significant digits. SHA-256 of those bytes is the content hash. The chain hash of a step is SHA-256 of the previous chain hash, a newline, and the new content hash. The cells are the first step, so their chain hash is their content hash.

| Step | Content hash |
| --- | --- |
| Cells | `f2460a6acdf2f50e12fdc8760c39753746d885282cd0bdfd0eec877c56e6fae5` |
| Yardstick | `e12910ac3d3d0460db9ce76719298d94f261b7a8a17f09fec675dc4cda635d66` |
| Balls | `3b84e9af30916cf42181a75d847eff6ba0cc992f606a069fe8fcfc5af0227bdd` |
| Record | `834058b318779e3811b0b19408329f702bbf3577623dc17912af55c62efc80f7` |

The chain, after the record, is `ce7d38c98d060ee26a038f8a7f5b1849b1f30996eeda15c6955c74912370b455`.

A matching hash means the cells and these scores were recomputed. It does not mean they were read. If a score changes, its hash changes, and every chain hash after it changes.

The conversion of the published chi-square was hashed after this note. The edit bound was hashed after that. The correction ledger was hashed after that. The regrouping was hashed after that. The column-key null was hashed after that. The language-model null was hashed after that. The bifid null was hashed after that. The period-4 search was hashed after that. The word-score search was hashed after that. The running keys were hashed after that. The dictionary shapes were hashed after that. The column-order shapes were hashed after that. The swarm board was hashed after that. The inference from that board was hashed after that. The foresight was hashed after that. The engine checks were hashed after that. The adversary was hashed after that. The autokey was hashed after that. The digit routes were hashed after that. The step, the unused cells, and the Playfair ban were hashed after that. The coordinate delay and the progressive shift were hashed after that. The book's exercise, used as a key, was hashed after that. The printed groups were hashed after that. Those heavy scores are now stored in `engine/data/swarm_cache`, and a later hash reads them instead of repeating the search. The chain tip is now `2ca2a0b1b8ebc950e36839a6e7aebb03c7db1570d7c3a8cfc616dc6d987c8ccc`. The four hashes in the table above did not change.

No letter string is stored.
