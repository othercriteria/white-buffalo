# White Buffalo - Writing Project

## Project Structure

```
drafts/      # Chapter drafts - the actual manuscript
notes/       # Working notes: characters, scenes, research, worldbuilding
planning/    # Story structure, outlines, arc tracking
reference/   # External style guides, context documents
scratch/     # Ephemera - safe to delete anytime
```

## Workflow

- **Commit frequently.** Small, meaningful commits. Be fearless about deleting material that no longer serves the work.
- **drafts/** contains canonical text. Number chapters for ordering: `01-chapter-name.md`
- **notes/** is for thinking. These inform drafts but aren't part of the manuscript.
- **scratch/** is for true throwaway content - experiments, dead ends, temporary dumps.

## Conventions

- All prose in Markdown
- One chapter per file in drafts/
- Use `## Scene` headers within chapters if helpful for navigation
- Character names in notes should use consistent filenames: `notes/characters/firstname-lastname.md`

## Useful Commands

```bash
# Word count for manuscript
find drafts -name '*.md' -exec cat {} + | wc -w

# Compile manuscript to single file
pandoc drafts/*.md -o manuscript.md

# Export to PDF (if needed)
pandoc drafts/*.md -o manuscript.pdf
```

## Context Management

At ~60k words target, the full manuscript approaches context limits. Strategies:
- Work on one chapter at a time when drafting
- Use grep/search to find specific passages rather than reading everything
- Keep notes files focused and atomic
- Summarize completed sections in planning/ to reduce need to re-read
- For revision: use "masking" - read all but one section, write expectations, verify after compaction

## Drafting Workflow

1. **Before writing a chapter:** Re-read outline, check what precedes it, note what must be established
2. **While drafting:** Stay in the voice, don't break for meta-commentary
3. **After drafting:** Self-review against checklist (see planning/process.md), commit
4. **After each Part:** Pause for consistency check, update continuity notes

## Self-Review Principles

- Does this feel like the same book as what came before?
- Would a reader who knows this period find it credible?
- Is there anything clever or cute? (If yes, cut it)
- Does the prose call attention to itself? (If yes, simplify)
- What does the reader know now that they didn't before?
- What question makes them turn the page?

## Quality Criteria

**Voice:** Each narrator distinct. No anachronisms in language or concepts. Prose appropriate to stated style target.

**Consistency:** Geography, timeline, character details, weather all internally coherent. Protagonist doesn't know things he hasn't learned.

**Pacing:** Each chapter earns its length. Momentum toward the next. No wheel-spinning.

**Authenticity:** Period-accurate material culture, social dynamics, speech patterns. No 21st-century framings imposed on 19th-century characters.

**Restraint:** Play it straight. No meta-textual games, no winking at the reader, no over-explanation.
