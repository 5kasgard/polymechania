# The door

The only way E1's workers, reviewer and judges reach a model (amendment 1,
B, of `prereg/cards-v2.md`). Workers get text in and text out; this
Worker's code is what enforces it.

- `worker.js`: deployed as `polymechania-door` on the owner's Cloudflare
  account. Claude through `/v1/messages`: Haiku and Sonnet only, text only,
  no tools, no files, no streaming, at most 4,096 tokens. Workers AI through
  `/ai`: the reviewer and judge models only.
- Two locks: a Cloudflare Access service token (`polymechania-door`), and a
  door token (secret `DOOR_TOKEN`). Neither is in this repository.
- The Anthropic key is a Worker secret (`ANTHROPIC_API_KEY`) that the owner
  sets in the Cloudflare dashboard; nothing that calls the door can read it.
  It is a key for its own Console workspace, with a monthly spend limit.
- `test_door.mjs`: local checks of every rule (`node test_door.mjs`).

After E1: delete the Worker, the Access application and service token, and
the API key.

## Change of 2026-10-29: effort and adaptive thinking

For T2c (`prereg/t2c-effort.md`): `output_config` is allowed with `effort`
only, and only `low`, `medium` or `high` (`xhigh` and `max` need far more
than the 4,096-token cap); thinking types `adaptive` and `between_tools`
are allowed besides `enabled` and `disabled`; `budget_tokens` only with
`enabled`; any other key inside `thinking` or `output_config` is refused.
Reviewed before deploy by a separate agent (verdict: safe; it found that
`budget_tokens` passed on other thinking types, now refused, and the
missing tests, now added). Deployed by replacing the script content only,
so bindings and secrets were kept; the live door then refused `effort`
`max`, `output_config.format`, `budget_tokens` with `adaptive`, and
`tools`. Deployed `worker.js` sha256
`97d22c61bfe1937e5ecc1809b62c8a2c787147560745e4d92432206572d72963`.

## Change of 2026-10-29 (b): more free models on /ai

For E-ext (`prereg/eext-benchmarks.md`): five free Workers AI text models
added to the `/ai` allowlist, and an opt-in `default_thinking: true` that
skips the Gemma-only "thinking off" (any other value is refused).
Temperature 0 and the 4,096-token cap still apply to every `/ai` call.
Reviewed before deploy by Gemma 4 26B (`REVIEW-2026-10-29b.md`: deploy).
Deployed by editing the live script (whose hash matched the last deploy,
`97d22c…`) and uploading only when the result matched the reviewed file:
sha256 `0632e72702216df699cace4fa298e090ad48a21d0613db9495b945b805936263`.
Live probes: an unlisted model and `default_thinking: "x"` refused; a new
model answered.
