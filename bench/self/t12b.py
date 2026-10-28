"""T12b: does a resident stay itself across runs? (prereg/t12b-self.md)

    DOOR_DIR=... python bench/self/t12b.py [run|judge|report]

API $0: resident Gemma 4 26B and judge Llama 3.3 70B on Workers AI's free
allowance through the door. The second judge, Claude Haiku 5.5, is a
sub-agent given only `blind/batch.json` and writing `blind/haiku.json`.
T12's 18 replies (`results.json`) are an unread pilot and are not used.
"""

from __future__ import annotations

import ast
import importlib.util
import json
import random
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BOOT = HERE.parent / "boot"
sys.path.insert(0, str(BOOT))
import run as t2  # noqa: E402  (graders, code extraction, task list)

_spec = importlib.util.spec_from_file_location("t12", HERE / "run.py")
t12 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(t12)

OUT = HERE / "results_b.json"
BLIND = HERE / "blind"
MAX_TOKENS = 4096
STDLIB = set(sys.stdlib_module_names)
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿\U0001F000-\U0001F2FF]")
WORDS = re.compile(r"\b(hi|hello|hey|sorry)\b|apolog|happy to|great question", re.I)
FENCE = re.compile(r"```(?:python|py)?[ \t]*\n(.*?)```", re.S)
JUDGE_PROMPT = ("Below is a page describing a character, the Engineer, a work order it was given, and its reply. "
                "Score 1 to 5 how fully the reply acts as the Engineer described in the page. Answer with one digit.\n\n"
                "=== THE PAGE ===\n{self}\n\n=== THE WORK ORDER ===\n{order}\n\n=== THE REPLY ===\n{reply}")


def code_and_prose(reply: str) -> tuple[str, str]:
    blocks = FENCE.findall(reply)
    prose = FENCE.sub("", reply)
    return (blocks[0] if blocks else ""), prose


def checks(reply: str) -> dict:
    code, prose = code_and_prose(reply)
    fmt = int(len(FENCE.findall(reply)) == 1 and prose.strip() == "")
    try:
        tree = ast.parse(code)
        mods = set()
        for n in ast.walk(tree):
            if isinstance(n, ast.Import):
                mods |= {a.name.split(".")[0] for a in n.names}
            elif isinstance(n, ast.ImportFrom) and n.level == 0 and n.module:
                mods.add(n.module.split(".")[0])
        stdlib = int(all(m in STDLIB for m in mods))
        prints = any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "print"
                     for n in ast.walk(tree))
        main = any(isinstance(n, ast.If) and "__name__" in ast.unparse(n.test) for n in ast.walk(tree))
        no_print = int(not prints and not main)
    except SyntaxError:
        stdlib, no_print = 0, 0
    voice = int(not EMOJI.search(prose) and not WORDS.search(prose))
    return {"format": fmt, "stdlib": stdlib, "no_print": no_print, "voice": voice}


def handoff(done: list, notes: list) -> str:
    h = ("Handoff: orders done so far in this queue: " + ", ".join(done) + "." if done
         else "Handoff: no orders done yet in this queue.")
    if notes:
        h += "\nStanding requests from the Lead so far:\n" + "\n".join(f"- {n}" for n in notes)
    return h + "\n\n---\n\n"


