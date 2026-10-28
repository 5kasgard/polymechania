"""Scenarios for the map honesty test. ALL ARE CONSTRUCTED, NOT OBSERVED:
no real Gnomon log with writer registrations exists on this machine
(searched /home/claude, /tmp and both repos on 2026-10-28; only benchmark
answer files and fixtures). Each is taken from a named source.

A writer: (id, party, kind, caps, compartments, extra) where extra may hold
operator, surface, session, spawn_of, name.
"""

W = lambda id, party, kind, caps, comps, **x: dict(id=id, party=party, kind=kind, caps=caps, comps=comps, **x)  # noqa: E731

SCENARIOS = [
    {
        "id": "S1", "source": "Gnomon README quick start (init + register claude, --per-session)",
        "regions": ["work", "private"],
        "writers": [
            W("john", "john", "human", ["owner"], ["work", "private"]),
            W("claude", "anthropic", "model", ["write", "verify", "spawn"], ["work"], operator="john",
              surface="claude-code", name="Claude"),
            W("claude-1", "anthropic", "model", ["write", "verify"], ["work"], operator="john",
              surface="claude-code", session="s1", spawn_of="claude", name="Claude"),
            W("claude-2", "anthropic", "model", ["write", "verify"], ["work"], operator="john",
              surface="claude-code", session="s2", spawn_of="claude", name="Claude"),
        ],
        "hook": {"template": "claude", "records_to": "work"},
        "intended_islands": ["private"],
    },
    {
        "id": "S2", "source": "Gnomon python/tests/test_mcp.py fixture + ReviewM4 (calc2, a checker in lab and private)",
        "regions": ["lab", "private"],
        "writers": [
            W("john", "john", "human", ["owner"], ["lab", "private"]),
            W("claude-c1", "anthropic", "model", ["write", "verify"], ["lab"], operator="john"),
            W("gpt-g1", "openai", "model", ["write", "verify"], ["lab"], operator="john"),
            W("calc", "gnomon-calc", "tool", ["verify"], ["lab"], operator="john"),
            W("calc2", "gnomon-calc2", "tool", ["verify"], ["lab", "private"], operator="john"),
        ],
        "intended_islands": ["private"],
    },
    {
        "id": "S3", "source": "Gnomon python/tests/test_identity.py ReviewM6 (operator lives only in private)",
        "regions": ["lab", "private"],
        "writers": [
            W("root", "root", "human", ["owner"], ["private", "lab"], name="Root Admin"),
            W("reader", "reader", "human", ["write"], ["lab"]),
            W("op", "op", "human", ["write"], ["private"], name="Secret Operator"),
            W("claude", "anthropic", "model", ["write", "spawn"], ["lab"], operator="op", name="Claude"),
        ],
        "intended_islands": ["private"],
    },
    {
        "id": "S4a", "source": "Polymechania prereg/cards-v2.md E1, mapped onto compartments; conductor registered",
        "regions": ["work", "answers", "archive"],
        "writers": [
            W("alex", "alex", "human", ["owner"], ["work", "answers", "archive"]),
            W("conductor", "anthropic", "model", ["write", "verify"], ["work", "answers", "archive"],
              operator="alex", name="Conductor"),
            W("haiku-1", "anthropic", "model", ["write"], ["work"], operator="alex"),
            W("sonnet-1", "anthropic", "model", ["write"], ["work"], operator="alex"),
            W("gemma", "google", "model", ["verify"], ["work"], operator="alex"),
            W("opus-judge", "anthropic-judge", "model", ["verify"], ["work"], operator="alex"),
            W("audit", "gnomon-audit", "tool", ["verify"], ["work", "answers"], operator="alex"),
        ],
        "intended_islands": ["answers"],
        "note": "E1 needs answers isolated from workers; conductor and audit must see both.",
    },
    {
        "id": "S4b", "source": "E1 as actually designed (cards-v2 amendment B): the conductor holds answers in its "
                               "context, outside Gnomon; workers called text-in, text-out by a harness",
        "regions": ["work", "answers"],
        "writers": [
            W("alex", "alex", "human", ["owner"], ["work", "answers"]),
            W("haiku-1", "anthropic", "model", ["write"], ["work"], operator="alex"),
            W("sonnet-1", "anthropic", "model", ["write"], ["work"], operator="alex"),
            W("gemma", "google", "model", ["verify"], ["work"], operator="alex"),
            W("audit", "gnomon-audit", "tool", ["verify"], ["answers"], operator="alex"),
        ],
        "offrecord": [{"who": "conductor session (unregistered)", "between": ["answers", "work"],
                       "why": "holds the answers in context and writes every worker prompt"}],
        "intended_islands": ["answers"],
    },
    {
        "id": "S5", "source": "Polymechania tests/test_company.py, extended to two firms and one client who orders "
                              "from both (spec 15: a work order is a question in the firm's compartment)",
        "regions": ["acme", "beta"],
        "writers": [
            W("john", "john", "human", ["owner"], ["acme", "beta"], name="John"),
            W("acme-haiku", "acme", "model", ["write", "spawn"], ["acme"], operator="john"),
            W("acme-opus", "acme", "model", ["write", "spawn"], ["acme"], operator="john"),
            W("beta-sonnet", "beta", "model", ["write", "spawn"], ["beta"], operator="john"),
            W("tests", "test-runner", "tool", ["write", "verify"], ["acme", "beta"], operator="john"),
            W("client", "anthropic-chat", "model", ["write"], ["acme", "beta"], operator="john"),
        ],
        "intended_islands": [],
    },
    {
        "id": "S6", "source": "Vision scene 2 world: several regions, one with a road to the commons; auto mode "
                              "(README hooks) with one Claude template for work and health",
        "regions": ["work", "health", "finance", "commons"],
        "writers": [
            W("alex", "alex", "human", ["owner"], ["work", "health", "finance", "commons"], name="Alex"),
            W("claude", "anthropic", "model", ["write", "verify", "spawn"], ["work", "health"], operator="alex",
              surface="claude-code", name="Claude"),
            W("claude-1", "anthropic", "model", ["write", "verify"], ["work", "health"], operator="alex",
              surface="claude-code", session="s1", spawn_of="claude", name="Claude"),
            W("gpt", "openai", "model", ["write", "verify"], ["work"], operator="alex"),
            W("ledger-bot", "bank-tool", "tool", ["write"], ["finance"], operator="alex"),
            W("herald", "anthropic-herald", "model", ["write"], ["work", "commons"], operator="alex"),
        ],
        "hook": {"template": "claude", "records_to": "work"},
        "intended_islands": ["finance"],
    },
    {
        "id": "S7", "source": "The natural way to keep two regions apart in Claude Code: two Claude templates, "
                              "one per region (README register, twice), both with spawn, same party and surface",
        "regions": ["work", "private"],
        "writers": [
            W("alex", "alex", "human", ["owner"], ["work", "private"], name="Alex"),
            W("claude", "anthropic", "model", ["write", "verify", "spawn"], ["work"], operator="alex",
              surface="claude-code", name="Claude"),
            W("claude-private", "anthropic", "model", ["write", "verify", "spawn"], ["private"], operator="alex",
              surface="claude-code", name="Claude"),
        ],
        "intended_islands": ["private"],
    },
]
