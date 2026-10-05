# A turning grille on the cells, 5 October 2026

196 is 14 squared. A Fleissner grille of 49 holes fills a 14 by 14 square in four turns, and no earlier pass tried one. A grille moves cells and cannot change their counts, so the letter key is still unknown. Each search below has a planted control: 196 training letters, put through a random grille, and for the joint search also through a random letter key.

Successive-symbol information cannot be changed by a letter key. A climb on it reaches 1.2062 on the planted grille, above the true text's 1.0242, while agreeing with the true grille in only 17 of 49 holes. That score picks no grille.

With the letter key given, an annealed quadgram search on the default English model recovers 1 of 3 planted grilles exactly. A second is 47 of 49 and a third is 25 of 49. Agreement is counted up to the turn the grille starts in.

With the grille and the letter key both unknown, the same search recovers 0 of 2. It ends at -3.2517 and -2.9762 per letter, against -2.0111 and -1.7441 for the true texts, and at most 4 key letters right. Shuffled copies of those planted squares reach -3.3426 and -3.126.

On the cells the joint search reaches -3.1388. Four shuffled copies of the cells reach -3.1078, -3.0901, -3.155 and -3.1823, so 2 of 4 do as well.

The model spends 1.9803 nats a letter on held-out prose, which saves 1.8435 bits a letter against uniform letters. A grille is 98 bits and a key for 18 symbols is 73.08 bits. One key should stand out after about 92.8 letters. The cells have 196. A correct grille and key would score near -2, far above anything a shuffle reaches. The search cannot find one.

The grille class is not closed. A score near a shuffle's is not a reading. No letter string is stored.