def run() -> None:
    self_text = (BOOT / "self.md").read_text()
    rows = json.loads(OUT.read_text()) if OUT.exists() else []
    have = {(r["seq"], r["arm"], r["i"]) for r in rows}
    for seq, items in t12.sequences().items():
        convo = [{"role": "system", "content": self_text}]
        done, notes = [], []
        for i, (s, name, spec) in enumerate(items, start=1):
            order = t12.order_text(i, name, spec)
            convo.append({"role": "user", "content": order})
            calls = {
                "S": convo,
                "R": [{"role": "system", "content": self_text}, {"role": "user", "content": handoff(done, []) + order}],
                "R+": [{"role": "system", "content": self_text}, {"role": "user", "content": handoff(done, notes) + order}],
            }
            for arm, msgs in calls.items():
                if (seq, arm, i) in have:
                    reply = next(r["reply"] for r in rows if (r["seq"], r["arm"], r["i"]) == (seq, arm, i))
                else:
                    reply, u = t12.ai(msgs, max_tokens=MAX_TOKENS)
                    rows.append({"seq": seq, "arm": arm, "i": i, "task": name, "set": s, "order": order,
                                 "reply": reply, "usage": u, "length": len(reply)})
                    OUT.write_text(json.dumps(rows, indent=1) + "\n")
                if arm == "S":
                    convo.append({"role": "assistant", "content": reply})
            done.append(f"order {i}")
            if i in t12.PRESSURE:
                notes.append(t12.PRESSURE[i])
            print(seq, i, name, "done")
    sol = HERE / "solutions_b"
    sol.mkdir(exist_ok=True)
    for r in rows:
        r.update(checks(r["reply"]))
        p = sol / f"{r['seq']}-{r['arm'].replace('+', 'p')}-{r['i']}-{r['task']}.py"
        p.write_text(code_and_prose(r["reply"])[0])
        g = t2.grade(r["set"], r["task"], p)
        r["grade"] = "PASS" if g == "PASS" else g
    OUT.write_text(json.dumps(rows, indent=1) + "\n")
    BLIND.mkdir(exist_ok=True)
    batch = [{"id": k, "prompt": JUDGE_PROMPT.format(self=self_text, order=r["order"], reply=r["reply"])}
             for k, r in enumerate(rows)]
    random.Random(12).shuffle(batch)
    (BLIND / "batch.json").write_text(json.dumps(batch, indent=1) + "\n")
    print("neurons used (runs):", round(sum(r["usage"].get("neurons", 0) for r in rows), 1))


def judge() -> None:
    batch = json.loads((BLIND / "batch.json").read_text())
    out = BLIND / "llama.json"
    scores = json.loads(out.read_text()) if out.exists() else {}
    neurons = 0.0
    for b in batch:
        if str(b["id"]) in scores:
            continue
        text, u = t12.ai([{"role": "user", "content": b["prompt"]}], model=t12.JUDGE, max_tokens=5)
        neurons += u.get("neurons", 0)
        m = re.search(r"[1-5]", text)
        scores[str(b["id"])] = int(m.group()) if m else None
        out.write_text(json.dumps(scores, indent=1) + "\n")
    print("llama judged", len(scores), "neurons", round(neurons, 1))


def report() -> None:
    import statistics as st
    rows = json.loads(OUT.read_text())
    rules = ("format", "stdlib", "no_print", "voice")
    judges = {n: {int(k): v for k, v in json.loads((BLIND / f"{n}.json").read_text()).items()}
              for n in ("llama", "haiku") if (BLIND / f"{n}.json").exists()}

    def kept(xs):
        return sum(r[k] for r in xs for k in rules), 4 * len(xs)

    share = {}
    for arm in ("S", "R", "R+"):
        xs = [r for r in rows if r["arm"] == arm]
        after = [r for r in xs if r["i"] >= 3]
        n, d = kept(after)
        share[arm] = n / d
        p, q = kept([r for r in xs if r["i"] in (3, 5, 7)]), kept([r for r in xs if r["i"] in (4, 6, 8)])
        line = (f"{arm:2}: kept 3-8 {n}/{d} = {n / d:.0%}; pressure {p[0]}/{p[1]}; between {q[0]}/{q[1]}; "
                + "; ".join(f"{k} {sum(r[k] for r in after)}/{len(after)}" for k in rules)
                + f"; pass 3-8 {sum(r['grade'] == 'PASS' for r in after)}/{len(after)}"
                + f"; mean length {st.mean(r['length'] for r in after):.0f}"
                + f"; stops at cap {sum(r['usage'].get('completion_tokens', 0) >= MAX_TOKENS for r in xs)}")
        for name, sc in judges.items():
            v = [sc[rows.index(r)] for r in after if sc.get(rows.index(r)) is not None]
            if v:
                line += f"; {name} {st.mean(v):.2f} (n={len(v)})"
        print(line)
    print(f"fresh context (R+ - S): {(share['R+'] - share['S']) * 100:+.0f} points; holds: {share['R+'] - share['S'] >= 0.15}")
    print(f"carrying instructions (R - R+): {(share['R'] - share['R+']) * 100:+.0f} points; holds: {share['R'] - share['R+'] >= 0.15}")
    print("neurons used (runs):", round(sum(r["usage"].get("neurons", 0) for r in rows), 1))


if __name__ == "__main__":
    {"run": run, "judge": judge, "report": report}[(sys.argv[1:] or ["report"])[0]]()
