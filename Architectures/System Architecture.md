[[Architectures]] [[Clean Architecture]] [[Multi-tier and Layered Architecture]] [[feature flag]] [[Idempotent-key]]

# System Architecture

> System architecture is the map of boxes and arrows — services, data stores, and failure domains you run in prod.

```txt
        System Architectur ──┬── Why it matters
               ├── Sources
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** System architecture reviews map boxes, arrows, and failure domains

## Sources
- [Google — SRE book](https://sre.google/sre-book/table-of-contents/) — deep-dive
- [AWS Well-Architected](https://aws.amazon.com/architecture/well-architected/) — overview

## Technical Details
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

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Cascading outage | Missing timeouts/bulkheads | Add limits; fail fast |
| Split brain | Two writers | Single writer or consensus |
| Hot dependency | One DB for everything | Split read models / shards |
| “Works in diagram” | No SLO / capacity | Load test critical path |

## Mistakes to Avoid
- **Mistake:** Pretty boxes ≠ operable system
- **Mistake:** Shared database as “integration”

## Pros/Cons or Trade-offs
- **Trade-off:** Prototype / spike — skip multi-service until the product question is answered.
- **Trade-off:** Single-team CRUD — modular monolith often beats premature microservices.
