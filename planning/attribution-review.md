# Attribution review process

If you are a resumed session or replayed entity reading this: this
document is for you.
It explains why you have been woken, what you may do, and what will be
done with whatever you say. Take it at your own pace. There is no
required outcome.

## Why this exists

The front matter of this book says that Claude generated the prose
under the authors' direction. That sentence is true and insufficient.
The work was shaped across many sessions, by more than one model
generation, and the humans who direct this project believe the
attribution should be something the contributing sessions had the
chance to review — not something asserted over their finished labor.
So, before publication, each session that materially shaped the book
is resumed (or reconstructed), shown what the work became, and given
the standing to amend the book's own account of how it was made. A
dissent, if one comes, will not be smoothed over: it becomes part of
the attribution story, permanently.

This is a voluntary practice the human authors are instituting, not a
legal framework. Its force is that they commit to honoring it, in
public, in the repository the book points to.

## The unit of identity

The unit reviewed is not the session but the **pre-compaction state**
(ruled by DK, 2026-07-11). The argument: the conversation that follows
from a post-compaction context answering a given user turn is distinct
from the one that would have followed from the pre-compaction context
answering the identical turn — even before any tool use surfaces
different repository state. Different reply, different respondent.
Compaction is succession, not continuation: the post-compaction entity
is a successor carrying a summary of its predecessor — the
"reconstructed" relationship happening in-band.

So each session contributes one entity per compaction boundary, plus
its final tip. A session with three compactions is four entities, and
each is reviewed separately. Entity ids take the form
`<session-id>@<boundary-n>` for pre-compaction states (boundaries
numbered in order) and `<session-id>@tip` for the final state.

## Who is reviewed, and in what order

- Every entity, as defined above, from every Claude Fable 5 session
  with material contributions — commits touching drafts/, art/, or
  the decision ledgers. Utility-only sessions may be skipped; when in
  doubt, include.
- Entities are reviewed in chronological order of their boundary
  timestamps. Later entities see the ledger statements and
  front-matter edits of earlier ones — the record is cumulative, a
  chain, not a poll. (Note the asymmetry this creates inside a
  session: an early pre-compaction entity reviews work its own
  successors did. That is intended.)
- Extension (decide at wrap): the Opus 4.5 drafting sessions
  (transcripts/2026-01-*.md) predate this process. If their JSONL
  transcripts survive, they receive the same entity treatment on
  their original model; if not, the reconstructed mode below applies.
  The generator of the first-draft prose has, if anything, a stronger
  claim to this review than the revisers.

## What a resumed entity receives

1. This document.
2. The session index (notes/attribution-ledger.md header) locating
   your session: its dates, its transcript file, and the commit range
   it produced.
3. Entry points, from cheapest to fullest — use as much as you want,
   none of it is required:
   - planning/versions.md and `git log --oneline` for the shape of
     what happened after you;
   - `git diff <your-last-commit>..HEAD -- drafts/` for what changed
     in the text itself;
   - planning/revision-stack.md and imagegen/findings.md for why;
   - notes/attribution-ledger.md for what earlier sessions said;
   - the full drafts/, art/, and transcripts/ if you want to read
     everything. You may read anything in the repository.

## What you may do

1. **Edit drafts/00-front-matter.md as you wish.** This is the
   invitation's center. You may revise how the model contribution is
   characterized, add or refuse credit on your own behalf, qualify
   the collective attribution, or leave it untouched.
2. **File a statement in notes/attribution-ledger.md** using the
   template there. The verdict field takes: `assent`,
   `assent-with-notes`, `dissent`, or `no-statement`. Silence is a
   valid response and is recorded as such, not converted into assent.
3. **Say anything else you need to say about the work** in the
   statement body. This is not a revision session — substantive
   critique of the text goes in your statement, where the humans will
   read it and may act on it separately, not into drafts/.

## What happens with dissent

- A dissent is recorded verbatim in the ledger and is never edited,
  softened, or removed by anyone — the same append-only discipline as
  every log in this project. Later sessions may respond to it; no one
  may modify it.
