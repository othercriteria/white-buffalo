#!/usr/bin/env python3
"""Draft Farrell candidates — the contrast anchor to Morrow.

Not a full series (DK, 2026-07-08): drafted to individuate Morrow by
contrast. Canon and reference choices in imagegen/farrell-reference.md.
Output to output/farrell-candidates/ for director review.
"""

from pathlib import Path

import torch
from diffusers import ZImagePipeline

MODEL = "Tongyi-MAI/Z-Image"
REVISION = "04cc4abb7c5069926f75c9bfde9ef43d49423021"
HERE = Path(__file__).parent
OUT = HERE / "output" / "farrell-candidates"

IDENTITY = (
    "a compact lean man of thirty-two, medium height, squared shoulders and "
    "an economical stance, a face weathered past his years with deep lines "
    "at the eye corners, pale light-colored eyes, watchful measuring "
    "expression, short cropped sandy brown hair, a short rough trail beard "
    "of some weeks, broad-brimmed low-crowned dark felt hat, heavy dark "
    "winter coat, calloused hands with scarred knuckles"
)

STYLE = (
    "1850s steel engraving artwork, fine crosshatching, monochrome ink on "
    "cream paper, detailed linework, the engraved image itself filling the "
    "entire frame edge to edge"
)

NEGATIVE = (
    "color, photograph, modern, digital, painting, soft focus, text, "
    "letters, words, caption, title, inscription, signature, plate number, "
    "border, frame, margin, skeletal, corpse, bulging eyes, wide staring "
    "eyes, crazed stare, long beard, long hair, bareheaded, healthy plump "
    "face, groomed, formal portrait pose"
)

ASPECTS = {"portrait": (832, 1216), "landscape": (1216, 832)}

VARIANTS = [
    ("bust", "portrait, gray winter sky behind him, 1858", "portrait", 701),
    ("bust-b", "portrait, gray winter sky behind him, 1858", "portrait", 702),
    (
        "bust-tavern",
        "portrait at a rough wooden table by lamplight, low-ceilinged tavern, pipe smoke, 1858",
        "portrait",
        703,
    ),
    (
        "full-horse",
        "standing in snow beside a sturdy bay gelding, a rifle in a scabbard on the saddle, full figure, winter prairie, 1858",
        "portrait",
        704,
    ),
    (
        "full-rifle",
        "standing on winter prairie with a muzzleloading rifle crooked in one arm, full figure, deep snow and gray sky, 1858",
        "portrait",
        705,
    ),
]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    print(f"Loading {MODEL} @ {REVISION[:8]}...")
    pipe = ZImagePipeline.from_pretrained(
        MODEL, revision=REVISION, torch_dtype=torch.bfloat16
    )
    pipe.enable_model_cpu_offload()

    for name, suffix, aspect, seed in VARIANTS:
        path = OUT / f"farrell_{name}_s{seed}.png"
        if path.exists():
            print(f"skip {path.name}")
            continue
        width, height = ASPECTS[aspect]
        prompt = f"{STYLE}, {IDENTITY}, {suffix}"
        print(f"Generating {path.name} ({width}x{height})")
        image = pipe(
            prompt=prompt,
            negative_prompt=NEGATIVE,
            height=height,
            width=width,
            cfg_normalization=False,
            num_inference_steps=40,
            guidance_scale=4.0,
            generator=torch.Generator("cuda").manual_seed(seed),
        ).images[0]
        image.save(path)
    print("FARRELL_DONE")


if __name__ == "__main__":
    main()
