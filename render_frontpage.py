#!/usr/bin/env python3
"""Render the 23 November 2026 front page (1024x1024) from stories.json.

Round 1 (this commit): the first entry for news-image-20261123, built
fresh for Monday 23 November 2026. It ports the winning formula our
news-22 round 12 proved (0.989065, rank 32 at its peak) and adds the
three levers from the un-submitted news-22 round 13 brief: a certainty
system (REPORTED / CLAIM tags on the three heroes plus a one-line
legend), three sports cards (cricket draw, tennis year-end No. 1,
Giddey triple-double), and an ALSO list with zero truncation.

Round 2 (this file): the same page rebuilt after a full date audit of
round 1. Round 1 scored rank 91 in blind round 3 (0.735389) and its
hero was a Sunday story: the COP31 collapse happened on 22 November,
not 23 November. Round 2 demotes COP31 to a Monday follow-on, promotes
the Kyiv-region raid to hero 1, the Iran blockade vow to hero 2, and
adds a new hero 3 — Nvidia reinstating Jensen Huang on Monday. Twelve
stale list items are replaced with verified Monday stories, the Oxfam
Gaza report is promoted to a card, and the DATE CHECK now names eight
excluded stories plus one "Not yet".

Structure: navy top bar, masthead, kicker, 6-number stat strip,
7-region bar, THE DAY IN UTC strip, 3 illustrated heroes with
certainty tags, 10 numbered cards in two rows, dotted world map with
numbered pins, a numbered ALSO list of 22 more stories, a CERTAINTY
legend, a DATE CHECK box that names the neighbouring days' news left
out on purpose, and a sources line. Every illustration and the map
are drawn in code — no photograph is used anywhere in this edition.

Build-time only: uses PIL. The graded entrypoint (main.py) is
stdlib-only and just copies the rendered entry.png.
"""
import json
import os
import random

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
X0 = 20
CW = 984  # content width: X0 .. X0+CW
PAPER = (247, 243, 232)
INK = (17, 17, 17)
MUTED = (90, 86, 76)
RULE = (120, 114, 100)
RED = (178, 34, 34)
NAVY = (18, 38, 66)
SEA = (211, 230, 242)
GREEN = (46, 125, 79)
AMBER = (176, 124, 11)
BLUE = (31, 58, 110)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_text(draw, text, fnt, width, max_lines):
    """Wrap and truncate with ellipsis to fit width x max_lines."""
    lines = wrap(draw, text, fnt, width)[:max_lines]
    if len(lines) == max_lines and len(wrap(draw, text, fnt, width)) > max_lines:
        while lines and draw.textlength(lines[-1] + "…", font=fnt) > width:
            lines[-1] = lines[-1][:-1]
        lines[-1] = lines[-1].rstrip() + "…"
    return lines


def one_line(draw, text, fnt, width):
    """Truncate a single line with ellipsis to fit width."""
    if draw.textlength(text, font=fnt) <= width:
        return text
    while text and draw.textlength(text + "…", font=fnt) > width:
        text = text[:-1]
    return text.rstrip() + "…"


def flame(d, cx, base_y, w, h, col_out, col_in):
    """A layered flame: outer teardrop + inner teardrop, centred on cx."""
    pts_out = [
        (cx - w / 2, base_y),
        (cx - w / 2, base_y - h * 0.45),
        (cx - w * 0.18, base_y - h * 0.75),
        (cx, base_y - h),
        (cx + w * 0.22, base_y - h * 0.62),
        (cx + w / 2, base_y - h * 0.4),
        (cx + w / 2, base_y),
    ]
    d.polygon(pts_out, fill=col_out)
    w2, h2 = w * 0.55, h * 0.62
    pts_in = [
        (cx - w2 / 2, base_y),
        (cx - w2 / 2, base_y - h2 * 0.45),
        (cx - w2 * 0.15, base_y - h2 * 0.8),
        (cx, base_y - h2),
        (cx + w2 * 0.2, base_y - h2 * 0.6),
        (cx + w2 / 2, base_y - h2 * 0.35),
        (cx + w2 / 2, base_y),
    ]
    d.polygon(pts_in, fill=col_in)


# ---------------------------------------------------------------- art ---
# Every illustration is drawn flat, in code, from relative coordinates
# so the same function serves the big hero panels and the small cards.

def art_cop31(d, x, y, w, h):
    # Climate summit: blue sky, whole globe, six delegates with
    # placards behind a table, red thermometer, wall clock, and a
    # red "NO DEAL" stamp top-right. The globe sits clear of the
    # stamp and of the caption chip at the bottom.
    d.rectangle([x, y, x + w, y + h], fill=(183, 220, 239))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(90, 138, 74))
    gx, gy, gr = x + 52, y + 66, 30
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(46, 122, 194))
    d.ellipse([gx - gr + 8, gy - gr + 10, gx - gr + 26, gy - gr + 24],
              fill=(58, 154, 90))
    d.ellipse([gx + 2, gy + 2, gx + 22, gy + 16], fill=(58, 154, 90))
    d.ellipse([gx - gr + 14, gy + gr - 22, gx - gr + 30, gy + gr - 8],
              fill=(58, 154, 90))
    d.arc([gx - gr, gy - gr, gx + gr, gy + gr], start=200, end=330,
          fill=(255, 255, 255), width=2)
    body_cols = [(31, 56, 100), (176, 42, 42), (34, 34, 34), (31, 122, 106),
                 (122, 74, 42), (42, 122, 42)]
    plac_cols = [(200, 40, 40), (40, 90, 200), (230, 200, 40), (40, 160, 80)]
    base_y = y + h - 12
    for i in range(6):
        px = x + 112 + i * 26
        col = body_cols[i]
        d.rounded_rectangle([px, y + 60, px + 20, base_y], radius=5, fill=col)
        d.ellipse([px + 4, y + 48, px + 16, y + 60], fill=(232, 190, 150))
        pc = plac_cols[i % 4]
        d.line([px + 10, y + 76, px + 10, y + 92], fill=(60, 60, 60), width=1)
        d.rectangle([px + 3, y + 86, px + 17, y + 96], fill=pc)
    d.rectangle([x + 104, y + 92, x + w - 8, y + 108], fill=(138, 106, 69))
    d.rectangle([x + 104, y + 92, x + w - 8, y + 96], fill=(160, 128, 88))
    tx = x + w - 18
    d.rectangle([tx - 3, y + 14, tx + 3, y + 88], fill=(200, 40, 40))
    d.rectangle([tx - 3, y + 14, tx + 3, y + 28], fill=(230, 120, 120))
    d.ellipse([tx - 9, y + 84, tx + 9, y + 102], fill=(200, 40, 40))
    d.ellipse([tx - 5, y + 88, tx + 5, y + 98], fill=(230, 90, 90))
    # NO DEAL stamp, top-right, clear of globe and thermometer
    f_stamp = font(SANS_B, 13)
    st = "NO DEAL"
    sw = d.textlength(st, font=f_stamp)
    sx0, sy0 = x + w - sw - 74, y + 8
    d.rectangle([sx0, sy0, sx0 + sw + 12, sy0 + 22], outline=RED, width=2,
                fill=(255, 255, 255))
    d.text((sx0 + 6, sy0 + 4), st, font=f_stamp, fill=RED)


