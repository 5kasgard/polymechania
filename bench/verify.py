"""The exact half of every audit: recompute numbers and regrade, for free.

    python bench/verify.py            # every known result set
    python bench/verify.py boot       # one

A model auditor then judges only what a script cannot (wording, overclaims,
missing caveats). Exits non-zero if anything recorded disagrees with what is
recomputed, so it can run in CI.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PILOT = ROOT / "bench" / "pilot"
BOOT = ROOT / "bench" / "boot"
sys.path.insert(0, str(ROOT))
from polymechania import plan  # noqa: E402

FIXED = {  # files fixed by hash in pre-registrations
    "bench/boot/self.md": "144012916a3c9ae8d13a6bfffb1ccc787aa12ba72d01293bf093f370907d11a8",
    "bench/boot/packet.txt": "27a78085d62b33fac879fc044c60741de6821803a7f2320b0c836bcf86d2a2af",
}
problems: list[str] = []


def price(model: str):
    p = plan.TIERS[model].price
    return p.input, p.output, p.cache_hit, p.cache_write


def usd(model: str, x: dict) -> float:
    i, o, cr, cw = price(model)
    return (x["input"] * i + x["output"] * o + x["cache_read"] * cr + x["cache_write"] * cw) / 1e6


def grade(s: str, task: str, path: Path) -> str:
    out = subprocess.run([sys.executable, f"{s}/grade.py", task, str(path)], cwd=PILOT,
                         capture_output=True, text=True, timeout=900)
    last = (out.stdout.strip() or "FAIL").splitlines()[-1]
    return "PASS" if last == "PASS" else "FAIL"


def check(label: str, recorded, recomputed, tol: float = 1e-6) -> None:
    ok = abs(recorded - recomputed) <= tol if isinstance(recorded, (int, float)) else recorded == recomputed
    if not ok:
        problems.append(f"{label}: recorded {recorded!r}, recomputed {recomputed!r}")


def hashes() -> None:
    for rel, want in FIXED.items():
        got = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
        check(f"hash {rel}", want, got)
    print("hashes checked:", len(FIXED))


def rows_check(name: str, rows: list, model_of, sol_of) -> None:
    by = {}
    for x in rows:
        m = model_of(x)
        check(f"{name} {x.get('arm')} {x['task']} usd", round(x["usd"], 6), round(usd(m, x), 6), 2e-6)
        path = sol_of(x)
        g = grade(x["set"], x["task"], path)
        check(f"{name} {x.get('arm')} {x['task']} grade", "PASS" if x["grade"] == "PASS" else "FAIL", g)
        key = (m, x.get("arm"))
        b = by.setdefault(key, {"n": 0, "pass": 0, "usd": 0.0, "empty": 0})
        b["n"] += 1
        b["pass"] += g == "PASS"
        b["usd"] += usd(m, x)
        b["empty"] += path.stat().st_size == 0
    for (m, arm), b in sorted(by.items()):
        print(f"  {name} {m} {arm}: {b['pass']}/{b['n']} pass, {b['empty']} empty, ${b['usd']:.6f}")


def boot() -> None:
    hashes()
    r = json.loads((BOOT / "results.json").read_text())
    print("T2:")
    rows_check("T2", r["runs"], lambda x: x["model"],
               lambda x: BOOT / "solutions" / x["model"] / x["arm"] / f"{x['task']}.py")
    for file, label in (("t2b_results.json", "T2b"), ("t2c_results.json", "T2c")):
        p = BOOT / file
        if p.exists():
            print(f"{label}:")
            rows_check(label, json.loads(p.read_text()), lambda x: "haiku",
                       lambda x: BOOT / "solutions" / "haiku" / x["arm"] / f"{x['task']}.py")


SETS = {"boot": boot}

if __name__ == "__main__":
    for name in sys.argv[1:] or SETS:
        SETS[name]()
    if problems:
        print("\nDISAGREEMENTS:")
        print("\n".join(problems))
        sys.exit(1)
    print("\nverify: everything recorded matches what is recomputed")
