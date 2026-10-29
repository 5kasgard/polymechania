"""Count what exists, exactly, so complexity can be tracked over time (complexity audit, 2026-10-29).

    python docs/audit/inventory.py [path-to-gnomon]   # writes docs/audit/inventory-<date>.json
"""
import json, re, subprocess, sys
from datetime import date
from pathlib import Path

POLY = Path(__file__).resolve().parents[2]
GN = Path(sys.argv[1]) if len(sys.argv) > 1 else POLY.parent / "gnomon"


def files(repo):
    return [repo / f for f in subprocess.run(["git", "ls-files"], cwd=repo, capture_output=True, text=True).stdout.split()]


def lines(paths, suffixes):
    n = 0
    for p in paths:
        if p.suffix in suffixes and p.is_file():
            n += sum(1 for l in p.read_text(errors="ignore").splitlines() if l.strip())
    return n


def words(paths):
    return sum(len(p.read_text(errors="ignore").split()) for p in paths if p.suffix == ".md" and p.is_file())


def repo_counts(repo):
    fs = files(repo)
    md = [p for p in fs if p.suffix == ".md"]
    tests = [p for p in fs if "test" in p.name and p.suffix in (".py", ".rs", ".mjs")]
    return {"tracked_files": len(fs), "python_lines": lines(fs, {".py"}), "rust_lines": lines(fs, {".rs"}),
            "js_lines": lines(fs, {".js", ".mjs"}), "html_lines": lines(fs, {".html"}),
            "markdown_files": len(md), "markdown_words": words(md), "test_files": len(tests),
            "commits": int(subprocess.run(["git", "rev-list", "--count", "HEAD"], cwd=repo, capture_output=True, text=True).stdout or 0)}


out = {"date": str(date.today()), "polymechania": repo_counts(POLY)}
p = out["polymechania"]
p["preregistrations"] = len(list((POLY / "prereg").glob("*.md")))
p["docs"] = sorted(x.name for x in (POLY / "docs").glob("*.md"))
q = json.loads((POLY / "queue.json").read_text())["items"]
p["queue_items"] = len(q)
p["queue_by_status"] = {s: sum(1 for i in q if i["status"] == s) for s in sorted({i["status"] for i in q})}
p["bench_folders"] = sorted(x.name for x in (POLY / "bench").iterdir() if x.is_dir() and not x.name.startswith("__"))
if GN.exists():
    g = out["gnomon_main"] = repo_counts(GN)
    schema = subprocess.run(["git", "show", "origin/main:crates/gnomon-core/src/schema.rs"], cwd=GN, capture_output=True, text=True).stdout
    ledger = subprocess.run(["git", "show", "origin/main:crates/gnomon-core/src/ledger.rs"], cwd=GN, capture_output=True, text=True).stdout
    spec = subprocess.run(["git", "show", "origin/main:spec/claim-protocol-v0.1.md"], cwd=GN, capture_output=True, text=True).stdout
    kinds = re.search(r"EVENT_KINDS: &\[&str\] = &\[(.*?)\];", schema, re.S)
    g["event_kinds"] = re.findall(r'"([a-z_]+)"', kinds.group(1)) if kinds else []
    g["error_codes"] = sorted(set(re.findall(r'"(E_[A-Z_]+)"', ledger + schema)))
    g["protocol_version"] = int(re.search(r"SCHEMA_VERSION: i64 = (\d+)", schema).group(1))
    g["spec_words"] = len(spec.split())
    g["python_modules"] = sorted(x.name for x in (GN / "python" / "gnomon").glob("*.py"))
    pr = subprocess.run(["gh", "api", "repos/5kasgard/gnomon/pulls?state=open", "-q", "[.[] | {number, title}]"],
                        cwd=GN, capture_output=True, text=True).stdout
    g["open_prs"] = json.loads(pr or "[]")
path = POLY / "docs" / "audit" / f"inventory-{out['date']}.json"
path.write_text(json.dumps(out, indent=1) + "\n")
print(json.dumps(out, indent=1))
