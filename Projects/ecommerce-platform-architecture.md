[[Projects]] [[marketplace application]] [[gRPC]] [[Messaging/Kafka/Kafka distributed event streaming]] [[Payment gateway]] [[Terraform setup]] [[ecommerce-cicd-environments]] [[ecommerce-eks-layout]]

# ecommerce platform architecture

> ecommerce platform architecture — client ──► API Gateway (REST) ──► BFF (optional) ──► domain services

---

## How it works


```txt
Client ──► API Gateway (REST) ──► BFF (optional) ──► domain services
                              │
                    gRPC (sync, low-latency reads)
                    Kafka (async, facts + side effects)
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
   Order orchestrator   Payment / Refund    Catalog / Pricing
         │                    │                    │
         └────────────────────┴────────────────────┘
                              ▼
                    Notification (always async)
```

**Money and catalog are separate failure domains.** Never hold catalog locks while waiting on PSP. Emit facts after local commit (outbox), consume with idempotent handlers.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **ecommerce platform architecture** | This note’s core idea | “I explain ecommerce platform architecture in plain words.” |
| **idea** | What it is for | “One sentence, no jargon.” |
| **check** | How I verify | “I name the command or signal I look at.” |
| **fail** | How it breaks | “I name the top production failure.” |

---


## Configuration and commands

```bash
# version / help / dry-run when available
# keep env-specific values out of git
```

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Hotspot | metrics by key | Shard or cache |
| Cascade fail | timeouts | Bulkheads and backoff |
| Unclear ownership | diagram actors | Name the single writer |

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
> Prefer words you can say aloud in an interview.

---


## When not to use

- Skip when a simpler existing approach already fits.

---


## Related

[[Projects]] [[marketplace application]] [[gRPC]] [[Messaging/Kafka/Kafka distributed event streaming]] [[Payment gateway]] [[Terraform setup]] [[ecommerce-cicd-environments]] [[ecommerce-eks-layout]]

## Sources

- [Wikipedia — ecommerce-platform-architecture](https://en.wikipedia.org/wiki/ecommerce-platform-architecture)
