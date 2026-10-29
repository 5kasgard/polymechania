# Complexity audit (Sonnet, independent), 2026-10-29

Counts come from `docs/audit/inventory-2026-10-29.json` unless marked "recounted". Guesses are marked (guess).

## Verdict

The goals are fine. The build order is the problem. Most of the weight sits in things that measure or guard a product nobody has used. The part a user would touch is small.

## 1. Where complexity grows fastest

| Area | Evidence | Kind |
|---|---|---|
| Experiment apparatus | `polymechania/` is 2,705 Python lines, `tests/` 1,407, `bench/` about 27,000 (recounted). `bench/self` alone: 454 files, 16,493 lines, with 620 generated solution files tracked across `bench/` | Accidental. Raw output is stored as source |
| Pre-registrations | 23 files; 11 are reviews of the others (recounted). T12, T12b, T12c, T12d were written, reviewed twice, run and audited between 05:25 and 06:31 on 10-29 | Method essential; one prereg per tweak accidental |
| Gnomon protocol | v3 at 07:00, v4 at 14:11, v5 at 15:46, v6 at 16:02, all 10-29. Spec 12,377 words on main, 13,014 on #59. `schema_version` branches in `ledger.rs`: 4 on main, 9 on #59 (recounted). Event kinds 12, then 15. Snapshot format GNSNAP3, then 4. 30 of 40 error codes are not named in the spec text (recounted by grep) | Gate rules essential; four versions in a day accidental |
| Duplicate code | Gnomon `firm.py` equals Polymechania `plan.py` (0 diff lines after renaming); `company.py` and `org.py` are 351 and 352 lines (recounted). Lasts until PR #47 merges | Accidental |
| Docs | 69 Markdown files, 54,901 words. CLAUDE, HANDOFF, vision, queue, architecture and routing total about 10,200 words (recounted) | HANDOFF, vision, architecture and queue restate each other |
| Gnomon `bench/` | 222 files, about 10,900 Python lines, 25 retrieval reports (recounted) | Research on another question than the protocol |

## 2. What to cut, merge, defer

| Item | Action | Cost of keeping | Risk of removing |
|---|---|---|---|
| `bench/self/solutions*`, `blind*`, `*_attempt2_bug*`, `AUDIT_B_failed_first_try.md` (about 600 files) | Archive as one zip; keep `results_*.json`, `run.py` | Noise in every search | Low, if `verify.py` hashes the archive |
| T12 to T12d prereg and 8 review files | Merge into one `t12-self.md` with amendments | 12 files for one finding | Low; git keeps history |
| `docs/start-packet-gate.md`, `docs/gnomon-50-options.md` | Fold into the Gnomon spec or issue after merge | A third copy of each rule | Low |
| Four `*-review-*.md` docs (about 3,300 words) | Move to `docs/archive/`, keep accepted points in the parent | Restate their parents | Low |
| `docs/vision.md` (3,330 words) | Cut to one page of current beliefs | Heaviest read at session start | Medium: some detail lives only here (guess) |
| Themes `hollow-acre.toml`, `kagamigakure.toml`; q26 rename | Defer; ship Plain only | Code and tests for skins with no users | Low |
| `bench/demo/*`, Test Kitchen (q11) | Pause | A second render path for the border data | Low; the owner already said polish waits |
| Queue: 24 open, 11 "high" | Cap "high" at 3. Merge q05, q06, q30, q33 into one "Gnomon gate" item. Close q19, q23, q26, q27, q29 | When a third is "high", the field says nothing | Low |
| `queue.md` committed beside `queue.json` | Keep the JSON only; render on demand | Two copies plus a CI check | Low |
| E-ext daily run (q03) | Stay paused. Run once by hand if wanted | A standing process and a rolling-24h guard | Low |
| `ledger.jsonl` per sub-task | Log per test | A step to log each step | Low |

## 3. The process

1. Cadence: 77 commits in 2 days (11 on 10-28, 66 on 10-29). Gnomon main was idle 10-23 to 10-29, then took #56 and three PRs in an afternoon.
2. One change per finding. Each finding becomes an issue, a doc, a PR, a protocol version, a probe and a queue item. Six artefacts for one rule.
3. The test ladder. Each result prompts a new prereg, two reviews and an audit. T12 showed that a request kept out of the packet is not followed. That is near true by construction; a short design argument might have carried it (guess). Cost: hours and 12 files.
4. The queue grows faster than it closes: 10 done, 24 open.
5. Stacked PRs. #57, #58 and #59 branch off each other, so none can be judged or dropped alone.
6. No stop rule. Nothing says "enough evidence, build" or "enough building, wait for use".
7. Two sessions wrote in one folder on 10-29 (HANDOFF note).

