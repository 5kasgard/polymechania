"""Render queue.json (the one queue of open work) as docs/queue.md, and check it.

    python bench/workqueue.py           # render and check
    python bench/workqueue.py --check   # check only (CI)

Order: what can run now first, by value, then cost; then what waits on the
owner or people; then blocked, scheduled and parked items. Checks: unique
ids, known fields and values, blockers that exist, no cycles.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
Q = ROOT / "queue.json"
OUT = ROOT / "docs" / "queue.md"
KINDS = {"test", "build", "fix", "doc", "infra", "decision"}
STATUS = {"open", "in-progress", "blocked", "waiting-owner", "scheduled", "parked", "done"}
NEEDS = {"free", "api", "pro", "owner", "people"}
VALUE = {"high": 0, "medium": 1, "low": 2}


def check(items: list) -> list:
    errs, ids = [], [i["id"] for i in items]
    if len(ids) != len(set(ids)):
        errs.append("duplicate ids")
    byid = {i["id"]: i for i in items}
    for i in items:
        for f, allowed in (("kind", KINDS), ("status", STATUS), ("needs", NEEDS), ("value", set(VALUE))):
            if i.get(f) not in allowed:
                errs.append(f"{i['id']}: bad {f} {i.get(f)!r}")
        for b in i.get("blocked_by", []):
            if b not in byid:
                errs.append(f"{i['id']}: blocked by unknown {b}")
        if not i.get("next"):
            errs.append(f"{i['id']}: no next step")
    for i in items:  # cycles
        seen, stack = set(), list(i.get("blocked_by", []))
        while stack:
            b = stack.pop()
            if b == i["id"]:
                errs.append(f"{i['id']}: blocked by itself through a cycle")
                break
            if b in seen or b not in byid:
                continue
            seen.add(b)
            stack += byid[b].get("blocked_by", [])
    return errs


def ready(i, byid) -> bool:
    return i["status"] in ("open", "in-progress") and all(
        byid[b]["status"] == "done" for b in i.get("blocked_by", []))


def render(q: dict) -> str:
    items = [i for i in q["items"] if i["status"] != "done"]
    byid = {i["id"]: i for i in q["items"]}
    groups = [
        ("Can run now", [i for i in items if ready(i, byid)]),
        ("Waiting on a blocker", [i for i in items if i["status"] in ("open", "in-progress", "blocked") and not ready(i, byid)]),
        ("Needs the owner", [i for i in items if i["status"] == "waiting-owner"]),
        ("Scheduled", [i for i in items if i["status"] == "scheduled"]),
        ("Parked", [i for i in items if i["status"] == "parked"]),
    ]
    out = [f"# The queue ({q['updated']})", "",
           "Generated from `queue.json` by `python bench/workqueue.py`; edit the JSON, not this file.", ""]
    total = sum(i.get("cost", 0) for i in items)
    out.append(f"{len(items)} open items; API cost if all ran: about ${total:.2f}.")
    out.append("")
    for name, xs in groups:
        if not xs:
            continue
        xs.sort(key=lambda i: (VALUE[i["value"]], i.get("cost", 0), i["id"]))
        out += [f"## {name} ({len(xs)})", "", "| | Item | Value | Needs | $ | Next step |", "|---|---|---|---|---|---|"]
        for i in xs:
            blk = f" (after {', '.join(i['blocked_by'])})" if i.get("blocked_by") else ""
            out.append(f"| {i['id']} | {i['title']} | {i['value']} | {i['needs']} | {i.get('cost', 0):g} | {i['next']}{blk} |")
        out.append("")
    return "\n".join(out)


if __name__ == "__main__":
    q = json.loads(Q.read_text())
    errs = check(q["items"])
    if errs:
        print("queue.json problems:\n" + "\n".join(errs))
        sys.exit(1)
    if "--check" not in sys.argv:
        OUT.write_text(render(q))
        print(f"wrote {OUT.relative_to(ROOT)}")
    print(f"queue ok: {len(q['items'])} items")
