#!/usr/bin/env python3
"""POD cover wrap: back board + spine + front board, with bleed.

Locked POD details (DK 2026-07-19):
- cream paper bulk 0.0025 in/page (period-right stock); spine width =
  print-interior pages x bulk. The print interior is the POD PDF minus
  its digital cover leaf (`make print-interior`), so pass THAT count.
- 0.125 in bleed all around; 5.5 x 8.5 trim.
- Front board = the typed cover (build/cover-typed.png), height-fit to
  full bleed height, gutter-side overflow cropped.
- Spine reads top-to-bottom (US convention), letterspaced Pagella.
- Back board: the book's own words only — a short excerpt over the
  paper ground; no blurb, no genre marker, no provenance line (the
  boards doctrine, catalog [cover-tracks]). Barcode zone (2 x 1.2 in,
  0.25 in off the trim corner) held pure white.

Usage: cover_wrap.py --pages 140 [--bulk 0.0025] -o build/cover-wrap.png
"""

import argparse
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

DPI = 300
TRIM_W, TRIM_H = 5.5, 8.5
BLEED = 0.125
INK = 15

EXCERPT = (
    "This is how I will die. Not by storm or starvation or the\n"
    "arrows of men who have every right to kill me. By her."
)


def font_file(style: str) -> str:
    query = "TeX Gyre Pagella" + (":style=Italic" if style == "italic" else "")
    return subprocess.run(
        ["fc-match", "--format=%{file}", query],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


def px(inches: float) -> int:
    return int(round(inches * DPI))


def tracked(draw, xy, text, font, tr, fill=INK):
    x, y = xy
    for c in text:
        draw.text((x, y), c, font=font, fill=fill)
        x += draw.textlength(c, font=font) + tr
    return x - tr - xy[0]


def tracked_width(draw, text, font, tr):
    return sum(draw.textlength(c, font=font) for c in text) + tr * (len(text) - 1)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--pages",
        type=int,
        required=True,
        help="print-interior page count (POD pdf minus cover leaf)",
    )
    ap.add_argument(
        "--bulk", type=float, default=0.0025, help="paper bulk in/page (cream default)"
    )
    ap.add_argument("--cover", type=Path, default=Path("build/cover-typed.png"))
    ap.add_argument("-o", "--out", type=Path, default=Path("build/cover-wrap.png"))
    args = ap.parse_args()

    spine = args.pages * args.bulk
    W = px(BLEED + TRIM_W + spine + TRIM_W + BLEED)
    H = px(TRIM_H + 2 * BLEED)
    print(f"wrap: {W}x{H}px  spine {spine:.3f}in  ({args.pages}pp x {args.bulk})")

    cover = Image.open(args.cover).convert("L")
    paper = 252  # near-white ground; boards match the page
    wrap = Image.new("L", (W, H), paper)
    d = ImageDraw.Draw(wrap)

    # front board (right panel), height-fit full bleed, crop overflow
    fw = int(round(H * cover.size[0] / cover.size[1]))
    front = cover.resize((fw, H))
    panel_w = px(TRIM_W + BLEED)
    x0 = W - panel_w
    crop = front.crop(
        (max(0, (fw - panel_w) // 2), 0, max(0, (fw - panel_w) // 2) + panel_w, H)
    )
    wrap.paste(crop, (x0, 0))

    # spine text, top-to-bottom, if the spine can carry it
    sx0 = px(BLEED + TRIM_W)
    sw = px(spine)
    if spine >= 0.25:
        size = int(min(sw * 0.52, px(0.16)))
        f = ImageFont.truetype(font_file("regular"), size)
        strip_h = size + 8
        tr = size * 0.16
        title_w = int(tracked_width(d, "WHITE BUFFALO", f, tr))
        fa = ImageFont.truetype(font_file("regular"), int(size * 0.78))
        tra = size * 0.10
        auth_w = int(tracked_width(d, "COHEN and KLEIN", fa, tra))
        strip = Image.new("L", (px(TRIM_H), strip_h), paper)
        ds = ImageDraw.Draw(strip)
        tracked(ds, (px(0.5), 0), "WHITE BUFFALO", f, tr)
        tracked(
            ds,
            (px(TRIM_H) - auth_w - px(0.5), int(size * 0.12)),
            "COHEN and KLEIN",
            fa,
            tra,
        )
        strip = strip.rotate(-90, expand=True)
        wrap.paste(strip, (sx0 + (sw - strip_h) // 2, px(BLEED)))

    # back board: excerpt, upper third, centered on the panel
    bx_c = px(BLEED + TRIM_W / 2)
    fe = ImageFont.truetype(font_file("regular"), px(0.195))
    lines = EXCERPT.split("\n")
    lh = int(px(0.195) * 1.6)
    y = px(BLEED + 2.6)
    for ln in lines:
        lw = d.textlength(ln, font=fe)
        d.text((bx_c - lw / 2, y), ln, font=fe, fill=INK)
        y += lh

    # barcode zone: pure white, 2 x 1.2in, 0.25in off the trim corner
    bz_w, bz_h, off = px(2.0), px(1.2), px(0.25)
    zx1 = px(BLEED + TRIM_W) - off
    zy1 = H - px(BLEED) - off
    d.rectangle([zx1 - bz_w, zy1 - bz_h, zx1, zy1], fill=255)

    wrap.save(args.out, dpi=(DPI, DPI))
    preview = wrap.resize((1000, int(1000 * H / W)))
    preview.save(args.out.with_suffix(".preview.jpg"), quality=76)
    print(f"wrote {args.out} (+preview)")


if __name__ == "__main__":
    main()