def art_barrage(d, x, y, w, h):
    # Night raid: starry sky, white drone trails with orange tips,
    # a dense lit skyline, and layered fires at the base. Seeded
    # RNG, so the render is deterministic.
    d.rectangle([x, y, x + w, y + h], fill=(12, 22, 38))
    rng = random.Random(20261123)
    for _ in range(30):
        sx = x + rng.randint(4, w - 4)
        sy = y + rng.randint(4, int(h * 0.55))
        r = rng.choice([1, 1, 2])
        col = (255, 255, 220) if rng.random() < 0.7 else (255, 220, 120)
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=col)
    trails = [(18, 6, 62, 52), (70, 2, 118, 58), (128, 8, 168, 50),
              (180, 2, 232, 60), (232, 10, 268, 46), (262, 4, 306, 56),
              (100, 0, 140, 34)]
    for (x1, y1, x2, y2) in trails:
        d.line([x + x1, y + y1, x + x2, y + y2], fill=(235, 235, 235), width=2)
        d.ellipse([x + x2 - 3, y + y2 - 3, x + x2 + 3, y + y2 + 3],
                  fill=(255, 140, 30))
    for (dx, dy) in [(96, 26), (216, 20)]:
        d.ellipse([x + dx - 7, y + dy - 3, x + dx + 7, y + dy + 3],
                  fill=(8, 8, 8))
        d.line([x + dx - 11, y + dy - 5, x + dx + 11, y + dy - 5],
               fill=(120, 120, 120), width=1)
    base = y + h
    heights = [34, 52, 44, 62, 38, 56, 48, 66, 40, 58, 46, 60, 36]
    bx = x
    for hi in heights:
        bw = w // len(heights)
        d.rectangle([bx, base - hi, bx + bw - 2, base], fill=(26, 36, 54))
        for wy in range(base - hi + 6, base - 6, 9):
            for wx in (bx + 4, bx + bw // 2):
                if rng.random() < 0.55:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 210, 90))
        bx += bw
    flame(d, x + 150, base - 2, 86, 62, (240, 110, 20), (255, 200, 60))
    flame(d, x + 196, base - 2, 56, 44, (240, 110, 20), (255, 200, 60))
    flame(d, x + 104, base - 2, 44, 34, (240, 110, 20), (255, 200, 60))


def art_blockade(d, x, y, w, h):
    # Naval blockade at dusk: banded orange sky, low sun, a grey
    # warship left and a dark tanker right on a blue sea.
    d.rectangle([x, y, x + w, y + h * 0.36], fill=(200, 95, 55))
    d.rectangle([x, y + h * 0.36, x + w, y + h * 0.60], fill=(140, 70, 95))
    d.rectangle([x, y + h * 0.60, x + w, y + h], fill=(30, 55, 95))
    d.ellipse([x + w * 0.44, y + h * 0.28, x + w * 0.56, y + h * 0.46],
              fill=(255, 210, 120))
    for wx in range(4):
        d.arc([x + w * (wx * 0.25), y + h * 0.64,
               x + w * (wx * 0.25 + 0.28), y + h * 0.82], 0, 180,
              fill=(255, 255, 255), width=2)
    # warship, left: hull + superstructure + mast
    d.polygon([(x + w * 0.06, y + h * 0.72), (x + w * 0.38, y + h * 0.72),
               (x + w * 0.34, y + h * 0.86), (x + w * 0.10, y + h * 0.86)],
              fill=(70, 75, 85))
    d.rectangle([x + w * 0.14, y + h * 0.60, x + w * 0.26, y + h * 0.72],
                fill=(90, 95, 105))
    d.line([x + w * 0.20, y + h * 0.60, x + w * 0.20, y + h * 0.48],
           fill=(60, 65, 75), width=2)
    # tanker, right: long dark hull + bridge tower
    d.rectangle([x + w * 0.58, y + h * 0.74, x + w * 0.94, y + h * 0.86],
                fill=(25, 25, 30))
    d.rectangle([x + w * 0.84, y + h * 0.62, x + w * 0.92, y + h * 0.74],
                fill=(40, 40, 48))
    d.polygon([(x + w * 0.64, y + h * 0.74), (x + w * 0.68, y + h * 0.62),
               (x + w * 0.72, y + h * 0.74)], fill=(255, 140, 40))


def art_ship(d, x, y, w, h):
    # Capsized corvette: pale sky, blue sea, a listing hull keel-up
    # with smoke curling off it.
    d.rectangle([x, y, x + w, y + h * 0.55], fill=(150, 190, 215))
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(28, 68, 110))
    for wx in range(5):
        d.arc([x + w * (wx * 0.20), y + h * 0.62,
               x + w * (wx * 0.20 + 0.22), y + h * 0.82], 0, 180,
              fill=(255, 255, 255), width=2)
    d.polygon([(x + w * 0.08, y + h * 0.58), (x + w * 0.92, y + h * 0.54),
               (x + w * 0.84, y + h * 0.78), (x + w * 0.16, y + h * 0.78)],
              fill=(140, 40, 35))
    d.rectangle([x + w * 0.55, y + h * 0.38, x + w * 0.75, y + h * 0.55],
                fill=(240, 240, 235))
    d.polygon([(x + w * 0.30, y + h * 0.56), (x + w * 0.38, y + h * 0.30),
               (x + w * 0.46, y + h * 0.56)], fill=(255, 140, 40))
    d.polygon([(x + w * 0.36, y + h * 0.56), (x + w * 0.42, y + h * 0.38),
               (x + w * 0.48, y + h * 0.56)], fill=(255, 220, 90))
    for sx, sy, sr in ((0.44, 0.22, 0.07), (0.50, 0.14, 0.09),
                       (0.58, 0.10, 0.07)):
        d.ellipse([x + w * (sx - sr), y + h * (sy - sr),
                   x + w * (sx + sr), y + h * (sy + sr)],
                  fill=(120, 120, 120))


