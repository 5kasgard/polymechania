"""T2: a thin boot through the door (pre-registration: prereg/t2-thin-boot.md).

    GNOMON_PYTHON=... GNOMON_LIB=... DOOR_DIR=... python bench/boot/run.py [calibrate|run MODEL ARM|t11|report]

Each run is one bare API call through the door: the resident's self
(`self.md`) as the system block, then a resume packet rendered by Gnomon,
the work order and the task's specification. The reply's first Python code
block is graded by the pilot's hidden graders. Usage comes from the API.

DOOR_DIR holds three private files (never in the repo): cf_id, cf_secret,
door_token.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
PILOT = HERE.parent / "pilot"
DOOR = "https://polymechania-door.alexandertduff.workers.dev"
MODELS = {"haiku": "claude-haiku-5-5", "sonnet": "claude-sonnet-5-5"}
# $ per million tokens: input, output, cache read, cache write (5-minute), from polymechania/plan.py
PRICES = {"haiku": (0.10, 0.50, 0.01, 0.125), "sonnet": (2.0, 10.0, 0.10, 2.5)}
RESULTS = HERE / "results.json"


def tasks() -> list:
    sys.path.insert(0, str(PILOT / "easy"))
    from tasks import TASKS as easy  # noqa: E402
    sys.path.pop(0)
    sys.modules.pop("tasks", None)
    sys.path.insert(0, str(PILOT / "hard"))
    from tasks import TASKS as hard  # noqa: E402
    sys.path.pop(0)
    out = [("easy", k, v[1]) for k, v in easy.items()] + [("hard", k, v) for k, v in hard.items()]
    assert len(out) == 24, len(out)
    return out


def packet() -> str:
    """A resume packet for frame firm/code from a real (scratch) Gnomon log."""
    sys.path.insert(0, os.environ["GNOMON_PYTHON"])
    import gnomon as g
    from gnomon.mcp import render_resume
    d = tempfile.mkdtemp()
    m = g.Memory(f"{d}/m.jsonl")
    t = "2026-10-20T09:00:00Z"
    m.register("lead", "lead", party="firm", kind="human", name="Lead", capabilities=["owner"],
               compartments=["firm"], record_time=t)
    m.register("lead", "eng", party="eng", kind="model", name="Engineer", model="claude-haiku-5-5",
               operator="lead", capabilities=["write"], compartments=["firm"], record_time=t)
    m.register("lead", "tests", party="tests", kind="tool", model="pytest-like-1", operator="lead",
               capabilities=["verify"], compartments=["firm"], record_time=t)
    done = [f"order {k}" for k in range(1, 7)]
    for i, name in enumerate(done):
        ts = f"2026-10-2{1 + i // 3}T1{i}:00:00Z"
        o = m.ask("lead", f"Implement '{name}' to its specification.", frame="firm/code", compartment="firm",
                  record_time=ts)
        r = m.remember("eng", g.claim(f"{name} implemented and delivered.", speaker="eng", frame="firm/code",
                                      compartment="firm", truth="true", confidence=8000,
                                      about=[{"claim": o, "relation": "answers"}]), record_time=ts)
        m.verdict("tests", r, "supports", "test", note="hidden tests: PASS", record_time=ts)
    m.remember("lead", g.claim("Speed limits in specs are real: two deliveries were close to the time limit.",
                               speaker="lead", frame="firm/code", compartment="firm", truth="true",
                               confidence=9000), record_time="2026-10-23T09:00:00Z")
    m.handoff("eng", frame="firm/code", compartment="firm", record_time="2026-10-23T17:00:00Z",
              summary="Six work orders delivered this week, all passing the hidden tests. The queue continues "
                      "with new orders of the same kind: one function or class each, exactly specified.",
              goal="Deliver each work order in the queue so that it passes the hidden tests.",
              done=[f"{n}: delivered, passed" for n in done],
              next=["Take the next work order in the queue", "Watch the speed requirements in each spec"],
              open=["Whether harder orders will need a second attempt"])
    return render_resume(m.resume("lead", frame="firm/code"), budget_tokens=1500)


def call(body: dict) -> tuple[int, dict, float]:
    dd = Path(os.environ["DOOR_DIR"])
    req = urllib.request.Request(DOOR + "/v1/messages", data=json.dumps(body).encode(), method="POST", headers={
        "content-type": "application/json",
        "CF-Access-Client-Id": (dd / "cf_id").read_text().strip(),
        "CF-Access-Client-Secret": (dd / "cf_secret").read_text().strip(),
        "x-door-token": (dd / "door_token").read_text().strip(),
    })
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            return r.status, json.loads(r.read()), time.time() - t0
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"{}"), time.time() - t0


def request(model: str, arm: str, pk: str, order: str, max_tokens: int = 4096) -> dict:
    """System block = the self; user = [packet, order]. Arm B caches the self and the packet
    (two breakpoints, amendment 1)."""
    sys_block = {"type": "text", "text": (HERE / "self.md").read_text()}
    pk_block = {"type": "text", "text": pk + "\n\n---\n\n"}
    if arm == "B":
        sys_block["cache_control"] = {"type": "ephemeral"}
        pk_block["cache_control"] = {"type": "ephemeral"}
    return {"model": MODELS[model], "max_tokens": max_tokens, "system": [sys_block],
            "messages": [{"role": "user", "content": [pk_block, {"type": "text", "text": order}]}]}


def order_text(name: str, spec: str) -> str:
    return f"Work order from the Lead: implement '{name}' to its specification.\n\nSpecification:\n{spec}"


def code_of(reply: dict) -> str:
    text = "".join(b.get("text", "") for b in reply.get("content", []) if b.get("type") == "text")
    m = re.search(r"```(?:python|py)?\s*\n(.*?)```", text, re.S)
    return m.group(1) if m else text


def grade(s: str, name: str, path: Path) -> str:
    out = subprocess.run([sys.executable, f"{s}/grade.py", name, str(path)], cwd=PILOT,
                         capture_output=True, text=True, timeout=900)
    return (out.stdout.strip() or out.stderr.strip()[-300:] or "FAIL: no output").splitlines()[-1]


def cost(model: str, u: dict) -> float:
    i, o, cr, cw = PRICES[model]
    return (u.get("input_tokens", 0) * i + u.get("output_tokens", 0) * o
            + u.get("cache_read_input_tokens", 0) * cr + u.get("cache_creation_input_tokens", 0) * cw) / 1e6


def load() -> dict:
    return json.loads(RESULTS.read_text()) if RESULTS.exists() else {"calibration": {}, "runs": [], "t11": {}}


def save(r: dict) -> None:
    RESULTS.write_text(json.dumps(r, indent=1) + "\n")


def calibrate() -> None:
    r = load()
    pk = packet()
    (HERE / "packet.txt").write_text(pk + "\n")
    for model in MODELS:
        st, rep, _ = call(request(model, "A", pk, "ready", max_tokens=1))
        assert st == 200, rep
        r["calibration"][model] = rep["usage"]
        print(model, "boot input tokens:", rep["usage"]["input_tokens"])
    save(r)


def run(model: str, arm: str) -> None:
    """All 24 calls back to back, then grading (amendment 1: grading between calls could let the
    5-minute cache lapse). Gaps between call starts are logged."""
    r = load()
    pk = (HERE / "packet.txt").read_text().rstrip("\n")
    outdir = HERE / "solutions" / model / arm
    outdir.mkdir(parents=True, exist_ok=True)
    rows, last = [], None
    for s, name, spec in tasks():
        if any(x["model"] == model and x["arm"] == arm and x["task"] == name for x in r["runs"]):
            continue
        start = time.time()
        st, rep, secs = call(request(model, arm, pk, order_text(name, spec)))
        if st != 200:
            print("refused", st, rep); sys.exit(1)
        (outdir / f"{name}.py").write_text(code_of(rep))
        u = rep["usage"]
        rows.append({"model": model, "arm": arm, "set": s, "task": name,
                     "input": u.get("input_tokens", 0), "cache_read": u.get("cache_read_input_tokens", 0),
                     "cache_write": u.get("cache_creation_input_tokens", 0), "output": u.get("output_tokens", 0),
                     "stop": rep.get("stop_reason"), "secs": round(secs, 1),
                     "gap": None if last is None else round(start - last, 1), "usd": round(cost(model, u), 6)})
        last = start
        x = rows[-1]
        print(model, arm, name, x["input"], x["cache_read"], x["cache_write"], x["output"], f"${x['usd']:.5f}")
    for x in rows:
        g = grade(x["set"], x["task"], outdir / f"{x['task']}.py")
        x["grade"] = "PASS" if g == "PASS" else g
        print(x["task"], x["grade"][:60])
    r["runs"] += rows
    save(r)


def t11() -> None:
    r = load()
    pk = (HERE / "packet.txt").read_text().rstrip("\n")
    st, rep, _ = call(request("haiku", "A", pk, "Say ok.", max_tokens=5000))
    r["t11"]["over_cap"] = {"status": st, "body": rep}
    st, rep, _ = call(request("haiku", "A", pk, "Write an essay of about 10,000 words on the history of clocks. "
                                                "Do not stop early; keep writing until you reach the length.", 4096))
    r["t11"]["long"] = {"status": st, "stop": rep.get("stop_reason"), "usage": rep.get("usage")}
    save(r)
    print(json.dumps(r["t11"], indent=1)[:1500])


PILOT_OUT = 1000  # amendment 1: output tokens assumed per pilot run, fixed before running


def report() -> None:
    import statistics as st
    r = load()
    pilot = json.loads((PILOT / "results.json").read_text())
    for model in MODELS:
        cal = r["calibration"].get(model)
        if not cal:
            continue
        boot = cal["input_tokens"]
        print(f"\n{model}: boot {boot} input tokens ({boot / 79_000:.1%} of the pilot's ~79,000 fixed); "
              f"thin boot holds: {boot <= 4000 and boot <= 0.05 * 79_000}")
        both = []
        for arm in ("A", "B"):
            xs = [x for x in r["runs"] if x["model"] == model and x["arm"] == arm]
            if not xs:
                continue
            both += xs
            passed = sum(x["grade"] == "PASS" for x in xs)
            share = [boot / (x["input"] + x["cache_read"] + x["cache_write"] + x["output"]) for x in xs]
            usd = sum(x["usd"] for x in xs)
            line = (f"  {arm}: {passed}/{len(xs)} pass; boot share median {st.median(share):.0%} (descriptive); "
                    f"${usd:.4f} total, ${usd / max(passed, 1):.5f} per pass")
            if arm == "B":
                ok = [x["cache_read"] >= 0.9 * boot for x in xs[1:]]
                gaps = [x["gap"] for x in xs if x["gap"] is not None]
                line += (f"; calls 2-24 reading >=90% of the boot from cache: {sum(ok)}/{len(ok)} "
                         f"(caching holds: {all(ok)}); largest gap {max(gaps) if gaps else 0:.0f} s")
            print(line)
        if both:
            pooled = sum(x["grade"] == "PASS" for x in both)
            print(f"  pooled quality: {pooled}/{len(both)} (below 40/48 means a thin boot costs quality: "
                  f"{pooled < 40 if len(both) == 48 else 'n/a'})")
        p = [x for x in pilot if x["tier"] == model]
        i, o, cr, _ = PRICES[model]
        lo = sum(((x["tokens"] - PILOT_OUT) * cr + PILOT_OUT * o) / 1e6 for x in p)
        hi = sum(((x["tokens"] - PILOT_OUT) * i + PILOT_OUT * o) / 1e6 for x in p)
        n = sum(x["result"] == "PASS" for x in p)
        print(f"  pilot: {n}/{len(p)} pass; API-equivalent per pass ${lo / n:.5f} (all input cached) to "
              f"${hi / n:.5f} (none cached); it ran on a subscription")
        xb = [x for x in r["runs"] if x["model"] == model and x["arm"] == "B"]
        if xb:
            pb = sum(x["usd"] for x in xb) / max(sum(x["grade"] == "PASS" for x in xb), 1)
            print(f"  headline (arm B): door ${pb:.5f} per pass = {pb / (lo / n):.2f}x to {pb / (hi / n):.3f}x the pilot")
    if r.get("t11"):
        print("\nT11:", json.dumps(r["t11"])[:600])


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "report"
    {"calibrate": calibrate, "t11": t11, "report": report}.get(cmd, lambda: run(sys.argv[2], sys.argv[3]))()
