#!/usr/bin/env python3
"""Breed the Morrow LoRA training set from the approved anchors.

Anchors (DK, 2026-07-08): bust r3 s121, full r2 s211. The identity block
below is those anchors' shared prompt language; each variant appends
framing/setting only. Output goes to output/morrow-breed/ for curation —
only facial cousins of the anchors survive into the training set.
Reference choices per imagegen/morrow-reference.md (canon vs signed-off
choices; blanket-over-head is the winter head covering, no hat ever).
"""

from pathlib import Path

import torch
from diffusers import ZImagePipeline

MODEL = "Tongyi-MAI/Z-Image"
REVISION = "04cc4abb7c5069926f75c9bfde9ef43d49423021"
HERE = Path(__file__).parent
OUT = HERE / "output" / "morrow-breed"

IDENTITY = (
    "a man of thirty-four worn down to sinew by three years of walking, "
    "hollow cheeks and weathered skin over a young man's bones, calm deep-set "
    "eyes with a level far-off gaze, alive and quiet, full head of long lank "
    "dark hair grayed at the temples and parted in the center, a very long "
    "tangled dark beard reaching well down past his chest, shapeless dark "
    "wool coat so worn it barely deserves the name, worn boots, bareheaded"
)

STYLE = (
    "1850s steel engraving artwork, fine crosshatching, monochrome ink on "
    "cream paper, detailed linework, the engraved image itself filling the "
    "entire frame edge to edge"
)

NEGATIVE = (
    "color, photograph, modern, digital, painting, soft focus, text, "
    "letters, words, caption, title, inscription, signature, plate number, "
    "border, frame, margin, skeletal, corpse, skull face, sunken dead eyes, "
    "zombie, bulging eyes, wide staring eyes, crazed stare, bald, receding "
    "hairline, healthy, well-fed, plump, groomed, respectable, formal "
    "portrait pose, short beard, hat, cap"
)

ASPECTS = {"portrait": (832, 1216), "landscape": (1216, 832)}

# (name, framing/setting suffix, aspect, seed)
VARIANTS = [
    # Anchor re-rolls (near-anchor seeds for facial cousins)
    ("bust-anchor", "portrait, winter prairie behind him, 1858", "portrait", 121),
    ("bust-anchor-b", "portrait, winter prairie behind him, 1858", "portrait", 125),
    ("bust-anchor-c", "portrait, winter prairie behind him, 1858", "portrait", 126),
    (
        "full-anchor",
        "standing alone on winter prairie, clothes hanging loose on a lean frame, a blanket roll under one arm, a small sheathed knife at his belt, no gun, snow and gray sky, 1858, full figure",
        "portrait",
        211,
    ),
    (
        "full-anchor-b",
        "standing alone on winter prairie, a blanket roll under one arm, a small sheathed knife at his belt, no gun, snow and gray sky, 1858, full figure",
        "portrait",
        215,
    ),
    # Angles
    (
        "bust-threequarter",
        "three-quarter view portrait, winter prairie behind him, 1858",
        "portrait",
        301,
    ),
    (
        "bust-profile",
        "profile view portrait, looking into the far distance, winter prairie, 1858",
        "portrait",
        302,
    ),
    (
        "bust-firelight",
        "portrait by the light of a small campfire at night, darkness behind him, 1858",
        "portrait",
        303,
    ),
    (
        "bust-blanket-hood",
        "portrait, a worn blanket drawn over his head and shoulders against the cold, snow falling, 1858",
        "portrait",
        304,
    ),
    # Activities (full figure)
    (
        "full-walking",
        "walking across snowy prairie with a steady unhurried pace, following a distant buffalo herd, full figure, 1858",
        "portrait",
        401,
    ),
    (
        "full-writing",
        "seated on a low rise writing in a small leather journal with a short pencil, winter prairie around him, full figure, 1858",
        "portrait",
        402,
    ),
    (
        "full-fire",
        "crouched on his heels by a small fire in a snow hollow, a tin cup in his hands, full figure, 1858",
        "portrait",
        403,
    ),
    (
        "full-behind",
        "seen from behind, standing on a rise watching a buffalo herd in a valley below, full figure, winter, 1858",
        "portrait",
        404,
    ),
    (
        "full-blanket-wrapped",
        "wrapped in a worn blanket over head and shoulders, standing in falling snow, full figure, 1858",
        "portrait",
        405,
    ),
    # Distance
    (
        "distant-ridge",
        "a small solitary figure on a ridgeline at great distance, walking behind a buffalo herd, vast winter prairie, 1858",
        "landscape",
        501,
    ),
    # Seasons
    (
        "full-summer",
        "standing in tall summer prairie grass under a high sky, clothes hanging loose, full figure, 1857",
        "portrait",
        601,
    ),
    (
        "full-autumn",
        "walking through autumn prairie, gold cottonwoods along a creek behind him, full figure, 1857",
        "portrait",
        602,
    ),
    (
        "bust-summer",
        "portrait, summer prairie and a high sky behind him, 1857",
        "portrait",
        603,
    ),
    # Top-up round (2026-07-08): boots now in the identity block; re-tries
    # for the barefoot/staging failures of round 1
    (
        "full-fire-b",
        "crouched on his heels by a small fire in a snow hollow, a tin cup in his hands, worn boots on his feet, full figure, 1858",
        "portrait",
        411,
    ),
    (
        "full-back",
        "walking away from the viewer across snowy prairie, his back to us, following a buffalo herd far ahead in the distance, full figure seen from behind, 1858",
        "portrait",
        412,
    ),
    (
        "full-summer-b",
        "standing in tall summer prairie grass, his beard down past his chest, clothes hanging loose, worn boots, full figure, 1857",
        "portrait",
        611,
    ),
    (
        "bust-summer-b",
        "portrait of the same lean weathered man, summer prairie behind him, 1857",
        "portrait",
        612,
    ),
    (
        "full-following",
        "a lean ragged figure walking a hundred yards behind a buffalo herd, steady unhurried stride, seen from the side at middle distance, winter prairie, 1858",
        "landscape",
        511,
    ),
    (
        "bust-threequarter-b",
        "three-quarter view portrait looking off to the left, winter prairie, 1858",
        "portrait",
        311,
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
        path = OUT / f"morrow_{name}_s{seed}.png"
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
    print("BREED_DONE")


if __name__ == "__main__":
    main()
