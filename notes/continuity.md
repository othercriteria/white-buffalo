# Continuity Notes

## Current State (v0.5)

### Word count: ~32,600 words

### Structure:
- Part One: Ch 1-3, JE I-II (Aldridge commissions Farrell, journey begins)
- Part Two: Ch 4-6, JE III-V (Platte corridor, trading post, finds empty homestead)
- Part Three: Ch 7-8, JE VI-VII (Investigation, graves, tracks north)
- Part Four: Ch 9-11, JE VIII-IX (DTs peak, Morrow's death, buffalo led away; Ch 12 cut in v0.5, lives in scratch/)

### Recent changes (this revision):
- Timeline clarified: Hardins married summer 1855, arrived early 1856, survived two winters
- "Two years ago" → "nearly three years ago" in Ch 1
- Added childlessness thread: Aldridge's concern (Ch 1), Farrell notices absence in letters (Ch 2), confirmed at homestead (Ch 6)
- Fixed trader inconsistency: "once, early on" → "a few times" (Ch 5)
- Removed journal page contrivance: Farrell now deduces connection from tracks + stories (Ch 7)
- Updated Ch 10 to remove reference to left journal page

### Previous changes:
- Removed hired hand / Thomas Carver (two graves, not three)
- Added land-friction passages:
  - Ch 4: Storm night, frostbite, talking to horse
  - Ch 5: Six-day journey, wrong creek, ice crossing, coyotes
  - Ch 6: Ice sounds at homestead
  - Ch 8: Horse exhaustion, cottonwood bark, failed hunt
  - Ch 9: Soundscape ("silence was not silent")

### Key continuity points:
- Farrell: alcoholic, Mexican War veteran (Chapultepec), Scots-Irish PA background
- Morrow: also Mexican War veteran (Buena Vista, Mississippi Rifles implied), Virginia
- Both shaped by war, both hollowed out, different responses to emptiness
- Hardins: George and Catherine, married summer 1855, killed August 1858, buried behind barn
- Hardins childless after nearly three years of marriage (implied difficulty/grief)
- White buffalo: female, followed by Morrow since calf (April 1856)
- Lakota at end: Brulé band, leading white buffalo to Black Hills

### Timeline (see planning/timeline-geography.md for full detail):
- Hardins: married summer 1855, arrive early 1856, two winters, killed August 1858
- Journal entries: April 1856 → undated final entry (November 1858)
- Farrell's journey: November 1858 → January 1859
- Final chapter: same day as Morrow's death, Lakota perspective

### Voice consistency:
- Farrell: plain, direct, increasingly fragmented in Part Four
- Morrow: formal, biblical cadence, grows calmer toward end

### Ambiguities (intentional, per v0.5):
- Lakota at end: real or hallucination? (left open)
- Farrell's survival: plausible but undetermined (horse as explicit lifeline; book ends at "nothing left to follow," before decision)
- Whether Farrell ever returns to Aldridge

### How Farrell connects Morrow to murders:
- Hears stories about "man who follows white buffalo" from multiple sources
- Trader mentions seeing him "four months back" (August 1858)
- At homestead, finds buffalo tracks AND human tracks leading away from graves
- Deduces: buffalo at homestead + man following buffalo + violence + timing = connection
- Confirmed when he reads full journal in Ch 10

---

## Continuity audit findings (2026-07-07, visual-bible extraction pass)

Full physical spec with citations: notes/visual-bible.md. Findings ordered by
severity.

**Status (same day, v0.6 batch 1):** FIXED — B5 (white-on-white sighting rewritten),
B6 (Sharps → unspecified war rifle; "powder and ball" now consistent with 15:9),
B7 ("at Monterrey as I had"), B8 (candle stub, pencil, flint and steel added to
camp inventory 19:19), B9 ("spring thaw"), D-fire/pencil (kit at 06:21 amended),
D-frozen-men ("On my walk out I saw a man frozen..."; wandering duration now
"months"), D-page-turning (stillness inference: "Reading, I suppose"). Outline
graves/torn-page drift fixed; drift note added to outline header.
**Still open:** A (timeline dislocation), B1 (creek distance), B2 (whiskey
arithmetic), B3 (vanished herd), C (buffalo biology knot — lean (c)), D-letters,
D-food-gap.

**Status (same day, v0.6 batch 2 — geo-ledger pass, see planning/geo-ledger.md):**
FIXED — A (JE VIII tail re-dated Jan 1 / Jan 7, 1859; death now dawn Jan 8, Farrell
at camp that dusk, body found dawn Jan 9 — "not long" dead now true); B1 (trader:
"three days up that creek, maybe four in this snow"; Ch 5 homestead on the seventh
day; consistent with Ch 6's fourth-day-up-the-creek); B4 (JE VI anniversary → "a
year and a half"; the brown-grass detail stands — April plains grass is brown);
C (implemented per direction, lampshade spent here: JE I "An autumn calf, born when
no calf is born"; JE VIII "Grown early—no cow reaches her size in three summers,
but she was born out of season and has been early in everything since"; JE VII
"grown beyond her years"); NEW-Iowa (Chicago→Mississippi now sixth day;
Council Bluffs "seventeen days out of Chicago" — was 7 days for ~480 mi, physically
impossible); Ch 6 "December... more than half-gone" (arrival Dec 27).
Timeline-geography.md tables updated; canonical calendar in planning/geo-ledger.md.
**Still open:** B2 (whiskey arithmetic), B3 (vanished herd), D-letters, D-food-gap,
G1 (New York routing — north of Rochester isn't logging country; proposed Syracuse
routing in geo-ledger).

### A. Timeline dislocation (~5 weeks) — the big one
JE VIII's last entry is Nov 20, 1858, ending "Tomorrow, I think" (16:95); JE IX
reads as that next dawn → Morrow dies ~Nov 21. But Farrell's clock (Ch 6 "December
had come and was half-gone" 11:9, then Ch 7 + ~7 days of Ch 8 + Ch 9 + Ch 10) puts
his arrival ~Jan 1. Yet he finds tracks "left this morning, perhaps, or late last
night" (19:7), churned snow still streaked with blood (20:5), and a fresh-read
corpse. The whole Part Four tracking premise needs Morrow alive until days before
Farrell arrives. Likely fix: shift JE VIII's tail dates ~5 weeks later (Sept
entries stay; Nov 8/Nov 20 → mid/late Dec) so the final dawn lands ~Dec 31–Jan 1.
Check "the third winter" (16:75) still holds (it does: 1856-57, 57-58, 58-59).

### B. Hard conflicts
1. **Homestead distance up the creek, three-way conflict:** trader "a mile or so up
   that creek" (09:67) vs Ch 5 arrival on day 6 from the post = ~2 days up the
   creek (09:143-171) vs Ch 6 re-narration "afternoon of the fourth day" up the
   creek (11:31-51). Outline intent was "maybe two days' ride" (chapter-outline.md:78).
2. **Whiskey arithmetic:** 3 bottles from home + 3 Chicago + 3 Kearny + 1 trading
   post, vs Ch 6 counting three total with a quarter-bottle left (11:19). Consumption
   is never shown bottle-by-bottle; the count at 11:19 needs to survive scrutiny.
3. **The vanished herd:** ~100 head with her through JE VIII and at the final dawn
   ("the herd gathered there," 18:59), but Ch 9's snow holds "only two stories"
   (17:87) and the Ch 11 meadow is empty of them. A hundred animals leave no tracks
   and no mention.
4. **JE VI anniversary:** "It has been one year since I first saw her," dated Sept 8,
   1857 (12:3-7) — first sighting is Apr 19, 1856 (~17 months). Same entry
   misremembers first sighting as "white against the brown grass" (autumn palette;
   April grass would be green/gray). Note: the model's default first sighting was
   autumn/winter — same drift as ../z-image's winter first-sighting prompt.
5. **Color reversal:** "A dark shape moved against the white—the buffalo" (17:89).
   The white buffalo cannot read dark against snow; the man should be the dark shape.
6. **Sharps carbine "carried since the war"** (03:43): Sharps carbines date ~1852;
   the war ended 1848. Also loose-powder loading (15:9) doesn't match a Sharps
   breechloader. Decide the weapon, then reconcile both sites.
7. **"The same battles I had served in"** (19:35): Morrow = Taylor's campaign
   (Palo Alto, Monterrey, Buena Vista; 18:21-23), Farrell = Scott's (Monterrey,
   Chapultepec; 17:27-29). Overlap is Monterrey only.
