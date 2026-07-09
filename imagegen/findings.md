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

## Gibberish suppression (2026-07-08, rounds v2-v3)

- v2 (negatives only: "text, letters, caption, ..."): 1/3 clean. Negatives
  alone don't reliably beat the register prior.
- v3 (also removed "book illustration" and "antique print" from the PREFIX,
  added "the engraved image itself filling the entire frame edge to edge"):
  4/4 free of captions. The furniture was invited by the positive tokens,
  not under-suppressed by the negative. Lesson generalizes: debug the
  positive prompt before stacking negatives.
- Residue: occasional thin plate margins and a faint corner signature —
  trivially croppable; acceptable. SFT rung not needed for gibberish.
- Still open (register prior, SFT-curation targets if we train a style
  LoRA): narrative calming (blizzard still comes back as brisk winter
  riding, rider mounted despite "leading"), occasional invented staffage
  (background riders), loose spatial staging (horse drifts into the
  hollow; invented dugout door at s44).

## Shared-seed rhyme (DK observation from ../z-image, confirmed 2026-07-08)

Same seed + same dimensions → same initial latent → shared low-frequency
blocking across different prompts; the prompt decides only what the masses
become. DK's example (06_homesteaders ↔ 07_buena_vista: foreground furrows
become bodies) measures +0.713 low-freq luminance correlation vs +0.38
median across all final/ pairings. Both eye-legible and measurable.

Exploitable as deliberate visual rhyme — a parallel left for the reader,
never announced (inside the tic discipline). Candidate pairs:
- morrow-hollow ↔ reading-night (Morrow writing / Farrell reading — the
  book's central transaction as shared bones)
- first-sighting ↔ finale-fifty-yards (calf trailing the herd / cow facing
  Farrell)
- offering-stake ↔ graves (the two markers left in the ground)
Method: for an intended pair, sweep seeds and keep the seed maximizing the
correlation metric (script in this repo's history; formalize as
rhyme_scan.py if adopted). Same aspect ratio is required.

### Implications for the pick

A hybrid is available: one register for narrative chapters, wet-plate for
evidence/portrait plates. But a single register keeps the book's uniform
restraint. Decision is DK's (plan step 5).

## Plate 1: morrow-hollow (2026-07-08) — the engine's first full cycle

Three seeds at the original prompt: identity/kit/register all passed
(no horse, no gun, no tent — the absences held), but the HOLLOW never
rendered — figure-forward composition, shelter reduced to background
noise, across all three seeds.

Bounced off the text: NOT a text gap. The manuscript is concrete here
(12:113 "hollow in the bluffs where the wind cannot reach"; 19:5 "six
feet deep," cutbank). Failure was prompt attention order.

**Rule (generalizes):** when architecture is load-bearing, LEAD the
prompt with it and seat the figure inside it afterward ("a deep hollow
eroded into the face of a bluff... jmorrow, the man seated within it").
Figure-first prompts let the character eat the composition. Applies to:
trading-post, homestead, reading-night, final-camp scenes.

Environment LoRA (DK): compositionally available (multi-adapter, own
trigger, reduced stacked weights, figure-free training captions) —
RESERVED for when a recurring location needs cross-plate consistency
(the homestead family of scenes is the likely first case). Not needed
for single-plate geometry; prompt-ordering sufficed.

Pick: s45 → art/morrow-hollow.png. s46 = variance confirmation.

## Plate 2: journal-found (2026-07-08)

Round 1 (full kit manifest in prompt): all three seeds strained — objects
rendered as a floating still-life at postcard scale BESIDE a crater, not
inside a hollow. DK's diagnosis: too many charges; scale coherence fails.

**Rule (generalizes, joins prompt-order):** ~three compositional charges
per frame (geometry, one subject, one trace). The text's full inventories
stay in the text; the plate carries its one essential object. Kit manifest
cut to journal-on-blankets + footprints → all three seeds coherent.

Audit: s49 rejected FOR scale — a monumental grotto vs the text's
"perhaps six feet deep" (19:5); the towering darkness announces grief
(significance-smoothing, the register's version of a cadence line).
s51 text-truest but domestic-plump bedding. s45: bedroll-true, modest
scale, and the shared-seed rhyme with art/morrow-hollow.png measures
+0.668 vs +0.360/+0.434 for other seeds — the deliberate rhyme works
when the paired scenes differ (writing/found). Pick: s45 →
art/journal-found.png.

## Plate 3: offering-stake (2026-07-09)

The beat's first deep scrutiny (v0.8 addition): the timeline computes —
stake predates first snow (pre-Nov 14), riders return to their own site
Jan 3, herd crossing reveals it to Morrow Jan 9. "It faced the valley"
is Morrow's intention-attribution, unrenderable literally; translated
to position + streaming cloth. The cloth's RED is withheld from the
plate (monochrome register); spot-color hand-tint available but would
announce the cloth/blood red-thread — flagged, not used.

**Rule #3: the engraving genre's landscape prior is ALPINE.** All three
first-round seeds grew mountain crags in sand hills country (09:5 —
"broken ridges and deep draws," nothing taller for 300 miles). Plains
plates must assert landform positively ("low rolling treeless sand
hills") AND negate mountains. Infrastructure: catalog entries now
support per-scene `negative`; generate.py merges style + scene + CLI
negatives.

Pick: s53 (cloth streaming in threads = the load-bearing detail; herd
incidental; settled lean). s52 quieter but cloth reads as knotted wrap;
s54 cloth oversized. → art/offering-stake.png

## Plate 4: first-sighting (2026-07-09)

Two failed rounds first: base-model "white buffalo calf" = white DAIRY
calf (domestic morphology), herd drifts ox-ward, spring brown-grass
scenes pull warm tint (winter plates held monochrome only because snow
is achromatic), invented trees, "moving away" ignored.

**Rule #4: anatomy can be prompted at species-and-age granularity.**
The rescue block: positive morphology for BOTH herd ("shaggy dark humped
shoulders, massive low-slung heads") and calf ("stocky, woolly-headed,
first rise of a shoulder hump"); the whole domestic family negated
("cattle, cows, oxen, dairy calf, livestock, farm animals"); "strictly
monochrome ink" in the positive + "color, tinted, hand-colored" negated
for any non-winter plate. Buffalo LoRA NOT forced — reserved for HER
cross-plate identity at multiple ages (cover/finale will rule).

Pick: s57 (receding column, calf trailing at the rear, real bison-calf
morphology) → art/first-sighting.png. Seed 57 binds the finale rhyme
sweep. s55 = strong alternate (aloneness inverted: calf far, herd near).

## Plate 5: cover (2026-07-09)

Round 1: 4/4 rendered a normal dark bison with a frosted hump — "wild
American bison cow" led the prompt and the species token's brown prior
beat the trailing whiteness clause. **Rule #1 generalizes to color: the
defining attribute LEADS** ("a great pure white bison cow, white over
her whole body..."). Round 2: 4/4 white, herd held dark — no
contamination either direction.

Morphology adjudication AGAINST further iteration: all seeds run
bull-adjacent in horn mass and scale, and the text LICENSES it — horns
"curved and thickened" (16:17), "no cow reaches her size in three
summers," "biggest damn cow I ever saw" (07:179). She is a wrong-sized
cow; almost-bull-but-cow is canon, not drift. Do not un-wrong her.

Pick: s62 (whole-body white, breath steam, calm title sky, and her own
deep track-line in the snow — unprompted, canon per 13:61) →
art/cover.png.