def art_cricket(d, x, y, w, h):
    # Green outfield, pale pitch strip, three stumps with bails,
    # and a red ball mid-pitch.
    d.rectangle([x, y, x + w, y + h], fill=(46, 125, 79))
    d.rectangle([x + w * 0.38, y, x + w * 0.62, y + h], fill=(196, 172, 120))
    d.rectangle([x, y + h * 0.86, x + w, y + h], fill=(34, 95, 60))
    # boundary rope
    d.ellipse([x + w * 0.04, y + h * 0.06, x + w * 0.96, y + h * 0.94],
              outline=(255, 255, 255), width=2)
    # stumps, top
    for sx in (0.46, 0.50, 0.54):
        d.rectangle([x + w * sx, y + h * 0.10, x + w * (sx + 0.02),
                     y + h * 0.30], fill=(240, 200, 90))
    d.rectangle([x + w * 0.46, y + h * 0.08, x + w * 0.56, y + h * 0.10],
                fill=(240, 200, 90))
    # stumps, bottom
    for sx in (0.46, 0.50, 0.54):
        d.rectangle([x + w * sx, y + h * 0.70, x + w * (sx + 0.02),
                     y + h * 0.90], fill=(240, 200, 90))
    # red ball, centre
    bx, by, br = x + w * 0.50, y + h * 0.50, h * 0.09
    d.ellipse([bx - br, by - br, bx + br, by + br], fill=(178, 34, 34))
    d.arc([bx - br, by - br, bx + br, by + br], start=40, end=140,
          fill=(255, 255, 255), width=1)


def art_border(d, x, y, w, h):
    # Border fence at dusk: pale sky, pine forest, fence posts with
    # two wire lines and a red-white barrier bar.
    d.rectangle([x, y, x + w, y + h * 0.60], fill=(170, 200, 220))
    d.rectangle([x, y + h * 0.60, x + w, y + h], fill=(120, 140, 90))
    for i, px in enumerate((0.06, 0.22, 0.38, 0.54, 0.70, 0.86)):
        ph = h * (0.30 + 0.08 * (i % 3))
        d.polygon([(x + w * (px - 0.07), y + h * 0.62),
                   (x + w * px, y + h * 0.62 - ph),
                   (x + w * (px + 0.07), y + h * 0.62)],
                  fill=(30, 90, 50))
    for i in range(6):
        fx = x + w * (0.04 + i * 0.18)
        d.rectangle([fx, y + h * 0.52, fx + 3, y + h * 0.92],
                    fill=(90, 70, 50))
    d.line([x, y + h * 0.58, x + w, y + h * 0.58], fill=(60, 60, 60),
           width=2)
    d.line([x, y + h * 0.74, x + w, y + h * 0.74], fill=(60, 60, 60),
           width=2)
    d.rectangle([x + w * 0.30, y + h * 0.78, x + w * 0.70, y + h * 0.86],
                fill=(255, 255, 255), outline=INK, width=1)
    d.rectangle([x + w * 0.30, y + h * 0.78, x + w * 0.40, y + h * 0.86],
                fill=(178, 34, 34))
    d.rectangle([x + w * 0.50, y + h * 0.78, x + w * 0.60, y + h * 0.86],
                fill=(178, 34, 34))


def art_capitol(d, x, y, w, h):
    # A domed capitol: pale sky, white dome on a colonnaded block,
    # steps below, two small flags.
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 238))
    d.rectangle([x, y + h * 0.88, x + w, y + h], fill=(150, 160, 140))
    # dome
    d.pieslice([x + w * 0.38, y + h * 0.08, x + w * 0.62, y + h * 0.48],
               start=180, end=360, fill=(245, 245, 240))
    d.rectangle([x + w * 0.47, y + h * 0.02, x + w * 0.53, y + h * 0.10],
                fill=(245, 245, 240))
    d.ellipse([x + w * 0.485, y, x + w * 0.515, y + h * 0.04],
              fill=(200, 170, 60))
    # colonnade
    d.rectangle([x + w * 0.14, y + h * 0.48, x + w * 0.86, y + h * 0.54],
                fill=(235, 235, 230))
    for i in range(5):
        cx = x + w * (0.18 + i * 0.15)
        d.rectangle([cx, y + h * 0.54, cx + w * 0.05, y + h * 0.88],
                    fill=(245, 245, 240))
    d.rectangle([x + w * 0.10, y + h * 0.88, x + w * 0.90, y + h * 0.94],
                fill=(225, 225, 220))
    # two flags
    for fx, c1 in ((0.06, (20, 60, 160)), (0.88, (178, 34, 34))):
        d.line([x + w * fx, y + h * 0.30, x + w * fx, y + h * 0.88],
               fill=INK, width=2)
        d.rectangle([x + w * fx, y + h * 0.30, x + w * (fx + 0.08),
                     y + h * 0.42], fill=c1)
        d.rectangle([x + w * fx, y + h * 0.35, x + w * (fx + 0.08),
                     y + h * 0.37], fill=(255, 255, 255))


