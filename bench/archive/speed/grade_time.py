"""S1, J1: time regrading the 96 saved T2 solutions (bench/archive/prereg/s1-speed.md).

    python bench/archive/speed/grade_time.py [--out file.json]

Runs three times with one worker and three times with one worker per CPU,
and prints medians. Grading only: the exact half of bench/verify.py.
"""

from __future__ import annotations

import json
import os
import platform
import statistics
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent
PILOT = ROOT / "bench" / "pilot"
BOOT = ROOT / "bench" / "boot"


def jobs() -> list:
    runs = json.loads((BOOT / "results.json").read_text())["runs"]
    return [(x["set"], x["task"], str(BOOT / "solutions" / x["model"] / x["arm"] / f"{x['task']}.py")) for x in runs]


def grade(j) -> str:
    out = subprocess.run([sys.executable, f"{j[0]}/grade.py", j[1], j[2]], cwd=PILOT,
                         capture_output=True, text=True, timeout=900)
    return (out.stdout.strip() or "FAIL").splitlines()[-1]


def timed(workers: int, js: list) -> tuple[float, int]:
    t = time.time()
    with ThreadPoolExecutor(workers) as ex:
        res = list(ex.map(grade, js))
    return time.time() - t, sum(r == "PASS" for r in res)


def main() -> None:
    js = jobs()
    cpus = os.cpu_count() or 1
    out = {"where": os.environ.get("S1_WHERE", "here"), "cpus": cpus, "python": platform.python_version(),
           "machine": platform.machine(), "jobs": len(js), "runs": {}}
    for w in (1, cpus):
        times, passes = [], set()
        for _ in range(3):
            s, p = timed(w, js)
            times.append(round(s, 2))
            passes.add(p)
        out["runs"][str(w)] = {"seconds": times, "median": statistics.median(times), "passes": sorted(passes)}
    print(json.dumps(out, indent=1))
    if "--out" in sys.argv:
        Path(sys.argv[sys.argv.index("--out") + 1]).write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
