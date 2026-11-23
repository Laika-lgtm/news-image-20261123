# The World in One Day — Monday 23 November 2026: 35 stories, 7 regions

[![news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/Laika-lgtm/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/Laika-lgtm/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123)

A one-image front page summing up the world's news of Monday 23 November
2026: 35 stories across 7 regions, led by the COP31 collapse in Antalya,
Russia's overnight strikes on the Kyiv region (Dymer toll 11), and Iran's
vow to use "every means" against the US naval blockade.

## The image

`entry.png` (1024×1024) is a newspaper front page: masthead, a 3-story
kicker, a 6-number stat strip, a 7-region bar, a THE DAY IN UTC strip,
3 illustrated heroes with certainty tags (REPORTED / CLAIM), 10 numbered
cards, a dotted world map with numbered pins, a numbered "ALSO ON" list
of 22 more stories, a CERTAINTY legend, and a DATE CHECK box that names
the neighbouring days' news left out on purpose. Every story was
reported, or was still developing, on 23 November 2026 in at least one
time zone, and every figure was verified against a live source — see
[SOURCES.md](SOURCES.md).

## How it is built

- `stories.json` — the 35 verified stories (title, deck, region,
  source) that the page is drawn from.
- `render_frontpage.py` — the build-time renderer (PIL). It draws the
  whole page, including every illustration and the dotted map, in code.
  Run it with `python3 render_frontpage.py` to regenerate `entry.png`.
- `main.py` — the graded entrypoint (stdlib only). It copies the
  pre-rendered `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`.

## Verification

- Wires read up to 14:00 UTC, Monday 23 November 2026.
- Region counts asserted in the renderer: EUROPE 8 · MIDDLE EAST 4 ·
  AMERICAS 8 · ASIA-PACIFIC 3 · AFRICA 2 · OCEANIA 2 · WORLD 8 = 35.
- Re-render is byte-identical (seeded RNG in the art functions).
