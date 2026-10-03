# Connected solver interface

Run `python3 -m engine tools` to list every allowlisted tool, its execution mode, input encoding and required parameters. The catalog is generated from the actual public function signatures. It includes supplied-key helpers, unknown-key searches, crib inference and composed investigation. There is no user-supplied module import or dynamic code evaluation. Required fields reflect Python signatures; semantic requirements still apply. For example, Hill inference needs a nonempty crib even though its signature defaults to an empty sequence, and Morse inference needs a lexicon or a crib. The topical documentation and runtime validation state these constraints.

```sh
python3 -m engine run progressive-key KCIWVCD --params '{"keyword":"GRAPEFRUIT","progression":1}'
python3 -m engine run transposition-ensemble AIVLHCEWPFIDRIRLE --params '{"max_checks":1000,"max_candidates":5}'
python3 -m engine run rsa-wiener 1511 --params '{"modulus":8927,"exponent":2621,"plaintext_length":2}'
python3 -m engine run rsa-common-modulus 2790 --params '{"c2":1317,"e1":17,"e2":7,"n":3233}'
python3 -m engine run morse-constraints 0 --params '{"families":["pollux"],"lexicon":["E"],"max_maps":1000}'
python3 -m engine investigate LXFOPVEFRNHR --crib 0:ATTACK --max-checks 5000
```

These invocations illustrate explicit parameter contracts. Consult the selected helper's certificate for a complete known-answer vector. Text input can be piped through stdin. AES and ChaCha20 use hexadecimal ciphertext and hexadecimal key/nonce fields. RSA Wiener, Fermat and common-modulus tools accept an integer ciphertext and explicit public parameters. Their plaintext byte results are hexadecimal.

`--params` must contain a JSON object. Unknown names, missing required fields and unexpected parameters fail before invocation. Reports preserve the selected mode and expose derived report fields, including Morse uniqueness only when the actual search establishes it. Cribs use records such as `{"offset":0,"plaintext":"KNOWN"}`. Most Latin tools use A-Z letter positions; Morse constraints and numeric investigation count decoded spaces and punctuation. See [Morse constraints](morse-constraints.md).

The adapter caps raw input at 8,192 characters, RSA values at 4,096 bits, parameter JSON at 64 KiB, nesting at eight levels, strings at 8,192 characters, sequences at 1,000 entries and mappings at 100 fields. Individual tools impose narrower bounds. It also caps restarts, iteration counts and requested byte lengths. These constraints bound local invocation rather than establishing a hard wall-time limit for every function.

Some repository experiments accept callbacks, lists of ciphertexts or physical-device signals; those require their documented Python APIs. They are not silently forced into a text invocation. `run` reports successful execution under the selected tool's assumptions. A recovered candidate, score, crib fit or reencryption check still requires independent evidence before a historical solve claim.
