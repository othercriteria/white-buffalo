#!/usr/bin/env python3
"""High-resolution refinement pass for promoted plates (Z-Image img2img).

Resolution strategy (B2): base renders are 1216x832-class; print wants
more. Same-seed re-generation at higher res is a full reroll (latent
shape changes), so the path is: Lanczos-upscale the blessed render,
then refine with ZImageImg2ImgPipeline under the SAME catalog prompt/
negative and a seeded generator. `--strength` is the load-bearing dial:
too low = soft upscale wearing engraving clothes; too high = the
composition we blessed starts to reroll. Sweep it, zoom-gate the
results like any other sweep. paper_clamp afterwards as usual.

Test case (2026-07-18, DK): homestead-alive s967 — watch whether the
figure pair's gender read pops as detail rises, with NO prompt tweaks.

Usage:
  hires_refine.py SCENE INPUT.png --seed N [--scales 1.5 2.0]
                  [--strengths 0.25 0.35 0.45] [--steps 40]
"""

import argparse
from pathlib import Path

import tomllib
import torch
from diffusers import ZImageImg2ImgPipeline
from PIL import Image

MODEL = "Tongyi-MAI/Z-Image"
REVISION = "04cc4abb7c5069926f75c9bfde9ef43d49423021"
HERE = Path(__file__).parent


def snap16(x: float) -> int:
    return int(round(x / 16)) * 16


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("scene", help="Scene key from catalog.toml")
    ap.add_argument("input", type=Path, help="Blessed base render (pre-clamp)")
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--scales", type=float, nargs="+", default=[1.5, 2.0])
    ap.add_argument("--strengths", type=float, nargs="+", default=[0.25, 0.35, 0.45])
    ap.add_argument("--steps", type=int, default=40)
    ap.add_argument("--guidance", type=float, default=4.0)
    ap.add_argument("--output-dir", type=Path, default=HERE / "output" / "hires")
    ap.add_argument(
        "--lora",
        help="Character LoRA name or name@weight (see generate.LORAS). "
        "Default: the scene's catalog 'lora' field — refinement must "
        "honor scene identity (learned on speaking-to-her: refining a "
        "LoRA-born figure without its LoRA pulls it off-model). "
        "Pass 'none' to disable.",
    )
    ap.add_argument(
        "--sequential",
        action="store_true",
        help="sequential CPU offload: much slower, far less VRAM "
        "(needed for net >2x targets on a shared 24GB card)",
    )
    args = ap.parse_args()

    with open(HERE / "catalog.toml", "rb") as f:
        catalog = tomllib.load(f)
    scene = catalog[args.scene]
    prompt, negative = scene["prompt"], scene.get("negative", "")

    from generate import DEFAULT_LORA_WEIGHT, LORAS

    lora_spec = args.lora or scene.get("lora")
    if lora_spec == "none":
        lora_spec = None
    lora = None
    if lora_spec:
        name, _, wgt = lora_spec.partition("@")
        if name not in LORAS:
            ap.error(f"unknown lora {name!r} (have: {', '.join(LORAS)})")
        lora = (name, float(wgt) if wgt else DEFAULT_LORA_WEIGHT)

    base = Image.open(args.input).convert("RGB")
    w0, h0 = base.size
    args.output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Loading {MODEL} @ {REVISION[:8]} (img2img)...")
    pipe = ZImageImg2ImgPipeline.from_pretrained(
        MODEL, revision=REVISION, torch_dtype=torch.bfloat16
    )
    if lora:
        name, weight = lora
        pipe.load_lora_weights(HERE / LORAS[name], adapter_name=name)
        pipe.set_adapters([name], adapter_weights=[weight])
        print(f"  lora: {name}@{weight}")
    if args.sequential:
        pipe.enable_sequential_cpu_offload()
    else:
        pipe.enable_model_cpu_offload()
    # Large targets (net 2.5-3x) OOM in VAE decode group_norm on a
    # 24GB card; tiled VAE + attention slicing trade a little speed
    # for headroom. Both are no-ops where unsupported.
    for meth in ("enable_vae_tiling", "enable_attention_slicing"):
        try:
            getattr(pipe, meth)()
            print(f"  {meth}: on")
        except Exception as e:
            print(f"  {meth}: unavailable ({e})")

    for scale in args.scales:
        w, h = snap16(w0 * scale), snap16(h0 * scale)
        up = base.resize((w, h), Image.LANCZOS)
        for strength in args.strengths:
            name = f"{args.scene}_s{args.seed}_x{scale:g}_d{strength:g}.png"
            out = args.output_dir / name
            if out.exists():
                print(f"  skip {name} (exists)")
                continue
            print(f"Refining {name} ({w}x{h}, strength={strength})")
            kwargs = dict(
                prompt=prompt,
                negative_prompt=negative,
                image=up,
                strength=strength,
                num_inference_steps=args.steps,
                guidance_scale=args.guidance,
                generator=torch.Generator("cuda").manual_seed(args.seed),
            )
            try:
                image = pipe(cfg_normalization=False, **kwargs).images[0]
            except TypeError:
                image = pipe(**kwargs).images[0]
            image.save(out)
            print(f"  saved {out}")


if __name__ == "__main__":
    main()
