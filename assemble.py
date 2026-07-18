#!/usr/bin/env python3
"""Assemble the book: drafts/ + art/ -> build/white-buffalo.{pdf,epub}.

v1 doctrine (2026-07-12, planning/assembly.md is the map of record):
- Plates are injected at their TEXT ANCHORS, matched by verbatim snippet
  (content-addressed, not line-addressed: a drifted anchor fails LOUDLY
  here rather than silently front-running the knowledge).
- Format doctrine implemented in full (DK 2026-07-18, production
  memo scratch/plate-leaves-memo-2026-07-18.md): the five portrait
  plates are DEDICATED FULL-PAGE LEAVES ("full" in PLACEMENTS) —
  \\fullplate: own page, folio counted but unprinted, versos live,
  no captions, no recto-forcing. Pinning for leaves relaxes to
  "never ahead of the anchor; behind it by at most one page break."
  Landscape cuts stay inline at 100% via \\bookplate; the one
  landscape-flex journal plate (speaking-to-her) stays inline.
  Full leaves gate on resolution: the build fails below 300ppi at
  laid size (the hires_refine 2x pass supplies ~415ppi).
- TWO ARTIFACTS (DK 2026-07-18): white-buffalo.pdf is CANONICAL
  (gatefold leaf intact); white-buffalo-pod.pdf is the POD setting —
  the gatefold panorama split across a facing spread (verso+recto,
  to its acknowledged artistic detriment), colophon note explains
  the reduction. No other differences.
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
        "full",
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
    ("08", "I did not touch it. I did not camp near it.", "offering-stake.png", "full"),
    (
        "09",
        "reaching up out of the white.",
        "frozen-man.png",
        "100%",
    ),
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
        "village-passing-foldout.png",
        "100%",
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
        "full",
    ),
    (
        "19",
        "sitting as if left to be found, a leather-bound book.",
        "journal-found.png",
        "full",
    ),
    ("20", "She looked back at me.", "finale-fifty-yards.png", "full"),
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
    "frozen-man.png": "The frozen man",
    "trading-post.png": "The trading post",
    "homestead-alive.png": "The land they had claimed",
    "homestead.png": "The homestead, abandoned",
    "homestead-interior.png": "The house",
    "village-passing-foldout.png": "The village, passing",
    "graves.png": "The graves",
    "tracks-north.png": "Tracks, north",
    "two-stories.png": "Two stories",
    "morrow-hollow.png": "The last night",
    "journal-found.png": "Left to be found",
    "finale-fifty-yards.png": "Fifty yards",
}


def pdf_transforms(prefix, text, pod=False):
    """PDF-only raw-LaTeX substitutions (raw TeX is dropped from EPUB).

    - scene-break rules become \\scenebreak (bound to following text,
      never stranded at a page foot);
    - JE dated subheads become \\JEdate{...} (kept with at least two
      lines of entry text; following paragraph flush per house style);
    - width=full plates become dedicated leaves (\\clearpage, image
      vertically centered, folio counted but unprinted);
    - pod=True replaces the gatefold leaf with a facing-spread split
      (verso+recto halves; the POD setting's one reduction).
    """
    text = re.sub(r"^---$", r"\\scenebreak", text, flags=re.M)
    if prefix in JE_PREFIXES:
        text = re.sub(r"^\*([^*\n]+)\*$", r"\\JEdate{\1}", text, flags=re.M)
    # Gatefold (the format doctrine's one permitted exception; DK bless
    # 2026-07-14, s1036). The panorama ships on a fold-out leaf: recto
    # (\cleardoublepage — the fold opens outward), double-width page via
    # the \pdfpagewidth primitive (mechanics probed same day: XeLaTeX +
    # xdvipdfmx handle mixed page sizes), folio counted but unprinted.
    # Leaf width 10.75in = 2x trim minus 1/4in fold clearance
    # (production-honest; the PDF carries the unfolded leaf). Centering
    # is hardcoded recto math: origin = 1in + \oddsidemargin = inner =
    # 0.85in; image left = (10.75 - 10.1)/2 = 0.325in; hspace = -0.525in.
    # Revisit if A-series geometry ever moves. Emitted as a {=latex}
    # fence (see illustrations_list on pandoc's raw-TeX line heuristic).
    # Must run BEFORE the \bookplate rule, which would otherwise match.
    if pod:
        # POD setting (DK 2026-07-18): no printer binds a 10.75in leaf
        # into a 5.5in trim. The panorama is divided across a facing
        # spread — forced to open on a VERSO so the halves face each
        # other — to its acknowledged artistic detriment; the colophon
        # says so. Half folios counted but unprinted (gatefold rule);
        # any parity filler page is empty-styled.
        text = re.sub(
            r"^!\[\]\(build/plates/village-passing-foldout\.png\)\{width=\d+%\}$",
            lambda m: (
                "```{=latex}\n"
                "\\clearpage\n"
                "\\ifodd\\value{page}\\thispagestyle{empty}\\null\\clearpage\\fi\n"
                "\\thispagestyle{empty}\n"
                "\\vspace*{\\fill}\n"
                "{\\centering\\includegraphics[width=\\textwidth]"
                "{build/plates/village-passing-pod-left.png}\\par}\n"
                "\\vspace*{\\fill}\n"
                "\\clearpage\n"
                "\\thispagestyle{empty}\n"
                "\\vspace*{\\fill}\n"
                "{\\centering\\includegraphics[width=\\textwidth]"
                "{build/plates/village-passing-pod-right.png}\\par}\n"
                "\\vspace*{\\fill}\n"
                "\\clearpage\n"
                "```"
            ),
            text,
            flags=re.M,
        )
    text = re.sub(
        r"^!\[\]\((build/plates/village-passing-foldout\.png)\)\{width=\d+%\}$",
        lambda m: (
            "```{=latex}\n"
            "\\clearpage{\\pagestyle{empty}\\cleardoublepage}\n"
            "\\pdfpagewidth=10.75in\n"
            "\\thispagestyle{empty}\n"
            "\\vspace*{\\fill}\n"
            "\\noindent\\hspace*{-0.525in}"
            f"\\includegraphics[width=10.1in]{{{m.group(1)}}}\n"
            "\\vspace*{\\fill}\n"
            "\\clearpage\n"
            "\\pdfpagewidth=5.5in\n"
            "```"
        ),
        text,
        flags=re.M,
    )
    # Full-page plate leaves (format doctrine implemented, DK
    # 2026-07-18): image alone on its page, vertically centered on the
    # measure, folio counted but unprinted (gatefold house rule), no
    # recto-forcing, versos live. Must run BEFORE the \bookplate rule.
    text = re.sub(
        r"^!\[\]\((build/plates/[^)]+)\)\{width=full\}$",
        lambda m: (
            "```{=latex}\n"
            "\\clearpage\n"
            "\\thispagestyle{empty}\n"
            "\\vspace*{\\fill}\n"
            f"{{\\centering\\includegraphics[width=\\textwidth]{{{m.group(1)}}}\\par}}\n"
            "\\vspace*{\\fill}\n"
            "\\clearpage\n"
            "```"
        ),
        text,
        flags=re.M,
    )
    # pandoc 3 leaves captionless images as bare \includegraphics in an
    # ordinary (indented!) paragraph — never centered, and immune to
    # float spacing. \bookplate centers on the measure with codified air.
    text = re.sub(
        r"^!\[\]\((build/plates/[^)]+)\)\{width=(\d+)%\}$",
        lambda m: f"\\bookplate{{{int(m.group(2)) / 100}}}{{{m.group(1)}}}",
        text,
        flags=re.M,
    )
    return text


def fail(msg):
    print(f"ASSEMBLY FAILED: {msg}", file=sys.stderr)
    sys.exit(1)


# Units that must NEVER carry a plate (guardrails, DK 2026-07-13):
# JE VII (14) — the murder-decision entry illustrated by nothing is the
# plate policy working as intended; three instrument rounds have called
# its bareness the program's best placement decision. The build fails
# rather than lets a future placement land there.
BARE_UNITS = {"14"}


def inject(prefix, text):
    """Insert plate markup after each anchor paragraph for this draft."""
    for pfx, snippet, plate, width in PLACEMENTS:
        if pfx in BARE_UNITS:
            fail(
                f"placement for art/{plate} targets unit {pfx}, which is "
                "guarded bare (BARE_UNITS) — see the plate-policy record"
            )
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
        # plates reference the knocked-out copies (grounds -> page
        # white, DK 2026-07-13: cream in art/ is the record; cream in
        # the book is artifice); art/ is never modified
        img = f"\n\n![](build/plates/{plate}){{width={width}}}"
        text = text[:para_end] + img + text[para_end:]
    return text


def knockout_plates():
    """Produce build/plates/ = art/ plates with grounds knocked to
    page white (imagegen/knockout.py; PIL lives in that venv). Also
    derives the POD spread halves of the gatefold panorama."""
    plates = sorted({p for _, _, p, _ in PLACEMENTS} | {"cover-tracks.png"})
    subprocess.run(
        [
            str(ROOT / "imagegen" / ".venv" / "bin" / "python"),
            "knockout.py",
            *[str(ROOT / "art" / p) for p in plates],
            "-o",
            str(BUILD / "plates"),
        ],
        check=True,
        cwd=ROOT / "imagegen",
    )
    subprocess.run(
        [
            str(ROOT / "imagegen" / ".venv" / "bin" / "python"),
            "-c",
            "from PIL import Image\n"
            "from pathlib import Path\n"
            f"src = Path(r'{BUILD}/plates/village-passing-foldout.png')\n"
            "left = src.with_name('village-passing-pod-left.png')\n"
            "right = src.with_name('village-passing-pod-right.png')\n"
            "if not (left.exists() and right.exists()\n"
            "        and left.stat().st_mtime >= src.stat().st_mtime):\n"
            "    im = Image.open(src)\n"
            "    w, h = im.size\n"
            "    im.crop((0, 0, w // 2, h)).save(left)\n"
            "    im.crop((w // 2, 0, w, h)).save(right)\n",
        ],
        check=True,
        cwd=ROOT,
    )


def check_full_plate_resolution():
    """Full-page leaves lay at the 4.0in measure; fail below 300ppi
    (the hires_refine 2x pass supplies ~415ppi for portraits)."""
    fulls = [p for _, _, p, w in PLACEMENTS if w == "full"]
    out = subprocess.run(
        [
            str(ROOT / "imagegen" / ".venv" / "bin" / "python"),
            "-c",
            "import sys\nfrom PIL import Image\n"
            "for p in sys.argv[1:]:\n"
            "    print(p, Image.open(p).size[0])\n",
            *[str(ROOT / "art" / p) for p in fulls],
        ],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    for line in out.splitlines():
        path, w = line.rsplit(None, 1)
        if int(w) < 1200:
            fail(
                f"full-page plate {Path(path).name} is {w}px wide "
                "(<300ppi at the 4.0in measure) — run the hires_refine "
                "2x pass before promoting it to a leaf"
            )


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
        "\\noindent Frontispiece.~The two trails\\par\\smallskip",
    ]
    for (_, _, plate, _), folio in zip(PLACEMENTS, folios):
        lines.append(
            f"\\noindent {PLATE_TITLES[plate]}\\dotfill~{folio}\\par\\smallskip"
        )
    lines.append("```")
    return "\n".join(lines)


def plate_folios(pdf, pod=False):
    """Physical pages of the plates from a built PDF, converted to folios.

    In the POD setting the gatefold occupies two facing pages; the
    second half collapses into the first for the List of Illustrations
    (the list names the plate, not its pieces)."""
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
    expected = len(PLACEMENTS) + (1 if pod else 0)
    if len(plates) != expected:
        fail(f"expected {expected} plate pages, found {len(plates)}")
    if pod:
        village = next(
            i
            for i, (_, _, p, _) in enumerate(PLACEMENTS)
            if p == "village-passing-foldout.png"
        )
        if plates[village + 1] != plates[village] + 1:
            fail("POD gatefold halves are not on consecutive pages")
        del plates[village + 1]
    return [p - offset for p in plates]


def main():
    BUILD.mkdir(exist_ok=True)
    knockout_plates()
    check_full_plate_resolution()
    epub_parts, pdf_parts, pod_parts = [], [], []
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
            # one break grammar book-wide: notices dividers are asterisms
            # too (DK 2026-07-13); List of Illustrations appended pass 2.
            # Notices are set as notices, not body prose (production r3
            # S2): smaller, flush-left, block-spaced — in place; nothing
            # moves to the back (disclosure precedes reading; the formal
            # round's edit rights target this front matter).
            ptext = re.sub(r"^---$", r"\\scenebreak", text, flags=re.M)
            notices = (
                "\\begingroup\\small\\setlength{\\parindent}{0pt}"
                "\\setlength{\\parskip}{0.6\\baselineskip}\n\n"
                + ptext
                + "\n\n\\endgroup"
            )
            pdf_parts.append(notices)
            pod_parts.append(notices)
            continue
        # "Journal Entry N" -> "From the Journal — N" (DK 2026-07-13):
        # each unit holds a batch of dated entries, and "From" admits
        # the excerption honestly — the compiler's one visible
        # fingerprint. Assembly-level: filenames and the "JE" planning
        # shorthand stay.
        if prefix in JE_PREFIXES:
            text = re.sub(
                r"^# Journal Entry (.+)$",
                r"# From the Journal — \1",
                text,
                count=1,
                flags=re.M,
            )
        # unnumbered chapters (H1 -> {.unnumbered}, once per file)
        text = re.sub(r"^# (.+)$", r"# \1 {.unnumbered}", text, count=1, flags=re.M)
        text = inject(prefix, text)
        # EPUB has no leaf concept: full plates render as inline images
        epub_parts.append(text.replace("{width=full}", "{width=85%}"))
        ptext = pdf_transforms(prefix, text)
        podtext = pdf_transforms(prefix, text, pod=True)
        if prefix == "01":
            # body proper begins here: folio 1 on a recto (PDF only;
            # raw TeX is dropped from the EPUB)
            head = "\\cleardoublepage\\pagenumbering{arabic}\n\n"
            ptext = head + ptext
            podtext = head + podtext
        pdf_parts.append(ptext)
        pod_parts.append(podtext)
    placed = sum(1 for p, *_ in PLACEMENTS)
    # end matter (PDF only): a spare colophon — craft information,
    # additive to the notices, never a relocation of them — then a
    # final blank leaf regardless of parity (production r3 M3), ending
    # on a verso.
    colophon_head = (
        "\\cleardoublepage\\thispagestyle{empty}"
        "\\null\\vspace{0.35\\textheight}"
        "{\\centering\\small "
        "Set in TeX Gyre Pagella.\\par\\medskip "
        "The frontispiece and eighteen plates were drawn by an image "
        "model in the idiom of the nineteenth-century wood engraving, "
        "curated by the authors and audited against the text.\\par"
    )
    colophon_tail = (
        "\\medskip Assembled from the working record at\\par "
        "github.com/othercriteria/white-buffalo\\par}"
        "\\clearpage\\thispagestyle{empty}\\null"
        "\\ifodd\\value{page}\\clearpage\\thispagestyle{empty}\\null\\fi\n"
    )
    (BUILD / "after-body.tex").write_text(colophon_head + colophon_tail)
    # POD colophon carries the reduction honestly (DK 2026-07-18): the
    # canonical setting is the one with the fold-out leaf.
    (BUILD / "after-body-pod.tex").write_text(
        colophon_head + "\\medskip This is the print-on-demand setting: the fold-out "
        "plate, \\emph{The village, passing}, is here divided across a "
        "facing spread. The canonical setting carries it whole, on a "
        "fold-out leaf.\\par" + colophon_tail
    )
    book_md = BUILD / "book.md"
    book_md.write_text("\n\n".join(epub_parts) + "\n")
    book_pdf_md = BUILD / "book-pdf.md"
    book_pdf_md.write_text("\n\n".join(pdf_parts) + "\n")
    book_pod_md = BUILD / "book-pod.md"
    book_pod_md.write_text("\n\n".join(pod_parts) + "\n")
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

    def build_pdf(src_md, out_pdf, after_body):
        subprocess.run(
            [
                "pandoc",
                str(src_md),
                "-o",
                str(out_pdf),
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
                # mirrored margins: binding gutter inner, same 4.0in measure.
                # top+headsep tuned so the folio clears the 0.5in head floor
                # (production r3; was 0.37in) with ~a line of air below it
                "geometry:paperwidth=5.5in,paperheight=8.5in,"
                "inner=0.85in,outer=0.65in,top=0.8in,bottom=0.9in,"
                "headsep=0.18in",
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
                # graphicx explicitly: with all images inside raw
                # \bookplate calls, pandoc no longer auto-loads it
                "header-includes=\\usepackage{graphicx}"
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
                # production's "loudest LaTeX tell" twice running).
                # 8 lines reserved, not 4: the asterism alone fit in 4, but
                # a following \JEdate's own \needspace{4} then broke the
                # page, stranding the asterism at the foot (folios
                # 48/75/78/89/103 in the 138pp build, all journal units)
                "\\newcommand{\\scenebreak}{\\par\\needspace{8\\baselineskip}"
                "\\bigskip{\\centering*\\enspace*\\enspace*\\par}"
                "\\nobreak\\bigskip\\nobreak}"
                # title page: quiet letterspaced trade (A3 design pass,
                # variant A of scratch/title-variants — no rules; the
                # book's boundary grammar is whitespace, not furniture)
                "\\renewcommand{\\maketitle}{\\thispagestyle{empty}"
                "\\null\\vspace{0.16\\textheight}"
                "{\\centering{\\addfontfeatures{LetterSpace=18}"
                "\\fontsize{22}{27}\\selectfont WHITE BUFFALO\\par}"
                "\\vspace{1.4\\baselineskip}"
                "{\\addfontfeatures{LetterSpace=14}\\scshape a novella\\par}"
                "\\vspace{0.32\\textheight}"
                "{\\addfontfeatures{LetterSpace=8}\\large BEN COHEN "
                "\\normalsize\\itshape and \\large\\upshape DANIEL KLEIN\\par}"
                "\\vfill{\\addfontfeatures{LetterSpace=8}2026\\par}"
                "\\vspace{0.06\\textheight}}\\clearpage}"
                # the template's \frontmatter/\mainmatter would reset folios
                # at the notices; numbering is driven explicitly instead
                "\\renewcommand{\\frontmatter}{}\\renewcommand{\\mainmatter}{}"
                # front matter: half title (p.1), cover plate as
                # frontispiece facing the title (p.2), then \maketitle;
                # cover/half-title typography still a design pass
                # plate/text boundary is whitespace, not furniture:
                # \bookplate centers each cut on the measure (recto and
                # verso alike) with the codified air on both sides
                "\\newcommand{\\bookplate}[2]{\\par"
                "\\addvspace{18pt plus 4pt minus 2pt}"
                "{\\centering\\includegraphics[width=#1\\linewidth]{#2}\\par}"
                "\\addvspace{18pt plus 4pt minus 2pt}}"
                "\\AtBeginDocument{\\pagenumbering{gobble}"
                "\\thispagestyle{empty}\\null\\vspace{0.28\\textheight}"
                "{\\centering\\LARGE White Buffalo\\par}\\clearpage"
                "\\thispagestyle{empty}"
                "{\\centering\\includegraphics[height=0.95\\textheight]"
                "{build/plates/cover-tracks.png}\\par}\\clearpage}",
                "--include-after-body",
                str(after_body),
            ],
            check=True,
            cwd=ROOT,
        )

    # pass 1: build without the List of Illustrations to measure folios;
    # pass 2: insert the list into the front matter (folios unaffected)
    build_pdf(book_pdf_md, pdf, BUILD / "after-body.tex")
    folios = plate_folios(pdf)
    pdf_parts[0] = pdf_parts[0] + "\n\n" + illustrations_list(folios)
    book_pdf_md.write_text("\n\n".join(pdf_parts) + "\n")
    build_pdf(book_pdf_md, pdf, BUILD / "after-body.tex")
    print(f"{pdf.relative_to(ROOT)} written (plates at folios {folios})")

    # POD setting: same two-pass dance, its own folio geography
    pod_pdf = BUILD / "white-buffalo-pod.pdf"
    build_pdf(book_pod_md, pod_pdf, BUILD / "after-body-pod.tex")
    pod_folios = plate_folios(pod_pdf, pod=True)
    pod_parts[0] = pod_parts[0] + "\n\n" + illustrations_list(pod_folios)
    book_pod_md.write_text("\n\n".join(pod_parts) + "\n")
    build_pdf(book_pod_md, pod_pdf, BUILD / "after-body-pod.tex")
    print(f"{pod_pdf.relative_to(ROOT)} written (plates at folios {pod_folios})")

    epub = BUILD / "white-buffalo.epub"
    subprocess.run(
        [
            "pandoc",
            str(book_md),
            "-o",
            str(epub),
            *common,
            "--epub-cover-image",
            str(BUILD / "plates" / "cover-tracks.png"),
            "--toc",
            "--toc-depth=1",
        ],
        check=True,
        cwd=ROOT,
    )
    print(f"{epub.relative_to(ROOT)} written")


if __name__ == "__main__":
    main()
