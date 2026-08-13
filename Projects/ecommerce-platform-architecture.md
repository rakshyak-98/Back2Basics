<!-- note-strategy: decision -->
[[Projects]] [[marketplace application]] [[gRPC]] [[Messaging/Kafka/Kafka distributed event streaming]] [[Payment gateway]] [[Terraform setup]] [[ecommerce-cicd-environments]] [[ecommerce-eks-layout]]

# ecommerce platform architecture

> ecommerce platform architecture — client ──► API Gateway (REST) ──► BFF (optional) ──► domain services

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

**Say it in one breath:** ecommerce platform architecture — I can explain the job, the configuration, and the top failure without jargon.


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

## Standard config / commands

```bash
# version / help / dry-run when available
# keep env-specific values out of git
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Hotspot | metrics by key | Shard or cache |
| Cascade fail | timeouts | Bulkheads and backoff |
| Unclear ownership | diagram actors | Name the single writer |

---

## Gotchas

> [!WARNING]
> Prefer words you can say aloud in an interview.

---

## When NOT to use

- Skip when a simpler existing approach already fits.

---

## Alternatives considered

| Alternative | Why rejected |
|-------------|--------------|
| … | … |

## Related

[[Projects]] [[marketplace application]] [[gRPC]] [[Messaging/Kafka/Kafka distributed event streaming]] [[Payment gateway]] [[Terraform setup]] [[ecommerce-cicd-environments]] [[ecommerce-eks-layout]]
