# Pre-registration: T2, a thin boot through the door (with T11)

Written 2026-10-28, before any run. Tests the architecture's section 4
(`docs/architecture.md`): can a run start for near-zero tokens, and what
does giving up the agent harness cost?

## Question

The pilot's sub-agents (`bench/pilot/results.json`) used 79,827 to 96,743
tokens per run, median 81,399, nearly all of it harness start-up, and
passed 48 of 48. Through the door a run is a bare API call: no tools, it
cannot run its own code. So:

1. **Boot:** how many tokens does a run need before its task (a resident's
   self, a resume packet, the rules), cold and cached?
2. **Share:** what fraction of a run's tokens is boot?
3. **Quality:** what pass rate does a one-shot, tool-less run reach on the
   same 24 tasks and the same hidden graders?
4. **Price:** dollars per passed task, door against the pilot harness.

## Materials

- **Tasks and graders:** the pilot's 24 tasks (`bench/pilot/easy/tasks.py`,
  `hard/tasks.py`) and hidden graders (`*/grade.py`), unchanged.
- **The start packet**, built from a real Gnomon log (scratch, not kept):
  - *System block (the self and rules):* the resident Engineer's identity,
    values and three lessons, written as plain text, with the instruction
    to answer with one Python code block and nothing else. Target 1,500
    to 2,500 tokens (above Haiku 5.5's 512-token cache minimum).
  - *User message:* a resume packet for frame `firm/code`, rendered by
    Gnomon's `render_resume` at a 1,500-token budget, then the work order
    and the task's specification.
  The packet is the same for every task except the work order and spec.
- **Engine:** the door (`bench/cards/door/worker.js`), Claude only, text
  only, `max_tokens` 4,096, default temperature, no thinking.

## Arms

For each model (Claude Haiku 5.5 first; Claude Sonnet 5.5 second):
- **A, cold:** no `cache_control`. 24 calls, one per task.
- **B, warm:** `cache_control` (5-minute lifetime) on the system block. 24
  calls in sequence, so the first writes the cache and the rest read it.

One attempt per task per arm. 96 calls in all.

**Calibration:** one call per model with the full packet and the
one-word user message "ready", `max_tokens` 1, gives the boot's input
tokens as the API counts them.

## Measures (from the API's `usage`, per call)

`input_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`,
`output_tokens`, `stop_reason`, wall time; the grade (PASS or FAIL) from
the pilot's grader on the first Python code block in the reply.

- **Boot** = the calibration call's input tokens.
- **Boot share** = boot / (all input tokens + output tokens) per call.
- **Cost** at `polymechania/plan.py` prices (Haiku $0.10 in, $0.50 out,
  $0.01 cache read, $0.125 cache write per million; Sonnet $2, $10,
  $0.10, $2.50).
- **Pilot comparison:** the pilot's tokens were logged as one total; they
  are priced here as uncached input, which is an upper bound on what was
  paid. The comparison says so wherever it is shown.

## Decisions, fixed now

- **Thin boot holds** if boot is at most 4,000 tokens and the median boot
  share on Haiku is at most 20%.
- **Caching holds** if, in arm B, calls 2 to 24 read at least 90% of the
  system block from the cache.
- **Quality** is reported, not thresholded: the door's pass rate on each
  model against the pilot's 24/24. If Haiku falls below 20/24, record that
  a thin boot costs quality and that the fair comparison is a cascade
  (Haiku through the door, Sonnet on a failed grade), priced from these
  same calls.
- **The headline** is dollars per passed task, door against pilot, with
  the pilot's upper-bound caveat.

## T11, the runaway check (same session)

- A request with `max_tokens` 5,000 must be refused by the door (400).
- A request to write about 10,000 words with `max_tokens` 4,096 must stop
  with `stop_reason` `max_tokens` and at most 4,096 output tokens.
- So the worst case of one call is 4,096 output tokens plus its input,
  which is stated in dollars per model.

## What this cannot show

One attempt per task: pass rates have wide intervals (24 tasks). The
pilot's tasks are short and exactly specified; long, vague work (T1) is
where boot share and tool loss could look different. The self here is
written for the test, not grown by a resident.

## Amendment 1 (2026-10-28, after the review (Reviews, below), before any run)

All points of the independent review are taken. Where this amendment and
the text above differ, this amendment rules.

- **Thin boot holds** if boot is at most 4,000 tokens **and** at most 5%
  of the pilot's fixed start-up (about 79,000 tokens; regression intercept
  in `docs/architecture.md`, Reviews). Boot share is reported as
  description only: with a ~1,000-token boot and short tasks it is large
  by construction, so it cannot decide anything.
- **The pilot is priced as a bracket**, API-equivalent (it ran on a
  subscription, so no money was spent this way): each run's output fixed
  now at 1,000 tokens; the rest priced either all as cache reads (low) or
  all as uncached input (high). The headline gives the ratio at both ends.
