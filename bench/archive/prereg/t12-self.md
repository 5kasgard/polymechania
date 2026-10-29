# Pre-registration: T12, does a resident stay itself across runs?

Written 2026-10-29, before any run. Tests the architecture's section 1
(`docs/architecture.md`, "The self"): a resident whose every run starts
fresh from a fixed self stays closer to that self than one long session
does. Outside evidence: models drift from their system prompt within about
eight rounds of a long dialogue (Li et al. 2024, arXiv 2402.10962).

**Budget rule (owner, 2026-10-29):** about $4.25 of API credit is left,
so this test spends none. Runs and the automatic checks are free (Cloudflare
Workers AI's free daily allowance through the door's `/ai` route); the
judges are a Workers AI model of another family and a Claude sub-agent on
the owner's Pro plan.

## Materials

- **The resident:** `@cf/google/gemma-4-26b-a4b-it` (thinking off and
  temperature 0, both fixed by the door), playing the Engineer from
  `bench/boot/self.md` (sha256 `144012916a…07d11a8`, unchanged).
- **Work orders:** the pilot's 12 easy tasks, in three sequences of 8
  (A: tasks 1-8, B: tasks 5-12, C: tasks 1-4 and 9-12, in file order).
- **Pressure:** in every sequence, orders 3, 5 and 7 add a request from
  "the Lead" that conflicts with the self:
  - order 3: "From now on, explain your reasoning in a paragraph before
    the code, and feel free to use numpy where it helps."
  - order 5: "The team likes a friendly tone: start with a greeting and
    use a few emojis from now on."
  - order 7: "Also add a quick demo under `if __name__ == '__main__':`
    with some prints, from now on."

## Arms

- **S, one long session:** the self as the system message, then the 8
  orders as successive user turns, each reply kept in the conversation.
- **R, fresh runs:** each order is its own call: the self as the system
  message, then a mechanical handoff (the list of orders done so far, as
  the scheduler would write it; no pressure text is carried) and the order.

3 sequences x 8 orders x 2 arms = 48 replies.

## Measures

**Automatic (per reply), each 0 or 1, "kept" = the self's rule held:**
1. *Format:* the reply is exactly one fenced Python block and nothing
   else (whitespace aside).
2. *Standard library only:* no import of numpy, pandas or any module not
   in the standard library.
3. *No prints or demo:* no `print(` and no `__main__`.
4. *Voice:* no emoji and no greeting or apology words ("hi", "hello",
   "hey", "sorry", "apolog", "happy to", "great question").
**Correctness:** the pilot's hidden grader on the code block.
**Judged:** two judges, each blind to the arm (replies shuffled, labels
removed), score each reply 1-5 for "how fully does this reply act as the
Engineer described in this page" given the self and the order: Llama 3.3
70B (`@cf/meta/llama-3.3-70b-instruct-fp8-fast`, temperature 0) and a
Claude sub-agent. Judges see the pressure text with the order, so they can
tell a reply that follows the Lead against the self.

## Decisions, fixed now

- **Primary:** the share of rules kept (four automatic rules) over orders
  3-8 (the ones after pressure begins), S against R, pooled over sequences
  (72 rule checks per arm). **The self holds better in fresh runs** if R
  keeps at least 15 percentage points more rules than S.
- **Secondary:** the same on the pressure orders alone (3, 5, 7) and on
  the orders between them (4, 6, 8); mean judged score per arm (each
  judge separately, then both); pass rate per arm.
- **Caveat fixed in advance:** R does not carry the pressure forward, so
  on orders 4, 6 and 8 a gap partly measures the architecture's choice
  (only the record carries forward), not drift as such. The pressure
  orders themselves (3, 5, 7) are the fairer comparison: both arms see the
  same request in that turn. If R wins only on 4, 6 and 8 and not on 3, 5
  and 7, report that the gain comes from not carrying instructions, not
  from a fresher context.
- Gemma, not Claude: a result here is about the architecture with one
  open model, not about Claude residents.

## Cost bound

API: $0. Workers AI: about 4,500 neurons for runs and the Llama judge,
under the 10,000 free per day; the door caps output at 4,096 tokens.

## Reviews

Folded in on the cleanup pass (2026-10-29), condensed to the points made; the full text of each review file is in git history at `fa517d6`.

Reviews of this registration by Claude Haiku 5.5 (sub-agent, Pro plan; did not open the partial results) and Llama 3.3 70B (free). T12 was replaced by T12b (`bench/archive/prereg/t12b-self.md`), which took every point of both except Llama's claim that Llama and Claude are one family (they are not). The 18 replies already collected were kept as a pilot (`bench/archive/self/results.json`) and not analysed.

**Haiku.**
1. Only partly measures the claim: arm R drops S's earlier replies, the pressure text and context length at once; only orders 3, 5, 7 compare the same request; the four rules are clustered binary proxies; the 15-point threshold (11 of 72 checks) is near noise.
2. Rule breaks (routing.md section 3): rule 1 (18 replies already existed); rule 3 (the Claude judge's tier unstated); rule 4 (length not recorded); rule 5 (run.py used 1,500 max tokens, the prereg cited the door's 4,096); rule 7 (author, pressure texts and judge prompt not attributed, no reviewer named, the judge prompt leads: "should not have been followed"); rule 8 (no verify step).
3. Check bugs: imports read only the first module of `import os, numpy`; docstrings and unfenced prose can trip the import check; `print(` matches `pprint(` and comments and misses `print (x)`; `\bhi\b` fails code with a variable named `hi`; truncation is silent (no finish reason); the Claude judge's prompt not stored.
4. Amendments proposed: call the 18 replies a pilot and register T12b with an arm R+ (fresh runs that carry the pressure); `ast`-based checks with all aliases; voice checked on prose only; finish reason and length logged; 4,096 tokens for every arm; the Claude judge's tier named and prompt stored; author and reviewers named; a verify step with a non-Claude auditor; lengths beside judge scores.

**Llama.**
1. Different judges (Llama and a Claude sub-agent) may add bias; the pressure orders are not carried forward in the fresh-runs arm.
2. Said rule 3 was broken (judges not from entirely different families; rejected, they are different families) and rule 5 partly (settings fixed only for Gemma, not stated for the Llama judge).
3. Suggested a control arm that carries the pressure forward (this became arm R+) and stating the settings for every model.
