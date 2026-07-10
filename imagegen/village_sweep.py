#!/usr/bin/env python3
"""Production seed sweep for village-passing with the travois LoRA.

Single pipeline load; reads prompt/negative/aspect/lora from the
production catalog so the sweep tests exactly what generate.py ships.
"""

from pathlib import Path

import tomllib
import torch
from diffusers import ZImagePipeline
from generate import ASPECTS, DEFAULT_LORA_WEIGHT, LORAS, MODEL, REVISION

HERE = Path(__file__).parent
OUT = HERE / "output" / "village"
# Gap-fill batch round 1 (2026-07-10). homestead-alive sweeps seed 100
# among its candidates: homestead.png is s100, so the alive/dead rhyme
# is free if that seed's quality passes (shared-seed massing).
SWEEPS = {
    "speaking-to-her": [230, 231, 232],
}
STYLE = "engraving"


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

    for scene_key, seeds in SWEEPS.items():
        scene = catalog[scene_key]
        spec = scene.get("lora")
        lora_label = "none"
        if spec:
            name, _, w = spec.partition("@")
            weight = float(w) if w else DEFAULT_LORA_WEIGHT
            if name not in loaded:
                pipe.load_lora_weights(HERE / LORAS[name], adapter_name=name)
                loaded.add(name)
            pipe.set_adapters([name], adapter_weights=[weight])
            lora_label = f"{name}@{weight}"
        elif loaded:
            pipe.set_adapters(list(loaded), adapter_weights=[0.0] * len(loaded))

        width, height = ASPECTS[scene.get("aspect", "landscape")]
        for seed in seeds:
            out_path = OUT / f"{scene_key}_{STYLE}_s{seed}.png"
            if out_path.exists():
                print(f"skip {out_path.name}")
                continue
            print(f"Generating {out_path.name} ({width}x{height}, lora={lora_label})")
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
