#!/usr/bin/env python3
"""Shared-seed rhyme measurement.

Downsamples images to a 16x24 (portrait) / 24x16 (landscape) grayscale
grid and reports normalized Pearson correlation between every pair —
the low-frequency massing kinship that shared seeds buy (findings.md,
"Shared-seed rhyme"). Usage:

    uv run python rhyme.py a.png b.png [c.png ...]

Pairs across different aspect ratios are skipped.
"""

import sys
from itertools import combinations

import numpy as np
from PIL import Image


def massing(path: str) -> np.ndarray:
    im = Image.open(path).convert("L")
    grid = (16, 24) if im.height > im.width else (24, 16)
    arr = np.asarray(im.resize(grid, Image.LANCZOS), dtype=np.float64)
    arr -= arr.mean()
    return arr / (arr.std() or 1.0)


def main():
    paths = sys.argv[1:]
    if len(paths) < 2:
        sys.exit(__doc__)
    grids = {p: massing(p) for p in paths}
    for a, b in combinations(paths, 2):
        if grids[a].shape != grids[b].shape:
            print(f"{a} x {b}: aspect mismatch, skipped")
            continue
        r = float((grids[a] * grids[b]).mean())
        print(f"{r:+.3f}  {a} x {b}")


if __name__ == "__main__":
    main()
