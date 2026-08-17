[[Architectures]] [[Clean Architecture]] [[Multi-tier and Layered Architecture]] [[feature flag]] [[Idempotent-key]]

# System Architecture

> System architecture is the map of boxes and arrows — services, data stores, and failure domains you run in prod.





## Interview Relevance
System architecture interviews map boxes, arrows, and failure domains — consistency, scale, and operability trade-offs.

## Sources
- [Google — SRE book](https://sre.google/sre-book/table-of-contents/) — deep-dive
- [AWS Well-Architected](https://aws.amazon.com/architecture/well-architected/) — overview

## Recall Cues
- Why do interviewers care about System architecture interviews map boxes, arrows, and failure domains — consistency, scale, and operability trade-offs?
- What is step 1: Actors & trust boundaries?
- What is step 2: Sync paths + timeouts?
- What is step 3: Async paths + DLQ?
- What is step 4: Data ownership per service?
- What is step 5: Blast radius on dependency loss?
- What mistake is **Pretty boxes ≠ operable system — without SLOs, runbooks, and ownership, architecture is a slide**?
- What mistake is **Shared database as “integration” — couples deploy cycles and schemas forever**?

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
- Pretty boxes ≠ operable system — without SLOs, runbooks, and ownership, architecture is a slide.
- Shared database as “integration” — couples deploy cycles and schemas forever.

## Pros/Cons or Trade-offs
- **Trade-off:** Prototype / spike — skip multi-service until the product question is answered.
- **Trade-off:** Single-team CRUD — modular monolith often beats premature microservices.
