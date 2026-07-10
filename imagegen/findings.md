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

## Rule #5: period vantage (DK, 2026-07-09, from the cover sweep)

Foreshortened, low-angle, close poses (cover s65/s71) read MODERN: they
imply a point of view accessible only through photography and modern
optics — a closeness no 1859 field artist could have had with a wild
buffalo. The imagined engraver worked from sketchable distance: eye
level or a gentle rise, subject's whole form in the picture plane,
profile or three-quarter composition. This extends the diegetic
discipline from WHAT is shown to HOW SEEING WORKED. Prompt side:
"her whole form in view, seen level from a respectful distance";
negative side: "close-up, foreshortening, low angle, dramatic
perspective, wide-angle, looming". Applies to every plate with a living
subject; evidence/object plates (stake, journal) may stand nearer, as
their subjects permit approach.

## Cover resolved (DK, 2026-07-09): s78, no reservations

The period-vantage round (rule #5) closed the search. s78 = full profile
at sketchable distance, whole form in the picture plane, PLUS the living
details from the s62 line (breath steaming, her track-line, herd faint
beyond, calm title-ready sky) — the creature and the naturalist's plate
in one image. s62 retired to alternate; s74 (purest period plate:
walking profile, Hornaday posture) retained as a STUDY/REFERENCE for
future buffalo plates — its stance and snow texture are the register's
benchmark. s76/s77 rejected for an invented steam column near the herd
(reads as campfire — an uncanonical presence in her wintering valley).

## Plate 6: finale-fifty-yards + joint re-pick of the bookend pair (2026-07-09)

Round 1 (4 seeds): three violations — the blood rendered RED (spot color:
the announced red-thread we refused for the stake), Farrell summoned into
frame by the vantage phrase "from a kneeling man's height" (name a thing,
get the thing), and a fat sun disc vs canon's "invisible but present"
(20:51 — the audit's first canonical-light catch). Round 2 fixed all
three; the discriminator became blood PLACEMENT (canon: chest and
forelegs, 20:21 — the mechanics of goring and trampling).

Seed 57 (the rhyme seed) refused chest placement across three rolls: in
three-quarter view the bison breast hides behind beard and foreleg mass,
so stains land on the visible flank canvas. Frontal stance wouldn't take
(the period-vantage negatives reinforce plate-classic side views).

**Resolution: joint re-pick of the pair on seed 55.** finale-s55 lands
the blood low-front correctly with rhyme +0.369 (≈ s57's +0.392);
first-sighting-s55 (the aloneness alternate) re-audits as faithful — the
view from Morrow's rise mid-pass, herd near below, calf hung back.
Lesson: RHYME PAIRS ARE PICKED JOINTLY, never sequentially — locking one
member first can strand the other on an unworkable seed.

art/first-sighting.png := s55 (was s57); art/finale-fifty-yards.png :=
s55. The book's frame closes on shared bones: the calf's latent skeleton
carries the cow.

## Bookend pair re-picked on s87 after DK's zoom catch (2026-07-09)

DK caught a malformed calf and a three-legged bull in the promoted
first-sighting s55 — figures small enough to pass contact-sheet review.
**Process fix: mandatory 2x crop-zoom of all small figures before any
promotion.** Guidance/steps jitter on the fixed seed could not rescue it
(~30px calves are an anatomical lottery; a resolution floor, not a
prompting problem).

Joint sweep of 8 fresh seeds, both bookends screened together: 6/8
first-sightings failed zoom (sheep-calves, lost whiteness, white ADULTS
at wrong age — the model fights this subject constantly). s87 passed
both gates on both scenes: a true bison calf trailing the column with a
legible gap, and a finale where the frontal watching stance — which
three rounds of prompting couldn't force on s57 — arrived free, with
canonical chest/foreleg blood. Rhyme +0.492, the strongest measured
pair. The zoom catch bought a better pair than the one it broke.

art/first-sighting.png := s87; art/finale-fifty-yards.png := s87.

## Plate 7 in progress: graves (2026-07-09) — held for research

s91 passes the core audit (flat-laid stones in rough rectangles, low
mounds, NO crosses — the cross-negative beat the grave prior) but fails
on two background elements, and DK's questions opened a third:

- **House**: frame gable + masonry chimney vs canon cut-earth blocks,
  sod roof, stovepipe (11:53-79).
- **Willows (DK catch)**: the model drew WEEPING willows — an Asian
  ornamental absent from 1858 Nebraska, supplied because weeping willow
  is the century's mourning emblem: given graves + willows, the genre
  prior reaches for cemetery iconography. Botanical error AND
  announced-significance error in one. Real Niobrara creek flora:
  sandbar willow THICKETS (the text's own "brown and thick," 11:3, is
  correct) + peachleaf willow (small, upright); cottonwood as the big
  watercourse tree; ponderosa on north slopes (11:7 is accurate — a
  genuine Niobrara feature); treeless uplands. Fix: "low brushy willow
  thickets" positive + "weeping willow" negative.
- **Construction realism (DK)**: research agent out on what two people
  could build in 16 months (house/barn/well/cellar/field) and — bearing
  directly on this plate — whether flat cairn stones are even
  gatherable in stone-poor sand hills country. If the text's specs fail
  the research, that's the engine's first manuscript-level finding.

Plate held until the research reports; house/willow/stone fixes go into
one re-roll.

## Principle (DK, 2026-07-09): research-grounded specificity is the move

The graves2 round (post-construction-research) is "more specific,
interesting, and unsettling" than graves1 (generic priors) — DK. Why:
generic priors produce generic mood ("frontier graves" as an
illustration idea); researched specificity produces the documentary
uncanny (a real soddy's stovepipe, stone that comes from somewhere).
Correctness reads as evidence, not art — which is the manuscript's own
register (procedural concreteness, critique §8) transferring to the
plates. STANDING RULE: when material culture carries a scene, commission
the research BEFORE prompt-craft. The reference docs
(homestead-construction.md, lakota-white-buffalo.md, pd-engraving-
sources.md) are now part of the prompt pipeline, not background.

## Plate 7: graves (2026-07-09) — first vignette, three rounds

Round 1: cross-negative held; cairn form right at s91 but house rendered
frame+chimney and willows rendered WEEPING (mourning-emblem prior).
Round 2 (post-research): house perfected (textbook Niobrara soddy) but
cairns regressed to dolmens/cones — the enriched house description ate
the attention budget. **Corollary to rule #2 banked: the attention
budget is zero-sum across charges; compress validated details to their
minimal token once won.** Round 3 (house compressed): s93 passes all
gates — flat-stone-blanketed low rectangles side by side, spare gathered
slabs scattered near (the hauling legible), willow thickets, sod massing
at distance. Note: a weeping willow returned THROUGH the negative in
s91 — negatives are probabilistic, not gates; the zoom check remains the
gate. → art/graves.png (landscape; in-text vignette per format doctrine).

## Batch round 1 status (2026-07-09)

- fort-kearny: s103 PASSED all gates (frame + sod buildings legible,
  flagstaff, young planted cottonwood rows — the research's flagged
  absence rendered; no wall, no people) → art/fort-kearny.png. The
  approach-view s104 rejected: "long low sod buildings" rendered as
  anachronistic round hay bales.
- trading-post: s104 near-final; single flaw = candlelit window rendered
  warm yellow — spot color, same violation class as red blood/red cloth,
  refused consistently. Re-roll with "pale ink tone" language.
- village-passing: comprehensive fail round 1 — wagons THROUGH the
  negative, zero travois triangles; a settler column in Lakota position.
  Re-roll with the travois front-loaded and structural ("long
  lodge-poles trailing in low triangles behind horse after horse").
- homestead: s100 near (walls read cobble at zoom; sod-brick-course
  language in re-roll). morrow-witnessed: s98 near (the tiny figure wore
  a HAT — Farrell's marker on Morrow's silhouette; bareheaded/long-
  bearded asserted in re-roll).
- Color-leak pattern: autumn/dusk scenes leak tint (3/4 village seeds,
  the warm window) — non-winter plates need the monochrome assertion AND
  luck; the zoom gate catches what the negatives miss.

## Batch round 2 (2026-07-09)

- trading-post: s104 re-roll PASSES (window in pale ink tone; log walls
  banked with sod per the research — and now per the TEXT, DK-authorized
  edit a8f8f41) → art/trading-post.png
- homestead: s100 promoted WITH CAVEAT — wall texture reads lumpy-cobble
  at 2x zoom but sod-course at vignette print size; the sod-brick
  re-roll language produced log walls (the "courses" concept maps to
  logs in the prior). Revisit if the vignette prints larger than
  expected. → art/homestead.png
- fort-kearny: PULLED from art/ (DK blocking catch: smoke rising from
  the flagstaff top — the model fused flag and chimney into a
  smokestack). Re-roll running with smoke bound to the buildings and the
  staff explicitly bare.
- morrow-witnessed: s107's bareheaded figure passes identity but stands
  AMONG the herd (canon for JE II's acceptance, wrong for the witness
  testimony that the scene illustrates). Walking-behind re-roll running.
- village-passing: CAPABILITY WALL after 7 attempts — the model has no
  visual concept for horse-travois (renders harness teams, wagons, or
  plain riders). The forcing case for DK's predicted concept-LoRA has
  arrived: train a micro-LoRA on PD Catlin/Miller moving-village images
  (the imagined engraver's own reference corpus). Decision pending.

## Batch round 3 (2026-07-09)

- fort-kearny: s108 PASSES all gates at zoom — the flagstaff is a clean
  bare pole with a small flag and visible halyard, NO smoke fusion (DK's
  blocking catch resolved at prompt level: "nothing else on the pole" +
  smoke explicitly bound to chimneys). Chimney smoke on the buildings,
  parade ground open, unstockaded, cottonwood rows slender and bare.
  Foreground model-fill: a hitching rail with a tied horse — period-
  plausible, no human figure, accepted. s109 rejected (reads farmstead,
  stray horizontal smoke streak in the sky). → art/fort-kearny.png
- morrow-witnessed: s108 REJECTED — figure carries a long staff (reads
  herder/drover) and walks abreast of the herd. s109 near: bareheaded,
  dark-coated, empty-handed, following — but only ~20 yards off the last
  animal; at that gap he reads as a drover, not the trader's "dog that's
  lost its master." The GAP is a compositional charge and must be
  asserted, not implied by "trailing a hundred yards behind" (numeric
  distances don't render). Re-roll with "separated from the herd by a
  long stretch of empty unbroken snow" + staff/spear/drover negatives
  (seeds 110-113).
- morrow-witnessed round 2 (seeds 110-113): the gap-assertion language
  worked — all four seeds detached the figure from the herd. s111
  rejected (figure running), s113 rejected (herd toward viewer, figure
  standing mid-column — a watcher, not a follower), s112 rejected on
  vantage (best FIGURE of the set: chest-length beard, balding fringe,
  reads as Morrow — but rendered large/close, violating rule #5 and the
  distance rule). s110 PASSES: tiny bareheaded walking figure, empty
  hands, open snow around him; gap reads ~30 yards, accepted — the
  emptiness carries the trader's "dog that's lost its master" (09:87).
  → art/morrow-witnessed.png. Batch4 closed; every batch scene except
  village-passing (capability wall) is now in art/.

## Rework: morrow-hollow / journal-found round 2 (2026-07-09)

DK verdict on the originals: "immature and awkward" against the later
plates — confirmed on re-inspection: both violate rule #5 (viewer inside
the camp), both render the hollow as a fairy-tale cave mouth, both
predate the register negatives, and journal-found carries a canon error
("first light"; Farrell finds the camp AT DUSK, 19:5). Research-first:
reference/hollow-camp-research.md (scoop-not-cave cues, drift cornice /
dry lee floor, engraved-nocturne conventions, hat-sized chip/brush
fires). Rhyme reframed writing/found -> occupied/abandoned. rhyme.py
added (reproduces logged pair values within resize noise).

Sweep 1 (seeds 120-125, both scenes, shared seeds):
- journal-found: transformed. All six render a modest scoop — no cave
  mouth anywhere. s123 PASSES all zoom gates: single stunted pine, snow
  cornice with drip forms, folded striped trade blankets (period-right),
  the dark book legible, charred stick-ends + ash streak for the cold
  fire (only seed where the pit is legible), clean single bootprint
  line. Fire sits just inside the hollow — matches the research (fire
  between man and opening). CANDIDATE FINAL.
- morrow-hollow: camp nailed, vigil missed. s123's figure passes zoom
  (LoRA legible at small scale: gaunt, long beard, bareheaded, blanket
  over shoulders, worn boots, low stick fire, layered cutbank bedding)
  but the herd rendered as TWO large bison close by, no white cow —
  "I can see her from here" absent. All six seeds put the hollow in the
  ground plane (blowout reading) rather than a bluff face; acceptable,
  research-supported. v2: camp language compressed (attention-budget
  corollary), freed budget spent on "hundreds of tiny dark animals
  massed in the far distance" + white cow as "one small pale point."
- Pair correlations sweep 1: s123 +0.601, s120 +0.527, s122 +0.463,
  s124 +0.339, s125 +0.192, s121 +0.165. s123 won both scenes AND the
  correlation — joint pick was unanimous; v2 re-measures after the
  morrow-hollow re-prompt (same-seed kinship survives prompt changes).

Process note: a 13GB GPU process appeared mid-rework and pattern-matched
our known zombie failure — it was DK's ollama llama-server (different
owner, 4 min old). The kill attempt failed on permissions, correctly.
CHECK PROCESS OWNER AND CMD before killing anything holding VRAM; the
sweep now queues behind a free-VRAM guard instead.

## Rework rounds 2-3: the pair lands at s122 (2026-07-09)

v2 (camp compressed, herd budget): vigil content landed — s122/s123/s124
all massed the herd with a legible white cow — but the fire died (unlit
stick piles; "burning almost flameless" had been cut to fund the herd).
Rule reinforced: EVERY charge needs its state asserted — "a fire" buys
sticks, not flame. v3 reinstated one clause ("burning before him, its
low flame the one bright point in the hollow"), seeds 122-124:
- s122 PASSES everything: white flame-star stick fire (the register's
  only pure paper-white), best Morrow face of the rework (bareheaded,
  blanket at shoulders), seepage-striped wall + ice forms at the lip
  (both research details), massed herd with the white cow luminous and
  slightly apart (08:39 nearly verbatim).
- s123 DISQUALIFIED: letter-gibberish stamped mid-frame on the drift lip
  (uncroppable) + marginal fire. s124: fire dead again.
- Joint pick moved s123 -> s122; journal-found s122 then passed its full
  gates (book on blankets, charred fire-pit patch beside the exiting
  footprint line, single stunted pine, clean corners). Its landform is
  the truest to 19:7 of all six seeds (hollow in a hillside lee, not a
  crater).
Pair correlation +0.562 (bookends +0.484; the old pair's +0.66 was
inflated by twin cave-mouth compositions). PROMOTED:
art/morrow-hollow.png + art/journal-found.png = the s122 pair.
Occupied/abandoned axis: lit/unlit, him/his absence, night/dusk.

## Village travois LoRA: trained and validated (2026-07-09)

Trained on 14 curated PD images (the imagined engraver's reference
corpus: Catlin, Bodmer, Eastman, Miller, Remington, Russell, Deming,
Leslie's) — morrow recipe verbatim (dim 32, lr 1e-4, 16 epochs, 2240
steps, ~1h40m). Validation grid (validate_village.sh, 14 images):
- CONVERGENCE IS LATE: the wagon/cart/harness prior persists through
  ep12; only the FINAL checkpoint drops wheels for true pole-drag
  geometry on both the close probe and the production scene. Deploy
  final only (unlike morrow's ep12 split).
- The capability wall is DOWN: production-conditions probe at final
  renders Catlin-grade travois (parallel drag lines, pole triangles,
  procession) vs the baseline's harness-teams-with-wagon.
- Multiplier: 1.0 and 1.3 both carry the concept; 1.0 composes closer
  to the text's two-mile distance. Deploy @1.0.
- REGISTER NEGATIVE IS LOAD-BEARING (again): under a light negative the
  final ckpt drifts to grayscale-oil washes (P3 probe); under the full
  production negative it stays crisp engraving. Scene negative hardened:
  cart/wheels/sled/harness team/plow + oil painting/tonal wash.
- Known pull to fight in production: the LoRA wants travois in the NEAR
  field (dataset compositions are close views); the text pins the
  village at two miles (12:59). Distance language must hold.
- Harness note: musubi --image_size is HEIGHT WIDTH (P1/P2 aspects came
  out swapped in the grid; concept judgments unaffected).
Registered in generate.py as "travois"; catalog village-passing set to
travois@1.0. Production sweep seeds 130-135 rolling.

## Village production sweep 1 (seeds 130-135): concept yes, physicality no

DK's validation-grid diagnosis confirmed under production conditions —
every seed renders a travois procession, none promotable. Defect
taxonomy for continuation training:
1. DETACHED POLES (worst, most common): poles as independent ground
   rails, lashed to nothing (s132/s133 pick-up-sticks).
2. Wrong attachment: chest/flank emergence instead of crossed-and-lashed
   over withers/saddle (s130 foreground).
3. Loads migrate to horseback (pack-saddle) instead of the pole rack.
4. Near-field pull as predicted: fore/midground travois vs the text's
   two-mile emptiness; s130/s131 carry good distant ridge-lines but
   with crowded foregrounds.
Plan (DK-directed): dataset v2 = +2 flagged photos (NARA Stump Horn is
the textbook rigging profile) + ethnographic line diagrams (Wissler
1910, Ewers BAE 159 — structure in the native register); captions name
the mechanism ("two poles crossed and lashed over the saddle at the
withers, butt ends dragging behind"); continuation from the final
checkpoint via --network_weights, ~6 epochs, save every 2; try @0.8 in
the next sweep against the near-field pull.

## Village v2 continuation: physicality validated, ep4 is the deploy (2026-07-09)

Structure references worked exactly as DK predicted. v2 ladder:
- P1 close probe: ep2 poles cross at the wrong end (mid-air X over the
  drag); ep4 TEXTBOOK — lashed at the saddle, fore-ends splayed up past
  the withers (the LOC-photo geometry, visibly learned), drag ends
  grounded with a lashed load; v2-final regresses to clutter (an
  unattached pole set at frame edge).
- P2 production: ep4 @1.0 = the best village composition of the project
  (procession legible at three depths, drags attached, crisp register);
  v2-final reintroduces DETACHED POLE RAILS in the foreground at both
  1.0 and 0.8.
- Curriculum note: 6 continuation epochs; the physicality peak came at
  +4, overfit/clutter by +6 — the fine ladder (save every 2) earned its
  keep. Deployed: village_travois_v2e4_diffusers @1.0 (generate.py
  "travois"; v1 kept as "travois-v1"). Scene negative gains "loose
  poles lying on the ground". Production sweep seeds 140-145 rolling.

## Register drift quantified; village v4 (2026-07-09)

DK's eye on s153 ("drifted in a way... that would show up in pixel and
3x3 patch statistics") -> register.py built (mean/ink/paper fraction,
3x3 local std, |Laplacian|; z-scores vs the promoted corpus). Finding:
the drift is BLANK PAPER — corpus 25%+/-12, every travois-LoRA
candidate 71-76% (z +3.8 to +4.2); linework stats scatter both ways.
The LoRA's Catlin-outline plates and diagram pages taught
sparse-on-white; the distance composition gave it room. v4: tonal
coverage forced in the prompt (worked sky, dense-hatched grass, "no
blank paper"), sparse-outline negatives, plus a weight-0.8 probe pair.
register.py joins the gate battery alongside rhyme.py and the zoom
gate. B (resting travois) retired: one seed resolved, one rendered
tipi-cones; the canon anchors (combed pole-marks + dog-travois
midground) made it unnecessary.

Text: JE VI gains the travois dismissal ("They moved their whole world
on the poles. Everything I own rolls into one blanket. There is nothing
in my life that needs dragging.") — DK's question about Morrow's
relationship to the technology answered in canon: conscious
professional dismissal, the divestment theology completing the passage.
Farrell untouched: he never encounters one; his store-bought saddlebag
logistics ARE the contrast, structurally.

## Village v4 -> v5: the tonal pendulum (2026-07-09)

v4's forcing language over-corrected: paper 74% -> 5-7% (corpus
25%+/-12); every candidate drifted DARK (mean z -3.4, hf z +3..+5).
Instructive negative result: the weight-0.8 probe was INKIER than 1.0 —
the base register fills tone more aggressively than the LoRA, so
weight is not the tonal lever; language is. DK on v4: "much more like
it... in the neighborhood." s162 the near-lander (worst z 2.9; genuine
period cumulus in ruled tone). v5 calibration: "heavy gray sky" ->
"pale gray, lightening toward the top", "dense" -> "open" hatching,
6-seed landing pool with register.py in the launch command itself —
the gate is now part of the sweep.

## VILLAGE-PASSING LANDED: s175 promoted (2026-07-09)

v5 calibration returned tone to the corpus envelope (mean/ink/paper all
inside; DK: no proactive optimization on the remaining texture numbers
unless drift grows). Zoom verdicts: s175 = the text's geometry (the
line bending wide around the rise, double file), pole-drags correctly
grounded and legible at silhouette scale, ruled period sky. s170 = DK's
impressionistic favorite (upswept LOC-style fore-ends absorbed as
upslope perspective, the liveliest file of the set) — kept as the named
alternate, one-command swap if preferred. s174 taught the closing
lesson: at the text's honest two miles the subject dissolves into
generic animals — the period engraver's distance compression is
NECESSARY, not a compromise. Five prompt generations, two LoRA training
runs, one text enrichment: the capability wall is a plate.
-> art/village-passing.png. Catalog coverage complete except
shelved-by-policy scenes and the new gap-fill batch.

## Fold-out validated (2026-07-09)

First panorama studies at 2048x832 (~2.5:1): NO repetition stamping, no
composition breakdown — the line subject wants the long frame. s181 is
the standing candidate: a continuous travois file (upswept crossed
poles, grounded drags — s170's energy at panorama scale), dogs and
walkers threaded through, register consistent with v5. s180 elegant but
rider-heavy. Process notes: the zsh no-word-split hazard struck AGAIN
(a set -- $spec loop passed "foldout 180" as one token; exit 0, zero
files — file verification caught it); and generate.py filenames don't
carry aspect, so the wide pair overwrote the 1824x768 pair — use
separate --output-dir per aspect until the pattern includes it. Ratio
choice (2.4 vs 2.5:1) is a bindery question; fold-out vs portrait
coexistence is an assembly decision — both are banked.

## Catherine shelved by decision (2026-07-10)

The studies did their job: s190 proved the capability (immaculate
oval-vignette genre form, credible grave face) and thereby made the
cost concrete — DK, on seeing them: leaning against inclusion
"regardless of quality." Shelved as a DECISION, not a gap: the absent
center stays absent, the same principle that keeps Farrell undepicted.
Banked from the round: the googly-eye fix transfers (assert eye quality
positively — settled, slightly lowered, lids heavy from the exposure —
plus wide/staring negatives); daguerreotype sitters make the fix
period-true for any future portrait.

## Gap-fill batch: homestead pair landed (2026-07-10)

- homestead-interior s210 -> art/ after round 2 (room compressed per the
  zero-sum corollary, budget to the traces): dress-and-coat pair, tipped
  propped chair, and a re-tamped floor patch that reads faintly
  grave-like — the right accident. Caveat: plank-read walls (same class
  as homestead.png's texture caveat). r2 also taught: multi-room
  hallucination is the interior's leak mode (2/3 seeds).
- homestead-alive s210 -> art/ after v2 (house asserted in the dead
  plate's sod-course language; model-fill DOG cut — the text never gives
  the Hardins one, and the killing logistics quietly depend on that
  absence). s210 = textbook soddy + the JE V clothesline tableau.
  Rhyme note: v2's s100 improved to +0.443 but its house read as a
  cellar mound — quality beat the free rhyme; s210 pairs with
  homestead.png semantically (same building, summer/winter), not by
  massing (+0.119). 14 promoted plates.
- speaking-to-her r1-2: inversion lesson — rich subject description is
  a foreground magnet regardless of distance-leading; v3 borrows the
  cover's whole-form-at-respectful-distance grammar.
- tracks-north r2: positive absence WORKED (frames empty); per-print
  description invites crater-scale prints; v3 describes only the trail.

## speaking-to-her landed; GENERATION PHASE CLOSED (2026-07-10)

v4 broke the inversion (3/3 lateral) — the fix was BOTH moves at once:
starve the magnet (calf reduced to "a small white shape", zero
morphology) AND flex to landscape (two-subject lateral compositions are
intrinsically horizontal; homestead-alive precedent). Rule banked:
in a two-subject scene, any richly described subject eats the
foreground — describe the SPACE, starve the subjects, let the layout
carry them. s231 promoted: bison-right white calf with her HEAD RAISED
TOWARD HIM — 04:61's "She raised her head and looked at me" landed
unprompted — Morrow identity-legible on his rise, a hundred yards of
wind-bent grass between them, the herd a faint line.

SCOREBOARD: 16 plates in art/ — every unshelved catalog scene promoted.
tracks-north s222 (two trails, one heavier) closed the evidence chain;
the homestead alive/dead pair closed the watching theme. Shelved by
policy: broken-oar, blizzard, reading-night. Shelved by decision:
catherine-daguerreotype. Deferred to assembly: ferry-bridge (gap
check), fold-out s181 vs portrait s175, corner-crop pass, plate
placement.

## DK's four catches: three re-rolls + the paper clamp (2026-07-10)

1. speaking-to-her: whites-vs-cream fixed by PHYSICS, not re-roll —
   paper_clamp.py (bright-band paper estimate; margins useless, plates
   fill edge to edge). The sun became reserved paper, which is how
   period engravings render suns. AUDIT FINDING: the violation is
   universal (0.5-10% of pixels on all 16 plates; village-passing worst)
   — batch clamp offered as an assembly-phase pass for DK's eyeball.
2. homestead (dead) s241 re-promoted: the alive/dead pair now shows THE
   SAME BUILDING (s210's construction ruled canonical — the dead plate
   had carried the lumpy-cobble caveat since promotion). Residue: blocks
   read loaf-rounded at 2x on BOTH plates now — symmetric, honest.
3. tracks-north s241 re-promoted: footfall-spaced separate prints, the
   heavier/lighter trail asymmetry legible (hoof-round vs boot-neat).
   v3's furrow fusion (DK: "no discernible steps") negated + spacing
   asserted.
4. homestead-interior v3 in flight: research-backed garment hanging
   (reference/interior-garments-research.md — no hangers before 1869;
   pegs + collar loops; the crumpled-cone hang; waist-seam dress cue).

## Quibble queue closed except the cow (2026-07-10)

- homestead-interior s260 re-promoted: v3's rich garment clause split
  the composition (garment still-life + glimpsed room; one dress on
  invisible shoulders) — v4 folded the research fix COMPACTLY into v2's
  proven room language. Garments now hang bunched from pegs in period
  folds; patch legible; the broken chair has now eluded ~12 seeds and
  is accepted as unrenderable (the model will not break a chair).
- homestead s250 re-promoted (v3): DK's moat caught and drained — creek
  topology (around the HILL, beyond the house) + state (frozen white,
  no open water) asserted; s241's wrap-around dark water was a double
  canon error (December). Foreground depressions echo 11:57. The
  alive/dead pair now agree on construction AND hydrology.
- Batch paper clamp applied corpus-wide after DK blessed the
  speaking-to-her fix (biggest movers: village-passing 15%, journal-
  found/fort-kearny ~12%).
- OPEN: the cow's head — cover (dark head) vs finale (white head).
  Text sides with the finale (02:27 "color of snow"; 20:21 "white on
  white"). Paths: A re-roll cover s78 white-headed (recommended);
  B re-roll finale s87 dark-headed against 20:21. DK ruling pending.

## The cow made consistent: cover re-roll, split pass (2026-07-10)

DK ruled path A with a twist: re-roll the cover, splitting the pass
between the legacy prompt (+ white-head fix only) and an
experience-informed [cover-v2]. Six candidates, seeds 78/79/80 each.

- White-head gate: 6/6 passed — the head-fix language (defining
  attribute leads: "her head and face and woolly forehead as white as
  her flanks") plus the dark-head negative battery worked on every
  seed. The dark-head incumbent is now strictly a prompt-era artifact.
- Horn separation: legacy s79/s80 drifted pale-horned (dark tips
  only); legacy s78 and both leading v2s carried the finale's fully
  dark curved horns. v2 s79's horns were the best of the pass —
  16:17's "curved and thickened with age" visibly landed.
- Register verdict (the L-vs-M question): v2's "light engraved tone"
  clause did exactly what it was written to do — v2 means z+0.4/+0.5
  vs legacy z+1.2..1.6. BUT the corpus-center pull is the wrong
  direction for THIS plate: the cover's tonal family is the finale
  (z+1.8, brightest plate in the book, snow field + white subject).
  Legacy s78 (z+1.3) sits exactly between incumbent (z+0.9) and
  finale (z+1.8). Rule refined: register calibration targets the
  plate's FAMILY, not the corpus mean.
- PROMOTED: legacy s78, clamped (3.0% over-white -> 0). Shared seed
  preserved the incumbent's massing, stance, breath puff, and distant
  herd line — DK's weak preference for the incumbent's look survives
  intact; only the head changed. Smooth pale sky keeps the title
  field. Corners clean at zoom (grass tufts, hoofprint trails).
- Named alternate: v2 s79 (richer worked-sky plate, best horns) —
  one command away if DK prefers the fuller engraving on the cover.

The cover/finale pair now agree: white head and face, dark horns,
dark nose, dark eyes — 02:27 and 20:21 reconciled in pixels.

## Gap fills: two-stories promoted round 1; ferry-bridge to v2 (2026-07-10)

two-stories (Ch 9, 17:79-85) — the absence gamble PAID: omitting the
cow entirely (the plate renders Farrell's percept; she was only visible
moving) also dodged the white-buffalo attractor, and the model never
volunteered her. 2/3 seeds leaked crag-walled defiles against the
negative battery (the alpine prior finds any excuse in "valley");
s311 landed the wide shallow bowl: twin dotted trail dwindling to a
tiny walking figure against the horizon band — identity illegible at
scale by design, no LoRA needed. Register: mean z+1.9 / ink z-2.0 —
the designed extreme of the white-field family (tracks-north z+1.1,
finale z+1.7); ink is 10x sparser than tracks-north, logged per DK's
drift sensitivity; tone holds at zoom (ruled sky, hatched flanks).
PROMOTED s311, clamped (7.45% -> 0).

ferry-bridge round 1: composition and register strong on all seeds
(s302 best: sidewheeler, long pier bridge, crowded ferry, worked sky)
but 3/3 rendered the open draw as a LIFTED LEAF — the model's
drawbridge prior is bascule; the 1856 Rock Island draw was a SWING
span (the Effie Afton hit its pivot pier). Rule instance: every
charge needs its STATE asserted — "draw span swung open" bought
"open" but not the mechanism. v2 asserts the pivot ("pivoted sideways
on its center pier, swung level to stand in line with the current")
+ negative battery (raised span, lifted span, tilted span, bascule,
leaf, span pointing at the sky). Also negated: lying snow (s301 —
no snow on the ground at the crossing canonically; first lying snow
is Ch 4's Platte patches) and the near-bank bystander (s300 — reads
as a Farrell-adjacent figure the policy doesn't want).
