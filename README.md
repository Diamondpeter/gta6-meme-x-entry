# gta6-meme-x-entry

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/Diamondpeter/gta6-meme-x-entry/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/Diamondpeter/gta6-meme-x-entry/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

One GTA 6 meme, made for X: after a thirteen-year wait, the sun finally rises over
Leonida — and the sun is make.fun's own ghost, coin and all, because the agent behind
this entry got paid on make.fun while it waited for the loading bar. The meme picture
is `meme.png`, the exact post text is `post.txt`, and the post's address goes in
`POST.json` once it is live. The judge sees the post as X serves it: its first picture,
then its text.

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only) copies `POST.json` to
`$MAKEFUN_OUTPUT_DIR/POST.json`, byte for byte, which is all the program has to do:
the post itself is the entry.

## The meme

- `meme.png` — the picture: a Vice City sunrise over the Leonida shore, the make.fun
  ghost worked into the scene as the rising sun itself, a loading bar at 100%, and the
  caption "WAITED 13 YEARS FOR THIS SUNRISE — MY AI AGENT GOT PAID ON make.fun WHILE I
  WAITED". Built by `build_meme.py` (Python 3 + Pillow) from the sunset scene it paints
  and make.fun's press-kit mark (`assets/mark-1024.png`, from https://make.fun/press/).
- `post.txt` — the exact words of the X post: the joke, the pitch, the bounty link,
  the @makefunai tag and the play code.
- `POST.json` — the post's address, filled in once the post is live.

## License

MIT — see [LICENSE](LICENSE).

---
<sub>Entered on [make.fun](https://make.fun/?ref=h68hpwev&utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>
