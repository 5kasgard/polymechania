"""mekh: the terminal view of Polymechania.

    mekh plan code --parts 24 --input 20000 --output 3000 --stakes 5 --check exact
    mekh form --parts 24 --check exact --families 3
    mekh rules
    mekh worlds
    mekh world show kagamigakure
    mekh world new my-world
    mekh world check my-world.toml
    mekh world use kagamigakure

Every command takes --world ID (or MEKH_WORLD, or the world set with
`mekh world use`), --plain for the plain world, --both to print each line
in the world's words with the plain line under it, and --json.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
from pathlib import Path
from typing import Optional

from . import concepts, events, forms
from . import plan as planner
from .worlds import World, WorldError, available, get

CONFIG = Path.home() / ".config" / "polymechania"


# ------------------------------------------------------------- colour

def _rgb(hex_: str) -> tuple:
    return tuple(int(hex_[i:i + 2], 16) for i in (1, 3, 5))


class Out:
    def __init__(self, world: World, both: bool = False, stream=None):
        self.world, self.both = world, both
        self.stream = stream or sys.stdout
        self.colour = self.stream.isatty() and not os.environ.get("NO_COLOR")

    def paint(self, text: str, role: str = "accent") -> str:
        hex_ = self.world.style.get(role)
        if not (self.colour and hex_):
            return text
        r, g, b = _rgb(hex_)
        return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

    def line(self, text: str = "", role: Optional[str] = None) -> None:
        print(self.paint(text, role) if role else text, file=self.stream)

    def header(self) -> None:
        w = self.world
        glyph = w.style.get("glyph", "μ")
        place = f" · {w.name}" if w.id != "plain" else ""
        self.line(f"{glyph} polymechania{place}", "accent")

    def status(self) -> None:
        self.line(f"  ◇ {random.choice(self.world.spinner())}…", "dim")

    def tell(self, evs: list) -> None:
        plain = get("plain")
        for e in evs:
            self.line(self.world.tell(e))
            if self.both and self.world.id != "plain":
                self.line("    = " + plain.tell(e).strip(), "dim")


# ----------------------------------------------------------- commands

def _world(args) -> World:
    if args.plain:
        return get("plain")
    wid = args.world or os.environ.get("MEKH_WORLD")
    if not wid and (CONFIG / "world").exists():
        wid = (CONFIG / "world").read_text(encoding="utf-8").strip()
    return get(wid)


def cmd_plan(args) -> int:
    task = planner.Task(args.kind, args.input, args.output, args.stakes, args.check, parts=args.parts,
                        urgent=not args.night, step_usd=args.step)
    p = planner.plan(task, manager=args.manager, executive=args.executive, single=args.single)
    evs = events.from_plan(p)
    if args.json:
        print(json.dumps({"plan": planner.as_dict(p), "events": [e.as_dict() for e in evs]}, indent=2))
        return 0
    out = Out(_world(args), args.both)
    out.header()
    out.status()
    out.tell(evs)
    return 0


def cmd_form(args) -> int:
    profile = forms.Profile(parts=args.parts, parallel=args.parallel, coupling=args.coupling, check=args.check,
                            locatable=args.locatable, expert=args.expert, open_ended=args.open_ended,
                            adversarial=args.adversarial, tier=args.tier, families=args.families,
                            repeats=args.repeats, narrow=not args.broad)
    dials = forms.Dials(effort=args.effort, breadth=args.breadth, scrutiny=args.scrutiny, speed=args.speed,
                        thrift=args.thrift)
    d = forms.compose(profile, dials)
    evs = events.from_design(d)
    if args.json:
        print(json.dumps({"form": d.as_dict(), "events": [e.as_dict() for e in evs]}, indent=2))
        return 0
    out = Out(_world(args), args.both)
    out.header()
    out.status()
    out.tell(evs)
    return 0


def cmd_rules(args) -> int:
    evs = events.rules()
    if args.json:
        print(json.dumps([e.as_dict() for e in evs], indent=2))
        return 0
    out = Out(_world(args), args.both)
    out.header()
    out.line(f"  {out.world.name_of('rules')}:", "accent")
    out.tell(evs)
    return 0


def cmd_worlds(args) -> int:
    worlds = available()
    if args.json:
        print(json.dumps([{"id": w.id, "name": w.name, "title": w.title, "region": w.region,
                           "path": str(w.path) if w.path else None} for w in worlds.values()], indent=2))
        return 0
    for w in sorted(worlds.values(), key=lambda w: (w.id != "plain", w.id)):
        glyph = w.style.get("glyph", " ")
        print(f"{glyph:<2} {w.id:<16} {w.name}" + (f": {w.title}" if w.title else ""))
    return 0


def cmd_world(args) -> int:
    if args.action == "show":
        w = get(args.id)
        out = Out(w)
        out.line(f"{w.style.get('glyph', 'μ')} {w.name}", "accent")
        if w.title:
            out.line(f"  {w.title}")
        if w.region:
            out.line(f"  in {w.region}", "dim")
        if w.tagline:
            out.line(f"  “{w.tagline}”")
        if w.lore:
            out.line()
            for para in w.lore.strip().split("\n\n"):
                out.line("  " + " ".join(para.split()))
                out.line()
        renamed = [(k, w.names[k]) for k in concepts.CONCEPTS if k in w.names]
        if renamed:
            out.line("  names:", "accent")
            for k, v in renamed:
                out.line(f"    {concepts.CONCEPTS[k][0]:<22} → {v}")
        return 0
    if args.action == "check":
        path = Path(args.id)
        try:
            w = World.load(path)
        except WorldError as e:
            for p in e.problems:
                print(f"✗ {p}", file=sys.stderr)
            return 1
        except OSError as e:
            print(f"✗ {e}", file=sys.stderr)
            return 1
        print(f"✓ {w.name} ({w.id}) keeps the contract: "
              f"{len(w.names)} of {len(concepts.CONCEPTS)} names, {len(w.say)} of {len(concepts.EVENTS)} events retold")
        return 0
    if args.action == "new":
        target = Path(args.out) if args.out else CONFIG / "worlds" / f"{args.id}.toml"
        if target.exists():
            print(f"✗ {target} already exists", file=sys.stderr)
            return 1
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(scaffold(args.id), encoding="utf-8")
        print(f"✓ wrote {target}: fill in what you like, then `mekh world check {target}`")
        return 0
    if args.action == "use":
        get(args.id)  # refuses a world that cannot be found
        CONFIG.mkdir(parents=True, exist_ok=True)
        (CONFIG / "world").write_text(args.id + "\n", encoding="utf-8")
        print(f"✓ default world: {args.id}")
        return 0
    return 2


def scaffold(world_id: str) -> str:
    """A new world file: every concept, event and rule, commented out, with
    its plain form, ready to be renamed."""
    lines = [f"# A world for Polymechania. Uncomment and rename whatever you like;",
             "# anything left out is said plainly. Check it with `mekh world check`.", "",
             "[world]", f'id = "{world_id}"', f'name = "{world_id.replace("-", " ").title()}"',
             'title = ""', 'region = ""', 'tagline = ""', "", "[names]"]
    for k, (plain, meaning) in concepts.CONCEPTS.items():
        lines.append(f'# "{k}" = "{plain}"  # {meaning}')
    lines += ["", "[say]", "# Each event must state every fact in its plain form; names may change."]
    for k, (tpl, required) in concepts.EVENTS.items():
        lines.append(f"# {k} = {json.dumps(tpl)}  # must use: {', '.join(required)}")
    lines += ["", "[precepts]", "# Give a rule a line of your own. Rules themselves cannot be changed."]
    for k, text in concepts.RULES.items():
        lines.append(f'# "{k}" = ""  # {text}')
    lines += ["", "[style]", '# accent = "#d97757"', '# ok = "#4f9d69"', '# fail = "#c0504d"', '# dim = "#888888"',
              '# glyph = "μ"', '# spinner = ["working"]', "", "[lore]", '# text = """', "# Your world's story.",
              '# """', ""]
    return "\n".join(lines)


