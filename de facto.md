[[de facto]] [[Release cycle]] [[general]]

# de facto standard

> Practice or product so widely adopted it **behaves like** a standard — without formal standards-body ratification (contrast **de jure**).

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Examples]]
- [[#When it matters]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**De jure** = by law/spec (ISO, RFC, ECMA). **De facto** = by market habit (Git, Docker, `{json}` APIs). Interop often follows de facto before formal specs catch up (e.g. OAuth flows, S3 API shape). Risk: vendor lock-in, spec drift, sudden deprecation.

## Standard config / commands

…

## Examples

| De facto | Notes |
|----------|-------|
| Git | Not the only VCS; default for OSS/commercial |
| Linux on servers | Not the only UNIX; dominant cloud image |
| JSON REST | Not the only API style; OpenAPI documents reality |
| `docker run` | OCI replaced single vendor runtime story |

## When it matters

- **Integration** — "everyone supports S3 API" beats obscure standard.
- **Hiring/tooling** — de facto skills transfer vs niche spec compliance.
- **Risk** — single implementer defines behavior until commoditized.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |

## Gotchas

> [!WARNING]
> …

## When NOT to use

…

## Related

[[Release cycle]] [[general]] [[Protocol/open api specification]]
