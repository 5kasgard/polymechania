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

Folded in on the cleanup pass (2026-10-29), verbatim from the review file named under each heading (git history, commit `fa517d6`); only the heading level of the review's own headings is lowered to nest here.

### Independent review of `t2-thin-boot.md`

Handling: amendment 1 of this file ("All points of the independent review are taken").

Independent review by a separate agent (Claude Opus 5.5), 2026-10-28,
before any run. Read: the prereg, `docs/architecture.md` §4 and tests,
`bench/pilot/` (results, tasks, graders, run.py), `bench/boot/` (run.py,
self.md), the door's `worker.js`, `plan.py` prices, and the prompt-caching
docs. Nothing edited but this file. 11 findings: 3 must, 5 should, 2 minor, 1 check that passes.

#### 1. Does the design answer its questions?

1. **(must) The 20% boot-share threshold fails by construction.** Boot is
   about 2,400 tokens (self.md is 3,627 chars, ~850 tokens; packet ≤1,500).
   A call adds a spec (~300) and a reply: pilot solutions average 1,644
   bytes (~450 tokens). Expected share ≈ 2,400 / 3,150 ≈ 75%. For short
   tasks, a thin boot *is* most of a thin run; the share cannot reach 20%.
   The question in §4 is absolute (80k against 2-4k). Replace with: boot
   ≤ 4,000 tokens **and** ≤ 5% of the pilot's fixed ~79,000; report share
   as a description only.
2. **(must) The pilot price is not an upper bound.** Pricing all pilot
   tokens at the input rate prices the pilot's *output* at 1/5 of its cost,
   which understates; Claude Code's prefix is mostly cache reads (0.1x/0.05x),
   which overstates. The net sign is unknown. Report a bracket: low = all
   non-output tokens at cache-read price, high = (T − O) at input plus O at
   output, with O fixed now (e.g. 5,000). The headline is the ratio at
   both ends. Also say the pilot ran on a subscription; these are API-
   equivalent prices, not money spent.
3. **(should) The quality comparison mixes three changes:** no tools (the
   pilot made 1-5 tool calls, mostly to test its code; Haiku more than
   Sonnet), one shot, and a new prompt. The self's lessons (recursion depth,
   tie rules, speed) were written knowing these 24 tasks, and the packet
   says six of them (slugify, roman, intervals, lru, topo, wrap) were
   already "delivered, passed". Both bias the door's pass rate up. Disclose
   this in the prereg, and fix self.md and the packet by hash now.
4. **(should) Arms A and B are the same prompt** (only `cache_control`
   differs), so they are two attempts per task. Say now how quality is
   reported: per arm and pooled (48 per model), and that a task passing
   in one arm and failing in the other is counted as such, not resolved.

#### 2. Thresholds left to the analyst

5. **(must) Which arm?** "Haiku falls below 20/24", "median boot share on
   Haiku" and "dollars per passed task" name no arm. Fix: quality on each
   arm and pooled, threshold on the pooled rate (< 40/48); price headline
   on arm B (the deployed form), arm A alongside; the cascade pairs
   Haiku-A with Sonnet-A and B with B.
6. **(should)** "Calls 2 to 24 read at least 90%" — say *each* call (the
   code takes the minimum). With one breakpoint a hit is all or nothing,
   so this means "every call hits"; say that.
7. **(minor) T11** has no outcome if Haiku stops early (`end_turn`) on
   the essay. State it as inconclusive, then repeat once with a prompt
   that asks for a numbered list to 3,000 items.

#### 3. Does the door permit it?

8. **Yes.** `FIELDS` checks only top-level keys (`system` is allowed);
   `textOnly` requires each block to have `type === "text"` and a string
   `text`, and ignores other keys, so `{"type":"text","text":…,
   "cache_control":{"type":"ephemeral"}}` passes, also in user content
   arrays (and `ttl: "1h"` would too). `max_tokens` 5,000 is refused by
   `checkClaude` with 400 before any upstream call, so T11a tests the door.
   Check the `x-door` header on the 400 so it is the door, not the API.

#### 4. Cache lifetime and minimum

9. **(should) Minimum and lifetime are right.** Haiku 5.5 and Sonnet 5.5
   are 512 tokens (docs); under the minimum, caching is silently skipped.
   The 5-minute lifetime is measured from the *start* of each request and
   refreshed on a hit. But self.md is ~850 tokens, not the stated 1,500-
   2,500: amend the target. And `run()` grades each reply before the next
   call; hard graders allow up to 120 s plus generation time, so a slow
   case can approach the 5 minutes. Grade after all 24 calls, or log the
   gap between request starts and declare any call after a > 5 minute gap
   excluded from the cache criterion.
10. **(should)** `report()` divides reads by call 1's `cache_creation`. If
    call 1 *reads* (a smoke test within 5 minutes, or a resumed run), the
    divisor is 0 and the criterion fails spuriously. Use the calibration's
    system-block count, or call 1's write + read.

#### 5. Amendments before running

- Replace the share threshold (1); bracket the pilot price (2).
- Name the arm for each decision; pool A and B for quality (4, 5).
- "Each call" for caching; fix the divisor; separate grading from calls
  (6, 9, 10).
- Amend the self's size; hash self.md and packet.txt; disclose that the
  lessons and packet were written knowing the tasks (3, 9).
- **(minor, 11)** Optional: cache the packet too. It is identical across
  calls and larger than the self; a second breakpoint on the packet as a
  user text block (the door allows it) is where most of the cached boot
  would be. If adopted, define the caching criterion on both blocks.
