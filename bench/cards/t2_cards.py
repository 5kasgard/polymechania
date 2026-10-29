"""Stat cards with cost and speed, filled from the T2, T2b and T2c runs (queue q16).

    python bench/cards/t2_cards.py      # writes bench/cards/T2_CARDS.md and t2_cards.json

Each run is one Result: the hidden graders are the verdict (a script, so
outside every model family, blind, on checks the worker never saw); cost
and time are what the run logged. One worker per model and settings.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
from polymechania.cards import PASS, FAIL, Result, Verdict, card, expected_cost  # noqa: E402

BOOT = ROOT / "bench" / "boot"
SETTINGS = {"A": "start packet in the prompt, default thinking", "B": "start packet cached, default thinking",
            "D": "cached, thinking off", "L": "cached, adaptive thinking, low effort", "DL": "cached, thinking off, low effort"}


def results():
    rows = [(x["model"], x) for x in json.loads((BOOT / "results.json").read_text())["runs"]]
    rows += [("haiku", x) for f in ("t2b_results.json", "t2c_results.json") for x in json.loads((BOOT / f).read_text())]
    for model, x in rows:
        worker = f"{model} {x['arm']}"
        yield Result(worker, "claude", f"code-{x['set']}", verdicts=(Verdict(PASS if x["grade"] == "PASS" else FAIL, "script"),),
                     tokens=x.get("output", 0), cost_usd=x["usd"], ms=int(x["secs"] * 1000), where="anthropic-api")


def main():
    rs = list(results())
    out = []
    for worker in sorted({r.worker for r in rs}):
        for kind in ("code-easy", "code-hard"):
            if not any(r.worker == worker and r.kind == kind for r in rs):
                continue
            c = card(rs, worker, kind)
            d = c.as_dict() | {"settings": SETTINGS[worker.split()[1]],
                               "expected_cost_loss_1c": expected_cost(c, 0.01), "expected_cost_loss_10c": expected_cost(c, 0.10)}
            out.append(d)
    (Path(__file__).parent / "t2_cards.json").write_text(json.dumps(out, indent=1) + "\n")
    lines = ["# Stat cards with cost and speed, from T2, T2b and T2c (q16)", "",
             "Built by `bench/cards/t2_cards.py` from the saved runs; nothing typed in. One attempt",
             "per task, 12 tasks per set, so intervals are wide and gaps of one pass are directions.",
             "Verdicts are the hidden graders (a script: outside every model family). The two",
             "expected-cost columns are examples of `expected_cost` with a wrong result costing",
             "1 cent or 10 cents (to redo or to catch); the right loss depends on the work.", "",
             "| Worker | Settings | Kind | Passes | Success (90%) | $ per run | $ per success | p50 s | p90 s | Expected $ (loss 1c / 10c) |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for d in out:
        lines.append(f"| {d['worker']} | {d['settings']} | {d['kind']} | {d['successes']}/{d['judged']} | "
                     f"{d['mean']:.2f} ({d['low']:.2f}-{d['high']:.2f}) | {d['cost_usd']:.5f} | {d['cost_per_success']:.5f} | "
                     f"{d['ms_p50'] / 1000:.1f} | {d['ms_p90'] / 1000:.1f} | {d['expected_cost_loss_1c']:.4f} / {d['expected_cost_loss_10c']:.4f} |")
    (Path(__file__).parent / "T2_CARDS.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[-len(out):]))


if __name__ == "__main__":
    main()
