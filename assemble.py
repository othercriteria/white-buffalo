#!/usr/bin/env python3
"""Assemble the book: drafts/ + art/ -> build/white-buffalo.{pdf,epub}.

v1 doctrine (2026-07-12, planning/assembly.md is the map of record):
- Plates are injected at their TEXT ANCHORS, matched by verbatim snippet
  (content-addressed, not line-addressed: a drifted anchor fails LOUDLY
  here rather than silently front-running the knowledge).
- Portrait plates render at 72% text width, landscape cuts at 100%.
- No captions (caption doctrine undecided -> none). Fold-out deferred:
  village-passing uses the promoted portrait. No corner-crop or ground
  normalization at v1 (print-prep queue, unchanged).
- PDF: 5.5x8.5in, TeX Gyre Pagella, chapters unnumbered, figures pinned
  in place ([H] float placement -- images may never drift ahead of or
  behind their anchor paragraph). EPUB: same body, cover.png as cover.

Run: python3 assemble.py   (or `make book`)
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DRAFTS = sorted((ROOT / "drafts").glob("*.md"))
BUILD = ROOT / "build"

# (draft prefix, anchor snippet -- plate goes AFTER this paragraph,
#  plate file, width) -- order within a file = insertion order.
PLACEMENTS = [
    (
        "02",
        "She moved through the brown grass like a ghost.",
        "first-sighting.png",
        "72%",
    ),
    (
        "04",
        "and I sat on my rise and watched the sun go down.",
        "speaking-to-her.png",
        "100%",
    ),
    (
        "05",
        "The current worked against the hull, and the far shore came on slowly.",
        "ferry-bridge.png",
        "100%",
    ),
    ("07", "carried a thousand miles on muleback.", "fort-kearny.png", "100%"),
    (
        "07",
        'I never saw anything like that. Never want to again."',
        "morrow-witnessed.png",
        "100%",
    ),
    ("08", "I did not touch it. I did not camp near it.", "offering-stake.png", "72%"),
    (
        "09",
        "a horse stood in a lean-to stable against the south wall, its breath steaming in the cold air.",
        "trading-post.png",
        "100%",
    ),
    (
        "10",
        "and they stood together looking out at the land they had claimed.",
        "homestead-alive.png",
        "100%",
    ),
    (
        "11",
        "marked where someone had tried to plant a garden.",
        "homestead.png",
        "100%",
    ),
    (
        "11",
        "the blankets on the bed had not been slept in for a very long time.",
        "homestead-interior.png",
        "100%",
    ),
    (
        "12",
        "the grass lay combed flat by the poles, long marks running south.",
        "village-passing.png",
        "72%",
    ),
    (
        "13",
        "not mounded up as they would have been over a shallow burial.",
        "graves.png",
        "100%",
    ),
    ("15", "But I knew he was out there. I could feel it.", "tracks-north.png", "100%"),
    (
        "17",
        "She was lost in the white, and I found her only when she moved.",
        "two-stories.png",
        "100%",
    ),
    (
        "18",
        "a twist of cloth burning in a horn of buffalo tallow.",
        "morrow-hollow.png",
        "72%",
    ),
    (
        "19",
        "sitting as if left to be found, a leather-bound book.",
        "journal-found.png",
        "72%",
    ),
    ("20", "She looked back at me.", "finale-fifty-yards.png", "72%"),
]


def fail(msg):
    print(f"ASSEMBLY FAILED: {msg}", file=sys.stderr)
    sys.exit(1)


def inject(prefix, text):
    """Insert plate markup after each anchor paragraph for this draft."""
    for pfx, snippet, plate, width in PLACEMENTS:
        if pfx != prefix:
            continue
        if not (ROOT / "art" / plate).exists():
            fail(f"missing plate art/{plate}")
        hits = text.count(snippet)
        if hits != 1:
            fail(
                f"anchor snippet for art/{plate} found {hits}x in "
                f"{prefix} (need exactly 1): ...{snippet[-50:]!r}"
            )
        # end of the paragraph containing the snippet = next blank line
        idx = text.index(snippet)
        para_end = text.find("\n\n", idx)
        if para_end == -1:
            para_end = len(text)
        img = f"\n\n![](art/{plate}){{width={width}}}"
        text = text[:para_end] + img + text[para_end:]
    return text


def main():
    BUILD.mkdir(exist_ok=True)
    parts = []
    for path in DRAFTS:
        prefix = path.name[:2]
        text = path.read_text()
        if prefix == "00":
            # metadata supplies the title page; 00 contributes only the
            # notices (novella marker, tradition note, AI note)
            text = re.sub(r"^# .*\n+\*\*.*\*\*\n+---\n+", "", text)
            parts.append(text)
            continue
        # unnumbered chapters (H1 -> {.unnumbered}, once per file)
        text = re.sub(r"^# (.+)$", r"# \1 {.unnumbered}", text, count=1, flags=re.M)
        parts.append(inject(prefix, text))
    placed = sum(1 for p, *_ in PLACEMENTS)
    book_md = BUILD / "book.md"
    book_md.write_text("\n\n".join(parts) + "\n")
    print(f"build/book.md written: {len(DRAFTS)} units, {placed} plates")

    common = [
        "--resource-path",
        str(ROOT),
        "--top-level-division=chapter",
        "-f",
        "markdown+smart",
        "--metadata",
        "title=White Buffalo",
        "--metadata",
        "author=Ben Cohen and Daniel Klein",
        "--metadata",
        "lang=en-US",
    ]
    pdf = BUILD / "white-buffalo.pdf"
    subprocess.run(
        [
            "pandoc",
            str(book_md),
            "-o",
            str(pdf),
            *common,
            "--pdf-engine=xelatex",
            "-V",
            "documentclass=book",
            "-V",
            "classoption=openany",
            "-V",
            "fontsize=11pt",
            "-V",
            "mainfont=TeX Gyre Pagella",
            "-V",
            "geometry:paperwidth=5.5in,paperheight=8.5in,margin=0.75in,bottom=0.9in",
            "-V",
            "header-includes=\\usepackage{float}\\floatplacement{figure}{H}",
        ],
        check=True,
        cwd=ROOT,
    )
    print(f"{pdf.relative_to(ROOT)} written")

    epub = BUILD / "white-buffalo.epub"
    subprocess.run(
        [
            "pandoc",
            str(book_md),
            "-o",
            str(epub),
            *common,
            "--epub-cover-image",
            str(ROOT / "art" / "cover.png"),
            "--toc",
            "--toc-depth=1",
        ],
        check=True,
        cwd=ROOT,
    )
    print(f"{epub.relative_to(ROOT)} written")


if __name__ == "__main__":
    main()
