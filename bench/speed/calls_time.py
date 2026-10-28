"""S1, J2: 24 short Gemma calls through the door, one at a time and 8 at once
(prereg/s1-speed.md). Free (Workers AI allowance).

    DOOR_DIR=... python bench/speed/calls_time.py
"""

from __future__ import annotations

import importlib.util
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "bench" / "boot"))
import run as t2  # noqa: E402

_spec = importlib.util.spec_from_file_location("t12", ROOT / "bench" / "self" / "run.py")
t12 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(t12)


def one(spec: str) -> tuple[float, float]:
    t = time.time()
    _, u = t12.ai([{"role": "user", "content": "Reply with the Python function only.\n\n" + spec}], max_tokens=256)
    return time.time() - t, u.get("neurons", 0)


def main() -> None:
    specs = [s for _, _, s in t2.tasks()]  # 24 task specs
    out = {}
    for label, workers in (("one at a time", 1), ("8 at once", 8)):
        t = time.time()
        with ThreadPoolExecutor(workers) as ex:
            res = list(ex.map(one, specs))
        out[label] = {"wall_s": round(time.time() - t, 1), "median_call_s": round(sorted(r[0] for r in res)[12], 1),
                      "neurons": round(sum(r[1] for r in res), 1)}
        print(label, out[label])
    (HERE / "s1-calls.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
