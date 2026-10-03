# Easy published recovery, 3 October 2026

Emperor's new search API receives the literal ciphertext
`IIWRILCPECLFDHVAEIR`, no key and no crib. After 1,444 checks its second-ranked
candidate is `CIVILWARFIELDCIPHER`, with Redefence row ranks 213 and offset 0.
Only after the search returned was this compared against the independently
printed [ACA Redefence example](https://www.cryptogram.org/downloads/aca.info/ciphers/Redefence.pdf)
and the recorded recovered-output hash. They match exactly.

The first ranked candidate is the cyclic reading `IVILWARFIELDCIPHERC`, also
forward-consistent under a different offset. The English score does not
identify the published answer uniquely from this short ciphertext. The
reference resolves the control, rather than retroactively making rank one
correct or supplying the key to search.

The [full report](easy-recovery-2026-10-03.json) separates actual search inputs,
all retained candidates and post-search reference comparison. This is a blind
key recovery on a known published example, with an honest ranking limitation.
It is not a new historical decipherment. No persona vocabulary, expected
plaintext or printed key entered the solver call.
