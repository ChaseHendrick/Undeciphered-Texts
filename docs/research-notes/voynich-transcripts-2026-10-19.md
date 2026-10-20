Voynich MS: transliteration corpus frozen — 19 October 2026

First execution step for the Voynich case (`voynich-status.json`). All four
families were `open` with nothing measured; the plan's first move was to
freeze the planned transliteration and independently authored comparison
files. That is what this log records. No statistics were computed, no
alignment was made, and no reading is proposed.

## What was frozen

Files fetched by HTTPS from voynich.nu on 19 October 2026, stored byte-exact
under `engine/data/voynich/`, hash-verified after download. Source of record
is René Zandbergen's transliteration page (Table 8,
https://www.voynich.nu/transcr.html, site update dated 31/05/2025); all three
files carry the IVTFF 2.0 format header.

| Code | File | Alphabet | Version line from header | SHA-256 | Bytes |
|------|------|----------|--------------------------|---------|-------|
| ZL | ZL3b-n.txt | Eva | `Version 3b of 13/05/2025` | bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc | 411,671 |
| GC | GC2a-n.txt | v101 | `Version 2a of 05/02/2023 modified 25/06/2025` | b09570cb6c993bc2d87134d115e60a978650a8a6495483ddbb1f6005a586096f | 314,916 |
| IT | IT2a-n.txt | Eva-T | `Version 2a of 02/02/2023 modified 25/06/2025` | 7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5 | 342,104 |

## Why these three

- **ZL 3b** is the transliteration the Voynich status note already chose as
  primary: essentially complete (per voynich.nu, 5,385 loci, 157,304
  characters), most heavily reviewed, and the only one of the three that
  carries the 2025 fixes (removal of the spurious f89v2 label locus and three
  later-addition f1r loci; corrected fRos locus and Eva high-Ascii handling).
- **GC 2a** (Glen Claston's v101 transliteration) and **IT 2a** (Takeshi
  Takahashi's transliteration as included in the Landini-Stolfi Interlinear)
  are both independently *authored* and essentially complete (5,367 and
  5,215 loci respectively), so folio-by-folio comparison against ZL is
  possible at scale — GC in a genuinely different alphabet family (v101,
  which splits characters differently than anything based on EVA), IT in
  capitalised-derived EVA.
- **RF (the Reference transliteration) is deliberately NOT frozen.** It is an
  automatically generated combination of ZL and GC, so it is not an
  independent transliteration; comparing ZL to RF would be circular for the
  transcription-robustness question.
- **CD (Currier-D'Imperio)** is far less complete (2,196 loci) and **FG
  (First Study Group)** covers only paragraph text (4,060 loci); both stay
  out of the frozen set for now. They remain public at the same source if a
  cross-check on their overlap ever becomes relevant.

## Known caveats recorded up front

- IT and GC still contain the spurious f89v2 label locus that ZL removed in
  May 2025, so naive agreement counts will report that known difference.
- The alphabet labels differ in kind, not just letter values: ZL/IT are
  EVA-family, GC is v101. Any disagreement table must state per-comparison
  which conversion (if any) was applied, or compare at the character-family
  level; no conversion has not been performed yet.
- File counts above the "approximate" sanity greps on `^<f` lines (5,451 /
  5,444 / 5,440, including page-marker lines) were close to but not exactly
  the site's locus counts; the exact reconciliation belongs to the parser,
  not to this log.

## Not claimed here

Nothing follows about language, cipher, hoax, or meaning. The only artifact
is the frozen corpus. Next step per the ledger: an IVTFF parser, locus-level
alignment across the three files, and the disagreement table for the
transcription-robustness family.
