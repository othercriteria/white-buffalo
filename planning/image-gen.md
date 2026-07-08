# Image-Gen Phase

Role (decided 2026-07-07): image generation is a **coherence auditor and
illustration source**, not an imagination source. Prompts are derived from
`notes/visual-bible.md` (every claim cited to drafts/) — never invented, never
imported from `../z-image` (whose story decisions are not canon; see memory).
Where a prompt can't be written because the bible is silent, that's a finding:
either the text is thin there or the detail is deliberately unspecified.

## Infrastructure (2026-07-08)

- `flake.nix`: merged writing + image-gen shells (uv, ruff, CUDA, git-lfs).
  Restart the Claude Code session inside `nix develop` before pipeline work.
- Git LFS enabled (`git lfs install --local`); `.gitattributes` tracks
  `art/**` images and `*.safetensors`.
- `imagegen/`: Python project (uv). Pins carried from the known-working
  `../z-image` env; revisit after model decision.
- Layout: `imagegen/output/` = working generations (gitignored);
  `art/` = curated finals (LFS). Base model weights never enter the repo.
- Hardware: RTX 4090 24 GB, 251 GB RAM. Reuse the HF cache / existing
  downloads where possible; ../z-image has Z-Image base + split files (~20 GB).

## What carries over from ../z-image (technical only)

- Working stack: diffusers `ZImagePipeline` (bf16, CPU offload), Qwen3-4B
  text encoder, musubi-tuner for character LoRA training on the 4090.
- The Morrow character LoRA (`../z-image/lora_output/`) was trained on
  **non-canon reference images** (wrong age/season assumptions). Do not reuse
  without validating its subject against the bible's Morrow spec; expect to
  regenerate the reference set from the bible and retrain.
- The old `generate.py` SCENES list is a cautionary artifact: albino buffalo,
  blue uniforms at Buena Vista, `killer_approach` / `murder_discovery` /
  battlefield-carnage scenes — non-canon details and direct violations of the
  do-not-illustrate rule. Nothing from it is reused verbatim.

## Rules

1. **Prompt-extraction discipline.** Every visual claim in a prompt must trace
   to a cited line in the visual bible. Prompts live in versioned files with
   their citations alongside.
2. **Do-not-illustrate list** (`notes/visual-bible.md` §"Do-not-illustrate")
   is enforced at the prompt-catalog level: evidence, not events. The killings,
   Morrow's death, and the ending's resolution stay off-page in images exactly
   as in text.
3. **Coherence-audit loop.** When a generation looks wrong, first ask whether
   the prompt (and thus the bible, and thus the text) underdetermines or
   contradicts itself — that's the valuable output. Model artifacts are noise;
   textual findings get filed against drafts/ like any continuity finding.
4. **Style is a decision, not a default.** Candidate registers (period
   engraving, painterly, photographic) get A/B'd and put to DK before any
   full catalog run.

## Plan

1. ~~Flake + LFS + imagegen scaffold~~ (done 2026-07-08)
2. Session restart in `nix develop`; `uv sync`; smoke-test generation
3. Model decision: Z-Image vs successor (survey commissioned 2026-07-08)
4. Prompt catalog v1 from visual bible (scenes + citations + DNI enforcement)
5. Style A/B on 2-3 scenes → DK picks register
6. Character reference sets from bible spec; LoRA training (Morrow first)
7. Catalog run; coherence findings filed; curation to art/
