#!/usr/bin/env python3
"""Z-Image generation CLI for White Buffalo.

Scene content comes from catalog.toml (derived from notes/visual-bible.md,
citations alongside — see planning/image-gen.md, "Rules"). Style registers
come from styles.toml and are applied as prefix + negative at generation
time. Free-prompt mode (--prompt) exists for smoke tests and probes only.
"""

import argparse
from pathlib import Path

import tomllib
import torch
from diffusers import ZImagePipeline

# This pinned revision == hub main as of 2026-01-28, i.e. the Z-Image (Base)
# release state (verified 2026-07-08). Turbo is a separate repo/cache.
MODEL = "Tongyi-MAI/Z-Image"
REVISION = "04cc4abb7c5069926f75c9bfde9ef43d49423021"

HERE = Path(__file__).parent

ASPECTS = {
    "portrait": (832, 1216),
    "landscape": (1216, 832),
    "square": (1024, 1024),
    # Fold-out studies (format doctrine: one gatefold exception may
    # exist; candidate = village-passing). Two ratios: ~2.4:1 and ~2.5:1.
    "foldout": (1824, 768),
    "foldout-wide": (2048, 832),
}

# Character LoRAs (imagegen/loras/, diffusers format). Recipe per
# morrow-reference.md: "morrow" (final ckpt) for portraits, "morrow-ep12"
# for narrative scene plates. Prompts must carry the trigger "jmorrow"
# plus light descriptors; the register negative is load-bearing.
LORAS = {
    "morrow": "loras/morrow_engraving_v1_diffusers.safetensors",
    "morrow-ep12": "loras/morrow_engraving_v1_ep12_diffusers.safetensors",
    # Travois/moving-village concept. v2e4 = physicality continuation
    # (structure diagrams/photos), epoch-4 sweet spot: correct saddle
    # lashing on both probes, no detached-pole artifact (which returns
    # at v2-final). Deploy ~1.0; the full register negative is
    # load-bearing (grayscale-oil drift otherwise). v1 kept for record.
    "travois": "loras/village_travois_v2e4_diffusers.safetensors",
    "travois-v1": "loras/village_travois_v1_diffusers.safetensors",
}
DEFAULT_LORA_WEIGHT = 1.3


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
    parser.add_argument(
        "--lora",
        help="Character LoRA: name or name@weight (see LORAS). Overrides the "
        "scene's 'lora' field; scene entries may set lora = 'name@weight'.",
    )
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
            (
                k,
                catalog[k]["prompt"],
                catalog[k].get("aspect", "landscape"),
                catalog[k].get("lora"),
                catalog[k].get("negative", ""),
            )
            for k in scene_keys
        ]
    else:
        jobs = [(args.name, args.prompt, args.aspect or "landscape", None, "")]

    style_keys = (
        list(styles) if args.style == "all" else [args.style] if args.style else [None]
    )
    for k in style_keys:
        if k is not None and k not in styles:
            parser.error(f"unknown style {k!r} (see --list)")

    args.output_dir.mkdir(parents=True, exist_ok=True)

    def parse_lora(spec):
        if not spec:
            return None
        name, _, w = spec.partition("@")
        if name not in LORAS:
            parser.error(f"unknown lora {name!r} (have: {', '.join(LORAS)})")
        return name, float(w) if w else DEFAULT_LORA_WEIGHT

    print(f"Loading {MODEL} @ {REVISION[:8]}...")
    pipe = ZImagePipeline.from_pretrained(
        MODEL, revision=REVISION, torch_dtype=torch.bfloat16
    )
    loaded_loras = set()
    pipe.enable_model_cpu_offload()

    for job_name, base_prompt, aspect, scene_lora, scene_negative in jobs:
        lora = parse_lora(args.lora or scene_lora)
        if lora:
            name, weight = lora
            if name not in loaded_loras:
                pipe.load_lora_weights(HERE / LORAS[name], adapter_name=name)
                loaded_loras.add(name)
            pipe.set_adapters([name], adapter_weights=[weight])
        elif loaded_loras:
            pipe.set_adapters(
                list(loaded_loras), adapter_weights=[0.0] * len(loaded_loras)
            )
        width, height = ASPECTS[args.aspect or aspect]
        for style_key in style_keys:
            if style_key:
                style = styles[style_key]
                prompt = f"{style['prefix']}, {base_prompt}"
                negative = ", ".join(
                    filter(
                        None, [style.get("negative", ""), scene_negative, args.negative]
                    )
                )
                out_name = f"{job_name}_{style_key}_s{args.seed}.png"
            else:
                prompt = base_prompt
                negative = ", ".join(filter(None, [scene_negative, args.negative]))
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