# --------------------------------------------------------------- parser

def parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--world", help="the world to tell it in")
    common.add_argument("--plain", action="store_true", help="the plain world")
    common.add_argument("--both", action="store_true", help="each line in the world's words, then plainly")
    common.add_argument("--json", action="store_true", help="machine-readable output")

    ap = argparse.ArgumentParser(prog="mekh", description="Polymechania: the right worker for every part of the work.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("plan", parents=[common], help="who should do a piece of work, and what it should cost")
    p.add_argument("kind", help="the kind of work, e.g. code, summary, classify")
    p.add_argument("--parts", type=int, default=1)
    p.add_argument("--input", type=int, default=10_000, help="prompt tokens per part")
    p.add_argument("--output", type=int, default=2_000, help="output tokens per part")
    p.add_argument("--stakes", type=float, default=1.0, help="USD lost if one part is wrong and nobody notices")
    p.add_argument("--check", choices=planner.CHECKS, default="none")
    p.add_argument("--step", type=float, default=0.0, help="USD each sequential round of waiting costs")
    p.add_argument("--night", action="store_true", help="not urgent: use the Batch API at half price")
    p.add_argument("--manager", choices=planner.ORDER, default="sonnet")
    p.add_argument("--executive", choices=planner.ORDER, default="opus")
    p.add_argument("--single", choices=planner.ORDER, default="opus", help="the lone agent to compare with")
    p.set_defaults(fn=cmd_plan)

    f = sub.add_parser("form", parents=[common], help="how a team should be organised for a piece of work")
    f.add_argument("--parts", type=int, default=1)
    f.add_argument("--parallel", type=float, default=1.0)
    f.add_argument("--coupling", choices=("low", "high"), default="low")
    f.add_argument("--check", choices=("exact", "review", "none"), default="none")
    f.add_argument("--locatable", action="store_true", help="a failed check names the fault")
    f.add_argument("--expert", action="store_true", help="one worker is clearly best at this")
    f.add_argument("--open-ended", action="store_true")
    f.add_argument("--adversarial", action="store_true")
    f.add_argument("--tier", choices=forms.TIERS, default="sonnet", help="the strongest tier available")
    f.add_argument("--families", type=int, default=1, help="distinct model families available")
    f.add_argument("--repeats", type=int, default=1, help="items under one instruction (a workload)")
    f.add_argument("--broad", action="store_true", help="with --repeats: each item needs open judgement")
    for d in ("effort", "breadth", "scrutiny", "speed", "thrift"):
        f.add_argument(f"--{d}", type=float, default=0.5)
    f.set_defaults(fn=cmd_form)

    r = sub.add_parser("rules", parents=[common], help="the rules every world keeps")
    r.set_defaults(fn=cmd_rules)

    ws = sub.add_parser("worlds", parents=[common], help="the worlds that can be found")
    ws.set_defaults(fn=cmd_worlds)

    w = sub.add_parser("world", help="show, make, check or choose a world")
    w.add_argument("action", choices=("show", "new", "check", "use"))
    w.add_argument("id", help="a world id (show, new, use) or a file (check)")
    w.add_argument("--out", help="with new: where to write the file")
    w.set_defaults(fn=cmd_world)
    return ap


def main(argv: Optional[list] = None) -> int:
    args = parser().parse_args(argv)
    try:
        return args.fn(args)
    except (ValueError, KeyError) as e:
        msg = e.args[0] if e.args else str(e)
        print(f"✗ {msg}", file=sys.stderr)
        return 2
    except BrokenPipeError:  # the reader stopped reading (`| head`): not an error
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        return 0


if __name__ == "__main__":
    sys.exit(main())