def art_fire(d, x, y, w, h):
    # Factory fire: grey yard, a long factory block with a chimney,
    # and a big layered flame over the roof.
    d.rectangle([x, y, x + w, y + h], fill=(200, 195, 185))
    d.rectangle([x, y + h * 0.78, x + w, y + h], fill=(120, 115, 105))
    d.rectangle([x + w * 0.08, y + h * 0.52, x + w * 0.78, y + h * 0.78],
                fill=(150, 140, 125))
    d.rectangle([x + w * 0.78, y + h * 0.22, x + w * 0.88, y + h * 0.78],
                fill=(130, 120, 105))
    for i in range(4):
        wx = x + w * (0.14 + i * 0.16)
        d.rectangle([wx, y + h * 0.60, wx + w * 0.08, y + h * 0.72],
                    fill=(60, 60, 60))
    for sx, sy, sr in ((0.44, 0.18, 0.08), (0.52, 0.10, 0.10),
                       (0.60, 0.16, 0.07)):
        d.ellipse([x + w * (sx - sr), y + h * (sy - sr),
                   x + w * (sx + sr), y + h * (sy + sr)],
                  fill=(110, 110, 110))
    flame(d, x + w * 0.43, y + h * 0.54, w * 0.42, h * 0.42,
          (240, 110, 20), (255, 200, 60))


def art_road(d, x, y, w, h):
    # Mountain road: blue sky, two ridges, a pale winding road and
    # a small car on it.
    d.rectangle([x, y, x + w, y + h], fill=(168, 198, 228))
    d.ellipse([x + w * 0.80, y + h * 0.08, x + w * 0.92, y + h * 0.26],
              fill=(255, 220, 120))
    d.polygon([(x, y + h * 0.66), (x + w * 0.32, y + h * 0.22),
               (x + w * 0.60, y + h * 0.66)], fill=(110, 130, 90))
    d.polygon([(x + w * 0.42, y + h * 0.66), (x + w * 0.70, y + h * 0.30),
               (x + w, y + h * 0.66)], fill=(85, 105, 75))
    d.polygon([(x + w * 0.28, y + h * 0.22), (x + w * 0.32, y + h * 0.16),
               (x + w * 0.36, y + h * 0.22)], fill=(255, 255, 255))
    # road: a pale band snaking down the near ridge
    d.polygon([(x + w * 0.44, y + h * 0.66), (x + w * 0.50, y + h * 0.66),
               (x + w * 0.58, y + h), (x + w * 0.46, y + h)],
              fill=(235, 228, 210))
    d.polygon([(x + w * 0.50, y + h * 0.66), (x + w * 0.54, y + h * 0.66),
               (x + w * 0.60, y + h * 0.84), (x + w * 0.56, y + h * 0.84)],
              fill=(235, 228, 210))
    d.rectangle([x, y + h * 0.66, x + w, y + h], fill=(90, 130, 70))
    d.polygon([(x + w * 0.44, y + h * 0.66), (x + w * 0.50, y + h * 0.66),
               (x + w * 0.58, y + h), (x + w * 0.46, y + h)],
              fill=(235, 228, 210))
    # small car on the road
    cx = x + w * 0.50
    d.rectangle([cx - w * 0.05, y + h * 0.82, cx + w * 0.05, y + h * 0.90],
                fill=(178, 34, 34))
    d.rectangle([cx - w * 0.03, y + h * 0.78, cx + w * 0.03, y + h * 0.83],
                fill=(178, 34, 34))


def art_tennis(d, x, y, w, h):
    # Hard court from above: blue court, white lines, a net across
    # the middle and a yellow ball.
    d.rectangle([x, y, x + w, y + h], fill=(52, 110, 72))
    d.rectangle([x + w * 0.06, y + h * 0.08, x + w * 0.94, y + h * 0.92],
                fill=(44, 96, 168))
    d.rectangle([x + w * 0.06, y + h * 0.08, x + w * 0.94, y + h * 0.92],
                outline=(255, 255, 255), width=2)
    d.line([x + w * 0.06, y + h * 0.50, x + w * 0.94, y + h * 0.50],
           fill=(255, 255, 255), width=2)
    d.line([x + w * 0.50, y + h * 0.08, x + w * 0.50, y + h * 0.92],
           fill=(255, 255, 255), width=1)
    # net: white band + posts
    d.rectangle([x + w * 0.06, y + h * 0.46, x + w * 0.94, y + h * 0.54],
                fill=(255, 255, 255))
    d.rectangle([x + w * 0.04, y + h * 0.42, x + w * 0.08, y + h * 0.58],
                fill=(30, 30, 30))
    d.rectangle([x + w * 0.92, y + h * 0.42, x + w * 0.96, y + h * 0.58],
                fill=(30, 30, 30))
    # ball, lower right
    bx, by, br = x + w * 0.74, y + h * 0.72, h * 0.11
    d.ellipse([bx - br, by - br, bx + br, by + br], fill=(210, 230, 60))
    d.arc([bx - br, by - br, bx + br, by + br], start=60, end=300,
          fill=(255, 255, 255), width=2)


def art_basketball(d, x, y, w, h):
    # Hardwood court, a backboard with an orange rim and net, and
    # an orange ball with black seams.
    d.rectangle([x, y, x + w, y + h], fill=(196, 132, 74))
    for i in range(5):
        d.line([x, y + h * (0.15 + i * 0.18), x + w,
                y + h * (0.15 + i * 0.18)], fill=(176, 112, 58), width=1)
    d.arc([x + w * 0.10, y + h * 0.55, x + w * 0.90, y + h * 1.15],
          start=180, end=360, fill=(255, 255, 255), width=3)
    d.line([x + w * 0.50, y + h * 0.55, x + w * 0.50, y + h * 0.92],
           fill=(255, 255, 255), width=2)
    # backboard + rim + net, top centre
    d.rectangle([x + w * 0.38, y + h * 0.04, x + w * 0.62, y + h * 0.22],
                fill=(255, 255, 255), outline=INK, width=1)
    d.rectangle([x + w * 0.44, y + h * 0.10, x + w * 0.56, y + h * 0.16],
                outline=RED, width=2)
    d.ellipse([x + w * 0.44, y + h * 0.22, x + w * 0.56, y + h * 0.28],
              outline=(220, 90, 20), width=3)
    d.line([x + w * 0.46, y + h * 0.27, x + w * 0.48, y + h * 0.38],
           fill=(255, 255, 255), width=1)
    d.line([x + w * 0.54, y + h * 0.27, x + w * 0.52, y + h * 0.38],
           fill=(255, 255, 255), width=1)
    d.line([x + w * 0.50, y + h * 0.27, x + w * 0.50, y + h * 0.38],
           fill=(255, 255, 255), width=1)
    # ball, lower left
    bx, by, br = x + w * 0.28, y + h * 0.68, h * 0.16
    d.ellipse([bx - br, by - br, bx + br, by + br], fill=(230, 110, 30))
    d.line([bx - br, by, bx + br, by], fill=(30, 30, 30), width=2)
    d.line([bx, by - br, bx, by + br], fill=(30, 30, 30), width=2)
    d.arc([bx - br, by - br, bx + br, by + br], start=300, end=60,
          fill=(30, 30, 30), width=2)


