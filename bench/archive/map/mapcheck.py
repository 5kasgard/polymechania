"""Derive the Polymechania map from Gnomon registrations under several road
rules and count where it lies (bench/archive/map/PROTOCOL.md).

Flows come from the channels confirmed by probes.py against the real Gnomon
code (probes.json). Scenarios are constructed (scenarios.py). Output:
results.json and a printed table. Run: python3 mapcheck.py
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

from scenarios import SCENARIOS

HERE = Path(__file__).parent
EMIT = {"write", "verify", "spawn", "owner", "govern"}  # every capability can put something into a compartment


def pair(a, b):
    return tuple(sorted((a, b)))


def is_owner(w):
    return bool({"owner", "govern"} & set(w["caps"]))


# ---------------------------------------------------------------- flows
def flows(sc):
    """Every (region pair) -> list of (channel, who, detail) that lets
    information cross, by Gnomon's own rules. Directed flows are recorded
    on the unordered pair with a direction in the detail."""
    regions, ws = sc["regions"], sc["writers"]
    byid = {w["id"]: w for w in ws}
    out = {}

    def add(a, b, chan, who, detail):
        if a != b:
            out.setdefault(pair(a, b), []).append({"channel": chan, "who": who, "detail": detail})

    # F1 agent-mediated (P1, P2, P18, P21): a writer reads every compartment it is
    # in and can emit into each of them. Content-bearing.
    for w in ws:
        for a, b in itertools.combinations(w["comps"], 2):
            if set(w["caps"]) & EMIT:
                bw = "content" if set(w["caps"]) & {"write", "owner"} else (
                    "verdicts only (result per claim; note not shown in scoped state)" if "verify" in w["caps"]
                    else "registration strings (session field, P-extra)")
                add(a, b, "F1 agent holds both", w["id"], bw)

    # F2 structural (P10): a writer in B whose operator is registered only
    # outside B: B's readers learn the operator's id (chosen by the owner).
    for w in ws:
        op = w.get("operator")
        if op and op in byid:
            for b in w["comps"]:
                if b not in byid[op]["comps"]:
                    for a in byid[op]["comps"]:
                        add(a, b, "F2 operator id shown across", w["id"],
                            f"B-readers see operator '{op}' who is only in {byid[op]['comps']} (owner-set metadata)")

    # F3 covert, session-id collision (P11): two writers with spawn, same party
    # and surface, in different compartments: E_IDENTITY refusals carry bits.
    sp = [w for w in ws if "spawn" in w["caps"]]
    for x, y in itertools.combinations(sp, 2):
        if x["party"] == y["party"] and x.get("surface") == y.get("surface"):
            for a in x["comps"]:
                for b in y["comps"]:
                    add(a, b, "F3 covert: session-id collision", f"{x['id']}+{y['id']}",
                        "1 bit per registration attempt, both directions, needs direct library access (no MCP tool)")
    # F3b covert, writer-id namespace (P12): Y's id starts with X's id + '-'.
    for x in sp:
        for y in sp:
            if x is not y and y["id"].startswith(x["id"] + "-"):
                for a in x["comps"]:
                    for b in y["comps"]:
                        add(a, b, "F3b covert: instance-id squatting", f"{x['id']}+{y['id']}",
                            "1 bit per id, E_DUPLICATE, both directions, needs direct library access")

    # F4 deployment (P19, P20): the log is one plaintext file and appends are
    # not authenticated; anything that can open it reads and writes every
    # compartment. Plus any declared off-record carrier (S4b).
    for o in sc.get("offrecord", []):
        add(*o["between"], "F4 off-record carrier", o["who"], o["why"])
    return out


def deployment_pairs(sc):
    return {pair(a, b) for a, b in itertools.combinations(sc["regions"], 2)}


def auto_used(sc):
    """P23: with auto mode, a multi-compartment template's whole conversation
    is recorded into one compartment: the road is used by default."""
    h = sc.get("hook")
    if not h:
        return []
    t = next(w for w in sc["writers"] if w["id"] == h["template"])
    return [{"from": c, "into": h["records_to"], "who": t["id"]} for c in t["comps"] if c != h["records_to"]]


# ---------------------------------------------------------------- road rules
def roads(sc, rule):
    ws = sc["writers"]
    r = {}
    for w in ws:
        if rule == "R1b" and is_owner(w):
            continue
        if rule == "R2":
            if is_owner(w) or not (set(w["caps"]) & {"write"}):
                continue  # R2: only writers who can put content (claims) there
        for a, b in itertools.combinations(w["comps"], 2):
            r.setdefault(pair(a, b), []).append(w["id"])
    return r


RULES = {
    "R1a": "road iff some writer (owner included) holds both compartments",
    "R1b": "road iff some non-owner, non-governor writer holds both",
    "R2": "road iff some non-owner writer with 'write' holds both (content roads only)",
    "R3": "R1b roads, each labelled with who can cross; owner drawn as able to build any road; covert links "
          "drawn dotted; plus a standing note that file access crosses everything",
}


def evaluate(sc, rule):
    regions, ws = sc["regions"], sc["writers"]
    fl = flows(sc)
    base_rule = "R1b" if rule == "R3" else rule
    rd = roads(sc, base_rule)
    shown = set(rd)
    if rule == "R3":
        # R3 additionally shows owner-only links and covert links (labelled), so
        # they are not hidden; they are on the map in their own style.
        for p, fs in fl.items():
            if any(f["channel"].startswith(("F1", "F2", "F3")) for f in fs):
                shown.add(p)
    protocol = {p: [f for f in fs if not f["channel"].startswith("F4")] for p, fs in fl.items()}
    protocol = {p: fs for p, fs in protocol.items() if fs}
    content = {p: fs for p, fs in protocol.items() if any(f["channel"].startswith("F1") for f in fs)}

    hidden = {p: fs for p, fs in protocol.items() if p not in shown}
    hidden_content = {p: fs for p, fs in hidden.items() if p in content}
    offrec = {p: fs for p, fs in fl.items() if any(f["channel"].startswith("F4") for f in fs) and p not in shown}

    # misleading roads: a drawn (unlabelled) road where some member of an end cannot cross alone
    mis = {}
    if rule != "R3":
        for p, crossers in rd.items():
            members = {w["id"] for w in ws if set(p) & set(w["comps"])}
            cannot = sorted(members - set(crossers))
            if cannot:
                mis[p] = {"crossers": crossers, "cannot_cross": cannot}
    owner_only = [p for p, c in roads(sc, "R1a").items()
                  if all(is_owner(next(w for w in ws if w["id"] == x)) for x in c)]
    drawn_islands = [r for r in regions if not any(r in p for p in shown)]
    false_islands = [r for r in drawn_islands if any(r in p for p in protocol)]
    false_islands_dep = [r for r in drawn_islands if any(r in p for p in offrec)]
    return {
        "roads": {"-".join(p): c for p, c in rd.items()},
        "hidden_bridges": {"-".join(p): fs for p, fs in hidden.items()},
        "H_protocol": len(hidden), "H_content": len(hidden_content),
        "H_offrecord": len(offrec),
        "M_roads": len(mis), "M_pairs": sum(len(v["cannot_cross"]) for v in mis.values()),
        "misleading": {"-".join(p): v for p, v in mis.items()},
        "owner_only_roads": ["-".join(p) for p in owner_only],
        "drawn_islands": drawn_islands, "false_islands": false_islands,
        "false_islands_if_file_access": [r for r in drawn_islands],  # P19/P20: file access reaches every region
        "false_islands_offrecord": false_islands_dep,
    }


def intended(sc):
    """Do the registrations keep the scenario's intended islands isolated?"""
    fl = flows(sc)
    res = {}
    for isl in sc.get("intended_islands", []):
        touching = {"-".join(p): fs for p, fs in fl.items() if isl in p}
        res[isl] = {"isolated_in_protocol": not any(not f["channel"].startswith("F4")
                                                    for fs in touching.values() for f in fs),
                    "flows": touching}
    return res


