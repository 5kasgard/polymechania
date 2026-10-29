# The queue (2026-10-29)

Generated from `queue.json` by `python bench/workqueue.py`; edit the JSON, not this file.

23 open items; API cost if all ran: about $1.05.

## Can run now (15)

| | Item | Value | Needs | $ | Next step |
|---|---|---|---|---|---|
| q06 | Gnomon blockers before anything runs unattended | high | free | 0 | #52, #53 merged (#56). Open, stacked: #55 in PR #57, #49 in #58, #54 in #59. Next: #50 (file access), #48, #51 |
| q11 | First Test Kitchen demo: one small web demo per hypothesis | high | free | 0 | First owner verdict 2026-10-29: the questions asked nothing important; it looks rough, which is fine at alpha, and what matters now is what is under the hood. So: demos ask only questions whose answer would change a decision; visual polish waits until the plain core is right |
| q18 | Free version engine: remote MCP for Gnomon | high | free | 0 | Gnomon's MCP server is stdio only; the Claude app needs a remote server with sign-in |
| q21 | Waitlist test for Free and Paid | high | owner | 0 | A one-page site with a button per version; owner decides when to share it |
| q30 | The border: security as a world's edge | high | free | 0 | Border check: 7 of 15 hold on Gnomon main, 9 with #57, 10 with #58, 11 with #59. Next: free review of the probes; #50 (file access) is the biggest gap left |
| q13 | E1: can stat cards be gamed? | high | api | 1 | Re-cost against the $4.14 left and the free engines; write amendment 3 (judges on Workers AI); owner decides whether to spend |
| q10 | Language as a routing row; Rust against Python test | medium | free | 0 | Add the row to docs/routing.md; write Rust graders for the pilot tasks; Gemma writes each task in both languages |
| q14 | T1: run shapes on long multi-step work | medium | pro | 0 | Draft prereg/t1-long.md (arms C one session, B fresh runs, BV fresh runs with a regression check on the boundary, SR reference control; 3 free models; $0 API). Free reviews tonight, then the owner sees it before it is final; runs after E-ext (after q15) |
| q20 | Vision cheap tests: card sort, menu picture, notification volume | medium | people | 0 | Notification volume can run now from logs; card sort and menu need 5 people |
| q32 | Record refused crossings in Gnomon (the watchtower) | medium | free | 0 | Gnomon refuses bad writes but keeps no record of them, so a live border cannot show alarms; propose a bounded refusal log (outside the hash chain, or as owner-only events) as a Gnomon issue |
| q34 | Speed: measure, then cache the hot spots | medium | free | 0 | Owner's idea 2026-10-29: a cache-minded design, software and hardware (CPU caches, page cache, GPU and other accelerators). Rule: measure the first real end-to-end run (time, cost, cache misses with perf if available) and cache only the top one or two hot spots. Known candidates: Gnomon's append re-reads the whole log (store.rs line 495); recall re-reads all visible memory per query, over pointer-heavy maps (a contiguous layout or a GPU only if measured); prompt caching already proven (T2) |
| q12 | Cascade with visible checks only | medium | api | 0.05 | T2's cascade escalated on hidden graders; rerun escalating only on what a run can see (spec examples, empty or cut-off answers) |
| q19 | Batch API through the door (half price, non-urgent work) | low | free | 0 | Allow /v1/messages/batches with the same checks per request; review before deploy |
| q26 | Rename 'world' files to 'themes' in the code | low | free | 0 | worlds.py, cli and tests; keep old names working once |
| q29 | Door credentials live only in one session's scratch folder | low | free | 0 | Fine for now (re-issue per HANDOFF); revisit when a scheduler needs standing access |

## Waiting on a blocker (1)

| | Item | Value | Needs | $ | Next step |
|---|---|---|---|---|---|
| q17 | The free clock (Cloudflare cron) and the scheduler | high | free | 0 | Needs revocation (PR #58) and leases (PR #59, closed for now with its branch kept): reopen #59 when this is built (after q06) |

## Needs the owner (4)

| | Item | Value | Needs | $ | Next step |
|---|---|---|---|---|---|
| q22 | Legal check of the business model | high | owner | 0 | Brief ready for the owner to take to a lawyer: https://claude.ai/artifact/1xLmnUpcqNrMQrhukPVNxj (option C ruled out by the consumer terms; the open line is A.1 product vs D.4(a) resale). Owner books the lawyer |
| q33 | Gnomon #50: sign appends (protocol 7) | high | owner | 0 | Options in docs/gnomon-50-options.md. Session recommends F (hash-chain tokens on existing SHA-256, no new dependency) over B (ed25519-dalek). Owner decides; a Sonnet sub-agent builds it from the session's spec |
| q07 | Gnomon PR #47 (teams of models move to Polymechania) | medium | owner | 0 | Checked 2026-10-29: every removed file exists in Polymechania (firm.py is plan.py, company.py is org.py); merges cleanly on main after #56; all 251 Gnomon tests pass. Recommend merge; owner decides |
| q27 | More skills from this work | low | owner | 0 | Proposed so far: route-and-test, taste-and-adjust, session-handoff, careful-live-changes, one-queue, weigh-the-evidence, honest-views. Next candidates: budgeted-free-runs (resumable runs inside free allowances), reproduce-before-filing (probe a finding before reporting it), plain-core-themes |

## Parked (3)

| | Item | Value | Needs | $ | Next step |
|---|---|---|---|---|---|
| q03 | E-ext: do public benchmarks predict our own results? | high | free | 0 | Paused 2026-10-29 in the complexity reset; 0 results so far. Resume only if the owner wants it (no scheduled task exists) |
| q28 | T8, T9, T10 (resume adequacy, Free latency, cost per resident-month) | medium | free | 0 | Need a running world; T8 can use push_scale data meanwhile (after q17) |
| q23 | Choose a licence | low | owner | 0 | Parked by the owner 2026-10-29; options and a recommendation stay in docs/licensing.md for when it comes back |
