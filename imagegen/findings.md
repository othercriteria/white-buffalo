# Image-gen findings log

Per planning/image-gen.md rule 3: generation failures are first read as
coherence findings (prompt → bible → text), then as register/model behavior.
Textual findings get filed against drafts/; register behaviors get recorded
here so prompts and expectations adjust.

## Style A/B, round 1 (2026-07-08; seed 42, 40 steps, CFG 4)

Scenes: cover, blizzard, reading-night × engraving, painterly, wet-plate,
cinematic. Grid: output/style-ab-contact-sheet.png.

### Register behaviors (systematic, will recur)

- **engraving** pulls hard toward its training genre: invents plate
  furniture — gibberish captions, publisher lines, borders. Croppable or
  negative-promptable ("no text, no caption"), but it also *calms* scenes
  toward natural-history composition: the blizzard came back as a serene
  winter portrait, whiteout suppressed. Strong period authority; weak
  narrative adherence.
- **painterly** warms and dramatizes: the buffalo's coat rendered
  cream/tawny — a direct conflict with canon ("Not pale, not cream-colored,"
  02:27). Golden-hour bias even under a prompted gray sky. Prompt-side
  fixes possible ("white as snow and bone, cold light") but the register
  fights the book's gray restraint.
- **wet-plate** poses its subjects (long-exposure logic: figures stop and
  face the lens — right for portraits, wrong for narrative scenes) and
  invents staffage: the blizzard gained a crowd of extra riders and
  figures. Whites render gray-silver, which suits her "silver sheen" but
  reads mid-gray, not white. Best register for *evidence* shots (graves,
  stake, homestead) and portraits; poor for action.
- **cinematic** adheres best by far — the only register that gave the
  blizzard as written (man LEADING the horse, visibility collapsed, alone)
  and the reading-night with correct staging (horse at the hollow's edge,
  small figure, big dark country). Cost: a modern eye; it is the only
  register with no 1850s existence.

### Scene-level notes

- cover: engraving and wet-plate read "white" via medium (line negative
  space / silver); painterly violated coat canon; cinematic morphology
  drifted ox-ward. All four rendered bull-heavy morphology — "cow" in the
  prompt is not enough; may need "buffalo cow, slighter horns" phrasing.
- reading-night: three of four put the horse inside the hollow (text: tied
  to the stunted pine at the edge, 19:11). Spatial prepositions are weak;
  consider composing these shots as two beats or accepting the drift.
- No text-driven (bible-level) contradictions surfaced this round — all
  mismatches trace to register priors, not to gaps in the visual bible.

### Implications for the pick

A hybrid is available: one register for narrative chapters, wet-plate for
evidence/portrait plates. But a single register keeps the book's uniform
restraint. Decision is DK's (plan step 5).
