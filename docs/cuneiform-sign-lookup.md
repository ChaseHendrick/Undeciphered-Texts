# Cuneiform sign lookup

This is a **lookup** of readings already published for a few known Sumero-Akkadian signs. It is **not** a decipherment of undeciphered texts, unknown tablets, or scripts this repository otherwise studies.

The table is a short excerpt of the Oracc Sign List, file `00lib/osl.asl`:

- Sign list: <https://github.com/oracc/osl/blob/master/00lib/osl.asl>
- Pinned copy used here: <https://github.com/oracc/osl/blob/dcee28e57d9387638c122e3435a98ceb6ea9e5e2/00lib/osl.asl> (commit `dcee28e57d9387638c122e3435a98ceb6ea9e5e2`, 2026-09-16)
- Project: <http://oracc.org/osl/>
- File format: <http://oracc.org/osl/asloslfileformat/>
- Why this list is the Unicode ancillary sign list: <https://www.unicode.org/reports/tr56/>

OSL is maintained by Niek Veldhuis, Steve Tinney, and contributors, and is licensed CC BY-SA by The OSL Project. The excerpt keeps sign names, Unicode code points, glyphs, and `@v` readings as published, including uncertainty marks (`?`) and non-standard index marks (`ₓ`). Those marks are data from the list, not judgments added here.

`lookup_sign` and `lookup_value` return only rows in `engine/data/cuneiform_osl_excerpt.json`. A name or value that is absent returns nothing. Absence is not a reading, a correction, or a claim about any tablet.

The unit test checks one fetched value: OSL sign **AN** (`U+1202D`, 𒀭, `CUNEIFORM SIGN AN`) publishes the reading **an**.
