#!/usr/bin/env python3
"""Paper-tone clamp: a print cannot be whiter than its paper.

DK's catch (speaking-to-her, 2026-07-10): the calf and sun rendered
pure white, brighter than the cream ground — a register violation no
period plate can commit. Paper tone is estimated per channel from the
outer margin strips (median); any pixel brighter than paper is clamped
to it channelwise. Audit mode reports violations without writing.

Usage:
  uv run python paper_clamp.py --audit img1.png [img2 ...]
  uv run python paper_clamp.py --fix img.png -o out.png
"""

import argparse
from pathlib import Path

import numpy as np
from PIL import Image


def paper_tone(a: np.ndarray) -> np.ndarray:
    """Estimate paper from the bulk bright band (75th-95th luminance
    percentile): in an engraving the bright bulk IS paper showing
    through. Margins are useless — plates fill edge to edge, and true
    whites (the violation) sit above this band, not inside it."""
    lum = a.mean(axis=2)
    lo, hi = np.percentile(lum, [75, 95])
    band = a[(lum >= lo) & (lum <= hi)]
    return np.median(band, axis=0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("images", nargs="+", type=Path)
    ap.add_argument("--fix", action="store_true")
    ap.add_argument("-o", "--output", type=Path, help="output path (single image)")
    ap.add_argument("--tol", type=float, default=4.0, help="violation tolerance")
    args = ap.parse_args()

    for path in args.images:
        im = Image.open(path).convert("RGB")
        a = np.asarray(im, dtype=np.float64)
        paper = paper_tone(a)
        over = (a > paper + args.tol).any(axis=2)
        frac = over.mean()
        print(
            f"{path.name}: paper=({paper[0]:.0f},{paper[1]:.0f},{paper[2]:.0f}) "
            f"over-white={frac:.4%}" + ("  <-- VIOLATION" if frac > 0.001 else "")
        )
        if args.fix and frac > 0:
            clamped = np.minimum(a, paper).astype(np.uint8)
            out = args.output if args.output else path
            Image.fromarray(clamped).save(out)
            print(f"  clamped -> {out}")


if __name__ == "__main__":
    main()
