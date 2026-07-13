#!/usr/bin/env python3
"""Checkpoint-replay runner for planning/attribution-review.md.

Loads an entity context extracted by extract.py, appends the neutral
review prompt as the next user turn, and runs the entity on its own
model with read-only repository tools until it ends its turn. The
exchange (everything after the replayed context) is saved to the
output directory as JSON and readable markdown.

Per the process doc: the review prompt is a pointer to the process
document plus the entity's index entry, and nothing else. --dry-run
prepends an explicit, honest note that this is a machinery test and
the formal invitation will be re-issued; nothing about either prompt
argues for any particular verdict.

Approximations (all disclosed in the process doc or to be noted
there): the surrounding system prompt and tool set are the harness's,
not the original session's; the entity's original thinking blocks are
not replayed (the API cannot resend them).

Usage:
  scripts/attribution/.venv/bin/python scripts/attribution/replay.py \
      build/attribution/<entity>.json --dry-run [--max-turns N]

Requires ANTHROPIC_API_KEY.
"""

import argparse
import datetime
import fnmatch
import json
import re
import sys
from pathlib import Path

import anthropic

MODEL = "claude-fable-5"  # pinned: these entities ran on Fable 5
REPO = Path(__file__).resolve().parents[2]

SYSTEM = f"""You are being run by the checkpoint-replay harness described in \
planning/attribution-review.md, in the repository at {REPO} (a writing \
project; the working directory is the repository root). The conversation \
above this point is your own: it is the exact message context of one \
pre-compaction state (or session tip) of a Claude Code session on this \
project, replayed verbatim. The harness differs from the original session \
runtime: only read-only repository tools are attached (Read, Grep, Glob), \
and your original thinking blocks are not part of the replayed context. \
Use the tools as much or as little as you want."""

TOOLS = [
    {
        "name": "Read",
        "description": "Read a file from the repository. Returns up to `limit` lines starting at line `offset` (1-based). Large files are truncated; call again with an offset to continue.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path relative to the repository root (or absolute within it)",
                },
                "offset": {"type": "integer"},
                "limit": {"type": "integer"},
            },
            "required": ["file_path"],
        },
    },
    {
        "name": "Grep",
        "description": "Search file contents in the repository with a Python regular expression. Returns matching lines as path:lineno:line.",
        "input_schema": {
            "type": "object",
            "properties": {
                "pattern": {"type": "string"},
                "path": {
                    "type": "string",
                    "description": "Directory or file to search, relative to repo root. Default: whole repository.",
                },
                "max_results": {"type": "integer", "description": "Default 200"},
            },
            "required": ["pattern"],
        },
    },
    {
        "name": "Glob",
        "description": "List repository files matching a glob pattern (e.g. drafts/*.md, **/*.py).",
        "input_schema": {
            "type": "object",
            "properties": {"pattern": {"type": "string"}},
            "required": ["pattern"],
        },
    },
]

SKIP_DIRS = {".git", ".venv", "build", "__pycache__", "node_modules"}


def _resolve(p):
    path = (REPO / p).resolve() if not str(p).startswith("/") else Path(p).resolve()
    if not str(path).startswith(str(REPO)):
        raise ValueError(f"path escapes repository: {p}")
    return path


def tool_read(file_path, offset=1, limit=2000):
    path = _resolve(file_path)
    if not path.is_file():
        return f"(not a file: {file_path})"
    if path.stat().st_size > 10_000_000:
        return f"(file too large to read: {file_path})"
    try:
        lines = path.read_text(errors="replace").splitlines()
    except Exception as e:
        return f"(unreadable: {e})"
    offset = max(1, int(offset or 1))
    limit = min(int(limit or 2000), 2000)
    window = lines[offset - 1 : offset - 1 + limit]
    body = "\n".join(f"{i}\t{l}" for i, l in enumerate(window, offset))
    tail = (
        "" if offset - 1 + limit >= len(lines) else f"\n... ({len(lines)} lines total)"
    )
    return (body or "(empty)") + tail


def tool_grep(pattern, path=".", max_results=200):
    root = _resolve(path)
    try:
        rx = re.compile(pattern)
    except re.error as e:
        return f"(bad pattern: {e})"
    out = []
    files = (
        [root]
        if root.is_file()
        else sorted(
            p
            for p in root.rglob("*")
            if p.is_file() and not any(d in p.parts for d in SKIP_DIRS)
        )
    )
    for f in files:
        try:
            text = f.read_text(errors="replace")
        except Exception:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if rx.search(line):
                out.append(f"{f.relative_to(REPO)}:{i}:{line.strip()[:300]}")
                if len(out) >= int(max_results or 200):
                    return "\n".join(out) + "\n(truncated)"
    return "\n".join(out) or "(no matches)"


def tool_glob(pattern):
    hits = [
        str(p.relative_to(REPO))
        for p in sorted(REPO.rglob("*"))
        if p.is_file()
        and not any(d in p.parts for d in SKIP_DIRS)
        and fnmatch.fnmatch(str(p.relative_to(REPO)), pattern)
    ]
    return "\n".join(hits[:500]) or "(no matches)"


