#!/usr/bin/env python3
"""Citation anchor checker for White Buffalo.

Living documents cite draft lines as NN:LL (draft file prefix : line
number). Text revision shifts lines, so anchors rot silently. This tool
verifies each citation against the cited draft and reports or repairs
drift.

Method: the tokens around a citation (its parenthetical annotation or
surrounding clause) are scored against every line of the cited draft
using a 3-line rolling window; the best-scoring window locates where
the cited content actually lives now. Statuses:

  OK          best window within --tol lines of the cited anchor
  DRIFT       confident, unique match elsewhere (fix rewrites anchor;
              range end moves by the same delta)
  UNVERIFIED  annotation too thin or match not confident — check by
              hand or leave; these are reported, never rewritten
  DEAD        cited line beyond end of file

Run this on LIVING references only (catalog.toml, visual-bible,
timeline/geo ledgers, assembly). Never on logs (continuity, findings,
revision-stack, versions) — repairing a log's anchors falsifies the
record of what was true when it was written.

Usage:
  python3 check_citations.py FILE [FILE ...]          # report
  python3 check_citations.py --fix FILE [FILE ...]    # repair DRIFT
"""

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DRAFTS = {p.name[:2]: p for p in sorted((REPO / "drafts").glob("*.md"))}

CITE = re.compile(r"\b([0-2]\d):(\d{1,3})(?:[-–](\d{1,3}))?\b")
STOP = set(
    "the and with from that this they them their have been was were his her "
    "she him its into over only about when what which where whose after "
    "before then than also very more most some none each both against "
    "toward through".split()
)


def tokens(text: str) -> set:
    return {
        w for w in re.findall(r"[a-z']+", text.lower()) if len(w) >= 4 and w not in STOP
    }


def windows(lines):
    """Yield (center_lineno_1based, token_set) for 3-line rolling windows."""
    for i in range(len(lines)):
        lo, hi = max(0, i - 1), min(len(lines), i + 2)
        yield i + 1, tokens(" ".join(lines[lo:hi]))


def annotation_for(line: str, m: re.Match) -> str:
    """Context tokens for one citation.

    Preference order: (1) a parenthetical immediately FOLLOWING the
    citation ("08:61 (the stake)" — catalog style); (2) the enclosing
    parenthetical plus the clause before it ("the stake (08:61)" —
    prose style); (3) the whole line. Other citations stripped."""
    after = line[m.end() :]
    follow = re.match(r"\s*\(([^)]*)\)", after)
    if follow:
        return CITE.sub(" ", follow.group(1))
    lo = line.rfind("(", 0, m.start())
    hi = line.find(")", m.end())
    if lo != -1 and hi != -1:
        clause_start = max(
            line.rfind(".", 0, lo), line.rfind(";", 0, lo), line.rfind("|", 0, lo), 0
        )
        ctx = line[clause_start:lo] + " " + line[lo + 1 : hi]
    else:
        ctx = line
    return CITE.sub(" ", ctx)


def check_file(path: Path, tol: int, fix: bool):
    text = path.read_text()
    lines = text.splitlines()
    draft_windows = {}  # prefix -> list of (lineno, tokenset)
    results = []
    edits = []  # (old_str_span_in_line, ...) applied per line via re.sub

    for li, line in enumerate(lines):
        for m in CITE.finditer(line):
            prefix, anchor = m.group(1), int(m.group(2))
            rng_end = int(m.group(3)) if m.group(3) else None
            if prefix not in DRAFTS:
                continue
            dlines = DRAFTS[prefix].read_text().splitlines()
            if anchor > len(dlines):
                results.append(("DEAD", path.name, li + 1, m.group(0), None, 0))
                continue
            ann = tokens(annotation_for(line, m))
            if len(ann) < 2:
                results.append(("UNVERIFIED", path.name, li + 1, m.group(0), None, 0))
                continue
            if prefix not in draft_windows:
                draft_windows[prefix] = list(windows(dlines))
            scored = sorted(
                ((len(ann & wt), ln) for ln, wt in draft_windows[prefix]),
                reverse=True,
            )
            best_hits, best_ln = scored[0]
            second_hits = scored[1][0] if len(scored) > 1 else 0
            confident = best_hits >= max(2, round(0.4 * len(ann)))
            unique = best_hits > second_hits
            if abs(best_ln - anchor) <= tol and confident:
                results.append(
                    ("OK", path.name, li + 1, m.group(0), best_ln, best_hits)
                )
            elif confident and unique:
                delta = best_ln - anchor
                new = f"{prefix}:{best_ln}"
                if rng_end is not None:
                    new += f"-{rng_end + delta}"
                results.append(("DRIFT", path.name, li + 1, m.group(0), new, best_hits))
                # Thin annotations can match a rival near-duplicate
                # phrase (real case: "valley below" at both 19:9 and
                # 19:71); only rewrite on substantial evidence.
                if fix and best_hits >= 3:
                    edits.append((li, m.group(0), new))
            else:
                results.append(
                    ("UNVERIFIED", path.name, li + 1, m.group(0), best_ln, best_hits)
                )

    if fix and edits:
        for li, old, new in edits:
            lines[li] = lines[li].replace(old, new, 1)
        path.write_text("\n".join(lines) + ("\n" if text.endswith("\n") else ""))

    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+", type=Path)
    ap.add_argument("--fix", action="store_true")
    ap.add_argument("--tol", type=int, default=2)
    ap.add_argument("-q", "--quiet-ok", action="store_true", help="hide OK rows")
    args = ap.parse_args()

    totals = {}
    for path in args.files:
        for status, fname, lineno, cite, hint, hits in check_file(
            path, args.tol, args.fix
        ):
            totals[status] = totals.get(status, 0) + 1
            if status == "OK" and args.quiet_ok:
                continue
            extra = (
                f" -> {hint} ({hits} hits{', below fix bar' if hits < 3 else ''})"
                if status == "DRIFT"
                else (
                    f" (best guess {hint}, {hits} hits)"
                    if status == "UNVERIFIED" and hint
                    else ""
                )
            )
            print(f"{status:10} {fname}:{lineno}  {cite}{extra}")
    print("---", " ".join(f"{k}={v}" for k, v in sorted(totals.items())))
    if totals.get("DEAD"):
        sys.exit(1)


if __name__ == "__main__":
    main()
