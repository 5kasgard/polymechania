# Gnomon #50: closing the file-access gap (design options)

Status: **options for the owner to decide**, 2026-10-29. Researched and written by a Sonnet
sub-agent (plan only) from a brief by the session; one claim checked by the session
(`store::append` re-reads the whole log on every append: confirmed, `store.rs` line 495).
Not yet reviewed by a non-Claude model.

## The gap

Hashing uses no secret, so any process that can open the log can append a valid event as any
writer (border probe B4), and every compartment is plain text in the file (B9). Compartments
hold only for callers that go through the gate.

## Options

| | A. The gate is the only file holder | B. Per-writer signatures (Ed25519) | C. Per-compartment encryption | D. B + C (+ A) |
|---|---|---|---|---|
| Stops | B4 and B9 for any process not running as the gate's user | B4, and edits to the file, for anyone without the writer's key | B9 for anyone without the compartment key, backups and sync included | both |
| Does not stop | a shell running as the same user; root; copies of the file | reads (B9); cutting off the tail; a key stolen from a same-user file | appends (junk can poison replay); a key holder reads its compartment | rollback, unless the head is pinned outside the log |
| Protocol | no change | version 7 | version 8 | 7 then 8 |
| Problem moves to | the daemon's user and socket | where keys are kept; the owner key becomes the root | key custody per compartment | both |
| New code | none in the core; a long-running server | an Ed25519 library (`ed25519-dalek`): the core's first outside crypto crate | an AEAD library (`chacha20poly1305`) | both |
| Cost (estimates) | +50-100 µs per append | about +55 µs per append; full verify of 1M events about 5 s on 8 cores | under 1 µs per append | |

Details, arithmetic and the migration plan are in the sub-agent's report (summarised here).
Main points:
- **Signatures (B):** the writer signs the envelope hash; registrations carry public keys; a
  `schema_change` to 7 carries the keys map, so the cutover is one event. A build without
  signature support must refuse a version-7 log. Hand-writing Ed25519 (with SHA-512) is advised
  against.
- **Encryption (C):** claim ids are hashes of the plaintext, so encrypted claims would need
  keyed ids, or a guessed statement could be confirmed; snapshots would hold plaintext and must
  be sealed; metadata (writer, kind, time, sizes) still shows.
- **Rollback:** sign a (count, head) checkpoint, as Certificate Transparency (RFC 6962) and
  Sigstore Rekor (C2SP checkpoints) do.

## Options with no new dependency (added 2026-10-29, after the owner asked)

The core already has SHA-256 and HMAC-SHA-256 (`sha256.rs`, tested against RFC 4231).

| | E. HMAC per writer | F. Hash chain per writer (S/KEY, Lamport 1981, [RFC 2289](https://www.rfc-editor.org/rfc/rfc2289)) |
|---|---|---|
| How | each write carries HMAC(writer key, envelope hash) | registration publishes the top of a SHA-256 chain from a secret seed; each write reveals the next value down |
| Who can check | only a holder of the writer's key (in practice the gate) | anyone, with SHA-256 alone |
| Stops B4 | yes, for anyone without the key; the gate itself could forge | yes, for anyone without the seed, the gate included |
| Limits | moves trust to the gate | a set number of writes per chain, then a re-key event; cutting off the newest event and rewriting it stays possible, as today (needs an outside checkpoint) |
| New code | a few lines on existing HMAC | a few lines on existing SHA-256 |

Also ruled out for now: calling the system's `ssh-keygen -Y sign` (real Ed25519 with no crate, but a program
call per append and installation differences); file permissions alone (A).

**Session's recommendation after this: F for version 7.** It is publicly checkable and needs nothing new.
Reading (B9) still needs encryption, the one part that needs an outside library or new crypto code.

## Recommendation (the sub-agent's, before options E and F)

Version 7 = signatures only (B). It is the smallest step that makes B4 cryptographic and survives
copies of the file. B9 stays open until version 8 (encryption), or meanwhile by running the gate
as a separate user (A). Tests that would prove it: a hand-made line without a valid signature is
refused on append and on replay; a wrong or unregistered key is refused; a flipped byte fails;
old logs and the test vectors still verify; a writer with no key fails closed; RFC 8032 vectors
pass; an instance signs only as itself.

## The decision for the owner

Adding `ed25519-dalek` would be the core's first outside dependency (today: standard library plus a
hand-written SHA-256). Yes, no, or wait.

## Found on the way

`store::append` reads the whole file on every append, so append cost grows with the log (a
separate speed issue, not security).

## Sources (opened by the sub-agent)

[ed25519-dalek](https://docs.rs/crate/ed25519-dalek/latest) ·
[its changelog](https://github.com/dalek-cryptography/curve25519-dalek/blob/main/ed25519-dalek/CHANGELOG.md) ·
[age spec](https://github.com/C2SP/C2SP/blob/main/age.md) · [RFC 6962](https://www.rfc-editor.org/rfc/rfc6962) ·
[C2SP tlog-checkpoint](https://c2sp.org/tlog-checkpoint) · [Sigstore Rekor](https://docs.sigstore.dev/logging/overview/) ·
[libsodium signatures](https://libsodium.gitbook.io/doc/public-key_cryptography/public-key_signatures)
