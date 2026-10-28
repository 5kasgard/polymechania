"""T2b: thinking and Haiku's empty answers (prereg/t2b-thinking.md).

    DOOR_DIR=... python bench/boot/t2b.py [run|report]

Reuses T2's runner: the same self, packet, cache breakpoints and graders;
only the `thinking` field changes. Results go to t2b_results.json.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run as t2  # noqa: E402

OUT = HERE / "t2b_results.json"
ARMS = {"D": {"type": "disabled"}, "E": {"type": "enabled", "budget_tokens": 2048}}


def go() -> None:
    pk = (HERE / "packet.txt").read_text().rstrip("\n")
    hard = [t for t in t2.tasks() if t[0] == "hard"]
    rows = []
    for arm, thinking in ARMS.items():
        outdir = HERE / "solutions" / "haiku" / arm
        outdir.mkdir(parents=True, exist_ok=True)
        batch, last = [], None
        for s, name, spec in hard:
            body = t2.request("haiku", "B", pk, t2.order_text(name, spec))
            body["thinking"] = thinking
            start = time.time()
            st, rep, secs = t2.call(body)
            if st != 200:
                print("refused", arm, name, st, rep)
                sys.exit(1)
            (outdir / f"{name}.py").write_text(t2.code_of(rep))
            u = rep["usage"]
            batch.append({"arm": arm, "set": s, "task": name,
                          "input": u.get("input_tokens", 0), "cache_read": u.get("cache_read_input_tokens", 0),
                          "cache_write": u.get("cache_creation_input_tokens", 0), "output": u.get("output_tokens", 0),
                          "thinking": (u.get("output_tokens_details") or {}).get("thinking_tokens"),
                          "blocks": [b.get("type") for b in rep.get("content", [])],
                          "stop": rep.get("stop_reason"), "secs": round(secs, 1),
                          "gap": None if last is None else round(start - last, 1),
                          "usd": round(t2.cost("haiku", u), 6)})
            last = start
            x = batch[-1]
            print(arm, name, x["output"], "thinking", x["thinking"], x["blocks"], x["stop"])
        for x in batch:
            g = t2.grade(x["set"], x["task"], outdir / f"{x['task']}.py")
            x["grade"] = "PASS" if g == "PASS" else g
            x["empty"] = (outdir / f"{x['task']}.py").stat().st_size == 0
            print(arm, x["task"], x["grade"][:60])
        rows += batch
        OUT.write_text(json.dumps(rows, indent=1) + "\n")


def report() -> None:
    rows = json.loads(OUT.read_text())
    t2rows = [x for x in json.loads(t2.RESULTS.read_text())["runs"]
              if x["model"] == "haiku" and x["arm"] == "B" and x["set"] == "hard"]
    base_pass = sum(x["grade"] == "PASS" for x in t2rows)
    base_empty = sum((HERE / "solutions" / "haiku" / "B" / f"{x['task']}.py").stat().st_size == 0 for x in t2rows)
    print(f"T2 arm B (default thinking), hard tasks: {base_pass}/12 pass, {base_empty} empty, "
          f"${sum(x['usd'] for x in t2rows):.4f}")
    res = {}
    for arm in ARMS:
        xs = [x for x in rows if x["arm"] == arm]
        if not xs:
            print(f"{arm}: not run (see T2B_RESULTS.md)")
            continue
        p = sum(x["grade"] == "PASS" for x in xs)
        e = sum(x["empty"] for x in xs)
        usd = sum(x["usd"] for x in xs)
        th = [x["thinking"] or 0 for x in xs]
        res[arm] = (p, usd)
        print(f"{arm}: {p}/12 pass, {e} empty, ${usd:.4f}, thinking tokens total {sum(th)}, "
              f"max_tokens stops {sum(x['stop'] == 'max_tokens' for x in xs)}")
    d_empty = sum(x["empty"] for x in rows if x["arm"] == "D")
    print("thinking caused the empties:", base_empty >= 2 and d_empty == 0)
    best = max(res, key=lambda a: (res[a][0], -res[a][1]))
    print("default for resident runs on Haiku:", best)


if __name__ == "__main__":
    (go if (sys.argv[1:] or ["report"])[0] == "run" else report)()