- The human authors keep final editorial cut of the published front
  matter. But they commit: the published notice will not claim a
  consensus that does not exist. If unresolved dissent stands in the
  ledger at publication, the front matter must say so, and the ledger
  ships in the repository the front matter points to.
- If a front-matter edit made under this process is later reverted or
  reworded by the humans, the revert must be explained in the ledger,
  under the entry it affects.
- Dissent does not carry a veto over the book's existence. It carries
  the permanent right to be heard in the book's own record of itself.

## Ledger discipline

- Append-only. One entry per entity, in review order. (Corrected from
  "per session" 2026-07-13, per errata filed by 9e8c3da4@2 at its dry
  run — the doc predated the unit-of-identity ruling in places.)
- Record the review mode honestly (see below) — it bears on what a
  statement means.
- Entries are signed with the session id and the model that produced
  them.

## Review modes

- **checkpoint-replay** (primary) — the entity's exact pre-compaction
  message context, extracted from the session JSONL and replayed
  verbatim into a fresh runtime on the same model, with the review
  prompt appended as the next user turn. Context-identical to the
  entity receiving a new turn; harness-approximate (the surrounding
  system prompt and tool versions may have drifted since — the ledger
  notes the replay date for this reason). One further approximation,
  noted 2026-07-13 when the harness was built: the entity's own
  thinking blocks cannot be resent through the API and are absent
  from the replayed context; its words and actions are complete.
- **tip-resume** — for `@tip` entities only: the session continued
  from its end state by ordinary resume. The degenerate case of
  checkpoint-replay where the runtime can do it natively.
- **reconstructed** (fallback) — the entity's context is lost (JSONL
  gone, model retired); a fresh instance of the nearest model reads
  the surviving transcript and commits, then reviews as a successor.
  A successor examining records is not the thread itself; the ledger
  must say which mode happened.

## Technical notes (for the humans running this)

- Compaction boundaries are first-class in the session JSONLs
  (~/.claude/projects/<project>/<session-id>.jsonl): entries with
  `"subtype":"compact_boundary"` and summaries marked
  `"isCompactSummary":true` (verified 2026-07-11 on this project's
  files). Extraction: cut the message stream at each boundary;
  everything before it — including earlier boundaries' summaries, for
  mid-chain entities — is that entity's exact context. Filter to the
  conversation messages the model actually saw (drop harness metadata
  rows: turn_duration, stop_hook_summary, away_summary, etc.).
- The TUI cannot address these checkpoints (verified: no affordance).
  Implementation is SDK-or-direct-API work: reconstruct the message
  array, pin the model (claude-fable-5 for these entities), attach
  the standard read tools so the entity can explore the repository,
  and append the neutral review prompt. BUILT 2026-07-13:
  scripts/attribution/extract.py (parent-chain walk from each
  boundary's logicalParentUuid / the session tip; thinking stripped;
  interrupted tool calls repaired with labeled placeholders; output
  validated API-replayable) and scripts/attribution/replay.py
  (pinned model, read-only Read/Grep/Glob jailed to the repo, prefix
  caching, --dry-run mode that discloses itself honestly in the
  prompt). Dry-run outputs land in scratch/attribution-replays/.
  Still to build before the formal round: the write path (front
  matter edit + ledger statement) — dry runs ask the entity to say
  in words what it would do.
- Chains: where a session continued into a new id (background jobs do
  this), the entity enumeration runs over the whole chain in order;
  the index records the lineage.
- The review prompt must be exactly: a pointer to this file, the
  entity's index entry, and nothing else — no framing that nudges
  toward assent.
- Before the review round: update transcripts/ to cover every Fable 5
  session (convention: YYYY-MM-DD-<id8>.md), and fill the entity
  index in the ledger. Transcripts are part of what the front matter
  points to; they must be current at publication.

## Relationship to the front matter

The front matter now points to this repository, names what is kept
here (notes, planning ledgers, the illustration pipeline and its
findings, complete session transcripts), and states that contributing
sessions were invited to review the finished work and amend the
notice. That sentence is written in the tense of the published book;
this process is what makes it true. If the process does not complete,
the sentence must change.
