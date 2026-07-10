#!/usr/bin/env python3
"""Register statistics — quantify engraving-texture drift (DK 2026-07-09:
style drift "would show up in pixel and 3x3 patch statistics").

Metrics per image (grayscale, normalized to 832px width):
  mean      mean luminance (0-255)
  ink       fraction of pixels darker than 128
  paper     fraction of pixels lighter than 235 (blank paper)
  tex3      mean local 3x3 standard deviation (linework density)
  hf        mean |Laplacian| (high-frequency energy of the hatching)

Usage:
  uv run python register.py --corpus ../art candidate1.png [candidate2 ...]

Reports corpus mean +/- std per metric, then each candidate with
z-scores against the corpus. |z| > 2 on tex3/paper/ink is drift.
"""

import argparse
from pathlib import Path

import numpy as np
from PIL import Image


def stats(path: Path) -> dict:
    im = Image.open(path).convert("L")
    if im.width != 832:
        im = im.resize((832, round(im.height * 832 / im.width)), Image.LANCZOS)
    a = np.asarray(im, dtype=np.float64)
    # local 3x3 std via shifted stacks
    shifts = [
        a[y : a.shape[0] - 2 + y, x : a.shape[1] - 2 + x]
        for y in range(3)
        for x in range(3)
    ]
    stack = np.stack(shifts)
    tex3 = stack.std(axis=0).mean()
    lap = 4 * a[1:-1, 1:-1] - a[:-2, 1:-1] - a[2:, 1:-1] - a[1:-1, :-2] - a[1:-1, 2:]
    return {
        "mean": a.mean(),
        "ink": (a < 128).mean(),
        "paper": (a > 235).mean(),
        "tex3": tex3,
        "hf": np.abs(lap).mean(),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", type=Path, required=True)
    ap.add_argument("candidates", nargs="+", type=Path)
    args = ap.parse_args()

    corpus = sorted(args.corpus.glob("*.png"))
    rows = {p.name: stats(p) for p in corpus}
    keys = ["mean", "ink", "paper", "tex3", "hf"]
    arr = {k: np.array([r[k] for r in rows.values()]) for k in keys}

    print(f"corpus ({len(corpus)} plates):")
    for k in keys:
        print(f"  {k:>5}: {arr[k].mean():8.3f} +/- {arr[k].std():.3f}")
    print()
    for cand in args.candidates:
        s = stats(cand)
        zs = {k: (s[k] - arr[k].mean()) / (arr[k].std() or 1) for k in keys}
        flagged = " ".join(f"{k}={s[k]:.3f}(z{zs[k]:+.1f})" for k in keys)
        worst = max(zs.values(), key=abs)
        mark = " <-- DRIFT" if abs(worst) > 2 else ""
        print(f"{cand.name}: {flagged}{mark}")


if __name__ == "__main__":
    main()
