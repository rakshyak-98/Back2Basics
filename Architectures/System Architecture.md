<!-- note-strategy: decision -->
[[Architectures]] [[Clean Architecture]] [[Multi-tier and Layered Architecture]]

# System Architecture

> System architecture is the map of boxes and arrows — services, data stores, and failure domains you run in prod.

---

## Index

- [[#Context]]
- [[#Decision]]
- [[#Consequences]]
- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Alternatives considered]]
- [[#Related]]

## Context

…

## Decision

We will … because …

## Consequences

**Positive:** …

**Negative / trade-offs:** …

## Mental model

**Say it in one breath:** Draw who talks to whom, what must stay up, and where data is the source of truth — before picking frameworks.

```txt
Clients → Edge (CDN/LB) → App services → Data (DB/queue/cache)
                ↓
           Observability + auth boundaries
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Boundary** | Trust / deploy unit | “This service owns orders.” |
| **Source of truth** | Canonical store | “Orders live in Postgres; cache is a hint.” |
| **Failure domain** | What dies together | “One AZ vs one pod.” |
| **Sync vs async** | Call now vs queue | “Checkout sync; email async.” |

---

## Standard config / commands

```txt
# Architecture checklist (write it down)
1. Actors & trust boundaries
2. Sync paths + timeouts
3. Async paths + DLQ
4. Data ownership per service
5. Blast radius on dependency loss
```

| Knob | Why it matters |
|------|----------------|
| Timeout + retry policy | Prevents retry storms |
| Idempotency on writes | Safe client retries |
| Health / readiness | LB doesn’t send to dead pods |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Cascading outage | Missing timeouts/bulkheads | Add limits; fail fast |
| Split brain | Two writers | Single writer or consensus |
| Hot dependency | One DB for everything | Split read models / shards |
| “Works in diagram” | No SLO / capacity | Load test critical path |

---

## Gotchas

> [!WARNING]
> **Pretty boxes ≠ operable system** — without SLOs, runbooks, and ownership, architecture is a slide.

> [!WARNING]
> **Shared database as “integration”** — couples deploy cycles and schemas forever.

---

## When NOT to use

- **Prototype / spike** — skip multi-service until the product question is answered.
- **Single-team CRUD** — modular monolith often beats premature microservices.

## Alternatives considered

| Alternative | Why rejected |
|-------------|--------------|
| … | … |

## Related

[[Clean Architecture]] [[Multi-tier and Layered Architecture]] [[feature flag]] [[Idempotent-key]]
