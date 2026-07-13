# Assembly: plates into the book

Draft map, 2026-07-10. Sources: format doctrine (planning/image-gen.md),
plate policy, the 16 promoted plates in art/, and a same-day full read
of the text. Everything here is proposal until DK signs the map.

## v1 BUILD — LIVE (2026-07-12, DK-directed)

`make book` → build/white-buffalo.{pdf,epub} via assemble.py. The
unit map below is implemented as of v1: all 17 plates injected at
their text anchors, matched by verbatim snippet (content-addressed —
a drifted anchor fails the build loudly rather than front-running
the knowledge). PDF: 5.5×8.5in, TeX Gyre Pagella 11pt, chapters
unnumbered, figures pinned [H] (no float drift); 131 pp. EPUB:
cover.png as cover, TOC depth 1. Front matter: LaTeX title page
from metadata (title, "A novella" subtitle, authors, year); 00
contributes the notices only (tradition note, AI note), unnumbered
on the title verso. QA rendering: poppler-utils in the flake
(pdftoppm thumbnails).

Production pass (2026-07-12 evening, from the four-instrument PDF
round): folio 1 = Chapter One forced recto (odd folios recto
book-wide — parity was inverted at v1); mirrored margins with
binding gutter (0.85in inner / 0.65in outer, measure unchanged);
\raggedbottom (kills the five flush-bottom blowout pages);
first-line indents, no inter-paragraph space; \frenchspacing;
widow/club/broken penalties; notices URL on its own line (was
clipped off-trim at v1); portrait plates 72%→85% width; spaced em
dashes closed (front matter + one JE VII instance); template
\frontmatter/\mainmatter neutralized (numbering driven explicitly).

