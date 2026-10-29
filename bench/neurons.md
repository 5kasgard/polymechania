# When does the Workers AI free allowance come back? (q24)

Written 2026-10-29 00:25 UTC, before the probes below, so the predictions
are fixed first.

## What happened

- Cloudflare's pricing page: "All limits reset daily at 00:00 UTC."
- Cloudflare's own analytics (GraphQL `aiInferenceAdaptiveGroups`, hourly):
  28 Oct 19:00 UTC 2,972; 20:00 UTC 6,357; 29 Oct 00:00 UTC 2,876 (the
  T12c Llama judge and one Gemma audit). Total 12,207 in the 24 hours
  before the refusal; 2,876 since 00:00 UTC.
- At 00:20 and 00:23 UTC the door was refused: "4006: you have used up your
  daily free allocation of 10,000 neurons".

So the documented reset does not explain the refusal. A rolling 24-hour
window does.

## Two readings and what each predicts

| Probe time (UTC, 29 Oct) | Rolling 24 h (used then) | Calendar day, counter lagging |
|---|---|---|
| 03:00 | refused (12,207) | allowed |
| 19:30 | refused unless under ~10,000 (9,233 once 19:00 rolls off: allowed) | allowed |
| 21:15 | allowed (about 2,900) | allowed |

The decisive probe is 03:00: refused supports rolling, allowed supports a
calendar day. The guard (`bench/neurons.py`) uses the rolling window,
the stricter reading, until the probes say otherwise.

## Probes

Raw rows: `neurons-probes.jsonl` (time, neurons used in the 24 h and the
UTC day by our log, allowed or refused).

- 00:23: refused (24 h 12,207; UTC day 2,876). Both readings allow this
  only if the counter lags, so it does not decide.
