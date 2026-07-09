#!/usr/bin/env python3
"""Production seed sweep for village-passing with the travois LoRA.

Single pipeline load; reads prompt/negative/aspect/lora from the
production catalog so the sweep tests exactly what generate.py ships.
"""

import tomllib
from pathlib import Path

import torch
from diffusers import ZImagePipeline
from generate import ASPECTS, DEFAULT_LORA_WEIGHT, LORAS, MODEL, REVISION

HERE = Path(__file__).parent
OUT = HERE / "output" / "village"
SCENE = "village-passing"
SEEDS = [140, 141, 142, 143, 144, 145]  # v2e4 round; 130-135 were v1
STYLE = "engraving"


def main():
    with open(HERE / "catalog.toml", "rb") as f:
        scene = tomllib.load(f)[SCENE]
    with open(HERE / "styles.toml", "rb") as f:
        style = tomllib.load(f)[STYLE]

    OUT.mkdir(parents=True, exist_ok=True)
    print(f"Loading {MODEL} @ {REVISION[:8]}...")
    pipe = ZImagePipeline.from_pretrained(
        MODEL, revision=REVISION, torch_dtype=torch.bfloat16
    )
    pipe.enable_model_cpu_offload()

    name, _, w = scene["lora"].partition("@")
    weight = float(w) if w else DEFAULT_LORA_WEIGHT
    pipe.load_lora_weights(HERE / LORAS[name], adapter_name=name)
    pipe.set_adapters([name], adapter_weights=[weight])

    width, height = ASPECTS[scene.get("aspect", "landscape")]
    for seed in SEEDS:
        out_path = OUT / f"{SCENE}_{STYLE}_s{seed}.png"
        if out_path.exists():
            print(f"skip {out_path.name}")
            continue
        print(f"Generating {out_path.name} ({width}x{height}, {name}@{weight})")
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
