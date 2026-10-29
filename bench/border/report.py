"""Write bench/border/RESULTS.md from the results-<label>.json files (queue q30).

    python bench/border/report.py main gate55
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
NOTES = """## Notes

- B5 was first worded "unmarked" and checked the Python result only; the text a model reads
  (`render_resume`) does label everything as data. T12d measured that such a label barely
  protects (+9 points, under the 15-point rule), so B5 checks whether the request reaches
  what the resident reads. With protocol version 4 (Gnomon #55) that is the start packet.
- B10 (recall scores) holds, as the earlier map probe P22 found; the #48 leak is a different
  side channel, probed by B10b (sequence gaps).
- B12 checks every tracked file in both repositories for key patterns and for the live door
  credentials themselves (compared, never printed).
- B3 (leases) and B13 (outside agents) have nothing to probe until those exist; they count
  against the border, not for it.
- Moved, not removed: B11 rests on the door's own test suite, so the spending border is only
  as good as `test_door.mjs`.

Run: `GNOMON_PYTHON=../gnomon/python python bench/border/check.py --label <name>`, then
`python bench/border/report.py <labels...>`.
"""


def main(labels):
    runs = [json.loads((HERE / f"results-{x}.json").read_text()) for x in labels]
    by = [{r["id"]: r for r in run["rows"]} for run in runs]
    lines = ["# The border check: which threats are refused today (q30)", "",
             "Exact probes (`bench/border/check.py`, no model), one or more per threat in `docs/security.md`.",
             "Raw: " + ", ".join(f"`results-{x}.json`" for x in labels) + ".", "",
             " ".join(f"**{x} (Gnomon {r['gnomon']}, {r['when'][:10]}): {r['holds']} of {r['of']} hold.**"
                      for x, r in zip(labels, runs)), "",
             "| Probe | Threat | Must hold | " + " | ".join(labels) + " | Fixed by |",
             "|---|---|---|" + "---|" * len(labels) + "---|"]
    for row in runs[0]["rows"]:
        cells = " | ".join(b.get(row["id"], {}).get("state", "-") for b in by)
        lines.append(f"| {row['id']} | {row['threat']} | {row['must']} | {cells} | {row['issue'] or ''} |")
    (HERE / "RESULTS.md").write_text("\n".join(lines) + "\n\n" + NOTES)


if __name__ == "__main__":
    main(sys.argv[1:])
