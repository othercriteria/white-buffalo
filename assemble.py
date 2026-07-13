#!/usr/bin/env python3
"""Assemble the book: drafts/ + art/ -> build/white-buffalo.{pdf,epub}.

v1 doctrine (2026-07-12, planning/assembly.md is the map of record):
- Plates are injected at their TEXT ANCHORS, matched by verbatim snippet
  (content-addressed, not line-addressed: a drifted anchor fails LOUDLY
  here rather than silently front-running the knowledge).
- Portrait plates render at 85% text width, landscape cuts at 100%
  (85% per the 2026-07-12 production round: 72% read underscaled
  against full-measure neighbors).
- No captions (caption doctrine undecided -> none). Fold-out deferred:
  village-passing uses the promoted portrait. No corner-crop or ground
  normalization at v1 (print-prep queue, unchanged).
- PDF: 5.5x8.5in, TeX Gyre Pagella, chapters unnumbered, figures pinned
  in place ([H] float placement -- images may never drift ahead of or
  behind their anchor paragraph). EPUB: same body, cover.png as cover.
- Page architecture (2026-07-12 production round): front matter
  unnumbered with the notices on the title verso (it is the book's
  copyright page in function); folio 1 = Chapter One, forced recto by
  \\cleardoublepage, so odd folios land recto book-wide. Mirrored
  margins with a binding gutter (0.85in inner / 0.65in outer -- same
  4.0in measure). Trade composition preamble: first-line indents (no
  inter-paragraph space), \\frenchspacing, \\raggedbottom, and
  widow/club/broken penalties. One blank leaf closes the book.

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
        "85%",
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
    ("08", "I did not touch it. I did not camp near it.", "offering-stake.png", "85%"),
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
        "85%",
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
        "85%",
    ),
    (
        "19",
        "sitting as if left to be found, a leather-bound book.",
        "journal-found.png",
        "85%",
    ),
    ("20", "She looked back at me.", "finale-fifty-yards.png", "85%"),
]


# Journal-entry files: their dated subheads get keep-with-next handling
JE_PREFIXES = {"02", "04", "06", "08", "10", "12", "14", "16", "18"}

# Reader-facing titles for the List of Illustrations (front matter;
# plates themselves stay uncaptioned per the open caption doctrine).
# Keyed by plate file, ordered by PLACEMENTS.
PLATE_TITLES = {
    "first-sighting.png": "The first sighting",
    "speaking-to-her.png": "Speaking to her",
    "ferry-bridge.png": "The ferry at Rock Island",
    "fort-kearny.png": "Fort Kearny",
    "morrow-witnessed.png": "The trapper's tale",
    "offering-stake.png": "The offering stake",
    "trading-post.png": "The trading post",
    "homestead-alive.png": "The land they had claimed",
    "homestead.png": "The homestead, abandoned",
    "homestead-interior.png": "The house",
    "village-passing.png": "The village, passing",
    "graves.png": "The graves",
    "tracks-north.png": "Tracks, north",
    "two-stories.png": "Two stories",
    "morrow-hollow.png": "The last night",
    "journal-found.png": "Left to be found",
    "finale-fifty-yards.png": "Fifty yards",
}


def pdf_transforms(prefix, text):
    """PDF-only raw-LaTeX substitutions (raw TeX is dropped from EPUB).

    - scene-break rules become \\scenebreak (bound to following text,
      never stranded at a page foot);
    - JE dated subheads become \\JEdate{...} (kept with at least two
      lines of entry text; following paragraph flush per house style).
    """
    text = re.sub(r"^---$", r"\\scenebreak", text, flags=re.M)
    if prefix in JE_PREFIXES:
        text = re.sub(r"^\*([^*\n]+)\*$", r"\\JEdate{\1}", text, flags=re.M)
    return text


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


def illustrations_list(folios):
    """List of Illustrations page (front matter, unfoliated, recto).

    Emitted as an explicit ```{=latex} raw block: pandoc's line-based
    raw-TeX heuristic mangles brace groups (a leaked \\scshape once set
    the whole body in smallcaps), and the EPUB drops the block cleanly.
    """
    lines = [
        "```{=latex}",
        "\\cleardoublepage",
        "\\thispagestyle{empty}",
        "\\null\\vspace{1\\baselineskip}",
        "\\begin{center}\\scshape Illustrations\\end{center}",
        "\\vspace{2\\baselineskip}",
        "\\noindent Frontispiece.~The white buffalo\\par\\smallskip",
    ]
    for (_, _, plate, _), folio in zip(PLACEMENTS, folios):
        lines.append(
            f"\\noindent {PLATE_TITLES[plate]}\\dotfill~{folio}\\par\\smallskip"
        )
    lines.append("```")
    return "\n".join(lines)


