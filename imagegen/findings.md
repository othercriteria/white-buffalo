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
