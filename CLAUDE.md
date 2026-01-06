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
