[[Architectures]] [[Clean Architecture]] [[Multi-tier and Layered Architecture]]

# System Architecture

> System architecture is the map of boxes and arrows — services, data stores, and failure domains you run in prod.

---

## How it works

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


## Configuration and commands

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


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Cascading outage | Missing timeouts/bulkheads | Add limits; fail fast |
| Split brain | Two writers | Single writer or consensus |
| Hot dependency | One DB for everything | Split read models / shards |
| “Works in diagram” | No SLO / capacity | Load test critical path |

---


## Decision

We will … because …


## Consequences

**Positive:** …

**Negative / trade-offs:** …


## Alternatives considered

| Alternative | Why rejected |
|-------------|--------------|
| … | … |


## Gotchas

> [!WARNING]
> **Pretty boxes ≠ operable system** — without SLOs, runbooks, and ownership, architecture is a slide.

> [!WARNING]
> **Shared database as “integration”** — couples deploy cycles and schemas forever.

---


## When not to use

- **Prototype / spike** — skip multi-service until the product question is answered.
- **Single-team CRUD** — modular monolith often beats premature microservices.


## Related

[[Clean Architecture]] [[Multi-tier and Layered Architecture]] [[feature flag]] [[Idempotent-key]]

## Sources

- [Wikipedia — System Architecture](https://en.wikipedia.org/wiki/System_Architecture)