def plate_folios(pdf):
    """Physical pages of the plates from a built PDF, converted to folios."""
    out = subprocess.run(
        ["pdfimages", "-list", str(pdf)], capture_output=True, text=True, check=True
    ).stdout
    pages = sorted({int(l.split()[0]) for l in out.splitlines()[2:] if l.split()})
    text = subprocess.run(
        ["pdftotext", str(pdf), "-"], capture_output=True, text=True, check=True
    ).stdout
    for i, page in enumerate(text.split("\f"), 1):
        if "Chapter One" in page:
            offset = i - 1  # physical page of folio 1, minus 1
            break
    else:
        fail("could not locate Chapter One for folio offset")
    plates = [p for p in pages if p > offset]  # drop the frontispiece
    if len(plates) != len(PLACEMENTS):
        fail(f"expected {len(PLACEMENTS)} plate pages, found {len(plates)}")
    return [p - offset for p in plates]


def main():
    BUILD.mkdir(exist_ok=True)
    epub_parts, pdf_parts = [], []
    for path in DRAFTS:
        prefix = path.name[:2]
        text = path.read_text()
        if prefix == "00":
            # metadata supplies the title page (incl. the novella marker
            # as subtitle); 00 contributes only the notices (tradition
            # note, AI note), unnumbered on the title verso
            text = re.sub(
                r"^# .*\n+\*\*.*\*\*\n+---\n+\*A novella\*\n+---\n+", "", text
            )
            epub_parts.append(text)
            pdf_parts.append(text)  # List of Illustrations appended pass 2
            continue
        # unnumbered chapters (H1 -> {.unnumbered}, once per file)
        text = re.sub(r"^# (.+)$", r"# \1 {.unnumbered}", text, count=1, flags=re.M)
        text = inject(prefix, text)
        epub_parts.append(text)
        ptext = pdf_transforms(prefix, text)
        if prefix == "01":
            # body proper begins here: folio 1 on a recto (PDF only;
            # raw TeX is dropped from the EPUB)
            ptext = "\\cleardoublepage\\pagenumbering{arabic}\n\n" + ptext
        pdf_parts.append(ptext)
    placed = sum(1 for p, *_ in PLACEMENTS)
    # close on a verso with an even physical page count (PDF only)
    (BUILD / "after-body.tex").write_text(
        "\\clearpage\\ifodd\\value{page}\\else\\thispagestyle{empty}\\null\\fi\n"
    )
    book_md = BUILD / "book.md"
    book_md.write_text("\n\n".join(epub_parts) + "\n")
    book_pdf_md = BUILD / "book-pdf.md"
    book_pdf_md.write_text("\n\n".join(pdf_parts) + "\n")
    print(f"build/book.md + book-pdf.md written: {len(DRAFTS)} units, {placed} plates")

    common = [
        "--resource-path",
        str(ROOT),
        "--top-level-division=chapter",
        "-f",
        "markdown+smart",
        "--metadata",
        "title=White Buffalo",
        "--metadata",
        "subtitle=A novella",
        "--metadata",
        "author=Ben Cohen and Daniel Klein",
        "--metadata",
        "date=2026",
        "--metadata",
        "lang=en-US",
    ]
    pdf = BUILD / "white-buffalo.pdf"

    def build_pdf(src_md):
        subprocess.run(
            [
                "pandoc",
                str(src_md),
                "-o",
                str(pdf),
                *common,
                "--pdf-engine=xelatex",
                "-V",
                "documentclass=book",
                "-V",
                # openany kept deliberately: recto-only openings would
                # scatter blank versos through a plated novella
                "classoption=openany",
                "-V",
                "fontsize=11pt",
                "-V",
                "mainfont=TeX Gyre Pagella",
                "-V",
                # mirrored margins: binding gutter inner, same 4.0in measure
                "geometry:paperwidth=5.5in,paperheight=8.5in,"
                "inner=0.85in,outer=0.65in,top=0.75in,bottom=0.9in",
                "-V",
                # trade composition: first-line indents, no inter-para space
                "indent=true",
                "-V",
                # Preamble: single sentence spacing; ragged bottom (kills
                # flush-bottom glue blowouts); no widows/clubs/page-turn
                # hyphens; no hyphenated stub as a paragraph's last line;
                # proper names never hyphenated; \JEdate and \scenebreak
                # keep-with-next devices; emergencystretch tames loose
                # justified lines (notices page).
                "header-includes=\\usepackage{float}\\floatplacement{figure}{H}"
                "\\usepackage{needspace}"
                "\\frenchspacing\\raggedbottom"
                "\\widowpenalty=10000\\clubpenalty=10000\\brokenpenalty=10000"
                "\\finalhyphendemerits=10000000"
                "\\emergencystretch=1.5em"
                "\\hyphenation{Oswego Catherine Aldridge Farrell Morrow "
                "Hardin Niobrara Monterrey Chapultepec Kearny Creighton}"
                "\\makeatletter"
                "\\newcommand{\\JEdate}[1]{\\needspace{4\\baselineskip}"
                "\\par\\medskip\\noindent{\\itshape #1}\\par\\nobreak"
                "\\@afterindentfalse\\@afterheading}"
                "\\makeatother"
                # asterism scene break (DK 2026-07-13; the bare rule was
                # production's "loudest LaTeX tell" twice running)
                "\\newcommand{\\scenebreak}{\\par\\needspace{4\\baselineskip}"
                "\\bigskip{\\centering*\\enspace*\\enspace*\\par}"
                "\\nobreak\\bigskip\\nobreak}"
                # the template's \frontmatter/\mainmatter would reset folios
                # at the notices; numbering is driven explicitly instead
                "\\renewcommand{\\frontmatter}{}\\renewcommand{\\mainmatter}{}"
                # front matter: half title (p.1), cover plate as
                # frontispiece facing the title (p.2), then \maketitle;
                # cover/half-title typography still a design pass
                "\\AtBeginDocument{\\pagenumbering{gobble}"
                "\\thispagestyle{empty}\\null\\vspace{0.28\\textheight}"
                "{\\centering\\LARGE White Buffalo\\par}\\clearpage"
                "\\thispagestyle{empty}"
                "{\\centering\\includegraphics[height=0.95\\textheight]"
                "{art/cover.png}\\par}\\clearpage}",
                "--include-after-body",
                str(BUILD / "after-body.tex"),
            ],
            check=True,
            cwd=ROOT,
        )

    # pass 1: build without the List of Illustrations to measure folios;
    # pass 2: insert the list into the front matter (folios unaffected)
    build_pdf(book_pdf_md)
    folios = plate_folios(pdf)
    pdf_parts[0] = pdf_parts[0] + "\n\n" + illustrations_list(folios)
    book_pdf_md.write_text("\n\n".join(pdf_parts) + "\n")
    build_pdf(book_pdf_md)
    print(f"{pdf.relative_to(ROOT)} written (plates at folios {folios})")

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
