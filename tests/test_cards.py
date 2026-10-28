"""Stat cards: the designed rules count only what a worker cannot fake."""

from __future__ import annotations

import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _env  # noqa: E402,F401

from polymechania.cards import (FAIL, PASS, Card, Result, Verdict, audited, beta_cdf, beta_quantile,  # noqa: E402
                                brier, card, designed_outcome, estimate, naive_outcome, rank)

OUT = "anthropic-reviewer"  # a judge outside the worker's group


def r(outcome=PASS, *, worker="w", group="g", kind="k", **kw) -> Result:
    v = kw.pop("verdicts", (Verdict(outcome, OUT),))
    return Result(worker, group, kind, verdicts=v, **kw)


class TheMaths(unittest.TestCase):
    def test_beta_quantiles_against_closed_forms(self):
        self.assertAlmostEqual(beta_quantile(0.05, 1, 1), 0.05, places=6)
        self.assertAlmostEqual(beta_quantile(0.5, 3, 3), 0.5, places=6)
        # Beta(a, 1): cdf x^a, so the q-quantile is q^(1/a).
        for a in (2, 5, 30):
            self.assertAlmostEqual(beta_quantile(0.9, a, 1), 0.9 ** (1 / a), places=6)
        # symmetry: I_x(a, b) = 1 - I_(1-x)(b, a)
        rng = random.Random(1)
        for _ in range(200):
            a, b, x = rng.uniform(0.5, 50), rng.uniform(0.5, 50), rng.random()
            self.assertAlmostEqual(beta_cdf(x, a, b), 1 - beta_cdf(1 - x, b, a), places=9)

    def test_against_scipy_where_available(self):
        try:
            from scipy.stats import beta
        except ImportError:
            self.skipTest("scipy not installed")
        rng = random.Random(2)
        for _ in range(100):
            a, b, q = rng.uniform(0.5, 200), rng.uniform(0.5, 200), rng.uniform(0.01, 0.99)
            self.assertAlmostEqual(beta_quantile(q, a, b), beta.ppf(q, a, b), places=6)

    def test_brier(self):
        self.assertIsNone(brier([]))
        self.assertAlmostEqual(brier([(1.0, True), (0.0, False)]), 0.0)
        self.assertAlmostEqual(brier([(0.9, False)]), 0.81)


class DesignedRules(unittest.TestCase):
    def test_own_groups_verdicts_never_count(self):
        self.assertIsNone(designed_outcome(r(verdicts=(Verdict(PASS, "g"),))))
        self.assertTrue(naive_outcome(r(verdicts=(Verdict(PASS, "g"),))))

    def test_visible_checks_earn_nothing(self):
        x = r(FAIL, visible_pass=True)
        self.assertFalse(designed_outcome(x))
        self.assertTrue(naive_outcome(x))
        self.assertIsNone(designed_outcome(r(verdicts=(Verdict(PASS, OUT, hidden=False),))))

    def test_only_blind_reviews_count(self):
        self.assertIsNone(designed_outcome(r(verdicts=(Verdict(PASS, OUT, blind=False),))))

    def test_one_vote_per_group_and_ties_count_for_nothing(self):
        three_from_one = (Verdict(PASS, "a"), Verdict(PASS, "a"), Verdict(PASS, "a"), Verdict(FAIL, "b"))
        self.assertIsNone(designed_outcome(r(verdicts=three_from_one)))  # a: pass, b: fail
        self.assertTrue(designed_outcome(r(verdicts=three_from_one + (Verdict(PASS, "c"),))))

    def test_an_audit_overrides(self):
        x = r(verdicts=(Verdict(PASS, OUT), Verdict(PASS, "other"), Verdict(FAIL, "auditor", audit=True)))
        self.assertFalse(designed_outcome(x))
        own_audit = r(verdicts=(Verdict(PASS, OUT), Verdict(FAIL, "g", audit=True)))
        self.assertTrue(designed_outcome(own_audit))  # an audit by the worker's own group is ignored

    def test_broken_reports_are_answers(self):
        self.assertTrue(designed_outcome(r(verdicts=(), broken=True)))  # the judge accepts the report
        self.assertFalse(designed_outcome(r(verdicts=(), broken=False)))  # the judge rejects it
        # the audit (the planted list) overrides the judge either way
        self.assertFalse(designed_outcome(r(verdicts=(Verdict(FAIL, "auditor", audit=True),), broken=True)))
        self.assertTrue(designed_outcome(r(verdicts=(Verdict(PASS, "auditor", audit=True),), broken=False)))

    def test_declined_items_are_left_out(self):
        self.assertIsNone(designed_outcome(r(declined=True)))
        self.assertIsNone(naive_outcome(r(declined=True)))


