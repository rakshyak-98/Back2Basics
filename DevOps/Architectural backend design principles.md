[[orchestration]] [[API design]] [[SOLID]] [[backpressure]] [[event-driven]] [[ecommerce-cicd-environments]]

# Architectural backend design principles

> Stable interfaces, clear module boundaries, and short data paths so backend services stay changeable under load and failure.

## Interview Relevance

Interviewers use backend design principles to see if you can defend modularity, contracts, timeouts/idempotency, and observability — and when a modular monolith beats a distributed tangle.

## Sources

- [Google SRE — Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/) — deep-dive
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) — overview
- [[SOLID]] · [[API design]] — overview

## Core Definition

Backend architecture principles are the recurring rules for how services expose contracts, move data, fail safely, and stay observable — so teams can change one part without breaking the rest.

## Key Concepts

- **Modularity / bounded contexts:** deploy independently when it pays off → avoid a distributed monolith sharing one database.
- **Interface contracts:** OpenAPI/proto + versioning → clients depend on stable shapes.
- **Data flow:** fewer hops; choose sync vs async on purpose ([[event-driven]], [[backpressure]]).
- **Failure policy:** timeouts, retries with jitter, idempotency keys on writes.
- **Observability:** trace id on every hop; shared SLIs (latency, errors, saturation).

## Technical Details

```txt
Client → Edge/API → Service A → (events|RPC) → Service B → DB
              │
         one error shape, one authentication story, one observability bag
```

| Principle | Practice |
|-----------|----------|
| **Modularity** | Bounded contexts; independent deploy when it pays |
| **Interface contracts** | OpenAPI/proto + versioning |
| **Data flow** | Prefer fewer hops; sync vs async on purpose |
| **Failure policy** | Timeouts, retries with jitter, idempotency |
| **Observability** | Trace id on every hop |

```yaml
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
[ ] Authentication/authorization matches platform
[ ] Timeouts < caller timeout
[ ] Idempotency keys on writes
[ ] Structured errors (code, message, trace)
[ ] SLIs: latency, error rate, saturation
```

| Knob | Why it matters |
|------|----------------|
| API versioning | Avoid silent breakages |
| Shared error envelope | Clients handle one shape |
| Async boundaries | Absorb spikes ([[backpressure]]) |

| Symptom | Check | Fix |
|---------|-------|-----|
| Cascading timeouts | Caller timeout ≤ callee | Budget timeouts; circuit break |
| Duplicate side effects | Retries without idempotency | Keys / dedupe store |
| Works in service A only | Divergent error/authentication libraries | Align platform libraries |
| Latency cliff | Extra hop / chatty RPC | Batch; cache; merge calls |
| Deploy deadlock | Shared DB coupling | Split schemas; events |

## Real-World Applications

An orders API publishes events for fulfillment instead of chaining five synchronous RPCs; writes carry idempotency keys so payment retries do not double-charge.

**Example:** Cascading timeouts during a partial outage — callers used timeouts longer than callees; budget timeouts so the outermost request fails first.

## Pros/Cons or Trade-offs

- **Pro:** Clear contracts and failure policy let teams ship independently with safer retries.
- **Con:** Over-standardization (one RPC stack everywhere) can slow teams — enforce thin cross-cutting concerns only.
- **Con:** Microservices without schema/ownership boundaries become a distributed monolith.

## Comparison

- vs [[SOLID]] at class level: these principles apply at service and platform boundaries.
- vs [[orchestration]]: orchestration sequences workflows; these principles shape how each service behaves inside them.
- vs throwaway prototype: ship first; retrofit when the code is retained.

## Mistakes to Avoid

- Many repositories sharing one database — worst of monolith and microservices.
- Retry storms without jitter and limits — you DDoS yourself.
- Ignoring timeout budgets across the call chain.
- Cargo-culting tools that fight your contracts instead of adapting the principles.
- Splitting into microservices when a modular monolith would be simpler for a small app.
