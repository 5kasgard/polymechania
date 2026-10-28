"""T2c: effort and capped thinking on Haiku (prereg/t2c-effort.md).

    DOOR_DIR=... python bench/boot/t2c.py [run|report]

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

OUT = HERE / "t2c_results.json"
ARMS = {"L": ({"type": "adaptive"}, {"effort": "low"}), "DL": ({"type": "disabled"}, {"effort": "low"})}


def go() -> None:
    pk = (HERE / "packet.txt").read_text().rstrip("\n")
    hard = [t for t in t2.tasks() if t[0] == "hard"]
    rows = []
    for arm, (thinking, output_config) in ARMS.items():
        outdir = HERE / "solutions" / "haiku" / arm
        outdir.mkdir(parents=True, exist_ok=True)
        batch, last = [], None
        for s, name, spec in hard:
            body = t2.request("haiku", "B", pk, t2.order_text(name, spec))
            body["thinking"] = thinking
            body["output_config"] = output_config
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
    d = [x for x in json.loads((HERE / "t2b_results.json").read_text()) if x["arm"] == "D"]
    res = {"D": (sum(x["grade"] == "PASS" for x in d), sum(x["usd"] for x in d))}
    print(f"T2 arm B (adaptive, medium default): 10/12 pass, 2 empty, $0.0126 (from T2)")
    print(f"T2b D (disabled, medium): {res['D'][0]}/12 pass, $ {res['D'][1]:.4f}")
    for arm in ARMS:
        xs = [x for x in rows if x["arm"] == arm]
        if not xs:
            print(f"{arm}: not run"); continue
        p = sum(x["grade"] == "PASS" for x in xs); usd = sum(x["usd"] for x in xs)
        res[arm] = (p, usd)
        print(f"{arm}: {p}/12 pass, {sum(x['empty'] for x in xs)} empty, ${usd:.4f}, thinking tokens "
              f"{sum(x['thinking'] or 0 for x in xs)}, max_tokens stops {sum(x['stop'] == 'max_tokens' for x in xs)}, "
              f"output tokens {sum(x['output'] for x in xs)}")
    if any(x["arm"] == "L" for x in rows):
        print("low effort avoids the empties:", not any(x["empty"] for x in rows if x["arm"] == "L"))
    print("setting for resident runs on Haiku (direction):", max(res, key=lambda a: (res[a][0], -res[a][1])))


if __name__ == "__main__":
    (go if (sys.argv[1:] or ["report"])[0] == "run" else report)()
