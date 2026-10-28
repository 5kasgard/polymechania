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
