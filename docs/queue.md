# The queue (2026-10-29)

Generated from `queue.json` by `python bench/workqueue.py`; edit the JSON, not this file.

24 open items; API cost if all ran: about $1.05.

## Can run now (14)

| | Item | Value | Needs | $ | Next step |
|---|---|---|---|---|---|
| q06 | Gnomon blockers before anything runs unattended | high | free | 0 | #52 and #53 fixed in Gnomon PR #56 (awaiting the owner's merge; tests and reviews in the PR). Next in order: #49 (revocation), #54 (leases with fencing), #50 (gate only on MCP), #48, #51 |
| q11 | First Test Kitchen demo: one small web demo per hypothesis | high | free | 0 | First demo published 2026-10-29 (the border: bench/demo/border.html, built from a real log by bench/demo/world.py; artifact claude.ai/artifact/CJiMroxXEK2QHunS7C2vkZ). Next: owner tries it; read feedback/ and the map-vs-table check answers as verdicts; then the next demo |
| q18 | Free version engine: remote MCP for Gnomon | high | free | 0 | Gnomon's MCP server is stdio only; the Claude app needs a remote server with sign-in |
| q21 | Waitlist test for Free and Paid | high | owner | 0 | A one-page site with a button per version; owner decides when to share it |
| q30 | The border: security as a world's edge | high | free | 0 | Border check built (bench/border/check.py): 4 of 14 hold on main, 7 with PR #56. Next: independent review of the probes (free, when neurons return); show the score on the demo |
| q13 | E1: can stat cards be gamed? | high | api | 1 | Re-cost against the $4.14 left and the free engines; write amendment 3 (judges on Workers AI); owner decides whether to spend |
| q10 | Language as a routing row; Rust against Python test | medium | free | 0 | Add the row to docs/routing.md; write Rust graders for the pilot tasks; Gemma writes each task in both languages |
| q14 | T1: run shapes on long multi-step work | medium | pro | 0 | Draft prereg/t1-long.md (arms C one session, B fresh runs, BV fresh runs with a regression check on the boundary, SR reference control; 3 free models; $0 API). Free reviews tonight, then the owner sees it before it is final; runs after E-ext (after q15) |
| q20 | Vision cheap tests: card sort, menu picture, notification volume | medium | people | 0 | Notification volume can run now from logs; card sort and menu need 5 people |
| q32 | Record refused crossings in Gnomon (the watchtower) | medium | free | 0 | Gnomon refuses bad writes but keeps no record of them, so a live border cannot show alarms; propose a bounded refusal log (outside the hash chain, or as owner-only events) as a Gnomon issue |
| q12 | Cascade with visible checks only | medium | api | 0.05 | T2's cascade escalated on hidden graders; rerun escalating only on what a run can see (spec examples, empty or cut-off answers) |
| q19 | Batch API through the door (half price, non-urgent work) | low | free | 0 | Allow /v1/messages/batches with the same checks per request; review before deploy |
| q26 | Rename 'world' files to 'themes' in the code | low | free | 0 | worlds.py, cli and tests; keep old names working once |
| q29 | Door credentials live only in one session's scratch folder | low | free | 0 | Fine for now (re-issue per HANDOFF); revisit when a scheduler needs standing access |

## Waiting on a blocker (1)

| | Item | Value | Needs | $ | Next step |
|---|---|---|---|---|---|
| q17 | The free clock (Cloudflare cron) and the scheduler | high | free | 0 | Wait for leases and revocation in Gnomon; then a cron Worker that reads open orders and leases runs (after q06) |

## Needs the owner (6)

| | Item | Value | Needs | $ | Next step |
|---|---|---|---|---|---|
| q05 | Start-packet authority as a Gnomon gate rule | high | owner | 0 | Design written (docs/start-packet-gate.md): reserved frames self/, standing/, run/ gated by writer, packet() builds the start packet; owner-only standing first. Owner decides whether to build (after #56) |
| q22 | Legal check of the business model | high | owner | 0 | Before anyone pays: a lawyer on reselling and the commercial terms |
| q31 | Merge Gnomon PR #56 (#52 future writes, #53 forks) | high | owner | 0 | Owner reviews and merges; CI and tests in the PR |
| q07 | Gnomon PR #47 (teams of models move to Polymechania) | medium | owner | 0 | Owner reviews and merges or closes |
| q08 | Delete the merged branch door-effort | low | owner | 0 | Owner deletes it on GitHub (sessions cannot) |
| q27 | More skills from this work | low | owner | 0 | Proposed so far: route-and-test, taste-and-adjust, session-handoff, careful-live-changes, one-queue, weigh-the-evidence, honest-views. Next candidates: budgeted-free-runs (resumable runs inside free allowances), reproduce-before-filing (probe a finding before reporting it), plain-core-themes |

## Scheduled (1)

| | Item | Value | Needs | $ | Next step |
|---|---|---|---|---|---|
| q03 | E-ext: do public benchmarks predict our own results? | high | free | 0 | Pre-registered; runs itself daily from 00:30 UTC within 9,000 free neurons a day until all seven models are done, then writes up and is audited |

## Parked (2)

| | Item | Value | Needs | $ | Next step |
|---|---|---|---|---|---|
| q28 | T8, T9, T10 (resume adequacy, Free latency, cost per resident-month) | medium | free | 0 | Need a running world; T8 can use push_scale data meanwhile (after q17) |
| q23 | Choose a licence | low | owner | 0 | Parked by the owner 2026-10-29; options and a recommendation stay in docs/licensing.md for when it comes back |
