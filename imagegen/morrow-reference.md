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
- Coat: shapeless dark wool coat, badly worn (text: [gap] coat/hat/boots —
  bible flags this gap; the coat must exist for winter plates).
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
