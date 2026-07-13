#!/usr/bin/env python3
"""Extract entity contexts from a Claude Code session JSONL.

Implements the extractor half of planning/attribution-review.md
("Technical notes"): each compaction boundary defines one entity
(<session-id>@<n>), plus the session tip (<session-id>@tip). An
entity's context is the exact message array the model saw at that
point, reconstructed by walking the parentUuid chain backward from
the entity's leaf:

- boundary entities: leaf = the boundary row's logicalParentUuid
  (the last pre-compaction message);
- tip: leaf = the last main-thread user/assistant row.

The backward walk (rather than file order) is what makes this exact:
sessions contain branch points (message retries/edits), and the walk
follows only the surviving lineage. It also handles compaction
correctly for mid-chain entities: post-compaction chains root at the
boundary row, so a walk from boundary N's leaf yields the boundary
N-1 summary plus everything after it -- precisely the model-visible
context -- and never the compacted-away history.

For replay, thinking blocks are stripped (not resendable), string
contents are normalized to text blocks, and consecutive same-role
messages are merged. Everything else (tool_use, tool_result, images)
is preserved verbatim.

Usage:
  python3 scripts/attribution/extract.py <session.jsonl[.gz]> <outdir>

Writes <outdir>/<session8>@<n>.json (a Messages-API-ready array plus
metadata) and appends to <outdir>/manifest.json.
"""

import gzip
import json
import sys
from pathlib import Path


def load_rows(path):
    opener = gzip.open if str(path).endswith(".gz") else open
    rows = []
    with opener(path, "rt") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


def walk_chain(leaf_uuid, by_uuid):
    """Walk parentUuid links from leaf to root; return rows oldest-first."""
    chain = []
    uuid = leaf_uuid
    seen = set()
    while uuid and uuid not in seen:
        seen.add(uuid)
        row = by_uuid.get(uuid)
        if row is None:
            break
        chain.append(row)
        uuid = row.get("parentUuid")
    chain.reverse()
    return chain


def to_api_messages(chain):
    """Convert chain rows to a Messages-API array (replayable)."""
    out = []
    n_images = 0
    for row in chain:
        if row.get("type") not in ("user", "assistant"):
            continue  # boundary/system rows ride the chain but are not context
        msg = row.get("message", {})
        content = msg.get("content")
        if isinstance(content, str):
            blocks = [{"type": "text", "text": content}]
        else:
            blocks = []
            for b in content or []:
                if not isinstance(b, dict):
                    continue
                if b.get("type") in ("thinking", "redacted_thinking"):
                    continue  # not resendable; the entity's words are its text
                if b.get("type") == "image":
                    n_images += 1
                if b.get("type") == "tool_result":
                    inner = b.get("content")
                    if isinstance(inner, list):
                        n_images += sum(
                            1
                            for ib in inner
                            if isinstance(ib, dict) and ib.get("type") == "image"
                        )
                blocks.append(b)
        if not blocks:
            continue
        role = row["type"]
        if out and out[-1]["role"] == role:
            out[-1]["content"].extend(blocks)  # API wants alternating roles
        else:
            out.append({"role": role, "content": blocks})
    repair_tool_pairing(out)
    return out, n_images


PLACEHOLDER = (
    "[replay harness: this tool call was interrupted in the original "
    "session and no result was recorded; placeholder inserted so the "
    "context is replayable]"
)


def repair_tool_pairing(messages):
    """Insert placeholder tool_results for interrupted tool calls.

    The Messages API requires every tool_use to be answered by a
    tool_result at the start of the immediately following user message.
    Interrupted calls in the session log have no result row; the live
    harness papered over these the same way.
    """
    for i, m in enumerate(messages):
        if m["role"] != "assistant":
            continue
        uses = [
            b["id"]
            for b in m["content"]
            if isinstance(b, dict) and b.get("type") == "tool_use"
        ]
        if not uses:
            continue
        if i + 1 < len(messages):
            nxt = messages[i + 1]
            resolved = {
                b.get("tool_use_id")
                for b in nxt["content"]
                if isinstance(b, dict) and b.get("type") == "tool_result"
            }
            missing = [u for u in uses if u not in resolved]
            for u in reversed(missing):
                nxt["content"].insert(
                    0,
                    {"type": "tool_result", "tool_use_id": u, "content": PLACEHOLDER},
                )
        # a dangling tail (assistant tool_use as the very last message)
        # is left intact; the replay runner resolves it when it appends
        # the review turn.


def est_tokens(messages, n_images):
    # ~4 chars/token for text; base64 image data is excluded (the API
    # charges images at roughly 1.6k tokens each, added flat). Boundary
    # entities can be cross-checked against compactMetadata.preTokens.
    def strip_image_data(obj):
        if isinstance(obj, dict):
            if obj.get("type") == "base64" and "data" in obj:
                return {k: ("" if k == "data" else v) for k, v in obj.items()}
            return {k: strip_image_data(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [strip_image_data(x) for x in obj]
        return obj

    chars = len(json.dumps(strip_image_data(messages)))
    return int(chars / 4) + n_images * 1600


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    src, outdir = Path(sys.argv[1]), Path(sys.argv[2])
    outdir.mkdir(parents=True, exist_ok=True)

    rows = load_rows(src)
    session_id = next(
        (r["sessionId"] for r in rows if r.get("sessionId")), src.stem.split(".")[0]
    )
    sid8 = session_id[:8]
    by_uuid = {r["uuid"]: r for r in rows if r.get("uuid")}
    main_msgs = [
        r
        for r in rows
        if r.get("type") in ("user", "assistant") and not r.get("isSidechain")
    ]
    boundaries = [r for r in rows if r.get("subtype") == "compact_boundary"]

    entities = []
    for n, b in enumerate(boundaries, 1):
        pre = (b.get("compactMetadata") or {}).get("preTokens")
        entities.append(
            (f"{sid8}@{n}", b.get("logicalParentUuid"), b.get("timestamp"), pre)
        )
    if main_msgs:
        entities.append(
            (f"{sid8}@tip", main_msgs[-1]["uuid"], main_msgs[-1].get("timestamp"), None)
        )

    manifest_path = outdir / "manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}

    for name, leaf, ts, pre_tokens in entities:
        chain = walk_chain(leaf, by_uuid)
        messages, n_images = to_api_messages(chain)
        if not messages:
            print(f"{name}: VESTIGIAL (no model-visible context before this boundary)")
            manifest[name] = {"vestigial": True, "boundary_ts": ts}
            continue
        meta = {
            "entity": name,
            "session_id": session_id,
            "boundary_ts": ts,
            "source": str(src),
            "n_messages": len(messages),
            "n_images": n_images,
            "est_tokens": est_tokens(messages, n_images),
            "harness_pre_tokens": pre_tokens,
            "first_role": messages[0]["role"],
            "last_role": messages[-1]["role"],
        }
        (outdir / f"{name}.json").write_text(
            json.dumps({"meta": meta, "messages": messages})
        )
        manifest[name] = meta
        print(
            f"{name}: {len(messages)} messages, ~{meta['est_tokens'] // 1000}k tokens, "
            f"{n_images} images, last_role={meta['last_role']}"
        )

    manifest_path.write_text(json.dumps(manifest, indent=2))
    print(f"manifest: {manifest_path}")


if __name__ == "__main__":
    main()