A2 pass (2026-07-13, from round 2): front matter re-plumbed — half
title p.1, cover plate as frontispiece facing the title p.2,
notices spread pp.4-5, LIST OF ILLUSTRATIONS on its own recto
(titles only, from PLATE_TITLES in assemble.py; plates stay
uncaptioned, so the caption doctrine holds; folios measured by a
two-pass build). JE dated subheads keep-with-next (\JEdate);
scene rules bound to following text (\scenebreak); no hyphenated
stub final lines; proper-name hyphenation exceptions;
\emergencystretch; book closes on a verso, even page count.
openany KEPT as a decision (recto-only openings would scatter
blank versos through a plated novella). PDF and EPUB now build
from separate variants (raw TeX transforms are PDF-only). Front
matter content (B): "generated and revised the prose" (the
chain-converged one-verb amendment) + the plates-attribution
paragraph (image-model-drawn, partiality-as-limit). Rights
line/ISBN/imprint still deliberately absent — await real
publication facts and the license decision (DK's).

Deliberately UNRESOLVED (open items): fold-out (village-passing
runs the promoted portrait in-line), captions (none), corner-crop
pass, cross-plate ground normalization, mobi (needs calibre; EPUB
suffices for now). Added by the production round, still open:
©/rights line (interacts with the attribution process — DK's
call), plate grayscale-vs-cream-ground for print stock, TOC/list
of plates (list blocked on caption doctrine; TOC placement fights
notices-on-title-verso in the pandoc template), Note on the plates
disclosing their synthesis (track B, content), running heads
(taste), cover plate re-cut + typography (track C).
PURPOSE: one artifact for future agent review rounds — no file
lists, no structure spoilers from filenames. NOTE for instrument
prompts: point agents at build/white-buffalo.pdf (regenerate with
`make book` first; build/ is gitignored).

## Principles

- Journal-side scenes are full-page PORTRAIT plates facing their entry;
  Farrell-side evidence/places are LANDSCAPE in-text cuts set into his
  narration (period practice). Two doctrinal flexes already ruled:
  homestead-alive and speaking-to-her are landscape (lateral subjects).
- A plate should sit at or just after its text anchor — the reader sees
  the image with the words, never before the knowledge, AND NEVER
  MERELY EQUAL TO IT (corollary, art-critic consultation 2026-07-13,
  DK-ratified): a plate earns adjacency by exceeding its sentence —
  detail to verify (the evidence class: graves) or difficulty to
  perform (the discovery class: frozen-man). Test for every future
  plate: after the anchor sentence is read, does the image still have
  a job? If the sentence exhausts the image, the placement (or the
  plate) is wrong. Said-then-shown deflates; said-then-sought and
  said-then-verified serve.
- Farrell is never depicted; killings/death/resolution stay traces-only.
- CAPTIONS: none, ever (CLOSED 2026-07-13, DK sign-off; both
  consultants, independently, high confidence). Uncaptioned in-text
  cuts + the titled List of Illustrations is the complete period
  arrangement (Kent's Moby-Dick; Tenniel's cuts). A caption under the
  frozen-man names what the image hides; the List does its naming at
  a distance where it cannot intervene in the act of reading.
- PLATE/TEXT BOUNDARY: whitespace only — no rules, no frames, and the
  journal-vignette/chapter-ruled split is DECLINED permanently (both
  consultants: orientation+scale already encode the narrator split; a
  second axis is apparatus to decode). \intextsep codified at 18pt.
  The half-page [b]-float grammar proposal: retired unimplemented.
- GROUNDS: knocked out to page white AT ASSEMBLY (build/plates/, via
  imagegen/knockout.py paper-tone division; DK 2026-07-13: cream in
  art/ is the record and the model's working register; cream in the
  assembled book is artifice — "Mexico as sepia filter." art/ is never
  modified). Road not taken, recorded: production consultant argued
  one uniform cream ("plates laid into the record"). Register bonus:
  plate snow and page paper are now the same white — the
  whiteness-as-paper metaphor is literal at assembly level.

## Unit-by-unit map

| # | Unit | Plate(s) | Anchor | Form |
|---|------|----------|--------|------|
| — | Cover | cover.png (s78, white-headed) | 02:27 / 20:21 | cover |
| 00 | Front matter | — | | |
| 01 | Ch 1 (Broken Oar) | — (broken-oar shelved by policy) | | |
| 02 | JE I | first-sighting | 02:24-30 (calf trailing the herd) | portrait plate |
| 03 | Ch 2 (letters, rail) | — | | |
| 04 | JE II | speaking-to-her | 04:57–63 ("I am waiting for you") | landscape cut (flexed) |
| 05 | Ch 3 (Mississippi) | ferry-bridge (PROMOTED s307, 2026-07-10) | 05:23–31 | landscape cut |
| 06 | JE III | — (optional: copper-light watch, 06:65 — HOLD) | | |
| 07 | Ch 4 (Platte, Kearny) | fort-kearny; morrow-witnessed | 07:89; 07:113–129 (trapper's tale) | two landscape cuts |
| 08 | JE IV | offering-stake | 08:59–63 | portrait plate |
| 09 | Ch 5 (trading post) | trading-post | 09:31 | landscape cut |
| 10 | JE V | homestead-alive | 10:67–71 (clothesline tableau) | landscape cut (flexed) |
| 11 | Ch 6 (dead homestead) | homestead; homestead-interior | 11:51–55; 11:73–83 | two landscape cuts |
| 12 | JE VI | village-passing | 12:45 | portrait plate — FOLD-OUT DECISION |
| 13 | Ch 7 (evidence) | graves | 13:17–21 | landscape cut |
| 14 | JE VII (the turn) | — deliberate | | |
| 15 | Ch 8 (pursuit) | tracks-north | 15:77–87 | landscape cut |
| 16 | JE VIII | — | | |
| 17 | Ch 9 (sighting) | two-stories (PROMOTED s311, 2026-07-10) | 17:75–81 | landscape cut |
| 18 | JE IX | morrow-hollow | 12:93 shelter, kept to the last vigil | portrait plate |
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
   17:77–83, Farrell's first sight of them: "The snow was deep here...
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