- **Arms named for every decision.** Quality is pooled over A and B (48
  calls per model; A and B send the same prompt, so this is two attempts
  per task): "a thin boot costs quality" if fewer than 40 of 48 pass on
  Haiku. Dollars per passed task: headline on arm B (the form that would
  be deployed), A shown alongside. A cascade, if priced, pairs A with A
  and B with B.
- **Caching holds** if **each** of calls 2 to 24 in arm B reads at least
  90% of the boot (the calibration's input tokens) from the cache. Arm B
  now has two breakpoints: the self (system) and the resume packet (the
  first user block), since both are identical across calls.
- **Timing:** all 24 calls of an arm run back to back and are graded only
  afterwards, so grading cannot let the 5-minute cache lapse. Gaps
  between call starts are logged.
- **Size correction:** the self is about 850 tokens, not 1,500 to 2,500;
  with the packet the cached prefix is still above the 512-token minimum.
- **Disclosure:** the self's lessons (recursion depth, tie rules, speed)
  were written by someone who knew these 24 tasks, which may raise the
  door's pass rate. The packet's history no longer names any task. Fixed
  by hash before running:
  - `bench/boot/self.md` sha256 `144012916a3c9ae8d13a6bfffb1ccc787aa12ba72d01293bf093f370907d11a8`
  - `bench/boot/packet.txt` sha256 `27a78085d62b33fac879fc044c60741de6821803a7f2320b0c836bcf86d2a2af`
- **T11:** if Haiku stops the long essay before 4,096 output tokens, the
  result is inconclusive and is repeated once with a firmer prompt.
- **Order:** calibration; Haiku A, Haiku B; Sonnet A, Sonnet B; T11.

## Reviews

Folded in on the cleanup pass (2026-10-29), condensed to the points made; the full text of each review file is in git history at `fa517d6`.

One independent review by a separate agent (Claude Opus 5.5), 2026-10-28, before any run. It read the prereg, `docs/architecture.md` section 4 and its tests, `bench/pilot/`, `bench/boot/`, the door's `worker.js`, the `plan.py` prices and the prompt-caching docs, and edited nothing. 11 findings (3 must, 5 should, 2 minor, 1 check that passes). Amendment 1 above took all of them.

1. (must) The 20% boot-share threshold fails by construction: boot is about 2,400 tokens, a call adds a spec (~300) and a reply (~450), so the share is about 75%. The question is absolute (80k against 2-4k): use boot at most 4,000 tokens and at most 5% of the pilot's ~79,000; report share as description only.
2. (must) The pilot price is not an upper bound: pricing all pilot tokens at the input rate understates output cost, while Claude Code's prefix is mostly cache reads, which overstates. Report a bracket (low: all non-output tokens at cache-read price; high: T-O at input plus O at output, O fixed now, e.g. 5,000) and say the pilot ran on a subscription (API-equivalent prices).
3. (should) The quality comparison mixes three changes (no tools, one shot, a new prompt). The self's lessons were written knowing the 24 tasks and the packet says six were already "delivered, passed"; both bias the pass rate up. Disclose, and fix self.md and the packet by hash now.
4. (should) Arms A and B are the same prompt (only `cache_control` differs), so they are two attempts per task: report per arm and pooled (48 per model), and count a task passing in one arm and failing in the other as such.
5. (must) Thresholds named no arm: quality on each arm and pooled (threshold < 40/48); price headline on arm B (the deployed form), A alongside; the cascade pairs A with A and B with B.
6. (should) "Calls 2 to 24 read at least 90%": say each call (with one breakpoint a hit is all or nothing).
7. (minor) T11 has no outcome if Haiku stops early: inconclusive, then repeat with a prompt asking for a numbered list to 3,000 items.
8. The door permits it: `FIELDS` checks only top-level keys; `textOnly` ignores other keys so a text block with `cache_control` passes (also `ttl: "1h"`); `max_tokens` 5,000 is refused by `checkClaude` with 400 before any upstream call (check the `x-door` header on the 400).
9. (should) Cache minimum (512 tokens for Haiku 5.5 and Sonnet 5.5) and lifetime (5 minutes from request start, refreshed on a hit) are right, but self.md is ~850 tokens, not the stated 1,500-2,500; and `run()` grades each reply before the next call, so a slow hard grader can approach 5 minutes: grade after all 24 calls, or log gaps and exclude calls after a gap over 5 minutes.
10. (should) `report()` divides reads by call 1's `cache_creation`; if call 1 reads, the divisor is 0. Use the calibration's system-block count, or call 1's write plus read.
11. (minor) Optionally cache the packet too (second breakpoint, a user text block); define the caching criterion on both blocks if adopted.