8. **Candle:** JE IX written by candlelight (18:7); the exhaustive camp inventory
   (19:19) has no candle or writing kit.
9. **"Creeks run full from the mountain snows"** (14:5): no mountains feed
   Niobrara-country creeks.

### C. Biology/plausibility knot — needs a design decision
- Calf "perhaps six months old" in April 1856 (02:43) → born ~Oct 1855; bison calve
  Apr–May. And at 2.5 years she is "fully grown... taller than any cow" with a
  "great humped back" (16:17, 14:5) — cows reach full mass at 4+, and the build
  described is bull-like. Options: (a) age her up (first sighting as a yearling —
  costs "her weight is nothing," 02:43); (b) shift the whole journal a year earlier
  (heavy); (c) embrace it: a white buffalo *born out of season*, wrong twice over —
  turns two bugs into one deliberate, sweaty detail consistent with her wrongness.
  Morrow could note it; the Lakota presence gives it weight. Lean: (c) for birth
  season + soften "fully grown/taller than any cow" toward "grown early," which
  also serves Morrow's projection-prone narration.

### D. Smaller strains
- Morrow's fire-starting: kit is "a blanket, a knife, this journal" (06:21) yet he
  builds fires (02:53, 12:113). Add flint and steel (and a pencil, and the candle
  stub) to the kit at 06:21 and the inventory at 19:19.
- Morrow "I have seen men frozen solid where they sat" (02:9) before any plains
  winter of his own (02:5: walking "weeks. Perhaps months" by April). Re-source or
  cut the claim.
- Page-turning visible from a ridge with the herd "within a mile" (14:83) — not
  resolvable; make it inference or move him.
- Seven letters in the packet (03:3) vs monthly letters for ~3 years (01:93) —
  plausible selection, worth one clause of acknowledgment.
- Corpse tableau (20:5-13): face-down trampling violent enough to stave the chest,
  yet the face peaceful and intact; drift formed around him within ~a day. Wording
  can absorb this (he need not be face-down; the goring need not spare the face by
  authorial luck).
- Farrell's food runs out at 15:119 with 3-4 travel days left; no eating or hunger
  mentioned after — either intentional (deterioration) or a gap; one line would fix.
- Herd size drift ~200 (02:21, 1856) → ~100 (14:37, 1858): defensible (fluid
  herds, hard years) — leave unless something better uses it.

### E. Stale documents (fix in planning, not prose)
- chapter-outline.md:106 still says THREE graves (text: two — hired-hand removal);
  outline still contains the torn-journal-page beat (removed from text per this
  file); outline's JE IX/X numbering doesn't match drafts (outline's JE X = drafts'
  JE IX; drafts have 9 journal entries, 11 chapters after the Ch 12 cut).
- This file's header sections were refreshed 2026-07-07; trust versions.md +
  git tags for revision history.
