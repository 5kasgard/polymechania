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