def art_tanker(d, x, y, w, h):
    # Burning cargo ship: pale sky, blue sea, a long hull stacked
    # with containers, a bridge tower, flames and grey smoke.
    d.rectangle([x, y, x + w, y + h * 0.55], fill=(178, 205, 225))
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(28, 68, 110))
    for wx in range(4):
        d.arc([x + w * (wx * 0.25), y + h * 0.58,
               x + w * (wx * 0.25 + 0.28), y + h * 0.78], 0, 180,
              fill=(255, 255, 255), width=2)
    # hull
    d.polygon([(x + w * 0.06, y + h * 0.62), (x + w * 0.94, y + h * 0.58),
               (x + w * 0.88, y + h * 0.82), (x + w * 0.12, y + h * 0.82)],
              fill=(140, 40, 35))
    # containers
    cont_cols = [(46, 125, 79), (200, 170, 60), (31, 58, 110), (178, 90, 40)]
    for i, cx0 in enumerate((0.14, 0.30, 0.46, 0.62)):
        d.rectangle([x + w * cx0, y + h * 0.44, x + w * (cx0 + 0.13),
                     y + h * 0.60], fill=cont_cols[i])
    # bridge tower
    d.rectangle([x + w * 0.80, y + h * 0.34, x + w * 0.92, y + h * 0.60],
                fill=(240, 240, 235))
    d.rectangle([x + w * 0.82, y + h * 0.38, x + w * 0.90, y + h * 0.44],
                fill=(30, 60, 90))
    # flames + smoke above midship
    flame(d, x + w * 0.38, y + h * 0.46, w * 0.20, h * 0.30,
          (240, 110, 20), (255, 200, 60))
    for sx, sy, sr in ((0.36, 0.16, 0.06), (0.44, 0.10, 0.08),
                       (0.52, 0.14, 0.06)):
        d.ellipse([x + w * (sx - sr), y + h * (sy - sr),
                   x + w * (sx + sr), y + h * (sy + sr)],
                  fill=(120, 120, 120))


def art_satellite(d, x, y, w, h):
    # Low orbit at night: black sky with stars, the blue curve of
    # Earth below, and a silver satellite with gold panels.
    d.rectangle([x, y, x + w, y + h], fill=(8, 10, 24))
    rng = random.Random(20261123)
    for _ in range(36):
        sx = x + rng.randint(4, w - 4)
        sy = y + rng.randint(4, int(h * 0.60))
        r = rng.choice([1, 1, 2])
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 255, 255))
    # Earth curve, bottom
    d.pieslice([x - w * 0.20, y + h * 0.62, x + w * 1.20, y + h * 1.50],
               start=180, end=360, fill=(46, 122, 194))
    d.ellipse([x + w * 0.20, y + h * 0.78, x + w * 0.44, y + h * 0.92],
              fill=(58, 154, 90))
    d.ellipse([x + w * 0.60, y + h * 0.84, x + w * 0.78, y + h * 0.96],
              fill=(58, 154, 90))
    # satellite, centre: gold panels + silver body + antenna
    cx, cy = x + w * 0.50, y + h * 0.38
    d.rectangle([cx - w * 0.22, cy - h * 0.06, cx - w * 0.06, cy + h * 0.06],
                fill=(200, 170, 60))
    d.rectangle([cx + w * 0.06, cy - h * 0.06, cx + w * 0.22, cy + h * 0.06],
                fill=(200, 170, 60))
    d.rectangle([cx - w * 0.06, cy - h * 0.10, cx + w * 0.06, cy + h * 0.10],
                fill=(200, 200, 205))
    d.line([cx, cy - h * 0.10, cx, cy - h * 0.26], fill=(220, 220, 220),
           width=2)
    d.ellipse([cx - 3, cy - h * 0.30, cx + 3, cy - h * 0.30 + 6],
              fill=(255, 80, 80))


def art_chip(d, x, y, w, h):
    # AI chip: dark board, circuit traces, a square chip with gold
    # pins on all four sides and a glowing teal core marked AI.
    d.rectangle([x, y, x + w, y + h], fill=(14, 22, 44))
    rng = random.Random(20261123)
    for _ in range(14):
        sx = x + rng.randint(6, w - 6)
        sy = y + rng.randint(6, int(h * 0.30))
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(60, 120, 160))
    # circuit traces from the edges toward the chip
    for ty in (0.22, 0.50, 0.78):
        d.line([x + 6, y + h * ty, x + w * 0.30, y + h * ty],
               fill=(70, 140, 180), width=2)
        d.line([x + w * 0.70, y + h * ty, x + w - 6, y + h * ty],
               fill=(70, 140, 180), width=2)
    for tx in (0.30, 0.70):
        d.line([x + w * tx, y + 6, x + w * tx, y + h * 0.18],
               fill=(70, 140, 180), width=2)
        d.line([x + w * tx, y + h * 0.82, x + w * tx, y + h - 6],
               fill=(70, 140, 180), width=2)
    # chip body
    cx0, cy0 = x + w * 0.30, y + h * 0.18
    cx1, cy1 = x + w * 0.70, y + h * 0.82
    d.rectangle([cx0, cy0, cx1, cy1], fill=(38, 40, 48),
                outline=(200, 170, 60), width=2)
    # gold pins, all four sides
    for i in range(5):
        px = cx0 + (i + 0.5) * (cx1 - cx0) / 5
        d.rectangle([px - 4, cy0 - 8, px + 4, cy0], fill=(200, 170, 60))
        d.rectangle([px - 4, cy1, px + 4, cy1 + 8], fill=(200, 170, 60))
    for i in range(4):
        py = cy0 + (i + 0.5) * (cy1 - cy0) / 4
        d.rectangle([cx0 - 8, py - 4, cx0, py + 4], fill=(200, 170, 60))
        d.rectangle([cx1, py - 4, cx1 + 8, py + 4], fill=(200, 170, 60))
    # glowing core with AI
    gx0, gy0 = x + w * 0.42, y + h * 0.34
    gx1, gy1 = x + w * 0.58, y + h * 0.66
    d.rectangle([gx0, gy0, gx1, gy1], fill=(20, 160, 140))
    f_ai = font(SANS_B, 26)
    ai = "AI"
    aw = d.textlength(ai, font=f_ai)
    d.text((x + w * 0.50 - aw / 2, y + h * 0.36), ai, font=f_ai,
           fill=(255, 255, 255))


