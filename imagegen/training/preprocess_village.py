#!/usr/bin/env python3
"""Preprocess village_raw/ acquisitions into the travois LoRA training set.

Per-file ops from village_raw/manifest.md: rotations, plate/panel crops
(fractional boxes, refined by eyeball over iterations), frame removal,
grayscale, downscale. Photos and the no-travois Bodmer panorama are
excluded (register/concept hygiene). Output: dataset/village/*.png.
"""

from pathlib import Path

from PIL import Image, ImageOps

HERE = Path(__file__).parent
RAW = HERE / "village_raw"
OUT = HERE / "dataset" / "village"
MAX_DIM = 2400

# name -> (source, rotate_deg_ccw, crop_frac (l, t, r, b) or None)
OPS = {
    "catlin-plate21-sioux-moving": (
        "catlin-letters-notes-plate21-sioux-moving-camp.jpg",
        0,
        (0.07, 0.07, 0.94, 0.45),
    ),
    "catlin-plate166-comanchees-moving": (
        "catlin-letters-notes-plate166-comanchees-moving.jpg",
        -90,
        (0.125, 0.165, 0.895, 0.85),
    ),
    "eastman-indians-travelling": (
        "eastman-indians-travelling-aboriginal-portfolio.jpg",
        -90,
        (0.08, 0.13, 0.92, 0.86),
    ),
    "remington-mother-boy-travois": (
        "remington-indian-mother-and-boy-travois.jpg",
        0,
        (0.10, 0.02, 0.98, 0.345),
    ),
    "leslie-crazy-horse-band-1877": (
        "leslie-crazy-horse-band-surrender-1877.tif",
        0,
        (0.19, 0.20, 0.81, 0.73),
    ),
    "bodmer-skin-lodge-assiniboin": (
        "bodmer-skin-lodge-assiniboin-chief.jpg",
        0,
        (0.14, 0.16, 0.845, 0.72),
    ),
    "catlin-band-of-sioux-moving-camp": (
        "catlin-band-of-sioux-moving-camp.jpg",
        0,
        None,
    ),
    "catlin-comanche-moving-camp": (
        "catlin-comanche-moving-camp-dog-fight-enroute.jpg",
        0,
        None,
    ),
    "halseys-bluff-sioux-on-march": (
        "halseys-bluff-sioux-indians-on-the-march.jpg",
        0,
        (0.24, 0.22, 0.76, 0.78),
    ),
    "eastman-sioux-breaking-up-camp": (
        "eastman-sioux-indians-breaking-up-camp.jpg",
        0,
        (0.03, 0.03, 0.97, 0.97),
    ),
    "miller-cavalcade": ("miller-cavalcade-indian-procession.jpg", 0, None),
    "russell-indian-women-moving": ("russell-indian-women-moving-1898.jpg", 0, None),
    "deming-dog-travois-blackfoot": (
        "deming-dog-travois-blackfoot-camp.jpg",
        0,
        (0.14, 0.155, 0.86, 0.845),
    ),
    "bodmer-dog-travois-detail": ("bodmer-dog-travois-detail-skin-lodge.jpg", 0, None),
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (src, rot, frac) in OPS.items():
        im = Image.open(RAW / src)
        if rot:
            im = im.rotate(rot, expand=True)
        if frac:
            l, t, r, b = frac
            im = im.crop(
                (
                    int(l * im.width),
                    int(t * im.height),
                    int(r * im.width),
                    int(b * im.height),
                )
            )
        im = ImageOps.grayscale(im)
        if max(im.size) > MAX_DIM:
            scale = MAX_DIM / max(im.size)
            im = im.resize(
                (round(im.width * scale), round(im.height * scale)), Image.LANCZOS
            )
        im.save(OUT / f"{name}.png")
        print(f"{name}.png {im.size}")


# Dataset v2 additions (2026-07-09, physicality round): the two flagged
# photos come IN — structure over register purity; captions bind
# "photograph" so the register stays separable. Diagram files from
# manifest-structure.md get appended here after eyeballing.
OPS_V2 = {
    "photo-nara-stump-horn-travois": (
        "photo-nara-cheyenne-stump-horn-horse-travois.jpg",
        0,
        (0.02, 0.02, 0.98, 0.97),
    ),
    "photo-loc-blackfoot-travois": (
        "photo-loc-blackfoot-travois.jpg",
        0,
        (0.02, 0.035, 0.98, 0.925),
    ),
}
OPS.update(OPS_V2)

if __name__ == "__main__":
    main()
