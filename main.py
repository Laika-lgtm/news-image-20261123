#!/usr/bin/env python3
"""Entrypoint: copy the pre-rendered front page to the output directory.

Standard library only — no network, no third-party imports. The image is
rendered at build time by render_frontpage.py (PIL) from stories.json and
committed as entry.png; this program just places it where the grader
expects it, so both runs write byte-identical output.

Round 1 (this commit): the first entry for news-image-20261123 —
Monday 23 November 2026. The page ports the winning formula our
news-22 round 12 proved (0.989065, rank 32 at its peak) and adds the
three levers from the un-submitted news-22 round 13 brief: a certainty
system (REPORTED / CLAIM tags on the three heroes plus a one-line
legend), three sports cards (cricket draw, tennis year-end No. 1,
Giddey triple-double), and an ALSO list with zero truncation. Every
fact is from Monday 23 November 2026 wires, read up to 14:00 UTC.
"""
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MAX_BYTES = 1 << 20  # competition limit: 1 MiB
EXPECTED_W, EXPECTED_H = 1024, 1024


def main():
    src = os.path.join(HERE, "entry.png")
    if not os.path.isfile(src):
        print("entry.png missing from repository", file=sys.stderr)
        return 1
    size = os.path.getsize(src)
    if size > MAX_BYTES:
        print(f"entry.png is {size} bytes, over the 1 MiB limit",
              file=sys.stderr)
        return 1
    with open(src, "rb") as fh:
        magic = fh.read(8)
        if magic != b"\x89PNG\r\n\x1a\n":
            print("entry.png is not a PNG file", file=sys.stderr)
            return 1
        ihdr = fh.read(25)
    if len(ihdr) < 25 or ihdr[4:8] != b"IHDR":
        print("entry.png has no PNG IHDR chunk", file=sys.stderr)
        return 1
    width, height = struct.unpack(">II", ihdr[8:16])
    if (width, height) != (EXPECTED_W, EXPECTED_H):
        print(f"entry.png is {width}x{height}, expected "
              f"{EXPECTED_W}x{EXPECTED_H}", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dest)
    print("wrote", dest, os.path.getsize(dest), "bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
