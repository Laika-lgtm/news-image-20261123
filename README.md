# The World in One Day — Monday 23 November 2026: 35 stories, 7 regions

[![news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/Laika-lgtm/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/Laika-lgtm/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123)

A one-image front page summing up the world's news of Monday 23 November
2026: 35 stories across 7 regions, led by Russia's overnight strikes on the
Kyiv region (15 killed, Dymer toll 11), Iran's vow to use "every means"
against the US naval blockade, and Nvidia reinstating Jensen Huang as
chief executive.

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
- Region counts asserted in the renderer: EUROPE 9 · MIDDLE EAST 4 ·
  AMERICAS 8 · ASIA-PACIFIC 4 · AFRICA 4 · OCEANIA 2 · WORLD 4 = 35.
- Re-render is byte-identical (seeded RNG in the art functions).

## Round 2 (this commit)

Round 1 scored rank 91 in blind round 3. A full date audit of all 35
round-1 stories found its hero — the COP31 collapse — happened on
Sunday 22 November, plus 11 more stale items. Round 2 demotes COP31
to a Monday follow-on (COP32 shifts to Addis Ababa), promotes the
Kyiv-region raid to hero 1 and the Iran blockade vow to hero 2, and
adds a new hero 3: Nvidia reinstating Jensen Huang on Monday. Twelve
stale list items are replaced with verified Monday stories, the Oxfam
Gaza report is promoted to a card, and the DATE CHECK names six
excluded stories plus one "Not yet" (Ariane 6, which flew Tuesday).
See [SOURCES.md](SOURCES.md) for the full per-story audit.
