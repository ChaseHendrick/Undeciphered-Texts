# D'Agapeyeff cipher — 2026-10-02 (EDT)

Not a decipherment. No plaintext of the 1939 challenge is claimed.

## Published status

- https://en.wikipedia.org/wiki/D%27Agapeyeff_cipher (wikitext fetched 2026-10-02 via `action=parse`). The page calls it an unsolved cipher from the first edition of Alexander D'Agapeyeff, *Codes and Ciphers* (Oxford University Press, 1939), p. 158. Later editions dropped it. The page says D'Agapeyeff is said to have forgotten how he encrypted it.
- The same page credits no one with a solution. Its references are challenge notes and an article titled "The Unsolved D'Agapeyeff Cipher" (Barker, *Cryptologia* 1978). Elonka Dunin's list is linked as unsolved codes.
- Printed ciphertext, 79 groups of five, 395 digits, ending `92000`. Dropping the final `000` leaves 392 digits, 196 pairs. The page's index of coincidence "1.812" on horizontal pairs matches `26 * Σ n(n−1) / (N(N−1))` on those 196 pairs (1.8122).

## Family that was tested

Polybius coordinates 1–5 (5×5 keyword square, J folded into I), then a repeating digit key added modulo 10, then an optional null in one residue of every 3rd, 4th, or 5th position. The null periods are the ones the book names on p. 111, quoted on the Wikipedia page. The keyword list is the straight alphabet plus the 641 words of at least four letters in `engine/data/english.txt` (631 distinct squares).

The solver is not given the keyword, the numeric key, or the null phase. A stream counts only when every undone digit is in 1–5. Survivors are ranked by the repo English quadgram model.

This is one family. It is not a search over every square, every transposition, or every cipher in the 1939 book.

## Known-example test (passes)

`tests/test_polybius_gronsfeld.py`

- `test_search_recovers_constructed_plaintext` — plaintext `MEET AT THE HARBOR AFTER THE BELL RINGS AT DAWN`, keyword `alphabet`, key `2718`, null every 5th digit (phase 4, dummy 9). Search returns `MEETATTHEHARBORAFTERTHEBELLRINGSATDAWN`, key `2718`, keyword `alphabet`. Mean quadgram −1.980.
- `test_book_polybius_example_matches_printed_square` — the page's 178-letter A–E example and the printed square. Row then column. Faithful reading, 89 letters: `THENEWPLANOFATTACKINCLUDESOPERATIONSBYTHREEBOMBRSQUDRONSOVERFACTORYARYASOUTHWESTOTHERIVER`. It starts `THENEWPLANOFATTACK` and contains `ARYA`, not `AREA`. The page's prose gloss is three letters longer (`BOMBER`, `SQUADRONS`, `OF`) and is not what those printed pairs produce. The page itself says the exercise contains a mis-encoding.

Command: `python3 -m unittest tests.test_polybius_gronsfeld -v` → 4 tests, OK (about 0.8s).

## Failed search on the challenge

Same function, `max_key_len=4`, null periods 0 and 3–5, every phase.

The 196 pairs are not a mixed digit string. Even positions are only `{0,6,7,8,9}` (one `0`). Odd positions are only `{1,2,3,4,5}`. Subtracting `5,0` on repeat therefore lands in 1–5 for every digit. Keys of length ≤4 with that property: `50`, `4050`, `5050`. That is a partition of the digits, not English. Straight-alphabet reading under `50`, 196 letters, mean quadgram −4.143:

`KBMPQBQDLDQIPODIIMONLCLLIIMBDKNMOQKIENKKKSCEELCLKPKKDBMRPICMKINLELOPDPDPPCMGBNBLLGLDCKMLDNCMPLCCCYILQQOCPOEDPEBTBBPQPQIQGKDEKFENBDILMOBMDQLSEBDOOQNPIQLEGINNPMNDBGBEBNKRGCMMGGNMPOKMLNGOBMNKLDKIPLBR`

Best quadgram inside the keyword list, still not a reading:

| reading | null | key | keyword | letters | mean quadgram |
| --- | --- | --- | ---: | ---: | ---: |
| constructed English control | 5 / phase 4 | 2718 | alphabet | 40 | −1.980 |
| 395 digits | 4 / phase 1 | 550 | ruts | 148 | −3.747 |
| 392 digits (drop final `000`) | 3 / phase 2 | 5004 | like | 131 | −3.705 |
| 392 digits, straight square, key `50` | none | 50 | straight | 196 | −4.143 |

395-digit best, not a claim: `BDLMESGPEIMEDDIGIGCOUUXHKUETHFEGATRGDWFRDNHMHCOGTTLTVLGICTGGHDSUXGTGHIRTANGPTTIMSGVPRDMKUMCVACRIRNGIMHSTORBKKTLETACOIIDSUBATHNBIHCDHINHIHKTDFGNEIRNZ`

392-digit best, not a claim: `GFPIQTEKPRFTOOKEFTISNFQXANGZKWHOGXGRMFFOGTHYOWPTPOCFIECIKYHTKFHMKSHAOOOWPWTCPEQUCWAXAMETMRMUHMITOEPUHXFOPFEDIWNZCOMDNFOYHNOFNYEXPIR`

Why these are not a solution:

1. The Wikipedia page prints no plaintext, and it credits nobody with a solution. Nothing here was matched to a published reading.
2. The English control from the same scorer sits near −1.98 per quadgram. Every challenge candidate sits past −3.7. The gap is more than 1.7.
3. The full-legal keys exist because the digits alternate between `{0,6,7,8,9}` and `{1,2,3,4,5}`, or fall into that split after a null strip. Any square then spells letters. The letters are an artifact of that split.
4. The keyword list's winners contain neither `ATTACK` nor the book's `THENEWPLAN`, and the straight-square string under key `50` does not either.

## Result

The Polybius-Gronsfeld search recovers the constructed cipher and the opening of the book's printed Polybius exercise. It does not recover a published plaintext of the D'Agapeyeff challenge. The challenge stays unsolved here.
