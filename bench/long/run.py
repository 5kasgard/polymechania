"""T1 runner: run shapes on long work (prereg/t1-long.md).

    DOOR_DIR=... python bench/long/run.py run [--models gemma llama qwen] [--dry] [--out DIR]
    python bench/long/run.py report [--out DIR]

Arms: C (one conversation), B (fresh call: own previous module + notes + this
round's change), BV (B plus the failures of earlier, still-active tests on the
previous module), SR (fresh call from the reference module of the round
before). Six tasks x five rounds x four arms x three models, one attempt per
round. Resumable: results go to DIR/results.json after every round, modules
to DIR/solutions/<model>/<arm>/<task>-r<k>.py (and the raw reply beside it as
.txt, which C and the notes need to resume). `--dry` uses a fake model that
returns the reference module and writes to a temporary folder.
"""

from __future__ import annotations

import json
import os
import re
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
import grade  # noqa: E402
import neurons  # noqa: E402  (rolling 24 h free-allowance guard)
from parallel import run_all  # noqa: E402

MODELS = ["@cf/google/gemma-4-26b-a4b-it", "@cf/meta/llama-3.3-70b-instruct-fp8-fast", "@cf/qwen/qwen3.8-27b"]
ARMS = ["C", "B", "BV", "SR"]
FORMAT = ("Reply with the complete module (the whole file, not a diff) in one fenced Python block. "
          "After the block, end with the line \"Notes for next time:\" and two short lines for yourself.")
NOTES = "Notes for next time:"


GRADING = threading.Lock()  # one grading process at a time: a busy machine must not turn into "timeout"


def grade_run(*a, **k) -> dict:
    with GRADING:
        return grade.run(*a, **k)


def short(model: str) -> str:
    return model.split("/")[-1]


# ---- the worker -------------------------------------------------------------

def door_call(model: str, messages: list) -> tuple:
    """(text, usage) through the door's /ai, as bench/eext/run.py's ai(). Raises
    neurons.OutOfNeurons when the allowance is spent, RuntimeError on other failures."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("boot_run", HERE.parent / "boot" / "run.py")
    boot = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(boot)  # only for the door's address, as bench/eext/run.py does
    dd = Path(os.environ["DOOR_DIR"])
    body = {"model": model, "max_tokens": 4096, "default_thinking": True, "messages": messages}
    req = urllib.request.Request(boot.DOOR + "/ai", method="POST", data=json.dumps(body).encode(), headers={
        "content-type": "application/json", "user-agent": "polymechania-bench/1",
        "CF-Access-Client-Id": (dd / "cf_id").read_text().strip(),
        "CF-Access-Client-Secret": (dd / "cf_secret").read_text().strip(),
        "x-door-token": (dd / "door_token").read_text().strip()})
    neurons.check(1500)
    last = None
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                out = json.loads(r.read())
            u = out.get("usage", {})
            neurons.log(model, u.get("neurons", 0), "bench/long")
            msg = (out.get("choices") or [{}])[0].get("message", {}) if "choices" in out else {}
            return msg.get("content") or out.get("response") or "", u
        except urllib.error.HTTPError as e:
            text = e.read().decode(errors="ignore")
            if neurons.refused_for_allowance(text):
                raise neurons.OutOfNeurons(text[:200])
            last = e
            time.sleep(10)
        except Exception as e:
            last = e
            time.sleep(10)
    raise RuntimeError(str(last))


def dry_call(model: str, messages: list) -> tuple:
    """Fake worker: the reference module of the round whose change text ends the last message."""
    last = messages[-1]["content"]
    found = [(last.rfind(r["spec"]), r["ref"]) for t in grade.names() for r in grade.task(t) if r["spec"] in last]
    if found:  # the change text comes last; a short earlier title may also sit inside the packet
        ref = max(found, key=lambda f: f[0])[1]
        return f"```python\n{ref}\n```\n{NOTES}\nkeep the reference\nnothing else", {"neurons": 0}
    raise RuntimeError("dry_call: no round's text found in the last message")


# ---- the packets ------------------------------------------------------------

def title(spec: str) -> str:
    s = re.sub(r"^Change:\s*", "", spec.strip())
    return re.split(r"(?<=[.:])\s", s, 1)[0][:90]


def code_of(text: str) -> str:
    m = re.search(r"```(?:python|py)?[ \t]*\n(.*?)```", text, re.S)
    return m.group(1) if m else ""


def notes_of(text: str) -> str:
    """The two lines after the last 'Notes for next time:'."""
    if NOTES not in text:
        return ""
    after = text.rsplit(NOTES, 1)[1]
    return "\n".join([ln.strip() for ln in after.splitlines() if ln.strip()][:2])


def ask(text: str) -> str:
    return f"{text}\n\n{FORMAT}"


def packet(arm: str, task: str, k: int, sol: Path) -> list:
    """The messages for round k (1-based) of this arm; reads the arm's earlier files from `sol`."""
    rounds = grade.task(task)
    spec = rounds[k - 1]["spec"]
    if k == 1:
        return [{"role": "user", "content": ask(spec)}]
    if arm == "C":
        msgs = []
        for j in range(1, k):
            msgs.append({"role": "user", "content": ask(rounds[j - 1]["spec"])})
            msgs.append({"role": "assistant", "content": (sol / f"{task}-r{j}.txt").read_text()})
        return msgs + [{"role": "user", "content": ask(spec)}]
    earlier = "Earlier changes: " + "; ".join(title(r["spec"]) for r in rounds[:k - 1]) + "."
    if arm == "SR":
        module, extra = rounds[k - 2]["ref"], ""
    else:
        module = (sol / f"{task}-r{k-1}.py").read_text()
        reply = (sol / f"{task}-r{k-1}.txt").read_text()
        extra = f"Notes you left for yourself:\n{notes_of(reply)}\n\n"
        if arm == "BV":
            # tests active in round k-1 that round k does not retire: never this round's new tests
            keep = set(grade.active(rounds, k - 1)) - set(rounds[k - 1].get("retires", ()))
            res = grade_run(task, k - 1, str(sol / f"{task}-r{k-1}.py"), only=keep)
            bad = [f"- {n}: {v}" for n, v in res.items() if v is not True]
            extra += ("Earlier tests that still apply and that your previous module fails:\n"
                      + ("\n".join(bad) if bad else "none") + "\n\n")
    return [{"role": "user", "content": ask(
        f"{earlier}\n\nThe previous module:\n```python\n{module}\n```\n\n{extra}This round:\n{spec}")}]


