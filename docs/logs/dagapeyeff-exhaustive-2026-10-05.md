# Every column order up to width 9, any language, 5 October 2026

A columnar transposition followed by any one-to-one substitution, in any language, leaves one thing a letter key cannot change: put the cells back in the right order and each symbol predicts the next as well as real text does. Successive-symbol information measures that and needs no language model. Earlier passes sampled random column keys and used only widths that divide 196. Van Eykelen (MsgTrail, June 2026) found his one surviving trace in narrow, ragged columns.

`engine.dagapeyeff_exhaustive` tries every order, k! of them, at widths 2 to 9, in three families: columnar undone (rows of k, a short last row allowed, copied out down the columns in key order), columnar done (the same operation applied again, the book's reversed direction), and periodic (each block of k cells permuted by one key). The readings match the repository's own `columnar_encrypt` and `columnar_decrypt`. Width 9 alone is 362,880 orders a text.

The score of the best order depends on the symbol counts, so each text is compared with the best order of shuffles of its own symbols. The margin is the excess.

Planted English and German, each with a random letter key and a random order, beat their shuffles by 0.0345 to 0.301. The margin is widest at small widths and smallest at width 9, where power is thinnest. The printed cells range from -0.0933 to 0.0698, and the regrouped cells from -0.1063 to 0.0447. In all 24 width and family cases, both the printed and the regrouped cells beat their shuffles by less than either planted text beats its own. Across the 72 shuffle comparisons for the printed cells, 33 shuffles score as high as the cells.

The highest best-order score for the printed cells is 0.7969. Every planted text's true order scores 1.0102 or more. A first run compared the regrouped cells with shuffles of the printed cells and showed the regrouping at 1.0187; that comparison was wrong, because regrouping changes the counts, and it was replaced.

Columnar transposition in either direction with a full or short last row, and periodic transposition, at widths 2 to 9, followed by any one-to-one substitution in any language, do not read the cells.

Not a reading. No letter string is stored.

## Width 10

`engine.dagapeyeff_exhaustive10` runs the same three families at width 10, every one of 3,628,800 orders a family, with two shuffles of each text. More orders lift what noise can reach, and here they reach English.

For columnar undone, planted English's best order scores 1.0355 and a shuffle of the same symbols reaches 1.0446; German beats its shuffle by 0.0193. For periodic, English's best is 1.0599 and a shuffle reaches 1.094. A real text no longer stands out in these two families at width 10, so nothing about the cells follows from them. For columnar done, planted English and German beat their shuffles by 0.1319 and 0.2243, the cells by -0.01 and the regrouping by 0.038.

Width 10 is where this method stops. It closes the done direction there and says nothing about the other two families.
