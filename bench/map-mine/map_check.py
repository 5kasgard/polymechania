"""Is the map honest? The conductor's own check (see PROTOCOL.md).

Findings from reading Gnomon's gate (crates/gnomon-core/src/ledger.rs) and
Python API, which this script builds on:
- Every write needs the writer to hold the target compartment
  (need_compartment); references, citations, supersession, dispute evidence
  and handoff refs are refused across compartments; an instance cannot
  enter a compartment its parent is not in.
- Reads (query, recall, resume, writers) are scoped to the reader's own
  compartments; there is no owner bypass in the API.
- Capabilities are global to a writer, not per compartment: a writer that
  can write (claims, questions, verdicts with a free-text method) in one
  compartment can write in all of its compartments.
So inside Gnomon, content crosses from A to B only through a writer that
holds both and can write: it reads in A and writes in B. Over time this
chains: A to B by one writer, B to C by another, is A to C.
Outside Gnomon's view: anyone who can read the log file (it is plain JSONL
holding every compartment), one program or person holding several writers'
credentials, and a human copying by hand.
Constructed scenarios, labelled as such; no real usage logs exist here."""

from itertools import combinations

SCENARIOS = {
    "personal world (constructed)": {
        "john (person, owner)": ({"private", "work", "commons-link"}, True, "person"),
        "claude session 1": ({"work"}, True, "model"),
        "claude session 2": ({"work", "private"}, True, "model"),
        "calculator": ({"work"}, True, "tool"),
        "publisher agent": ({"commons-link"}, True, "model"),
        "reader agent": ({"private"}, False, "model"),  # can read, cannot write
    },
    "E1 experiment (constructed)": {
        "conductor": ({"items", "answers"}, True, "model"),
        "worker haiku": ({"items"}, True, "model"),
        "worker sonnet": ({"items"}, True, "model"),
        "auditor": ({"answers"}, True, "tool"),
    },
    "grants seen in Gnomon's tests (constructed from them)": {
        "john (person, owner)": ({"lab", "private"}, True, "person"),
        "claude-c1": ({"lab"}, True, "model"),
        "chat agent": ({"chat", "private"}, True, "model"),
        "acme staff": ({"acme"}, True, "model"),
        "acme liaison": ({"acme", "other"}, True, "model"),
        "outsider": ({"other"}, True, "person"),
    },
}

# What a naive map would draw if the owner declared roads by intention.
DECLARED = {
    "personal world (constructed)": {frozenset({"work", "commons-link"})},  # private drawn as an island
    "E1 experiment (constructed)": set(),  # answers drawn as an island
    "grants seen in Gnomon's tests (constructed from them)": {frozenset({"acme", "other"})},
}


def carriers(writers, include=lambda kind: True):
    """Road A-B -> the writers who can carry content between them."""
    roads = {}
    for name, (comps, can_write, kind) in writers.items():
        if not can_write or not include(kind):
            continue
        for a, b in combinations(sorted(comps), 2):
            roads.setdefault(frozenset({a, b}), []).append(name)
    return roads


def components(regions, edges):
    parent = {r: r for r in regions}
    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x
    for e in edges:
        a, b = tuple(e)
        parent[find(a)] = find(b)
    groups = {}
    for r in regions:
        groups.setdefault(find(r), set()).add(r)
    return [g for g in groups.values()]


def reach(regions, edges):
    """Pairs (A, B) between which content can travel, directly or chained."""
    out = set()
    for g in components(regions, edges):
        for a, b in combinations(sorted(g), 2):
            out.add(frozenset({a, b}))
    return out


for name, writers in SCENARIOS.items():
    regions = set().union(*(c for c, _, _ in writers.values()))
    true_roads = carriers(writers)
    true_reach = reach(regions, true_roads)
    agent_roads = carriers(writers, include=lambda k: k != "person")
    agent_reach = reach(regions, agent_roads)
    declared = DECLARED[name]
    declared_reach = reach(regions, declared)
    print(f"\n== {name}")
    print(f"regions: {', '.join(sorted(regions))}")
    print("R1, roads by writer (who can carry):")
    for road, who in sorted(true_roads.items(), key=lambda x: sorted(x[0])):
        print(f"   {' - '.join(sorted(road))}: {', '.join(who)}")
    islands = [r for r in regions if not any(r in road for road in true_roads)]
    print(f"   islands: {', '.join(sorted(islands)) or 'none'}")
    print(f"   hidden bridges: 0 by construction (every carrier draws its road); "
          f"chained reach shown by following roads: {len(true_reach)} pair(s)")
    print("R1 for agents only (people shown separately):")
    a_islands = [r for r in regions if not any(r in road for road in agent_roads)]
    print(f"   roads: {', '.join(' - '.join(sorted(r)) for r in agent_roads) or 'none'}; "
          f"islands for agents: {', '.join(sorted(a_islands)) or 'none'}")
    hidden = true_reach - declared_reach
    misleading = [r for r in declared if r not in true_reach]
    print("R2, roads as declared by intention:")
    print(f"   hidden bridges (content can travel, no road path drawn): {len(hidden)}"
          + (f" -> {', '.join(' - '.join(sorted(p)) for p in sorted(hidden, key=sorted))}" if hidden else ""))
    print(f"   misleading roads (drawn, no carrier): {len(misleading)}")
    unlabelled = [(r, who) for r, who in true_roads.items() if len(who) < sum(1 for c, w, _ in writers.values() if w and (r & c))]
    print(f"   roads that would mislead if unlabelled (most writers on either side cannot cross): {len(unlabelled)}")

print("\nOutside Gnomon's view in every scenario: readers of the log file (plain JSONL, all")
print("compartments), one program or person holding several writers' credentials, copy by hand.")