# ---- the run ----------------------------------------------------------------

def load(out: Path) -> list:
    f = out / "results.json"
    return json.loads(f.read_text()) if f.exists() else []


def chain(job: tuple, call, out: Path, state: dict) -> None:
    model, arm, task = job
    sol = out / "solutions" / short(model) / arm
    sol.mkdir(parents=True, exist_ok=True)
    for k in range(1, len(grade.task(task)) + 1):
        if (model, arm, task, k) in state["have"]:
            continue
        if state["stop"].is_set():
            return
        try:
            text, u = call(model, packet(arm, task, k, sol))
        except neurons.OutOfNeurons as e:
            state["stop"].set()
            print(f"stopped: the free allowance is spent ({str(e)[:80]}); run again later")
            return
        except Exception as e:  # not saved, so the next run tries this round again
            print(f"  {short(model)} {arm} {task} r{k}: {e}")
            return
        code = code_of(text)
        (sol / f"{task}-r{k}.txt").write_text(text)
        (sol / f"{task}-r{k}.py").write_text(code)
        res = grade_run(task, k, str(sol / f"{task}-r{k}.py"))
        bad = [n for n, v in res.items() if v is not True]
        row = {"model": model, "arm": arm, "task": task, "round": k, "pass": not bad, "failing": bad,
               "neurons": u.get("neurons", 0) or 0, "output_tokens": u.get("completion_tokens"),
               "input_tokens": u.get("prompt_tokens"), "reply_length": len(text),
               "error": None if code else "no code block"}
        with state["lock"]:
            state["rows"].append(row)
            state["have"].add((model, arm, task, k))
            (out / "results.json").write_text(json.dumps(state["rows"], indent=1) + "\n")


def run(models: list, call, out: Path = HERE, workers: int = 8) -> None:
    out.mkdir(parents=True, exist_ok=True)
    rows = load(out)
    state = {"rows": rows, "have": {(r["model"], r["arm"], r["task"], r["round"]) for r in rows},
             "lock": threading.Lock(), "stop": threading.Event()}
    jobs = [(m, a, t) for m in models for a in ARMS for t in grade.names()]
    print(f"{len(rows)} rounds done of {len(jobs) * 5}")
    run_all(lambda j: chain(j, call, out, state), jobs, workers=workers)
    print(f"{len(state['rows'])} rounds done of {len(jobs) * 5}")


