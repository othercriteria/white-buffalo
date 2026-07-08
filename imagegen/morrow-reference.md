# Morrow reference set (for character LoRA)

Goal: a DK-approved set of engraving-register portraits that lock Morrow's
appearance for the LoRA. Everything in "Canon" is cited via the visual bible;
everything in "Reference choices" is underdetermined by the text and gets
FIXED here for visual consistency only — these choices are not canon and
must never migrate into prose.

The old ../z-image Morrow LoRA is not reused: trained on non-canon refs
(wrong age/period assumptions) and in a photographic register.

## Canon (visual-bible §Morrow)

- Born Virginia 1824 → 32 when he leaves (12:47), ~34 by the final winter.
- Witnessed (all 1858, the only outside descriptions): "thin as a rail,
  beard down to his chest" (05:117); "Tall. Thin. Beard like a bird's nest"
  (09:95); "nothing in his eyes. Nothing at all" (07:183).
- Self: "My clothes hang loose" (04:13); "my body is thinner than it has
  ever been" (12:63); clothes "so worn they barely deserved the name" (19:19).
- Kit if shown: blanket, knife, flint and steel, tin cup, journal, short
  pencil (06:21, 19:19). NO gun (02:13). On foot, steady pace (15:87).
- Corpse posture (if ever needed): on his back, arms wide, face peaceful,
  eyes open (20:5-11) — DNI: traces only.

## Reference choices (underdetermined; DK signed off 2026-07-08)

- Hair: dark, gone long and unkempt; grayed at the temples by 1858.
  (Text gives nothing; dark reads as default for engraving contrast.)
- Face: long, high-boned, deep-set eyes — supports "nothing in his eyes"
  read at plate resolution.
- Coat: shapeless dark wool coat, badly worn. UPGRADE (full-read
  2026-07-08): the coat and a shirt are canon — the corpse wears both
  ("His coat was torn, his shirt beneath it shredded," 20:13) — and worn
  boots are canon via his tracks (15:87). Only color/material/cut remain
  reference choices.
- Hat: none. (Never mentioned in 2.5 years of text; bareheaded is the
  bolder and equally licensed choice, and distinguishes him from Farrell,
  who has a hat, 07:85.) Survivability rider (DK): in winter plates the
  blanket — the one head-covering his cited kit actually contains (06:21)
  — may be worn over head and shoulders; period-true, consistent with how
  the text has him survive (buried in snow 08:5, hollows 08:37), and it
  strengthens the silhouette. Bareheaded proper is for fair-weather and
  portrait plates.
- Mexican War flashback (DK): if ever illustrated, he IS hatted —
  Mississippi Rifles campaign kit was famously red shirt, white duck
  trousers, broad-brimmed black felt hat. Note: 1846-47 Morrow (early 20s,
  fed, soldierly) is a different visual identity, outside this LoRA's
  scope; he would be prompted fresh, not LoRA'd. No war scene is in
  catalog v1.
- Period: late (1858) look — the emaciated vigil-keeper. All witnessed
  descriptions are from 1858; early-period Morrow (1856, fresh from
  Virginia) appears in no illustratable scene.

## Bearing (full-read 2026-07-08 — key art direction)

Morrow is a soldier gone to rags, NOT a wild man. What unnerves every
witness is his composure, not his dishevelment: the walk is "steady. Not
fast, not slow, never once stopping to look around" (07:121), "like he had
all the time in the world" (07:175); the handwriting is "careful, formal"
across years (19:35); the camp is neat, blankets "neatly arranged," the
journal set out "as if left to be found" (19:21-23); the graves he dug are
deliberate, stones "placed just so" (13:17-23). Eyes read as FLAT and
still — "nothing in his eyes. Nothing at all" (07:179) — never intense,
never crazed. The wildness lives in beard and rags only; the posture is
erect, the movements deliberate. In prompts: "quiet unhurried bearing,"
"level far-off gaze," never "wild-eyed" — and reject candidates whose
gaze does the Monster Manual work the text refuses.

## Breed round 1 curation (2026-07-08)

Identity held across all 18 — the block is working. Failures are kit/
staging drift, not face drift.

KEEP (12): bust-anchor s121, bust-anchor-b s125, bust-anchor-c s126,
bust-threequarter s301, bust-profile s302, bust-firelight s303,
bust-blanket-hood s304 (the winter blanket-hood look works), full-anchor
s211, full-anchor-b s215, full-writing s402 (also a plate candidate),
full-blanket-wrapped s405, full-walking s401 (staging off-canon — herd
beside not ahead — but identity and kit right; LoRA learns appearance,
not staging).

DROP (6): full-fire s403 and full-behind s404 (barefoot — boots were
missing from the identity block, now added), full-summer s601 and
full-autumn s602 (beard inflates to waist-length; s602 also barefoot),
bust-summer s603 (age drift, corner signature), distant-ridge s501
(composition fail — gave a foreground bust; note: distant plates don't
need the identity block or LoRA at all).

Top-up round (seeds 311, 411-412, 511, 611-612): KEEP s411 (fire, boots
correct now), s311 (three-quarter full-length), s511 (following the herd
— staging drift again, identity strong). DROP s412 ("back to us" still
rendered a front view — the identity block's face tokens overpower view
directives; back/distance shots must be prompted WITHOUT the identity
block, which is fine since they never need the LoRA), s611 (summer beard
inflation again), s612 (proportion failure).

**FINAL TRAINING SET (15), pending DK sign-off:** s121, s125, s126, s301,
s302, s303, s304, s211, s215, s401, s402, s405, s411, s511, s311.

## Training notes

- Register: train on engraving-style refs so identity and the book's
  decided style cohere (styles.toml).
- Trainer: musubi-tuner against Z-Image (Base) — hyperparameters still
  settling per community (planning/image-gen.md); budget iteration.
  bitsandbytes/triton need the training-env fix (gcc in shell) before this
  starts.
- Reference set: ~16-24 images. Vary: angle (profile/three-quarter/front),
  distance (bust/full figure), setting (hollow camp, open snow, following
  the herd at distance), season permitting winter emphasis.