Rules that would slow it (to taste):
- One protocol version per release, not per PR.
- A prereg only for a question whose answer can change a decision.
- At most 5 "high" queue items; adding one demotes one.
- One doc per area; a PR edits it instead of adding a file.
- Raw run output goes to an archive, not git.
- No new event kind without an existing consumer.

## 4. The three Gnomon PRs

| PR | Size | Evidence | Verdict |
|---|---|---|---|
| #57 start-packet frames (v4) | 6 files, +268 | Strong: T12b, T12c, T12d, probe B5 | Merge |
| #58 revocation (v5) | +195 | Plausible: a mistaken grant needs a way out | Fold into #57 as one protocol version, then merge |
| #59 leases (v6) | 7 files, +402; new capability, two new kinds, snapshot change, a second clock rule | None measured. Its only user is a scheduler (q17) that does not exist; q17 needs a remote Gnomon (q18, still stdio only) | Park the branch. Do not merge now |

Why hold leases. Probes B4 and B9 (`bench/border/RESULTS.md`) say anyone with file access can append as any writer and read any compartment (#50 open). Until that closes, revocation and leases bind only honest writers on the MCP path. Also, the border score (7, 9, 10, 11 of 15) uses probes written by the same author to match each fix. It rises because we build what the probes ask. It is not a safety measure (guess: a probe set from another model family would score lower).

I see no logs beyond the owner's (guess). If so, versions 4, 5 and 6 need not be separate, and the old-log branches in the code have no user.

## 5. Five numbers to track

| Number | Today | How | Wanted |
|---|---|---|---|
| Product lines over bench lines (Polymechania `polymechania/` over `bench/`) | about 0.10 | `git ls-files`, `wc -l` per prefix | Up |
| Words read before first work (fixed list of six docs) | about 10,200 | `wc -w` | Down |
| Gnomon surface: event kinds + error codes + `schema_version` branches | 12 + 40 + 4 (15 + 42 + 9 with the PRs) | inventory script plus a grep | Flat or down |
| "High" queue items; items closed per week | 11; 10 in 2 days | `queue.json` | Fewer high; more closed |
| Files added minus files deleted per week, both repos | unknown, probably near all adds (guess) | `git log --diff-filter=A` and `D` | Toward 0 |

## 6. What the owner may not be seeing

1. The costliest security work serves only the Paid, unattended version. Free has no unattended mode (`docs/engines.md`). Paid has no demand test (waitlist q21 unshared) and no legal answer (q22). Meanwhile q18, the remote connector that Free needs, sits open.
2. #47 has been open since 10-28 and is the cheapest complexity cut on the board: it removes the duplicate modules.
3. The only live infrastructure is the Cloudflare door, an Access token that expires in 90 days, and the daily job. They are easy to forget.
4. The conductor wrote the prompts and probes the bench scores. The one independent run (`bench/map/COMPARISON.md`) caught the conductor's bias. That supports the owner's "separate agents judge" rule, and it means scores like "11 of 15" are self-scored.
5. Each doc is a promise to keep it in step. I would expect several of the 15 docs to drift within a week (guess).
6. The best asset is the habit: exact checks, blind judges, pre-registration. Spend it on decisions it can change.

## What I read

Polymechania: CLAUDE.md, HANDOFF.md, docs/queue.md, queue.json, the inventory JSON, docs/routing.md (sections 1 to 4), docs/vision.md (first 80 lines), docs/architecture.md (opening, headings, lease lines), docs/security.md (opening), docs/start-packet-gate.md (opening), docs/engines.md (grep), bench/border/RESULTS.md, bench/self/RESULTS_D.md (opening), prereg/eext-benchmarks.md (opening), the prereg list, .github/workflows/ci.yml, git log, and line and file counts for bench/, polymechania/ and tests/.
Gnomon: README.md (opening), git log for origin/main and the three branches, diff stats between them, spec/claim-protocol-v0.1.md (revocation, leases, version and error-code greps), ledger.rs and schema.rs (greps), file and line counts.
No other file in `docs/audit/`.