# ---- the report -------------------------------------------------------------

def mt(rows: list) -> float | None:
    """Rounds passed before a task's first failure, averaged over the tasks that have rows."""
    per = {}
    for r in sorted(rows, key=lambda r: r["round"]):
        d = per.setdefault(r["task"], [0, False])
        if r["pass"] and not d[1]:
            d[0] += 1
        else:
            d[1] = True
    return sum(d[0] for d in per.values()) / len(per) if per else None


def regressions(rows: list) -> int:
    """Rounds that fail a test the arm's module passed one round earlier (and the round did not retire)."""
    n = 0
    by = {(r["task"], r["round"]): r for r in rows}
    for (t, k), r in by.items():
        prev = by.get((t, k - 1))
        if prev and prev["pass"] is not None:
            old = set(grade.active(grade.task(t), k - 1)) - set(prev["failing"])
            n += bool(old & set(r["failing"]))
    return n


def report(out: Path = HERE) -> None:
    rows = load(out)
    pooled = {a: [0, 0] for a in ARMS}
    for m in MODELS:
        for a in ARMS:
            xs = [r for r in rows if r["model"] == m and r["arm"] == a]
            if not xs:
                continue
            p = sum(r["pass"] for r in xs)
            pooled[a][0] += p
            pooled[a][1] += len(xs)
            m_t = mt(xs) if a != "SR" else None
            print(f"{short(m):34} {a:2} pass {p:2}/{len(xs):2} of 30  "
                  f"MT {'-' if m_t is None else format(m_t, '.2f'):>5}  "
                  f"regressions {regressions(xs):2}  no code {sum(1 for r in xs if r.get('error') == 'no code block'):2}  neurons {sum(r['neurons'] for r in xs):7.0f}")
    print("\npooled over models (rounds passed / rounds done):")
    for a in ARMS:
        print(f"  {a:2} {pooled[a][0]}/{pooled[a][1]}")
    if not all(pooled[a][1] for a in ARMS):
        print("some arm has no rows yet; no decisions")
        return
    rate = {a: Fraction(*pooled[a]) for a in ARMS}
    done = all(pooled[a][1] == 90 * len([m for m in MODELS if any(r["model"] == m for r in rows)]) for a in ARMS)
    print("" if done else "(incomplete: not every round is done)")

    def gap(x, y):
        g = 100 * (rate[x] - rate[y])
        return g, f"{x} minus {y} = {float(g):+.1f} points"

    g, s = gap("B", "C")
    print(f"1. fresh start alone helps (B - C >= 15): {s}: {'YES' if g >= 15 else 'no (direction only)' if abs(g) < 15 else 'no'}")
    g, s = gap("BV", "B")
    print(f"2. check on the boundary helps (BV - B >= 15): {s}: {'YES' if g >= 15 else 'no (direction only)' if abs(g) < 15 else 'no'}")
    g, s = gap("SR", "C")
    verdict = "prior holds" if 15 <= g <= 45 else "too easy to show it" if g < 15 else "too hard"
    print(f"3. outside prior (SR - C between 15 and 45): {s}: {verdict}")
    sat = all(rate[a] >= Fraction(9, 10) for a in ("C", "B", "BV"))
    print(f"4. C, B and BV all >= 90%: {'YES, the tasks did not separate the shapes' if sat else 'no'}")


if __name__ == "__main__":
    args = sys.argv[1:]
    cmd = args.pop(0) if args and not args[0].startswith("-") else "report"
    dry = "--dry" in args
    out = Path(args[args.index("--out") + 1]) if "--out" in args else (
        Path(tempfile.mkdtemp(prefix="long-dry-")) if dry else HERE)
    models = MODELS
    if "--models" in args:
        names = [a for a in args[args.index("--models") + 1:] if not a.startswith("-")]
        models = [m for m in MODELS if any(n in m for n in names)]
    if cmd == "run":
        print("output folder:", out)
        run(models, dry_call if dry else door_call, out)
        if dry:
            report(out)
    else:
        report(out)
