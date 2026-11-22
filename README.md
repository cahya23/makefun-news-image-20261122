# The World Today — 22 November 2026

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/cahya23/makefun-news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/cahya23/makefun-news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

A one-page newspaper front page summing up world news on Sunday, 22 November 2026.

## What the image shows

Masthead **THE WORLD TODAY**, dated Sunday, 22 November 2026, above a lead
story on the COP31 climate summit, a night-sky panel on the war in Ukraine,
and smaller stories on the Baltic, the peace talks and the ATP Finals.
Everything is drawn from scratch with Python's standard library only — a
hand-made 5x7 bitmap font and a hand-written PNG encoder — no photographs
or copied images.

## The stories

1. **COP31 DEAL GOES TO VOTE WITHOUT A WORD ON FOSSIL FUELS** — After two
   days in overtime, negotiators in Antalya were handed a final text in the
   early hours of Sunday. It sets a 35% electrification goal for 2035,
   drops the $120bn adaptation-finance target, and never names fossil
   fuels. Delegates vote today. (Multiple outlets, 22 Nov 2026.)
2. **NIGHT OF DRONES OVER UKRAINE** — Russia fired 148 drones and 3
   ballistic missiles overnight. At least 2 people were killed and 83
   wounded. Kryvyi Rih was hit hardest: a boy of 7 and a paramedic died
   there. (Ukraine Monitor daily briefing, 22 Nov 2026.)
3. **SHIP HIT IN THE BALTIC** — Ukrainian drones hit the Russian cargo
   ship Sparta II in the Gulf of Finland. Finland said the ship drifted
   into its waters. (Ukraine Monitor daily briefing, 22 Nov 2026.)
4. **TRUMP PRESSES FOR UKRAINE DEAL BY EARLY JANUARY** — The US president
   is preparing what he calls a large-scale ceasefire, as Kyiv forms a
   European negotiating group with Poland, Britain, Germany, France and
   Italy. (Financial Times, via Ukraine Monitor, 22 Nov 2026.)
5. **FINAL TONIGHT: ZVEREV v ALCARAZ** — World No. 1 Alexander Zverev
   meets Carlos Alcaraz in the ATP Finals title match in Turin at 18:00
   CET. Alcaraz chases a first title on a 13-match winning run; Zverev
   chases a third crown. (ATP Tour, 22 Nov 2026.)
6. **ALSO TODAY** — Gaza: 4 killed, 14 hurt in ceasefire breaches; US
   sanctions 14 Iranians over oil sales; tanker hit by projectile near
   Oman. (Reports dated Sun 22 Nov 2026.)

## Build

```bash
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` paints the page pixel by pixel and encodes the PNG by hand with
`zlib` and `struct`. It reads no files, uses no network and no randomness,
so two runs write identical bytes.
