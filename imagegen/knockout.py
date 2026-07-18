#!/usr/bin/env python3
"""Knock plate grounds out to page white (assembly-time transform).

DK ruling 2026-07-13: the cream ground is valid in art/ (the model's
working register, the archival record) but applying that cream to the
assembled book is artifice — "Mexico as sepia filter." The book prints
black-line on the page's own white, so the assembly divides each
plate by its estimated paper tone (paper_clamp.paper_tone), mapping
ground -> white and neutralizing the cast; ink scales proportionally.
art/ is never modified; outputs land in build/plates/.

DK ruling 2026-07-18 (grayscale/ink pass): an engraving is ink or
paper; residual color cast and wash mids are generator artifacts,
not printmaking. After the ground division the plate is reduced to
luminance and put through a fixed ink curve — levels 40/235 with
gamma 0.9 — verified at 1:1 to preserve the finest hatching and
stipple at both hires (2x) and base plate resolution while clearing
ground haze to true white and settling near-blacks to ink. Outputs
are single-channel ("L") PNGs.

Usage: knockout.py <src.png> [<src.png> ...] -o <outdir>
Skips files whose output is newer than the source (assemble.py calls
this every build).
"""

import argparse
from pathlib import Path

import numpy as np
from paper_clamp import paper_tone
from PIL import Image

# Ink curve (DK 2026-07-18): levels black-in/white-in on luminance,
# then gamma. Tested as "C strong" against gray-only and gentle
# variants; exhibits scratch/gs_*.jpg (2026-07-18).
BLACK_IN = 40.0
WHITE_IN = 235.0
GAMMA = 0.9


def knockout(src: Path, dst: Path) -> bool:
    if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
        return False
    a = np.asarray(Image.open(src).convert("RGB"), dtype=np.float64)
    paper = paper_tone(a)
    out = np.clip(a / paper * 255.0, 0, 255)
    g = out @ [0.2126, 0.7152, 0.0722]
    g = np.clip((g - BLACK_IN) / (WHITE_IN - BLACK_IN), 0.0, 1.0) ** GAMMA
    Image.fromarray((g * 255.0).astype(np.uint8), "L").save(dst)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("images", nargs="+")
    ap.add_argument("-o", "--outdir", required=True)
    args = ap.parse_args()
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    done = skipped = 0
    for s in args.images:
        src = Path(s)
        if knockout(src, outdir / src.name):
            done += 1
        else:
            skipped += 1
    print(f"knockout: {done} processed, {skipped} current -> {outdir}")


if __name__ == "__main__":
    main()
