# Ogham letter lookup

This is a **lookup**, not a decipherment.

`engine/ogham_lookup.py` maps Ogham code points, characters, and Unicode
character names. It does not read an inscription, recover Primitive Irish,
or claim that any undeciphered text is Ogham (or that Ogham itself is
undeciphered). Ogham as a script is a known alphabet; this table only
repeats published character identities.

## Source

Fetched 2026-10-02 from the Unicode 18.0.0 Ogham names list (block
U+1680-U+169F, assigned characters through U+169C):

https://unicode.org/Public/18.0.0/charts/nameslist/1680/

The names list prints, under Traditional letters:

`1681` `ᚁ` `OGHAM LETTER BEITH`

`tests/test_ogham_lookup.py` checks that one fetched row: the character
`ᚁ` looks up as U+1681, name `OGHAM LETTER BEITH`.

Other rows in the module are the remaining names and code points from that
same page (space mark, traditional letters, forfeda, feather marks). The
character is the Unicode scalar of the listed code point. Groups follow the
headings on the names list (`space`, `traditional`, `forfeda`,
`punctuation`).

## What this does not do

- It does not transliterate into Latin beyond the Unicode name.
- It does not date, translate, or authenticate an inscription.
- It does not treat a match against this table as a decipherment.
