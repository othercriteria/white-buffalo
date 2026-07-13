#!/usr/bin/env python3
"""Shared-seed rework sweep over catalog scenes.

Usage: rework_sweep.py <scene> [<scene> ...] -- <seed> [<seed> ...]
(defaults preserved: morrow-hollow/journal-found across 122-124, the
original joint rhyme-partner rework). Loads the pipeline once and
generates every scene at every seed. Reads prompts, negatives, aspects,
and LoRA specs from the production catalog/styles so the sweep tests
exactly what generate.py would ship.
"""

import sys
from pathlib import Path

import tomllib
import torch
from diffusers import ZImagePipeline
from generate import ASPECTS, DEFAULT_LORA_WEIGHT, LORAS, MODEL, REVISION

HERE = Path(__file__).parent
OUT = HERE / "output" / "rework"
SCENES = ["morrow-hollow", "journal-found"]
SEEDS = [122, 123, 124]
STYLE = "engraving"

if "--" in sys.argv[1:]:
    split = sys.argv.index("--")
    SCENES = sys.argv[1:split] or SCENES
    SEEDS = [int(s) for s in sys.argv[split + 1 :]] or SEEDS


def main():
    with open(HERE / "catalog.toml", "rb") as f:
        catalog = tomllib.load(f)
    with open(HERE / "styles.toml", "rb") as f:
        style = tomllib.load(f)[STYLE]

    OUT.mkdir(parents=True, exist_ok=True)
    print(f"Loading {MODEL} @ {REVISION[:8]}...")
    pipe = ZImagePipeline.from_pretrained(
        MODEL, revision=REVISION, torch_dtype=torch.bfloat16
    )
    pipe.enable_model_cpu_offload()
    loaded = set()

    for seed in SEEDS:
        for key in SCENES:
            out_path = OUT / f"{key}_{STYLE}_s{seed}.png"
            if out_path.exists():
                print(f"skip {out_path.name}")
                continue
            scene = catalog[key]
            spec = scene.get("lora")
            if spec:
                name, _, w = spec.partition("@")
                weight = float(w) if w else DEFAULT_LORA_WEIGHT
                if name not in loaded:
                    pipe.load_lora_weights(HERE / LORAS[name], adapter_name=name)
                    loaded.add(name)
                pipe.set_adapters([name], adapter_weights=[weight])
            elif loaded:
                pipe.set_adapters(list(loaded), adapter_weights=[0.0] * len(loaded))
            width, height = ASPECTS[scene.get("aspect", "landscape")]
            print(f"Generating {out_path.name} ({width}x{height})")
            image = pipe(
                prompt=f"{style['prefix']}, {scene['prompt']}",
                negative_prompt=", ".join(
                    filter(None, [style.get("negative", ""), scene.get("negative", "")])
                ),
                height=height,
                width=width,
                cfg_normalization=False,
                num_inference_steps=40,
                guidance_scale=4.0,
                generator=torch.Generator("cuda").manual_seed(seed),
            ).images[0]
            image.save(out_path)
            print(f"  saved {out_path}")


if __name__ == "__main__":
    main()
