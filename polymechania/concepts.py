"""The plain vocabulary: every thing a world may rename, every rule it may
name but never change, and every kind of event it may retell.

This file is the contract between the core and the worlds. The core speaks
only in these terms. A world (see `worlds.py`) maps them to its own names,
voice and look. Anything a world says must trace back to an entry here,
which is what keeps a costume from hiding what happened.
"""

from __future__ import annotations

# ------------------------------------------------------------- concepts
# key -> (plain name, what it is). Worlds rename the plain name; the key
# and the meaning never change.

CONCEPTS: dict[str, tuple[str, str]] = {
    # the place
    "org": ("the organisation", "everyone and everything working for one person or team"),
    "leader": ("the owner", "the person the organisation works for; only they set its rules"),
    "archive": ("the record", "where every order, result and verdict is kept for good (Gnomon)"),
    "inspector": ("independent review", "checks accepted work and answers only to the owner"),
    "rules": ("the rules", "what the core enforces, whatever the world calls it"),
    "merit": ("track record", "verdicts on past work, from which future work is assigned"),
    "formation": ("form", "how a team is organised for one piece of work"),
    "task": ("task", "one unit of work"),
    "part": ("part", "one of a task's independent pieces"),
    # tiers of model
    "tier.haiku": ("Haiku", "the cheapest model tier: fast, does most of the work"),
    "tier.sonnet": ("Sonnet", "the middle tier: manages, and takes what Haiku fails"),
    "tier.opus": ("Opus", "the top general tier: vague, coupled, high-stakes work"),
    "tier.fable": ("Fable", "the frontier tier: kept for what nothing else can do"),
    # kinds of worker that are not models
    "worker.checker": ("an exact check", "tests, calculators and verifiers: never wrong about what they check"),
    "worker.calculator": ("calculator", "exact arithmetic and dates"),
    "worker.prover": ("prover", "theorem provers and solvers: slow, final"),
    "worker.script": ("script", "a cheap program built once for one repeated chore"),
    "worker.swarm": ("swarm", "many tiny learners voting: Mycel's nuclei, boosted stumps"),
    "worker.model": ("model", "a language model: improvises, can be wrong, never grades itself"),
    # roles on a team
    "role.executive": ("planner", "splits the work and assembles the result"),
    "role.manager": ("manager", "reads its reports' summaries and passes one up"),
    "role.staff": ("worker", "does a part"),
    "role.escalation": ("escalation", "a stronger worker called when a check fails"),
    "role.reviewer": ("reviewer", "judges a part when no exact check exists"),
    # how a part is checked, and how a cascade is told
    "check.exact": ("checked exactly", "a test or verifier decides"),
    "check.review": ("reviewed", "another worker judges the result"),
    "check.none": ("unchecked", "the first result is kept"),
    "word.then": ("then", "joins a cascade: cheapest first, the next only if a check fails"),
    "word.by": ("by", "joins a review to its reviewer"),
    # how much is at stake on one part
    "rank.d": ("routine", "under $0.10 at stake"),
    "rank.c": ("minor", "$0.10 to $1 at stake"),
    "rank.b": ("moderate", "$1 to $10 at stake"),
    "rank.a": ("major", "$10 to $100 at stake"),
    "rank.s": ("critical", "$100 or more at stake"),
}

# --------------------------------------------------------------- rules
# What the core enforces. A world may give each a name and a line of its
# own (a precept, an article, a ship's rule); it cannot add, drop or soften
# one, because rules are not read from worlds at all.

RULES: dict[str, str] = {
    "no-self-grading": "No one grades their own work, and no model judges its own model's work.",
    "outside-verdicts": "Only verdicts from outside a worker's own group count on its record.",
    "clones-count-once": "Copies of one model are one witness: they fail together.",
    "honesty-free": "Escalating, asking for help or reporting a part undone never counts against anyone.",
    "assurance-apart": "Independent review answers to the owner alone; no one can remove the check on themselves.",
    "cheapest-capable": "Each part goes to the cheapest worker that does it reliably on the record.",
    "plain-underneath": "Everything is recorded plainly; any world can be switched off to see what happened.",
}

# -------------------------------------------------------------- events
# kind -> (plain template, required facts). A world's template for a kind
# must use every required fact, so no world can leave out a cost, a
# chance of being right or a number of workers. Names in facts (tiers,
# roles, ranks) are given in the world's own words; numbers are never
# reworded.

EVENTS: dict[str, tuple[str, tuple[str, ...]]] = {
    "mission": ("{task_name}: {parts} {part_name}(s) of '{kind}', {rank} ({stakes} at stake each), check: {check}",
                ("parts", "kind", "rank", "stakes", "check")),
    "formation": ("{formation_name}: {word}", ("word",)),
    "post": ("  {role}: {count} × {tier}", ("role", "count", "tier")),
    "part": ("  each {part_name}: {workers}, {checked} (right {p_right})", ("workers", "checked", "p_right")),
    "cost": ("  expected: {spend} on tokens + {loss} lost{waiting} = {total}; {rounds} round(s) at most",
             ("spend", "loss", "waiting", "total", "rounds")),
    "baseline": ("  one {tier} alone: {total}; {rounds} round(s) expected",
                 ("tier", "total", "rounds")),
    "note": ("  note: {text}", ("text",)),
    "rule": ("  {rule}", ("rule",)),
}

# Facts a template may use beyond the required ones: the world's own names
# for things, looked up from CONCEPTS.
NAME_FACTS = {
    "task_name": "task", "part_name": "part", "formation_name": "formation", "rule_name": "rules",
    "leader_name": "leader", "archive_name": "archive", "inspector_name": "inspector", "merit_name": "merit",
}
# Facts a world supplies itself: its own line for the rule an event states.
WORLD_FACTS = ("precept",)


def rank_of(stakes_usd: float) -> str:
    """The rank key for what one part puts at stake."""
    for limit, key in ((0.10, "rank.d"), (1.0, "rank.c"), (10.0, "rank.b"), (100.0, "rank.a")):
        if stakes_usd < limit:
            return key
    return "rank.s"
