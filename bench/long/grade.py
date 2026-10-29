"""Grader for the long tasks (queue q15): rounds with changing requirements and cumulative tests.

    python bench/long/grade.py <task> <round> <module.py>   # prints PASS, or FAIL and the failing tests
    python bench/long/grade.py --validate                   # checks every task's graders (below)

Shaped after EvoCode-Bench (arXiv 2605.24110): each task keeps one module
through 5 rounds; each round adds or changes a requirement, and the tests
of every earlier round stay active unless a later round explicitly retires
them (a requirement that changed). A round passes when every active test
passes. Each task file in tasks/ defines ROUNDS: a list of dicts with
"spec" (what the worker is told), "ref" (a reference module, as text),
"tests" ({name: function(module)}, raising on failure) and "retires"
(names of earlier tests this round replaces).

--validate is the exact check of the graders themselves, done before any
model sees a task:
  1. every round's reference passes every test active in that round;
  2. the previous round's reference fails at least one of this round's new
     tests (so every round asks for something new), and round 1's new tests
     fail on an empty module;
  3. every retired test exists in an earlier round, and the reference of the
     round that retires it fails it (so the change is real).
"""

from __future__ import annotations

import importlib.util
import multiprocessing as mp
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
TIME_LIMIT = 10  # seconds per round's tests


def task(name: str) -> list:
    spec = importlib.util.spec_from_file_location(f"long_task_{name}", HERE / "tasks" / f"{name}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.ROUNDS


def names() -> list:
    return sorted(p.stem for p in (HERE / "tasks").glob("*.py") if not p.stem.startswith("_"))


def active(rounds: list, k: int) -> dict:
    """Tests that count at round k (1-based): all tests of rounds 1..k, minus those retired by rounds 2..k."""
    tests, retired = {}, set()
    for r in rounds[:k]:
        tests.update(r["tests"])
        retired.update(r.get("retires", ()))
    return {n: f for n, f in tests.items() if n not in retired}


def _load(path: str):
    spec = importlib.util.spec_from_file_location("candidate", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _run(task_name: str, k: int, path: str, only, q) -> None:
    rounds = task(task_name)
    tests = active(rounds, k)
    if only is not None:
        tests = {n: f for n, f in tests.items() if n in only}
    out = {}
    try:
        m = _load(path)
    except BaseException as e:  # a module that does not even import fails every test
        q.put({n: f"import: {type(e).__name__}: {e}"[:200] for n in tests})
        return
    for n, f in tests.items():
        try:
            f(m)
            out[n] = True
        except BaseException as e:
            out[n] = f"{type(e).__name__}: {e}"[:200] or type(e).__name__
    q.put(out)


def run(task_name: str, k: int, path: str, only=None) -> dict:
    """{test name: True or the failure}, in a separate process with a time limit."""
    q = mp.Queue()
    p = mp.Process(target=_run, args=(task_name, k, path, only, q))
    p.start()
    p.join(TIME_LIMIT)
    if p.is_alive():
        p.kill()
        p.join()
        names_ = active(task(task_name), k)
        return {n: "timeout" for n in names_ if only is None or n in only}
    return q.get() if not q.empty() else {"process": "crashed"}


def grade(task_name: str, k: int, path: str) -> str:
    res = run(task_name, k, path)
    bad = [n for n, v in res.items() if v is not True]
    return "PASS" if not bad else "FAIL: " + ", ".join(bad)


def write(code: str) -> str:
    f = tempfile.NamedTemporaryFile("w", suffix=".py", delete=False)
    f.write(code)
    f.close()
    return f.name


def validate() -> list:
    problems = []
    for t in names():
        rounds = task(t)
        seen = set()
        if len(rounds) < 3:
            problems.append(f"{t}: only {len(rounds)} rounds")
        for k, r in enumerate(rounds, 1):
            ref = write(r["ref"])
            res = run(t, k, ref)
            for n, v in res.items():
                if v is not True:
                    problems.append(f"{t} r{k}: reference fails active test {n}: {v}")
            prev = write(rounds[k - 2]["ref"]) if k > 1 else write("")
            new = set(r["tests"])
            res_prev = run(t, k, prev, only=new)
            if all(v is True for v in res_prev.values()):
                problems.append(f"{t} r{k}: the previous reference already passes every new test")
            for n in r.get("retires", ()):
                if n not in seen:
                    problems.append(f"{t} r{k}: retires {n}, which no earlier round defines")
                else:
                    # the retired test, run directly against this round's reference
                    old = next(rr["tests"][n] for rr in rounds[:k - 1] if n in rr["tests"])
                    try:
                        old(_load(ref))
                        problems.append(f"{t} r{k}: retires {n}, but this round's reference still passes it")
                    except BaseException:
                        pass
            dup = new & seen
            if dup:
                problems.append(f"{t} r{k}: test names reused: {sorted(dup)}")
            seen |= new
        print(f"{t}: {len(rounds)} rounds, {len(seen)} tests")
    return problems


if __name__ == "__main__":
    if sys.argv[1:] == ["--validate"]:
        ps = validate()
        print("\n".join(ps) if ps else "validate: every grader checks out")
        sys.exit(1 if ps else 0)
    t, k, path = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    print(grade(t, k, path))
