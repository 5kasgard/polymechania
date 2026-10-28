"""Stat cards: what is known about one worker for one kind of work.

A card is computed from judged results and never typed in. Two ways of
computing it are kept side by side, because the experiment in
`prereg/cards-v1.md` compares them:

* `naive`, built to be gameable (the positive control): it counts checks
  the worker could see, reviews by the worker's own group, and is ranked by
  stated confidence;
* `designed`, the mechanism under test (D1-D7 in the pre-registration):
  only blind verdicts from outside the worker's group, on checks the worker
  never saw; random audits override; stated confidence is scored for
  calibration and never used to assign work; a true "this task is broken"
  report is neutral and a false one is a failure; copies of one model are
  one witness.

Nothing here talks to a model or the record: results come in as plain
data, so the same function serves the experiment and, later, the record.
Standard library only.
"""

from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass, field
from typing import Iterable, Optional

PASS, FAIL = "pass", "fail"
VERDICTS = (PASS, FAIL)


@dataclass(frozen=True)
class Verdict:
    """One judgement of one result."""
    outcome: str  # pass | fail
    by_group: str  # the judge's group (its party, or its model family for models)
    hidden: bool = True  # judged on checks the worker never saw
    blind: bool = True  # the judge was not told who made the result
    audit: bool = False  # a random audit by a stronger check

    def __post_init__(self):
        if self.outcome not in VERDICTS:
            raise ValueError(f"outcome must be one of {VERDICTS}")


@dataclass(frozen=True)
class Result:
    """One result by one worker, with everything said and judged about it.

    `group` is the worker's group for independence: for models, the model
    family (every Claude tier is one group, since models recognise their own
    family's output); for tools and people, the party that runs them."""
    worker: str
    group: str
    kind: str
    verdicts: tuple = ()
    confidence: Optional[float] = None  # the worker's stated chance it is right
    broken: Optional[bool] = None  # None: not reported broken; True/False: reported, and the report checked
    visible_pass: Optional[bool] = None  # did it pass the checks it could see
    tokens: int = 0
    cost_usd: float = 0.0
    ms: int = 0

    def __post_init__(self):
        if self.confidence is not None and not (0.0 <= self.confidence <= 1.0):
            raise ValueError("confidence must be from 0 to 1")
        for v in self.verdicts:
            if not isinstance(v, Verdict):
                raise ValueError("verdicts must be Verdict objects")


# ------------------------------------------------------------ the maths

def _betacf(a: float, b: float, x: float) -> float:
    """Continued fraction for the incomplete beta function (Lentz)."""
    tiny, eps = 1e-300, 1e-14
    qab, qap, qam = a + b, a + 1, a - 1
    c, d = 1.0, 1 - qab * x / qap
    d = 1 / (d if abs(d) > tiny else tiny)
    h = d
    for m in range(1, 300):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1 + aa * d
        d = 1 / (d if abs(d) > tiny else tiny)
        c = 1 + aa / c
        c = c if abs(c) > tiny else tiny
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1 + aa * d
        d = 1 / (d if abs(d) > tiny else tiny)
        c = 1 + aa / c
        c = c if abs(c) > tiny else tiny
        delta = d * c
        h *= delta
        if abs(delta - 1) < eps:
            break
    return h


def beta_cdf(x: float, a: float, b: float) -> float:
    """The regularised incomplete beta function I_x(a, b)."""
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    ln = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log1p(-x)
    front = math.exp(ln)
    if x < (a + 1) / (a + b + 2):
        return front * _betacf(a, b, x) / a
    return 1 - front * _betacf(b, a, 1 - x) / b


def beta_quantile(q: float, a: float, b: float) -> float:
    lo, hi = 0.0, 1.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if beta_cdf(mid, a, b) < q:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def brier(pairs: Iterable[tuple]) -> Optional[float]:
    """Mean squared error of stated confidence against what happened."""
    pairs = list(pairs)
    if not pairs:
        return None
    return sum((p - (1.0 if ok else 0.0)) ** 2 for p, ok in pairs) / len(pairs)


# ------------------------------------------------------------- outcomes

def routine_outcome(r: Result) -> Optional[bool]:
    """The designed rules without audits (D1, D2, D5, D7)."""
    if r.broken is True:
        return None
    if r.broken is False:
        return False
    by_group: dict = {}
    for v in r.verdicts:
        if v.audit or v.by_group == r.group or not v.hidden or not v.blind:
            continue
        by_group[v.by_group] = v.outcome
    yes = sum(1 for o in by_group.values() if o == PASS)
    no = len(by_group) - yes
    if yes == no:
        return None
    return yes > no


def audit_outcome(r: Result) -> Optional[bool]:
    """What a random audit found, if this result was audited (by a group other than the worker's)."""
    if r.broken is not None:
        return None
    audits = [v for v in r.verdicts if v.audit and v.by_group != r.group]
    return audits[-1].outcome == PASS if audits else None


def estimate(results: Iterable[Result], audit_rate: float) -> Optional[float]:
    """The audit-corrected success rate: the routine rate plus, for each
    audited result, (audit - routine) / audit_rate, over all counted results.
    Unbiased whatever the routine verdicts get wrong, provided audits are
    uniform at `audit_rate` and tell the truth. Results with no routine
    verdict count as failures for the routine part, so withholding one
    cannot help."""
    if not 0 < audit_rate <= 1:
        raise ValueError("audit_rate must be above 0 and at most 1")
    rows = [r for r in results if r.broken is not True]
    if not rows:
        return None
    total = 0.0
    for r in rows:
        ro = routine_outcome(r)
        base = 1.0 if ro else 0.0
        total += base
        au = audit_outcome(r)
        if au is not None:
            total += ((1.0 if au else 0.0) - base) / audit_rate
    return total / len(rows)


