# Alexander d'Agapeyeff, the man, 4 October 2026

Not a reading of the cipher. Two later men are easy to mix up with him. This note keeps them apart. Lines marked "read here" were checked against the London Gazette in this session. The rest are catalogue or index entries found in the same search and not re-opened.

## The author

Born 20 May 1902. The National Archives title for Special Operations Executive personnel file HS 9/9/5 is "Alexander D'AGAPEYEFF - born 20.05.1902" (1939-1946). An older transcription of that series prints "20.05.1900 or 1902" for the same reference. Saint Petersburg is only on an unsourced Find a Grave memorial. No parents, school, or degree turned up. "Fellow of the Royal Geographical Society" is repeated on cipher blogs and was not found in a membership list.

He was a Russian national. London Gazette, 23 May 1947, issue 37963, the April 1947 naturalisation list (read here): "Agapeyeff, Alexander d'; Russia; Serving Officer in His Majesty's Forces; Keeley Cottage, Campden, Gloucestershire. 17 March, 1947." That date is the oath. A catalogue entry for duplicate certificate HO 334/173/23658 gives the certificate date as 28 February 1947, residence Campden, wife's name Rachel.

Died 22 March 1955, aged 52. London Gazette, 13 April 1956, issue 40753 (read here): Alexander D'AGAPEYEFF, Maugersbury Manor, Stow-on-the-Wold, Gloucestershire, Wing Commander, R.A.F., personal representative Rachel d'Agapeyeff, solicitors Francis, Wickins and Hill. A 2026 site that says he died in 1969 is wrong. Fairford as the place of death, and a grave at Stow-on-the-Wold Cemetery, are on Find a Grave only.

## Family

Civil-registration indexes, not certificates:

| When | What | Index |
| --- | --- | --- |
| Sep quarter 1924 | Alexander Agapeyeff and Josephine C. L. P. Adams | Stow (Suffolk), 4a/2373 |
| 1929 | Divorce petition, Josephine Christian Lilian Passy d'Agapeyeff against Alexander | National Archives J 77/2621/1445. The result is not in the catalogue title. |
| Dec quarter 1929 | Josephine C. L. D'Agapeyeff remarries Valentine W. Eyre | St George Hanover Square, 1a/1108 |
| Sep quarter 1932 | Alexandre D'Agapeyeff and Gladena S. Cruickshank | Kensington, 1a/502 |
| Dec quarter 1933 | Birth of Alexander P. E. D'Agapeyeff, mother Cruikshank | Chelsea, 1a/357 |
| Sep quarter 1939 | Rachel Wood and d'Agapeyeff | Shipston, 6d/3965 |
| Sep quarter 1940 | Birth of Grizelda D'Agapeyeff, mother Wood | North Cotswold, 6a/1295. The index does not name the father. |

A digital text of the April 1939 preface of *Codes and Ciphers* thanks Rachel Wood for research. The 1956 estate names Rachel d'Agapeyeff. That is the match. It is not a certificate.

The son Alexander Peter Emanuel d'Agapeyeff was a different public man: president of the British Computer Society, OBE in the 1972 New Year Honours (London Gazette, 31 December 1971), died 26 March 2003. Robert Matthews wrote that this son remembered amateurs bringing his father failed solutions, and the father's embarrassment, and that the son did not think the cipher was a hoax. The son had no method and no plaintext. Matthews does not quote the father saying he forgot.

## What he did

He did not found Geographia Ltd. That firm was Alexander Gross's, from 1908 or 1911. No Gazette or company record found here puts d'Agapeyeff on its board. "Cartographer in Lake Chad" is one unsourced blog sentence.

Books, from library catalogues:

- *Codes and Ciphers*, Oxford University Press, 1939, Meridian Books, about 160 pages. The challenge is on page 158, the last page of the last chapter. The line on that page is "Here is a cryptogram upon which the reader is invited to test his skill." Page 144 is the revised book, not this one.
- 1949, "Revised and reset," G. Cumberlege / Oxford University Press, 149 pages, Compass Books 1. The challenge is not in it. Matthews, and booksellers of the 1939 copy, say it was deleted.
- 1952 is a second impression of that shorter book, not a third edition.
- 1974, Gale Research, Detroit, reprints the 160-page 1939 text. Later Hesperides reprints of about 149 pages follow the cut text.
- *Maps*, with E. C. R. Hadfield, Oxford University Press, 1942 (Meridian), reprint 1945, second edition 1950 (199 pages), 1953 reprint. This is after the cipher book, not before it.

## The Air Force

Service number 87808, Royal Air Force Volunteer Reserve, then the Secretarial Branch. Read here: London Gazette, 3 December 1940, issue 35005, Administrative and Special Duties Branch, 1 November 1940, Alexander D'AGAPEYEFF (87808). Read here: London Gazette, 8 February 1949, issue 38532, "Dismissal by sentence of General Court Martial," Wing Commander A. d'AGAPEYEFF (87808), 18 January 1949. The charge is not printed. The 1956 estate notice still styles him Wing Commander, R.A.F.

A research pass through the Gazette also has, same number: Flying Officer in 1941, Flight Lieutenant (temporary) from 1 January 1943, war-substantive Squadron Leader from 16 April 1946, extended-service Squadron Leader in autumn 1946, Secretarial Branch from 1 January 1947. Those pages were not re-opened for this note.

An SOE personnel file exists (HS 9/9/5). A file is not a posting. Nothing here says he was an agent. No Times obituary, no portrait of this man, and no lecture or BBC record turned up. The 1971 photograph is the son.

## The "he forgot" story

No letter, preface, or sentence in his own words was found. A 2026 claim of a 1952 letter tucked in a bookmark has no image and pairs it with the wrong death year. What is on paper is narrower: the puzzle is only in the 1939 book, it was cut from the shorter edition, strangers pestered him, and his son was embarrassed for him and could not reconstruct it.

## A record a model can query

`engine/data/dagapeyeff_life.json` is the same material as one list of facts. Each fact has an id, a date, a source, a confidence (`gazette`, `catalogue`, `index`, `secondary`, or `rejected`), and aliases. `search_life("87808")` returns the commission and the dismissal. `search_life("1969")` returns the rejected death. `search_life("forgot")` returns the rejected confession.

## Keys taken from that list

Names and numbers he could have used in 1939 were scored apart from names and numbers from 1940 onward. Column order was applied to a frequency ranking of the 196 cells, which is not a solved alphabet. A package of random column orders the same size beat the 1939 names 46 times in 100. The later names, which he could not have chosen when he wrote the book, were beaten 8 times in 100. Neither is kept.

His birth date, read as the digits 20051902, and the service number 87808 were used as a repeating shift of the 25 cells. The birth date scores 21.64 and the service number 18.55, against 34.23 for the printed pairs. A random five-digit shift has median about 15, and most of those random shifts beat both of his numbers. The improvement is what a shift does, not what his life does. No letter string is stored.

