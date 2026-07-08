# Public-domain engraving sources (recon 2026-07-08)

Shallow acquisition survey for the two recurring-consistency LoRA
candidates (DK: homestead, white buffalo). Full agent report in session
transcript; essentials below. Everything pre-1930 US publication = PD;
no repository obstacles found (LOC "no known restrictions", IA, BHL,
Commons, NYPL PD-flagged with hi-res TIFFs).

## Bison — RICH (the easy half)

- **Hornaday, *The Extermination of the American Bison* (1889)**, ~22
  plates including CALF, YEARLING, COW, BULL, winter scenes:
  archive.org/details/exterminationofa00horn (also BHL bibliography
  78803). The life-stage coverage directly addresses the age-progression
  problem: one LoRA with age-token captions ("calf"/"cow") rather than
  an age-locked model.
- Audubon & Bachman, *Viviparous Quadrupeds*, Plate LVI (bull) + LVII
  (cow AND calf), 29 IA copies.
- Catlin 1844 portfolio (~6-8 buffalo subjects incl. winter/snowshoe
  hunts); Bodmer *Herd of Bisons on the Upper Missouri* (LOC PGA);
  Currier & Ives hunt lithos; Commons Category:Bison in art.
- Volume: 100-300 distinct usable prints. Deeper pass: ~4-6 h scripted
  (IA bulk + LOC TIFF endpoints + Commons dumps) → **150-250 clean
  ≥1024px training images with life-stage coverage.**

## Sod houses / dugouts — SCARCE in engravings (the hard half)

- Period *engravings* of soddies barely exist as a genre; the visual
  record is photographic (Solomon Butcher's ~1,000+ Nebraska homestead
  photos, 1886-1900s).
- Best engraving veins: Richardson, *Beyond the Mississippi* (1867),
  200+ wood engravings of frontier dwellings
  (archive.org/details/cu31924030995942); Harper's/Leslie's weeklies
  (page-level mining); Andreas county atlases (1870s-80s KS/NE).
- Volume: 20-60 genuine engravings after 4-8 h of eyeball mining.
- **The tradeoff to decide before a deep pass:** admitting Butcher
  photographs (re-rendered into the register, or as secondary
  conditioning) lifts yield to 500+ for ~2 h more — at the cost of a
  photographic substrate under an engraving-style target.

## Level of effort (deep pass, both subjects): ~6-12 h total,
asymmetric — bison cheap and abundant, sod houses expensive and thin.

## Implications

- White-buffalo LoRA: viable and well-fed; Hornaday's life-stage plates
  suggest age-conditioned captions in a single LoRA (solves DK's
  "without locking in a particular age").
- Homestead LoRA: self-distillation (our own curated generations) is
  probably the better primary source given engraving scarcity, with the
  20-60 mined plates as seasoning; or accept the Butcher-rerender
  tradeoff. Decide only when the homestead plate family actually forces
  the need.