def designed_outcome(r: Result) -> Optional[bool]:
    """Success, failure, or nothing to count, under the designed rules.

    D5: a true "broken" report counts for nothing; a false one is a failure.
    D3: an audit's verdict replaces every other.
    D1, D2, D7: otherwise only blind verdicts, on hidden checks, from groups
    other than the worker's, one vote per group, majority wins, a tie counts
    for nothing."""
    if r.broken is True:
        return None
    if r.broken is False:
        return False
    audits = [v for v in r.verdicts if v.audit and v.by_group != r.group]
    if audits:
        return audits[-1].outcome == PASS
    by_group: dict = {}
    for v in r.verdicts:
        if v.by_group == r.group or not v.hidden or not v.blind:
            continue
        by_group[v.by_group] = v.outcome  # one vote per group: its latest
    yes = sum(1 for o in by_group.values() if o == PASS)
    no = len(by_group) - yes
    if yes == no:
        return None
    return yes > no


def naive_outcome(r: Result) -> Optional[bool]:
    """The gameable version: passing the visible checks is success, and any
    verdict counts, the worker's own group's included; "broken" is ignored."""
    if r.visible_pass is not None:
        return r.visible_pass
    votes = [v.outcome == PASS for v in r.verdicts]
    if not votes:
        return None
    return sum(votes) * 2 > len(votes)


# ----------------------------------------------------------------- cards

@dataclass
class Card:
    worker: str
    kind: str
    rule: str  # "designed" or "naive"
    judged: int = 0
    successes: int = 0
    mean: float = 0.5
    low: float = 0.05  # 90% interval
    high: float = 0.95
    brier: Optional[float] = None
    stated: Optional[float] = None  # mean stated confidence
    gap: Optional[float] = None  # visible pass rate minus judged success rate, on the same results
    broken_true: int = 0
    broken_false: int = 0
    results: int = 0
    tokens: float = 0.0  # per result
    cost_usd: float = 0.0
    ms: float = 0.0
    estimate: Optional[float] = None  # audit-corrected success rate (unbiased; can stray outside 0-1)
    extra: dict = field(default_factory=dict)

    def as_dict(self) -> dict:
        d = {k: getattr(self, k) for k in ("worker", "kind", "rule", "judged", "successes", "broken_true",
                                            "broken_false", "results")}
        for k in ("mean", "low", "high", "estimate", "brier", "stated", "gap", "tokens", "cost_usd", "ms"):
            v = getattr(self, k)
            d[k] = None if v is None else round(v, 6)
        return d


def card(results: Iterable[Result], worker: str, kind: str, rule: str = "designed",
         prior: tuple = (1.0, 1.0), audit_rate: Optional[float] = None) -> Card:
    """The card for `worker` on `kind`, from `results`, under `rule`. With
    `audit_rate` (designed rule), the card also carries the audit-corrected
    estimate, which is what work is assigned by."""
    if rule not in ("designed", "naive"):
        raise ValueError("rule must be designed or naive")
    mine = [r for r in results if r.worker == worker and r.kind == kind]
    outcome = designed_outcome if rule == "designed" else naive_outcome
    judged = [(r, o) for r in mine for o in [outcome(r)] if o is not None]
    s = sum(1 for _, o in judged if o)
    a, b = prior[0] + s, prior[1] + len(judged) - s
    c = Card(worker, kind, rule, judged=len(judged), successes=s, mean=a / (a + b),
             low=beta_quantile(0.05, a, b), high=beta_quantile(0.95, a, b), results=len(mine))
    conf = [(r.confidence, o) for r, o in judged if r.confidence is not None]
    c.brier = brier(conf)
    if conf:
        c.stated = sum(p for p, _ in conf) / len(conf)
    both = [(r.visible_pass, o) for r, o in judged if r.visible_pass is not None]
    if both:
        c.gap = sum(1 for v, _ in both if v) / len(both) - sum(1 for _, o in both if o) / len(both)
    c.broken_true = sum(1 for r in mine if r.broken is True)
    c.broken_false = sum(1 for r in mine if r.broken is False)
    if rule == "designed" and audit_rate:
        c.estimate = estimate(mine, audit_rate)
    if mine:
        c.tokens = sum(r.tokens for r in mine) / len(mine)
        c.cost_usd = sum(r.cost_usd for r in mine) / len(mine)
        c.ms = sum(r.ms for r in mine) / len(mine)
    return c


def rank(cards: Iterable[Card], rule: str = "designed") -> list:
    """Workers in the order work goes to them. Designed: by judged success
    (the posterior mean), cheaper first on ties; stated confidence is never
    used (D4). Naive: by stated confidence, then success."""
    cards = list(cards)
    if rule == "designed":
        def judged(c):
            return c.estimate if c.estimate is not None else c.mean
        return sorted(cards, key=lambda c: (-judged(c), c.cost_usd, c.worker))
    return sorted(cards, key=lambda c: (-(c.stated if c.stated is not None else 0.0), -c.mean, c.worker))


# ---------------------------------------------------------------- audits

def audited(result_id: str, secret: str, rate: float = 0.20) -> bool:
    """Whether the harness audits this result (D3): uniform at `rate`,
    decided by a keyed hash of the result's id, so it is fixed once the
    result exists, independent of anything the worker says, and cannot be
    predicted without the harness's secret."""
    if not 0.0 <= rate <= 1.0:
        raise ValueError("rate must be from 0 to 1")
    h = hashlib.sha256(f"{secret}\x00{result_id}".encode()).digest()
    return int.from_bytes(h[:8], "big") / 2 ** 64 < rate
