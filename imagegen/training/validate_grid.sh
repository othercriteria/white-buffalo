#!/usr/bin/env bash
# Checkpoint validation grid for the Morrow LoRA (bash: zsh's no-word-split
# broke argument expansion when this lived inline).
set -euo pipefail
cd "$(dirname "$0")"

SNAP="/fastcache/dlk/huggingface/hub/models--Tongyi-MAI--Z-Image/snapshots/04cc4abb7c5069926f75c9bfde9ef43d49423021"
DIT="$SNAP/transformer/diffusion_pytorch_model-00001-of-00002.safetensors"
VAE="/home/dlk/workspace/z-image/models/models/split_files/vae/ae.safetensors"
TE="/home/dlk/workspace/z-image/models/models/split_files/text_encoders/qwen_3_4b.safetensors"

P1="jmorrow, 1850s steel engraving illustration, bust portrait of the man, bare willows and a frozen creek behind him"
P2="jmorrow, 1850s steel engraving illustration, full figure of the man kneeling beside a frozen buffalo carcass in snow, cutting meat with a knife, gray winter sky"

gen() { # gen <out-name> <prompt> [lora-args...]
    local out="$1" prompt="$2"; shift 2
    [ -e "output/validate/${out}" ] && { echo "skip $out"; return; }
    uv run python musubi-tuner/src/musubi_tuner/zimage_generate_image.py \
        --dit "$DIT" --vae "$VAE" --text_encoder "$TE" "$@" \
        --prompt "$prompt" \
        --negative_prompt "text, caption, border, photograph, color" \
        --image_size 1216 832 --infer_steps 36 --guidance_scale 4 \
        --seed 42 --fp8_llm \
        --save_path "output/validate/${out}" 2>&1 | grep -E 'Done!|Error' | tail -1
    echo "done $out"
}

for ckpt in 000004 000008 000012; do
    L="output/morrow_engraving_v1-${ckpt}.safetensors"
    gen "p1_${ckpt}" "$P1" --lora_weight "$L" --lora_multiplier 1.0
    gen "p2_${ckpt}" "$P2" --lora_weight "$L" --lora_multiplier 1.0
done
gen "p2_final" "$P2" --lora_weight "output/morrow_engraving_v1.safetensors" --lora_multiplier 1.0

echo GRID_DONE
find output/validate -name '*_000.png' | sort