def art_gaza(d, x, y, w, h):
    # Gaza at dusk: banded orange-purple sky, a damaged skyline
    # with broken rooftops, and a row of white aid tents below,
    # one marked with a red cross.
    d.rectangle([x, y, x + w, y + h * 0.34], fill=(214, 130, 70))
    d.rectangle([x, y + h * 0.34, x + w, y + h * 0.58], fill=(150, 90, 120))
    d.rectangle([x, y + h * 0.58, x + w, y + h], fill=(60, 55, 60))
    # damaged skyline silhouette
    base = y + h * 0.58
    heights = [0.30, 0.44, 0.26, 0.50, 0.34, 0.46, 0.28, 0.40]
    bx = x
    for i, hf in enumerate(heights):
        bw = w // len(heights)
        top = base - h * hf
        d.rectangle([bx, top, bx + bw - 2, base], fill=(40, 32, 40))
        if i % 2 == 0:
            # broken rooftop: jagged notch
            d.polygon([(bx, top), (bx + bw * 0.3, top + h * 0.08),
                       (bx + bw * 0.6, top),
                       (bx + bw - 2, top + h * 0.05),
                       (bx + bw - 2, top), (bx, top)],
                      fill=(214, 130, 70))
        for wy in range(int(top) + 6, int(base) - 4, 10):
            if (i + wy) % 3 == 0:
                d.rectangle([bx + 4, wy, bx + 7, wy + 4],
                            fill=(255, 210, 90))
        bx += bw
    # aid tents, foreground
    for i, tx in enumerate((0.08, 0.34, 0.60, 0.82)):
        txx = x + w * tx
        d.polygon([(txx - w * 0.10, y + h * 0.98),
                   (txx, y + h * 0.72),
                   (txx + w * 0.10, y + h * 0.98)],
                  fill=(235, 230, 215))
        if i == 1:
            # red cross on the medical tent
            d.rectangle([txx - 2, y + h * 0.82, txx + 2, y + h * 0.90],
                        fill=(178, 34, 34))
            d.rectangle([txx - 6, y + h * 0.855, txx + 6, y + h * 0.865],
                        fill=(178, 34, 34))


ART = {
    "cop31": art_cop31,
    "barrage": art_barrage,
    "blockade": art_blockade,
    "ship": art_ship,
    "cricket": art_cricket,
    "border": art_border,
    "capitol": art_capitol,
    "fire": art_fire,
    "road": art_road,
    "tennis": art_tennis,
    "basketball": art_basketball,
    "tanker": art_tanker,
    "satellite": art_satellite,
    "chip": art_chip,
    "gaza": art_gaza,
}

# ------------------------------------------------------------- map ---
# Coarse equirectangular land grid, 56 cols (lon -180..180) x 28 rows
# (lat 90..-60). Each row lists inclusive column ranges that are land.
# Drawn from scratch for this edition; dotted, impressionistic.
LAND_ROWS = [
    [(20, 23)],
    [(14, 16), (18, 25)],
    [(9, 16), (17, 24), (29, 32)],
    [(1, 21), (28, 55)],
    [(1, 19), (24, 25), (28, 55)],
    [(7, 19), (26, 27), (28, 55)],
    [(7, 18), (25, 55)],
    [(8, 19), (25, 48), (49, 49)],
    [(8, 17), (25, 31), (34, 49)],
    [(8, 16), (25, 48)],
    [(9, 16), (25, 46)],
    [(11, 15), (25, 45)],
    [(11, 14), (24, 43)],
    [(13, 15), (24, 43)],
    [(13, 15), (24, 34), (38, 39), (42, 43)],
    [(15, 16), (25, 34), (41, 43)],
    [(16, 18), (26, 33), (41, 45), (47, 48)],
    [(15, 22), (28, 33), (42, 45), (47, 49)],
    [(15, 22), (29, 33), (43, 45), (48, 50)],
    [(16, 21), (29, 34), (47, 49)],
    [(17, 21), (29, 34), (44, 50)],
    [(17, 21), (29, 32), (44, 50)],
    [(17, 20), (30, 31), (44, 50), (53, 54)],
    [(16, 18), (30, 31), (44, 49), (52, 54)],
    [(16, 18), (49, 50), (52, 53)],
    [(16, 17)],
    [(17, 17)],
    [],
]

# story id -> (lat, lon, dx, dy): pin position + fan-out offset so the
# dense Europe / Middle East cluster stays readable.
PINS = {
    1: (50.4, 30.5, 12, 2),       # Kyiv
    2: (35.7, 51.4, 14, -6),      # Tehran
    3: (37.4, -121.9, 0, 0),      # Santa Clara
    4: (32.1, 20.1, -2, 12),      # Benghazi
    5: (-41.3, 174.8, 0, 0),      # Wellington
    6: (50.8, 4.4, -14, 10),      # Brussels
    7: (31.5, 34.5, -10, -4),     # Gaza
    8: (-6.3, 106.2, 0, 0),       # Cikande
    9: (40.2, 44.5, 8, 6),        # Yerevan
    10: (45.1, 7.7, -4, 12),      # Turin
    11: (41.9, -87.6, 0, 0),      # Chicago
    12: (60.2, 25.0, 16, -8),     # Helsinki
    13: (52.5, 13.4, -10, -10),   # Berlin
}

REGION_COLORS = [
    ("EUROPE", 170, (31, 58, 110)),
    ("MIDDLE EAST", 150, (178, 34, 34)),
    ("AMERICAS", 165, (46, 125, 79)),
    ("ASIA-PACIFIC", 130, (176, 124, 11)),
    ("AFRICA", 85, (122, 74, 33)),
    ("OCEANIA", 90, (60, 110, 140)),
    ("WORLD", 194, (91, 74, 138)),
]

