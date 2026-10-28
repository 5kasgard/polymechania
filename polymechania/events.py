"""Events: the one seam between the work and every way of showing it.

The core never prints. It produces plain events; a view (the `mekh`
terminal, a dashboard, a map) turns them into lines, tiles or buildings in
a world's style. Each event carries two kinds of facts:

* **names**, given as concept keys (`tier.haiku`, `role.staff`): a world
  may call them whatever it likes;
* **values**, already written out (`$0.0123`, `97.2%`, `4`): no world can
  reword them.

So the same event reads as a ship's log, a village scroll or a plain line,
and the numbers are the same in all of them.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Union

from . import concepts

Name = Union[str, list]  # a concept key, or a list of them (a cascade)


@dataclass(frozen=True)
class Event:
    kind: str
    names: dict = field(default_factory=dict)  # fact -> concept key (or list of keys)
    values: dict = field(default_factory=dict)  # fact -> text that no world rewords

    def __post_init__(self):
        if self.kind not in concepts.EVENTS:
            raise ValueError(f"unknown event kind {self.kind!r}")
        for fact, key in self.names.items():
            for k in key if isinstance(key, list) else [key]:
                if k not in concepts.CONCEPTS:
                    raise ValueError(f"{fact}: unknown concept {k!r}")
        missing = set(concepts.EVENTS[self.kind][1]) - set(self.names) - set(self.values)
        if missing:
            raise ValueError(f"{self.kind} event lacks {', '.join(sorted(missing))}")

    def as_dict(self) -> dict:
        return {"kind": self.kind, "names": dict(self.names), "values": dict(self.values)}


# ------------------------------------------------------------ formatting

def usd(x: float) -> str:
    """Cents above a dollar, hundredths of a cent below it."""
    return f"${x:,.2f}" if x >= 1 else f"${x:.4f}"


def pct(p: float) -> str:
    """A chance, with enough digits that nothing short of certain reads as 100%."""
    for digits in range(1, 5):
        s = f"{p:.{digits}%}"
        if p >= 1 or not s.startswith("100"):
            return s
    return "<100%"


_ROLE = re.compile(r"^(executive|managers|staff|escalations|reviews)")
_ROLE_KEY = {"executive": "role.executive", "managers": "role.manager", "staff": "role.staff",
             "escalations": "role.escalation", "reviews": "role.reviewer"}


def _role_key(role: str) -> str:
    m = _ROLE.match(role)
    if not m:
        raise ValueError(f"unknown role {role!r}")
    return _ROLE_KEY[m.group(1)]


def _check_names(reviewer) -> list:
    if reviewer is None:
        return ["check.none"]
    if reviewer == "exact":
        return ["check.exact"]
    return ["check.review", f"tier.{reviewer}"]


# ------------------------------------------------------------- narrators

def from_plan(p) -> list:
    """A plan (`polymechania.plan.Plan`) as events, in the order a reader
    wants them: the task, who works on it, how each part is done, what it
    should cost, and the same work done by one agent alone."""
    t = p.task
    out = [Event("mission",
                 names={"rank": concepts.rank_of(t.stakes_usd), "check": f"check.{t.check}"},
                 values={"parts": str(t.parts), "kind": t.kind, "stakes": usd(t.stakes_usd)})]
    for role, tier, n in p.floors:
        floor = re.search(r"floor (\d+)", role)
        out.append(Event("post", names={"role": _role_key(role), "tier": f"tier.{tier}"},
                         values={"count": str(n) + (f" (floor {floor.group(1)})" if floor else "")}))
    out.append(Event("part", names={"workers": [f"tier.{w}" for w in p.unit.workers],
                                    "checked": _check_names(p.unit.reviewer)},
                     values={"p_right": pct(p.unit.p_right)}))
    waiting = f" + {usd(t.step_usd * p.rounds)} waiting" if t.step_usd else ""
    out.append(Event("cost", values={"spend": usd(p.spend), "loss": usd(p.loss), "waiting": waiting,
                                     "total": usd(p.total), "rounds": str(p.rounds)}))
    out.append(Event("baseline", names={"tier": f"tier.{p.single}"},
                     values={"total": usd(p.baseline_total), "rounds": f"{p.baseline_rounds:.1f}"}))
    for n in p.notes:
        out.append(Event("note", values={"text": n}))
    return out


def from_design(d) -> list:
    """A form (`polymechania.forms.Design`) as events: its word, then each
    stage and why it was chosen."""
    from .forms import ALPHABET
    out = [Event("formation", values={"word": d.word})]
    for s in d.stages:
        out.append(Event("note", values={"text": f"{s.spell()} {ALPHABET[s.letter].name}: {s.why}"}))
    for w, y in d.considered:
        out.append(Event("note", values={"text": f"not {w}: {y}"}))
    for w in d.warnings:
        out.append(Event("note", values={"text": f"! {w}"}))
    return out


def rules() -> list:
    """Every rule the core enforces, as events."""
    return [Event("rule", values={"rule": text, "rule_id": rid}) for rid, text in concepts.RULES.items()]
