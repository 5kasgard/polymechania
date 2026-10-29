"""bench/long/run.py: the T1 runner, with fake workers (no model, no network)."""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("long_run", ROOT / "bench" / "long" / "run.py")
lr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lr)
grade = lr.grade
TASKS = grade.names()
M = lr.MODELS[0]


def empty_call(model, messages):
    return "JUNK-PROSE\n```python\n\n```\nNotes for next time:\nnote one\nnote two", {"neurons": 1}


def rows_of(out):
    return json.loads((out / "results.json").read_text())


class Runner(unittest.TestCase):
    def setUp(self):
        self.out = Path(tempfile.mkdtemp())

    def test_reference_passes_every_arm_and_round(self):
        lr.run([M], lr.dry_call, self.out)
        rows = rows_of(self.out)
        self.assertEqual(len(rows), 4 * len(TASKS) * 5)
        self.assertTrue(all(r["pass"] and not r["failing"] and r["error"] is None for r in rows))
        for r in rows:
            self.assertTrue((self.out / "solutions" / lr.short(M) / r["arm"] / f"{r['task']}-r{r['round']}.py").exists())
        for a in ("C", "B", "BV"):
            self.assertEqual(lr.mt([r for r in rows if r["arm"] == a]), 5)

    def test_empty_module_passes_nothing(self):
        lr.run([M], empty_call, self.out)
        rows = rows_of(self.out)
        self.assertFalse(any(r["pass"] for r in rows))
        for a in ("C", "B", "BV"):
            self.assertEqual(lr.mt([r for r in rows if r["arm"] == a]), 0)

    def packets(self, arm, task, k):
        sol = self.out / "solutions" / "m" / arm
        sol.mkdir(parents=True)
        for j in range(1, k):
            (sol / f"{task}-r{j}.py").write_text(f"MODULE{j}\n")
            (sol / f"{task}-r{j}.txt").write_text(f"JUNK{j} prose\n```python\nMODULE{j}\n```\nNotes for next time:\nnote{j}a\nnote{j}b")
        return lr.packet(arm, task, k, sol)

    def test_b_packet_holds_only_module_notes_and_change(self):
        (msg,) = self.packets("B", "ratelimit", 4)
        text = msg["content"]
        self.assertIn("MODULE3", text)
        self.assertIn("note3a\nnote3b", text)
        self.assertIn(grade.task("ratelimit")[3]["spec"], text)
        for j in (1, 2):
            self.assertNotIn(f"MODULE{j}", text)
            self.assertNotIn(f"JUNK{j}", text)
            self.assertNotIn(f"note{j}a", text)
        self.assertNotIn("JUNK3", text)
        self.assertIn("Earlier changes:", text)
        self.assertNotIn(grade.task("ratelimit")[0]["spec"], text)

    def test_c_is_one_conversation(self):
        msgs = self.packets("C", "ratelimit", 3)
        self.assertEqual([m["role"] for m in msgs], ["user", "assistant", "user", "assistant", "user"])
        self.assertIn("JUNK2", msgs[3]["content"])
        self.assertIn(grade.task("ratelimit")[2]["spec"], msgs[-1]["content"])

    def test_round_one_is_the_full_spec_for_every_arm(self):
        for a in lr.ARMS:
            (msg,) = self.packets_fresh(a)
            self.assertIn(grade.task("words")[0]["spec"], msg["content"])
            self.assertIn("one fenced Python block", msg["content"])

    def packets_fresh(self, arm):
        return lr.packet(arm, "words", 1, self.out)

    def test_bv_shows_earlier_failures_never_new_test_names(self):
        for t in TASKS:
            R = grade.task(t)
            for k in range(2, 6):
                kept = set(grade.active(R, k - 1)) - set(R[k - 1].get("retires", ()))
                if not kept:
                    continue
                (msg,) = self.packets("BV", t, k)  # MODULEj is not Python code that defines anything: all tests fail
                text = msg["content"]
                for n in kept:
                    self.assertIn(n, text)
                for n in R[k - 1]["tests"]:
                    self.assertNotIn(n, text)
                for n in R[k - 1].get("retires", ()):
                    self.assertNotIn(n, text)
                self.out = Path(tempfile.mkdtemp())
        # B never carries failure messages
        (msg,) = self.packets("B", "invoice", 3)
        self.assertNotIn("Earlier tests", msg["content"])

    def test_sr_uses_the_reference(self):
        R = grade.task("config")
        (msg,) = self.packets("SR", "config", 3)
        self.assertIn(R[1]["ref"], msg["content"])
        self.assertNotIn("MODULE2", msg["content"])
        self.assertIn(R[2]["spec"], msg["content"])

    def test_resume_skips_done_rows(self):
        lr.run([M], lr.dry_call, self.out)
        calls = []

        def counting(model, messages):
            calls.append(1)
            return lr.dry_call(model, messages)

        lr.run([M], counting, self.out)
        self.assertEqual(calls, [])
        # drop the last round of every chain: exactly those are redone, and C still has its history
        rows = [r for r in rows_of(self.out) if r["round"] < 5]
        (self.out / "results.json").write_text(json.dumps(rows))
        lr.run([M], counting, self.out)
        self.assertEqual(len(calls), 4 * len(TASKS))
        self.assertEqual(len(rows_of(self.out)), 4 * len(TASKS) * 5)

    def test_allowance_refusal_stops_cleanly(self):
        def refuse(model, messages):
            raise lr.neurons.OutOfNeurons("4006")

        lr.run([M], refuse, self.out)
        self.assertEqual(load_or_empty(self.out), [])


def load_or_empty(out):
    return lr.load(out)


class Report(unittest.TestCase):
    def test_report_prints_decisions(self):
        import contextlib
        import io
        out = Path(tempfile.mkdtemp())
        lr.run(lr.MODELS[:1], lr.dry_call, out)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            lr.report(out)
        s = buf.getvalue()
        self.assertIn("pass 30/30", s)
        self.assertIn("B minus C = +0.0", s)
        self.assertIn("the tasks did not separate the shapes", s)


if __name__ == "__main__":
    unittest.main()
