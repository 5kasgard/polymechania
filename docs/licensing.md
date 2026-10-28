# Licensing: options and a recommendation (not legal advice)

Status: **recommendation for the owner to decide**, 2026-10-29. Licences
bind the owner legally; check with a lawyer before relying on any of this,
and before anyone pays (queue q22, q23).

## Options, as published

| Option | What it allows | Protects the hosted product? | Catches |
|---|---|---|---|
| Apache-2.0 or MIT | anything, with attribution (Apache adds a patent grant) | no: anyone can host a copy | maximum adoption |
| AGPL-3.0 | anything, but a modified version run as a service must publish its source | partly | many companies refuse AGPL by policy ([FSL's FAQ](https://fsl.software/)) |
| Dual: AGPL-3.0 + commercial | the AGPL, or a paid licence without its duties | yes | needs the owner to hold all copyright (a contributor agreement for outside contributions) |
| FSL-1.1-Apache-2.0 (Fair Source) | read, use, modify and self-host for anything but a competing product; each release becomes Apache-2.0 after two years | yes, for two years per release | "source-available", not OSI open source; used by Sentry ([Sentry licensing](https://open.sentry.io/licensing), [fair.io](https://fair.io/licenses)) |
| Business Source License | like FSL, with a chosen change date and use grant | yes | more terms to choose |

## Recommendation (hypothesis): license by part

The vision depends on two things pulling different ways: a plain protocol
and theme format that *anyone's* engine and art can speak (wants adoption),
and a hosted product that pays for itself (wants protection).

- **Apache-2.0** for the parts others should build on: the plain protocol
  and spec, the concepts/events contract, the theme ("world" file) format
  and the shipped themes, client libraries, and benchmarks.
- **FSL-1.1-Apache-2.0** for the product: the scheduler, the routing and
  cards services, the hosted world, the door.
- **Packs** people share (themes, art, mechanics): the author's choice,
  with a default of CC BY 4.0 offered in the pack tool.
- Gnomon: the same split (protocol and spec Apache-2.0; core FSL), if the
  owner wants the same model there.
- A short contributor agreement before accepting outside contributions,
  so the owner can relicense later (keeps a commercial licence possible).

**Why this and not AGPL dual licensing:** FSL keeps company users
comfortable (no copyleft) while still stopping a direct competitor, and
becomes fully open on a timer; the permissive protocol keeps the commons
open for any engine. **What would change it:** a lawyer's view; or if the
owner wants the code fully open from day one (then Apache-2.0 throughout,
competing on the hosted service and the record alone).

## To decide

One word from the owner: **"split"** (as above), **"apache"** (all
permissive), **"fsl"** (all FSL), or **"agpl-dual"**. Nothing is licensed
until then.
