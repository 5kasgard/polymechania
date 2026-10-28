"""Worlds: how a person's organisation looks, sounds and is named.

A world is one TOML file. It can rename any concept, retell any event in
its own voice, give each rule a line of its own, and set the colours,
glyph and spinner words a view uses. It cannot do anything else: there is
no field for changing a rule, every retold event must still state every
required fact, and every name maps back to a plain concept. Partial worlds
are fine; whatever a world leaves out is said plainly.

    [world]
    id = "harbour"
    name = "Saltmarsh Harbour"
    title = "A fishing port that runs on errands"

    [names]
    "tier.haiku" = "deckhand"

    [say]
    mission = "A job comes in: {parts} × '{kind}', {rank} ({stakes} each). Checked: {check}."

    [precepts]
    "no-self-grading" = "No hand weighs their own catch."

    [style]
    accent = "#2a9d8f"
    glyph = "⚓"
    spinner = ["mending nets", "reading the tide"]

Built-in worlds live beside this file; a person's own worlds live in
`~/.config/polymechania/worlds/` (or wherever MEKH_WORLDS points).
"""

from __future__ import annotations

import os
import re
import string
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from . import concepts
from .events import Event

BUILT_IN = Path(__file__).resolve().parent / "worlds"
_HEX = re.compile(r"^#[0-9a-fA-F]{6}$")
_ID = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}$")
_SECTIONS = {"world", "names", "say", "precepts", "style", "lore"}


class WorldError(ValueError):
    """A world file that breaks the contract. `problems` lists every one."""

    def __init__(self, problems: list):
        self.problems = problems
        super().__init__("; ".join(problems))


def _fields(template: str) -> set:
    return {f for _, f, _, _ in string.Formatter().parse(template) if f}


def check(data: dict) -> list:
    """Every way `data` (a parsed world file) breaks the contract."""
    problems = []
    for k in data:
        if k not in _SECTIONS:
            problems.append(f"unknown section [{k}] (a world has only {', '.join(sorted(_SECTIONS))})")
    w = data.get("world", {})
    if not isinstance(w.get("id"), str) or not _ID.match(w.get("id", "")):
        problems.append("[world] id must be lowercase letters, digits and dashes")
    if not isinstance(w.get("name"), str) or not w.get("name", "").strip():
        problems.append("[world] needs a name")
    for k in w:
        if k not in ("id", "name", "title", "region", "tagline"):
            problems.append(f"[world] {k}: unknown field")
    for key, val in data.get("names", {}).items():
        if key not in concepts.CONCEPTS:
            problems.append(f"[names] {key}: not a concept (see polymechania/concepts.py)")
        elif not isinstance(val, str) or not val.strip():
            problems.append(f"[names] {key}: must be some text")
    allowed_extra = set(concepts.NAME_FACTS) | set(concepts.WORLD_FACTS)
    for kind, tpl in data.get("say", {}).items():
        if kind not in concepts.EVENTS:
            problems.append(f"[say] {kind}: not an event")
            continue
        if not isinstance(tpl, str):
            problems.append(f"[say] {kind}: must be some text")
            continue
        try:
            used = _fields(tpl)
        except ValueError as e:
            problems.append(f"[say] {kind}: {e}")
            continue
        required = set(concepts.EVENTS[kind][1])
        if required - used:
            problems.append(f"[say] {kind}: must state {', '.join(sorted(required - used))} "
                            f"(a world may retell an event, not leave out its facts)")
        if used - required - allowed_extra:
            problems.append(f"[say] {kind}: unknown fact(s) {', '.join(sorted(used - required - allowed_extra))}")
    for rid, val in data.get("precepts", {}).items():
        if rid not in concepts.RULES:
            problems.append(f"[precepts] {rid}: not a rule (a world names rules; it cannot add them)")
        elif not isinstance(val, str):
            problems.append(f"[precepts] {rid}: must be some text")
    s = data.get("style", {})
    for k in s:
        if k not in ("accent", "ok", "fail", "dim", "glyph", "spinner"):
            problems.append(f"[style] {k}: unknown field")
    for k in ("accent", "ok", "fail", "dim"):
        if k in s and not (isinstance(s[k], str) and _HEX.match(s[k])):
            problems.append(f"[style] {k}: must be a colour like #c8553d")
    if "glyph" in s and not (isinstance(s["glyph"], str) and 1 <= len(s["glyph"]) <= 2):
        problems.append("[style] glyph: one or two characters")
    if "spinner" in s and not (isinstance(s["spinner"], list) and s["spinner"]
                               and all(isinstance(x, str) and x.strip() for x in s["spinner"])):
        problems.append("[style] spinner: a list of short phrases")
    lore = data.get("lore", {})
    if lore and not (isinstance(lore, dict) and set(lore) <= {"text"} and isinstance(lore.get("text", ""), str)):
        problems.append("[lore] has one field, text")
    return problems


