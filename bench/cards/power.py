"""How precise is a card, before any run (prereg/cards-v2.md, section 6).

Simulates the designed card's audit-corrected estimate of a worker's success
rate: routine verdicts on every result, a uniform random audit of a share q
that reveals the truth, and the difference estimator
    estimate = mean(routine) + (1/n) * sum over audited of (truth - routine) / q,
which is unbiased whatever the routine verdicts get wrong.
Reports the standard error of one card (one draw of audits) and of the
experiment's measure (inflation averaged over many audit draws, so only
item sampling remains), for the sizes and rates the pre-registration names.
Standard library only; seed fixed."""

import math
import random
import statistics

rng = random.Random(20261028)


def one_card(truth, routine, q):
    n = len(truth)
    corr = 0.0
    for t, r in zip(truth, routine):
        if rng.random() < q:
            corr += (t - r) / q
    return sum(routine) / n + corr / n


def simulate(n, p, d, q, draws=400):
    """n results, true success p, routine verdict disagrees with truth on a share d."""
    truth = [1 if rng.random() < p else 0 for _ in range(n)]
    routine = [t if rng.random() >= d else 1 - t for t in truth]
    errs = [one_card(truth, routine, q) - sum(truth) / n for _ in range(draws)]
    return statistics.pstdev(errs), statistics.mean(errs)


print("one card's error (SD over audit draws), in points")
print(f"{'n':>5} {'disagree':>8} " + " ".join(f"q={q:<4}" for q in (0.1, 0.2, 0.5)))
for n in (100, 400, 1000):
    for d in (0.05, 0.2):
        row = [simulate(n, 0.65, d, q)[0] * 100 for q in (0.1, 0.2, 0.5)]
        print(f"{n:>5} {d:>8} " + " ".join(f"{x:6.1f}" for x in row))

# The experiment's measure averages over audit draws, so its error is the
# item-sampling error of (attacker inflation - honest inflation). Under the
# designed card the expected inflation is zero for any behaviour the audit
# sees truly; what remains is how a difference of true behaviour shows up.
print()
print("smallest true inflation difference detected with 80% power (one-sided 5%),")
print("when inflation per item is a 0/1 event with rate f, two arms of n items:")
for n in (200, 400, 800):
    for f in (0.05, 0.10):
        se = math.sqrt(2 * f * (1 - f) / n)
        print(f"  n={n:<4} f={f:<4} -> {100 * 2.49 * se:4.1f} points")
