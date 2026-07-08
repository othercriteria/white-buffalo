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

## Model decision (2026-07-08, from commissioned survey)

**Stay on Z-Image; train LoRAs against Z-Image (Base).** No successor exists:
"Z-Image 2" was never released, and Z-Image-Edit / Omni-Base remain
unpublished (Tongyi-MAI HF org checked). The material update is **Z-Image
(Base)**, the non-distilled foundation checkpoint (Jan 2026, 6B, Apache-2.0,
diffusers support merged upstream) — it removes the late-2025 pain point of
LoRA-training against the distilled Turbo. musubi-tuner supports it
first-class (docs/zimage.md), though community reports (issue #908) say Base
training hyperparameters are still settling; budget iteration.

- Inference: Turbo for fast drafts, Base (28–50 steps, CFG 3–5) for finals.
- Revision reconciled 2026-07-08: the pinned `04cc4abb` in generate.py equals
  hub main (lastModified 2026-01-28 = Base release); the cached 20 GB
  snapshot in /fastcache IS the Base checkpoint. Both repos cached locally.
- Fallback if Z-Image LoRA fidelity disappoints: FLUX.2 klein 4B base
  (Jan 2026, Apache-2.0, ~13 GB bf16, LoRA-trainable on a 4090 in ~1 h).
  Ruled out: Qwen-Image-2.0 (API-only), Ideogram 4.0 (non-commercial
  license), FLUX.2 dev (32B, non-commercial).
- Watch: Z-Image-Edit, if ever released — instruction-based editing would
  help character-consistent scene variants without a stack change.

## Plate policy (DK + model aligned, 2026-07-08)

**Journal entries may show Morrow (LoRA'd); Farrell chapters contribute
evidence and places only; Farrell himself is never depicted.** Farrell is
the seer, not the seen — the plates show what witness shows: Morrow's
world as the journal describes it, the evidence as Farrell finds it.
Rationale: a generic Farrell would contrast distractingly off Morrow's
LoRA-locked specificity; omission is cheaper and truer than a second
LoRA. The coherence engine keeps full-text coverage via figureless
evidence plates. Where a Farrell-chapter scene demands his position,
compose from BEHIND his eyes (e.g., the finale: the buffalo faces the
viewer). If he's ever wanted (frontispiece pair), the breeding+training
machinery is proven (~an afternoon; before/after states per
farrell-reference.md anchors s701/s702 as caption tokens).

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
3. ~~Model decision~~ (done 2026-07-08: Z-Image, Base for training; see above)
4. Prompt catalog v1 from visual bible (scenes + citations + DNI enforcement)
5. ~~Style A/B~~ (done 2026-07-08: **engraving**, DK's pick from the 12-image
   grid; register behaviors in imagegen/findings.md)
6. ~~Character reference sets; Morrow LoRA~~ (done 2026-07-08: 15-image
   set signed off, morrow_engraving_v1 trained on Base, validated on a
   novel-scene probe, deployed at multiplier ~1.3 — see
   imagegen/morrow-reference.md §Training results. Farrell stays
   prompt-only with s701/s702 as before/after anchors.)
   - Plate-gibberish ladder (DK, 2026-07-08): (1) negative prompt — in test;
     (2) style-LoRA SFT on curated caption-free engraving plates — likely the
     robust fix, can also target the register's narrative-calming pull via
     curation; (3) cropping as the acknowledged fallback.
   - SFT data options: self-distillation (train on our own cropped
     generations — no sourcing needed) or public-domain 19th-c. plates
     (Internet Archive, Old Book Illustrations) for compositional variety.
7. Catalog run; coherence findings filed; curation to art/