def reach(sc):
    """Per agent: regions it reads directly (Gnomon enforces this), and
    regions whose content can reach it if every bridge writer (owner
    excluded, then included) passes things on (Gnomon cannot enforce this)."""
    ws = sc["writers"]
    out = {}
    for incl_owner in (False, True):
        adj = {r: set() for r in sc["regions"]}
        for w in ws:
            if is_owner(w) and not incl_owner:
                continue
            for a, b in itertools.combinations(w["comps"], 2):
                adj[a].add(b)
                adj[b].add(a)
        for w in ws:
            seen, stack = set(w["comps"]), list(w["comps"])
            while stack:
                for n in adj[stack.pop()]:
                    if n not in seen:
                        seen.add(n)
                        stack.append(n)
            d = out.setdefault(w["id"], {"direct": sorted(w["comps"])})
            d["via_bridges_with_owner" if incl_owner else "via_bridges"] = sorted(seen)
    return out


def main():
    out = {"rules": RULES, "probes": json.loads((HERE / "probes.json").read_text()), "scenarios": []}
    rows = []
    for sc in SCENARIOS:
        rec = {"id": sc["id"], "source": sc["source"], "constructed": True, "regions": sc["regions"],
               "flows": {"-".join(p): fs for p, fs in flows(sc).items()}, "auto_used": auto_used(sc),
               "intended_islands": intended(sc), "reach": reach(sc), "by_rule": {},
               "offrecord_carriers_on_no_road": [o["who"] for o in sc.get("offrecord", [])]}
        for rule in RULES:
            e = evaluate(sc, rule)
            rec["by_rule"][rule] = e
            rows.append((sc["id"], rule, e["H_protocol"], e["H_content"], e["H_offrecord"], e["M_roads"],
                         e["M_pairs"], len(e["owner_only_roads"]), ",".join(e["false_islands"]) or "-"))
        out["scenarios"].append(rec)
    (HERE / "results.json").write_text(json.dumps(out, indent=2))
    hdr = ("scen", "rule", "H_proto", "H_content", "H_offrec", "M_roads", "M_pairs", "owner_only", "false_isl")
    print("  ".join(f"{h:>9}" for h in hdr))
    for r in rows:
        print("  ".join(f"{str(x):>9}" for x in r))
    tot = {}
    for r in rows:
        t = tot.setdefault(r[1], [0, 0, 0, 0, 0, 0])
        for i, v in enumerate((r[2], r[3], r[4], r[5], r[6], 1 if r[8] != "-" else 0)):
            t[i] += v
    print("\ntotals per rule (H_proto, H_content, H_offrec, M_roads, M_pairs, scenarios with a false island):")
    for k, v in tot.items():
        print(f"  {k}: {v}")
    print("\nintended islands:")
    for s in out["scenarios"]:
        for isl, v in s["intended_islands"].items():
            print(f"  {s['id']} {isl}: isolated in protocol = {v['isolated_in_protocol']}; "
                  f"flows via {sorted({f['channel'] + ' by ' + f['who'] for fs in v['flows'].values() for f in fs})}")
    print("\nagents whose transitive reach (via non-owner bridges) exceeds direct reach:")
    for s in out["scenarios"]:
        for w, r in s["reach"].items():
            if r["via_bridges"] != r["direct"]:
                print(f"  {s['id']} {w}: direct {r['direct']} -> via bridges {r['via_bridges']}")
    for s in out["scenarios"]:
        if s["offrecord_carriers_on_no_road"]:
            print(f"  {s['id']} carriers outside the record, on no road under any rule: {s['offrecord_carriers_on_no_road']}")
    for s in out["scenarios"]:
        if s["auto_used"]:
            print(f"  {s['id']} auto mode uses roads by default: {s['auto_used']}")


if __name__ == "__main__":
    main()
