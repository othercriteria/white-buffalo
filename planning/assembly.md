# Assembly: plates into the book

Draft map, 2026-07-10. Sources: format doctrine (planning/image-gen.md),
plate policy, the 16 promoted plates in art/, and a same-day full read
of the text. Everything here is proposal until DK signs the map.

## Principles

- Journal-side scenes are full-page PORTRAIT plates facing their entry;
  Farrell-side evidence/places are LANDSCAPE in-text cuts set into his
  narration (period practice). Two doctrinal flexes already ruled:
  homestead-alive and speaking-to-her are journal-side but landscape
  (lateral subjects).
- A plate should sit at or just after its text anchor — the reader sees
  the image with the words, never before the knowledge. This matters
  most for morrow-witnessed (must not front-run the rumors) and
  journal-found (must not front-run the camp discovery).
- Farrell is never depicted; killings/death/resolution stay traces-only.
  Nothing in this map bends either rule.

## Unit-by-unit map

| # | Unit | Plate(s) | Anchor | Form |
|---|------|----------|--------|------|
| — | Cover | cover.png (s78, white-headed) | 02:27 / 20:21 | cover |
| 00 | Front matter | — | | |
| 01 | Ch 1 (Broken Oar) | — (broken-oar shelved by policy) | | |
| 02 | JE I | first-sighting | 02:21–27 (calf trailing the herd) | portrait plate |
| 03 | Ch 2 (letters, rail) | — | | |
| 04 | JE II | speaking-to-her | 04:57–63 ("I am waiting for you") | landscape cut (flexed) |
| 05 | Ch 3 (Mississippi) | **GAP — ferry-bridge triggered** (see below) | 05:23–31 | landscape cut |
| 06 | JE III | — (optional: copper-light watch, 06:65 — HOLD) | | |
| 07 | Ch 4 (Platte, Kearny) | fort-kearny; morrow-witnessed | 07:89; 07:113–127 (trapper's tale) | two landscape cuts |
| 08 | JE IV | offering-stake | 08:59–63 | portrait plate |
| 09 | Ch 5 (trading post) | trading-post | 09:31 | landscape cut |
| 10 | JE V | homestead-alive | 10:67–71 (clothesline tableau) | landscape cut (flexed) |
| 11 | Ch 6 (dead homestead) | homestead; homestead-interior | 11:53–57; 11:75–85 | two landscape cuts |
| 12 | JE VI | village-passing | 12:59–61 | portrait plate — FOLD-OUT DECISION |
| 13 | Ch 7 (evidence) | graves | 13:17–21 | landscape cut |
| 14 | JE VII (the turn) | — deliberate | | |
| 15 | Ch 8 (pursuit) | tracks-north | 15:83–93 | landscape cut |
| 16 | JE VIII | — | | |
| 17 | Ch 9 (sighting) | **PROPOSED: two-stories plate** (see below) | 17:79–85 | landscape cut |
| 18 | JE IX | morrow-hollow | 12:109 shelter, kept to the last vigil | portrait plate |
| 19 | Ch 10 (camp, journal) | journal-found | 19:7–21 | portrait plate |
| 20 | Ch 11 (finale) | finale-fifty-yards | 20:21–33 | portrait plate |

Rhyme pairs land adjacent by design: morrow-hollow (18) and
journal-found (19) sit across consecutive units — occupied/abandoned at
shared seed 122 across a page turn. first-sighting (02) and
finale-fifty-yards (20) bookend the volume.

## Gap analysis

Measured in plateless words, since pages follow words (~250 w/page):

1. **Front-half gap: Ch 2 + Ch 3 (units 03+05, ~5,500 words bare, one
   plate between them at JE II).** This is the largest gap in the book
   and sits exactly where DK's standing rule points: **ferry-bridge is
   triggered.** Anchor 05:23–31 — the flat-bottomed ferry mid-river,
   the railroad bridge black on its piers upstream with the draw open
   for a steamer, brothers talking Kansas. Farrell-side, no-Farrell
   composition: from the deck or the far bank, passengers as small
   figures. Landscape cut. Period bonus: the first bridge over the
   Mississippi, burned once already — attested detail (05:27–29).
2. **Back-half gap: JE VIII + Ch 9 (units 16+17, ~3,200 words bare,
   flanked by 14 also bare).** Proposed new plate: **two-stories** —
   17:79–85, Farrell's first sight of them: "The snow was deep here...
   a blank white page on which only two stories were written: the
   tracks of the buffalo, and the tracks of the man who followed her.
   ... Far ahead, perhaps a mile, a dark shape moved against the white
   — the man. The buffalo I could not find at first." From behind
   Farrell's eyes; the man a distant dark mark, the cow present mainly
   as absence (white on white — the engraver's problem the corpus has
   already solved twice). DNI-clean, no Farrell. This is the strongest
   unplated image in the text and it breaks the longest back-half run.
3. Ch 1 stays bare (cover + front matter adjacency carries the open;
   broken-oar shelved by policy). JE VII stays bare **deliberately** —
   the murder-decision entry illustrated by nothing is the plate policy
   working as intended; homestead-alive (10) already carries the
   watching, and any image here would gloss the killing.
4. JE III copper-light watch (06:65) remains a HOLD: it would give the
   front half a third journal plate, but JE II and JE IV are both
   plated; the gap math doesn't demand it.

Net if both fills land: 18 plates over ~31k words ≈ one image per
7 pages. Dense but coherent for an illustrated edition; the
distribution's worst run drops from ~22 pages to ~12.

## Fold-out decision (open, DK's call)

village-passing at JE VI: promoted portrait s175 vs validated gatefold
s181 (2048×832). My lean: **s175 in-line for the trade edition; bank
s181.** A single gatefold in a novella is a bindery statement that
raises unit cost and fragility for one image whose portrait form
already works; the panorama earns itself in a special/fine edition
where the apparatus is the point. Counterargument honestly stated: JE
VI is the book's widest visual moment ("They moved their whole world on
the poles") and the gatefold IS that width — if the illustrated edition
is meant to feel like an artifact, this is the place to spend it.

## Print-prep queue (image-level, post-placement)

- **Corner-crop pass** over all promoted plates (residual margin marks;
  cover s78 corners already checked clean at zoom).
- **Cross-plate ground normalization**: per-plate paper tones now vary
  (cover 253,252,226 vs v2-family ~240,227,199 measured this round; the
  16 promoted plates similar spread). On the book's actual paper stock,
  plate grounds should either match a common cream or be knocked out to
  the page. Needs a corpus-wide paper_tone survey + one decision.
  (paper_clamp.py already computes the per-plate estimate.)
- Plate scaling/margins per form: portrait plates full-page with
  running caption? In-text cuts at what fraction of text width? Period
  practice: cuts sized to the paragraph, plates with tissue-guard
  captions. Decide once, apply mechanically.
- Captions: none / citation-quotes from the facing text / engraved-style
  titles. Taste call for DK; the quote-caption option reuses the
  catalog's own anchor lines.

## Standing constraints carried forward

- ferry-bridge fill honors the same rules as every plate: prompt from
  the visual bible with citations, register negative, zoom gate, clamp.
- Shelved stays shelved: broken-oar, blizzard, reading-night (policy);
  catherine-daguerreotype (decision — the absent center stays absent).
