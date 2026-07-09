#!/usr/bin/env bash
# Travois LoRA validation grid. Run AFTER train_village.sh completes —
# never concurrently (the 4090 cannot hold both; morrow grid 1 failed
# silently on exactly that contention).
#
# PLAN (decision criteria, zoom-gate all of these at 2x):
#   1. Concept: pole pairs dragging in LOW TRIANGLES behind horses —
#      no wagons, no harness teams, no plain riders standing in for drags.
#   2. Distance: does the concept survive at tiny-silhouette scale
#      (P2, the production scene)? This was the original capability wall.
#   3. Register: linework must stay engraving under the style prefix —
#      half the dataset is grayscaled oils; watch for painterly mush.
#   4. Leakage: no standing tipis in the moving scene, no Miller
#      mountains, no willow cages where the text doesn't ask.
#   5. Multiplier response: 1.0 vs 1.3 on the production scene; morrow
#      needed 1.3, a concept may saturate earlier.
# Baseline row = final checkpoint at multiplier 0.0 (same seed) — the
# controlled epoch-0 equivalent; the seven pre-LoRA failures in
# output/plates are the informal baseline.
set -euo pipefail
cd "$(dirname "$0")"

SNAP="/fastcache/dlk/huggingface/hub/models--Tongyi-MAI--Z-Image/snapshots/04cc4abb7c5069926f75c9bfde9ef43d49423021"
DIT="$SNAP/transformer/diffusion_pytorch_model-00001-of-00002.safetensors"
VAE="/home/dlk/workspace/z-image/models/models/split_files/vae/ae.safetensors"
TE="/home/dlk/workspace/z-image/models/models/split_files/text_encoders/qwen_3_4b.safetensors"

NEG_LIGHT="text, caption, border, photograph, color"
# P2 runs under production conditions: style prefix + style negative + scene negative (catalog.toml village-passing, verbatim)
NEG_PROD="color, photograph, modern, digital, painting, soft focus, text, letters, words, caption, title, inscription, signature, plate number, border, frame, margin, mountains, peaks, crags, cliffs, alpine, trees, forest, faces, close-up, foreshortening, wagons, covered wagons, tipis standing, dust cloud, color, tinted, hand-colored, artist signature, monogram, lettering"

P1="1850s steel engraving illustration, a single horse dragging a travois, two long lodge-poles trailing on the ground in a low triangle behind the horse, bundles lashed between the poles, an Indian woman riding the horse, open prairie"
P2="1850s steel engraving artwork, fine crosshatching, monochrome ink on cream paper, detailed linework, the engraved image itself filling the entire frame edge to edge, strictly monochrome ink, horses dragging long lodge-poles that trail behind them on the ground in low triangles, pole-drags behind horse after horse, bundles slung between the trailing poles, small dog-drawn pole-drags low among them: a Lakota village moving as a broad loose procession of tiny dark silhouettes along a distant low ridgeline two miles off, riders scattered ahead and on the flanks, a separate loose mass of driven horses trailing, seen from far across open autumn prairie under a wide gray sky, figures far too small for faces, brown October grass in the empty foreground"
P3="1850s steel engraving illustration, three horses dragging travois down a grassy slope toward a shallow creek, long pole-drags leaving furrows in the grass, riders and dogs among them, seen level from a low rise"

gen() { # gen <out-name> <prompt> <multiplier> <lora-file> <neg> <w> <h>
    local out="$1" prompt="$2" mult="$3" lora="$4" neg="$5" w="$6" h="$7"
    [ -e "output/validate_village/${out}" ] && { echo "skip $out"; return; }
    uv run python musubi-tuner/src/musubi_tuner/zimage_generate_image.py \
        --dit "$DIT" --vae "$VAE" --text_encoder "$TE" \
        --lora_weight "$lora" --lora_multiplier "$mult" \
        --prompt "$prompt" --negative_prompt "$neg" \
        --image_size "$w" "$h" --infer_steps 36 --guidance_scale 4 \
        --seed 42 --fp8_llm \
        --save_path "output/validate_village/${out}" 2>&1 | tail -3
    echo "done $out"
}

mkdir -p output/validate_village
LF="output/village_travois_v1.safetensors"

# Baseline (controlled epoch-0: multiplier 0.0, same seed)
gen "p1_base_m00" "$P1" 0.0 "$LF" "$NEG_LIGHT" 1216 832
gen "p2_base_m00" "$P2" 0.0 "$LF" "$NEG_PROD" 832 1216

# Checkpoint ladder at 1.3
for ckpt in 000004 000008 000012; do
    L="output/village_travois_v1-${ckpt}.safetensors"
    gen "p1_${ckpt}_m13" "$P1" 1.3 "$L" "$NEG_LIGHT" 1216 832
    gen "p2_${ckpt}_m13" "$P2" 1.3 "$L" "$NEG_PROD" 832 1216
done
gen "p1_final_m13" "$P1" 1.3 "$LF" "$NEG_LIGHT" 1216 832
gen "p2_final_m13" "$P2" 1.3 "$LF" "$NEG_PROD" 832 1216

# Multiplier response on the production scene
gen "p2_000008_m10" "$P2" 1.0 "output/village_travois_v1-000008.safetensors" "$NEG_PROD" 832 1216
gen "p2_final_m10" "$P2" 1.0 "$LF" "$NEG_PROD" 832 1216

# Generalization probe (novel composition, mid-distance)
gen "p3_000012_m13" "$P3" 1.3 "output/village_travois_v1-000012.safetensors" "$NEG_LIGHT" 1216 832
gen "p3_final_m13" "$P3" 1.3 "$LF" "$NEG_LIGHT" 1216 832

echo VILLAGE_GRID_DONE
