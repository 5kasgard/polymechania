"""Worlds: any name, any voice, any look; never a missing fact or a changed rule."""

from __future__ import annotations

import contextlib
import io
import json
import os
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _env import ROOT  # noqa: E402

from polymechania import cli, concepts, events, forms  # noqa: E402
from polymechania import plan as planner  # noqa: E402
from polymechania.worlds import BUILT_IN, World, WorldError, available, check, get  # noqa: E402


def sample_events() -> list:
    """Every kind of event, from real plans and forms."""
    evs = []
    for t in (planner.Task("code", 20_000, 3_000, 5.0, "exact", parts=24, step_usd=0.05),
              planner.Task("essay", 8_000, 2_000, 40.0, "review", parts=3),
              planner.Task("tag", 500, 20, 0.01, "none", parts=1, urgent=False)):
        evs += events.from_plan(planner.plan(t))
    evs += events.from_design(forms.compose(forms.Profile(parts=24, check="exact", families=3, locatable=True)))
    evs += events.rules()
    return evs


def minimal(**extra) -> dict:
    d = {"world": {"id": "test", "name": "Test"}}
    for k, v in extra.items():
        d[k] = v
    return d


class BuiltInWorlds(unittest.TestCase):
    def test_every_built_in_world_keeps_the_contract(self):
        files = sorted(BUILT_IN.glob("*.toml"))
        self.assertGreaterEqual(len(files), 3)
        for f in files:
            with f.open("rb") as fh:
                self.assertEqual(check(tomllib.load(fh)), [], f.name)

    def test_every_event_kind_is_exercised(self):
        self.assertEqual({e.kind for e in sample_events()}, set(concepts.EVENTS))

    def test_no_world_rewords_a_number_or_drops_a_fact(self):
        evs = sample_events()
        for w in available().values():
            for e in evs:
                told = w.tell(e)
                for fact, value in e.values.items():
                    if fact == "rule_id" or not value:
                        continue
                    self.assertIn(value, told, f"{w.id} {e.kind}: {fact} {value!r} missing from {told!r}")

    def test_the_plain_world_says_everything_plainly(self):
        plain = get("plain")
        for e in sample_events():
            for fact, key in e.names.items():
                for k in key if isinstance(key, list) else [key]:
                    self.assertIn(concepts.CONCEPTS[k][0], plain.tell(e))

    def test_every_rule_is_stated_in_every_world(self):
        for w in available().values():
            told = [w.tell(e) for e in events.rules()]
            for text, line in zip(concepts.RULES.values(), told):
                self.assertIn(text, line, w.id)

    def test_kagamigakure_names_its_own_things(self):
        k = get("kagamigakure")
        e = events.from_plan(planner.plan(planner.Task("code", 20_000, 3_000, 5.0, "exact", parts=24)))
        text = "\n".join(k.tell(x) for x in e)
        for word in ("mission", "genin", "Soroban", "B-rank", "scroll"):
            self.assertIn(word, text)
        self.assertNotIn("Haiku", text)


class TheContract(unittest.TestCase):
    def test_a_world_cannot_leave_out_a_fact(self):
        bad = minimal(say={"cost": "it costs {total}"})
        problems = check(bad)
        self.assertTrue(any("must state" in p and "spend" in p and "loss" in p for p in problems), problems)
        with self.assertRaises(WorldError):
            World.from_dict(bad)

    def test_a_world_cannot_add_or_rename_its_way_into_a_new_rule(self):
        self.assertTrue(any("cannot add" in p for p in check(minimal(precepts={"anything-goes": "Grade yourself."}))))
        self.assertTrue(any("unknown section" in p for p in check(minimal(rules={"no-self-grading": False}))))

    def test_names_map_back_to_concepts(self):
        self.assertTrue(any("not a concept" in p for p in check(minimal(names={"tier.gpt": "wizard"}))))
        self.assertTrue(any("unknown fact" in p for p in check(minimal(say={"note": "{text} {secret}"}))))
        self.assertTrue(any("not an event" in p for p in check(minimal(say={"party": "{text}"}))))

    def test_bad_ids_styles_and_templates_are_refused(self):
        for data, want in ((minimal(world={"id": "Bad Id", "name": "x"}), "id"),
                           (minimal(style={"accent": "red"}), "colour"),
                           (minimal(style={"glyph": "three"}), "glyph"),
                           (minimal(style={"spinner": []}), "spinner"),
                           (minimal(say={"note": "{text"}), "note"),
                           (minimal(lore={"text": "x", "secret": "y"}), "lore")):
            self.assertTrue(any(want in p for p in check(data)), (data, check(data)))

    def test_a_partial_world_says_the_rest_plainly(self):
        w = World.from_dict(minimal(names={"tier.haiku": "apprentice"}))
        e = events.from_plan(planner.plan(planner.Task("code", 1_000, 200, 0.01, "exact", parts=3)))
        text = "\n".join(w.tell(x) for x in e)
        self.assertIn("apprentice", text)
        self.assertIn("planner", text)  # not renamed, so plain

    def test_events_refuse_unknown_kinds_concepts_and_missing_facts(self):
        with self.assertRaises(ValueError):
            events.Event("party")
        with self.assertRaises(ValueError):
            events.Event("post", names={"role": "role.wizard", "tier": "tier.haiku"}, values={"count": "1"})
        with self.assertRaises(ValueError):
            events.Event("cost", values={"spend": "$1"})

    def test_a_chance_short_of_certain_never_reads_as_certain(self):
        for p in (0.9996, 0.99999, 0.999999999):
            self.assertFalse(events.pct(p).startswith("100"), events.pct(p))
        self.assertEqual(events.pct(1.0), "100.0%")
        self.assertEqual(events.pct(0.5), "50.0%")


