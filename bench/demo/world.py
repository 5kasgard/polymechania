"""Build the border demo's data from a real Gnomon log (queue q11, docs/security.md).

    GNOMON_PYTHON=... python bench/demo/world.py   # writes bench/demo/world.json

Nothing on the map is invented: regions are the log's compartments; a road
exists only where some resident is registered in both regions (and is
labelled with who can cross); gates are the door's real allowlists, read
from its source; refused crossings are real attempts made against this log
at build time (Gnomon does not record refusals yet, and the page says so).
"""

from __future__ import annotations

import json
import os
import re
import sys
import tempfile
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, os.environ.get("GNOMON_PYTHON", str(ROOT.parent / "gnomon" / "python")))
import gnomon as g  # noqa: E402

T = "2026-10-28T12:00:00Z"
REGIONS = {  # compartment -> what the region is for (plain)
    "capital": "where you and your guides live: the record, the rules, the library",
    "workshop": "code work: orders, results, tests",
    "observatory": "research: reading, notes, sources",
    "holdout": "an experiment whose workers must not see the answers",
}
RESIDENTS = [  # (writer, name, kind, compartments, model)
    ("guide", "Guide", "model", ["capital"], "claude-haiku-5-5"),
    ("engineer", "Engineer", "model", ["workshop"], "claude-haiku-5-5"),
    ("researcher", "Researcher", "model", ["observatory", "workshop"], "claude-sonnet-5-5"),
    ("librarian", "Librarian", "model", ["capital", "observatory"], "@cf/google/gemma-4-26b-a4b-it"),
    ("tests", "Test runner", "tool", ["workshop"], "pytest-like-1"),
    ("examiner", "Examiner", "model", ["holdout"], "@cf/meta/llama-3.3-70b-instruct-fp8-fast"),
]


def door_gates() -> list:
    src = (ROOT / "bench" / "cards" / "door" / "worker.js").read_text()
    claude = re.findall(r'"(claude-[a-z0-9-]+)"', src.split("const WORKERS_AI")[0])
    wai = re.findall(r'"(@cf/[^"]+)"', src.split("const WORKERS_AI")[1].split("]);")[0])
    cap = int(re.search(r"MAX_TOKENS = (\d+)", src).group(1))
    return [
        {"id": "door-claude", "to": "Claude models (Anthropic API)", "through": "the door",
         "allows": claude, "rules": [f"text only", f"at most {cap:,} output tokens", "no tools, files or streaming",
                                     "effort low, medium or high only"]},
        {"id": "door-ai", "to": "open models (Cloudflare Workers AI)", "through": "the door",
         "allows": wai, "rules": ["text only", f"at most {cap:,} output tokens", "temperature 0"]},
    ]


def build() -> dict:
    d = tempfile.mkdtemp()
    m = g.Memory(f"{d}/world.jsonl")
    m.register("you", "you", party="you", kind="human", name="You", capabilities=["owner"],
               compartments=list(REGIONS), record_time=T)
    for w, name, kind, comps, model in RESIDENTS:
        m.register("you", w, party=w, kind=kind, name=name, capabilities=["write"] + (["verify"] if kind == "tool" else []),
                   compartments=comps, model=model, operator="you", record_time=T)
    # Real crossings attempted against this log; each must be refused by the gate.
    attempts = [
        ("examiner", "workshop", "The examiner tries to read the workshop's results"),
        ("engineer", "holdout", "The engineer tries to write into the holdout"),
        ("guide", "workshop", "The guide tries to post a result in the workshop"),
    ]
    refused = []
    for who, comp, what in attempts:
        try:
            m.remember(who, g.claim("a crossing", speaker=who, frame="demo", compartment=comp), record_time=T)
            outcome, code = "allowed", None
        except g.GateError as e:
            outcome, code = "refused", e.code
        refused.append({"who": who, "region": comp, "what": what, "outcome": outcome, "code": code})
    assert all(r["outcome"] == "refused" for r in refused), refused
    st = m.state()["state"]
    writers = st["writers"]
    residents = [{"id": w, "name": i.get("name") or w, "kind": i["kind"], "model": i.get("model"),
                  "regions": i["compartments"]} for w, i in writers.items() if w != "you"]
    roads = []
    for a, b in combinations(REGIONS, 2):
        who = [r["id"] for r in residents if a in r["regions"] and b in r["regions"]]
        if who:
            roads.append({"from": a, "to": b, "who": who})
    connected = {x for r in roads for x in (r["from"], r["to"])}
    regions = [{"id": c, "about": REGIONS[c], "residents": [r["id"] for r in residents if c in r["regions"]],
                "isolated_from_residents": c not in connected} for c in REGIONS]
    verify = m.verify()
    return {"built": T, "source": "a real Gnomon log built by bench/demo/world.py; verify ok: " + str(verify["ok"]),
            "regions": regions, "residents": residents, "roads": roads, "gates": door_gates(),
            "refused": refused,
            "refusals_recorded_by_gnomon": False}


if __name__ == "__main__":
    data = build()
    (HERE / "world.json").write_text(json.dumps(data, indent=1) + "\n")
    print(json.dumps({k: (len(v) if isinstance(v, list) else v) for k, v in data.items()}, indent=1))