@dataclass
class World:
    id: str
    name: str
    title: str = ""
    region: str = ""
    tagline: str = ""
    names: dict = field(default_factory=dict)
    say: dict = field(default_factory=dict)
    precepts: dict = field(default_factory=dict)
    style: dict = field(default_factory=dict)
    lore: str = ""
    path: Optional[Path] = None

    @classmethod
    def from_dict(cls, data: dict, path: Optional[Path] = None) -> "World":
        problems = check(data)
        if problems:
            raise WorldError(problems)
        w = data["world"]
        return cls(id=w["id"], name=w["name"], title=w.get("title", ""), region=w.get("region", ""),
                   tagline=w.get("tagline", ""), names=dict(data.get("names", {})), say=dict(data.get("say", {})),
                   precepts=dict(data.get("precepts", {})), style=dict(data.get("style", {})),
                   lore=data.get("lore", {}).get("text", ""), path=path)

    @classmethod
    def load(cls, path) -> "World":
        path = Path(path)
        with path.open("rb") as f:
            try:
                data = tomllib.load(f)
            except tomllib.TOMLDecodeError as e:
                raise WorldError([f"{path.name}: not valid TOML ({e})"]) from None
        return cls.from_dict(data, path)

    # --------------------------------------------------------- telling

    def name_of(self, key: str) -> str:
        return self.names.get(key) or concepts.CONCEPTS[key][0]

    def _names(self, key) -> str:
        if isinstance(key, list):
            if key and key[0].startswith("check."):
                if len(key) == 2:  # reviewed by whom
                    return f"{self.name_of(key[0])} {self.name_of('word.by')} {self.name_of(key[1])}"
                return self.name_of(key[0])
            return f" {self.name_of('word.then')} ".join(self.name_of(k) for k in key)
        return self.name_of(key)

    def tell(self, e: Event) -> str:
        """`e` in this world's words. Numbers are never reworded."""
        facts = {f: self._names(k) for f, k in e.names.items()}
        facts.update(e.values)
        for f, key in concepts.NAME_FACTS.items():
            facts.setdefault(f, self.name_of(key))
        facts["precept"] = self.precepts.get(e.values.get("rule_id", ""), "")
        tpl = self.say.get(e.kind, concepts.EVENTS[e.kind][0])
        if e.kind == "rule":
            if not facts["precept"]:
                tpl = concepts.EVENTS["rule"][0]  # no line of its own for this rule: say it plainly
            elif "{precept}" not in tpl:
                tpl = "  {precept} ({rule})"
        return tpl.format(**facts)

    def spinner(self) -> list:
        return self.style.get("spinner") or ["working"]


PLAIN = World(id="plain", name="Plain", title="Everything called what it is")


def search_path() -> list:
    paths = []
    if os.environ.get("MEKH_WORLDS"):
        paths += [Path(p) for p in os.environ["MEKH_WORLDS"].split(os.pathsep) if p]
    paths.append(Path.home() / ".config" / "polymechania" / "worlds")
    paths.append(BUILT_IN)
    return paths


def available() -> dict:
    """Every world that can be found, by id: a person's own first, then the
    built-in ones. A broken file is skipped here; `mekh world check` says why."""
    found: dict = {}
    for d in reversed(search_path()):
        if not d.is_dir():
            continue
        for p in sorted(d.glob("*.toml")):
            try:
                w = World.load(p)
            except (WorldError, OSError):
                continue
            found[w.id] = w
    found.setdefault("plain", PLAIN)
    return found


def get(world_id: Optional[str]) -> World:
    if not world_id or world_id == "plain":
        return available().get("plain", PLAIN)
    worlds = available()
    if world_id not in worlds:
        raise KeyError(f"no world called {world_id!r} (have: {', '.join(sorted(worlds))})")
    return worlds[world_id]
