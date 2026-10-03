# Choosing a tractable historical target

Evidence checked on 3 October 2026. The machine-readable companion is
[target-shortlist.json](target-shortlist.json). This is a research triage, with
no new historical decipherment claimed.

The best starting category is an archival letter with a verified transcription,
a known language, substantial text, and a key, deciphered sibling, or clear
duplicate nearby. That is a judgment about useful constraints. It does not
establish that a particular remaining unsolved cipher is easy. None of the named
unread targets checked here qualifies for that claim.

## Check status before spending compute

An archive record marked non-decrypted is evidence about that record, rather
than proof that nobody has read its text. DECODE collects ciphertexts, keys and
related documents, which can require matching across records. Its authors
describe this infrastructure in [The DECODE Database, Version 2](https://ecp.ep.liu.se/index.php/histocrypt/article/download/397/355/298).
The practical consequence is to check editions, key sheets, duplicates and
recent firsthand results before opening an attack.

Two current primary catalogs demonstrate the need for that check:

- [Satoshi Tomokiyo's list](https://cryptiana.web.fc2.com/code/unsolved.htm),
  last modified 3 October 2026, says that its September solutions are not all
  reflected in the list. It directs readers to recent contributor results.
- [Daniel Bourdeau's firsthand catalog](https://dbourdeau.github.io/cyphersolver/writeups.html),
  updated 2 October 2026, distinguishes new attacks, applied keys, existing
  decipherments, partial readings and unread targets. These are different
  outcomes. His claimed readings still need independent verification.

The [CryptoCellar unbroken overview](https://cryptocellar.org/bgac/1941-msg-list-unbroken.html)
states 19 September 2026. Its AWTZK, ZNLZT and FMNGI entries are superseded by
Broken markers on the [July message page](https://cryptocellar.org/bgac/g-army-july-1941.html),
updated 28 September. They are excluded from the unresolved shortlist.
Nr. 86 is also excluded as requested.

## The most useful next steps

**For a new archival project, prioritize evidence acquisition.** The two
Baudouin-Desportes letters in BnF fr. 3984, ff. 186 and 189, have a published
polyphonic key and deciphered siblings, yet are reported unread. That makes
the unknowns more concrete: produce a checked glyph transcription and resolve
ambiguous letter values. Bourdeau's [17 September working notes](https://raw.githubusercontent.com/dbourdeau/cyphersolver/main/targets/sega1593/NOTES.md)
report that his transcription pipeline failed its held-out sibling controls.
The next action is a small blind transcription of the known sibling, checked
against its contemporary decipherment, before undertaking the target pages.
This is a difficult document-reading project with a supplied key, not a
ciphertext-only key recovery claim. Generic printed-text OCR success does not
validate recognition of these manuscript glyphs.

**WEUWY Nr. 138 is already reported solved.** The publisher's
[master list, status 30 September 2026](https://cryptocellar.org/bgac/1941-msg-list.html)
credits its puzzle solution to Cécile Sakellis with Claude on 26 September.
The older July page and unbroken overview lag that specific report. Master-list
footnote 44 supplies `NUG YKS`, which reproduces start `SPE` under the
[published July key](https://cryptocellar.org/bgac/e-keys-july-1941.html).
The Nr. 140 body also ends at the listed `TSA`, but its raw reading contains
errors. This is a partial supplied-key reproduction, with no independent complete
plaintext validation or new-solve claim. Source hashes and remaining gaps are in
[the dated audit](logs/enigma-open-target-2026-10-03.md).

**For a quick cryptanalytic result in this repository, use a constructed or
already solved control first.** A long word-separated substitution with a
matching lexicon fits `word_pattern`. A historical homophonic text requires
checked tokenization and a language model appropriate to its period. A successful
control establishes capability on those conditions; it does not turn an unread
archive record into a solved case.

## Remaining CryptoCellar candidates

The five entries below have no Broken marker on the checked message pages and
remain unmarked Broken in the 30 September master list. Global unsolved status
remains unverified. Counts exclude the five-letter designator; each printed
hyphen is retained as one unknown position. WEUWY is excluded after the dated
master-list correction above.

| Candidate | Known letters / unknown positions | First useful action |
|---|---:|---|
| EHSTQ, 22 June 1941, Nr. 3 | 52 / 0 | Check the facsimile, indicator and network before choosing constraints. |
| RXPSB, 28 June, Nr. 53 | 105 / 2 | Reconcile the current transcription, header and stale table. |
| KLJBO, 3 July, Nr. 87 | 46 / 4 | Verify the four missing positions on the image. |
| LXACA, received 5 July, Nr. 100 | 20 / 0 | Check 4 July evidence; the key page suggests the previous day. |
| JBIYH, 20 July, Nr. 242 | 55 / 0 | Look for same-network traffic or external key material. |

Sources: [current June messages](https://cryptocellar.org/bgac/g-army-messages.html)
and [current July messages](https://cryptocellar.org/bgac/g-army-july-1941.html).
These short or damaged messages give few plaintext constraints. A larger search
budget cannot replace missing key evidence.

RXPSB specifically needs a fresh transcription audit: the current body contains
107 positions, including its two hyphens. The current header says 114 total,
which would imply 109 body positions after removing the designator. The old
overview says 104 total / 99 body. Store all three observations as conflicting
evidence; do not silently truncate or invent letters.

## Defer these as quick-win candidates

- **SP 53/16 nos. 78 and 79.** Their 507 and 644 transcription tokens initially
  look promising. Bourdeau's [working notes](https://raw.githubusercontent.com/dbourdeau/cyphersolver/main/targets/sp53/NOTES.md)
  retract the same-key assumption and report that plausible null/nomenclator
  controls remain unread by his method. Start with images and symbol separation,
  rather than pooling the letters or interpreting a high language score as a solve.
- **Ultimate Enigma challenge.** Its publisher questions the machine and rotor
  wiring. BYQMZ, FKQLZ and XFEDT therefore require identification evidence before
  a normal Enigma search. The challenge also includes QTXMA and SZAEJ. Longer
  ciphertext does not resolve unknown wiring. [Publisher's challenge](https://cryptocellar.org/bgac/ultimate-enigma.html).
- **Henry Percy to Cecil, 23 July 1559.** A contemporary decipherment is reported
  on the TNA original, while the online copy is a tracing. Obtaining that original
  is an archival recovery task, so this is not a verified never-solved target.
  [Firsthand examination](https://dbourdeau.github.io/cyphersolver/percy1559.html).

## What the current engine can test

`engine/solvers/enigma.py` implements supplied-key Enigma I with rotors I-V and
reflectors B/C. Its text normalization removes hyphens. The newer
`engine/solvers/enigma_crib_search.py` preserves missing slots and tests bounded
unknown starts for supplied rotor order, rings, reflector, plugboard and cribs.
It does not recover unknown daily keys. RXPSB lacks a verified applicable key:
the nearby solved Nr. 51 was enciphered on 27 June, despite reception on 28 June.
The linked [June-October key page](https://cryptocellar.org/bgac/e-keys-jun-oct-1941.html)
does not publish a 28 June key. These evidence gaps are recorded in the audit.

`word_pattern` expects A-Z monoalphabetic text with word boundaries and an
explicit lexicon. Its uniqueness is only within that lexicon and a completed
search. Historical spellings, nulls, homophones and word codes require different
models. The existing homophonic search accepts space-separated symbols but
assigns each to one A-Z letter and scores English; syllables, nulls and
polyphonic signs are outside that model. Modern AES and ChaCha20 supplied-key
support does not supply historical keys.

Promote a target to an attack only after preserving its source and uncertainty,
checking current solution status, and passing held-out matched controls. Record
the key, reversible transformation and residual unread symbols for every
proposed reading. Plausible prose and repeated heuristic convergence are
candidate evidence, not independent proof of a unique solution.
