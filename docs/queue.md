# The queue (2026-10-29)

Generated from `queue.json` by `python bench/queue.py`; edit the JSON, not this file.

27 open items; API cost if all ran: about $1.05.

## Can run now (17)

| | Item | Value | Needs | $ | Next step |
|---|---|---|---|---|---|
| q02 | Evidence model: how external and internal evidence combine | high | free | 0 | Write docs/evidence-model.md (owner agreed 2026-10-29) |
| q05 | Start-packet authority as a Gnomon gate rule | high | free | 0 | Design the standing/<resident> frame and resume change in Gnomon; owner decides whether to build |
| q06 | Gnomon blockers before anything runs unattended | high | free | 0 | Fix in order: #52 (gate-assigned time), #53 (handoff forks), #49 (revocation), #54 (leases with fencing), #50 (gate only on MCP), #48, #51 |
| q11 | First Test Kitchen demo: one small web demo per hypothesis | high | free | 0 | Pick the first (the honest map is best evidenced); build as a phone-friendly artifact with one-tap feedback stored as verdicts |
| q18 | Free version engine: remote MCP for Gnomon | high | free | 0 | Gnomon's MCP server is stdio only; the Claude app needs a remote server with sign-in |
| q21 | Waitlist test for Free and Paid | high | owner | 0 | A one-page site with a button per version; owner decides when to share it |
| q13 | E1: can stat cards be gamed? | high | api | 1 | Re-cost against the $4.14 left and the free engines; write amendment 3 (judges on Workers AI); owner decides whether to spend |
| q04 | Door: allow more free Workers AI models on /ai | medium | free | 0 | Add a short allowlist of free text models (reviewed before deploy, careful-live-changes), so tests reach 6-10 models |
| q10 | Language as a routing row; Rust against Python test | medium | free | 0 | Add the row to docs/routing.md; write Rust graders for the pilot tasks; Gemma writes each task in both languages |
| q15 | Longer multi-step tasks with hidden graders | medium | free | 0 | Build 6-10 tasks of several dependent steps each, graded by tests |
| q16 | Cost and speed fields on stat cards | medium | free | 0 | Add fixed cost per call, marginal cost, setup, where it runs and measured speed to cards.py; fill from bench/ledger.jsonl and S1 |
| q20 | Vision cheap tests: card sort, menu picture, notification volume | medium | people | 0 | Notification volume can run now from logs; card sort and menu need 5 people |
| q12 | Cascade with visible checks only | medium | api | 0.05 | T2's cascade escalated on hidden graders; rerun escalating only on what a run can see (spec examples, empty or cut-off answers) |
| q19 | Batch API through the door (half price, non-urgent work) | low | free | 0 | Allow /v1/messages/batches with the same checks per request; review before deploy |
| q24 | Track Workers AI neurons per day | low | free | 0 | Log neurons per call to the ledger and stop runs that would cross the free 10,000 a day |
| q26 | Rename 'world' files to 'themes' in the code | low | free | 0 | worlds.py, cli and tests; keep old names working once |
| q29 | Door credentials live only in one session's scratch folder | low | free | 0 | Fine for now (re-issue per HANDOFF); revisit when a scheduler needs standing access |

## Waiting on a blocker (2)

| | Item | Value | Needs | $ | Next step |
|---|---|---|---|---|---|
| q03 | E-ext: do public benchmarks predict our own results? | high | free | 0 | Pre-register; run the 24 pilot tasks on the free Workers AI models; compare public rankings with ours (Haiku and Sonnet already measured in T2) (after q02, q04) |
| q17 | The free clock (Cloudflare cron) and the scheduler | high | free | 0 | Wait for leases and revocation in Gnomon; then a cron Worker that reads open orders and leases runs (after q06) |

## Needs the owner (5)

| | Item | Value | Needs | $ | Next step |
|---|---|---|---|---|---|
| q22 | Legal check of the business model | high | owner | 0 | Before anyone pays: a lawyer on reselling and the commercial terms |
| q07 | Gnomon PR #47 (teams of models move to Polymechania) | medium | owner | 0 | Owner reviews and merges or closes |
| q08 | Delete the merged branch door-effort | low | owner | 0 | Owner deletes it on GitHub (sessions cannot) |
| q23 | Choose a licence | low | owner | 0 | README says not yet chosen |
| q27 | Two more skills: 'the picture is shaped by what is underneath' and 'plain core, any theme on top' | low | owner | 0 | Propose when the owner wants them |

## Scheduled (1)

| | Item | Value | Needs | $ | Next step |
|---|---|---|---|---|---|
| q01 | T12c: Llama judge and audit | low | free | 0 | Runs itself at 10:10 Brisbane (scheduled task), after the Workers AI free allowance resets; fills the pending cells in RESULTS_C.md |

## Parked (2)

| | Item | Value | Needs | $ | Next step |
|---|---|---|---|---|---|
| q14 | T1: run shapes on long multi-step work | medium | pro | 0 | Needs a set of longer tasks with hidden graders first; T12b-d already showed the start packet matters more than run length (after q15) |
| q28 | T8, T9, T10 (resume adequacy, Free latency, cost per resident-month) | medium | free | 0 | Need a running world; T8 can use push_scale data meanwhile (after q17) |
