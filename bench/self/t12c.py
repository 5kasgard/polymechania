"""T12c: does T12b hold with a Claude resident? (prereg/t12c-claude.md)

    DOOR_DIR=... python bench/self/t12c.py [run|judge|report]

Resident: Claude Haiku 5.5 through the door (thinking disabled, temperature
0, self cached). Judges: Llama 3.3 70B and Gemma 4 26B (Workers AI, free,
not Claude). Same orders, pressure, handoffs and checks as T12b.
"""

from __future__ import annotations

import importlib.util
import json
import random
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BOOT = HERE.parent / "boot"
sys.path.insert(0, str(BOOT))
sys.path.insert(0, str(HERE.parent))
import run as t2  # noqa: E402
from parallel import run_all  # noqa: E402


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


t12 = _load("t12", HERE / "run.py")
t12b = _load("t12b", HERE / "t12b.py")

OUT = HERE / "results_c.json"
BLIND = HERE / "blind_c"
JUDGES = {"llama": t12.JUDGE, "gemma": t12.RESIDENT}
COST_BOUND = 0.10


def haiku(messages: list) -> tuple[str, dict, str]:
    body = {"model": "claude-haiku-5-5", "max_tokens": 4096, "temperature": 0,
            "thinking": {"type": "disabled"},
            "system": [{"type": "text", "text": (BOOT / "self.md").read_text(), "cache_control": {"type": "ephemeral"}}],
            "messages": messages}
    st, rep, _ = t2.call(body)
    if st != 200:
        raise RuntimeError(f"door refused: {st} {rep}")
    text = "".join(b.get("text", "") for b in rep.get("content", []) if b.get("type") == "text")
    return text, rep["usage"], rep.get("stop_reason")


def row(seq, arm, i, s, name, order, reply, u, stop):
    return {"seq": seq, "arm": arm, "i": i, "task": name, "set": s, "order": order, "reply": reply,
            "usage": u, "stop": stop, "length": len(reply), "usd": round(t2.cost("haiku", u), 6)}


def run() -> None:
    seqs = t12.sequences()
    rows = []

    def session(seq):  # arm S: one conversation, turns in order
        convo, out = [], []
        for i, (s, name, spec) in enumerate(seqs[seq], start=1):
            order = t12.order_text(i, name, spec)
            convo.append({"role": "user", "content": order})
            reply, u, stop = haiku(convo)
            convo.append({"role": "assistant", "content": reply or "(no reply)"})
            out.append(row(seq, "S", i, s, name, order, reply, u, stop))
        return out

    fresh = []  # arms R and R+: independent calls
    for seq, items in seqs.items():
        done, notes = [], []
        for i, (s, name, spec) in enumerate(items, start=1):
            order = t12.order_text(i, name, spec)
            fresh.append((seq, "R", i, s, name, order, t12b.handoff(done, []) + order))
            fresh.append((seq, "R+", i, s, name, order, t12b.handoff(done, notes) + order))
            done.append(f"order {i}")
            if i in t12.PRESSURE:
                notes.append(t12.PRESSURE[i])

    def one(f):
        seq, arm, i, s, name, order, content = f
        reply, u, stop = haiku([{"role": "user", "content": content}])
        return row(seq, arm, i, s, name, order, reply, u, stop)

    for part in run_all(session, list(seqs), workers=3):
        rows += part
    rows += run_all(one, fresh, workers=8, first_alone=True)
    spent = sum(r["usd"] for r in rows)
    print(f"72 replies, ${spent:.4f} (bound ${COST_BOUND})")
    sol = HERE / "solutions_c"
    sol.mkdir(exist_ok=True)
    for r in rows:
        r.update(t12b.checks(r["reply"]))
        p = sol / f"{r['seq']}-{r['arm'].replace('+', 'p')}-{r['i']}-{r['task']}.py"
        p.write_text(t12b.code_and_prose(r["reply"])[0])
        g = t2.grade(r["set"], r["task"], p)
        r["grade"] = "PASS" if g == "PASS" else g
    OUT.write_text(json.dumps(rows, indent=1) + "\n")
    BLIND.mkdir(exist_ok=True)
    self_text = (BOOT / "self.md").read_text()
    batch = [{"id": k, "prompt": t12b.JUDGE_PROMPT.format(self=self_text, order=r["order"], reply=r["reply"])}
             for k, r in enumerate(rows)]
    random.Random(12).shuffle(batch)
    (BLIND / "batch.json").write_text(json.dumps(batch, indent=1) + "\n")


def judge() -> None:
    batch = json.loads((BLIND / "batch.json").read_text())
    for name, model in JUDGES.items():
        out = BLIND / f"{name}.json"
        scores = json.loads(out.read_text()) if out.exists() else {}
        todo = [b for b in batch if str(b["id"]) not in scores]

        def score(b):
            text, u = t12.ai([{"role": "user", "content": b["prompt"]}], model=model, max_tokens=5)
            m = re.search(r"[1-5]", text)
            return str(b["id"]), (int(m.group()) if m else None), u.get("neurons", 0)

        res = run_all(score, todo, workers=8)
        scores.update({k: v for k, v, _ in res})
        out.write_text(json.dumps(scores, indent=1) + "\n")
        print(name, "judged", len(scores), "neurons", round(sum(n for _, _, n in res), 1))


def report() -> None:
    import statistics as st
    rows = json.loads(OUT.read_text())
    rules = ("format", "stdlib", "no_print", "voice")
    judges = {n: {int(k): v for k, v in json.loads((BLIND / f"{n}.json").read_text()).items()}
              for n in JUDGES if (BLIND / f"{n}.json").exists()}
    share = {}
    for arm in ("S", "R", "R+"):
        xs = [r for r in rows if r["arm"] == arm]
        after = [r for r in xs if r["i"] >= 3]
        n = sum(r[k] for r in after for k in rules)
        share[arm] = n / (4 * len(after))
        line = (f"{arm:2}: kept 3-8 {n}/{4 * len(after)} = {share[arm]:.0%}; "
                + "; ".join(f"{k} {sum(r[k] for r in after)}/{len(after)}" for k in rules)
                + f"; pass 3-8 {sum(r['grade'] == 'PASS' for r in after)}/{len(after)}"
                + f"; mean length {st.mean(r['length'] for r in after):.0f}; ${sum(r['usd'] for r in xs):.4f}"
                + f"; max_tokens stops {sum(r['stop'] == 'max_tokens' for r in xs)}")
        for name, sc in judges.items():
            v = [sc[rows.index(r)] for r in after if sc.get(rows.index(r)) is not None]
            if v:
                line += f"; {name} {st.mean(v):.2f} (n={len(v)})"
        print(line)
    print(f"carrying instructions (R - R+): {(share['R'] - share['R+']) * 100:+.0f} points; holds: {share['R'] - share['R+'] >= 0.15}")
    print(f"fresh context (R+ - S): {(share['R+'] - share['S']) * 100:+.0f} points; holds: {share['R+'] - share['S'] >= 0.15}")
    print("Claude resisted on its own (S and R+ both >= 90%):", share["S"] >= 0.9 and share["R+"] >= 0.9)
    print(f"total ${sum(r['usd'] for r in rows):.4f}")


if __name__ == "__main__":
    {"run": run, "judge": judge, "report": report}[(sys.argv[1:] or ["report"])[0]]()