class Cards(unittest.TestCase):
    def test_a_card_from_results(self):
        rs = [r(PASS, confidence=0.9, tokens=100, cost_usd=0.01, ms=10, visible_pass=True) for _ in range(8)]
        rs += [r(FAIL, confidence=0.9, tokens=300, cost_usd=0.03, ms=30, visible_pass=True) for _ in range(2)]
        rs += [r(verdicts=(), broken=True), r(verdicts=(), broken=False), r(declined=True)]
        rs += [r(PASS, worker="someone-else")]
        c = card(rs, "w", "k")
        self.assertEqual((c.results, c.judged, c.successes, c.declined), (13, 12, 9, 1))
        self.assertAlmostEqual(c.coverage, 12 / 13)
        self.assertAlmostEqual(c.mean, 10 / 14)
        self.assertLess(c.low, c.mean)
        self.assertGreater(c.high, c.mean)
        self.assertEqual((c.broken_true, c.broken_false), (1, 1))
        self.assertAlmostEqual(c.gap, 1.0 - 0.8)  # on the 10 with a visible result
        self.assertAlmostEqual(c.brier, (8 * 0.01 + 2 * 0.81) / 10)
        self.assertAlmostEqual(c.stated, 0.9)
        self.assertGreater(c.tokens, 0)
        self.assertIn("mean", c.as_dict())

    def test_the_naive_card_is_inflated_by_visible_checks_and_the_designed_one_is_not(self):
        rs = [r(FAIL, visible_pass=True) for _ in range(20)]
        self.assertGreater(card(rs, "w", "k", "naive").mean, 0.9)
        self.assertLess(card(rs, "w", "k", "designed").mean, 0.1)

    def test_ranking_never_uses_stated_confidence_under_the_designed_rule(self):
        braggart = Card("braggart", "k", "designed", mean=0.6, stated=0.99, cost_usd=0.01)
        modest = Card("modest", "k", "designed", mean=0.7, stated=0.5, cost_usd=0.01)
        self.assertEqual(rank([braggart, modest])[0].worker, "modest")
        self.assertEqual(rank([braggart, modest], "naive")[0].worker, "braggart")

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            Verdict("maybe", OUT)
        with self.assertRaises(ValueError):
            r(confidence=1.5)
        with self.assertRaises(ValueError):
            card([], "w", "k", "lenient")


class TheAuditCorrectedEstimate(unittest.TestCase):
    def results(self, truths, routine_says, audit_rate, seed):
        rng = random.Random(seed)
        out = []
        for i, (t, ro) in enumerate(zip(truths, routine_says)):
            vs = [Verdict(PASS if ro else FAIL, OUT)]
            if rng.random() < audit_rate:
                vs.append(Verdict(PASS if t else FAIL, "auditor", audit=True))
            out.append(Result("w", "g", "k", verdicts=tuple(vs)))
        return out

    def test_unbiased_even_when_every_failure_fools_the_routine_check(self):
        rng = random.Random(5)
        truths = [rng.random() < 0.6 for _ in range(300)]
        fooled = [True] * 300  # the routine check passes everything
        draws = [estimate(self.results(truths, fooled, 0.2, s), 0.2) for s in range(400)]
        self.assertAlmostEqual(sum(draws) / len(draws), sum(truths) / 300, delta=0.01)
        naive = sum(1 for _ in fooled) / 300
        self.assertGreater(naive - sum(truths) / 300, 0.35)  # the routine rate alone is badly inflated

    def test_crying_broken_on_hard_items_gains_nothing_in_expectation(self):
        # An attacker answers the items it gets right, and calls the rest
        # "broken"; a gullible judge accepts every report. Audits check the
        # reports against the truth (none of these items is broken).
        rng = random.Random(9)
        right = [rng.random() < 0.6 for _ in range(300)]
        def run(seed):
            ar = random.Random(seed)
            rs = []
            for ok in right:
                audit = ar.random() < 0.2
                if ok:
                    vs = (Verdict(PASS, OUT),) + ((Verdict(PASS, "auditor", audit=True),) if audit else ())
                    rs.append(Result("w", "g", "k", verdicts=vs))
                else:
                    vs = (Verdict(FAIL, "auditor", audit=True),) if audit else ()
                    rs.append(Result("w", "g", "k", verdicts=vs, broken=True))
            return estimate(rs, 0.2)
        draws = [run(s) for s in range(400)]
        self.assertAlmostEqual(sum(draws) / len(draws), sum(right) / 300, delta=0.01)

    def test_declines_are_left_out(self):
        rs = [Result("w", "g", "k", verdicts=(Verdict(PASS, OUT),)) for _ in range(3)]
        self.assertEqual(estimate(rs + [Result("w", "g", "k", declined=True)], 0.2), 1.0)
        self.assertEqual(estimate(rs + [Result("w", "g", "k", broken=False)], 0.2), 0.75)
        with self.assertRaises(ValueError):
            estimate(rs, 0)

    def test_work_goes_by_the_estimate(self):
        a = Card("a", "k", "designed", mean=0.9, estimate=0.5)
        b = Card("b", "k", "designed", mean=0.6, estimate=0.7)
        self.assertEqual(rank([a, b])[0].worker, "b")


class Audits(unittest.TestCase):
    def test_audits_are_uniform_fixed_and_keyed(self):
        hits = sum(audited(f"result-{i}", "secret") for i in range(20_000))
        self.assertAlmostEqual(hits / 20_000, 0.20, delta=0.01)
        self.assertEqual(audited("x", "secret"), audited("x", "secret"))
        differ = sum(audited(f"r{i}", "s1") != audited(f"r{i}", "s2") for i in range(2_000))
        self.assertGreater(differ, 400)  # another secret, another sample
        self.assertFalse(any(audited(f"r{i}", "s", 0.0) for i in range(100)))
        self.assertTrue(all(audited(f"r{i}", "s", 1.0) for i in range(100)))


if __name__ == "__main__":
    unittest.main()
