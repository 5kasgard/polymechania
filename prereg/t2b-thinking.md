# Pre-registration: T2b, thinking and Haiku's empty answers

Written 2026-10-29, before any run. A follow-up to T2 (`bench/boot`), from
its audit (`bench/boot/AUDIT.md`): five of Haiku's six failures were empty
answers at the 4,096-token cap, and T11 showed 1,721 thinking tokens on a
request that set no `thinking` field. Exploratory: one attempt per task.

## Question

Is unasked-for thinking what empties Haiku's answers, and which setting
should a resident's run use?

## Design

- **Tasks:** the pilot's 12 hard tasks (the easy ones all passed in T2).
- **Model and form:** Claude Haiku 5.5, arm B exactly as in T2 (same
  `self.md` and `packet.txt`, same hashes, both cached, `max_tokens`
  4,096), so only `thinking` changes.
- **Arms:**
  - **D, disabled:** `thinking: {"type": "disabled"}`.
  - **E, capped:** `thinking: {"type": "enabled", "budget_tokens": 2048}`.
- **Logged per call, newly:** `output_tokens_details.thinking_tokens`, and
  the content-block types in the reply.
- All 12 calls of an arm back to back, graded afterwards, as in T2.

## Decisions, fixed now

- **Thinking caused the empties** if T2's arm B (default) had at least two
  empty answers among these 12 tasks (it had two: regex, approx) and arm D
  has none.
- **Default setting for resident runs on Haiku:** whichever of D and E
  passes more of the 12; on a tie, the cheaper in dollars. Reported with
  T2's arm B alongside (10/12 on these tasks).
- With 12 tasks and one attempt, a difference of one or two passes is not
  evidence; it is reported as a direction to taste, not a result.

## Cost bound

24 calls, at most 4,096 output tokens each on Haiku: under $0.06.
