"""E-ext: do public benchmarks predict our own results? (prereg/eext-benchmarks.md)

    DOOR_DIR=... python bench/eext/run.py [run|report]

Free Workers AI models through the door's /ai, every model at its own
default thinking (`default_thinking: true`), temperature 0 and 4,096 tokens
(fixed by the door). Resumable: `run` spends at most DAILY neurons by its
own count, then stops; the next day's `run` continues where it stopped.
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "bench" / "boot"))
sys.path.insert(0, str(ROOT / "bench"))
import run as t2  # noqa: E402  (tasks, graders, code extraction, door URL)
from parallel import run_all  # noqa: E402

OUT = HERE / "results.json"
DAILY = 9000
INDEX = {  # AA Coding Index, frozen in the pre-registration
    "@cf/qwen/qwen3.8-27b": 68.1,
    "@cf/google/gemma-4-26b-a4b-it": 39.3,
    "@cf/nvidia/nemotron-3-120b-a12b": 37.7,
    "@cf/openai/gpt-oss-120b": 30.4,
    "@cf/meta/llama-3.3-70b-instruct-fp8-fast": 11.9,
    "@cf/meta/llama-4-scout-17b-16e-instruct": 8.2,
    "@cf/meta/llama-3.1-8b-instruct-fp8-fast": 5.4,
}
PROMPT = ("Write the Python module described below. Reply with exactly one fenced Python code block "
          "containing the complete module, and nothing else.\n\n")


def ai(model: str, text: str) -> dict:
    dd = Path(os.environ["DOOR_DIR"])
    body = {"model": model, "max_tokens": 4096, "default_thinking": True,
            "messages": [{"role": "user", "content": text}]}
    req = urllib.request.Request(t2.DOOR + "/ai", method="POST", data=json.dumps(body).encode(), headers={
        "content-type": "application/json", "user-agent": "polymechania-bench/1",
        "CF-Access-Client-Id": (dd / "cf_id").read_text().strip(),
        "CF-Access-Client-Secret": (dd / "cf_secret").read_text().strip(),
        "x-door-token": (dd / "door_token").read_text().strip()})
    last = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                return json.loads(r.read())
        except Exception as e:
            last = e
            time.sleep(10)
    return {"error": str(last)}


def today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def run() -> None:
    rows = json.loads(OUT.read_text()) if OUT.exists() else []
    have = {(r["model"], r["task"]) for r in rows}
    spent = sum(r["neurons"] for r in rows if r["day"] == today())
    todo = [(m, s, n, spec) for m in INDEX for s, n, spec in t2.tasks() if (m, n) not in have]
    print(f"{len(rows)} done, {len(todo)} to do; {spent:.0f} of {DAILY} neurons already spent today (UTC)")
    sol = HERE / "solutions"
    sol.mkdir(exist_ok=True)
    while todo and spent < DAILY:
        batch, todo = todo[:8], todo[8:]

        def one(job):
            m, s, n, spec = job
            out = ai(m, PROMPT + spec)
            msg = (out.get("choices") or [{}])[0].get("message", {}) if "choices" in out else {}
            text = msg.get("content") or out.get("response") or ""
            u = out.get("usage", {})
            path = sol / f"{m.split('/')[-1]}-{n}.py"
            path.write_text(t2.code_of({"content": [{"type": "text", "text": text}]}) if "```" in text else "")
            return {"model": m, "served": out.get("model"), "set": s, "task": n, "day": today(),
                    "error": out.get("error"), "finish": (out.get("choices") or [{}])[0].get("finish_reason"),
                    "output_tokens": u.get("completion_tokens"), "input_tokens": u.get("prompt_tokens"),
                    "neurons": u.get("neurons", 0) or 0, "length": len(text)}

        res = run_all(one, batch, workers=8)
        for r in res:
            p = sol / f"{r['model'].split('/')[-1]}-{r['task']}.py"
            r["grade"] = ("PASS" if t2.grade(r["set"], r["task"], p) == "PASS" else "FAIL") if not r["error"] else "ERROR"
        rows += [r for r in res if not r["error"]]  # errors are retried on the next run
        spent += sum(r["neurons"] for r in res)
        OUT.write_text(json.dumps(rows, indent=1) + "\n")
        print(f"  +{len(res)} ({sum(1 for r in res if r['error'])} errors), {spent:.0f} neurons today")
    print("stopped:", "all done" if not todo else "daily budget reached; run again after 00:00 UTC")


def ranks(xs: list) -> list:
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(xs):
        j = i
        while j + 1 < len(xs) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return r


def spearman(a: list, b: list) -> float:
    ra, rb = ranks(a), ranks(b)
    ma, mb = sum(ra) / len(ra), sum(rb) / len(rb)
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** 0.5
    return num / den if den else float("nan")


def kendall(a: list, b: list) -> tuple[float, int, int]:
    conc = disc = 0
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            s = (a[i] - a[j]) * (b[i] - b[j])
            conc += s > 0
            disc += s < 0
    n = len(a) * (len(a) - 1) / 2
    return (conc - disc) / n, conc, disc


def report() -> None:
    rows = json.loads(OUT.read_text())
    done = {m for m in INDEX if sum(r["model"] == m for r in rows) == 24}
    print(f"models complete: {len(done)} of {len(INDEX)}")
    table = []
    for m in INDEX:
        xs = [r for r in rows if r["model"] == m]
        p = sum(r["grade"] == "PASS" for r in xs)
        ph = sum(r["grade"] == "PASS" for r in xs if r["set"] == "hard")
        neu = sum(r["neurons"] for r in xs)
        served = sorted({r["served"] for r in xs if r.get("served")})
        table.append((m, INDEX[m], p, ph, len(xs), neu))
        print(f"{m:44} index {INDEX[m]:5}  pass {p:2}/{len(xs)}  hard {ph:2}  neurons {neu:7.0f}  "
              f"per pass {neu / max(p, 1):6.0f}  served {served}")
    if len(done) == len(INDEX):
        idx = [t[1] for t in table]
        print(f"Spearman (index vs pass/24): {spearman(idx, [t[2] for t in table]):.3f}; predicts: "
              f"{spearman(idx, [t[2] for t in table]) >= 0.714}")
        print(f"Spearman (index vs hard pass/12): {spearman(idx, [t[3] for t in table]):.3f}")
        tau, c, d = kendall(idx, [t[2] for t in table])
        print(f"Kendall tau {tau:.3f}; pairs ordered the same {c} of 21, opposite {d}, tied {21 - c - d}")


if __name__ == "__main__":
    {"run": run, "report": report}[(sys.argv[1:] or ["report"])[0]]()