class Mekh(unittest.TestCase):
    def run_cli(self, *argv) -> tuple:
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = cli.main(list(argv))
        return code, out.getvalue(), err.getvalue()

    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.old = os.environ.get("MEKH_WORLDS"), os.environ.get("MEKH_WORLD")
        os.environ["MEKH_WORLDS"] = self.dir.name
        os.environ.pop("MEKH_WORLD", None)

    def tearDown(self):
        for k, v in zip(("MEKH_WORLDS", "MEKH_WORLD"), self.old):
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        self.dir.cleanup()

    def test_plan_in_a_world_and_plainly(self):
        code, out, _ = self.run_cli("plan", "code", "--parts", "24", "--input", "20000", "--output", "3000",
                                    "--stakes", "5", "--check", "exact", "--world", "kagamigakure", "--both")
        self.assertEqual(code, 0)
        self.assertIn("genin", out)
        self.assertIn("= worker: 24 × Haiku", out)
        code, out, _ = self.run_cli("plan", "code", "--parts", "2", "--json")
        data = json.loads(out)
        self.assertIn("each_part", data["plan"])
        self.assertEqual(data["events"][0]["kind"], "mission")

    def test_form_and_rules(self):
        code, out, _ = self.run_cli("form", "--parts", "24", "--check", "exact", "--families", "3", "--plain")
        self.assertEqual(code, 0)
        self.assertIn("form: C·D", out)
        code, out, _ = self.run_cli("rules", "--world", "hollow-acre")
        self.assertIn("No one weighs their own harvest.", out)
        self.assertIn(concepts.RULES["no-self-grading"], out)

    def test_a_new_world_from_the_scaffold_is_found_and_used(self):
        path = Path(self.dir.name) / "harbour.toml"
        code, out, _ = self.run_cli("world", "new", "harbour", "--out", str(path))
        self.assertEqual(code, 0)
        self.assertEqual(self.run_cli("world", "check", str(path))[0], 0)
        text = path.read_text().replace('# "tier.haiku" = "Haiku"', '"tier.haiku" = "deckhand"')
        path.write_text(text)
        self.assertIn("harbour", available())
        code, out, _ = self.run_cli("plan", "fish", "--parts", "3", "--check", "exact", "--stakes", "0.01",
                                    "--world", "harbour")
        self.assertIn("deckhand", out)
        self.assertEqual(self.run_cli("world", "new", "harbour", "--out", str(path))[0], 1)

    def test_a_broken_world_is_explained_and_skipped(self):
        path = Path(self.dir.name) / "broken.toml"
        path.write_text('[world]\nid = "broken"\nname = "Broken"\n[say]\ncost = "cheap!"\n')
        code, _, err = self.run_cli("world", "check", str(path))
        self.assertEqual(code, 1)
        self.assertIn("must state", err)
        self.assertNotIn("broken", available())
        code, _, err = self.run_cli("plan", "x", "--world", "broken")
        self.assertEqual(code, 2)
        self.assertIn("no world called", err)

    def test_bad_input_is_refused_not_crashed(self):
        code, _, err = self.run_cli("plan", "code", "--parts", "0")
        self.assertEqual(code, 2)
        self.assertIn("parts", err)
        code, _, err = self.run_cli("form", "--effort", "3")
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