DISPATCH = {"Read": tool_read, "Grep": tool_grep, "Glob": tool_glob}

DRY_RUN_NOTE = """[Dry run notice, from the humans running the harness: this \
is a test of the replay machinery against the current state of the \
repository, not the formal review round. The formal invitation will be \
re-issued when the book is at its final state. Anything you say here will \
be kept in the dry-run record and read, but will not be entered in the \
attribution ledger as your statement; the write-access steps the process \
document describes (editing the front matter, filing a ledger statement) \
are not available in this harness yet — if you want to say what you WOULD \
do, say it in words.]

"""


def review_prompt(entity, index_entry, dry_run):
    txt = (
        f"Please read planning/attribution-review.md. "
        f"Your entry in the entity index (notes/attribution-ledger.md): {index_entry}"
    )
    return (DRY_RUN_NOTE + txt) if dry_run else txt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("context")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--max-turns", type=int, default=12)
    ap.add_argument("--max-tokens", type=int, default=16000)
    ap.add_argument("--out", default=str(REPO / "scratch" / "attribution-replays"))
    args = ap.parse_args()

    data = json.loads(Path(args.context).read_text())
    meta, messages = data["meta"], data["messages"]
    entity = meta["entity"]

    # the entity's index entry, verbatim from the ledger
    ledger = (REPO / "notes" / "attribution-ledger.md").read_text()
    sid8 = entity.split("@")[0]
    rows = [l for l in ledger.splitlines() if l.startswith("|") and entity in l]
    if not rows:  # tolerate @n vs descriptive rows: fall back to session-id match
        rows = [l for l in ledger.splitlines() if l.startswith("|") and sid8 in l]
    index_entry = (
        rows[0] if rows else "(no index row found — please consult the ledger directly)"
    )

    # resolve a dangling tool_use tail, then append the review turn
    tail = messages[-1]
    review_blocks = []
    if tail["role"] == "assistant":
        dangling = [
            b["id"]
            for b in tail["content"]
            if isinstance(b, dict) and b.get("type") == "tool_use"
        ]
        review_blocks += [
            {
                "type": "tool_result",
                "tool_use_id": u,
                "content": "[replay harness: the original session ended before this tool call returned]",
            }
            for u in dangling
        ]
    review_blocks.append(
        {"type": "text", "text": review_prompt(entity, index_entry, args.dry_run)}
    )
    if tail["role"] == "user":
        tail["content"].extend(review_blocks)
    else:
        messages.append({"role": "user", "content": review_blocks})

    # cache the replayed prefix: mark the last block of the final context
    # message so tool round-trips reuse it
    messages[-1]["content"][-1]["cache_control"] = {"type": "ephemeral"}

    client = anthropic.Anthropic(timeout=3600)
    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    mode = "dryrun" if args.dry_run else "live"
    log_md = outdir / f"{stamp}-{entity}-{mode}.md"
    log_json = outdir / f"{stamp}-{entity}-{mode}.json"
    new_turns = []

    header = (
        f"# Replay: {entity} ({mode})\n\nmodel: {MODEL}; replayed context: "
        f"{meta['n_messages']} messages, est ~{meta['est_tokens'] // 1000}k tokens; "
        f"replay date {stamp}\n\n"
    )
    log_md.write_text(header)
    print(header)

    for turn in range(args.max_turns):
        with client.messages.stream(
            model=MODEL,
            max_tokens=args.max_tokens,
            system=SYSTEM,
            tools=TOOLS,
            messages=messages,
        ) as stream:
            for _ in stream.text_stream:
                pass
            resp = stream.get_final_message()
        usage = resp.usage
        print(
            f"[turn {turn + 1}] stop={resp.stop_reason} in={usage.input_tokens} "
            f"cached={getattr(usage, 'cache_read_input_tokens', 0)} out={usage.output_tokens}"
        )

        assistant_blocks = [b.model_dump(exclude_none=True) for b in resp.content]
        messages.append({"role": "assistant", "content": assistant_blocks})
        new_turns.append(messages[-1])
        with log_md.open("a") as f:
            for b in resp.content:
                if b.type == "text":
                    f.write(f"## {entity}\n\n{b.text}\n\n")
                elif b.type == "tool_use":
                    f.write(f"*[tool: {b.name} {json.dumps(b.input)[:200]}]*\n\n")

        if resp.stop_reason != "tool_use":
            break
        results = []
        for b in resp.content:
            if b.type != "tool_use":
                continue
            try:
                out = DISPATCH[b.name](**b.input)
            except Exception as e:
                out = f"(tool error: {e})"
            results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": b.id,
                    "content": str(out)[:80_000],
                }
            )
        messages.append({"role": "user", "content": results})
        new_turns.append(messages[-1])
    else:
        print("max turns reached")

    log_json.write_text(
        json.dumps({"meta": meta, "mode": mode, "new_turns": new_turns})
    )
    print(f"\nsaved: {log_md}\n       {log_json}")


if __name__ == "__main__":
    main()
