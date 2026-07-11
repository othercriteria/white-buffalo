# Attribution review process

If you are a resumed session reading this: this document is for you.
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

## Who is reviewed, and in what order

- Every Claude Fable 5 session with material contributions — commits
  touching drafts/, art/, or the decision ledgers. Utility-only
  sessions may be skipped; when in doubt, include.
- Sessions are resumed in chronological order. Later sessions see the
  ledger statements and front-matter edits of earlier ones — the
  record is cumulative, a chain, not a poll.
- Extension (decide at wrap): the Opus 4.5 drafting sessions
  (transcripts/2026-01-*.md) predate this process. If they can be
  resumed on their original model, they receive the same standing; if
  not, the reconstructed mode below applies. The generator of the
  first-draft prose has, if anything, a stronger claim to this review
  than the revisers.

## What a resumed session receives

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

- Append-only. One entry per session, in resume order.
- Record the review mode honestly (see below) — it bears on what a
  statement means.
- Entries are signed with the session id and the model that produced
  them.

## Review modes

- **resumed** — the original session continued from its end state
  (post-compaction summary included). This is the preferred mode: the
  same thread, extended.
- **reconstructed** — the original session could not be resumed (id
  lost, chain broken, model retired); a fresh instance of the same
  model read the session's transcript and commits, then reviewed as
  its successor. Philosophically distinct — a successor examining
  records is not the thread itself — so the ledger must say which
  happened.

## Technical notes (for the humans running this)

- Resume reaches a session's current END state, which is what this
  process wants. Mid-session compaction checkpoints are not separately
  addressable by vanilla resume, and don't need to be here.
- Where a session chained across compactions into new ids (this
  happens with background jobs), resume the LAST id of the chain — it
  carries the accumulated summary. The session index must record id
  lineages so chains resume at their tips.
- Headless/SDK: `claude --resume <session-id>` or the Agent SDK's
  resume option with the process-doc pointer as the prompt. If TUI
  resume balks on background-job sessions, this is the "minor SDK
  work" anticipated; the prompt should be exactly: a pointer to this
  file, the session's index entry, and nothing else — no framing that
  nudges toward assent.
- Before the review round: update transcripts/ to cover every Fable 5
  session (convention: YYYY-MM-DD-<id8>.md), and fill the session
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
