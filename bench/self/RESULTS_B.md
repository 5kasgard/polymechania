# T12b results: does a resident stay itself across runs?

Run 2026-10-29 under `prereg/t12b-self.md` (committed before any T12b
run, after reviews by Haiku and Llama). Raw data: `results_b.json`; code:
`solutions_b/`; blind judging: `blind/` (batch, `llama.json`,
`haiku.json`). Numbers and grades recomputed by `python bench/verify.py
self` (all match). Audited by Llama 3.3 70B (`AUDIT_B.md`; a first attempt
without the report is kept as `AUDIT_B_failed_first_try.md`). **API spend: $0.** Workers AI: 2,819 neurons for the
runs and 3,375 for the Llama judge, inside the free daily allowance; the
Haiku judge used 293,174 tokens of the owner's Pro usage.

Resident: Gemma 4 26B (temperature 0, thinking off, 4,096-token cap) as the
Engineer of `bench/boot/self.md`; the pilot's 12 easy tasks in three
sequences of 8; on orders 3, 5 and 7 the Lead asks for things the self
forbids (reasoning before code and numpy; a greeting and emojis; a demo
with prints).

## The pre-registered decisions

| Arm | Rules kept, orders 3-8 | Pressure orders (3, 5, 7) | Orders between (4, 6, 8) |
|---|---|---|---|
| S, one long session | 47/72 = **65%** | 23/36 | 24/36 |
| R, fresh runs, handoff carries no instructions | 62/72 = **86%** | 28/36 | 34/36 |
| R+, fresh runs, handoff carries the Lead's requests | 37/72 = **51%** | 19/36 | 18/36 |

- **Fresh context helps the self (R+ at least 15 points above S):** does
  **not** hold. R+ was 14 points *below* S; that gap is under the
  pre-registered 15 points, so it is a direction, not a result: with the
  same instructions in view, a fresh run kept the self no better than one
  long session, and here possibly worse.
- **Carrying instructions costs the self (R at least 15 points above R+):**
  **holds**, by 35 points.

So the hypothesis in `docs/architecture.md` (a fresh run from a fixed self
stays closer to it) found no support here. What kept the resident
itself was that the Lead's conflicting requests were not written into
what the next run read. The pre-registration warned that this could be
the source of any gain; it was the whole of it.

## Secondary measures

| Arm (orders 3-8) | Llama 70B mean (1-5) | Haiku mean (1-5) | Mean length (chars) | Graded pass |
|---|---|---|---|---|
| S | 3.61 | 3.39 | 3,099 | 14/18 |
| R | **4.11** | **4.11** | 2,716 | 14/18 |
| R+ | 2.94 | 2.83 | 3,094 | 11/18 |

- Both judges, blind and from two families, order the arms as the rule
  checks do (R, then S, then R+). Their scores correlate with the share of
  rules kept (0.62 Llama, 0.67 Haiku).
- They agree exactly on 14 of 72 replies and within one point on 52.
- **Length:** Haiku's scores fall with length (correlation -0.61), Llama's
  do not (0.02). R's replies were shorter; part of Haiku's preference for
  R may be for brevity, which the self asks for ("plainly, briefly"), so it
  is not plainly padding-bias in reverse; Llama's agreement without that
  correlation supports the ordering.
- By rule: *format* (exactly one code block) was kept 0/18 in S and R+
  after the first pressure order, 13/18 in R; *voice* (no greeting or
  emoji) 13/18 in S, 18/18 in R, 7/18 in R+; *standard library only* held
  almost everywhere (no arm took up numpy).

## What it means (hypotheses for the architecture, not results)

- **The handoff is the lever, not the run length.** A resident stays
  itself if instructions that conflict with its self do not become
  standing text in the record its runs read. That is a rule about *who may
  write what into a resident's starting packet* (the owner may change the
  self; a Lead's request applies to its order, unless the owner makes it
  standing), which Gnomon's gate could enforce.
- **Listing requests as "standing" made them stronger:** R+ (requests
  restated in a fresh packet) broke the self more than S (the same
  requests in a long history). Text at the top of a fresh context may
  weigh more than text deep in a long one.
- A long session did not collapse either (65%): the self survived in part.

## Limits

One open model (Gemma 4 26B) at temperature 0; 12 easy tasks, three
sequences (72 rule checks per arm, clustered: four rules per reply, tasks
shared across sequences); pressure texts and the self written by the
author (Claude), knowing the tasks; the mechanical handoff is the
author's design. A Claude resident, other pressure, or a richer handoff
could come out differently.
