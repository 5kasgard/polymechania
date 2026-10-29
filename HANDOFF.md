# Handoff: start here

Rewritten 2026-10-29 as a **reset**, after a long session drifted. Three independent audits
(Claude Opus, a separate Claude Sonnet, Gemini) found the same thing: the product is small
and the apparatus around it is large; no resident has done one real task end to end.
Read this, then `docs/audit/SUMMARY.md`. Read anything else only when the task in hand needs it.

## The owner's decision (answered 2026-10-29)

Of the five-part proposal in `docs/audit/SUMMARY.md`, the owner took **part 3 only**: the
cleanup pass. Parts 1 (one goal), 2 (Gnomon PRs), 4 (rules) and 5 (weekly numbers) were not
taken; do not act on them unless the owner raises them again.

- **Cleanup: done** (PR #2, merged). Finished experiments are under `bench/archive/` (one line
  each in its README); review files are folded verbatim into their parents under "## Reviews"
  (a condensed first try lost points, found by a Gemini review). `bench/border` stays, as q30 is
  open. It cut files (74 to 60 Markdown), not words.
- **Queue: left as is** by the owner. Two pruned copies were shown, not committed: **A**, what is
  live now (open: q06, q30, q05, q22, q33, q07, q27; rest parked); **C**, the goal (open: a new
  goal-run item and q05; rest parked). The owner has not picked one.

## How the owner works (apply always)

- Never impose a design: hypothesise, taste and adjust, backed by numbers.
- Separate agents judge Claude's work; at least one not Claude.
- **Route the work:** Opus plans, writes briefs and reviews; Sonnet or Haiku sub-agents build
  (`model` set); free open models (the door's `/ai`) review and judge. On 2026-10-29 Opus built
  everything itself, and the owner caught it.
- iOS Safari: short, plain replies. Keep the owner's real name out of the repositories.
- The owner may paste a prompt into another family's chat (e.g. Gemini) when free engines are
  out: give them one self-contained file (as `docs/audit/prompt-outside.md`).

## What stands (with evidence)

- **Start-packet rule** (T12b-d, `bench/archive/self/RESULTS_B.md`, `_C.md`, `_D.md`): keeping another
  writer's request out of a resident's next packet kept 86-92% of its rules; carrying it 51-59%;
  labels added only 9 points. Built as Gnomon PR #57.
- **Thin boot and settings** (T2, T2b, T2c in `bench/boot`): Haiku with thinking off is the
  cheapest per correct task here (`bench/cards/T2_CARDS.md`).
- **Workers AI's free allowance** acted as a rolling 24 hours, not the documented midnight UTC
  reset (`bench/neurons.md`); `bench/neurons.py` guards every call.
- Hypotheses only: the vision, the architecture, the security border (`docs/security.md`; its
  border score is self-scored, and anyone with file access bypasses Gnomon's gate, #50).

## Open (the one queue is `queue.json`; `docs/queue.md` is generated from it)

| Item | State | Next |
|---|---|---|
| Gnomon main | #47, #57 (protocol 4), #60 (revocation, leases; protocol 6) and #61 merged 2026-10-29. #61 closes #51: an auto-mode session's writer holds only the compartment it is recorded in, and the MCP server takes `--require-attach`; chosen by a pre-registered test of four fixes on eight leak roads (gnomon `bench/issue51/`, branch `auto-one-compartment`; reviewed by Haiku and Gemini) | done | |
| Gnomon #48 (side channels) | pre-registered test on branch `issue-48` (`bench/issue48/`): a Haiku review found four more channels; nine arms, a combination and two follow-ups (I2b, G) built by Sonnet, every number rerun by Opus. Chosen: S1, I2b, O1, V1, T1 with G on `arm48-combo2` (protocol 7; 0 failures; old logs replay identically). Event-count gaps stay a documented limit | owner pastes `bench/issue48/review-prompt.md` into Gemini; then a PR from `arm48-combo2` |
| Gnomon #48 leases (q35) | a hidden lease on a frame name blocks another compartment's lease on it | owner: scope leases per compartment (protocol change) or accept one bit |
| Gnomon #50 (file access) | options in `docs/gnomon-50-options.md`; hash-chain tokens on existing SHA-256 recommended | owner decides, after the goal |
| Gnomon append re-reads the whole log (`store.rs` line 495) | found, not measured | measure when it matters |
| T1 (run shapes on long tasks) | tasks `bench/long`, runner `bench/long/run.py` (Sonnet-built), draft `prereg/t1-long.md` | owner sees the draft; paused |
| E-ext (public benchmarks vs ours) | registered, **0 results**; paused | resume only if the owner wants it |
| Legal check | brief: https://claude.ai/artifact/1xLmnUpcqNrMQrhukPVNxj | owner books a lawyer |
| Licence | parked by the owner | |

## Budget

About **$4.14 of API credit** left (none spent after T12d). Workers AI: free 10,000 neurons,
acting as a rolling 24 h; found used up 29 Oct about 10:20 UTC (not by this work). Pro plan sub-agents: usage, not dollars.

## Left running or pending

- **Scheduled tasks: none** (all deleted 2026-10-29 in the pause).
- **The door** (`bench/cards/door/`): Cloudflare Worker behind Access, Anthropic key set by the
  owner. Its credentials live only in a session's scratch folder; a new session issues fresh
  ones through the Cloudflare connector (`careful-live-changes` skill).
- **Gnomon branches:** merged and deletable by the owner (sessions cannot delete remote branches):
  `start-packet-gate`, `revoke`, `leases`, `gate-time-and-forks`, `issue-51-one-compartment`. Kept as the
  #51 evidence: `auto-one-compartment` (bench) and `arm-A`, `arm-B`, `arm-C`, `arm-C2`, `arm-D`, `arm-D1`, `arm-D2`. #48: `issue-48` (bench), `arm48-*` (nine arms, `arm48-combo`, `arm48-combo2`); deletable once the PR merges, except `issue-48`.
- Protocol numbers: #48's combination takes 7; #50's options doc also planned 7, so whichever lands second takes 8.
- Before writing, check `git log` and `git status` for changes you did not make (a duplicate
  session once worked here at the same time).
