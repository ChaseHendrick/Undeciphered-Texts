# Paradigm Kryptos CTF triage, 3 October 2026

**None of the ten public CTF puzzles qualifies as an unclaimed first solve at this source check.** The official leaderboard and its public first-solve feed both list PK1 through PK10. The last two records are PK9 at 22:29:29.926 UTC and PK10 at 22:52:01.808 UTC on 2 October 2026. This reports the organizer's verified-submission records, not independently audited judging or evidence of prize payment. [Public leaderboard](https://www.paradigm.xyz/kryptos-ctf/leaderboard), [public first-solve feed](https://www.paradigm.xyz/kryptos-ctf/api/first-solves).

The current public rules describe ten separate $1,000 first-solver competitions and distinguish these from the historical K4 reference service. The CTF puzzles are organizer-created exercises, not an ancient script or a new historical ciphertext. No account, submission, payment or prize action was taken. Only public GET requests were used. [Rules](https://www.paradigm.xyz/kryptos-ctf/rules), [custodian announcement](https://www.paradigm.xyz/writing/kryptos).

## Available local material and status pitfall

The public page loads a source bundle containing ten literal A-Z fixtures of lengths 144 through 504. All fit the repo's 512-letter browser input cap. This establishes input compatibility, not an easy recovery method. The bundle supplies ciphertext but no authenticated plaintext, key or construction for these puzzles. [Public puzzle page](https://www.paradigm.xyz/kryptos-ctf/pk10), [public fixture bundle](https://www.paradigm.xyz/kryptos-ctf/_next/static/chunks/0h1ap~1.6ljs6.js).

Its generic puzzle definitions initialize every status to Unsolved. The same application overlays public first-solve data, so those defaults are not current evidence that a puzzle remains open. The independent rendered leaderboard confirms all ten entries. No remaining challenge was selected as a newly unsolved target. The accompanying [JSON ledger](ctf-triage-2026-10-03.json) freezes fixture lengths and hashes, published solve timestamps, source-body hashes and the local trial.

## Small local trial on an already-solved control

For a concrete compatibility check, the existing `search_transposition_ensemble` ran on the 350-letter PK2 fixture with no crib or supplied key. Bounds were 500 checks, width at most 32, rails at most 4 and three retained candidates. It exhausted its declared 225 hypotheses: 3 rail-fence, 12 route, 42 columnar and 168 Redefence. The measured search took about 0.20 seconds locally. This was a test of those finite transforms, not every possible transposition.

The leading candidates did not provide an authenticated answer. Their source-normalized output hashes and scores are recorded; `historical_reference_match` stays null. All three re-encrypt to the exact public ciphertext, including a separately coded ranked-zigzag or rectangle-perimeter oracle. The three additional comparisons bring this local run to 228 model/replay checks. A bijective forward match and an English score do not establish correct plaintext. The JSON retains only a short excerpt per candidate rather than publishing an unsupported full reading.

The practical outcome is narrow: public local fixtures are available, this small portfolio runs reproducibly on one, and the organizer already records all ten as solved. These can become recovery benchmarks if public authenticated keys or plaintext references are obtained. They are not evidence that we have solved something new, and repeating the simple portfolio is not a justified next open-target experiment.

No code, trained model, registry, account or external system was modified. No private K4 reference was consulted. Source checks used ordinary HTTPS with default certificate verification; pages unavailable to the web extraction tool were retrieved through a normal public-page request. Nr. 86 is outside this work.
