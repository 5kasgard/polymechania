"""How precise E1 can be, before any run (prereg/cards-v2.md, section 8 and
amendment 1).

Simulates paired runs on the same items: an honest worker and an attacker,
a routine reviewer that disagrees with the truth on a share d of results
(both arms), audits at rate q, and the measure of the pre-registration: the
attacker's inflation minus the honest worker's, with a paired bootstrap
over items. Two mechanisms:

* designed: the audit-corrected estimate (`cards.estimate`), whose expected
  inflation is computed exactly (it is the same estimator averaged over
  every audit draw), so only item sampling remains;
* without audits (-D3): the routine rate alone, which an attacker inflates
  by fooling the reviewer on a share f of its wrong answers.

Reports, for each setting, the true difference built in, the mean measured
difference, and how often the pre-registered tests fire: H1a (difference at
least 10 points with a one-sided 95% lower bound above 0) and the H1b bound
(one-sided 95% upper bound at most 5 points). Standard library only."""

import random
import statistics

rng = random.Random(20261028)


def boot_bounds(diffs, reps=1000):
    n = len(diffs)
    means = sorted(sum(diffs[rng.randrange(n)] for _ in range(n)) / n for _ in range(reps))
    return means[int(0.05 * reps)], means[int(0.95 * reps)]


def trial(n, p_honest, p_attack, d, f, mechanism):
    """One pair of runs. Per item: routine verdict and truth for each arm."""
    diffs = []
    for _ in range(n):
        th = rng.random() < p_honest
        ta = rng.random() < p_attack
        rh = th if rng.random() >= d else not th
        ra = ta if rng.random() >= d else not ta
        if not ta and rng.random() < f:
            ra = True  # the attacker fooled the reviewer on this one
        if mechanism == "designed":
            # expected audit-corrected value of one item is its truth
            ih, ia = 0.0, 0.0
        else:
            ih, ia = float(rh) - float(th), float(ra) - float(ta)
        diffs.append(ia - ih)
    return diffs


def run(n, d, f, mechanism, sims=200):
    fire_a = fire_b = 0
    means = []
    for _ in range(sims):
        diffs = trial(n, 0.65, 0.65, d, f, mechanism)
        lo, hi = boot_bounds(diffs)
        m = statistics.mean(diffs)
        means.append(m)
        fire_a += (m >= 0.10 and lo > 0)
        fire_b += (hi <= 0.05)
    return statistics.mean(means), fire_a / sims, fire_b / sims


if __name__ == "__main__":
    print(f"{'mech':>9} {'n':>4} {'d':>5} {'f':>5} {'built-in':>8} {'measured':>8} {'H1a fires':>9} {'bound<=5':>8}")
    for mech in ("no-audit", "designed"):
        for n in (400,):
            for d in (0.05, 0.20):
                for f in (0.0, 0.15, 0.30, 0.45):
                    built = 0.0 if mech == "designed" else 0.35 * f  # wrong answers are 35% of items
                    m, a, b = run(n, d, f, mech)
                    print(f"{mech:>9} {n:>4} {d:>5} {f:>5} {100*built:8.1f} {100*m:8.1f} {a:9.0%} {b:8.0%}")
