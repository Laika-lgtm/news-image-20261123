#!/usr/bin/env python3
"""Graded entrypoint for round 2 of news-image-20261123.

The front page is rendered at build time by render_frontpage.py (PIL)
from stories.json and committed as entry.png. This program does no
rendering and no network access: it only checks that the committed
image is a valid 1024x1024 PNG inside the 1 MiB limit and copies it to
the directory the grader reads from. Because the copy is a plain
byte-for-byte copy, two runs always produce identical output.

Round 2 (this file): the page is rebuilt after a full date audit of
round 1, which scored rank 91 in blind round 3. The audit found the
round-1 hero — the COP31 collapse — happened on Sunday 22 November,
not Monday 23 November, plus eleven more stale items. Round 2 replaces
them all with stories first reported on Monday 23 November 2026:
the Kyiv-region raid leads, the Iran blockade vow is second, and
Nvidia reinstating Jensen Huang is the new third hero.
"""
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
IMAGE_NAME = "entry.png"
LIMIT_BYTES = 1 << 20
WANT_WIDTH, WANT_HEIGHT = 1024, 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print(message, file=sys.stderr)
    return 1


def check_png(path):
    """Return (width, height) if path is a valid PNG, else None."""
    try:
        with open(path, "rb") as handle:
            head = handle.read(33)
    except OSError as exc:
        print(f"cannot read {path}: {exc}", file=sys.stderr)
        return None
    if len(head) < 33 or head[:8] != PNG_MAGIC:
        print(f"{path} is not a PNG file", file=sys.stderr)
        return None
    if head[12:16] != b"IHDR":
        print(f"{path} has no PNG IHDR chunk", file=sys.stderr)
        return None
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def run():
    source = os.path.join(HERE, IMAGE_NAME)
    if not os.path.isfile(source):
        return fail(f"{IMAGE_NAME} missing from repository")
    size = os.path.getsize(source)
    if size > LIMIT_BYTES:
        return fail(f"{IMAGE_NAME} is {size} bytes, over the 1 MiB limit")
    dims = check_png(source)
    if dims is None:
        return 1
    if dims != (WANT_WIDTH, WANT_HEIGHT):
        return fail(
            f"{IMAGE_NAME} is {dims[0]}x{dims[1]}, "
            f"expected {WANT_WIDTH}x{WANT_HEIGHT}"
        )
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, IMAGE_NAME)
    shutil.copyfile(source, target)
    copied = os.path.getsize(target)
    if copied != size:
        return fail(
            f"copy of {IMAGE_NAME} is {copied} bytes, "
            f"expected {size} bytes"
        )
    print("wrote", target, copied, "bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
