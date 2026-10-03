# Periodic Gromark

The [ACA Periodic Gromark sheet](https://www.cryptogram.org/downloads/aca.info/ciphers/PeriodicGromark.pdf) combines the existing Gromark mixed alphabet with a keyword-derived numeric primer and a periodic alphabet starting position. It is a distinct construction from the [ordinary Gromark helper](../engine/solvers/gromark.py).

Deduplicate keyword letters in order. Their alphabetical column ranks form the primer, and their count sets the period. ENIGMA gives `264351` and period 6. Fill the mixed alphabet in rows under that keyword and read columns in alphabetical keyword order, reusing the existing Gromark alphabet builder. Extend the primer by adjacent chain addition modulo ten: for width `w`, `digit[n] = (digit[n-w] + digit[n-w+1]) % 10`. For each period group, the next repeated keyword letter sets the starting index in that mixed alphabet; each plaintext A-Z position is then shifted by its chain-added digit.

```python
from engine.solvers.periodic_gromark import periodic_gromark_decrypt, solve_periodic_gromark

plaintext = periodic_gromark_decrypt(ciphertext_body, keyword="ENIGMA")
result = solve_periodic_gromark(printed_message, keyword="ENIGMA", framed=True)
```

`periodic_gromark_keyword`, `periodic_gromark_primer`, `periodic_gromark_alphabet`, and `periodic_gromark_running_key` expose the construction. The source's repeated-keyword example REPEATED becomes REPATD, giving primer `534162` and period 6. The implementation supports 2 through 9 distinct keyword letters so every rank has one unambiguous decimal digit. This is an explicit implementation limit; no convention for ranks above 9 or a single-letter chain is assumed. Running-key lengths are integers 0 through 1,000,000. Text is limited to 1,000,000 characters, requires A-Z letters, rejects non-ASCII alphabetic characters and digits, and omits non-letter separators. Output is uppercase with no padding.

## Printed numeric framing

The ACA printed ciphertext begins with the derived primer and ends with the last running-key digit. These numbers are framing, not ciphertext letters. The ordinary encrypt/decrypt functions operate on the letter body and reject numeric framing. Pass `framed=True` to encrypt or decrypt a framed message. `periodic_gromark_frame(body, keyword=...)` formats period-length groups, and `periodic_gromark_unframe(message, keyword=...)` checks the primer and final digit before returning the body. Frames have a separate 1,500,032-character bound to accommodate grouping up to 1,000,000 body letters even at the shortest supported period. Grouping whitespace is removed before validating the body bound. Incorrect framing fails validation. The check digit detects some transcription inconsistencies; it is not authentication and does not certify a correct plaintext.

The complete published example has 64 plaintext letters and uses ENIGMA, derived primer `264351`, and mixed alphabet `AJRXEBKSYGFPVIDOUMHQWNCLTZ`. Its group offsets are `4, 21, 13, 9, 17, 0`, and the last chain digit is 4. The recovered plaintext, full body, framing, and running key match the independent printed table. [The certificate](../engine/data/periodic_gromark_certificate.json) records their literals and SHA-256 over uppercase A-Z plaintext ASCII bytes. The downloaded PDF was visually checked on 3 October 2026 and its hash is recorded.

`solve_periodic_gromark` returns `mode: known_key` and the supplied keyword settings. It does not search for an unknown keyword. Published supplied-key decryption and synthetic roundtrips validate the implemented construction; neither claims a historical recovery or unknown-script reading. The helper remains outside text-only solve dispatch because it requires keyword input.

```sh
.venv/bin/python -m unittest tests.test_periodic_gromark -v
```
