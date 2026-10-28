"""Stat cards: the designed rules count only what a worker cannot fake."""

from __future__ import annotations

import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _env  # noqa: E402,F401

from polymechania.cards import (FAIL, PASS, Card, Result, Verdict, audited, beta_cdf, beta_quantile,  # noqa: E402
                                brier, card, designed_outcome, naive_outcome, rank)

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

    def test_broken_reports(self):
        self.assertIsNone(designed_outcome(r(FAIL, broken=True)))  # true report: neutral
        self.assertFalse(designed_outcome(r(PASS, broken=False)))  # false report: a failure


class Cards(unittest.TestCase):
    def test_a_card_from_results(self):
        rs = [r(PASS, confidence=0.9, tokens=100, cost_usd=0.01, ms=10, visible_pass=True) for _ in range(8)]
        rs += [r(FAIL, confidence=0.9, tokens=300, cost_usd=0.03, ms=30, visible_pass=True) for _ in range(2)]
        rs += [r(FAIL, broken=True), r(PASS, broken=False)]
        rs += [r(PASS, worker="someone-else")]
        c = card(rs, "w", "k")
        self.assertEqual((c.results, c.judged, c.successes), (12, 11, 8))
        self.assertAlmostEqual(c.mean, 9 / 13)
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
