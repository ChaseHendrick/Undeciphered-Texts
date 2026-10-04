# LXACA neighborhood, 4 October 2026

Not solved. No plaintext claimed.

## What is close

The [1941 master list](https://cryptocellar.org/bgac/1941-msg-list.html), updated September 2026, no longer lists MVUEH, FMNGI, AWTZK, ZNLZT, or WEUWY as open. Those breaks are already credited. The rows still unmarked Broken are EHSTQ, AFKZT, RXPSB, KLJBO, LXACA, JBIYH, BYQMZ, FKQLZ, and XFEDT. The last three are the Ultimate Enigma challenge, whose wiring the publisher questions. RXPSB still has no published 28 June key. EHSTQ, KLJBO, and JBIYH have no daily key on the pages checked here.

LXACA is the row the publisher already marks as one day away. On the [July key page](https://cryptocellar.org/bgac/e-keys-july-1941.html), updated 28 September 2026, message 100 is footnoted: received at 04:45, header time 23:40, probably 4 July, and it does not break on the 5 July key. There is no `Enigma keys for 04.07.1941` block on that page. The dates jump from 1 July to 5 July.

## Controls

The repo machine matches two published indicator results before LXACA is touched.

| Check | Result | Published |
| --- | --- | --- |
| 5 July, ground AIK, group SUD | WER | WER, message 101 |
| 9 July, ground NUG, corrected group YKS | SPE | SPE, master-list footnote 44 |
| 9 July, printed group YKI | SPF | The older mismatch |

Decrypting the first 20 letters of DEROP at start WER gives `BETRIEBSSPRUQXKUPPLU`. That is the known Betriebsspruch prefix, with the published garble. Its German quadgram score is -57.06. This is the bar for a 20-letter output from the same scorer. It is not a threshold that was fit to LXACA.

## Attack

Body, after dropping the Kenngruppe LXACA: `ZIXAGNQRKOHBPNKXRLFU`. Indicator as printed: ground OGD, second group PKN. Each day uses that day's rotors, rings, and plugboard. The second group is deciphered at the ground to get the start, then the body is deciphered.

| Date | Walzenlage | Start | Machine output | Score |
| --- | --- | --- | --- | --- |
| 1 July | 423 | YSZ | YCCQTVXHZIOZJHVVEZMM | -77.26 |
| 5 July | 354 | LXI | EXRVWBVWWYDHIINMHFDO | -74.73 |
| 6 July | 513 | ODO | XAZPAKIPQYTEGDJTYKYS | -72.88 |
| 7 July | 245 | HWF | LCMTNMANRXSULQPUMISO | -64.50 |
| 8 July | 432 | IVR | MTSVEQEFBCKILJFBNHDD | -64.85 |
| 9 July | 315 | STI | CHZRYVUPBMNANGEWUYEF | -65.98 |

None of these is a reading. The 5 July line confirms the publisher's note rather than replacing it.

A second lane edits the 5 July indicator. That is the printed pair, the two groups swapped, and each of the 150 one-letter substitutions: 152 settings. One of them scores -54.72, which is higher than the DEROP control's -57.06. The output is `WOYUCFRSONAGVWOPOABE`, from second group PNN and start LLI. It does not read as German. A 20-letter quadgram score can beat a garbled control without being text. The other 151 edits do not beat the control.

## What this does not do

The 4 July key was not invented and not searched. No rotor order outside the six published Walzenlagen was tried. A right key on 20 letters would still not be a unique historical reading. `solved` stays false and `claimed_plaintext` stays null.
