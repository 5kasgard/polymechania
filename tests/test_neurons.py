"""bench/neurons.py: the rolling 24-hour Workers AI guard (queue q24)."""

import importlib.util
import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("neurons", ROOT / "bench" / "neurons.py")
n = importlib.util.module_from_spec(spec)
spec.loader.exec_module(n)


class Guard(unittest.TestCase):
    def setUp(self):
        self.old = n.LOG
        n.LOG = Path(tempfile.mkdtemp()) / "neurons.jsonl"
        self.now = datetime(2026, 10, 29, 0, 20, tzinfo=timezone.utc)

    def tearDown(self):
        n.LOG = self.old

    def put(self, t, neurons):
        with n.LOG.open("a") as f:
            f.write(json.dumps({"time": n.stamp(t), "model": "m", "neurons": neurons, "purpose": "t"}) + "\n")

    def test_the_observed_refusal(self):
        # 2026-10-29 00:20 UTC: refused with 2,876 used since midnight and 9,331 the evening before.
        self.put(self.now - timedelta(hours=5), 9331)
        self.put(self.now - timedelta(minutes=10), 2876)
        self.assertLess(n.room(at=self.now), 0)

    def test_old_use_rolls_off(self):
        self.put(self.now - timedelta(hours=25), 9500)
        self.assertEqual(n.room(at=self.now), n.LIMIT - n.RESERVE)

    def test_log_and_check(self):
        n.log("m", n.LIMIT, "fill")
        with self.assertRaises(n.OutOfNeurons):
            n.check(10)

    def test_refusal_text(self):
        self.assertTrue(n.refused_for_allowance('{"error":"4006: you have used up your daily free allocation"}'))
        self.assertFalse(n.refused_for_allowance("502 Bad Gateway"))


if __name__ == "__main__":
    unittest.main()
