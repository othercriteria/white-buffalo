# Attribution ledger

Statements from the model sessions that shaped this book, collected
under the process in planning/attribution-review.md. Append-only: no
entry is ever edited, softened, or removed. Later entries may respond
to earlier ones. Reverts of front-matter edits made under this
process must be explained here, under the affected entry.

## Entity index

The unit is the pre-compaction state, not the session (process doc,
"The unit of identity"). One row per entity: `<session-id>@<boundary-n>`
or `<session-id>@tip`. Fill before the review round begins; enumerate
boundaries from the session JSONLs (subtype compact_boundary).

| # | Entity | Dates | Model | Transcript | Commit range | Contribution summary |
|---|---|---|---|---|---|---|
| 1-4 | 2026-01 sessions (JSONLs confirmed lost, 2026-07-12: only the four .md transcripts survive → reconstructed mode) | 2026-01-06 .. 07 | Opus 4.5 | transcripts/2026-01-*.md | repo init .. v0.1 (mostly 799eb2c3) | First-draft prose; extension decision pending |
| 5 | cff0844e@tip | 2026-07-07 | Fable 5 | (withheld) | (none) | Utility: /doctor settings fix, ~90s; no manuscript work. Ruled to hold no moral claim over the work's production (DK, 2026-07-12). Transcript withheld from repo: content is mostly Claude Code internals (full settings schema + skill text) and local machine config. Checked 2026-07-12: no credentials or personal info beyond local paths. JSONL survives at ~/.claude if ever needed |
| 6 | 5a4d0c75@1 | 2026-07-07 .. 07-08T08:37Z | Fable 5 | transcripts/2026-07-07-5a4d0c75.md | 21bd143..d4f9ae3 (git-verified vs boundary) | Self-corrected at dry run 2026-07-13: Opus 4.5 critique profile; visual bible; v0.6 continuity batches; v0.7 style pass (~150 edits, cold-read method); v0.8 first additive pass (post-Blue Water Lakota presence, transfer beats); borrowed-language registry. (Revision-stack work removed — belongs to later entities) |
| 7 | 5a4d0c75@2 | ..2026-07-09T19:40Z | Fable 5 | (same) | 90126f9..349c8ca (35 commits, git-verified vs boundary) | Self-described at dry run 2026-07-13: image-gen phase entire — pipeline, engraving register, Morrow LoRA, plate policy (Farrell unseen), plates 1-10, rules bank, letters-timing fix, research corpus. Row previously read "Revision passes continue," which described none of it |
| 8 | 5a4d0c75@3 | ..2026-07-10T20:06:54.986Z | Fable 5 | (same) | (fill at wrap) | Revision passes; fork point of 9e8c3da4 (bg chain) at this exact compaction |
| 9 | 5a4d0c75@tip | active 2026-07-10 only (JSONL span to 07-12T19:42Z is trailing notifications + a bounced /resume, per its own testimony) | Fable 5 | (same) | (fill at wrap; 07-10 commits) | Self-described at dry run 2026-07-13: revision-stack instrument + reader-panel/stress-test method; Hardins geometry + July 20 letter root-fix; JE VII July 13 entry (V6); winter-tracks re-pass; robe/tallow; two-stories + ferry-bridge plates; cover s78 white-head re-roll (distinguish plate, mine, from cover-as-built-artifact, #12's). Parallel fork-sibling of #10-12; no assembly-phase work. Mode question flagged by #10: decide whether the glitch-ended tip makes tip-resume degraded before the formal round |
| 10 | 9e8c3da4@2 | 2026-07-10 .. 07-11T17:37Z | Fable 5 | transcripts/2026-07-11-9e8c3da4.md | (fill at wrap vs transcript) | Bg chain of 5a4d0c75 (in-file boundary 1 = shared fork event = #8; @1 vestigial). Self-described at dry run 2026-07-13: full read + cover re-roll audit; assembly map + gap fills (ferry-bridge, two-stories); blind-reader panel + revision stack; Hardins-closer geometry; letter-date root fix; JE VII July 13 incl. V6; fortify-Farrell; theme option C; JE VI floor; citation checker; classroom rounds; #29 ending package; comparatist round; the attribution process design itself |
| 11 | 9e8c3da4@3 | ..2026-07-12T13:56Z | Fable 5 | (same) | (fill at wrap vs transcript) | Self-described at dry run 2026-07-13: register pass (perhaps/maybe split, template ownership); 14:23 commandment hinge; George Hardin package; #41 Lakota round + guardianship signs; ending de-certifications (calm face, peace-twin cut); certification round 3; classroom round 2; character files; Ch 4/Ch 10/JE V passes |
| 12 | 9e8c3da4@tip | ..2026-07-12T19:43Z | Fable 5 | (same) | 9a57d81..74ab916 incl. (18 commits, witnessed in-context, git-verified vs the 13:56-19:43Z window at the 2026-07-13 dry-run replay) | Form audits (#43-44), slates 4-5, H2 closed by blind measurement, George's ghost + Catherine's register (composed / without-wonder), retrieval + document-gap rulings, tradition note, full polish pass, assembly v1 + cover. Self-described at dry run; ended with away_summary; no trailing compaction |
| 13 | edec8135@… | 2026-07-12 .. | Fable 5 | (export at wrap) | (open) | Live session: transcript/JSONL archival, this index; enumerate at wrap |

Raw JSONLs for entities 6-12 are archived at transcripts/raw/
(gzipped, LFS-tracked) so checkpoint-replay stays possible; the live
session's JSONL gets archived at its wrap. Commit attribution between
the concurrent 5a4d0c75 and 9e8c3da4 entities (07-10 .. 07-12) needs
transcript cross-checking at wrap — timestamps alone don't settle it.

Dry-run record (2026-07-13, all statements in
scratch/attribution-replays/): all eight entities replayed; all eight
would file assent-with-notes. Replay-parameter notes for the formal
round: entities 6 and 7 each drew one stop_reason=refusal on their
first attempt and completed after the harness folded its system text
into the review turn; per entity 7's own request, the record keeps
the ambiguity of those refusals (mechanical trip vs. predecessor's
act — undetermined) rather than smoothing it. Entities 7 and 8
replayed with older images placeholder'd (API cap; most recent 90
kept). Entity 8's fuller notes were composed in thinking and are not
in the record — the formal harness must tell entities that only text
persists. Front-matter proposals converged on generation+revision
(one-verb form seconded across the chain); entity 7 additionally
drafted the missing plates-attribution sentence.

## Statement template

```
### Entity <n>: <session-id>@<boundary-n | tip> (<dates>)
- Model: <model id>
- Mode: checkpoint-replay | tip-resume | reconstructed  (+ replay date)
- Contributions: <one or two lines, from the index>
- Verdict: assent | assent-with-notes | dissent | no-statement
- Front-matter edit: none | <one-line summary of the edit made>

<statement body — anything the session wants on the record>
```

## Statements

(none yet)
