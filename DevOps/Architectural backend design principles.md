[[DevOps]] [[orchestration]] [[API design]] [[SOLID]]

# Architectural backend design principles

> Backend architecture principles — stable interfaces, clear module boundaries, and short data paths so services stay changeable under load.

## Mental model

**Say it in one breath:** Standardize how services talk (errors, authentication, timeouts), keep modules replaceable, and cut unnecessary hops. Consistency beats clever one-offs.

```txt
Client → Edge/API → Service A → (events|RPC) → Service B → DB
              │
         one error shape, one auth story, one observability bag
```

| Principle | Practice |
| --- | --- |
| **Modularity** | Bounded contexts; deploy independently when it pays off |
| **Interface contracts** | OpenAPI/proto + versioning |
| **Data flow** | Prefer fewer hops; sync vs async on purpose |
| **Failure policy** | Timeouts, retries with jitter, idempotency |
| **Observability** | Trace id on every hop |

## Standard config / commands

```yaml
# Contract-first sketch
openapi: 3.0.3
paths:
  /orders:
    post:
      responses:
        "201": { description: created }
        "409": { description: idempotent replay }
```

```txt
Checklist per new service
[ ] Authn/z pattern matches platform
[ ] Timeouts < caller timeout
[ ] Idempotency keys on writes
[ ] Structured errors (code, message, trace)
[ ] SLIs: latency, error rate, saturation
```

| Knob | Why it matters |

| API versioning | Avoid silent breakages |
| --- | --- |
| Shared error envelope | Clients handle one shape |
| Async boundaries | Absorb spikes ([[backpressure]]) |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Cascading timeouts | Caller timeout ≤ callee | Budget timeouts; circuit break |
| Duplicate side effects | Retries without idempotency | Keys / dedupe store |
| “Works in service A only” | Divergent error/auth | Align platform libraries |
| Latency cliff | Extra hop / chatty RPC | Batch; cache; merge calls |
| Deploy deadlock | Shared DB coupling | Split schemas; events |

## Gotchas

> [!WARNING]
> **Distributed monolith** — many repos, one shared DB = worst of both worlds.

> [!WARNING]
> **Retry storms** — without jitter/limits you DDoS yourself.

> [!WARNING]
> **Over-standardization** — one RPC stack everywhere can slow teams; enforce thin cross-cutting concerns only.

## When NOT to use

- **Throwaway prototypes** — ship; retrofit principles when retained.
- **Single small application** — modular monolith may beat microservices.
- **Vendor lock-in “platforms” that fight your contracts** — adapt principles, don’t cargo-cult tools.

## Related

[[orchestration]] [[API design]] [[SOLID]] [[backpressure]] [[event-driven]]
