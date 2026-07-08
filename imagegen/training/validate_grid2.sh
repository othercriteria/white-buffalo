#!/usr/bin/env bash
# Round 2: checkpoint grid at the working recipe (multiplier 1.3 + light
# descriptors), plus two probes disambiguating the white-background effect
# (multiplier 2.0 vs missing negative prompt).
set -euo pipefail
cd "$(dirname "$0")"

SNAP="/fastcache/dlk/huggingface/hub/models--Tongyi-MAI--Z-Image/snapshots/04cc4abb7c5069926f75c9bfde9ef43d49423021"
DIT="$SNAP/transformer/diffusion_pytorch_model-00001-of-00002.safetensors"
VAE="/home/dlk/workspace/z-image/models/models/split_files/vae/ae.safetensors"
TE="/home/dlk/workspace/z-image/models/models/split_files/text_encoders/qwen_3_4b.safetensors"
NEG="text, caption, border, photograph, color"

P1="jmorrow, 1850s steel engraving illustration, bust portrait of the tall thin bearded man, bare willows and a frozen creek behind him"
P2="jmorrow, 1850s steel engraving illustration, full figure of the tall thin bearded man kneeling beside a frozen buffalo carcass in snow, cutting meat with a knife, gray winter sky"
PV="jmorrow, 1850s steel engraving illustration, full figure of a tall thin bearded man standing in snow, a blanket roll under one arm, worn boots"

gen() { # gen <out-name> <prompt> <multiplier> <lora-file> [--no-neg]
    local out="$1" prompt="$2" mult="$3" lora="$4" negopt=("--negative_prompt" "$NEG")
    [ "${5:-}" = "--no-neg" ] && negopt=()
    [ -e "output/validate2/${out}" ] && { echo "skip $out"; return; }
    uv run python musubi-tuner/src/musubi_tuner/zimage_generate_image.py \
        --dit "$DIT" --vae "$VAE" --text_encoder "$TE" \
        --lora_weight "$lora" --lora_multiplier "$mult" \
        --prompt "$prompt" "${negopt[@]}" \
        --image_size 1216 832 --infer_steps 36 --guidance_scale 4 \
        --seed 42 --fp8_llm \
        --save_path "output/validate2/${out}" 2>&1 | grep -E 'Done!' | tail -1
    echo "done $out"
}

mkdir -p output/validate2

for ckpt in 000004 000008 000012; do
    L="output/morrow_engraving_v1-${ckpt}.safetensors"
    gen "p1_${ckpt}_m13" "$P1" 1.3 "$L"
    gen "p2_${ckpt}_m13" "$P2" 1.3 "$L"
done
LF="output/morrow_engraving_v1.safetensors"
gen "p1_final_m13" "$P1" 1.3 "$LF"
gen "p2_final_m13" "$P2" 1.3 "$LF"

# Background probes
gen "probe_verbatim_m20_withneg" "$PV" 2.0 "$LF"
gen "probe_verbatim_m13_noneg" "$PV" 1.3 "$LF" --no-neg

echo GRID2_DONE
