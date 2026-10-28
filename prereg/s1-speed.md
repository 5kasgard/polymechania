# Pre-registration: S1, speed by where a job runs

Written 2026-10-29, before any run. Tests the routing hypothesis that
*where it runs* belongs on every worker's card (`docs/routing.md`
section 2), with the owner's question: does the machine matter, and how
much does doing things at once help?

**Authorship:** Claude Opus 5.5 (the session). **Budget:** API $0; Workers
AI free allowance (about 500 neurons); GitHub Actions free on public
repositories; Codespaces only within the personal free quota (120 core
hours a month on GitHub Free; GitHub docs, `product-usage-included`) and
only if this session can reach it.

## Published facts used, not re-measured

- GitHub's standard Linux runner for public repositories: sources
  disagree (the docs page shows a 2-CPU row; GitHub's 2024 blog and a
  2026 summary say 4 vCPU and 16 GB). **Measured here instead**: each arm
  prints its CPU count.
- Workers AI text generation: 300 requests a minute per model (Cloudflare
  docs, Limits), so 8 calls at once is well inside.
- Claude through the API is left out: it costs money, and its limits come
  back in the response headers during real work.

## Jobs and arms

**J1, exact work (grading):** regrade the 96 saved T2 solutions with the
pilot's graders (the same `bench/verify.py` work, grading only), three
times; workers = 1 (one at a time) and workers = the machine's CPU count.
- **Here:** this session's container.
- **Actions:** a `workflow_dispatch` job on `ubuntu-latest`, plus queue
  time (from dispatch to the job starting) and set-up time, read from the
  run's timings.
- **Codespaces:** the default machine, only if `gh codespace` works from
  here; otherwise reported as not reachable.

**J2, model calls:** 24 short calls to `@cf/google/gemma-4-26b-a4b-it`
through the door (the easy task specs, "reply with the function only",
`max_tokens` 256), one at a time and 8 at once, from this container.

## Measures

Wall time per arm (median of three for J1; one pass each for J2),
CPU count, and for Actions the queue and set-up time separately.

## Decisions, fixed now

- **Doing things at once pays** for a job if its wall time drops by at
  least half (2x).
- **Route a job to Actions** if, *including* queue and set-up time, it
  finishes at least 2x faster than here, or if it frees the session for
  other work for more than a minute at no loss of speed. Otherwise
  report where it is fastest.
- Speed is descriptive per machine and day; one day's numbers are a
  direction, not a constant.
