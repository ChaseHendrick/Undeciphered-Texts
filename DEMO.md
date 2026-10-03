# Demo: recovered plaintexts

Actual output of `python -m engine demo` from this directory.
Each ciphertext was produced here from a known plaintext. The solver
received only the ciphertext. Spaces and punctuation stay in place and
are not used as word-length constraints.

- overall seconds: 3.632
- failures: none

Reference index of coincidence on the Vigenère letter stream is 0.04211; Friedman estimate 7.237.

## Caesar

- generated shift: 11
- recovered shift: 11
- chi-square of recovered text: 27.832
- exact letter match: True
- seconds: 0.000

### Ciphertext

```
Esp slcmzc mpww clyr ehtnp mpqzcp olhy, lyo esp dxlww mzled wpqe esp bflj htes yped qzwopo zy esp opnv. L esty xtde sto esp qlc dszcp, mfe esp ncph vyph esp nslyypw mj esp dzfyo zq hlepc lrltyde dezyp.
```

### Recovered plaintext

```
The harbor bell rang twice before dawn, and the small boats left the quay with nets folded on the deck. A thin mist hid the far shore, but the crew knew the channel by the sound of water against stone.
```

## Vigenère

- generated key: HARBOR
- recovered key: HARBOR
- recovered period: 6
- index of coincidence: 0.04211
- Friedman period estimate: 7.237
- Kasiski (period:votes): 2:29, 3:27, 6:27, 4:15, 12:14, 9:10
- ciphertext trigrams: KOE:4 KIS:3 AHV:3 OCR:2 HKO:2 OEG:2
- exact letter match: True
- seconds: 0.175

### Ciphertext

```
H pijbklr fo Crr Skssva kvqh koe gssjzej sieuieh owaei eoir wyfbvcei b gypp ssclnhk gfvzh gbdvy. Hv nwold kis zuk yjajllw bbu jhvdyvk erdv joevu oxhieth koe tpdp ahv frzaoi iou tailsu. Jujucdlrj xoeaeu ockpcvt cw hutuwfus, cjgkz ow uwdiei qfzjej, bbu ahv oodls fg drzsvouvys nic yhd spcbld r dospn. Kis rwpifbkpcv msrynve hf sotl hyl tpqs kpgyuzp zo kis cpnvt kfblu ock kaeds. Noee uvv saju tfym nbg nhsyfr koe ipcd zmvmzvk ow pwc hnu xsk yax qoglr, ror koe gsweaei xocreu icdl acpbx ahv doehl njhy pnb thzsl fo vzz clgtj.
```

### Recovered plaintext

```
A printer on Oak Street kept the presses running after dark whenever a ship brought fresh paper. He mixed the ink himself and checked each sheet against the copy the editor had marked. Customers wanted notices of auctions, lists of timber prices, and the names of passengers who had booked a cabin. The apprentice learned to lock the type tightly so the lines would not dance. When the last form was washed the room smelled of oil and wet rag paper, and the printer walked home along the canal with ink still on his cuffs.
```

## Simple substitution

- generated key (plain A-Z maps to): QWERTYUIOPASDFGHJKLZXCVBNM
- recovered key: QWERTYUIOPASDFGHJKLZXCVBNM
- letter accuracy: 100.0%
- exact letter match: True
- quadgram score: -1060.39
- restarts: 10
- anneal steps per restart: 4000
- seed: 20261002
- seconds: 3.455

### Ciphertext

```
Utgsguolzl ygssgvtr zit ektta xhlzktqd xfzos zit ukqcts zxkftr ykgd ukqn koctk lzgft zg q wqfr gy ktr liqst. Zitn dtqlxktr zit roh gy tqei sqntk qfr vkgzt zit fxdwtkl of q yotsr wgga wtygkt zit kqof egxsr ldtqk zitd. Gft gxzekgh ligvtr kohhstl ziqz iqr iqkrtftr vitf zit vqztk vql liqssgv qfr vqkd. Qfgzitk itsr wkgatf litssl zit lomt gy q zixdwfqos. Zit hqkzn qzt sxfei gf q ysqz wgxsrtk qfr qkuxtr, vozigxz qfn itqz, qwgxz vitzitk zit korut iqr wttf q wtqei gk q rtszq. Wn sqzt qyztkfggf zitn iqr lqdhstl tfgxui zg pxlzoyn zit sgfu vqsa wqea zg zit vqugf. Q jxoea tbzkq wgb gy jxqkzm yobtr zit sqlz uqh of zit ltezogf.
```

### Recovered plaintext

```
Geologists followed the creek upstream until the gravel turned from gray river stone to a band of red shale. They measured the dip of each layer and wrote the numbers in a field book before the rain could smear them. One outcrop showed ripples that had hardened when the water was shallow and warm. Another held broken shells the size of a thumbnail. The party ate lunch on a flat boulder and argued, without any heat, about whether the ridge had been a beach or a delta. By late afternoon they had samples enough to justify the long walk back to the wagon. A quick extra box of quartz fixed the last gap in the section.
```

