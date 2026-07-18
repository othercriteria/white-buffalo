#!/usr/bin/env python3
"""Compose the typed cover (assembly-time overlay; art/ never typed).

Cover doctrine (DK 2026-07-18, catalog [cover-tracks]): full-bleed
boards on the two-trails image, letterspaced Pagella title + author
line in the sky the image reserved, NO genre marker, and no
provenance line ever (the never-enact guard on the compiler frame).
Type is laid over the knocked-out plate at build time so lettering
tweaks never touch the image.

Usage: cover_compose.py <knocked-cover.png> -o <out.png>
Skips when the output is newer than the source (assemble.py calls
this every build).
"""

import argparse
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

TITLE = "WHITE BUFFALO"
AUTHORS = [("BEN COHEN", "regular"), ("and", "italic"), ("DANIEL KLEIN", "regular")]
INK = 15  # near-black, matching plate ink after the knockout curve


def font_file(style: str) -> str:
    query = "TeX Gyre Pagella" + (":style=Italic" if style == "italic" else "")
    return subprocess.run(
        ["fc-match", "--format=%{file}", query],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


def compose(src: Path, dst: Path) -> bool:
    if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
        return False
    im = Image.open(src).convert("L")
    w, h = im.size
    d = ImageDraw.Draw(im)
    regular, italic = font_file("regular"), font_file("italic")

    # Title: letterspaced caps fitted to 80% of the width (v3 layout,
    # DK bless 2026-07-18).
    size = int(w * 0.115)
    while size > 10:
        f = ImageFont.truetype(regular, size)
        tr = size * 0.18
        tw = sum(d.textlength(c, font=f) for c in TITLE) + tr * (len(TITLE) - 1)
        if tw <= w * 0.80:
            break
        size -= 4
    x = w / 2 - tw / 2
    ty = int(h * 0.072)
    for c in TITLE:
        d.text((x, ty), c, font=f, fill=INK)
        x += d.textlength(c, font=f) + tr

    # Author line under the title, italic "and".
    asize = int(size * 0.31)
    fr = ImageFont.truetype(regular, asize)
    fi = ImageFont.truetype(italic, int(asize * 0.93))
    y = ty + size + int(size * 0.46)
    segs = [
        (t, fr if s == "regular" else fi, asize * 0.13 if s == "regular" else 2)
        for t, s in AUTHORS
    ]
    gap = asize * 0.5
    widths = [
        sum(d.textlength(c, font=fnt) for c in t) + tr2 * (len(t) - 1)
        for t, fnt, tr2 in segs
    ]
    x = w / 2 - (sum(widths) + gap * (len(segs) - 1)) / 2
    for (t, fnt, tr2), tw2 in zip(segs, widths):
        xx = x
        for c in t:
            d.text((xx, y), c, font=fnt, fill=INK)
            xx += d.textlength(c, font=fnt) + tr2
        x += tw2 + gap

    im.save(dst)
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("src", type=Path)
    ap.add_argument("-o", "--out", type=Path, required=True)
    args = ap.parse_args()
    changed = compose(args.src, args.out)
    print(f"cover: {'composed' if changed else 'current'} -> {args.out}")


if __name__ == "__main__":
    main()
