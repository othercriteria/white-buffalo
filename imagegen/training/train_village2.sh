#!/usr/bin/env bash
# Village travois LoRA v2: CONTINUATION from v1's final checkpoint on the
# physicality-augmented dataset (photos + structural diagrams). Fine
# checkpoint ladder (every 2 epochs) — physicality may peak before
# overfit. DK-directed 2026-07-09.
set -euo pipefail
cd "$(dirname "$0")"

SNAP="/fastcache/dlk/huggingface/hub/models--Tongyi-MAI--Z-Image/snapshots/04cc4abb7c5069926f75c9bfde9ef43d49423021"
DIT="$SNAP/transformer/diffusion_pytorch_model-00001-of-00002.safetensors"
VAE="/home/dlk/workspace/z-image/models/models/split_files/vae/ae.safetensors"
TE="/home/dlk/workspace/z-image/models/models/split_files/text_encoders/qwen_3_4b.safetensors"

DATASET="./village_dataset.toml"
OUT="./output"
NAME="village_travois_v2"

mkdir -p "$OUT" cache/village

echo "=== Step 1: cache latents (new items only) ==="
uv run python musubi-tuner/src/musubi_tuner/zimage_cache_latents.py \
    --dataset_config "$DATASET" \
    --vae "$VAE"

echo "=== Step 2: cache text encoder outputs (new items only) ==="
uv run python musubi-tuner/src/musubi_tuner/zimage_cache_text_encoder_outputs.py \
    --dataset_config "$DATASET" \
    --text_encoder "$TE" \
    --batch_size 4 --fp8_llm

echo "=== Step 3: continue training from v1 final ==="
uv run accelerate launch --num_cpu_threads_per_process 1 --mixed_precision bf16 \
    musubi-tuner/src/musubi_tuner/zimage_train_network.py \
    --dit "$DIT" \
    --vae "$VAE" \
    --text_encoder "$TE" \
    --dataset_config "$DATASET" \
    --network_weights output/village_travois_v1.safetensors \
    --sdpa --mixed_precision bf16 \
    --timestep_sampling shift --weighting_scheme none --discrete_flow_shift 2.0 \
    --optimizer_type adamw8bit --learning_rate 1e-4 --gradient_checkpointing \
    --max_data_loader_n_workers 2 --persistent_data_loader_workers \
    --network_module networks.lora_zimage --network_dim 32 \
    --max_train_epochs 6 --save_every_n_epochs 2 --seed 43 \
    --output_dir "$OUT" --output_name "$NAME"

echo "TRAINING_COMPLETE: $OUT/$NAME.safetensors"
