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
| 1-4 | 2026-01 sessions (entity enumeration pending JSONL survival check) | 2026-01-06 .. 07 | Opus 4.5 | transcripts/2026-01-*.md | (fill) | First-draft prose; extension decision pending |
| 5+ | 5a4d0c75@1..3, 5a4d0c75@tip, 9e8c3da4@1.., ... (fill at wrap) | 2026-07-.. | Fable 5 | (update transcripts/) | (fill) | (fill) |

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
