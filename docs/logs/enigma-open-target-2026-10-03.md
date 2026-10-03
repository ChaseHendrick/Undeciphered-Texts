# Enigma target source audit, 3 October 2026

No new historical solution was recovered. WEUWY Nr. 138 is already reported
solved; RXPSB Nr. 53 lacks verified applicable daily settings. The
[machine-readable record](enigma-open-target-2026-10-03.json) contains the ten
primary-source URLs, retrieval times, byte counts, response metadata and SHA-256
hashes, plus literal inputs and actual outputs. Cipher searches examined zero
start positions. No work was performed on Nr. 86.

## WEUWY status and controls

The [master list, status 30 September 2026](https://cryptocellar.org/bgac/1941-msg-list.html)
credits the Nr. 138 puzzle solution to Cécile Sakellis with Claude on 26 September.
The July message page and older unresolved overview lag that specific report.
Master-list footnote 44 corrects the indicator to `NUG YKS`. This resolves the
target-selection conflict; details of the reported Nr. 138 correction were not
found in the fetched material.

The [9 July key](https://cryptocellar.org/bgac/e-keys-july-1941.html) supplies
reflector B, rotors III/I/V from left to right, rings NAV, and plugboard
`AC BN FM GI JL KO PU QX RZ TV`. The following are actual supplied-key controls:

| Input | Machine output | Published comparison |
|---|---|---|
| Corrected indicator, ground NUG, input YKS | SPE | Matches corrected start |
| Nr. 138 printed indicator, ground NUG, input YKI | SPF | Does not give SPE |
| Nr. 140 printed indicator, ground NIG, input IKS | FWO | Does not give SPE |
| Nr. 140 body at supplied start SPE | End windows TSA | Matches key-table stop |

The exact raw machine output from Nr. 140 is:

```text
FURHRUNGSSJAFFELINXIUNAKIXIBSALRXROEAXEILSRAJMWN
```

This output is retained with its garbles. It was not silently rewritten into
German prose. An independent arithmetic oracle agrees, and forward replay
matches all 48 transcribed cipher letters. Those checks establish machine
consistency, not correctness of a complete historical reading. The linked
incoming and outgoing facsimiles are ciphertext forms; they do not provide a
complete independent plaintext control. No unknown-start search was run on this
already solved target.

## RXPSB evidence gate

RXPSB remains unmarked Broken in the dated master list. The
[current transcription](https://cryptocellar.org/bgac/g-army-messages.html)
has 107 body slots: 105 known letters and gaps at zero-based positions 17 and
103. Its header total 114 would imply 109 body slots after the designator. The
linked scan was inspected, but no comprehensive new transcription is claimed.

The [June-October key page](https://cryptocellar.org/bgac/e-keys-jun-oct-1941.html)
publishes a 27 June key, with III/V/II, reflector B, rings RGP and ten plugs;
it publishes no 28 June key. Related solved Nr. 51 PLDRV has call sign 5l8 but
was explicitly enciphered on 27 June despite receipt on 28 June. That does not
establish settings for RXPSB. Two 27 June indicator controls reproduce listed
starts: `SDG EKN` gives LTA and `BPG KGM` gives CSX. A third exposes a discrepancy:
`ZKT HLP` gives RPZ, while the table says RTZ. An initial assertion expecting RTZ
failed; the disagreement is preserved in the JSON instead of being normalized
away.

A justified start-only search still needs a verified applicable rotor order,
rings and plugboard, checked on a matched sibling, plus reconciliation of the
missing-slot count. No tentative German crib or arbitrary default daily key was
introduced. The new gap-preserving start-search backend is available, but cannot
recover an unknown daily key.

## Checks actually run

Eight supplied-key machine invocations, seven independent arithmetic comparisons
and one full forward body replay were recorded. These are controls, not new
breaks. The hashes of all ten downloaded primary sources were checked against
their saved scratch bytes.

```sh
.venv/bin/python -m unittest tests.test_enigma_crib_search tests.test_enigma
```

17 tests passed in 0.288 seconds. No full suite, unknown daily-key search or new
historical solution is claimed by this log.
