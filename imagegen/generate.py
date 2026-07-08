#!/usr/bin/env python3
"""Z-Image generation CLI for White Buffalo.

Scene content comes from catalog.toml (derived from notes/visual-bible.md,
citations alongside — see planning/image-gen.md, "Rules"). Style registers
come from styles.toml and are applied as prefix + negative at generation
time. Free-prompt mode (--prompt) exists for smoke tests and probes only.
"""

import argparse
import tomllib
from pathlib import Path

import torch
from diffusers import ZImagePipeline

# Known-working revision carried over from ../z-image. The Jan 2026 Base
# checkpoint may live at a newer revision of this repo; reconcile before
# LoRA training (planning/image-gen.md, "Model decision").
MODEL = "Tongyi-MAI/Z-Image"
REVISION = "04cc4abb7c5069926f75c9bfde9ef43d49423021"

HERE = Path(__file__).parent

ASPECTS = {
    "portrait": (832, 1216),
    "landscape": (1216, 832),
    "square": (1024, 1024),
}


def load_toml(name: str) -> dict:
    with open(HERE / name, "rb") as f:
        return tomllib.load(f)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    src = parser.add_mutually_exclusive_group()
    src.add_argument(
        "--scene", help="Scene key from catalog.toml ('all' for every scene)"
    )
    src.add_argument("--prompt", help="Free prompt (smoke tests / probes only)")
    parser.add_argument(
        "--style", help="Style key from styles.toml ('all' for every style)"
    )
    parser.add_argument("--negative", default="", help="Extra negative prompt")
    parser.add_argument("--aspect", choices=ASPECTS, help="Override aspect")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--steps", type=int, default=40)
    parser.add_argument("--guidance", type=float, default=4.0)
    parser.add_argument(
        "--name", default="out", help="Filename prefix in --prompt mode"
    )
    parser.add_argument("--output-dir", type=Path, default=HERE / "output")
    parser.add_argument("--list", action="store_true", help="List scenes and styles")
    args = parser.parse_args()

    catalog = load_toml("catalog.toml")
    styles = load_toml("styles.toml")

    if args.list:
        print("Scenes:", ", ".join(catalog))
        print("Styles:", ", ".join(styles))
        return
    if not args.scene and not args.prompt:
        parser.error("one of --scene / --prompt is required (or --list)")

    if args.scene:
        scene_keys = list(catalog) if args.scene == "all" else [args.scene]
        for k in scene_keys:
            if k not in catalog:
                parser.error(f"unknown scene {k!r} (see --list)")
        jobs = [
            (k, catalog[k]["prompt"], catalog[k].get("aspect", "landscape"))
            for k in scene_keys
        ]
    else:
        jobs = [(args.name, args.prompt, args.aspect or "landscape")]

    style_keys = (
        list(styles) if args.style == "all" else [args.style] if args.style else [None]
    )
    for k in style_keys:
        if k is not None and k not in styles:
            parser.error(f"unknown style {k!r} (see --list)")

    args.output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Loading {MODEL} @ {REVISION[:8]}...")
    pipe = ZImagePipeline.from_pretrained(
        MODEL, revision=REVISION, torch_dtype=torch.bfloat16
    )
    pipe.enable_model_cpu_offload()

    for job_name, base_prompt, aspect in jobs:
        width, height = ASPECTS[args.aspect or aspect]
        for style_key in style_keys:
            if style_key:
                style = styles[style_key]
                prompt = f"{style['prefix']}, {base_prompt}"
                negative = ", ".join(
                    filter(None, [style.get("negative", ""), args.negative])
                )
                out_name = f"{job_name}_{style_key}_s{args.seed}.png"
            else:
                prompt, negative = base_prompt, args.negative
                out_name = f"{job_name}_s{args.seed}.png"

            print(f"Generating {out_name} ({width}x{height})")
            image = pipe(
                prompt=prompt,
                negative_prompt=negative,
                height=height,
                width=width,
                cfg_normalization=False,
                num_inference_steps=args.steps,
                guidance_scale=args.guidance,
                generator=torch.Generator("cuda").manual_seed(args.seed),
            ).images[0]
            image.save(args.output_dir / out_name)
            print(f"  saved {args.output_dir / out_name}")


if __name__ == "__main__":
    main()
