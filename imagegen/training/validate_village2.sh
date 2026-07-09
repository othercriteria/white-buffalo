#!/usr/bin/env bash
# v2 continuation ladder — physicality check. P1 (close single travois)
# is where rigging improvement shows first; P2 verbatim production scene
# confirms it survives at distance. Same gates as validate_village.sh.
# NOTE: musubi --image_size is HEIGHT WIDTH.
set -euo pipefail
cd "$(dirname "$0")"

SNAP="/fastcache/dlk/huggingface/hub/models--Tongyi-MAI--Z-Image/snapshots/04cc4abb7c5069926f75c9bfde9ef43d49423021"
DIT="$SNAP/transformer/diffusion_pytorch_model-00001-of-00002.safetensors"
VAE="/home/dlk/workspace/z-image/models/models/split_files/vae/ae.safetensors"
TE="/home/dlk/workspace/z-image/models/models/split_files/text_encoders/qwen_3_4b.safetensors"

NEG_LIGHT="text, caption, border, photograph, color, oil painting, tonal wash"
NEG_PROD="color, photograph, modern, digital, painting, soft focus, text, letters, words, caption, title, inscription, signature, plate number, border, frame, margin, mountains, peaks, crags, cliffs, alpine, trees, forest, faces, close-up, foreshortening, wagons, covered wagons, cart, wheels, sled, sledge, harness team, plow, tipis standing, dust cloud, oil painting, tonal wash, soft wash, tinted, hand-colored, artist signature, monogram, lettering"

P1="1850s steel engraving illustration, a single horse dragging a travois, two long lodge-poles trailing on the ground in a low triangle behind the horse, bundles lashed between the poles, an Indian woman riding the horse, open prairie"
P2="1850s steel engraving artwork, fine crosshatching, monochrome ink on cream paper, detailed linework, the engraved image itself filling the entire frame edge to edge, strictly monochrome ink, horses dragging long lodge-poles that trail behind them on the ground in low triangles, pole-drags behind horse after horse, bundles slung between the trailing poles, small dog-drawn pole-drags low among them: a Lakota village moving as a broad loose procession of tiny dark silhouettes along a distant low ridgeline two miles off, riders scattered ahead and on the flanks, a separate loose mass of driven horses trailing, seen from far across open autumn prairie under a wide gray sky, figures far too small for faces, brown October grass in the empty foreground"

gen() { # gen <out-name> <prompt> <multiplier> <lora-file> <neg> <h> <w>
    local out="$1" prompt="$2" mult="$3" lora="$4" neg="$5" h="$6" w="$7"
    [ -e "output/validate_village2/${out}" ] && { echo "skip $out"; return; }
    uv run python musubi-tuner/src/musubi_tuner/zimage_generate_image.py \
        --dit "$DIT" --vae "$VAE" --text_encoder "$TE" \
        --lora_weight "$lora" --lora_multiplier "$mult" \
        --prompt "$prompt" --negative_prompt "$neg" \
        --image_size "$h" "$w" --infer_steps 36 --guidance_scale 4 \
        --seed 42 --fp8_llm \
        --save_path "output/validate_village2/${out}" 2>&1 | tail -3
    echo "done $out"
}

mkdir -p output/validate_village2

for ckpt in 000002 000004; do
    L="output/village_travois_v2-${ckpt}.safetensors"
    gen "p1_${ckpt}_m13" "$P1" 1.3 "$L" "$NEG_LIGHT" 832 1216
done
LF="output/village_travois_v2.safetensors"
gen "p1_final_m13" "$P1" 1.3 "$LF" "$NEG_LIGHT" 832 1216
gen "p2_000004_m10" "$P2" 1.0 "output/village_travois_v2-000004.safetensors" "$NEG_PROD" 1216 832
gen "p2_final_m10" "$P2" 1.0 "$LF" "$NEG_PROD" 1216 832
gen "p2_final_m08" "$P2" 0.8 "$LF" "$NEG_PROD" 1216 832

echo VILLAGE_GRID2_DONE