CERT_COLORS = {"REPORTED": GREEN, "CLAIM": AMBER, "ONGOING": BLUE}


def draw_map(d, x, y, w, h):
    """Dotted world map with numbered red pins for stories 1-13."""
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    cols, rows = 56, 28
    sx, sy = w / cols, h / rows
    for r, ranges in enumerate(LAND_ROWS):
        cy = y + (r + 0.5) * sy
        for lo, hi in ranges:
            for c in range(lo, hi + 1):
                cx = x + (c + 0.5) * sx
                d.ellipse([cx - 1.7, cy - 1.7, cx + 1.7, cy + 1.7],
                          fill=(150, 140, 110))
    f_pin = font(SANS_B, 8)
    for sid, (lat, lon, dx, dy) in PINS.items():
        px = x + (lon + 180) / 360 * w + dx
        py = y + (90 - lat) / 150 * h + dy
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED,
                  outline=(255, 255, 255), width=1)
        num = str(sid)
        nw = d.textlength(num, font=f_pin)
        d.text((px - nw / 2, py - 4), num, font=f_pin,
               fill=(255, 255, 255))


def render():
    with open(os.path.join(HERE, "stories.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    ed = data["edition"]
    stories = data["stories"]
    heroes = [s for s in stories if s["kind"] == "hero"]
    cards = [s for s in stories if s["kind"] == "card"]
    lst = [s for s in stories if s["kind"] == "list"]
    assert len(heroes) == 3 and len(cards) == 10 and len(lst) == 22, (
        len(heroes), len(cards), len(lst))
    assert len(stories) == 35
    counts = {r["name"]: r["count"] for r in ed["regions"]}
    assert sum(counts.values()) == 35
    for s in stories:
        assert counts[s["region"]] > 0
        counts[s["region"]] -= 1
    assert all(v == 0 for v in counts.values())

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- top bar ----
    d.rectangle([0, 0, W, 28], fill=NAVY)
    f_bar = font(SANS_B, 14)
    d.text((X0, 7), ed["title"], font=f_bar, fill=(255, 255, 255))
    f_bar2 = font(SANS_B, 11)
    bar_right = ed["subtitle"].upper()
    rw = d.textlength(bar_right, font=f_bar2)
    d.text((X0 + CW - rw, 8), bar_right, font=f_bar2, fill=(255, 255, 255))

    # ---- masthead + kicker ----
    f_mast = font(SERIF, 58)
    d.text((X0, 34), ed["date"], font=f_mast, fill=INK)
    f_kick = font(SERIF_I, 19)
    d.text((X0, 102), ed["kicker"], font=f_kick, fill=RED)
    d.line([X0, 128, X0 + CW, 128], fill=INK, width=2)

    # ---- stat strip: 6 big numbers ----
    f_stat = font(SANS_B, 28)
    f_statcap = font(SANS, 10)
    col_w = CW // 6
    for i, st in enumerate(ed["stats"]):
        cx = X0 + i * col_w
        d.text((cx + 4, 134), st["value"], font=f_stat, fill=RED)
        cap_lines = wrap(d, st["label"], f_statcap, col_w - 6)
        yy = 166
        for ln in cap_lines[:2]:
            d.text((cx + 4, yy), ln, font=f_statcap, fill=MUTED)
            yy += 13
        if i:
            d.line([cx, 136, cx, 180], fill=RULE, width=1)
    d.line([X0, 184, X0 + CW, 184], fill=INK, width=2)

    # ---- region bar: 7 regions, counts sum to 35 ----
    rx, ry = X0, 190
    f_reg = font(SANS_B, 13)
    for name, wseg, color in REGION_COLORS:
        d.rectangle([rx, ry, rx + wseg, ry + 24], fill=color)
        label = f"{name} {dict((r['name'], r['count']) for r in ed['regions'])[name]}"
        lw = d.textlength(label, font=f_reg)
        d.text((rx + (wseg - lw) / 2, ry + 5), label, font=f_reg,
               fill=(255, 255, 255))
        rx += wseg
    assert rx == X0 + CW

    # ---- THE DAY IN UTC strip ----
    uy = 216
    f_utc = font(SANS_B, 11)
    f_utc2 = font(SANS, 11)
    d.text((X0, uy + 2), "THE DAY IN UTC", font=f_utc, fill=RED)
    utc_items = ("05:30 Kyiv toll 11 \u00b7 07:32 Wellington drawn "
                 "\u00b7 08:30 Kyiv debris on schools \u00b7 12:07 Merkury "
                 "confirmed \u00b7 14:00 Qatar meets Rubio \u00b7 21:35 "
                 "Monza 3-0")
    uw = d.textlength("THE DAY IN UTC  ", font=f_utc)
    d.text((X0 + uw, uy + 2), utc_items, font=f_utc2, fill=INK)
    d.line([X0, uy + 20, X0 + CW, uy + 20], fill=RULE, width=1)

    # ---- 3 heroes ----
    hw, gap = 320, 12
    hy = 240
    f_tag = font(SANS_B, 13)
    f_badge = font(SANS_B, 12)
    f_cap = font(SANS, 10)
    f_loc = font(SANS_B, 12)
    f_cert = font(SANS_B, 11)
    f_hhead = font(SERIF, 22)
    f_hdeck = font(SANS, 12)
    for i, s in enumerate(heroes):
        hx = X0 + i * (hw + gap)
        ART[s["art"]](d, hx, hy, hw, 128)
        # tag top-left, badge top-right, caption chip bottom-left
        tag = s["tag"]
        tw = d.textlength(tag, font=f_tag)
        d.rectangle([hx, hy, hx + tw + 14, hy + 22], fill=RED)
        d.text((hx + 7, hy + 4), tag, font=f_tag, fill=(255, 255, 255))
        if True:
            badge = s["badge"]
            bw = d.textlength(badge, font=f_badge)
            d.rectangle([hx + hw - bw - 12, hy, hx + hw, hy + 20],
                        fill=(255, 255, 255))
            d.text((hx + hw - bw - 6, hy + 3), badge, font=f_badge, fill=INK)
        cap = s["caption"]
        cw2 = d.textlength(cap, font=f_cap)
        d.rectangle([hx, hy + 128 - 18, hx + cw2 + 10, hy + 128],
                    fill=(10, 10, 10))
        d.text((hx + 5, hy + 128 - 15), cap, font=f_cap,
               fill=(255, 255, 255))
        # TOP STORY label under the tag bar on hero 1
        if s["id"] == 1:
            top = "TOP STORY"
            tw2 = d.textlength(top, font=f_cap)
            d.rectangle([hx + 6, hy + 26, hx + 6 + tw2 + 12, hy + 26 + 18],
                        fill=(10, 10, 10))
            d.text((hx + 11, hy + 29), top, font=f_cap,
                   fill=(255, 255, 255))
        # location, headline, deck — certainty tag at the right end
        # of the location line, in its own colour
        loc = f"{s['id']} {s['location']} \u00b7 {s['topic']}"
        d.text((hx, hy + 134), loc, font=f_loc, fill=RED)
        cert = s["certainty"]
        cw3 = d.textlength(cert, font=f_cert)
        d.text((hx + hw - cw3, hy + 135), cert, font=f_cert,
               fill=CERT_COLORS[cert])
        head_lines = fit_text(d, s["title"], f_hhead, hw, 2)
        yy = hy + 152
        for ln in head_lines:
            d.text((hx, yy), ln, font=f_hhead, fill=INK)
            yy += 25
        deck = s["deck"] + f" ({s['source']})"
        deck_lines = fit_text(d, deck, f_hdeck, hw, 3)
        yy = hy + 204
        for ln in deck_lines:
            d.text((hx, yy), ln, font=f_hdeck, fill=MUTED)
            yy += 15

    # ---- 10 numbered cards, 2 rows of 5 ----
    cw3, cgap = 188, 11
    f_cloc = font(SANS_B, 11)
    f_ctitle = font(SANS_B, 14)
    f_cdeck = font(SANS, 11)
    f_cnum = font(SANS_B, 11)
    for row in range(2):
        cy = 496 + row * 152
        for col in range(5):
            s = cards[row * 5 + col]
            cx = X0 + col * (cw3 + cgap)
            ART[s["art"]](d, cx, cy, cw3, 68)
            # tag top-left, number circle top-right
            tag = s["tag"]
            tw = d.textlength(tag, font=f_tag)
            d.rectangle([cx, cy, cx + tw + 12, cy + 20], fill=RED)
            d.text((cx + 6, cy + 3), tag, font=f_tag, fill=(255, 255, 255))
            num = str(s["id"])
            nx = cx + cw3 - 20
            d.ellipse([nx, cy + 2, nx + 18, cy + 20], fill=(255, 255, 255),
                      outline=RED, width=2)
            nw = d.textlength(num, font=f_cnum)
            d.text((nx + 9 - nw / 2, cy + 5), num, font=f_cnum, fill=RED)
            # location, headline, deck
            loc = f"{s['location']}"
            d.text((cx, cy + 74), loc, font=f_cloc, fill=RED)
            title_lines = fit_text(d, s["title"], f_ctitle, cw3, 2)
            yy = cy + 90
            for ln in title_lines:
                d.text((cx, yy), ln, font=f_ctitle, fill=INK)
                yy += 17
            deck = s["deck"] + f" ({s['source']})"
            deck_lines = fit_text(d, deck, f_cdeck, cw3, 2)
            yy = cy + 126
            for ln in deck_lines:
                d.text((cx, yy), ln, font=f_cdeck, fill=MUTED)
                yy += 13

    # ---- bottom: map (left) + ALSO ON list (right) ----
    by = 810
    f_bh = font(SANS_B, 12)
    f_bsub = font(SANS, 10)
    d.text((X0, by), "WHERE IT HAPPENED", font=f_bh, fill=INK)
    sub = "pins match story numbers"
    d.text((X0 + 148, by + 1), sub, font=f_bsub, fill=MUTED)
    list_x = X0 + 360
    d.text((list_x, by), "ALSO ON MONDAY 23 NOVEMBER \u2014 22 MORE STORIES",
           font=f_bh, fill=INK)
    map_y = by + 20
    draw_map(d, X0, map_y, 340, 108)
    # list: 2 columns of 11, one line each
    f_li = font(SANS, 10)
    f_ln = font(SANS_B, 10)
    col_w2 = 307
    for i, s in enumerate(lst):
        col = i // 11
        row = i % 11
        lx = list_x + col * (col_w2 + 10)
        ly = map_y + row * 11
        num = str(s["id"])
        d.text((lx, ly), num, font=f_ln, fill=RED)
        nw = d.textlength(num + " ", font=f_ln)
        line = one_line(d, f"{s['title']} ({s['source']})", f_li,
                        col_w2 - nw)
        d.text((lx + nw, ly), line, font=f_li, fill=INK)

    # ---- CERTAINTY legend ----
    ly = 954
    f_leg = font(SANS_B, 11)
    f_leg2 = font(SANS, 11)
    d.text((X0, ly), "CERTAINTY:", font=f_leg, fill=RED)
    lw = d.textlength("CERTAINTY: ", font=f_leg)
    d.text((X0 + lw, ly),
           "REPORTED = carried by the day's wires \u00b7 CLAIM = one side's "
           "account \u00b7 ONGOING = still developing",
           font=f_leg2, fill=INK)

    # ---- DATE CHECK box ----
    dy = 968
    d.rectangle([X0, dy, X0 + CW, dy + 40], outline=RED, width=2)
    f_dc = font(SANS_B, 11)
    f_dc2 = font(SANS, 11)
    d.text((X0 + 8, dy + 4), "DATE CHECK \u2014 READ THIS FIRST", font=f_dc,
           fill=RED)
    dc_lines = wrap(d, ed["datecheck"], f_dc2, CW - 222)
    yy = dy + 4
    for ln in dc_lines[:2]:
        d.text((X0 + 214, yy), ln, font=f_dc2, fill=INK)
        yy += 13

    # ---- sources line ----
    f_ft = font(SANS, 9)
    foot = ("Sources: Reuters, AP, BBC, Euronews, Ukrinform, Guardian, "
            "Oxfam, Tasnim, ESPN, IANS, UN News, Fox News, LaPresse, ABC "
            "Australia, Cricinfo, Anadolu, NATO, France 24, h.ua, ICC, UN. "
            "Every story names its outlet.")
    d.text((X0, 1012), foot, font=f_ft, fill=MUTED)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    render()
