# Independent review of `t2-thin-boot.md`

Independent review by a separate agent (Claude Opus 5.5), 2026-10-28,
before any run. Read: the prereg, `docs/architecture.md` §4 and tests,
`bench/pilot/` (results, tasks, graders, run.py), `bench/boot/` (run.py,
self.md), the door's `worker.js`, `plan.py` prices, and the prompt-caching
docs. Nothing edited but this file. 11 findings: 3 must, 5 should, 2 minor, 1 check that passes.

## 1. Does the design answer its questions?

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

## 2. Thresholds left to the analyst

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

## 3. Does the door permit it?

8. **Yes.** `FIELDS` checks only top-level keys (`system` is allowed);
   `textOnly` requires each block to have `type === "text"` and a string
   `text`, and ignores other keys, so `{"type":"text","text":…,
   "cache_control":{"type":"ephemeral"}}` passes, also in user content
   arrays (and `ttl: "1h"` would too). `max_tokens` 5,000 is refused by
   `checkClaude` with 400 before any upstream call, so T11a tests the door.
   Check the `x-door` header on the 400 so it is the door, not the API.

## 4. Cache lifetime and minimum

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

## 5. Amendments before running

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
